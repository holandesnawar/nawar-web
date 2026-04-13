import type { APIRoute } from 'astro'

export const prerender = false

const SYSTEME_BASE = 'https://api.systeme.io/api'
const TAG_NAME     = 'Lista de espera'

export const POST: APIRoute = async ({ request }) => {
  try {
    const body  = await request.json().catch(() => null)
    const email = body?.email?.trim()
    const tagName =
      typeof body?.tagName === 'string' && body.tagName.trim()
        ? body.tagName.trim()
        : TAG_NAME

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
    let isDuplicate = false

    const createRes = await fetch(`${SYSTEME_BASE}/contacts`, {
      method:  'POST',
      headers,
      body: JSON.stringify({ email }),
    })

    if (createRes.ok) {
      // 201 — contacto nuevo, el body trae el objeto con el id
      const data = await createRes.json().catch(() => null)
      contactId  = data?.id ?? null
    } else {
      const errText = await createRes.text()
      isDuplicate = createRes.status === 409 || (createRes.status === 422 && errText.includes('utilizado'))
      
      if (isDuplicate) {
        // Contacto ya existe → búscalo por email
        const searchRes = await fetch(
          `${SYSTEME_BASE}/contacts?email=${encodeURIComponent(email)}`,
          { headers }
        )
        if (searchRes.ok) {
          const data = await searchRes.json().catch(() => null)
          console.log('[waitlist] search results:', data)
          const items = data?.items ?? (Array.isArray(data) ? data : (data?.contacts ?? null))
          contactId   = Array.isArray(items) ? (items[0]?.id ?? null) : (data?.id ?? null)
          console.log('[waitlist] extracted contactId from duplicate:', contactId)
        }
      } else {
        console.error('[waitlist] create error:', createRes.status, errText)
        // Intentar parsear el json para dar un mensaje de error más útil
        try {
          const errData = JSON.parse(errText)
          if (errData?.detail) {
            return json({ error: errData.detail }, 400)
          }
        } catch(e) {}
        return json({ error: 'Error al registrar el email' }, 500)
      }
    }

    if (!contactId) {
      console.error('[waitlist] no se pudo obtener el contactId para', email)
      return json({ error: 'No se pudo obtener el contacto, tal vez el email es inválido' }, 400)
    }

    // ── Paso 2: buscar el tagId y añadir la etiqueta ──────────────────────
    let tagId: number | null = null;
    const tagsRes = await fetch(`${SYSTEME_BASE}/tags`, { headers });
    if (tagsRes.ok) {
      const tagsData = await tagsRes.json().catch(() => null);
      const tags = tagsData?.items || [];
      const foundTag = tags.find((t: any) => t.name.toLowerCase() === tagName.toLowerCase());
      if (foundTag) {
        tagId = foundTag.id;
      }
    }

    if (tagId) {
      const tagAddRes = await fetch(`${SYSTEME_BASE}/contacts/${contactId}/tags`, {
        method:  'POST',
        headers,
        body: JSON.stringify({ tagId }),
      })

      if (!tagAddRes.ok) {
        const err = await tagAddRes.text()
        console.error('[waitlist] tag error:', tagAddRes.status, err)
        // Devolvemos éxito igualmente — el contacto fue creado
      }
    } else {
      console.error('[waitlist] tag error: No se encontró la etiqueta con nombre', tagName)
    }

    return json({ success: true, message: isDuplicate ? "Ya estabas en la lista, pero hemos actualizado tu etiqueta." : "Registrado con éxito." })

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
