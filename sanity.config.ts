import { defineConfig } from 'sanity'
import { structureTool } from 'sanity/structure'
import { visionTool } from '@sanity/vision'
import { presentationTool } from 'sanity/presentation'
import { schema } from './src/sanity/schemas'
import { resolve } from './src/sanity/presentation/resolve'

const projectId = 't0qvkil8'
const dataset = 'production'

const SINGLETONS = [
  { id: 'landingPage', title: '🏠 Página de inicio' },
]

export default defineConfig({
  projectId,
  dataset,
  title: 'Nawar Web',
  schema,
  plugins: [
    structureTool({
      structure: (S) =>
        S.list()
          .title('Contenido')
          .items([
            // Singletons — abren directamente el documento
            ...SINGLETONS.map(({ id, title }) =>
              S.listItem()
                .title(title)
                .id(id)
                .child(S.document().schemaType(id).documentId(id))
            ),
            S.divider(),
            // Resto de tipos normales (posts, contacto, lista de espera…)
            ...S.documentTypeListItems().filter(
              (item) => !SINGLETONS.find((s) => s.id === item.getId())
            ),
          ]),
    }),
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
