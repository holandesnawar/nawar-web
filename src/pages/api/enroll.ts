import type { APIRoute } from 'astro'

export const prerender = false

// Backend de la academia que crea la sesión de pago de Stripe y devuelve { checkout_url }.
const ACADEMIA_ENROLL_URL = 'https://academia.holandesnawar.nl/api/v1/payments/enroll'

// systeme.io — CRM centralizado (mismo que usa la lista de espera).
const SYSTEME_BASE = 'https://api.systeme.io/api'
// ID de la etiqueta "Matriculado sin pagar" en systeme.io (para reenganche).
// Cableado por ID en vez de por nombre: es más fiable y no depende de que el texto coincida.
const TAG_ID_SIN_PAGAR = 2033154

// ── systeme.io helpers (mismo patrón que waitlist.ts) ──────────────────────────

// Crea o encuentra el contacto, actualiza sus datos y le añade el tag de reenganche.
// Nunca lanza: el CRM no debe bloquear el pago.
async function syncToCRM(
  lead: {
    email: string
    firstName: string
    lastName: string
    phone: string
    country: string
    city: string
  },
  headers: Record<string, string>
): Promise<void> {
  try {
    const body: Record<string, any> = { email: lead.email }
    if (lead.firstName) body.firstName = lead.firstName
    if (lead.lastName)  body.surname   = lead.lastName
    if (lead.phone)     body.phone     = lead.phone
    const fields: { slug: string; value: string }[] = []
    if (lead.country) fields.push({ slug: 'country', value: lead.country })
    if (lead.city)    fields.push({ slug: 'city',    value: lead.city })
    if (fields.length) body.fields = fields

    const createRes = await fetch(`${SYSTEME_BASE}/contacts`, {
      method: 'POST', headers, body: JSON.stringify(body),
    })

    let contactId: number | null = null

    if (createRes.ok) {
      const data = await createRes.json().catch(() => null)
      contactId = data?.id ?? null
      console.log('[enroll] contact created:', contactId)
    } else {
      console.log('[enroll] create failed:', createRes.status, '— buscando contacto existente')
      // Ya existía: buscarlo y actualizar sus datos.
      const searchRes = await fetch(
        `${SYSTEME_BASE}/contacts?email=${encodeURIComponent(lead.email)}`,
        { headers }
      )
      if (searchRes.ok) {
        const sd = await searchRes.json().catch(() => null)
        const items = sd?.items ?? sd?.contacts ?? (Array.isArray(sd) ? sd : null)
        if (Array.isArray(items) && items.length > 0) contactId = items[0]?.id ?? null
        else if (sd?.id) contactId = sd.id

        if (contactId) {
          const upd: Record<string, any> = {}
          if (lead.firstName) upd.firstName = lead.firstName
          if (lead.lastName)  upd.surname   = lead.lastName
          if (lead.phone)     upd.phone     = lead.phone
          const updFields: { slug: string; value: string }[] = []
          if (lead.country) updFields.push({ slug: 'country', value: lead.country })
          if (lead.city)    updFields.push({ slug: 'city',    value: lead.city })
          if (updFields.length) upd.fields = updFields
          if (Object.keys(upd).length > 0) {
            let pr = await fetch(`${SYSTEME_BASE}/contacts/${contactId}`, {
              method: 'PATCH', headers, body: JSON.stringify(upd),
            })
            if (!pr.ok && pr.status === 405) {
              pr = await fetch(`${SYSTEME_BASE}/contacts/${contactId}`, {
                method: 'PUT', headers, body: JSON.stringify(upd),
              })
            }
            if (pr.ok) console.log('[enroll] contact updated:', contactId)
            else console.error('[enroll] update error:', pr.status)
          }
        }
      }
    }

    // Añadir el tag de reenganche por su ID (más fiable que buscar por nombre).
    if (contactId) {
      const tr = await fetch(`${SYSTEME_BASE}/contacts/${contactId}/tags`, {
        method: 'POST', headers, body: JSON.stringify({ tagId: TAG_ID_SIN_PAGAR }),
      })
      if (tr.ok) console.log('[enroll] tag', TAG_ID_SIN_PAGAR, 'added to', contactId)
      else if (tr.status !== 409) console.error('[enroll] tag error:', tr.status)
    } else {
      console.error('[enroll] no contactId for:', lead.email)
    }
  } catch (e) {
    console.error('[enroll] syncToCRM error:', e)
  }
}

// ── Route handler ──────────────────────────────────────────────────────────────

export const POST: APIRoute = async ({ request }) => {
  const body = await request.json().catch(() => null)

  const email     = (body?.email      ?? '').toString().trim().toLowerCase()
  const firstName = (body?.first_name ?? '').toString().trim()
  const lastName  = (body?.last_name  ?? '').toString().trim()
  const phone     = (body?.phone      ?? '').toString().trim()
  const country   = (body?.country    ?? '').toString().trim()
  const city      = (body?.city       ?? '').toString().trim()

  // ── Honeypot anti-bot ──
  const honeypot = (body?.website ?? '').toString().trim()
  if (honeypot) {
    console.log('[enroll] honeypot triggered, ignoring submission from:', email)
    return json({ detail: 'No se pudo crear la matrícula.' }, 400)
  }

  if (!email || !email.includes('@') || !firstName || !lastName) {
    return json({ detail: 'Faltan datos obligatorios.' }, 400)
  }

  // ── 1) systeme.io (no bloqueante): guardamos el lead aunque el pago falle ──
  const apiKey =
    (import.meta.env.SYSTEME_API_KEY as string | undefined) ||
    (typeof process !== 'undefined' ? process.env.SYSTEME_API_KEY : undefined)

  if (apiKey) {
    const headers = {
      'X-API-Key':    apiKey,
      'Content-Type': 'application/json',
      accept:         'application/json',
    }
    // await para que Vercel no mate la promesa; los errores nunca bloquean el pago.
    await syncToCRM({ email, firstName, lastName, phone, country, city }, headers)
  } else {
    console.warn('[enroll] SYSTEME_API_KEY not set — skipping CRM sync for:', email)
  }

  // ── 2) Crear la sesión de pago en la academia y devolver checkout_url ──
  try {
    const res = await fetch(ACADEMIA_ENROLL_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        accept: 'application/json',
      },
      body: JSON.stringify({
        email,
        first_name: firstName,
        last_name: lastName,
        phone,
        country,
        city,
      }),
    })

    const data = await res.json().catch(() => null)

    if (!res.ok) {
      const detail =
        (data && (data.detail || data.message)) ||
        'No se pudo crear la matrícula. Vuelve a intentarlo en un momento.'
      console.error('[enroll] academia error:', res.status, JSON.stringify(data).slice(0, 200))
      return json({ detail }, 502)
    }

    const checkoutUrl = data?.checkout_url ?? data?.checkoutUrl ?? data?.url ?? null
    if (!checkoutUrl) {
      console.error('[enroll] academia ok pero sin checkout_url:', JSON.stringify(data).slice(0, 200))
      return json(
        { detail: 'No se pudo iniciar el pago. Vuelve a intentarlo en un momento.' },
        502
      )
    }

    return json({ checkout_url: checkoutUrl })
  } catch (e) {
    console.error('[enroll] academia request failed:', e)
    return json(
      { detail: 'Hubo un problema al conectar con el pago. Vuelve a intentarlo en un momento.' },
      502
    )
  }
}

function json(data: object, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json' },
  })
}
