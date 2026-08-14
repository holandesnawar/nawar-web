import type { APIRoute } from 'astro'
import { getEstadoPlazas } from '../../lib/plazas'

export const prerender = false

/**
 * Estado de la matrícula para el navegador.
 *
 * La landing es estática y no puede leer MATRICULA_ABIERTA (es una variable de
 * servidor). Podría llamar directamente al endpoint de la academia, que tiene
 * CORS abierto, pero entonces se saltaría el interruptor manual. Así que pasa
 * por aquí, que es donde se combinan los dos.
 *
 * Cache-Control de 60 s, el mismo horizonte que la caché en memoria: si el CDN
 * de Vercel sirve la respuesta guardada, mejor.
 */
export const GET: APIRoute = async () => {
  const estado = await getEstadoPlazas()
  return new Response(JSON.stringify(estado), {
    status: 200,
    headers: {
      'Content-Type': 'application/json',
      'Cache-Control': 'public, max-age=30, s-maxage=60, stale-while-revalidate=120',
    },
  })
}
