import { defineConfig } from 'astro/config'
import react from '@astrojs/react'
import vercel from '@astrojs/vercel'
import tailwindcss from '@tailwindcss/vite'
import sitemap from '@astrojs/sitemap'

export default defineConfig({
  site: 'https://www.holandesnawar.com',
  output: 'server',
  adapter: vercel(),
  vite: {
    plugins: [tailwindcss()],
  },
  integrations: [
    react(),
    sitemap({
      // Sólo indexamos home, /nuestra-vision, /blog, /blog/*, /guia/*
      // El resto (contacto, acceso, lista-de-espera, legales, admin, api) NO se incluye
      filter: (page) =>
        !page.includes('/api/') &&
        !page.includes('/admin/') &&
        !page.includes('/acceso') &&
        !page.includes('/contacto') &&
        !page.includes('/lista-de-espera') &&
        !page.includes('/cookies') &&
        !page.includes('/politica-de-privacidad') &&
        !page.includes('/terminos-y-condiciones') &&
        !page.includes('/og-preview'),
    }),
  ],
})
