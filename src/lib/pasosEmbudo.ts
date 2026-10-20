/**
 * Hasta dónde llega cada visita de los embudos, para los KPIs del panel de la
 * escuela (20/10/2026: "qué porcentaje ve el anuncio y de ahí cuántos dejan
 * su mail y datos y cuántos no, cuántos ven el vídeo y continúan y cuántos en
 * el vídeo se van").
 *
 * Sin datos personales: un número de sesión al azar (en `sessionStorage`, se
 * pierde al cerrar la pestaña), el embudo, el paso y la campaña. La escuela
 * guarda una fila por sesión y embudo y la va subiendo
 * (learnhouse: apps/api/src/services/contactos/embudo_visitas.py).
 *
 * Se manda directo a la escuela como texto: así no hay consulta previa de
 * CORS y `keepalive` deja que llegue aunque la página se esté yendo. Cada paso
 * se manda una vez por sesión; el vídeo, solo cuando pasa un hito nuevo.
 * Si falla, no pasa nada: es un contador.
 */
import { ESCUELA_URL } from './escuela'
import { leerUTM } from './utm'

export type Embudo = 'anuncio' | 'web' | 'admision'
export type Paso = 'visita' | 'datos' | 'formulario' | 'preguntas' | 'reserva'

const CLAVE_SESION = 'nawar.embudo.sesion'
/** Los hitos del vídeo: le dio al play, cuartos y entero. */
const HITOS = [1, 25, 50, 75, 100]

function sesion(): string {
  try {
    let s = sessionStorage.getItem(CLAVE_SESION)
    if (!s) {
      s = Array.from(crypto.getRandomValues(new Uint8Array(12)), (b) => b.toString(16).padStart(2, '0')).join('')
      sessionStorage.setItem(CLAVE_SESION, s)
    }
    return s
  } catch {
    return ''
  }
}

/** Una vez por sesión y clave. */
function primeraVez(clave: string): boolean {
  try {
    const k = `nawar.embudo.${clave}`
    if (sessionStorage.getItem(k)) return false
    sessionStorage.setItem(k, '1')
    return true
  } catch {
    return true
  }
}

function enviar(embudo: Embudo, paso: Paso | 'video', video = 0): void {
  const s = sesion()
  if (!s) return
  const u = leerUTM()
  try {
    fetch(`${ESCUELA_URL}/api/v1/contactos/paso`, {
      method: 'POST',
      keepalive: true,
      headers: { 'Content-Type': 'text/plain' },
      body: JSON.stringify({
        s, e: embudo, p: paso, v: video,
        utm_source: u.utmSource, utm_medium: u.utmMedium, utm_campaign: u.utmCampaign, utm_content: u.utmContent,
      }),
    }).catch(() => {})
  } catch {}
}

/** Llegó a un paso del embudo (una vez por sesión). */
export function marcarPaso(embudo: Embudo, paso: Paso): void {
  if (primeraVez(`${embudo}.${paso}`)) enviar(embudo, paso)
}

/** Por dónde va viendo el vídeo, en % (0-100). Solo manda los hitos nuevos. */
export function marcarVideo(embudo: Embudo, pct: number): void {
  if (!isFinite(pct)) return
  for (const h of HITOS) {
    if (pct >= h && primeraVez(`${embudo}.video.${h}`)) enviar(embudo, 'video', h)
  }
}
