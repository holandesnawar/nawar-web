import type { APIRoute } from 'astro'
import { createHash, timingSafeEqual } from 'node:crypto'
import {
  asignarEtiqueta,
  crearOBuscarContacto,
  escribirCampos,
  leerEnv,
  relojDe,
  resolverEtiqueta,
  type Ctx,
} from '../../../lib/systeme'

export const prerender = false

/**
 * Puente Inrō → systeme.io.
 *
 * Inrō captura el email dentro del DM de Instagram y dispara un `http_request`
 * contra esta ruta. Aquí se da de alta a la persona en el CRM con la etiqueta de
 * lista de espera y se guarda de dónde vino.
 *
 * Dos decisiones que gobiernan todo lo demás:
 *
 * 1. **Salvo el secreto y el email, siempre se contesta 200.** Si systeme.io
 *    falla, Inrō no debe reintentar en bucle: el escenario se quedaría atascado
 *    y el usuario, sin respuesta en el DM. El fallo se cuenta en el log, no en
 *    el código de estado.
 * 2. **Cada paso es independiente.** Contacto, campos y etiqueta van por
 *    separado, así que un slug mal escrito no impide que la persona entre en el
 *    CRM ni que reciba la etiqueta.
 *
 * Es idempotente: el mismo email dos veces no duplica nada. El alta contesta
 * 4xx si ya existe y entonces se recupera el contacto, y la etiqueta contesta
 * 409 si ya la tenía, que aquí cuenta como éxito.
 */

/**
 * Presupuesto total para hablar con systeme.io.
 *
 * Por debajo del `maxDuration` de Vercel (10 s por defecto): preferimos
 * contestar con la verdad a medias que morir a mitad y que Inrō lo lea como
 * fallo.
 */
const PRESUPUESTO_MS = 8_500

/**
 * Los campos personalizados del contacto, por slug.
 *
 * ⚠️ Estos cinco campos hay que crearlos a mano en systeme.io
 * (Contactos → Campos personalizados) ANTES de que esto sirva de algo. El slug
 * lo genera systeme.io a partir del nombre, y lo hace quitando los caracteres
 * no ingleses en vez de transliterarlos: "Nivel de neerlandés" acabó siendo
 * `nivel_de_neerlands`. Por eso los nombres propuestos van sin tildes y sin ñ,
 * para que el slug salga previsible.
 *
 * Si al crearlos systeme.io genera un slug distinto, se cambia AQUÍ y en ningún
 * otro sitio.
 */
const CAMPOS = {
  username: 'instagram_username',
  origen: 'origen',
  utm_source: 'utm_source',
  utm_medium: 'utm_medium',
  utm_campaign: 'utm_campaign',
} as const

/** Etiqueta por defecto si Inrō no manda ninguna. */
const ETIQUETA_POR_DEFECTO = 'Lista de espera'

// Suficientemente estricto para descartar basura, suficientemente laxo para no
// rechazar direcciones raras pero legítimas.
const EMAIL_RE = /^[^\s@,;]+@[^\s@,;.]+(\.[^\s@,;.]+)+$/

/**
 * Nombre de la cabecera que lleva el secreto compartido.
 *
 * Coincide con el de la variable de entorno a propósito: es como está puesto en
 * el escenario de Inrō y así solo hay un nombre que recordar. Las cabeceras HTTP
 * son insensibles a mayúsculas, así que da igual cómo la escriba Inrō.
 */
const CABECERA_SECRETO = 'NAWAR_WEBHOOK_SECRET'

/**
 * Compara dos secretos sin filtrar por dónde dejan de parecerse.
 *
 * Se comparan los hashes, no los textos: así los dos búferes miden siempre lo
 * mismo (`timingSafeEqual` revienta con longitudes distintas) y de paso la
 * longitud del secreto tampoco se filtra.
 */
function igualEnTiempoConstante(a: string, b: string): boolean {
  const ha = createHash('sha256').update(a, 'utf8').digest()
  const hb = createHash('sha256').update(b, 'utf8').digest()
  return timingSafeEqual(ha, hb)
}

/** El email nunca se escribe en claro en los logs. Los 16 primeros caracteres
 *  del sha256 bastan para seguirle la pista a un alta concreta. */
function huella(email: string): string {
  return createHash('sha256').update(email, 'utf8').digest('hex').slice(0, 16)
}

function json(data: object, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' },
  })
}

/**
 * Lee un campo del cuerpo, descartando las plantillas sin sustituir.
 *
 * En Inrō el cuerpo se escribe con variables (`{{ ... }}`) que la plataforma
 * reemplaza al vuelo. Si una se escribe mal, o el contacto no tiene ese dato,
 * lo que llega aquí es el texto de la plantilla en crudo. Guardar eso en el CRM
 * sería peor que no guardar nada: dejaría contactos con un `{{ contact.username }}`
 * de nombre de usuario y nadie se enteraría. Así que se tira.
 */
function texto(v: unknown): string {
  if (typeof v !== 'string') return ''
  const limpio = v.trim()
  return limpio.includes('{{') || limpio.includes('}}') ? '' : limpio
}

export const POST: APIRoute = async ({ request }) => {
  const t0 = Date.now()

  // ── 1. El secreto ─────────────────────────────────────────────────────────
  const secretoEsperado = leerEnv('NAWAR_WEBHOOK_SECRET')
  if (!secretoEsperado) {
    // Sin secreto configurado no se abre la puerta "por defecto": se cierra.
    console.error(JSON.stringify({ evt: 'inro_systeme', resultado: 'sin_secreto_configurado' }))
    return json({ ok: false, error: 'no autorizado' }, 401)
  }
  const secretoRecibido = request.headers.get(CABECERA_SECRETO) ?? ''
  if (!igualEnTiempoConstante(secretoRecibido, secretoEsperado)) {
    console.warn(JSON.stringify({ evt: 'inro_systeme', resultado: 'secreto_invalido' }))
    return json({ ok: false, error: 'no autorizado' }, 401)
  }

  // ── 2. El cuerpo ──────────────────────────────────────────────────────────
  const body = await request.json().catch(() => null)
  const email = texto(body?.email).toLowerCase()
  if (!EMAIL_RE.test(email)) {
    console.warn(JSON.stringify({ evt: 'inro_systeme', resultado: 'email_invalido' }))
    return json({ ok: false, error: 'email inválido' }, 400)
  }

  const username = texto(body?.username)
  const origen = texto(body?.origen)
  const etiqueta = texto(body?.tag) || ETIQUETA_POR_DEFECTO
  const nombre = texto(body?.name)
  // systeme.io guarda nombre y apellido por separado. Lo que llegue del DM es
  // un nombre suelto: la primera palabra al nombre, el resto al apellido.
  const [firstName = '', ...resto] = nombre ? nombre.split(/\s+/) : []
  const surname = resto.join(' ')

  const log = (resultado: string, extra: Record<string, unknown> = {}) => {
    console.log(
      JSON.stringify({
        ts: new Date().toISOString(),
        evt: 'inro_systeme',
        email_sha256: huella(email),
        origen: origen || null,
        resultado,
        ms: Date.now() - t0,
        ...extra,
      })
    )
  }

  // ── 3. systeme.io ─────────────────────────────────────────────────────────
  const apiKey = leerEnv('SYSTEME_API_KEY')
  if (!apiKey) {
    log('sin_api_key')
    return json({ ok: true, contact_id: null })
  }

  const ctx: Ctx = { apiKey, reloj: relojDe(PRESUPUESTO_MS) }

  try {
    // El alta del contacto y la búsqueda de la etiqueta no dependen la una de la
    // otra, así que van a la vez y ahorran un viaje entero del presupuesto.
    const [contacto, tag] = await Promise.all([
      crearOBuscarContacto(email, firstName, surname, ctx),
      resolverEtiqueta(etiqueta, ctx),
    ])

    if (contacto.id === null) {
      log('fallo_contacto', {
        status: contacto.status,
        detalle: contacto.error?.slice(0, 200) ?? null,
        tag_via: tag.via,
      })
      return json({ ok: true, contact_id: null })
    }

    const campos = [
      { slug: CAMPOS.username, value: username },
      { slug: CAMPOS.origen, value: origen },
      { slug: CAMPOS.utm_source, value: texto(body?.utm_source) },
      { slug: CAMPOS.utm_medium, value: texto(body?.utm_medium) },
      { slug: CAMPOS.utm_campaign, value: texto(body?.utm_campaign) },
    ].filter((c) => c.value)

    // En serie y no en paralelo: los dos escriben sobre el mismo contacto y no
    // conviene que se pisen.
    const resCampos = await escribirCampos(contacto.id, campos, ctx)
    const resTag = tag.id !== null ? await asignarEtiqueta(contacto.id, tag.id, ctx) : null

    const problemas: string[] = []
    if (!resCampos.ok) problemas.push(`campos:${resCampos.status}`)
    if (tag.id === null) problemas.push(`etiqueta:${tag.via}`)
    else if (resTag && !resTag.ok) problemas.push(`etiqueta:${resTag.status}`)

    log(problemas.length ? 'parcial' : 'ok', {
      contact_id: contacto.id,
      contacto: contacto.via,
      tag_id: tag.id,
      tag_via: tag.via,
      campos: campos.length,
      problemas: problemas.length ? problemas : undefined,
    })

    return json({ ok: true, contact_id: contacto.id })
  } catch (e) {
    // Red a la nada, JSON imposible, lo que sea: Inrō igualmente recibe un 200.
    log('excepcion', { detalle: (e as Error).message })
    return json({ ok: true, contact_id: null })
  }
}

/** Cualquier otro método. Existe para que un GET curioso no devuelva el HTML
 *  de la web con un 200 y confunda a quien esté depurando el escenario. */
export const ALL: APIRoute = () =>
  json({ ok: false, error: 'usa POST' }, 405)
