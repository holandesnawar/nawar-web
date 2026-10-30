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
 * en WebP. Papel, bio y orden (Rida, Paul, Bas, Luna), también del usuario el
 * 30/10: si cambia algo, que lo diga él; no añadir datos que no haya dado.
 */
export interface MiembroEquipo {
  nombre: string
  rol: string
  foto: string
  bio: string
}

export const EQUIPO: MiembroEquipo[] = [
  {
    nombre: 'Rida Nawar',
    rol: 'Fundador · Creador del método',
    foto: '/img/equipo/rida.webp',
    bio: 'Fundador de Holandés Nawar y **creador del método**. Es **hispanohablante** y pasó por lo mismo que tú al aprender neerlandés.',
  },
  {
    nombre: 'Paul Plaat',
    rol: 'Director académico',
    foto: '/img/equipo/paul.webp',
    bio: '**Director académico** de la escuela. Se encarga de los **módulos de la formación**: qué aprendes en cada uno y en qué orden.',
  },
  {
    nombre: 'Bas Wanders',
    rol: 'Profesor',
    foto: '/img/equipo/bas.webp',
    bio: 'Profesor en la escuela y parte del **equipo docente**. Se encarga también de los **módulos** de la formación.',
  },
  {
    nombre: 'Luna Zegers',
    rol: 'Profesora nativa',
    foto: '/img/equipo/luna.webp',
    bio: '**Nativa** y profesora en la escuela. Da la **clase semanal** y la **masterclass**, y se encarga también de los **módulos**.',
  },
]
