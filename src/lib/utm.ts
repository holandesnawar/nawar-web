/**
 * De qué anuncio viene cada visita.
 *
 * Los `utm_*` llegan en la dirección de la página a la que Meta manda a la
 * gente. El problema es que ahí se quedan: en cuanto la persona toca un enlace
 * o recarga, desaparecen, y si el formulario los lee solo en el momento de
 * enviar, la mitad de los leads entran sin procedencia. Por eso se guardan en
 * cuanto la página abre y se leen después.
 *
 * `sessionStorage` y no `localStorage` a propósito: dura lo que dura la visita.
 * Con localStorage, alguien que vino de un anuncio en marzo seguiría contando
 * como ese anuncio en junio, y la campaña vieja se llevaría leads que no son
 * suyos.
 *
 * Todo va envuelto en try: en el navegador de Instagram y en las ventanas
 * privadas, tocar el almacenamiento puede lanzar excepción, y un lead no se
 * puede perder por no haber podido guardar de dónde venía.
 */

export type UTM = {
  utmSource: string
  utmMedium: string
  utmCampaign: string
}

const CLAVE = 'nawar_utm'
const VACIO: UTM = { utmSource: '', utmMedium: '', utmCampaign: '' }

/**
 * Llamar al cargar la página. Si la dirección trae `utm_*`, los guarda.
 *
 * Solo escribe cuando hay algo que escribir: si esta visita no trae UTM, lo
 * guardado antes se respeta. Alguien puede llegar por el anuncio, mirar dos
 * páginas y volver al formulario, y esa persona sigue siendo del anuncio.
 */
export function guardarUTM(): void {
  try {
    const p = new URLSearchParams(window.location.search)
    const datos: UTM = {
      utmSource: (p.get('utm_source') || '').slice(0, 120),
      utmMedium: (p.get('utm_medium') || '').slice(0, 120),
      utmCampaign: (p.get('utm_campaign') || '').slice(0, 120),
    }
    if (!datos.utmSource && !datos.utmMedium && !datos.utmCampaign) return
    sessionStorage.setItem(CLAVE, JSON.stringify(datos))
  } catch {
    /* sin almacenamiento se sigue igual, solo que sin procedencia */
  }
}

/** Lo guardado en esta visita. Todo vacío si vino por su cuenta. */
export function leerUTM(): UTM {
  try {
    const crudo = sessionStorage.getItem(CLAVE)
    if (!crudo) return { ...VACIO }
    const d = JSON.parse(crudo)
    return {
      utmSource: typeof d?.utmSource === 'string' ? d.utmSource : '',
      utmMedium: typeof d?.utmMedium === 'string' ? d.utmMedium : '',
      utmCampaign: typeof d?.utmCampaign === 'string' ? d.utmCampaign : '',
    }
  } catch {
    return { ...VACIO }
  }
}
