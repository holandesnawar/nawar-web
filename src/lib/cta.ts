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
// Desde el 29/09 la matrícula ES /agendar: datos, unas preguntas y llamada
// reservada. El formulario corto (nombre, correo y teléfono) se retiró; sus
// direcciones redirigen aquí (src/lib/redirecciones.ts). Quien deja los
// datos y se va a mitad no se pierde: sale en la escuela como "No terminó".
export const CTA_PRINCIPAL = '/agendar'
