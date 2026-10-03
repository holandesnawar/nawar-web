/**
 * El proceso de admisión (/proceso-de-admision), el embudo nuevo del 02/10.
 *
 * Tres pasos, pidiendo poco al principio y más solo a quien ya está dentro:
 *  1. Un vídeo bloqueado. Al darle al play se piden nombre, correo y WhatsApp
 *     (una ventanita, tres datos). Con eso el lead ya está en la escuela.
 *  2. El vídeo. El botón de seguir se ve desde el principio, pero bloqueado,
 *     y se desbloquea al terminar el vídeo (pedido del usuario): el primer
 *     filtro es quién lo ve entero.
 *  3. La cualificación: una copia de /agendar con los datos ya puestos
 *     (/proceso-de-admision/paso-3). /agendar no se toca: este embudo se
 *     prueba aparte.
 *
 * Todo lo que llega a la escuela va marcado con `embudo: 'admision'` y el
 * estado del vídeo, para que en Panel → Llamadas se distinga de /agendar.
 */

/**
 * El vídeo del paso 2. Vale cualquiera de estas formas:
 *  - Bunny Stream: https://iframe.mediadelivery.net/embed/<biblioteca>/<id>
 *  - YouTube: https://www.youtube.com/watch?v=<id> o https://youtu.be/<id>
 *  - Vimeo: https://vimeo.com/<id>
 *  - Un .mp4 directo.
 * Vacío = el hueco del vídeo con un aviso de "vídeo en preparación", y el
 * botón de seguir abierto (para no dejar a nadie atascado).
 * PUBLIC_ADMISION_VIDEO en Vercel lo cambia sin tocar código; si no está,
 * vale el de abajo (el vídeo de matrícula, en su propia biblioteca de Bunny, 03/10).
 */
export const VIDEO_POR_DEFECTO = 'https://player.mediadelivery.net/play/769328/90342e57-d3b6-4e08-ad96-0f664cbcf531'
export const VIDEO_URL = ((import.meta.env.PUBLIC_ADMISION_VIDEO as string | undefined) || VIDEO_POR_DEFECTO).trim()

/** Imagen de portada del vídeo bloqueado (la miniatura de Bunny, si se pone
 *  una). Vacío = el fondo de la marca. */
export const VIDEO_PORTADA = ''

/** El trozo del vídeo que se ve de fondo, en silencio y en bucle, mientras
 *  está bloqueado (03/10: "del segundo 20 al 30 y luego bucle"; luego, del 35 al 40). */
export const PREVIEW_DESDE = 35
export const PREVIEW_HASTA = 40

/** Lo que dura el vídeo, para la barra de abajo del vídeo bloqueado: que se
 *  vea un reproductor de verdad y no un botón suelto (03/10, "muy IA"). */
export const VIDEO_DURACION = '2:57'

export type Proveedor = 'bunny' | 'youtube' | 'vimeo' | 'mp4' | ''

export interface Video {
  proveedor: Proveedor
  /** Para iframes: la dirección del reproductor ya montada. Para mp4: el archivo. */
  src: string
}

/** De la URL que se pega a lo que necesita la página para reproducirlo y
 *  saber cuándo termina. */
export function leerVideo(url: string): Video {
  const u = (url || '').trim()
  if (!u) return { proveedor: '', src: '' }
  let m = u.match(/mediadelivery\.net\/(?:embed|play)\/(\d+)\/([\w-]+)/)
  if (m) return { proveedor: 'bunny', src: `https://iframe.mediadelivery.net/embed/${m[1]}/${m[2]}?autoplay=true&preload=true&responsive=true` }
  m = u.match(/(?:youtube\.com\/(?:watch\?v=|embed\/|shorts\/)|youtu\.be\/)([\w-]{6,})/)
  if (m) return { proveedor: 'youtube', src: `https://www.youtube-nocookie.com/embed/${m[1]}?enablejsapi=1&rel=0&modestbranding=1&playsinline=1&autoplay=1` }
  m = u.match(/vimeo\.com\/(?:video\/)?(\d+)/)
  if (m) return { proveedor: 'vimeo', src: `https://player.vimeo.com/video/${m[1]}?autoplay=1&title=0&byline=0&portrait=0` }
  if (/\.(mp4|webm|mov)(\?|$)/i.test(u)) return { proveedor: 'mp4', src: u }
  return { proveedor: '', src: '' }
}

/**
 * Los prefijos del teléfono, con bandera. Así el número llega siempre con
 * prefijo (el 29/09 llegó uno sin él y no hubo forma de escribirle) y de
 * paso se sabe el país sin preguntarlo. Primero los de donde viven los
 * alumnos; luego España y Latinoamérica; luego el resto de Europa.
 */
export const PREFIJOS: { pais: string; bandera: string; prefijo: string }[] = [
  { pais: 'Países Bajos', bandera: '🇳🇱', prefijo: '+31' },
  { pais: 'Bélgica', bandera: '🇧🇪', prefijo: '+32' },
  { pais: 'España', bandera: '🇪🇸', prefijo: '+34' },
  { pais: 'México', bandera: '🇲🇽', prefijo: '+52' },
  { pais: 'Colombia', bandera: '🇨🇴', prefijo: '+57' },
  { pais: 'Venezuela', bandera: '🇻🇪', prefijo: '+58' },
  { pais: 'Argentina', bandera: '🇦🇷', prefijo: '+54' },
  { pais: 'Perú', bandera: '🇵🇪', prefijo: '+51' },
  { pais: 'Chile', bandera: '🇨🇱', prefijo: '+56' },
  { pais: 'Ecuador', bandera: '🇪🇨', prefijo: '+593' },
  { pais: 'República Dominicana', bandera: '🇩🇴', prefijo: '+1' },
  { pais: 'Cuba', bandera: '🇨🇺', prefijo: '+53' },
  { pais: 'Uruguay', bandera: '🇺🇾', prefijo: '+598' },
  { pais: 'Paraguay', bandera: '🇵🇾', prefijo: '+595' },
  { pais: 'Bolivia', bandera: '🇧🇴', prefijo: '+591' },
  { pais: 'Guatemala', bandera: '🇬🇹', prefijo: '+502' },
  { pais: 'El Salvador', bandera: '🇸🇻', prefijo: '+503' },
  { pais: 'Honduras', bandera: '🇭🇳', prefijo: '+504' },
  { pais: 'Nicaragua', bandera: '🇳🇮', prefijo: '+505' },
  { pais: 'Costa Rica', bandera: '🇨🇷', prefijo: '+506' },
  { pais: 'Panamá', bandera: '🇵🇦', prefijo: '+507' },
  { pais: 'Estados Unidos', bandera: '🇺🇸', prefijo: '+1' },
  { pais: 'Alemania', bandera: '🇩🇪', prefijo: '+49' },
  { pais: 'Francia', bandera: '🇫🇷', prefijo: '+33' },
  { pais: 'Italia', bandera: '🇮🇹', prefijo: '+39' },
  { pais: 'Portugal', bandera: '🇵🇹', prefijo: '+351' },
  { pais: 'Reino Unido', bandera: '🇬🇧', prefijo: '+44' },
  { pais: 'Marruecos', bandera: '🇲🇦', prefijo: '+212' },
]

/**
 * El número completo: prefijo elegido + lo que escribió. Si ya lo escribió
 * con + o 00, se respeta tal cual (sabe lo que hace). Si empieza por un 0
 * (06…, 0470…, 07…), ese 0 es el de llamar dentro del país y se quita: con
 * prefijo internacional no va.
 */
export function telefonoCompleto(prefijo: string, numero: string): string {
  const crudo = (numero || '').trim()
  if (crudo.startsWith('+')) return `+${crudo.replace(/\D/g, '')}`
  const d = crudo.replace(/\D/g, '')
  if (!d) return ''
  if (d.startsWith('00')) return `+${d.slice(2)}`
  return `${prefijo}${d.replace(/^0/, '')}`
}

/** Lo que se recuerda entre el paso 1-2 y el paso 3, en el navegador. */
export const CLAVE_DATOS = 'nawar.admision.datos'
export const CLAVE_VIDEO = 'nawar.admision.video'
/** Por qué segundo iba, para seguir desde ahí si vuelve (03/10). */
export const CLAVE_POSICION = 'nawar.admision.posicion'

export interface DatosAdmision {
  first_name: string
  email: string
  phone: string
  pais: string
}
