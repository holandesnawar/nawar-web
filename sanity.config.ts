import { defineConfig } from 'sanity'
import { structureTool } from 'sanity/structure'
import { visionTool } from '@sanity/vision'
import { presentationTool } from 'sanity/presentation'
import { schema } from './src/sanity/schemas'
import { resolve } from './src/sanity/presentation/resolve'

const projectId = 't0qvkil8'
const dataset = 'production'

export default defineConfig({
  projectId,
  dataset,
  title: 'Nawar Web',
  schema,
  plugins: [
    structureTool(),
    visionTool({ defaultApiVersion: '2026-04-08' }),
    presentationTool({
      resolve,
      previewUrl: {
        // Cambia esto a tu URL de Vercel en producción
        origin: process.env.NODE_ENV === 'development'
          ? 'http://localhost:4321'
          : 'https://nawar-web.vercel.app',
        previewMode: {
          enable: '/api/preview',
        },
      },
    }),
  ],
})
