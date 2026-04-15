import type { APIRoute } from 'astro'

export const prerender = false

const SYSTEME_BASE = 'https://api.systeme.io/api'
const TAG_NAME     = 'Lista de espera'

// ── Helpers ───────────────────────────────────────────────────────────────────

async function findTagId(tagName: string, headers: Record<string, string>): Promise<number | null> {
  try {
    const res = await fetch(`${SYSTEME_BASE}/tags?itemsPerPage=100`, { headers })
    if (!res.ok) return null
    const data = await res.json().catch(() => null)
    const tags: any[] = data?.items ?? []
    const match = tags.find((t: any) => t.name?.toLowerCase() === tagName.toLowerCase())
    if (match) return match.id
    if (tags.length === 100) {
      const res2 = await fetch(`${SYSTEME_BASE}/tags?itemsPerPage=100&page=2`, { headers })
      if (res2.ok) {
        const data2 = await res2.json().catch(() => null)
        const m2 = (data2?.items ?? []).find((t: any) => t.name?.toLowerCase() === tagName.toLowerCase())
        if (m2) return m2.id
      }
    }
  } catch (e) {
    console.error('[waitlist] findTagId error:', e)
  }
  return null
}

async function createOrUpdateContact(
  email: string,
  firstName: string,
  lastName: string,
  phone: string,
  conociste: string,
  nivel: string,
  headers: Record<string, string>
): Promise<{ contactId: number | null; isDuplicate: boolean }> {
  try {
    const body: Record<string, any> = { email }
    if (firstName) body.firstName = firstName
    if (lastName)  body.surname   = lastName
    if (phone)     body.phone     = phone
    const fields: { slug: string; value: string }[] = []
    if (conociste) fields.push({ slug: 'cmo_conociste_nawar', value: conociste })
    if (nivel)     fields.push({ slug: 'nivel_de_neerlands',  value: nivel })
    if (fields.length) body.fields = fields

    // Intento crear contacto
    const createRes = await fetch(`${SYSTEME_BASE}/contacts`, {
      method: 'POST', headers, body: JSON.stringify(body),
    })

    if (createRes.ok) {
      const data = await createRes.json().catch(() => null)
      const contactId = data?.id ?? null
      console.log('[waitlist] contact created:', contactId)
      return { contactId, isDuplicate: false }
    }

    const errText = await createRes.text()
    console.log('[waitlist] create response:', createRes.status, errText.slice(0, 200))

    // Buscar contacto existente (cualquier error de creación)
    const searchRes = await fetch(
      `${SYSTEME_BASE}/contacts?email=${encodeURIComponent(email)}`,
      { headers }
    )

    if (searchRes.ok) {
      const searchData = await searchRes.json().catch(() => null)
      const items = searchData?.items ?? searchData?.contacts ?? (Array.isArray(searchData) ? searchData : null)
      let contactId: number | null = null
      if (Array.isArray(items) && items.length > 0) contactId = items[0]?.id ?? null
      else if (searchData?.id) contactId = searchData.id

      if (contactId) {
        console.log('[waitlist] found existing contact:', contactId, '— updating...')

        // PATCH con los datos nuevos
        const updateBody: Record<string, any> = {}
        if (firstName) updateBody.firstName = firstName
        if (lastName)  updateBody.surname   = lastName
        if (phone)     updateBody.phone     = phone
        const updateFields: { slug: string; value: string }[] = []
        if (conociste) updateFields.push({ slug: 'cmo_conociste_nawar', value: conociste })
        if (nivel)     updateFields.push({ slug: 'nivel_de_neerlands',  value: nivel })
        if (updateFields.length) updateBody.fields = updateFields

        if (Object.keys(updateBody).length > 0) {
          let patchRes = await fetch(`${SYSTEME_BASE}/contacts/${contactId}`, {
            method: 'PATCH', headers, body: JSON.stringify(updateBody),
          })
          if (!patchRes.ok && patchRes.status === 405) {
            patchRes = await fetch(`${SYSTEME_BASE}/contacts/${contactId}`, {
              method: 'PUT', headers, body: JSON.stringify(updateBody),
            })
          }
          if (patchRes.ok) console.log('[waitlist] contact updated:', contactId)
          else console.error('[waitlist] update error:', patchRes.status)
        }

        return { contactId, isDuplicate: true }
      }
    }

    console.error('[waitlist] could not find contact for:', email)
    return { contactId: null, isDuplicate: false }

  } catch (e) {
    console.error('[waitlist] createOrUpdate exception:', e)
    return { contactId: null, isDuplicate: false }
  }
}

// ── Route handler ─────────────────────────────────────────────────────────────

export const POST: APIRoute = async ({ request }) => {
  try {
    const body      = await request.json().catch(() => null)
    const email     = (body?.email     ?? '').trim()
    const firstName = (body?.firstName ?? body?.name ?? '').trim()
    const lastName  = (body?.lastName  ?? '').trim()
    const phone     = (body?.phone     ?? '').trim()
    const conociste = (body?.conociste ?? '').trim()
    const nivel     = (body?.nivel     ?? '').trim()
    const tagName   =
      typeof body?.tagName === 'string' && body.tagName.trim()
        ? body.tagName.trim()
        : TAG_NAME

    if (!email || !email.includes('@')) {
      return json({ error: 'Email inválido' }, 400)
    }

    const apiKey = import.meta.env.SYSTEME_API_KEY
    if (!apiKey) {
      console.error('[waitlist] SYSTEME_API_KEY no configurada')
      // Devolver éxito igualmente — el usuario no debe ver este error
      return json({ success: true, message: '¡Registrado! Te avisamos en cuanto abramos plazas.' })
    }

    const headers = {
      'X-API-Key':    apiKey,
      'Content-Type': 'application/json',
      'accept':       'application/json',
    }

    // Crear/actualizar contacto y buscar tag en paralelo
    // Si Systeme.io falla, seguimos adelante y mostramos éxito igualmente
    const [{ contactId, isDuplicate }, tagId] = await Promise.all([
      createOrUpdateContact(email, firstName, lastName, phone, conociste, nivel, headers),
      findTagId(tagName, headers),
    ])

    // Intentar añadir etiqueta solo si tenemos contactId
    if (contactId && tagId) {
      try {
        const tagRes = await fetch(`${SYSTEME_BASE}/contacts/${contactId}/tags`, {
          method: 'POST', headers, body: JSON.stringify({ tagId }),
        })
        if (tagRes.ok) {
          console.log('[waitlist] tag', tagName, 'added to', contactId)
        } else if (tagRes.status !== 409) {
          console.error('[waitlist] tag error:', tagRes.status)
        }
      } catch (e) {
        console.error('[waitlist] tag exception:', e)
      }
    } else {
      if (!contactId) console.error('[waitlist] no contactId — tag not added for:', email)
      if (!tagId)     console.error('[waitlist] tag not found in systeme:', tagName)
    }

    // Siempre éxito al usuario — los errores de CRM son internos
    return json({
      success: true,
      message: isDuplicate
        ? 'Ya estabas en la lista — hemos actualizado tus datos.'
        : '¡Registrado con éxito! Te avisamos en cuanto abramos plazas.',
    })

  } catch (e) {
    console.error('[waitlist] exception:', e)
    // Incluso en excepción inesperada, devolver éxito
    return json({ success: true, message: '¡Registrado! Te avisamos pronto.' })
  }
}

function json(data: object, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json' },
  })
}
