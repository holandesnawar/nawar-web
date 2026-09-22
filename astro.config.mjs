import { defineConfig } from 'astro/config'
import react from '@astrojs/react'
import vercel from '@astrojs/vercel'
import tailwindcss from '@tailwindcss/vite'
import sitemap from '@astrojs/sitemap'
import { REDIRECCIONES } from './src/lib/redirecciones.ts'

export default defineConfig({
  site: 'https://www.holandesnawar.com',
  output: 'server',
  adapter: vercel(),

  // Las redirecciones fijas viven en src/lib/redirecciones.ts, que también
  // las enseña /api/paginas al panel de la escuela. Las nuevas se crean desde
  // el panel y no pasan por aquí (ver src/pages/[...slug].astro).
  redirects: REDIRECCIONES,
  vite: {
    plugins: [tailwindcss()],
  },
  integrations: [
    react(),
    sitemap({
      // Sólo indexamos home, /nuestra-vision, /blog, /blog/*, /guia/*
      // El resto (contacto, acceso, lista-de-espera, legales, admin, api,
      // landings de venta) NO se incluye
      filter: (page) =>
        !page.includes('/api/') &&
        // Todas las landings de venta de un tirón, con el guion incluido
        // para no cazar nada más. Antes ponía "/formacion-a0-a1" y se
        // quedaba corto dos veces: al renombrar la landing y al aparecer
        // /formacion-nawar-a0-a1, que lleva "nawar" en medio y no
        // contiene esa cadena. Cubre las tres que hay y las que vengan:
        //   /formacion-a0-a1  ·  /formacion-a0-a1-sept-ads
        //   /formacion-nawar-a0-a1
        // (gracias-pre-formacion no empieza por "/formacion-", así que
        //  no le afecta.)
        !page.includes('/formacion-') &&
        // Las guías SÍ se indexan, pero su variante de anuncios no: lleva
        // noindex y la canónica apuntando a la original. Estando además en
        // el sitemap le decíamos a Google dos cosas contrarias —"indexa
        // esto" y "no indexes esto"—, y la que gana no la elegimos
        // nosotros. Casa /guia/<lo-que-sea>-a y todo lo que cuelgue de
        // ella (su página de gracias), sin tocar la original, que no
        // termina en "-a".
        !/\/guia\/[a-z0-9-]+-a(\/|$)/.test(page) &&
        // Y las páginas de gracias, que también van con noindex. Se casa el
        // segmento entero ("…/gracias/" o "…/gracias") y no la palabra
        // suelta, para no llevarse por delante /gracias-pre-formacion.
        !/\/gracias\/?$/.test(page) &&
        !page.includes('/admin/') &&
        !page.includes('/acceso') &&
        !page.includes('/contacto') &&
        !page.includes('/lista-de-espera') &&
        // Las matrículas y sus páginas de gracias son embudo, no
        // captación. La de siempre no llegaba aquí porque se renderiza
        // en servidor, pero la de anuncios sí es estática y entraría.
        !page.includes('/matricula') &&
        !page.includes('/cookies') &&
        !page.includes('/politica-de-privacidad') &&
        !page.includes('/terminos-y-condiciones') &&
        !page.includes('/condiciones-de-contratacion'),
    }),
  ],
})
