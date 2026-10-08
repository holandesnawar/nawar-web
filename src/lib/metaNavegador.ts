/**
 * El lado del navegador de los eventos que van a Meta por dos caminos (el
 * píxel y la API de conversiones del servidor). 08/10.
 *
 * Cada evento lleva un `event_id` que se crea AQUÍ y se usa para los dos: el
 * píxel lo recibe como `eventID` y el servidor como `event_id`. Con el mismo
 * id y el mismo nombre, Meta lo cuenta una sola vez.
 */
import { CLAVE_DATOS, type DatosAdmision } from './admision'
import { hashUsuario } from './metaUsuario'

/** Un id por evento: `<prefijo>-<milisegundos>-<azar>`. */
export const nuevoEventId = (prefijo: string) =>
  `${prefijo}-${Date.now()}-${Math.random().toString(36).slice(2, 10)}`

/**
 * VSLVisto / VSL50: al píxel del navegador y, con el mismo id, al servidor
 * (/api/embudo). Los datos de la persona (los que dejó en el formulario, si
 * los hay en este navegador) salen de aquí YA cifrados; si no se pueden
 * cifrar, no salen.
 */
export function eventoDelVideo(evento: 'VSLVisto' | 'VSL50', contenido = 'Formación Nawar FB') {
  const eventId = nuevoEventId(evento.toLowerCase())
  try { (window as any).fbq?.('trackCustom', evento, { content_name: contenido }, { eventID: eventId }) } catch {}
  void (async () => {
    let usuario = {}
    try {
      const d = JSON.parse(localStorage.getItem(CLAVE_DATOS) || 'null') as DatosAdmision | null
      if (d) usuario = await hashUsuario(d.email, d.phone, d.first_name)
    } catch {}
    try {
      await fetch('/api/embudo', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        keepalive: true,
        body: JSON.stringify({ evento, event_id: eventId, pagina: location.href, usuario }),
      })
    } catch {}
  })()
}
