/**
 * La cualificación antes de la llamada.
 *
 * Quien pide una llamada contesta seis preguntas. No son para conocerle:
 * son para que a la llamada lleguen los que tienen el nivel, el momento y
 * la disposición de invertir, y los demás reciban lo que les toca ahora
 * (la guía gratis) sin gastar una llamada. Es lo que hace UDIA y lo que
 * está en el plan de la escuela: cualificar → llamada → cerrar hablando.
 *
 * La puntuación es transparente a propósito: cada opción tiene sus puntos
 * aquí, a la vista, y se recalcula en el servidor (api/cualificacion.ts)
 * con esta misma tabla. Cambiar el corte o los puntos es cambiar un número.
 */

export interface Opcion {
  valor: string
  texto: string
  puntos: number
}

export interface Pregunta {
  clave: string
  titulo: string
  ayuda?: string
  opciones: Opcion[]
}

export const PREGUNTAS: Pregunta[] = [
  {
    clave: 'nivel',
    titulo: '¿Cuál es tu nivel de neerlandés ahora mismo?',
    opciones: [
      { valor: 'cero', texto: 'Cero, empiezo desde nada', puntos: 2 },
      { valor: 'palabras', texto: 'Algunas palabras y frases sueltas', puntos: 2 },
      { valor: 'a1', texto: 'Tengo un A1 más o menos', puntos: 1 },
      { valor: 'a2', texto: 'A2 o más', puntos: 0 },
    ],
  },
  {
    clave: 'situacion',
    titulo: '¿Dónde estás?',
    opciones: [
      { valor: 'vivo', texto: 'Ya vivo en Países Bajos o Bélgica', puntos: 3 },
      { valor: 'pronto', texto: 'Me mudo en menos de 6 meses', puntos: 2 },
      { valor: 'futuro', texto: 'Me mudaré más adelante', puntos: 1 },
      { valor: 'otro', texto: 'Ninguna de estas', puntos: 0 },
    ],
  },
  {
    clave: 'motivo',
    titulo: '¿Para qué lo necesitas?',
    opciones: [
      { valor: 'trabajo', texto: 'Trabajo: mejorar en el mío o encontrar otro', puntos: 2 },
      { valor: 'examen', texto: 'El examen de inburgering o el NT2', puntos: 2 },
      { valor: 'vida', texto: 'La vida diaria: médico, colegio, vecinos, familia', puntos: 2 },
      { valor: 'curiosidad', texto: 'Curiosidad, por ahora', puntos: 0 },
    ],
  },
  {
    clave: 'cuando',
    titulo: '¿Cuándo quieres empezar?',
    opciones: [
      { valor: 'ya', texto: 'Esta semana', puntos: 3 },
      { valor: 'mes', texto: 'Este mes', puntos: 2 },
      { valor: 'trimestre', texto: 'En uno a tres meses', puntos: 1 },
      { valor: 'mirando', texto: 'Solo estoy mirando', puntos: 0 },
    ],
  },
  {
    clave: 'horas',
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
    clave: 'inversion',
    titulo: 'La formación cuesta 397 € (pago único, o a plazos con Klarna). Si en la llamada ves que encaja, ¿estás en disposición de invertirlo?',
    opciones: [
      { valor: 'si', texto: 'Sí, si encaja lo hago', puntos: 3 },
      { valor: 'dudo', texto: 'Quiero saber más en la llamada', puntos: 1 },
      { valor: 'no', texto: 'Ahora mismo no', puntos: -10 },
    ],
  },
]

/** A partir de cuántos puntos se le ofrece la llamada. */
export const CORTE_APTO = 7

export interface Resultado {
  puntuacion: number
  apto: boolean
  /** Las respuestas, en cristiano, para la ficha del contacto. */
  respuestas: { pregunta: string; respuesta: string; puntos: number }[]
}

/** Puntúa un juego de respuestas {clave: valor}. Lo que no sea una opción
 *  válida cuenta cero y se apunta como "sin responder". */
export function puntuar(respuestas: Record<string, string>): Resultado {
  let total = 0
  const detalle: Resultado['respuestas'] = []
  for (const p of PREGUNTAS) {
    const op = p.opciones.find((o) => o.valor === respuestas[p.clave])
    total += op?.puntos ?? 0
    detalle.push({ pregunta: p.titulo, respuesta: op?.texto ?? 'Sin responder', puntos: op?.puntos ?? 0 })
  }
  return { puntuacion: total, apto: total >= CORTE_APTO, respuestas: detalle }
}
