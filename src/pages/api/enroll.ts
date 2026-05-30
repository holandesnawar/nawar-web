import type { APIRoute } from 'astro'

export const prerender = false

// Backend de la academia que crea la sesión de pago de Stripe y devuelve { checkout_url }.
const ACADEMIA_ENROLL_URL = 'https://academia.holandesnawar.nl/api/v1/payments/enroll'

// Brevo (Sendinblue) — guardamos el lead antes de pagar para poder reengancharlo.
const BREVO_BASE = 'https://api.brevo.com/v3'

// ── Brevo: guardar/actualizar el lead (no bloquea el pago) ─────────────────────

async function syncToBrevo(
  lead: {
    email: string
    firstName: string
    lastName: string
    phone: string
    country: string
    city: string
  },
  apiKey: string,
  listId: string
): Promise<void> {
  try {
    const attributes: Record<string, string> = {}
    if (lead.firstName) attributes.FIRSTNAME = lead.firstName
    if (lead.lastName)  attributes.LASTNAME  = lead.lastName
    if (lead.phone)     attributes.SMS       = lead.phone
    if (lead.country)   attributes.COUNTRY   = lead.country
    if (lead.city)      attributes.CITY      = lead.city
    // Estado para campañas de reenganche de quienes no completan el pago.
    attributes.ESTADO = 'matriculado-sin-pagar'

    const body: Record<string, unknown> = {
      email: lead.email,
      attributes,
      updateEnabled: true,
    }
    const listIdNum = Number(listId)
    if (Number.isFinite(listIdNum) && listIdNum > 0) {
      body.listIds = [listIdNum]
    }

    const res = await fetch(`${BREVO_BASE}/contacts`, {
      method: 'POST',
      headers: {
        'api-key': apiKey,
        'Content-Type': 'application/json',
        accept: 'application/json',
      },
      body: JSON.stringify(body),
    })

    if (res.ok || res.status === 204) {
      console.log('[enroll] brevo contact upserted:', lead.email)
    } else {
      const txt = await res.text().catch(() => '')
      console.error('[enroll] brevo error:', res.status, txt.slice(0, 200))
    }
  } catch (e) {
    console.error('[enroll] syncToBrevo error:', e)
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

  // ── 1) Brevo (no bloqueante): guardamos el lead aunque el pago falle ──
  const brevoKey =
    (import.meta.env.BREVO_API_KEY as string | undefined) ||
    (typeof process !== 'undefined' ? process.env.BREVO_API_KEY : undefined)
  const brevoListId =
    (import.meta.env.BREVO_LIST_ID as string | undefined) ||
    (typeof process !== 'undefined' ? process.env.BREVO_LIST_ID : undefined)

  if (brevoKey) {
    // await para que Vercel no mate la promesa, pero los errores nunca bloquean el pago.
    await syncToBrevo(
      { email, firstName, lastName, phone, country, city },
      brevoKey,
      brevoListId ?? ''
    )
  } else {
    console.warn('[enroll] BREVO_API_KEY not set — skipping CRM sync for:', email)
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
