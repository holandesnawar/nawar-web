import { defineConfig } from 'astro/config'
import sanity from '@sanity/astro'
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
    optimizeDeps: {
      exclude: ['@sanity/astro'],
    },
    ssr: {
      noExternal: ['sanity', '@sanity/ui', '@sanity/icons'],
    },
  },
  integrations: [
    react(),
    sitemap({
      filter: (page) =>
        !page.includes('/studio/') && !page.includes('/api/'),
    }),
    sanity({
      projectId: 't0qvkil8',
      dataset: 'production',
      apiVersion: '2026-04-08',
      useCdn: false, // false para builds estáticos, siempre datos frescos
      studioBasePath: '/studio',
      stega: {
        enabled: true,
        studioUrl: '/studio',
      },
    }),
  ],
})
