/**
 * El subdominio blackfriday.holandesnawar.com, servido por esta misma web.
 *
 * El problema: en Vercel las páginas se sirven por su ruta, no por el
 * dominio. El subdominio apunta al mismo proyecto que www, así que
 * blackfriday.holandesnawar.com/ enseñaría la home y no la página de Black
 * Friday, que vive en /black-friday.
 *
 * Lo normal sería una regla `rewrites` con `has: host` en vercel.json, pero
 * NO vale aquí: el adaptador de Vercel de Astro (8.x) escribe él mismo
 * `.vercel/output/config.json` (la "Build Output API") y Vercel usa ese
 * archivo tal cual, sin mirar las reglas de vercel.json. Por eso esta
 * integración retoca config.json DESPUÉS de que lo escriba el adaptador:
 * Astro pone el adaptador el primero de la lista (`integrations.unshift`), así
 * que nuestro `astro:build:done` corre detrás del suyo.
 *
 * Mete al principio de las rutas, antes de mirar los archivos, unas reglas
 * que solo valen con ese dominio (`has: host`):
 *   /          → /black-friday
 *   /ebook     → /black-friday/ebook          (y /oferta, /ebook-ads, /admision)
 * Lo demás (/_astro, /api, /politica-de-privacidad…) sigue su camino normal:
 * en el subdominio se sirve lo mismo que en www.
 *
 * Para añadir otra página al subdominio: su nombre en PAGINAS. Comprobar con
 * `npx astro build` que salen las reglas al principio de
 * .vercel/output/config.json.
 */
import type { AstroIntegration } from 'astro'
import { readFile, writeFile } from 'node:fs/promises'
import { fileURLToPath } from 'node:url'

const HOST = 'blackfriday.holandesnawar.com'
const CARPETA = '/black-friday'
const PAGINAS = ['oferta', 'ebook', 'ebook-ads', 'admision']

export function rutasDelSubdominio() {
  const has = [{ type: 'host', value: HOST }]
  return [
    { src: '^/$', has, dest: CARPETA, check: true },
    { src: `^/(${PAGINAS.join('|')})/?$`, has, dest: `${CARPETA}/$1`, check: true },
  ]
}

export default function subdominios(): AstroIntegration {
  let raiz: URL
  return {
    name: 'nawar-subdominios',
    hooks: {
      'astro:config:done': ({ config }) => {
        raiz = config.root
      },
      'astro:build:done': async ({ logger }) => {
        const ruta = fileURLToPath(new URL('./.vercel/output/config.json', raiz))
        let config: { routes?: unknown[] }
        try {
          config = JSON.parse(await readFile(ruta, 'utf-8'))
        } catch {
          // Sin config.json (otro adaptador, build en local sin Vercel): nada que hacer.
          logger.warn('No hay .vercel/output/config.json: el subdominio de Black Friday no se ha configurado.')
          return
        }
        const nuevas = rutasDelSubdominio()
        const resto = (config.routes || []).filter(
          (r) => !(r && typeof r === 'object' && JSON.stringify((r as { has?: unknown }).has || null).includes(HOST))
        )
        config.routes = [...nuevas, ...resto]
        await writeFile(ruta, JSON.stringify(config, null, 2))
        logger.info(`Subdominio ${HOST}: ${nuevas.length} reglas al principio de config.json.`)
      },
    },
  }
}
