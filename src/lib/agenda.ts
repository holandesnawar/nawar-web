/**
 * El calendario de la llamada de admisión (Calendly), en UN solo sitio.
 *
 * Desde el 04/11/2026 es el evento «por turnos» del equipo (Calendly Teams):
 * Calendly elige a qué closer le toca y le pone la llamada en su calendario,
 * con su Google Meet o su Zoom. La escuela reconoce sola ese evento (es el
 * por turnos) y le asigna la llamada al closer que eligió Calendly.
 *
 * Antes eran seis copias del enlace viejo (el evento individual de una sola
 * cuenta), una por página. PUBLIC_AGENDA_URL en Vercel lo sigue cambiando sin
 * tocar código, salvo si todavía apunta al enlace viejo: ese se ignora, para
 * que una variable olvidada no siga mandando a la gente al evento de antes.
 */

export const AGENDA_VIEJA = 'https://calendly.com/holandesnawar/llamada-de-consultoria'
export const AGENDA_POR_DEFECTO = 'https://calendly.com/d/dtzn-ywx-fcs/llamada-de-consultoria-hn'

/** La dirección del calendario: la de la variable, si vale, o la del equipo. */
export function direccionAgenda(variable?: string | null): string {
  const v = (variable || '').trim().replace(/\/+$/, '')
  if (!v || v === AGENDA_VIEJA || !/^https:\/\//.test(v)) return AGENDA_POR_DEFECTO
  return v
}

export const AGENDA_URL = direccionAgenda(import.meta.env.PUBLIC_AGENDA_URL as string | undefined)
