import type { APIRoute } from 'astro'
import { normalizarTelefono } from '../../lib/telefono'
import { ESCUELA_URL } from '../../lib/escuela'

export const prerender = false

/**
 * Manda una solicitud de plaza a la escuela, para que salga en
 * Panel → Estadísticas → "Matrículas nuevas" y el equipo pueda llamar.
 *
 * Esto NO sustituye a /api/waitlist: el alta en systeme.io la sigue haciendo
 * aquel, que es donde vive la clave del CRM y de donde cuelga la secuencia de
 * seguimiento. Son dos destinos con dos trabajos distintos y el formulario los
 * llama a los dos.
 *
 * Nunca devuelve error al navegador aunque la escuela falle. El lead ya está
 * en el CRM para entonces: enseñar "no se pudo enviar" haría que la persona lo
 * mandara otra vez o se fuera, cuando en realidad lo hemos recibido. El fallo
 * va al log, no a la cara del visitante. Mismo criterio que el webhook de Inrō.
 *
 * A mano y no desde el navegador porque así el visitante no necesita hablar
 * con un segundo dominio: menos CORS, menos bloqueadores y la petición sale
 * aunque él cierre la pestaña un segundo después.
 */
const ESCUELA_SOLICITUD_URL = `${ESCUELA_URL}/api/v1/payments/solicitudes`

// Por debajo del maxDuration de Vercel (10 s por defecto): si la escuela está
// reiniciando, preferimos contestar que sí y perder el registro del panel a
// dejar el formulario colgado.
const TIMEOUT_MS = 6000

export const POST: APIRoute = async ({ request }) => {
  const body = await request.json().catch(() => null)

  // Honeypot: si el campo trampa viene relleno es un bot. Se contesta que sí
  // para no enseñarle que le hemos calado.
  const honeypot = (body?.website ?? '').toString().trim()
  if (honeypot) return json({ success: true })

  const email = (body?.email ?? '').toString().trim().toLowerCase()
  if (!email || !email.includes('@')) {
    return json({ error: 'Email inválido' }, 400)
  }

  const payload = {
    email,
    first_name: (body?.firstName ?? body?.first_name ?? '').toString().trim(),
    last_name: (body?.lastName ?? body?.last_name ?? '').toString().trim(),
    phone: normalizarTelefono((body?.phone ?? '').toString()),
    source: body?.source === 'ads' ? 'ads' : body?.source === 'llamada' ? 'llamada' : 'web',
    // Por dónde pasó antes de rellenar. Lo manda el navegador, así que se
    // recorta y se filtra: nada de guardar una cadena larga que venga de
    // fuera. Las marcas son de un juego cerrado (lib/recorrido.ts) y lo que
    // no encaje se tira.
    recorrido: Array.isArray(body?.recorrido)
      ? body.recorrido
          .filter((x: unknown) => typeof x === 'string' && /^[a-z-]{1,24}$/.test(x))
          .slice(-12)
      : [],
    referrer: (body?.referrer ?? '').toString().trim().slice(0, 120),
    utm_source: (body?.utmSource ?? '').toString().trim().slice(0, 120),
    utm_medium: (body?.utmMedium ?? '').toString().trim().slice(0, 120),
    utm_campaign: (body?.utmCampaign ?? '').toString().trim().slice(0, 120),
  }

  try {
    const control = new AbortController()
    const reloj = setTimeout(() => control.abort(), TIMEOUT_MS)
    // Con la clave de la web (SCHOOL_WEB_TOKEN en Vercel) la escuela no le
    // aplica el tope de 5/hora/IP: todas estas peticiones salen de Vercel.
    const tokenWeb =
      (import.meta.env.SCHOOL_WEB_TOKEN as string | undefined) ||
      (typeof process !== 'undefined' ? process.env.SCHOOL_WEB_TOKEN : undefined)
    const res = await fetch(ESCUELA_SOLICITUD_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', ...(tokenWeb ? { 'X-Web-Token': tokenWeb } : {}) },
      body: JSON.stringify(payload),
      signal: control.signal,
    })
    clearTimeout(reloj)
    if (!res.ok) {
      console.error('[solicitud] la escuela contestó', res.status)
    }
  } catch (e) {
    console.error('[solicitud] no se pudo avisar a la escuela:', e)
  }

  return json({ success: true })
}

function json(data: object, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json' },
  })
}
