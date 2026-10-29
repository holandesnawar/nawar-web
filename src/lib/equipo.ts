/**
 * El equipo de la escuela, para «Quién te acompaña en el camino»
 * (components/black-friday/EquipoNawar.astro).
 *
 * ⚠️ Solo personas de verdad, con su foto, su nombre y lo que hacen. Mientras
 * la lista esté vacía, la sección NO sale en ninguna página. (En /v4/pruebas
 * hay otra lista con nombres inventados para probar el diseño: no copiarla.)
 *
 * - `foto`: la ruta de la foto dentro de public/ (p. ej. '/img/equipo/rida.webp'),
 *   vertical 3:4. Vacío = sus iniciales sobre el azul.
 * - `bio`: dos o tres frases; lo que va entre ** sale en negrita.
 */
export interface MiembroEquipo {
  nombre: string
  rol: string
  foto: string
  bio: string
}

export const EQUIPO: MiembroEquipo[] = []
