import type { APIRoute } from 'astro'
import { REDIRECCIONES } from '../../lib/redirecciones'

export const prerender = false

/**
 * El inventario de páginas de esta web, sacado del código en cada despliegue.
 *
 * Lo lee Panel → Webs de la escuela para enseñar qué páginas existen de
 * verdad, cuáles redirigen y cuáles no están clasificadas en su mapa. Antes
 * ese mapa estaba escrito a mano y se quedaba viejo sin avisar.
 *
 * Público y solo de lectura: es lo mismo que ver el sitemap. Con CORS abierto
 * porque lo pide el navegador del administrador desde app.holandesnawar.com.
 */

// import.meta.glob resuelve en el build: la lista es la de los archivos que
// existen en este despliegue, no una copia escrita a mano.
const archivos = import.meta.glob('/src/pages/**/*.astro')

function rutaDe(archivo: string): string | null {
  let r = archivo.replace(/^\/src\/pages/, '').replace(/\.astro$/, '')
  if (r.endsWith('/index')) r = r.slice(0, -'/index'.length) || '/'
  if (r === '') r = '/'
  // Fuera lo que no es una página para personas.
  if (r === '/404' || r.includes('[...') || r.startsWith('/_')) return null
  // Las dinámicas ([slug]) se enseñan con su patrón.
  return r
}

export const GET: APIRoute = async () => {
  const paginas = Object.keys(archivos)
    .map(rutaDe)
    .filter((r): r is string => !!r)
    .sort()
  const redirecciones = Object.entries(REDIRECCIONES).map(([desde, r]) => ({ desde, hacia: r.destination, status: r.status }))
  return new Response(JSON.stringify({ paginas, redirecciones, generado: new Date().toISOString() }), {
    status: 200,
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*',
      'Cache-Control': 'public, max-age=300',
    },
  })
}
