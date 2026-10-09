/**
 * A dónde llevan los botones principales de la web.
 *
 * Existe porque este destino cambia a menudo —lista de espera entre
 * convocatorias, landing durante el lanzamiento, matrícula cuando se recogen
 * solicitudes— y estaba escrito a mano en cada componente. Cambiarlo
 * significaba acordarse de cuatro archivos y siempre se quedaba uno.
 *
 * Aquí se toca UNA línea y se mueven todos a la vez: el botón "Apúntate" del
 * menú, el del final del proceso y el de la sección de valor.
 *
 * ⚠️ Si el destino deja de ser un formulario de contacto, mira también el
 * TEXTO de los botones. Un botón que dice "Únete a la lista de espera" y lleva
 * a una matrícula miente, y el visitante lo nota en el primer segundo.
 *
 * Los textos viven en src/data/landing.json (ctaText, ctaPrimary).
 */
// Decidido con el usuario el 29/09, después de dar una vuelta:
//  · Botones generales (menú de toda la web, home, Nuestra visión, blog) →
//    el FORMULARIO CORTO (nombre, correo y teléfono obligatorio): es tráfico
//    frío y lo corto capta más.
//  · Landings sin precio (anuncios) → /agendar (LandingCaptacion y cía.).
//  · Landings con precio → el pago.
// Se probó a mandar todo a /agendar y se deshizo el mismo día.
// 03/10, lanzamiento del proceso de admisión (pedido del usuario): los
// botones generales van a /proceso-de-admision (datos → vídeo → preguntas).
// El formulario corto /matricula-a0-a1 sigue vivo por si hay que volver.
// 09/10 (usuario, tras verla): los botones generales van a /formacion, la
// página que explica la formación con la barra y el pie de la web (copia de
// la del anuncio, /formacion-nawar-fb, con su propio camino y su marca
// `formacion-web` en el recorrido). /proceso-de-admision sigue vivo: ahí
// llega /agendar y lo que ya se envió con ese enlace.
export const CTA_PRINCIPAL = '/formacion'
