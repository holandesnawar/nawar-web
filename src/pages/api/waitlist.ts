import type { APIRoute } from 'astro'
import { avisarEscuela } from '../../lib/escuela'
import { camposDePersona, escribirCampos as escribirCamposLib, relojDe } from '../../lib/systeme'
import { createHash, timingSafeEqual } from 'node:crypto'

export const prerender = false

const SYSTEME_BASE = 'https://api.systeme.io/api'
const TAG_NAME     = 'Lista de espera'

// ── Helpers ───────────────────────────────────────────────────────────────────

/**
 * Cómo se comparan los nombres de etiqueta.
 *
 * Sin acentos, sin mayúsculas y con los guiones y los espacios de más
 * aplanados. Mismo criterio que el webhook de Inrō, y por el mismo motivo:
 * "Nuevo Bases", "nuevo bases" y "Nuevo-Bases" son la misma etiqueta para una
 * persona, y si el código no lo ve así acaba creando duplicados que parten la
 * campaña en dos sin que salte ningún error.
 */
function normalizar(nombre: string): string {
  return (nombre || '')
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .replace(/[-_]+/g, ' ')
    .replace(/\s+/g, ' ')
    .trim()
}

/** Todas las etiquetas de la cuenta, paginando hasta que se acaban. */
async function listarEtiquetas(headers: Record<string, string>): Promise<any[]> {
  const todas: any[] = []
  // Tope de seguridad: 20 páginas = 2000 etiquetas. Con más que eso, algo raro
  // pasa y es mejor parar que quedarse dando vueltas dentro de una función
  // serverless que Vercel va a cortar igualmente.
  for (let page = 1; page <= 20; page++) {
    const res = await fetch(`${SYSTEME_BASE}/tags?itemsPerPage=100&page=${page}`, { headers })
    if (!res.ok) break
    const data = await res.json().catch(() => null)
    const items: any[] = data?.items ?? []
    todas.push(...items)
    if (items.length < 100) break
  }
  return todas
}

async function findTagId(tagName: string, headers: Record<string, string>): Promise<number | null> {
  try {
    // ⚠️ Antes esto miraba SOLO dos páginas (200 etiquetas) y comparaba el
    // nombre tal cual en minúsculas. Las dos cosas fallan en silencio
    // devolviendo null, y quien llama se queda sin saber si la etiqueta no
    // existe o si simplemente no se llegó a ella.
    const buscado = normalizar(tagName)
    const match = (await listarEtiquetas(headers)).find((t: any) => normalizar(t.name) === buscado)
    return match ? match.id : null
  } catch (e) {
    console.error('[waitlist] findTagId error:', e)
  }
  return null
}

/**
 * El id de una etiqueta, creándola si todavía no existe.
 *
 * Se crea sola a propósito: si la etiqueta se escribe aquí y falta en
 * systeme.io, el contacto entraría sin etiquetar y la campaña que cuelga de
 * ella no le llegaría a nadie, sin que salte ningún error a la vista. Es el
 * tipo de fallo que no se descubre hasta contar las ventas.
 */
async function ensureTagId(tagName: string, headers: Record<string, string>): Promise<number | null> {
  const existente = await findTagId(tagName, headers)
  if (existente) return existente
  try {
    const res = await fetch(`${SYSTEME_BASE}/tags`, {
      method: 'POST', headers, body: JSON.stringify({ name: tagName }),
    })
    if (res.ok) {
      const data = await res.json().catch(() => null)
      console.log('[waitlist] etiqueta creada:', tagName, data?.id)
      return data?.id ?? null
    }
    // Crear ha fallado. La causa más normal es que la etiqueta SÍ existe y la
    // búsqueda no dio con ella, así que se vuelve a mirar antes de rendirse:
    // rendirse aquí es lo que dejaba al lead sin etiquetar y a la campaña sin
    // nadie dentro.
    const cuerpo = await res.text().catch(() => '')
    console.error('[waitlist] no se pudo crear la etiqueta', tagName, res.status, cuerpo.slice(0, 150))
    const segundoIntento = await findTagId(tagName, headers)
    if (segundoIntento) return segundoIntento
  } catch (e) {
    console.error('[waitlist] error creando la etiqueta', tagName, e)
  }
  return null
}

type SyncDebug = {
  personaStatus?: number
  personaError?: string
  /** Lo que decide si entra en la campaña de bienvenida. Es EL dato. */
  esNuevo?: boolean
  campos?: string[]
  camposStatus?: number
  camposError?: string
  createStatus?: number
  createBody?: string
  contactId?: number | null
  tagId?: number | null
  tagStatus?: number
  tagNuevoId?: number | null
  tagNuevoStatus?: number
  searchStatus?: number
  searchBody?: string
  error?: string
}

/** Lo que se sabe de dónde vino esta persona. Todo opcional. */
export type Procedencia = {
  conociste?: string
  nivel?: string
  utmSource?: string
  utmMedium?: string
  utmCampaign?: string
}

/**
 * Escribe los campos personalizados del contacto, APARTE del alta.
 *
 * ⚠️ Antes iban dentro del POST que crea el contacto, y eso es justo lo que no
 * se puede hacer: systeme.io escribe los campos por SLUG, y un slug que no
 * exista hace fallar la petición ENTERA. Resultado: el lead no se crea, el
 * código baja a buscarlo, no lo encuentra, y la persona se pierde sin que
 * salte nada. Y solo les pasaría a los formularios que mandan campos —o sea,
 * justo a los de los anuncios, que son los que se pagan.
 *
 * Yendo aparte, lo peor que puede pasar es un contacto sin el campo relleno.
 * El lead se queda.
 */
async function escribirCampos(
  contactId: number,
  de: Procedencia,
  headers: Record<string, string>,
  debug: SyncDebug
): Promise<void> {
  // Los slugs los genera systeme.io quitando los caracteres no ingleses, no
  // transliterándolos: "Cómo conociste Nawar" -> cmo_conociste_nawar y
  // "Nivel de neerlandés" -> nivel_de_neerlands. No son erratas.
  const fields: { slug: string; value: string }[] = []
  if (de.conociste)   fields.push({ slug: 'cmo_conociste_nawar', value: de.conociste })
  if (de.nivel)       fields.push({ slug: 'nivel_de_neerlands',  value: de.nivel })
  if (de.utmSource)   fields.push({ slug: 'utm_source',          value: de.utmSource })
  if (de.utmMedium)   fields.push({ slug: 'utm_medium',          value: de.utmMedium })
  if (de.utmCampaign) fields.push({ slug: 'utm_campaign',        value: de.utmCampaign })
  if (!fields.length) return

  debug.campos = fields.map((f) => f.slug)
  try {
    // El PATCH de API Platform quiere merge-patch; con application/json
    // contesta 415. Se prueban los tres que acepta systeme.io según el caso.
    const intentos: [string, string][] = [
      ['PATCH', 'application/merge-patch+json'],
      ['PATCH', 'application/json'],
      ['PUT',   'application/json'],
    ]
    for (const [method, contentType] of intentos) {
      const res = await fetch(`${SYSTEME_BASE}/contacts/${contactId}`, {
        method,
        headers: { ...headers, 'Content-Type': contentType },
        body: JSON.stringify({ fields }),
      })
      debug.camposStatus = res.status
      if (res.ok) return
      // 415 = tipo de contenido que no le vale: se prueba el siguiente.
      // Cualquier otro error no se arregla cambiando el método.
      if (res.status !== 415) {
        debug.camposError = (await res.text().catch(() => '')).slice(0, 200)
        console.error('[waitlist] campos error:', res.status, debug.camposError)
        return
      }
    }
  } catch (e) {
    debug.camposError = (e as Error).message
    console.error('[waitlist] campos error:', e)
  }
}

async function syncToCRM(
  email: string,
  firstName: string,
  lastName: string,
  phone: string,
  de: Procedencia,
  tagName: string,
  /** Etiqueta que recibe SOLO quien no estaba ya en el CRM. Vacío = ninguna. */
  tagNuevoName: string,
  headers: Record<string, string>,
  debug: SyncDebug
): Promise<void> {
  try {
    // Solo los campos de toda la vida. Los personalizados van después y por
    // su cuenta: ver escribirCampos() para el porqué, que no es un detalle.
    const body: Record<string, any> = { email }
    if (firstName) body.firstName = firstName
    if (lastName)  body.surname   = lastName
    if (phone)     body.phone     = phone

    // Crear o encontrar contacto y buscar tag en paralelo
    const [createRes, tagId] = await Promise.all([
      fetch(`${SYSTEME_BASE}/contacts`, { method: 'POST', headers, body: JSON.stringify(body) }),
      findTagId(tagName, headers),
    ])
    debug.createStatus = createRes.status
    debug.tagId = tagId

    let contactId: number | null = null
    // Nuevo = systeme.io ha aceptado el alta. Si el correo ya estaba, el POST
    // devuelve 4xx y bajamos a buscarlo. Ese es todo el criterio, y es el
    // bueno: lo decide el CRM, no nosotros.
    let esNuevo = false

    if (createRes.ok) {
      const data = await createRes.json().catch(() => null)
      contactId = data?.id ?? null
      esNuevo = true
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
    debug.esNuevo = esNuevo

    // Los campos personalizados, ahora que hay contacto y venga de donde venga
    // (recién creado o encontrado). Si falla, falla solo esto.
    if (contactId) await escribirCampos(contactId, de, headers, debug)

    // Y el nombre, el apellido y el teléfono como campos por slug, aparte.
    // Mandarlos como propiedades sueltas del contacto (arriba, en el POST) no
    // los guardaba y no avisaba: ver camposDePersona() en lib/systeme.ts.
    if (contactId) {
      const rp = await escribirCamposLib(
        contactId,
        camposDePersona(firstName, lastName, phone),
        { apiKey: headers['X-API-Key'], reloj: relojDe(8000) }
      )
      debug.personaStatus = rp.status
      if (!rp.ok) {
        debug.personaError = (rp.error ?? '').slice(0, 200)
        console.error('[waitlist] persona error:', rp.status, debug.personaError)
      }
    }

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

    // La etiqueta de "lead nuevo": solo para quien no estaba ya en el CRM, que
    // es de lo que cuelga la campaña de bienvenida. A quien ya está dentro no
    // se le vuelve a dar la bienvenida.
    if (contactId && esNuevo && tagNuevoName) {
      const idNuevo = await ensureTagId(tagNuevoName, headers)
      debug.tagNuevoId = idNuevo
      if (idNuevo) {
        const tr = await fetch(`${SYSTEME_BASE}/contacts/${contactId}/tags`, {
          method: 'POST', headers, body: JSON.stringify({ tagId: idNuevo }),
        })
        debug.tagNuevoStatus = tr.status
        // 409 = ya la tenía = también es éxito.
        if (tr.ok || tr.status === 409) console.log('[waitlist] lead nuevo etiquetado:', tagNuevoName, contactId)
        else console.error('[waitlist] error etiquetando lead nuevo:', tr.status)
      }
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
  // De qué anuncio viene. Los manda el formulario leyéndolos de su propia URL;
  // si la visita es orgánica llegan vacíos y no se escribe nada, que es lo
  // correcto: un utm_source en blanco pisaría el de una visita anterior.
  const utmSource   = (body?.utmSource   ?? '').trim().slice(0, 120)
  const utmMedium   = (body?.utmMedium   ?? '').trim().slice(0, 120)
  const utmCampaign = (body?.utmCampaign ?? '').trim().slice(0, 120)
  const tagName   =
    typeof body?.tagName === 'string' && body.tagName.trim()
      ? body.tagName.trim()
      : TAG_NAME
  // Qué guía es ("bases", "hebben"). Lo manda solo el formulario de una guía;
  // los demás (lista de espera, contacto de anuncios) no lo mandan y no se
  // avisa a la escuela desde aquí: el de anuncios ya avisa por /api/solicitud
  // y la lista de espera no es una descarga.
  const guia = typeof body?.guia === 'string' ? body.guia.trim().slice(0, 20) : ''
  const recorrido: string[] = Array.isArray(body?.recorrido)
    ? body.recorrido.filter((x: unknown) => typeof x === 'string' && /^[a-z-]{1,24}$/.test(x)).slice(-12)
    : []
  const referrer = (body?.referrer ?? '').toString().trim().slice(0, 120)
  // Opcional: la manda solo el formulario que quiere separar a los que llegan
  // por primera vez. Si no viene, no se etiqueta nada de más.
  const tagNuevo =
    typeof body?.tagNuevo === 'string' && body.tagNuevo.trim() ? body.tagNuevo.trim() : ''

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
  const apiKey =
    (import.meta.env.SYSTEME_API_KEY as string | undefined) ||
    (typeof process !== 'undefined' ? process.env.SYSTEME_API_KEY : undefined)

  console.log('[waitlist] received:', { email, tagName, hasKey: !!apiKey })

  // ⚠️ El diagnóstico se calculaba entero y se tiraba a la basura: la
  // respuesta era siempre el mismo "¡Registrado con éxito!" pasara lo que
  // pasara. Por eso, cuando la etiqueta de lead nuevo dejó de ponerse, no
  // había forma de saber si fallaba la etiqueta, el alta o el nombre.
  //
  // Ahora se puede pedir, pero SOLO con la clave: decir en abierto si un correo
  // ya estaba en la lista dejaría que cualquiera comprobase quién está apuntado
  // probando direcciones una a una.
  const claveDada = typeof body?.clave === 'string' ? body.clave : ''
  const claveBuena =
    (import.meta.env.NAWAR_WEBHOOK_SECRET as string | undefined) ||
    (typeof process !== 'undefined' ? process.env.NAWAR_WEBHOOK_SECRET : undefined)
  const conDiagnostico = !!claveDada && !!claveBuena && mismaClave(claveDada, claveBuena)

  const debug: SyncDebug = {}
  if (apiKey) {
    const headers = {
      'X-API-Key':    apiKey,
      'Content-Type': 'application/json',
      'accept':       'application/json',
    }
    try {
      await syncToCRM(
        email,
        firstName,
        lastName,
        phone,
        { conociste, nivel, utmSource, utmMedium, utmCampaign },
        tagName,
        tagNuevo,
        headers,
        debug
      )
    } catch (e) {
      debug.error = (e as Error).message
      console.error('[waitlist] sync failed:', e)
    }
  } else {
    debug.error = 'SYSTEME_API_KEY not set'
    console.error('[waitlist] SYSTEME_API_KEY not set — skipping CRM sync for:', email)
  }
  // La copia en la escuela: con o sin CRM, que quede rastro del alta. Las
  // guías van con su nombre; la lista de espera (la que no manda `guia` y
  // entra con la etiqueta de siempre) también, para que el orgánico no se
  // quede solo en systeme.io. El formulario de contacto de anuncios NO pasa
  // por aquí: ya avisa por /api/solicitud y avisar dos veces sacaría a la
  // persona dos veces en su historial.
  const esListaDeEspera = !guia && tagName === TAG_NAME
  if ((guia || esListaDeEspera) && email) {
    await avisarEscuela({
      kind: guia === 'bases' ? 'guia-bases' : guia === 'hebben' ? 'guia-hebben' : guia ? 'guia' : 'lista-espera',
      email,
      first_name: firstName,
      last_name: lastName,
      phone,
      source: conociste === 'Anuncio' || utmSource ? 'ads' : 'web',
      tag: tagName,
      recorrido,
      referrer,
      utm_source: utmSource,
      utm_medium: utmMedium,
      utm_campaign: utmCampaign,
    })
  }


  return json({
    success: true,
    message: '¡Registrado con éxito! Te avisamos en cuanto abramos plazas.',
    ...(conDiagnostico ? { diagnostico: debug } : {}),
  })
}

/**
 * Las dos claves, comparadas en tiempo constante. Se hashean antes para que los
 * búferes midan igual (`timingSafeEqual` revienta con longitudes distintas) y
 * de paso no se filtre la longitud de la buena. Mismo patrón que el webhook de
 * Inrō.
 */
function mismaClave(a: string, b: string): boolean {
  const ha = createHash('sha256').update(a, 'utf8').digest()
  const hb = createHash('sha256').update(b, 'utf8').digest()
  return timingSafeEqual(ha, hb)
}

function json(data: object, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json' },
  })
}
