import type { APIRoute } from 'astro'
import { ESCUELA_URL } from '../../lib/escuela'
import { META_EBOOK } from '../../lib/blackFriday'
import { enviarEventoServidor, ipDe, urlDelEvento } from '../../lib/metaCapi'
import { hashUsuario } from '../../lib/metaUsuario'

export const prerender = false

/**
 * ¿Está pagado el ebook? La página de Black Friday lo pregunta al volver de
 * Stripe (?compra=cs_…) para enseñar "tu ebook va de camino" con su nombre.
 * Lo contesta la escuela, que lo comprueba con Stripe.
 *
 * Si está pagado, manda además el «Purchase» a Meta desde el servidor (API de
 * conversiones) con el id de la sesión de pago como `event_id`: el píxel de la
 * página manda el mismo, así que Meta lo cuenta una vez aunque recargue. Sin
 * token de Meta, no manda nada.
 */
export const GET: APIRoute = async (ctx) => {
  const { request, cookies, url } = ctx
  const cs = (url.searchParams.get('cs') || '').trim()
  if (!/^cs_(test|live)_[A-Za-z0-9]{10,240}$/.test(cs)) return json({ pagado: false }, 400)

  let datos: { pagado?: boolean; nombre?: string; email?: string; importe_cents?: number; moneda?: string } | null = null
  try {
    const r = await fetch(`${ESCUELA_URL}/api/v1/ebook/compra/${encodeURIComponent(cs)}`, { signal: AbortSignal.timeout(8000) })
    if (r.status === 404) return json({ pagado: false }, 404)
    datos = await r.json().catch(() => null)
    if (!r.ok || !datos) return json({ pagado: false }, 502)
  } catch (e) {
    console.error('[ebook-compra] escuela:', (e as Error).message)
    return json({ pagado: false }, 502)
  }

  const pagado = datos.pagado === true
  const nombre = (datos.nombre || '').toString().slice(0, 120)
  const email = (datos.email || '').toString().slice(0, 200)
  const importe = Number.isFinite(Number(datos.importe_cents)) ? Number(datos.importe_cents) : 0

  if (pagado) {
    const pagina = urlDelEvento((url.searchParams.get('pagina') || '').toString(), request)
    await hashUsuario(email, '', nombre).then((usuario) =>
      enviarEventoServidor({
        nombre: 'Purchase',
        eventId: cs,
        url: pagina,
        usuario,
        ip: ipDe(ctx),
        agente: request.headers.get('user-agent') || '',
        fbc: cookies.get('_fbc')?.value,
        fbp: cookies.get('_fbp')?.value,
        contenido: META_EBOOK,
        valor: importe / 100,
        moneda: (datos?.moneda || 'EUR').toString(),
      })
    )
  }

  return json({ pagado, nombre, email, importe_cents: importe })
}

function json(data: object, status = 200) {
  return new Response(JSON.stringify(data), { status, headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' } })
}
