/**
 * La cualificación antes de la llamada.
 *
 * Quien pide una llamada contesta siete preguntas. No son para conocerle:
 * son para que a la llamada lleguen los que tienen el nivel, el momento y
 * la disposición de invertir, y los demás reciban lo que les toca ahora
 * (la guía gratis) sin gastar una llamada. Es lo que hacen UDIA e ICO y lo
 * que está en el plan de la escuela: cualificar → llamada → cerrar hablando.
 *
 * Tres tipos de pregunta:
 *  - `opciones`: una lista, con letra (A, B, C…) y puntos por opción.
 *  - `escala`: del 1 al 5, con un texto en los extremos y en el medio.
 *  - `texto`: respuesta abierta. No puntúa; es para leerla antes de llamar.
 *
 * La puntuación es transparente a propósito: cada opción tiene sus puntos
 * aquí, a la vista, y se recalcula en el servidor (api/cualificacion.ts)
 * con esta misma tabla. Cambiar el corte o los puntos es cambiar un número.
 *
 * `etiqueta` es el nombre corto de la pregunta para la ficha del contacto y
 * el correo al equipo: el título largo (el que "vende") ahí solo estorba.
 */

export interface Opcion {
  valor: string
  texto: string
  puntos: number
}

interface Base {
  clave: string
  /** Nombre corto, para la ficha y el correo. */
  etiqueta: string
  /** Lo que ve la persona. Puede ser largo: aquí es donde se vende. */
  titulo: string
  ayuda?: string
}

export interface PreguntaOpciones extends Base {
  tipo: 'opciones'
  opciones: Opcion[]
}

export interface PreguntaEscala extends Base {
  tipo: 'escala'
  /** Texto bajo el 1, el 3 y el 5. */
  extremos: [string, string, string]
  /** Puntos por cada valor del 1 al 5. */
  puntos: [number, number, number, number, number]
}

export interface PreguntaTexto extends Base {
  tipo: 'texto'
  placeholder?: string
  /** Menos caracteres que esto no se acepta. */
  minimo: number
}

export type Pregunta = PreguntaOpciones | PreguntaEscala | PreguntaTexto

export const PREGUNTAS: Pregunta[] = [
  {
    tipo: 'opciones',
    clave: 'nivel',
    etiqueta: 'Nivel',
    titulo: '¿Cuál es tu nivel de neerlandés ahora mismo?',
    opciones: [
      { valor: 'cero', texto: 'Cero, empiezo desde nada', puntos: 2 },
      { valor: 'palabras', texto: 'Algunas palabras y frases sueltas', puntos: 2 },
      { valor: 'a1', texto: 'Tengo un A1 más o menos', puntos: 1 },
      { valor: 'a2', texto: 'A2 o más', puntos: 0 },
    ],
  },
  {
    tipo: 'opciones',
    clave: 'situacion',
    etiqueta: 'Dónde está',
    titulo: '¿Dónde estás?',
    opciones: [
      { valor: 'vivo', texto: 'Ya vivo en Países Bajos o Bélgica', puntos: 3 },
      { valor: 'pronto', texto: 'Me mudo en menos de 6 meses', puntos: 2 },
      { valor: 'futuro', texto: 'Me mudaré más adelante', puntos: 1 },
      { valor: 'otro', texto: 'Ninguna de estas', puntos: 0 },
    ],
  },
  {
    tipo: 'opciones',
    clave: 'motivo',
    etiqueta: 'Para qué',
    titulo: '¿Para qué lo necesitas?',
    opciones: [
      { valor: 'trabajo', texto: 'Trabajo: mejorar en el mío o encontrar otro', puntos: 2 },
      { valor: 'examen', texto: 'El examen de inburgering o el NT2', puntos: 2 },
      { valor: 'vida', texto: 'La vida diaria: médico, colegio, vecinos, familia', puntos: 2 },
      { valor: 'curiosidad', texto: 'Curiosidad, por ahora', puntos: 0 },
    ],
  },
  {
    tipo: 'texto',
    clave: 'objetivo',
    etiqueta: 'Qué espera conseguir',
    titulo:
      'Hablar neerlandés te abre puertas: el trabajo, el médico, el colegio de tus hijos, los vecinos. Pero cada persona tiene su propio motivo, y queremos conocer el tuyo para ver cómo podemos ayudarte.\n\n¿Qué esperas haber conseguido en tres meses con Nawar?',
    ayuda: 'Descríbelo con detalle y honestidad: de tus respuestas depende que te propongamos plaza o no.',
    placeholder: 'Escribe aquí tu respuesta…',
    minimo: 15,
  },
  {
    tipo: 'opciones',
    clave: 'horas',
    etiqueta: 'Horas a la semana',
    titulo: '¿Cuántas horas a la semana puedes dedicarle?',
    ayuda: 'Con menos de dos no se avanza, y preferimos decírtelo antes.',
    opciones: [
      { valor: 'menos2', texto: 'Menos de 2', puntos: 0 },
      { valor: '2a4', texto: 'Entre 2 y 4', puntos: 1 },
      { valor: '4a7', texto: 'Entre 4 y 7', puntos: 2 },
      { valor: 'mas7', texto: 'Más de 7', puntos: 2 },
    ],
  },
  {
    tipo: 'opciones',
    clave: 'inversion',
    etiqueta: 'Disponibilidad económica',
    // Sin cifra, a propósito: el precio se cuenta en la llamada, con la
    // persona delante. Aquí se mide la disposición, no se negocia.
    titulo:
      'Aprender el idioma es lo que más cambia tu vida aquí, y en Nawar no lo haces solo: clases en vivo, profesores que hablan tu idioma y un acompañamiento cercano durante todo el camino.\n\nSabiendo esto, ¿hasta qué punto puedes invertir en ti hoy?',
    opciones: [
      { valor: 'contado', texto: 'El dinero no es un problema: puedo pagarlo al contado', puntos: 3 },
      { valor: 'plazos', texto: 'Puedo hacerlo con un plan de pago a plazos', puntos: 2 },
      { valor: 'busco', texto: 'Ahora mismo me cuesta, pero estoy comprometido a encontrar la forma', puntos: 1 },
      { valor: 'no', texto: 'No tengo capacidad de inversión ni pienso buscarla', puntos: -10 },
    ],
  },
  {
    tipo: 'escala',
    clave: 'compromiso',
    etiqueta: 'Compromiso (1 a 5)',
    titulo: 'Con lo que has contestado, ¿hasta qué punto estás comprometido a aprender neerlandés de verdad en los próximos tres meses?',
    extremos: ['No es mi momento', 'Sin más…', 'Al 100 %'],
    puntos: [-5, -1, 0, 1, 2],
  },
]

/**
 * A partir de cuántos puntos se le ofrece la llamada. Máximo posible: 14.
 *
 * Quitadas el 23/09 (decisión del usuario): edad, ocupación, cuándo empieza y
 * quién decide. Para un ticket de 397 € cada pantalla de más cuesta leads;
 * edad y ocupación no cambiaban nada, casi no hay menores ni gente que no
 * decida por sí misma, y "cuándo empiezas" lo trabaja el closer en la
 * llamada: si es un proceso de admisión, es para empezar ya.
 */
export const CORTE_APTO = 8

/** Hasta dónde se guarda una respuesta abierta. */
export const MAX_TEXTO = 800

export interface Resultado {
  puntuacion: number
  apto: boolean
  /** Las respuestas, en cristiano, para la ficha del contacto. */
  respuestas: { pregunta: string; respuesta: string; puntos: number }[]
}

/** Letras para las opciones: A, B, C… */
export const LETRAS = 'ABCDEFGHIJ'

/** Puntúa un juego de respuestas {clave: valor}. Lo que no sea una opción
 *  válida cuenta cero y se apunta como "sin responder". Las respuestas
 *  abiertas van en `textos` y no puntúan. */
export function puntuar(respuestas: Record<string, string>, textos: Record<string, string> = {}): Resultado {
  let total = 0
  const detalle: Resultado['respuestas'] = []
  for (const p of PREGUNTAS) {
    if (p.tipo === 'opciones') {
      const op = p.opciones.find((o) => o.valor === respuestas[p.clave])
      total += op?.puntos ?? 0
      detalle.push({ pregunta: p.etiqueta, respuesta: op?.texto ?? 'Sin responder', puntos: op?.puntos ?? 0 })
    } else if (p.tipo === 'escala') {
      const n = Number(respuestas[p.clave])
      const valido = Number.isInteger(n) && n >= 1 && n <= 5
      const puntos = valido ? p.puntos[n - 1] : 0
      total += puntos
      detalle.push({
        pregunta: p.etiqueta,
        respuesta: valido ? `${n} de 5 (${n === 1 ? p.extremos[0] : n === 5 ? p.extremos[2] : n === 3 ? p.extremos[1] : ''})`.replace(' ()', '') : 'Sin responder',
        puntos,
      })
    } else {
      const t = (textos[p.clave] ?? '').toString().trim().slice(0, MAX_TEXTO)
      detalle.push({ pregunta: p.etiqueta, respuesta: t || 'Sin responder', puntos: 0 })
    }
  }
  return { puntuacion: total, apto: total >= CORTE_APTO, respuestas: detalle }
}
