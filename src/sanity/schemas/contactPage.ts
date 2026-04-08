import { defineField, defineType } from 'sanity'
import { EnvelopeIcon } from '@sanity/icons'

export const contactPage = defineType({
  name: 'contactPage',
  title: 'Página de contacto',
  type: 'document',
  icon: EnvelopeIcon,
  __experimental_actions: ['update', 'publish'],
  fields: [
    defineField({
      name: 'title',
      title: 'Título de la página',
      type: 'string',
      validation: (r) => r.required(),
    }),
    defineField({
      name: 'intro',
      title: 'Texto introductorio',
      type: 'array',
      of: [{ type: 'block' }],
    }),
    defineField({
      name: 'email',
      title: 'Email de contacto',
      type: 'string',
    }),
    defineField({
      name: 'formTitle',
      title: 'Título del formulario',
      type: 'string',
    }),
    defineField({
      name: 'seo',
      title: 'SEO',
      type: 'object',
      fields: [
        defineField({ name: 'title', title: 'Meta título', type: 'string' }),
        defineField({ name: 'description', title: 'Meta descripción', type: 'text', rows: 2 }),
      ],
    }),
  ],
})
