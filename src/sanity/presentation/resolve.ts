import { defineLocations, type PresentationPluginOptions } from 'sanity/presentation'

export const resolve: PresentationPluginOptions['resolve'] = {
  locations: {
    post: defineLocations({
      select: { title: 'title', slug: 'slug.current' },
      resolve: (doc) => ({
        locations: [
          {
            title: doc?.title || 'Sin título',
            href: `/blog/${doc?.slug}`,
          },
          { title: 'Blog (lista)', href: '/blog' },
        ],
      }),
    }),
    homePage: defineLocations({
      resolve: () => ({ locations: [{ title: 'Inicio', href: '/' }] }),
    }),
    landingPage: defineLocations({
      resolve: () => ({ locations: [{ title: 'Inicio', href: '/' }] }),
    }),
    contactPage: defineLocations({
      resolve: () => ({ locations: [{ title: 'Contacto', href: '/contacto' }] }),
    }),
    waitlistPage: defineLocations({
      resolve: () => ({ locations: [{ title: 'Lista de espera', href: '/lista-de-espera' }] }),
    }),
  },
}
