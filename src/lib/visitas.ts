/**
 * Cuenta cada página vista para la analítica del panel de la escuela
 * (17/11/2026: "ver las analíticas de las webs dentro del panel… de dónde
 * viene el tráfico, cuántos leads por paid vs orgánico, quién agendó gracias a
 * qué utm").
 *
 * Sin datos personales ni cookies: un número de sesión al azar en
 * `sessionStorage` (se pierde al cerrar la pestaña), la web, la página, la web
 * de la que venía (solo el nombre, y solo si era de fuera), la campaña del
 * enlace y el ancho de la pantalla (para móvil u ordenador). La escuela guarda
 * una fila por sesión (learnhouse: apps/api/src/services/stats/analitica.py).
 *
 * Se llama desde el Layout, o sea en TODAS las páginas, también las del
 * subdominio de Black Friday. Se manda directo a la escuela como texto: sin
 * consulta previa de CORS, y `keepalive` deja que llegue aunque la página se
 * esté yendo. Si falla, no pasa nada: es un contador.
 *
 * No cuenta en local ni en las vistas previas de Vercel: la escuela solo
 * acepta las webs *.holandesnawar.com.
 */
import { ESCUELA_URL } from './escuela'
import { leerUTM } from './utm'

const CLAVE_SESION = 'nawar.visita.sesion'
const CLAVE_ORIGEN = 'nawar.visita.origen'

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

/**
 * La web de fuera de la que llegó esta visita (Instagram, Google…), la
 * primera vez que se sabe. Se guarda para la visita entera: al pasar a otra
 * página de la web, `document.referrer` ya es nuestra propia web.
 */
export function webDeOrigen(): string {
  try {
    const guardada = sessionStorage.getItem(CLAVE_ORIGEN)
    if (guardada !== null) return guardada
  } catch {
    /* sin almacenamiento, se mira cada vez */
  }
  let web = ''
  try {
    const r = document.referrer || ''
    if (r) {
      const host = new URL(r).hostname.toLowerCase()
      if (!host.endsWith('holandesnawar.com')) web = host.slice(0, 120)
    }
  } catch {
    /* referrer ilegible */
  }
  try {
    sessionStorage.setItem(CLAVE_ORIGEN, web)
  } catch {}
  return web
}

export function contarVisita(): void {
  const s = sesion()
  if (!s) return
  const u = leerUTM()
  try {
    fetch(`${ESCUELA_URL}/api/v1/contactos/visita`, {
      method: 'POST',
      keepalive: true,
      headers: { 'Content-Type': 'text/plain' },
      body: JSON.stringify({
        s,
        h: window.location.hostname,
        r: window.location.pathname,
        ref: webDeOrigen(),
        w: window.innerWidth || 0,
        utm_source: u.utmSource,
        utm_medium: u.utmMedium,
        utm_campaign: u.utmCampaign,
        utm_content: u.utmContent,
        utm_term: u.utmTerm,
      }),
    }).catch(() => {})
  } catch {}
}
