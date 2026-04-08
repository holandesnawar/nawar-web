import { defineField, defineType } from 'sanity'
import { HomeIcon } from '@sanity/icons'

export const homePage = defineType({
  name: 'homePage',
  title: 'Página de inicio',
  type: 'document',
  icon: HomeIcon,
  // Solo puede existir un documento de este tipo
  __experimental_actions: ['update', 'publish'],
  fields: [
    defineField({
      name: 'hero',
      title: 'Hero',
      type: 'object',
      fields: [
        defineField({ name: 'headline', title: 'Titular principal', type: 'string', validation: (r) => r.required() }),
        defineField({ name: 'subheadline', title: 'Subtítulo', type: 'text', rows: 2 }),
        defineField({ name: 'cta', title: 'Botón CTA', type: 'string' }),
        defineField({ name: 'ctaUrl', title: 'URL del botón', type: 'string' }),
      ],
    }),
    defineField({
      name: 'about',
      title: 'Sección sobre mí',
      type: 'object',
      fields: [
        defineField({ name: 'title', title: 'Título', type: 'string' }),
        defineField({ name: 'body', title: 'Texto', type: 'array', of: [{ type: 'block' }] }),
        defineField({ name: 'image', title: 'Foto', type: 'image', options: { hotspot: true } }),
      ],
    }),
    defineField({
      name: 'featuredPosts',
      title: 'Posts destacados en inicio',
      type: 'array',
      of: [{ type: 'reference', to: [{ type: 'post' }] }],
      validation: (r) => r.max(3),
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
