import type { APIRoute } from 'astro'

export const prerender = false

const SYSTEME_BASE = 'https://api.systeme.io/api'
const TAG_NAME     = 'Lista de espera'

export const POST: APIRoute = async ({ request }) => {
  try {
    const body  = await request.json().catch(() => null)
    const email = body?.email?.trim()

    if (!email || !email.includes('@')) {
      return json({ error: 'Email inválido' }, 400)
    }

    const apiKey = import.meta.env.SYSTEME_API_KEY
    if (!apiKey) return json({ error: 'API key no configurada' }, 500)

    const headers = {
      'X-API-Key':    apiKey,
      'Content-Type': 'application/json',
      'accept':       'application/json',
    }

    // ── Paso 1: crear o encontrar el contacto ──────────────────────────────
    let contactId: number | null = null

    const createRes = await fetch(`${SYSTEME_BASE}/contacts`, {
      method:  'POST',
      headers,
      body: JSON.stringify({ email }),
    })

    if (createRes.ok) {
      // 201 — contacto nuevo, el body trae el objeto con el id
      const data = await createRes.json().catch(() => null)
      contactId  = data?.id ?? null
    } else if (createRes.status === 409) {
      // Contacto ya existe → búscalo por email
      const searchRes = await fetch(
        `${SYSTEME_BASE}/contacts?email=${encodeURIComponent(email)}`,
        { headers }
      )
      if (searchRes.ok) {
        const data = await searchRes.json().catch(() => null)
        // La API devuelve { items: [...] } o directamente el array
        const items = data?.items ?? data
        contactId   = Array.isArray(items) ? (items[0]?.id ?? null) : null
      }
    } else {
      const err = await createRes.text()
      console.error('[waitlist] create error:', createRes.status, err)
      return json({ error: 'Error al registrar el email' }, 500)
    }

    if (!contactId) {
      console.error('[waitlist] no se pudo obtener el contactId para', email)
      return json({ error: 'No se pudo obtener el contacto' }, 500)
    }

    // ── Paso 2: añadir la etiqueta ────────────────────────────────────────
    const tagRes = await fetch(`${SYSTEME_BASE}/contacts/${contactId}/tags`, {
      method:  'POST',
      headers,
      body: JSON.stringify({ name: TAG_NAME }),
    })

    if (!tagRes.ok) {
      const err = await tagRes.text()
      console.error('[waitlist] tag error:', tagRes.status, err)
      // Devolvemos éxito igualmente — el contacto fue creado
    }

    return json({ success: true })

  } catch (e) {
    console.error('[waitlist] exception:', e)
    return json({ error: 'Error del servidor' }, 500)
  }
}

function json(data: object, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json' },
  })
}
