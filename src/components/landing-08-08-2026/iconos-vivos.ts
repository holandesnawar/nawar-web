/**
 * Iconos ilustrados de la landing.
 *
 * Los que había eran de trazo fino a un solo color: correctos y
 * aburridos. Estos son planos y macizos, a dos azules de marca más el
 * índigo, con un destello suelto para darles gracia. Es el lenguaje de
 * los mockups que pasó Rida, traído a nuestra paleta en vez de copiado
 * en rojo y azul.
 *
 * Se dibujan en una caja de 64×64 y llenan unos 56, así que se pueden
 * pintar a cualquier tamaño sin retocarlos. No usan currentColor a
 * propósito: son ilustraciones, no iconos de interfaz, y tienen que
 * verse igual en cualquier tarjeta.
 *
 * Paleta:
 *   #1D0084  índigo, las masas oscuras
 *   #0b6df0  azul vivo, la forma principal
 *   #4da3ff  azul claro, el segundo plano
 *   #7dbcff  destellos
 */

const destello = (x: number, y: number, r = 6) =>
  `<path d="M${x} ${y - r}l${r * 0.28} ${r * 0.72} ${r * 0.72} ${r * 0.28}-${r * 0.72} ${r * 0.28}-${r * 0.28} ${r * 0.72}-${r * 0.28}-${r * 0.72}-${r * 0.72}-${r * 0.28} ${r * 0.72}-${r * 0.28}z" fill="#7dbcff"/>`

const wrap = (contenido: string) =>
  `<svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">${contenido}</svg>`

export const ICONOS: Record<string, string> = {
  /* ── El coste de seguir igual ─────────────────────────────── */

  // Reloj de arena: el tiempo que se va
  tiempo: wrap(`
    <rect x="13" y="7" width="34" height="7" rx="3.5" fill="#1D0084"/>
    <rect x="13" y="50" width="34" height="7" rx="3.5" fill="#1D0084"/>
    <path d="M19 14h22v5c0 7-8 10-8 13s8 6 8 13v5H19v-5c0-7 8-10 8-13s-8-6-8-13v-5z" fill="#4da3ff"/>
    <path d="M30 34c1 2 7 5 7 11v2H23v-2c0-6 6-9 7-11z" fill="#0b6df0"/>
    <circle cx="30" cy="22" r="2.6" fill="#0b6df0"/>
    ${destello(54, 13, 7)}
  `),

  // Maletín con una flecha que se escapa: las oportunidades
  oportunidad: wrap(`
    <path d="M21 20v-3a7 7 0 017-7h6a7 7 0 017 7v3h-7v-2.5a1.5 1.5 0 00-1.5-1.5h-3a1.5 1.5 0 00-1.5 1.5V20h-7z" fill="#1D0084"/>
    <rect x="5" y="20" width="52" height="34" rx="7" fill="#0b6df0"/>
    <rect x="5" y="32" width="52" height="6" fill="#1D0084" opacity=".38"/>
    <rect x="26" y="30" width="10" height="10" rx="3" fill="#4da3ff"/>
    <path d="M45 17L57 5" stroke="#4da3ff" stroke-width="5" stroke-linecap="round"/>
    <path d="M47 5h10v10" stroke="#4da3ff" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
  `),

  // Dos burbujas, una apagada: quedarte fuera de la conversación
  conversacion: wrap(`
    <path d="M4 15a8 8 0 018-8h25a8 8 0 018 8v13a8 8 0 01-8 8H20l-10 8v-8.7A8 8 0 014 28V15z" fill="#0b6df0"/>
    <circle cx="16" cy="21.5" r="3.1" fill="#fff"/>
    <circle cx="25" cy="21.5" r="3.1" fill="#fff"/>
    <circle cx="34" cy="21.5" r="3.1" fill="#fff"/>
    <path d="M60 34a7 7 0 00-7-7H41a7 7 0 00-7 7v8a7 7 0 007 7h7l8 6v-6.6A7 7 0 0060 42v-8z" fill="#4da3ff" opacity=".55"/>
    <path d="M42 34l10 10M52 34l-10 10" stroke="#1D0084" stroke-width="3.4" stroke-linecap="round" opacity=".45"/>
  `),

  // Escudo con signo: la inseguridad que se acumula
  inseguridad: wrap(`
    <path d="M32 5l21 8v17c0 14-9 24-21 29-12-5-21-15-21-29V13l21-8z" fill="#0b6df0"/>
    <path d="M32 5v54c-12-5-21-15-21-29V13l21-8z" fill="#1D0084" opacity=".28"/>
    <rect x="28.6" y="19" width="6.8" height="17" rx="3.4" fill="#fff"/>
    <circle cx="32" cy="43" r="3.9" fill="#fff"/>
    ${destello(56, 12, 6)}
  `),

  // Pasaporte y globo: vivir aquí de visitante
  pasaporte: wrap(`
    <rect x="10" y="5" width="38" height="54" rx="6" fill="#1D0084"/>
    <rect x="15" y="10" width="33" height="44" rx="4" fill="#0b6df0"/>
    <circle cx="31" cy="26" r="11" fill="#4da3ff"/>
    <path d="M31 15c-4 4-4 18 0 22M31 15c4 4 4 18 0 22M20.5 22h21M20.5 30h21" stroke="#1D0084" stroke-width="2.2" stroke-linecap="round" opacity=".55"/>
    <rect x="22" y="43" width="18" height="4.4" rx="2.2" fill="#4da3ff" opacity=".75"/>
    ${destello(55, 49, 6)}
  `),

  /* ── Lo que cambia cuando hablas ──────────────────────────── */

  // Una puerta que se abre: entrar a entrevistas.
  //
  // Aquí hubo dos intentos de apretón de manos y los dos fracasaron:
  // a 52 px dos manos entrelazadas son una mancha, y con la geometría
  // simplificada el resultado se leía como una pesa de gimnasio. La
  // puerta con la flecha entrando se entiende a la primera y además
  // dice literalmente lo que dice el título.
  trabajo: wrap(`
    <rect x="22" y="3" width="36" height="58" rx="7" fill="#1D0084"/>
    <rect x="27" y="8" width="26" height="48" rx="4.5" fill="#0b6df0"/>
    <circle cx="47" cy="32" r="3" fill="#fff"/>
    <path d="M4 32h14" stroke="#4da3ff" stroke-width="6" stroke-linecap="round"/>
    <path d="M13 24l8 8-8 8" stroke="#4da3ff" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
    ${destello(12, 12, 6)}
  `),

  // Burbujas con rayo: entender y responder al momento
  responder: wrap(`
    <path d="M4 14a8 8 0 018-8h27a8 8 0 018 8v14a8 8 0 01-8 8H21l-10 8v-8.6A8 8 0 014 28V14z" fill="#0b6df0"/>
    <path d="M28 12l-9 12h6l-2 9 9-12h-6l2-9z" fill="#fff"/>
    <path d="M60 39a6 6 0 00-6-6H38a6 6 0 00-6 6v7a6 6 0 006 6h11l7 5v-5.4a6 6 0 004-5.6v-7z" fill="#4da3ff"/>
    <circle cx="41" cy="42.5" r="2.6" fill="#1D0084" opacity=".5"/>
    <circle cx="48" cy="42.5" r="2.6" fill="#1D0084" opacity=".5"/>
  `),

  // Documento con sello: tus gestiones, tuyas
  gestiones: wrap(`
    <path d="M12 9a6 6 0 016-6h18l14 14v34a6 6 0 01-6 6H18a6 6 0 01-6-6V9z" fill="#4da3ff"/>
    <path d="M36 3l14 14H40a4 4 0 01-4-4V3z" fill="#1D0084" opacity=".45"/>
    <rect x="20" y="24" width="24" height="4.2" rx="2.1" fill="#fff" opacity=".85"/>
    <rect x="20" y="33" width="17" height="4.2" rx="2.1" fill="#fff" opacity=".85"/>
    <circle cx="45" cy="46" r="14" fill="#0b6df0"/>
    <path d="M39 46.2l4.4 4.4L52 42" stroke="#fff" stroke-width="4.2" stroke-linecap="round" stroke-linejoin="round"/>
  `),

  // Personas y corazón: dejar de sentirte de fuera
  gente: wrap(`
    <circle cx="20" cy="19" r="9" fill="#0b6df0"/>
    <path d="M4 51c0-9 7-15 16-15s16 6 16 15v3a3 3 0 01-3 3H7a3 3 0 01-3-3v-3z" fill="#0b6df0"/>
    <circle cx="45" cy="23" r="8" fill="#4da3ff"/>
    <path d="M32 52c0-8.5 6-14 13-14s13 5.5 13 14v2a3 3 0 01-3 3H35a3 3 0 01-3-3v-2z" fill="#4da3ff"/>
    <path d="M47 4.5c2.6-2.6 6.8-2.6 9.4 0 2.6 2.6 2.6 6.8 0 9.4L47 23.3l-9.4-9.4c-2.6-2.6-2.6-6.8 0-9.4 2.6-2.6 6.8-2.6 9.4 0z" fill="#1D0084" opacity=".22"/>
  `),

  // Chincheta y avión: moverte sin depender de nadie
  moverte: wrap(`
    <path d="M22 3c10 0 18 8 18 18 0 12-18 30-18 30S4 33 4 21C4 11 12 3 22 3z" fill="#0b6df0"/>
    <circle cx="22" cy="20.5" r="7.5" fill="#fff"/>
    <path d="M58 26l-14 6-8-3-4 2 6 5-2 6 4 1 5-5 8 4 6-14a2.6 2.6 0 00-1-2z" fill="#4da3ff"/>
    <path d="M12 56h40" stroke="#1D0084" stroke-width="4" stroke-linecap="round" stroke-dasharray="1 9" opacity=".45"/>
    ${destello(54, 10, 6)}
  `),

  // Persona hablando con destello: hablar sin ensayar la frase
  confianza: wrap(`
    <circle cx="26" cy="18" r="11" fill="#0b6df0"/>
    <path d="M6 53c0-11 9-18 20-18s20 7 20 18v3a3 3 0 01-3 3H9a3 3 0 01-3-3v-3z" fill="#0b6df0"/>
    <path d="M40 6h16a5 5 0 015 5v9a5 5 0 01-5 5h-3l-6 5v-5h-7a5 5 0 01-5-5v-9a5 5 0 015-5z" fill="#4da3ff"/>
    <circle cx="44" cy="15.5" r="2.3" fill="#1D0084" opacity=".55"/>
    <circle cx="51" cy="15.5" r="2.3" fill="#1D0084" opacity=".55"/>
    ${destello(11, 34, 7)}
  `),
}
