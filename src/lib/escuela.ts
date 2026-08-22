/**
 * Dónde vive la escuela.
 *
 * La academia se mudó de academia.holandesnawar.nl a app.holandesnawar.com.
 * El dominio estaba escrito a mano en cinco sitios, así que se sale por aquí:
 * el día que vuelva a cambiar se toca un valor y no cinco archivos.
 *
 * PUBLIC_ESCUELA_URL es la escotilla: no hace falta definirla en Vercel,
 * porque el valor por defecto ya es el bueno. Está para poder apuntar a otro
 * host —una rama de pruebas de la academia, por ejemplo— sin recompilar la
 * idea de la web.
 *
 * El .replace quita las barras finales: si alguien pone la variable con barra
 * al final, `${ESCUELA_URL}/api/...` acabaría con doble barra y algunos
 * servidores contestan un 404 por eso.
 */
export const ESCUELA_URL = (
  import.meta.env.PUBLIC_ESCUELA_URL || 'https://app.holandesnawar.com'
).replace(/\/+$/, '')

/** Sin protocolo, para cuando hay que enseñarlo escrito y no enlazarlo. */
export const ESCUELA_HOST = ESCUELA_URL.replace(/^https?:\/\//, '')
