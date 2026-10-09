/**
 * Por dónde ha pasado esta persona antes de dejar sus datos.
 *
 * El problema que resuelve: llegan matrículas y no se sabe qué sabe ya el
 * lead. Uno viene del pie del home y no ha visto nada de la formación; otro
 * pulsó el botón de la página de gracias de una guía y tampoco; y otro se leyó
 * la landing entera con el precio y el desglose. A los tres hay que escribirles
 * cosas distintas, y con el nombre y el correo no se distinguen.
 *
 * Lo único que de verdad cambia la conversación es **si ya ha visto el
 * precio**. Por eso las páginas se agrupan por lo que ENSEÑAN, no por su URL:
 * `/formacion-nawar-a0-a1` y `/formacion-a0-a1-sept-ads` son la misma página y
 * cuentan como una sola cosa, y la única que enseña la cifra va aparte.
 *
 * Se guarda en `sessionStorage`, o sea que dura la visita. No es seguimiento
 * entre sesiones: si vuelve mañana, empieza de cero. Es a propósito — lo que
 * interesa es el recorrido que acaba en el formulario, no un historial.
 *
 * Todo va en try: en el navegador dentro de Instagram y en ventanas privadas
 * el almacenamiento puede lanzar excepción, y un lead no se pierde por no
 * poder apuntar de dónde venía.
 */

const CLAVE = 'nawar_recorrido'
const TOPE = 12

/** Las páginas que dicen algo del producto, y qué enseña cada una. */
const PAGINAS: { prueba: RegExp; marca: string }[] = [
  // /proceso-agendar: el formulario de llamada solo, sin vídeo (06/10). /agendar ya
  // lleva al proceso de admisión.
  { prueba: /^\/(proceso-)?agendar\/?$/, marca: 'agendar' },
  // El proceso de admisión (02/10): el vídeo y, aparte, las preguntas.
  { prueba: /^\/proceso-de-admision\/paso-3\/?$/, marca: 'admision-preguntas' },
  { prueba: /^\/proceso-de-admision\/?$/, marca: 'admision' },
  // El embudo del anuncio de Facebook/Instagram (07/10; antes /formacion/v2):
  // la página que explica la formación y pide los datos, luego el vídeo y
  // luego las preguntas. Su marca propia, `anuncio-fb`, es la que dice en el
  // panel que el lead vino del anuncio. El vídeo y las preguntas cuentan como
  // los del proceso de admisión: son lo mismo.
  { prueba: /^\/formacion-nawar-fb\/proceso-de-admision\/?$/, marca: 'admision-preguntas' },
  { prueba: /^\/formacion-nawar-fb\/vsl\/?$/, marca: 'admision' },
  { prueba: /^\/formacion-nawar-fb\/?$/, marca: 'anuncio-fb' },
  // La misma página para la gente de la web, con la barra y el pie de
  // siempre (09/10). Marca propia para no confundirla con el anuncio.
  { prueba: /^\/formacion\/proceso-de-admision\/?$/, marca: 'admision-preguntas' },
  { prueba: /^\/formacion\/vsl\/?$/, marca: 'admision' },
  { prueba: /^\/formacion\/?$/, marca: 'formacion-web' },
  // ⚠️ La única con precio. Es la que parte a los leads en dos grupos.
  { prueba: /^\/formacion-a0-a1\/?$/, marca: 'landing-precio' },
  // ⚠️ La otra ruta CON precio y su formulario de pago (02/10): no se
  // apuntaban, así que quien entraba por un enlace directo (un correo, un
  // mensaje) llegaba a la caja "sin recorrido" y no se sabía cómo.
  { prueba: /^\/formacion-nawar\/?$/, marca: 'landing-precio' },
  { prueba: /^\/matricula-formacion-nawar\/?$/, marca: 'matricula-pago' },
  // Las dos rutas de la landing de captación: mismo contenido, sin cifras.
  { prueba: /^\/formacion-a0-a1-sept-ads\/?$/, marca: 'landing' },
  { prueba: /^\/formacion-nawar-a0-a1\/?$/, marca: 'landing' },
  // Las guías. La página de gracias cuenta aparte: es donde está el botón que
  // lleva a la formación, así que saber si pasó por ella explica el salto.
  { prueba: /^\/guia\/bases-neerlandes(-a)?\/gracias\/?$/, marca: 'gracias-bases' },
  { prueba: /^\/guia\/bases-neerlandes(-a)?\/?$/, marca: 'guia-bases' },
  { prueba: /^\/guia\/hebben-zijn(-a)?\/gracias\/?$/, marca: 'gracias-hebben' },
  { prueba: /^\/guia\/hebben-zijn(-a)?\/?$/, marca: 'guia-hebben' },
  { prueba: /^\/$/, marca: 'home' },
]

/**
 * Apunta la página actual, si es de las que cuentan.
 *
 * Se llama desde el Layout, o sea en TODAS las páginas: así una página nueva
 * solo tiene que añadir su regla aquí arriba, y no hay que acordarse de tocar
 * la página. Las que no encajan no guardan nada.
 */
export function registrarPagina(): void {
  try {
    const ruta = window.location.pathname
    const encontrada = PAGINAS.find((p) => p.prueba.test(ruta))
    if (!encontrada) return

    const visto = leerRecorrido()
    // Recargar o volver atrás no cuenta como paso nuevo: solo se apunta si
    // cambia respecto a lo último, para que el recorrido se lea como un camino.
    if (visto[visto.length - 1] === encontrada.marca) return

    const nuevo = [...visto, encontrada.marca].slice(-TOPE)
    sessionStorage.setItem(CLAVE, JSON.stringify(nuevo))
  } catch {
    /* sin almacenamiento, el lead entra igual pero sin recorrido */
  }
}

/** Las páginas por las que ha pasado, en orden. */
export function leerRecorrido(): string[] {
  try {
    const crudo = sessionStorage.getItem(CLAVE)
    if (!crudo) return []
    const d = JSON.parse(crudo)
    return Array.isArray(d) ? d.filter((x) => typeof x === 'string').slice(-TOPE) : []
  } catch {
    return []
  }
}

/**
 * Lo que se manda con el formulario.
 *
 * `referrer` solo cuando es de fuera: dentro de la web el recorrido ya lo dice
 * mejor, y guardar nuestra propia URL anterior es ruido. De fuera sí importa
 * —Instagram, un correo, una búsqueda—, y es lo único que explica a alguien
 * que aterriza directamente en el formulario sin pasar por ninguna página.
 */
export function contextoDelLead(): { recorrido: string[]; referrer: string } {
  let referrer = ''
  try {
    const r = document.referrer || ''
    if (r && !r.startsWith(window.location.origin)) {
      referrer = new URL(r).hostname.slice(0, 120)
    }
  } catch {
    /* referrer ilegible: se queda vacío */
  }
  return { recorrido: leerRecorrido(), referrer }
}
