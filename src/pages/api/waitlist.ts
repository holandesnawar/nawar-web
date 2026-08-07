import type { APIRoute } from 'astro'

export const prerender = false

const SYSTEME_BASE = 'https://api.systeme.io/api'
const TAG_NAME     = 'Lista de espera'

/**
 * Id de la etiqueta "Lista de espera" en systeme.io.
 *
 * Se pone a mano (sale en la URL de la etiqueta en el panel de systeme) porque
 * buscarla por NOMBRE es frágil: basta con que systeme cambie el formato de su
 * listado, lo pagine distinto o limite `itemsPerPage` para que deje de
 * encontrarse — y entonces el contacto se crea pero se queda SIN etiquetar, que
 * es justo lo que pasó. El endpoint de matrícula (enroll.ts) ya usa ids fijos y
 * por eso nunca ha fallado.
 *
 * Se puede sobreescribir con la variable de entorno SYSTEME_WAITLIST_TAG_ID.
 */
const TAG_ID_LISTA_ESPERA = 0 // 0 = sin configurar → se busca por nombre

/** Lee una variable de entorno tanto en desarrollo como en Vercel. */
function env(name: string): string | undefined {
  return (
    ((import.meta as any).env?.[name] as string | undefined) ||
    (typeof process !== 'undefined' ? process.env[name] : undefined)
  )
}

/** Compara nombres de etiqueta sin que estorben acentos raros ni espacios. */
function normalizeName(value: unknown): string {
  return String(value ?? '')
    .normalize('NFC')
    .replace(/\s+/g, ' ')
    .trim()
    .toLowerCase()
}

// ── Helpers ───────────────────────────────────────────────────────────────────

async function findTagId(
  tagName: string,
  headers: Record<string, string>,
  debug: SyncDebug
): Promise<number | null> {
  // 1) El id configurado manda: ni una llamada de más, ni nada que se rompa.
  const fromEnv = Number(env('SYSTEME_WAITLIST_TAG_ID') ?? '')
  const fixedId = Number.isFinite(fromEnv) && fromEnv > 0 ? fromEnv : TAG_ID_LISTA_ESPERA
  if (fixedId > 0) return fixedId

  // 2) Respaldo: buscarla por nombre, paginando de verdad y dejando dicho en
  //    los logs QUÉ ha fallado (antes se devolvía null en silencio).
  const target = normalizeName(tagName)
  const seen: string[] = []
  try {
    for (let page = 1; page <= 5; page++) {
      const res = await fetch(`${SYSTEME_BASE}/tags?itemsPerPage=50&page=${page}`, { headers })
      if (!res.ok) {
        const body = await res.text().catch(() => '')
        debug.tagLookupStatus = res.status
        debug.tagLookupBody = body.slice(0, 200)
        console.error('[waitlist] listado de etiquetas falló:', res.status, body.slice(0, 200))
        return null
      }
      const data = await res.json().catch(() => null)
      // systeme ha devuelto la lista en varios formatos según la versión.
      const items: any[] = Array.isArray(data) ? data : (data?.items ?? data?.data ?? [])
      if (!Array.isArray(items) || items.length === 0) break

      for (const t of items) {
        if (t?.name) seen.push(String(t.name))
        if (normalizeName(t?.name) === target && t?.id) return Number(t.id)
      }
      if (items.length < 50) break // última página
    }
    debug.tagsSeen = seen.slice(0, 15)
    console.error(
      '[waitlist] etiqueta no encontrada:', tagName,
      '— etiquetas vistas:', seen.slice(0, 15).join(' | ') || '(ninguna)'
    )
  } catch (e) {
    debug.error = (e as Error).message
    console.error('[waitlist] findTagId error:', e)
  }
  return null
}

type SyncDebug = {
  createStatus?: number
  tagLookupStatus?: number
  tagLookupBody?: string
  tagsSeen?: string[]
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
      findTagId(tagName, headers, debug),
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
      if (!contactId) console.error('[waitlist] sin contactId para:', email)
      // El contacto SÍ está creado; lo único que falta es la etiqueta. Se avisa
      // así de claro para no volver a leerlo como "no se guardó nada".
      if (contactId && !tagId) {
        console.error(
          '[waitlist] contacto', contactId, 'creado SIN etiqueta —',
          'pon SYSTEME_WAITLIST_TAG_ID en Vercel con el id de "' + tagName + '"'
        )
      }
    }
  } catch (e) {
    debug.error = (e as Error).message
    console.error('[waitlist] syncToCRM error:', e)
  }
}

// ── Aviso cuando un alta NO llega al CRM ──────────────────────────────────────

/**
 * Manda un correo al equipo con el alta que no se ha podido guardar.
 *
 * Existe porque la web SIEMPRE le dice al visitante "¡registrado con éxito!"
 * (no vamos a enseñarle un error por un problema nuestro), así que si el CRM
 * falla nadie se entera. Pasó: entre junio y agosto de 2026 caducó la clave de
 * systeme y se perdieron dos meses de altas en silencio.
 *
 * Va por Resend, la misma casa que ya manda los correos de la academia.
 */
async function alertFailedSignup(details: {
  email: string
  firstName: string
  lastName: string
  phone: string
  tagName: string
  page: string
  reason: string
}): Promise<void> {
  const key = env('RESEND_API_KEY')
  const to = env('ALERT_EMAIL_TO') || 'holandesnawar@gmail.com'
  const from = env('ALERT_EMAIL_FROM') || 'Holandés Nawar <noreply@mail.holandesnawar.com>'

  if (!key) {
    console.error('[waitlist] RESEND_API_KEY no configurada: no se puede avisar del alta perdida')
    return
  }

  const cuando = new Date().toLocaleString('es-ES', { timeZone: 'Europe/Madrid' })
  const fila = (etiqueta: string, valor: string) =>
    valor
      ? `<tr><td style="padding:4px 12px 4px 0;color:#5A6480;">${etiqueta}</td>
           <td style="padding:4px 0;color:#0a1656;font-weight:600;">${escapeHtml(valor)}</td></tr>`
      : ''

  const html = `
    <div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;max-width:520px;">
      <h2 style="color:#1D0084;font-size:18px;margin:0 0 6px;">Un alta no ha llegado al CRM</h2>
      <p style="color:#5A6480;font-size:14px;line-height:1.6;margin:0 0 16px;">
        Esta persona se apuntó en la web y vio el mensaje de confirmación, pero
        <strong>no se ha podido guardar en systeme.io</strong>. Apúntala a mano y
        revisa el motivo.
      </p>
      <table style="font-size:14px;border-collapse:collapse;">
        ${fila('Email', details.email)}
        ${fila('Nombre', [details.firstName, details.lastName].filter(Boolean).join(' '))}
        ${fila('Teléfono', details.phone)}
        ${fila('Se apuntó en', details.page)}
        ${fila('Etiqueta que tocaba', details.tagName)}
        ${fila('Cuándo', cuando)}
      </table>
      <p style="margin:16px 0 0;padding:10px 12px;background:#F0F5FF;border-radius:8px;
                color:#0a1656;font-size:13px;line-height:1.5;">
        <strong>Motivo técnico:</strong> ${escapeHtml(details.reason)}
      </p>
    </div>
  `

  try {
    const res = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { Authorization: `Bearer ${key}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        from,
        to: [to],
        subject: `⚠️ Alta perdida en la web: ${details.email}`,
        html,
      }),
    })
    if (!res.ok) {
      console.error('[waitlist] no se pudo avisar por email:', res.status, (await res.text()).slice(0, 200))
    } else {
      console.log('[waitlist] aviso de alta perdida enviado a', to)
    }
  } catch (e) {
    console.error('[waitlist] error avisando del alta perdida:', e)
  }
}

function escapeHtml(value: string): string {
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
}

/** En qué página estaba el visitante al apuntarse. */
function sourcePage(request: Request, body: any): string {
  const explicit = (body?.source ?? body?.page ?? '').toString().trim()
  if (explicit) return explicit
  const referer = request.headers.get('referer') || ''
  return referer || '(desconocida)'
}

/** Resumen legible de por qué no se guardó. */
function failureReason(debug: SyncDebug): string {
  if (debug.error) return debug.error
  const partes: string[] = []
  if (debug.createStatus) partes.push(`crear contacto → ${debug.createStatus}`)
  if (debug.createBody) partes.push(debug.createBody)
  if (debug.searchStatus) partes.push(`buscar contacto → ${debug.searchStatus}`)
  return partes.join(' · ') || 'systeme.io no devolvió ningún contacto'
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

  // ── Honeypot anti-bot ──
  // Si el campo trampa 'website' viene relleno, es un bot.
  // Devolvemos success silencioso para no avisar al bot.
  const honeypot = (body?.website ?? '').toString().trim()
  if (honeypot) {
    console.log('[waitlist] honeypot triggered, ignoring submission from:', email)
    return json({
      success: true,
      message: '¡Registrado con éxito! Te avisamos en cuanto abramos plazas.',
    })
  }

  // Única validación que bloquea: email inválido
  if (!email || !email.includes('@')) {
    return json({ error: 'Email inválido' }, 400)
  }

  // Doble acceso: import.meta.env (dev) + process.env (serverless Vercel)
  const apiKey = env('SYSTEME_API_KEY')
  const page = sourcePage(request, body)

  console.log('[waitlist] received:', { email, tagName, page, hasKey: !!apiKey })

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
    debug.error = 'SYSTEME_API_KEY no configurada'
    console.error('[waitlist] SYSTEME_API_KEY no configurada — alta sin guardar:', email)
  }

  // Si no hay contacto, el alta se ha perdido: avisar YA, con todo lo que hace
  // falta para apuntarla a mano. Se espera al envío a propósito: en Vercel la
  // función se congela al responder y una promesa suelta se quedaría sin salir.
  if (!debug.contactId) {
    await alertFailedSignup({
      email,
      firstName,
      lastName,
      phone,
      tagName,
      page,
      reason: failureReason(debug),
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
