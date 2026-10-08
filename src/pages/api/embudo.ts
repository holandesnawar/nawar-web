import type { APIRoute } from 'astro'
import { enviarEventoServidor, ipDe, urlDelEvento, type NombreEvento } from '../../lib/metaCapi'

export const prerender = false

/**
 * Los eventos del vídeo del embudo del anuncio (VSLVisto y VSL50), mandados
 * también desde el servidor a Meta (ver src/lib/metaCapi.ts). 08/10.
 *
 * El navegador manda el nombre del evento, el MISMO `event_id` que acaba de
 * dar al píxel (así Meta deduplica) y, si los tiene, el correo, el teléfono y
 * el nombre YA cifrados con SHA-256: esta ruta nunca ve un dato en claro, y
 * lo que no sea una huella se tira antes de mandarlo. Las cookies del píxel
 * (_fbp, _fbc), la IP y el navegador se leen aquí.
 *
 * Lead y Schedule NO entran por aquí: van con /api/cualificacion, que ya
 * recibe los datos de la persona. Solo estos dos nombres, para que nadie
 * pueda usar la ruta para colar otros eventos en el píxel.
 *
 * Se llama /api/embudo (y no "pixel", "track"…) a propósito: los bloqueadores
 * de anuncios cortan esas direcciones, y esto existe justo para llegar cuando
 * el píxel no llega.
 */
const PERMITIDOS = new Set<NombreEvento>(['VSLVisto', 'VSL50'])

export const POST: APIRoute = async (ctx) => {
  const { request, cookies } = ctx
  const body = await request.json().catch(() => null)
  const evento = (body?.evento ?? '').toString() as NombreEvento
  const eventId = (body?.event_id ?? '').toString()
  if (!PERMITIDOS.has(evento) || !/^[a-z0-9-]{6,80}$/.test(eventId)) return new Response(null, { status: 400 })

  const url = urlDelEvento((body?.pagina ?? '').toString(), request)
  if (!url) return new Response(null, { status: 400 })

  const u = (body?.usuario ?? {}) as Record<string, unknown>
  await enviarEventoServidor({
    nombre: evento,
    eventId,
    url,
    usuario: { em: u.em as string, ph: u.ph as string, fn: u.fn as string },
    ip: ipDe(ctx),
    agente: request.headers.get('user-agent') || '',
    fbc: cookies.get('_fbc')?.value,
    fbp: cookies.get('_fbp')?.value,
    contenido: 'Formación Nawar FB',
  })
  return new Response(null, { status: 204 })
}
