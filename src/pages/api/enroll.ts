import type { APIRoute } from 'astro'
import { getEstadoPlazas, MENSAJE_CERRADO } from '../../lib/plazas'
import { ESCUELA_URL } from '../../lib/escuela'

export const prerender = false

// Backend de la academia: crea un PaymentIntent y devuelve la URL de NUESTRO
// checkout embebido (Stripe Elements dentro de la academia), no el de Stripe.
// payment_url = app.holandesnawar.com/auth/matricula-formacion-nawar-a0-a1?ei=&cs=&pk=
// Esa URL la construye la academia con su propia variable de dominio, así que
// viene sola con el host correcto; aquí sólo mandamos la petición.
// La academia debe servir la rama que tiene este endpoint (adoring-dijkstra).
//
// A mano y no confiando en el redirect del dominio viejo: esto es un POST, y
// un POST contra un 301 se reenvía como GET, así que la matrícula llegaría
// vacía al otro lado en vez de fallar limpio.
const ACADEMIA_ENROLL_URL = `${ESCUELA_URL}/api/v1/payments/enroll-intent`

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
  // ── Puerta 3: red de seguridad ──
  // Para quien tuviera el formulario ya abierto en el móvil cuando cerramos.
  // Va lo primero, antes de tocar systeme.io o la academia: con las puertas
  // cerradas no se crea contacto ni se pide PaymentIntent.
  const plazas = await getEstadoPlazas()
  if (!plazas.abierta) {
    console.log('[enroll] matrícula cerrada, rechazando')
    return json({ detail: MENSAJE_CERRADO }, 403)
  }

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

  // ── 2) Crear el PaymentIntent en la academia y devolver payment_url ──
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

    const paymentUrl = data?.payment_url ?? data?.paymentUrl ?? data?.checkout_url ?? data?.url ?? null
    if (!paymentUrl) {
      console.error('[enroll] academia ok pero sin payment_url:', JSON.stringify(data).slice(0, 200))
      return json(
        { detail: 'No se pudo iniciar el pago. Vuelve a intentarlo en un momento.' },
        502
      )
    }

    // El front (matricula) lee `payment_url` y redirige a nuestro checkout embebido.
    return json({ payment_url: paymentUrl })
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
