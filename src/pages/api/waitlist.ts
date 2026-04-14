import type { APIRoute } from 'astro'

export const prerender = false

const SYSTEME_BASE = 'https://api.systeme.io/api'
const TAG_NAME     = 'Lista de espera'

// ── Helpers ───────────────────────────────────────────────────────────────────

/** Busca el tagId por nombre */
async function findTagId(tagName: string, headers: Record<string, string>): Promise<number | null> {
  try {
    const res = await fetch(`${SYSTEME_BASE}/tags?itemsPerPage=100`, { headers })
    if (!res.ok) return null
    const data = await res.json().catch(() => null)
    const tags: any[] = data?.items ?? []
    const match = tags.find((t: any) => t.name?.toLowerCase() === tagName.toLowerCase())
    if (match) return match.id
    // Segunda página si hay más de 100
    if (tags.length === 100) {
      const res2 = await fetch(`${SYSTEME_BASE}/tags?itemsPerPage=100&page=2`, { headers })
      if (res2.ok) {
        const data2 = await res2.json().catch(() => null)
        const match2 = (data2?.items ?? []).find((t: any) => t.name?.toLowerCase() === tagName.toLowerCase())
        if (match2) return match2.id
      }
    }
  } catch (e) {
    console.error('[waitlist] findTagId error:', e)
  }
  return null
}

/** Construye el body para crear/actualizar un contacto en systeme.io
 *  Systeme.io usa:  surname (no lastName),  phone (no phoneNumber)
 */
function buildContactBody(
  firstName: string,
  lastName: string,
  phone: string,
  conociste: string,
  nivel: string
): Record<string, any> {
  const body: Record<string, any> = {}
  if (firstName) body.firstName = firstName
  if (lastName)  body.surname   = lastName   // ← campo correcto en systeme.io
  if (phone)     body.phone     = phone      // ← campo correcto en systeme.io

  // Campos personalizados
  const fields: { slug: string; value: string }[] = []
  if (conociste) fields.push({ slug: 'cmo_conociste_nawar', value: conociste })
  if (nivel)     fields.push({ slug: 'nivel_de_neerlands',  value: nivel })
  if (fields.length) body.fields = fields

  return body
}

/**
 * Crea el contacto si no existe.
 * Si ya existe, lo busca por email y lo actualiza (PATCH) con los datos nuevos.
 * Devuelve el contactId y si era duplicado.
 */
async function createOrUpdateContact(
  email: string,
  firstName: string,
  lastName: string,
  phone: string,
  conociste: string,
  nivel: string,
  headers: Record<string, string>
): Promise<{ contactId: number | null; isDuplicate: boolean }> {

  const contactData = buildContactBody(firstName, lastName, phone, conociste, nivel)

  // ── Intento de creación ───────────────────────────────────────────────────
  const createRes = await fetch(`${SYSTEME_BASE}/contacts`, {
    method: 'POST',
    headers,
    body: JSON.stringify({ email, ...contactData }),
  })

  if (createRes.ok) {
    const data = await createRes.json().catch(() => null)
    const contactId = data?.id ?? null
    console.log('[waitlist] contact created, id:', contactId)
    return { contactId, isDuplicate: false }
  }

  // ── Contacto ya existente o error ─────────────────────────────────────────
  const errText = await createRes.text()
  console.log('[waitlist] create response:', createRes.status, errText.slice(0, 200))

  const isDuplicate =
    createRes.status === 409 ||
    (createRes.status === 422 &&
      (errText.toLowerCase().includes('email') ||
       errText.toLowerCase().includes('utilizado') ||
       errText.toLowerCase().includes('already') ||
       errText.toLowerCase().includes('exist')))

  // ── Buscar el contacto por email ──────────────────────────────────────────
  const searchRes = await fetch(
    `${SYSTEME_BASE}/contacts?email=${encodeURIComponent(email)}`,
    { headers }
  )

  if (!searchRes.ok) {
    console.error('[waitlist] search error:', searchRes.status)
    return { contactId: null, isDuplicate }
  }

  const searchData = await searchRes.json().catch(() => null)
  const items = searchData?.items ?? searchData?.contacts ?? (Array.isArray(searchData) ? searchData : null)
  let contactId: number | null = null
  if (Array.isArray(items) && items.length > 0) {
    contactId = items[0]?.id ?? null
  } else if (searchData?.id) {
    contactId = searchData.id
  }

  if (!contactId) {
    console.error('[waitlist] could not find contact for:', email)
    return { contactId: null, isDuplicate }
  }

  console.log('[waitlist] found existing contact:', contactId, '— updating...')

  // ── Actualizar el contacto existente — PATCH (o PUT como fallback) ──────────
  // Solo enviamos campos informados para no machacar datos existentes.
  // Systeme.io: apellido = surname, teléfono = phone
  const updateBody: Record<string, any> = {}
  if (firstName) updateBody.firstName = firstName
  if (lastName)  updateBody.surname   = lastName   // ← surname, no lastName
  if (phone)     updateBody.phone     = phone      // ← phone, no phoneNumber

  const updateFields: { slug: string; value: string }[] = []
  if (conociste) updateFields.push({ slug: 'cmo_conociste_nawar', value: conociste })
  if (nivel)     updateFields.push({ slug: 'nivel_de_neerlands',  value: nivel })
  if (updateFields.length) updateBody.fields = updateFields

  console.log('[waitlist] updateBody:', JSON.stringify(updateBody))

  if (Object.keys(updateBody).length > 0) {
    // Intentar PATCH primero
    let updateRes = await fetch(`${SYSTEME_BASE}/contacts/${contactId}`, {
      method:  'PATCH',
      headers,
      body: JSON.stringify(updateBody),
    })

    // Si PATCH no funciona (405 Method Not Allowed), reintentar con PUT
    if (!updateRes.ok && updateRes.status === 405) {
      console.log('[waitlist] PATCH not allowed, retrying with PUT...')
      updateRes = await fetch(`${SYSTEME_BASE}/contacts/${contactId}`, {
        method:  'PUT',
        headers,
        body: JSON.stringify(updateBody),
      })
    }

    if (updateRes.ok) {
      console.log('[waitlist] contact updated successfully:', contactId)
    } else {
      const updateErr = await updateRes.text()
      console.error('[waitlist] update error:', updateRes.status, updateErr.slice(0, 300))
    }
  }

  return { contactId, isDuplicate: true }
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
    if (!apiKey) return json({ error: 'API key no configurada' }, 500)

    const headers = {
      'X-API-Key':    apiKey,
      'Content-Type': 'application/json',
      'accept':       'application/json',
    }

    // ── Crear/actualizar contacto + buscar tag en paralelo ────────────────────
    const [{ contactId, isDuplicate }, tagId] = await Promise.all([
      createOrUpdateContact(email, firstName, lastName, phone, conociste, nivel, headers),
      findTagId(tagName, headers),
    ])

    if (!contactId) {
      console.error('[waitlist] no contactId for:', email)
      return json({ error: 'No se pudo registrar el email. Por favor inténtalo de nuevo.' }, 400)
    }

    // ── Añadir etiqueta ───────────────────────────────────────────────────────
    if (tagId) {
      const tagAddRes = await fetch(`${SYSTEME_BASE}/contacts/${contactId}/tags`, {
        method:  'POST',
        headers,
        body: JSON.stringify({ tagId }),
      })
      if (!tagAddRes.ok) {
        const err = await tagAddRes.text()
        // 409 significa que ya tiene la etiqueta, no es error real
        if (tagAddRes.status !== 409) {
          console.error('[waitlist] tag add error:', tagAddRes.status, err)
        }
      } else {
        console.log('[waitlist] tag', tagName, 'added to contact', contactId)
      }
    } else {
      console.error('[waitlist] tag not found in systeme.io:', tagName)
    }

    return json({
      success: true,
      message: isDuplicate
        ? 'Ya estabas en la lista — hemos actualizado tus datos.'
        : '¡Registrado con éxito! Te avisamos en cuanto abramos plazas.',
    })

  } catch (e) {
    console.error('[waitlist] exception:', e)
    return json({ error: 'Error del servidor. Por favor inténtalo de nuevo.' }, 500)
  }
}

function json(data: object, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json' },
  })
}
