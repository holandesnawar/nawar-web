import { defineField, defineType } from 'sanity'
import { UsersIcon } from '@sanity/icons'

export const waitlistPage = defineType({
  name: 'waitlistPage',
  title: 'Lista de espera',
  type: 'document',
  icon: UsersIcon,
  __experimental_actions: ['update', 'publish'],
  fields: [
    defineField({
      name: 'title',
      title: 'Título de la página',
      type: 'string',
      validation: (r) => r.required(),
    }),
    defineField({
      name: 'headline',
      title: 'Titular principal',
      type: 'string',
    }),
    defineField({
      name: 'body',
      title: 'Descripción',
      type: 'array',
      of: [{ type: 'block' }],
    }),
    defineField({
      name: 'formTitle',
      title: 'Título del formulario',
      type: 'string',
      initialValue: 'Apúntate a la lista de espera',
    }),
    defineField({
      name: 'formButtonText',
      title: 'Texto del botón',
      type: 'string',
      initialValue: 'Quiero apuntarme',
    }),
    defineField({
      name: 'successMessage',
      title: 'Mensaje de confirmación',
      type: 'string',
      initialValue: '¡Genial! Te avisamos en cuanto abramos plazas.',
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
