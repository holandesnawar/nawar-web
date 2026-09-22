/**
 * Las redirecciones fijas de la web: rutas viejas que no pueden quedarse en
 * un 404 porque circulan en correos ya enviados y por WhatsApp.
 *
 * Viven aquí, en un solo sitio, por dos motivos: las lee `astro.config.mjs`
 * (que es quien las aplica) y las enseña `/api/paginas` (para que el panel de
 * la escuela sepa que existen). Antes estaban solo en la configuración y el
 * panel no podía verlas.
 *
 * 302 y no 301 a propósito: el 301 se queda cacheado en el navegador de quien
 * lo visite una vez, y si algún día hay que reactivar una URL esa gente
 * seguiría cayendo en el destino viejo sin remedio.
 *
 * Para redirecciones NUEVAS ya no hace falta tocar esto: se crean desde
 * Panel → Webs → Enlaces (tipo "redirección") y funcionan al momento, sin
 * despliegue. Esto se queda para las dos que ya existían.
 */
export const REDIRECCIONES: Record<string, { status: 302; destination: string }> = {
  '/formacion-a0-a1-sept': { status: 302, destination: '/lista-de-espera' },
  '/matricula-formacion-nawar-a0-a1': { status: 302, destination: '/lista-de-espera' },
}
