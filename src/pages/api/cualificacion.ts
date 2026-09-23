import type { APIRoute } from 'astro'
import { MAX_TEXTO, puntuar } from '../../lib/cualificacion'
import { ESCUELA_URL, avisarEscuela } from '../../lib/escuela'
import {
  asignarEtiqueta,
  camposDePersona,
  crearOBuscarContacto,
  escribirCampos,
  leerEnv,
  relojDe,
  resolverEtiqueta,
  type Ctx,
} from '../../lib/systeme'

export const prerender = false

/**
 * Recibe la cualificación de /agendar, la puntúa AQUÍ (el navegador solo
 * enseña; la nota que cuenta es la del servidor) y reparte:
 *  - a la escuela, como solicitud de plaza (sale en Matrículas nuevas para
 *    que el closer la vea) y como evento "cualificacion" con las respuestas
 *    (sale en la ficha del contacto);
 *  - a systeme.io, con la etiqueta "Llamada" y sus datos por slug.
 * Contesta si es apto y a dónde mandarle a agendar. Nunca 500 por el CRM:
 * el lead ya está en la escuela para entonces.
 */
const ETIQUETA = 'Llamada'
const PRESUPUESTO_MS = 8000

export const POST: APIRoute = async ({ request }) => {
  const body = await request.json().catch(() => null)
  if ((body?.website ?? '').toString().trim()) return json({ ok: true, apto: false })

  const email = (body?.email ?? '').toString().trim().toLowerCase()
  const firstName = (body?.first_name ?? '').toString().trim().slice(0, 120)
  const lastName = (body?.last_name ?? '').toString().trim().slice(0, 120)
  const phone = (body?.phone ?? '').toString().trim().slice(0, 40)
  if (!email || !email.includes('@') || !firstName) return json({ error: 'Faltan el nombre o el correo' }, 400)

  const recorridoParcial: string[] = Array.isArray(body?.recorrido)
    ? body.recorrido.filter((x: unknown) => typeof x === 'string' && /^[a-z-]{1,24}$/.test(x)).slice(-12)
    : []

  // Modo parcial: la persona acaba de pasar la pantalla de datos. Se guarda
  // YA en la escuela como evento "agendar-empezado", para que si cierra la
  // pestaña a mitad no se pierda: sale en Panel → Llamadas como "No
  // terminó". Sin CRM, sin solicitud y sin correo al equipo: eso va al
  // terminar. Solo el evento a propósito: /payments/solicitudes tiene un
  // tope de 5 por hora y por IP, y todas las llamadas de la web salen de
  // las IP de Vercel; gastar dos por persona acercaría el tope.
  if (body?.parcial === true) {
    await avisarEscuela({
      kind: 'agendar-empezado',
      email,
      first_name: firstName,
      last_name: lastName,
      phone,
      source: 'llamada',
      recorrido: recorridoParcial,
    })
    return json({ ok: true })
  }

  const respuestas: Record<string, string> = {}
  for (const [k, v] of Object.entries((body?.respuestas ?? {}) as Record<string, unknown>)) {
    if (typeof v === 'string' && /^[a-z0-9]{1,20}$/.test(v) && /^[a-z]{1,20}$/.test(k)) respuestas[k] = v
  }
  // Las respuestas abiertas: texto libre, acotado. Se guardan tal cual (la
  // escuela y el correo las escapan al pintarlas), sin saltos raros.
  const textos: Record<string, string> = {}
  for (const [k, v] of Object.entries((body?.textos ?? {}) as Record<string, unknown>)) {
    if (typeof v === 'string' && /^[a-z]{1,20}$/.test(k)) textos[k] = v.replace(/[\u0000-\u0008\u000B-\u001F]/g, '').trim().slice(0, MAX_TEXTO)
  }
  const resultado = puntuar(respuestas, textos)

  const recorrido: string[] = Array.isArray(body?.recorrido)
    ? body.recorrido.filter((x: unknown) => typeof x === 'string' && /^[a-z-]{1,24}$/.test(x)).slice(-12)
    : []
  const referrer = (body?.referrer ?? '').toString().trim().slice(0, 120)
  const utm = {
    utm_source: (body?.utmSource ?? '').toString().trim().slice(0, 120),
    utm_medium: (body?.utmMedium ?? '').toString().trim().slice(0, 120),
    utm_campaign: (body?.utmCampaign ?? '').toString().trim().slice(0, 120),
  }

  // 1) La escuela: solicitud (para llamarle) + evento con las respuestas.
  const solicitud = fetch(`${ESCUELA_URL}/api/v1/payments/solicitudes`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, first_name: firstName, last_name: lastName, phone, source: 'llamada', recorrido, referrer, ...utm }),
    signal: AbortSignal.timeout(6000),
  }).catch((e) => console.error('[cualificacion] solicitud:', (e as Error).message))

  const evento = avisarEscuela({
    kind: 'cualificacion',
    email,
    first_name: firstName,
    last_name: lastName,
    phone,
    source: 'llamada',
    tag: ETIQUETA,
    recorrido,
    referrer,
    ...utm,
    extra: { puntuacion: resultado.puntuacion, apto: resultado.apto, respuestas: resultado.respuestas },
  })

  // 2) systeme.io, en blando.
  const crm = (async () => {
    const apiKey = leerEnv('SYSTEME_API_KEY')
    if (!apiKey) return
    const ctx: Ctx = { apiKey, reloj: relojDe(PRESUPUESTO_MS) }
    try {
      const [contacto, tag] = await Promise.all([crearOBuscarContacto(email, firstName, lastName, ctx), resolverEtiqueta(ETIQUETA, ctx)])
      if (contacto.id === null) return
      await escribirCampos(contacto.id, camposDePersona(firstName, lastName, phone), ctx)
      if (tag.id !== null) await asignarEtiqueta(contacto.id, tag.id, ctx)
    } catch (e) {
      console.error('[cualificacion] crm:', (e as Error).message)
    }
  })()

  await Promise.all([solicitud, evento, crm])

  // A dónde agendar: Calendly/Cal.com si está puesto; si no, WhatsApp con el
  // mensaje ya escrito. Así la página funciona desde hoy.
  const agenda = leerEnv('PUBLIC_AGENDA_URL') || ''
  const nombre = encodeURIComponent(`${firstName} ${lastName}`.trim())
  const agendaUrl = agenda
    ? `${agenda}${agenda.includes('?') ? '&' : '?'}name=${nombre}&email=${encodeURIComponent(email)}`
    : `https://wa.me/31616084212?text=${encodeURIComponent(`Hola, soy ${firstName}. Quiero agendar la llamada sobre la formación.`)}`

  return json({ ok: true, apto: resultado.apto, puntuacion: resultado.puntuacion, agenda_url: agendaUrl })
}

function json(data: object, status = 200) {
  return new Response(JSON.stringify(data), { status, headers: { 'Content-Type': 'application/json' } })
}
