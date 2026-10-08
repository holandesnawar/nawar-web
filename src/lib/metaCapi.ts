/**
 * La API de conversiones de Meta ("CAPI"): los eventos del embudo mandados
 * TAMBIÉN desde el servidor al conjunto de datos de la web (el píxel
 * «Hebben&Zijn», PIXEL_META). 07/10 el Lead; 08/10 Schedule, VSLVisto y VSL50.
 *
 * Por qué: el píxel del navegador pierde entre un 10 y un 25 % de los eventos
 * (bloqueadores de anuncios, Safari, el navegador de Instagram). Con una
 * campaña de 15 €/día, cada conversión que Meta no ve es aprendizaje que no
 * hace. Desde el servidor no hay bloqueador que valga.
 *
 * ⚠️ Deduplicación: el navegador y el servidor mandan el MISMO `event_id`
 * (lo crea la página antes de disparar el píxel). Así Meta cuenta UNA
 * conversión aunque le lleguen las dos. Sin eso, cada una contaría doble.
 *
 * De dónde sale cada evento del servidor:
 *  - Lead y Schedule: de /api/cualificacion, que ya recibe el nombre, el
 *    correo y el teléfono (los cifra aquí antes de mandarlos);
 *  - VSLVisto y VSL50: de /api/embudo; el navegador manda los datos YA
 *    cifrados, así que esa ruta nunca ve un correo en claro.
 *
 * ⚠️ Datos de la persona: SOLO cifrados. `cuerpoEvento` tira cualquier valor
 * de em/ph/fn que no sea una huella SHA-256, venga de donde venga.
 *
 * Solo se manda si hay token: `META_CAPI_ACCESS_TOKEN` en Vercel (vale también
 * el nombre viejo, `META_CAPI_TOKEN`). Sin token no hace nada y el píxel del
 * navegador sigue igual. `META_CAPI_TEST_CODE` (opcional) manda los eventos a
 * «Probar eventos» en vez de a la campaña: quitarlo al terminar de probar.
 * `META_GRAPH_VERSION` cambia la versión de la Graph API sin tocar código.
 *
 * Nunca rompe nada: si Meta no contesta o contesta mal, se apunta en el log y
 * ya. Para entonces el lead ya está guardado en la escuela.
 */
import type { APIContext } from 'astro'
import { PIXEL_META } from './admision'
import { esHash, type UsuarioHash } from './metaUsuario'
import { leerEnv } from './systeme'

/** La versión actual de la Graph API (v26.0 salió el 29/07/2026). */
const VERSION_API = 'v26.0'

export type NombreEvento = 'Lead' | 'Schedule' | 'VSLVisto' | 'VSL50'

export type EventoServidor = {
  nombre: NombreEvento
  /** El mismo que lleva el evento del navegador (`eventID`). */
  eventId: string
  /** La dirección de la página donde pasó (con ?fbclid= y ?utm_…). */
  url: string
  usuario: UsuarioHash
  ip?: string
  agente?: string
  /** Cookies del píxel: `_fbc` (clic en el anuncio) y `_fbp` (navegador). */
  fbc?: string
  fbp?: string
  /** `content_name`, el mismo que lleva el evento del navegador. */
  contenido?: string
}

const tokenCapi = () => leerEnv('META_CAPI_ACCESS_TOKEN') || leerEnv('META_CAPI_TOKEN') || ''

/** La cookie `_fbc` si la hay; si no, se rehace con el fbclid de la dirección
 *  (es el formato que pide Meta: fb.1.<milisegundos>.<fbclid>). */
export function fbcDe(cookie: string | undefined, url: string, ahora = Date.now()): string {
  if (cookie && /^fb\.\d\.\d+\.[\w-]+$/.test(cookie)) return cookie
  try {
    const fbclid = new URL(url).searchParams.get('fbclid')
    if (fbclid && /^[\w-]{10,500}$/.test(fbclid)) return `fb.1.${ahora}.${fbclid}`
  } catch {}
  return ''
}

/** `_fbp` solo si tiene la forma que pone el píxel (fb.1.<ms>.<número>). */
export const fbpDe = (cookie: string | undefined) => (cookie && /^fb\.\d\.\d+\.\d+$/.test(cookie) ? cookie : '')

/**
 * La página del evento, solo si es de esta web: la que mande el navegador o,
 * si no vale, la de `Referer`. Sin una dirección buena no se manda nada (Meta
 * la pide para los eventos de un sitio web).
 */
export function urlDelEvento(pagina: string, request: Request): string {
  const propia = (() => { try { return new URL(request.url).hostname } catch { return '' } })()
  const vale = (u: string) => {
    try {
      const x = new URL(u)
      const host = x.hostname
      const deLaWeb = host === 'holandesnawar.com' || host.endsWith('.holandesnawar.com') || (!!propia && host === propia)
      return /^https?:$/.test(x.protocol) && deLaWeb ? x.toString().slice(0, 1000) : ''
    } catch {
      return ''
    }
  }
  return vale(pagina) || vale(request.headers.get('referer') || '')
}

/** La IP de quien manda. En Vercel va en x-forwarded-for; `clientAddress`
 *  puede lanzar si el adaptador no la da. */
export function ipDe(ctx: APIContext): string {
  const delante = (ctx.request.headers.get('x-forwarded-for') || '').split(',')[0].trim()
  if (delante) return delante
  try { return ctx.clientAddress } catch { return '' }
}

/** El cuerpo que se manda a Meta. Aparte para poder probarlo sin red. */
export function cuerpoEvento(e: EventoServidor, ahora = Date.now()) {
  const user_data: Record<string, unknown> = {}
  // Solo huellas SHA-256. Un correo en claro (o cualquier otra cosa) se tira.
  for (const k of ['em', 'ph', 'fn'] as const) {
    const v = e.usuario?.[k]
    if (esHash(v)) user_data[k] = [v]
  }
  if (e.ip) user_data.client_ip_address = e.ip
  if (e.agente) user_data.client_user_agent = e.agente.slice(0, 500)
  const fbc = fbcDe(e.fbc, e.url, ahora)
  if (fbc) user_data.fbc = fbc
  const fbp = fbpDe(e.fbp)
  if (fbp) user_data.fbp = fbp
  const test = leerEnv('META_CAPI_TEST_CODE')
  return {
    data: [
      {
        event_name: e.nombre,
        event_time: Math.floor(ahora / 1000),
        event_id: e.eventId,
        action_source: 'website',
        event_source_url: e.url,
        user_data,
        ...(e.contenido ? { custom_data: { content_name: e.contenido } } : {}),
      },
    ],
    ...(test ? { test_event_code: test } : {}),
  }
}

export async function enviarEventoServidor(e: EventoServidor): Promise<void> {
  const token = tokenCapi()
  if (!token || !PIXEL_META || !e.eventId || !e.url) return
  const version = /^v\d{2,3}\.\d$/.test(leerEnv('META_GRAPH_VERSION') || '') ? leerEnv('META_GRAPH_VERSION') : VERSION_API
  try {
    const r = await fetch(`https://graph.facebook.com/${version}/${PIXEL_META}/events`, {
      method: 'POST',
      // El token va en el cuerpo, no en la dirección: así no acaba en ningún
      // registro de peticiones.
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ...cuerpoEvento(e), access_token: token }),
      signal: AbortSignal.timeout(4000),
    })
    if (!r.ok) console.error('[capi]', e.nombre, 'Meta contestó', r.status, (await r.text().catch(() => '')).slice(0, 300))
  } catch (err) {
    console.error('[capi]', e.nombre, 'no se pudo mandar:', (err as Error).message)
  }
}
