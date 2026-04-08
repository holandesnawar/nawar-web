import { defineArrayMember, defineField, defineType } from 'sanity'

export const landingPage = defineType({
  name: 'landingPage',
  title: 'Página de inicio',
  type: 'document',
  fields: [
    // ── Hero ──────────────────────────────────────────────────────────────────
    defineField({
      name: 'hero',
      title: 'Hero',
      type: 'object',
      fields: [
        defineField({ name: 'badge',            type: 'string', title: 'Badge (eyebrow)' }),
        defineField({ name: 'headlineMain',     type: 'string', title: 'Titular — palabra principal' }),
        defineField({ name: 'headlineAccent',   type: 'string', title: 'Titular — palabra en azul' }),
        defineField({ name: 'headlineSuffix',   type: 'string', title: 'Titular — resto' }),
        defineField({ name: 'subtitleDesktop',  type: 'text',   title: 'Subtítulo (escritorio)' }),
        defineField({ name: 'subtitleMobile',   type: 'text',   title: 'Subtítulo (móvil)' }),
        defineField({ name: 'ctaPrimary',       type: 'string', title: 'CTA principal' }),
        defineField({ name: 'ctaSecondary',     type: 'string', title: 'CTA secundario' }),
        defineField({ name: 'socialProofLabel', type: 'string', title: 'Social proof (ej: +600 estudiantes · 4.9 / 5)' }),
      ],
    }),

    // ── Stats ─────────────────────────────────────────────────────────────────
    defineField({
      name: 'stats',
      title: 'Estadísticas',
      type: 'array',
      of: [
        defineArrayMember({
          type: 'object',
          fields: [
            defineField({ name: 'value', type: 'string', title: 'Valor (ej: 600+)' }),
            defineField({ name: 'label', type: 'string', title: 'Etiqueta' }),
          ],
        }),
      ],
    }),

    // ── Marquee ───────────────────────────────────────────────────────────────
    defineField({
      name: 'marqueeItems',
      title: 'Marquee — países',
      type: 'array',
      of: [defineArrayMember({ type: 'string' })],
    }),

    // ── Pain points ───────────────────────────────────────────────────────────
    defineField({
      name: 'painPoints',
      title: 'Pain points',
      type: 'array',
      of: [
        defineArrayMember({
          type: 'object',
          fields: [
            defineField({ name: 'icon',        type: 'string', title: 'Emoji / icono' }),
            defineField({ name: 'title',       type: 'string', title: 'Título' }),
            defineField({ name: 'description', type: 'text',   title: 'Descripción' }),
          ],
        }),
      ],
    }),

    // ── Features ──────────────────────────────────────────────────────────────
    defineField({
      name: 'features',
      title: 'Características (método)',
      type: 'array',
      of: [
        defineArrayMember({
          type: 'object',
          fields: [
            defineField({ name: 'icon',        type: 'string', title: 'Emoji / icono' }),
            defineField({ name: 'title',       type: 'string', title: 'Título' }),
            defineField({ name: 'description', type: 'text',   title: 'Descripción' }),
          ],
        }),
      ],
    }),

    // ── Steps ─────────────────────────────────────────────────────────────────
    defineField({
      name: 'steps',
      title: 'Pasos del proceso',
      type: 'array',
      of: [
        defineArrayMember({
          type: 'object',
          fields: [
            defineField({ name: 'number',      type: 'string', title: 'Número (01, 02…)' }),
            defineField({ name: 'title',       type: 'string', title: 'Título' }),
            defineField({ name: 'description', type: 'text',   title: 'Descripción' }),
          ],
        }),
      ],
    }),

    // ── Comparison ────────────────────────────────────────────────────────────
    defineField({
      name: 'comparison',
      title: 'Comparativa (Nawar vs clásico)',
      type: 'array',
      of: [
        defineArrayMember({
          type: 'object',
          fields: [
            defineField({ name: 'icon',        type: 'string', title: 'Emoji / icono' }),
            defineField({ name: 'title',       type: 'string', title: 'Título del punto' }),
            defineField({ name: 'nawarText',   type: 'text',   title: 'Texto columna Nawar' }),
            defineField({ name: 'classicText', type: 'text',   title: 'Texto columna clásico' }),
          ],
        }),
      ],
    }),

    // ── Testimonials ──────────────────────────────────────────────────────────
    defineField({
      name: 'testimonials',
      title: 'Testimonios',
      type: 'array',
      of: [
        defineArrayMember({
          type: 'object',
          fields: [
            defineField({ name: 'name',   type: 'string', title: 'Nombre' }),
            defineField({ name: 'origin', type: 'string', title: 'Origen (ej: Madrid · trabaja en Ámsterdam)' }),
            defineField({ name: 'text',   type: 'text',   title: 'Testimonio' }),
            defineField({ name: 'stars',  type: 'number', title: 'Estrellas (1-5)' }),
            defineField({ name: 'avatar', type: 'string', title: 'Iniciales del avatar' }),
          ],
        }),
      ],
    }),

    // ── Doubts ────────────────────────────────────────────────────────────────
    defineField({
      name: 'doubts',
      title: '¿Te suena esto? (dudas)',
      type: 'array',
      of: [
        defineArrayMember({
          type: 'object',
          fields: [
            defineField({ name: 'icon', type: 'string', title: 'Emoji' }),
            defineField({ name: 'text', type: 'text',   title: 'Texto' }),
          ],
        }),
      ],
    }),

    // ── About ─────────────────────────────────────────────────────────────────
    defineField({
      name: 'about',
      title: 'Sobre la academia',
      type: 'object',
      fields: [
        defineField({ name: 'paragraph1', type: 'text', title: 'Párrafo 1' }),
        defineField({ name: 'paragraph2', type: 'text', title: 'Párrafo 2' }),
        defineField({ name: 'paragraph3', type: 'text', title: 'Párrafo 3' }),
      ],
    }),
  ],
})
