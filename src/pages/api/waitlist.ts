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

type SyncDebug = {
  createStatus?: number
  createBody?: string
  contactId?: number | null
  tagId?: number | null
  tagStatus?: number
  searchStatus?: number
  searchBody?: string
  error?: string
}

async function syncToCRM(
  email: string,
  firstName: string,
  lastName: string,
  phone: string,
  conociste: string,
  nivel: string,
  tagName: string,
  headers: Record<string, string>,
  debug: SyncDebug
): Promise<void> {
  try {
    const body: Record<string, any> = { email }
    if (firstName) body.firstName = firstName
    if (lastName)  body.surname   = lastName
    if (phone)     body.phone     = phone
    const fields: { slug: string; value: string }[] = []
    if (conociste) fields.push({ slug: 'cmo_conociste_nawar', value: conociste })
    if (nivel)     fields.push({ slug: 'nivel_de_neerlands',  value: nivel })
    if (fields.length) body.fields = fields

    // Crear o encontrar contacto y buscar tag en paralelo
    const [createRes, tagId] = await Promise.all([
      fetch(`${SYSTEME_BASE}/contacts`, { method: 'POST', headers, body: JSON.stringify(body) }),
      findTagId(tagName, headers),
    ])
    debug.createStatus = createRes.status
    debug.tagId = tagId

    let contactId: number | null = null

    if (createRes.ok) {
      const data = await createRes.json().catch(() => null)
      contactId = data?.id ?? null
      console.log('[waitlist] contact created:', contactId)
    } else {
      const errText = await createRes.text()
      debug.createBody = errText.slice(0, 200)
      console.log('[waitlist] create failed:', createRes.status, errText.slice(0, 150))

      // Buscar el contacto existente
      const searchRes = await fetch(
        `${SYSTEME_BASE}/contacts?email=${encodeURIComponent(email)}`,
        { headers }
      )
      debug.searchStatus = searchRes.status
      if (searchRes.ok) {
        const sd = await searchRes.json().catch(() => null)
        debug.searchBody = JSON.stringify(sd).slice(0, 200)
        const items = sd?.items ?? sd?.contacts ?? (Array.isArray(sd) ? sd : null)
        if (Array.isArray(items) && items.length > 0) contactId = items[0]?.id ?? null
        else if (sd?.id) contactId = sd.id

        if (contactId) {
          console.log('[waitlist] found existing contact:', contactId, '— updating...')
          // Actualizar datos
          const upd: Record<string, any> = {}
          if (firstName) upd.firstName = firstName
          if (lastName)  upd.surname   = lastName
          if (phone)     upd.phone     = phone
          const updFields: { slug: string; value: string }[] = []
          if (conociste) updFields.push({ slug: 'cmo_conociste_nawar', value: conociste })
          if (nivel)     updFields.push({ slug: 'nivel_de_neerlands',  value: nivel })
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
            if (pr.ok) console.log('[waitlist] contact updated:', contactId)
            else console.error('[waitlist] update error:', pr.status)
          }
        }
      }
    }

    debug.contactId = contactId

    // Añadir etiqueta
    if (contactId && tagId) {
      const tr = await fetch(`${SYSTEME_BASE}/contacts/${contactId}/tags`, {
        method: 'POST', headers, body: JSON.stringify({ tagId }),
      })
      debug.tagStatus = tr.status
      if (tr.ok) console.log('[waitlist] tag added:', tagName, 'to', contactId)
      else if (tr.status !== 409) console.error('[waitlist] tag error:', tr.status)
    } else {
      if (!contactId) console.error('[waitlist] no contactId for:', email)
      if (!tagId)     console.error('[waitlist] tag not found:', tagName)
    }
  } catch (e) {
    debug.error = (e as Error).message
    console.error('[waitlist] syncToCRM error:', e)
  }
}

// ── Route handler ─────────────────────────────────────────────────────────────

export const POST: APIRoute = async ({ request }) => {
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

  // Única validación que bloquea: email inválido
  if (!email || !email.includes('@')) {
    return json({ error: 'Email inválido' }, 400)
  }

  // Doble acceso: import.meta.env (dev) + process.env (serverless Vercel)
  const apiKey =
    (import.meta.env.SYSTEME_API_KEY as string | undefined) ||
    (typeof process !== 'undefined' ? process.env.SYSTEME_API_KEY : undefined)

  console.log('[waitlist] received:', { email, tagName, hasKey: !!apiKey })

  const debug: SyncDebug = {}
  if (apiKey) {
    const headers = {
      'X-API-Key':    apiKey,
      'Content-Type': 'application/json',
      'accept':       'application/json',
    }
    try {
      await syncToCRM(email, firstName, lastName, phone, conociste, nivel, tagName, headers, debug)
    } catch (e) {
      debug.error = (e as Error).message
      console.error('[waitlist] sync failed:', e)
    }
  } else {
    debug.error = 'SYSTEME_API_KEY not set'
    console.error('[waitlist] SYSTEME_API_KEY not set — skipping CRM sync for:', email)
  }

  // ?debug=1 → devuelve info de Systeme para diagnosticar
  const url = new URL(request.url)
  if (url.searchParams.get('debug') === '1') {
    return json({
      success: true,
      message: '¡Registrado con éxito! Te avisamos en cuanto abramos plazas.',
      debug,
    })
  }

  return json({
    success: true,
    message: '¡Registrado con éxito! Te avisamos en cuanto abramos plazas.',
  })
}

function json(data: object, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json' },
  })
}
