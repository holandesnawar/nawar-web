import { defineConfig } from 'astro/config'
import react from '@astrojs/react'
import vercel from '@astrojs/vercel'
import tailwindcss from '@tailwindcss/vite'
import sitemap from '@astrojs/sitemap'

export default defineConfig({
  site: 'https://www.holandesnawar.com',
  output: 'server',
  adapter: vercel(),

  /* La landing de la formación pasó de /formacion-a0-a1-sept a
     /formacion-a0-a1: la convocatoria de septiembre se acabó y el
     nombre de un mes en la URL la deja vieja cada temporada.
     La vieja circula por correos ya enviados y por WhatsApp, así que
     no puede quedarse en un 404: manda a la lista de espera, que es
     donde tiene sentido acabar si venías buscando aquella
     convocatoria.

     302 y no 301 a propósito: el 301 se queda cacheado en el
     navegador de quien lo visite una vez, y si algún día hay que
     reactivar esa URL esa gente seguiría cayendo en la lista de
     espera sin remedio. Cuando esto se dé por definitivo, subirlo a
     301.

     Ojo: sólo cambia la landing normal. /formacion-a0-a1-sept-ads se
     queda con su nombre —tiene anuncios apuntando ahí— y no le afecta
     esta regla, que casa la ruta exacta y no por prefijo.

     La matrícula sigue la misma lógica: era
     /matricula-formacion-nawar-a0-a1 y ahora es
     /matricula-formacion-nawar. El nivel en la URL la dejaba vieja en
     cuanto se abra el A1 → A2, y ese enlace está pegado en correos ya
     enviados y reenviado por WhatsApp, así que la ruta vieja tampoco
     puede quedarse en un 404.

     No hace falta duplicar ninguna página: renombrar el archivo cambia
     la URL, y la regla de aquí abajo se encarga de la vieja. Lo que sí
     hubo que tocar son los siete sitios que enlazaban a la ruta
     antigua, o los botones de la landing habrían acabado en la lista
     de espera sin decirlo.

     Ojo con las dos rutas de anuncios: la regla casa la ruta EXACTA,
     así que ni /formacion-a0-a1-sept-ads ni
     /matricula-formacion-nawar-a0-a1-ads se ven afectadas. */
  redirects: {
    '/formacion-a0-a1-sept': { status: 302, destination: '/lista-de-espera' },
    '/matricula-formacion-nawar-a0-a1': { status: 302, destination: '/lista-de-espera' },
  },
  vite: {
    plugins: [tailwindcss()],
  },
  integrations: [
    react(),
    sitemap({
      // Sólo indexamos home, /nuestra-vision, /blog, /blog/*, /guia/*
      // El resto (contacto, acceso, lista-de-espera, legales, admin, api,
      // landings de venta) NO se incluye
      filter: (page) =>
        !page.includes('/api/') &&
        // Sin el "-sept": la landing se renombró y con el nombre viejo
        // este filtro ya no la cazaba, así que se habría colado en el
        // sitemap. Así, por subcadena, cubre las dos: /formacion-a0-a1
        // y /formacion-a0-a1-sept-ads.
        !page.includes('/formacion-a0-a1') &&
        !page.includes('/admin/') &&
        !page.includes('/acceso') &&
        !page.includes('/contacto') &&
        !page.includes('/lista-de-espera') &&
        // Las matrículas y sus páginas de gracias son embudo, no
        // captación. La de siempre no llegaba aquí porque se renderiza
        // en servidor, pero la de anuncios sí es estática y entraría.
        !page.includes('/matricula') &&
        !page.includes('/cookies') &&
        !page.includes('/politica-de-privacidad') &&
        !page.includes('/terminos-y-condiciones') &&
        !page.includes('/condiciones-de-contratacion'),
    }),
  ],
})
