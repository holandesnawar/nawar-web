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
 * Desde el 22/11/2026 manda además la zona horaria del navegador (de ahí sale
 * el país, sin IP), si ese navegador ya había venido otro día y si en esta
 * visita se mandó algún formulario. Sigue sin haber nada que diga quién es.
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
// 22/11/2026: tres cosas más para la analítica, igual de anónimas.
const CLAVE_PRIMERA = 'nawar.visita.primera' // localStorage: el primer día que vino este navegador
const CLAVE_VUELVE = 'nawar.visita.vuelve' // sessionStorage: 1 si ya había venido otro día
const CLAVE_DATOS = 'nawar.visita.datos' // sessionStorage: 1 si en esta visita mandó un formulario

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

/**
 * La zona horaria del navegador (Europe/Amsterdam…). La escuela saca de ahí
 * el país de la visita, sin mirar la IP. Vacía si el navegador no la da.
 */
function zona(): string {
  try {
    return (Intl.DateTimeFormat().resolvedOptions().timeZone || '').slice(0, 40)
  } catch {
    return ''
  }
}

/**
 * Si este navegador ya había venido antes de esta visita. Es una marca suya
 * (el primer día que vino), no un identificador: no dice quién es. Se decide
 * una vez por visita, para que la segunda página no cuente como «vuelve».
 */
function vuelve(): boolean {
  try {
    const sabido = sessionStorage.getItem(CLAVE_VUELVE)
    if (sabido !== null) return sabido === '1'
    let antes = false
    try {
      antes = localStorage.getItem(CLAVE_PRIMERA) !== null
      if (!antes) localStorage.setItem(CLAVE_PRIMERA, new Date().toISOString().slice(0, 10))
    } catch {
      /* sin localStorage (modo privado): cuenta como primera vez */
    }
    sessionStorage.setItem(CLAVE_VUELVE, antes ? '1' : '0')
    return antes
  } catch {
    return false
  }
}

function dejoDatos(): boolean {
  try {
    return sessionStorage.getItem(CLAVE_DATOS) === '1'
  } catch {
    return false
  }
}

function avisar(mas: Record<string, unknown> = {}): void {
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
        z: zona(),
        v: vuelve() ? 1 : 0,
        d: dejoDatos() ? 1 : 0,
        ...mas,
      }),
    }).catch(() => {})
  } catch {}
}

export function contarVisita(): void {
  avisar()
}

/**
 * En esta visita se ha mandado un formulario con los datos de una persona.
 * A la escuela solo le llega «en esta visita sí» (no de quién): así la
 * analítica sabe qué página de entrada, qué país y qué hora acaban en un
 * lead. Lo llama `contextoDelLead` (recorrido.ts), que usan todos los
 * formularios al enviar. Una vez por visita, y no cuenta como otra página.
 */
export function marcarDatosDejados(): void {
  try {
    if (sessionStorage.getItem(CLAVE_DATOS) === '1') return
    sessionStorage.setItem(CLAVE_DATOS, '1')
  } catch {
    return
  }
  avisar({ e: 'datos', d: 1 })
}
