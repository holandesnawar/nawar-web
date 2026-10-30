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
 * - `rol`: lo que hace en la escuela. Vacío = solo el nombre.
 * - `bio`: dos o tres frases; lo que va entre ** sale en negrita. Vacía = la
 *   tarjeta no tiene cortina (solo foto y nombre).
 *
 * Las fotos las pasó el usuario el 30/10 (docs.holandesnawar.com/img/Profes/,
 * 1254 × 1254 con el fondo azul ya puesto); aquí van recortadas a 3:4, 600 × 800
 * en WebP. ⚠️ El papel y la bio de cada uno están PENDIENTES de que los mande:
 * no inventarlos.
 */
export interface MiembroEquipo {
  nombre: string
  rol: string
  foto: string
  bio: string
}

export const EQUIPO: MiembroEquipo[] = [
  { nombre: 'Bas', rol: '', foto: '/img/equipo/bas.webp', bio: '' },
  { nombre: 'Luna', rol: '', foto: '/img/equipo/luna.webp', bio: '' },
  { nombre: 'Paul', rol: '', foto: '/img/equipo/paul.webp', bio: '' },
  { nombre: 'Rida', rol: '', foto: '/img/equipo/rida.webp', bio: '' },
]
