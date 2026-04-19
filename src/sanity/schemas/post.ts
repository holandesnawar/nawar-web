import { defineField, defineType } from 'sanity'
import { DocumentTextIcon } from '@sanity/icons'

export const post = defineType({
  name: 'post',
  title: 'Post de blog',
  type: 'document',
  icon: DocumentTextIcon,
  fields: [
    defineField({
      name: 'title',
      title: 'Título',
      type: 'string',
      validation: (rule) => rule.required(),
    }),
    defineField({
      name: 'slug',
      title: 'Slug (URL)',
      type: 'slug',
      options: { source: 'title', maxLength: 96 },
      validation: (rule) => rule.required(),
    }),
    defineField({
      name: 'publishedAt',
      title: 'Fecha de publicación',
      type: 'datetime',
      initialValue: () => new Date().toISOString(),
    }),
    defineField({
      name: 'excerpt',
      title: 'Extracto',
      type: 'text',
      rows: 3,
      validation: (rule) => rule.max(200).warning('Máximo 200 caracteres para SEO'),
    }),
    defineField({
      name: 'category',
      title: 'Categoría',
      type: 'string',
      options: {
        list: [
          { title: 'Inburgering', value: 'inburgering' },
          { title: 'Cultura', value: 'cultura' },
          { title: 'Vocabulario', value: 'vocabulario' },
          { title: 'Pronunciación', value: 'pronunciacion' },
        ],
        layout: 'radio',
      },
    }),
    defineField({
      name: 'mainImage',
      title: 'Imagen principal',
      type: 'image',
      options: { hotspot: true },
      fields: [
        defineField({ name: 'alt', title: 'Texto alternativo', type: 'string' }),
      ],
    }),
    defineField({
      name: 'body',
      title: 'Contenido',
      type: 'array',
      of: [
        { type: 'block' },
        {
          type: 'image',
          options: { hotspot: true },
          fields: [
            defineField({ name: 'alt', title: 'Texto alternativo', type: 'string' }),
          ],
        },
      ],
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
  preview: {
    select: { title: 'title', media: 'mainImage', date: 'publishedAt' },
    prepare({ title, media, date }) {
      return {
        title,
        media,
        subtitle: date ? new Date(date).toLocaleDateString('es-ES') : 'Sin fecha',
      }
    },
  },
  orderings: [{ title: 'Más recientes', name: 'publishedAtDesc', by: [{ field: 'publishedAt', direction: 'desc' }] }],
})
