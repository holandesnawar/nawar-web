/**
 * Estado de la matrícula: ¿están abiertas las puertas?
 *
 * Manda la conjunción de dos cosas:
 *
 *   1. MATRICULA_ABIERTA, variable de entorno SOLO DE SERVIDOR (sin prefijo
 *      PUBLIC_, para que no acabe en el bundle del navegador). Vale como
 *      interruptor manual: poniéndola a "no" se cierra al instante, sin
 *      esperar a que se llenen las plazas.
 *   2. El campo `abierta` del endpoint de la academia, que ya combina el tope
 *      de plazas con el interruptor del servidor.
 *
 * Abierto = MATRICULA_ABIERTA ≠ "no"  Y  endpoint dice abierta: true.
 *
 * Si el endpoint falla NO cerramos por nuestra cuenta: nos quedamos con lo que
 * diga MATRICULA_ABIERTA. La cerradura de verdad está en el servidor de la
 * academia, que rechaza cualquier matrícula nueva pase lo que pase aquí; lo
 * peor que puede ocurrir si nos equivocamos hacia el lado abierto es que
 * alguien llegue al formulario y reciba un mensaje limpio. Equivocarnos hacia
 * el lado cerrado, en cambio, sería dejar de vender por un timeout.
 */

import { ESCUELA_URL } from './escuela'

const ENDPOINT = `${ESCUELA_URL}/api/v1/payments/plazas`
const TIMEOUT_MS = 2500
const CACHE_MS = 60_000

/** Mensaje que devuelve la academia con las puertas cerradas. Se repite aquí
 *  para poder responder 403 sin llegar a llamarla. */
export const MENSAJE_CERRADO =
  'Las plazas de esta convocatoria están completas. Apúntate a la lista de espera y te avisamos de la próxima.'

export const RUTA_LISTA_ESPERA = '/lista-de-espera'

export interface EstadoPlazas {
  /** true = se puede pagar. */
  abierta: boolean
  /** Plazas libres, o null si no hay tope configurado o no se pudo consultar. */
  quedan: number | null
}

/** Caché en memoria del proceso. En serverless cada instancia tiene la suya,
 *  que es justo lo que queremos: evita machacar a la academia en cada visita
 *  sin necesidad de un almacén compartido. */
let cache: { estado: EstadoPlazas; expira: number } | null = null

function interruptorManual(): boolean {
  const raw =
    (import.meta.env.MATRICULA_ABIERTA as string | undefined) ??
    (typeof process !== 'undefined' ? process.env.MATRICULA_ABIERTA : undefined)
  // Solo "no" cierra. Sin definir, vacía o cualquier otra cosa = abierta.
  return (raw ?? '').trim().toLowerCase() !== 'no'
}

export async function getEstadoPlazas(): Promise<EstadoPlazas> {
  const manual = interruptorManual()

  // Cerrado a mano: ni consultamos. Es instantáneo y no depende de la red.
  if (!manual) return { abierta: false, quedan: null }

  if (cache && Date.now() < cache.expira) return cache.estado

  let estado: EstadoPlazas = { abierta: true, quedan: null }

  try {
    const ctrl = new AbortController()
    const t = setTimeout(() => ctrl.abort(), TIMEOUT_MS)
    const res = await fetch(ENDPOINT, { signal: ctrl.signal, headers: { accept: 'application/json' } })
    clearTimeout(t)

    if (res.ok) {
      const data: any = await res.json().catch(() => null)
      if (data && typeof data.abierta === 'boolean') {
        const quedan = typeof data.quedan === 'number' ? data.quedan : null
        estado = { abierta: data.abierta, quedan }
      } else {
        console.warn('[plazas] respuesta sin campo `abierta`, se mantiene abierto')
      }
    } else {
      console.warn('[plazas] endpoint respondió', res.status, '— se mantiene abierto')
    }
  } catch (e) {
    // Timeout, DNS, caída… da igual: no cerramos la tienda por nuestra cuenta.
    console.warn('[plazas] no se pudo consultar el endpoint, se mantiene abierto:', e)
  }

  cache = { estado, expira: Date.now() + CACHE_MS }
  return estado
}
