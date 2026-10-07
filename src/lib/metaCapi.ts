/**
 * El "Lead" del embudo del anuncio, mandado TAMBIÉN desde el servidor
 * (la API de conversiones de Meta, "CAPI"). 07/10.
 *
 * Por qué: el píxel del navegador pierde entre un 10 y un 25 % de los eventos
 * (bloqueadores de anuncios, Safari, el navegador de Instagram). Con una
 * campaña de 15 €/día, cada conversión que Meta no ve es aprendizaje que no
 * hace. Desde el servidor no hay bloqueador que valga.
 *
 * ⚠️ Deduplicación: el navegador y el servidor mandan el MISMO `event_id`
 * (lo crea la página antes de enviar el formulario). Así Meta cuenta UNA
 * conversión aunque le lleguen las dos. Sin eso, cada lead contaría doble.
 *
 * Solo se manda si hay token (`META_CAPI_TOKEN` en Vercel; se saca en el
 * Administrador de eventos → el píxel → Configuración → API de conversiones →
 * Generar identificador de acceso). Sin token, no hace nada: el píxel del
 * navegador sigue funcionando igual. `META_CAPI_TEST_CODE` (opcional) manda
 * los eventos a la pestaña «Probar eventos» en vez de a la campaña; quitarlo
 * al terminar de probar.
 *
 * Nunca rompe el formulario: si Meta no contesta o contesta mal, se apunta en
 * el log y ya. El lead ya está guardado en la escuela para entonces.
 */
import { createHash } from 'node:crypto'
import { PIXEL_META } from './admision'
import { leerEnv } from './systeme'

const VERSION_API = 'v21.0'

const sha256 = (texto: string) => createHash('sha256').update(texto).digest('hex')

export type LeadServidor = {
  eventId: string
  email: string
  telefono: string
  nombre: string
  /** La dirección de la página donde se mandó (con ?fbclid= y ?utm_…). */
  url: string
  ip?: string
  agente?: string
  /** Cookies del píxel: `_fbc` (clic en el anuncio) y `_fbp` (navegador). */
  fbc?: string
  fbp?: string
}

/** La cookie `_fbc` si la hay; si no, se rehace con el fbclid de la dirección
 *  (es el formato que pide Meta: fb.1.<milisegundos>.<fbclid>). */
export function fbcDe(cookie: string | undefined, url: string): string {
  if (cookie && /^fb\.\d\.\d+\./.test(cookie)) return cookie
  try {
    const fbclid = new URL(url).searchParams.get('fbclid')
    if (fbclid) return `fb.1.${Date.now()}.${fbclid}`
  } catch {}
  return ''
}

/** El cuerpo que se manda a Meta. Aparte para poder probarlo sin red. */
export function cuerpoLead(d: LeadServidor, ahora = Date.now()) {
  const user_data: Record<string, unknown> = {}
  const em = d.email.trim().toLowerCase()
  const ph = d.telefono.replace(/\D/g, '')
  const fn = d.nombre.trim().toLowerCase()
  if (em) user_data.em = [sha256(em)]
  if (ph) user_data.ph = [sha256(ph)]
  if (fn) user_data.fn = [sha256(fn)]
  if (d.ip) user_data.client_ip_address = d.ip
  if (d.agente) user_data.client_user_agent = d.agente
  const fbc = fbcDe(d.fbc, d.url)
  if (fbc) user_data.fbc = fbc
  if (d.fbp) user_data.fbp = d.fbp
  const test = leerEnv('META_CAPI_TEST_CODE')
  return {
    data: [
      {
        event_name: 'Lead',
        event_time: Math.floor(ahora / 1000),
        event_id: d.eventId,
        action_source: 'website',
        event_source_url: d.url,
        user_data,
        custom_data: { content_name: 'Formación Nawar FB' },
      },
    ],
    ...(test ? { test_event_code: test } : {}),
  }
}

export async function enviarLeadServidor(d: LeadServidor): Promise<void> {
  const token = leerEnv('META_CAPI_TOKEN')
  if (!token || !PIXEL_META || !d.eventId) return
  try {
    const r = await fetch(`https://graph.facebook.com/${VERSION_API}/${PIXEL_META}/events?access_token=${encodeURIComponent(token)}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(cuerpoLead(d)),
      signal: AbortSignal.timeout(4000),
    })
    if (!r.ok) console.error('[capi] Meta contestó', r.status, (await r.text().catch(() => '')).slice(0, 300))
  } catch (e) {
    console.error('[capi] no se pudo mandar:', (e as Error).message)
  }
}
