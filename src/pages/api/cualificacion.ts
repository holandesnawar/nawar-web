import type { APIRoute } from 'astro'
import { normalizarTelefono } from '../../lib/telefono'
import { MAX_TEXTO, PREGUNTAS, puntuar } from '../../lib/cualificacion'
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

/**
 * Las etiquetas del proceso de admisión en systeme.io (03/10: "¿se añade al
 * CRM con etiqueta de que vio el vídeo?"). Antes, quien dejaba sus datos en
 * el vídeo NO entraba en systeme.io hasta terminar las preguntas, así que no
 * había forma de mandarle un correo si se iba a mitad. Ahora entra en cada
 * hito, con su etiqueta, y las secuencias se pueden colgar de ellas:
 *  - datos: dejó nombre, correo y WhatsApp en la ventanita del vídeo;
 *  - video: vio el vídeo entero (el VSL);
 *  - completada: terminó las preguntas (además de "Llamada", como /agendar).
 * Si la etiqueta no existe, systeme.io la crea al primer uso.
 */
const ETIQUETAS_ADMISION = {
  datos: 'Admisión - datos',
  video: 'Admisión - vio el vídeo',
  completada: 'Admisión - completada',
} as const

/** Alta en systeme.io con sus etiquetas, en blando: si falla, lo dice en el
 *  log y sigue. El lead ya está en la escuela para entonces. */
async function alCRM(
  persona: { email: string; firstName: string; lastName: string; phone: string },
  etiquetas: string[],
  campos: { slug: string; value: string }[] = []
) {
  const apiKey = leerEnv('SYSTEME_API_KEY')
  if (!apiKey) return
  const ctx: Ctx = { apiKey, reloj: relojDe(PRESUPUESTO_MS) }
  try {
    const [contacto, ...tags] = await Promise.all([
      crearOBuscarContacto(persona.email, persona.firstName, persona.lastName, ctx),
      ...etiquetas.map((e) => resolverEtiqueta(e, ctx)),
    ])
    if (contacto.id === null) return
    // Nombre y teléfono por un lado y lo demás por otro: si un slug
    // personalizado fallara, que no se lleve por delante el nombre.
    await escribirCampos(contacto.id, camposDePersona(persona.firstName, persona.lastName, persona.phone), ctx)
    if (campos.length) await escribirCampos(contacto.id, campos, ctx)
    for (const t of tags) if (t.id !== null) await asignarEtiqueta(contacto.id, t.id, ctx)
  } catch (e) {
    console.error('[cualificacion] crm:', (e as Error).message)
  }
}

export const POST: APIRoute = async ({ request }) => {
  const body = await request.json().catch(() => null)
  if ((body?.website ?? '').toString().trim()) return json({ ok: true, apto: false })

  const email = (body?.email ?? '').toString().trim().toLowerCase()
  const firstName = (body?.first_name ?? '').toString().trim().slice(0, 120)
  const lastName = (body?.last_name ?? '').toString().trim().slice(0, 120)
  const phone = normalizarTelefono((body?.phone ?? '').toString().slice(0, 40))
  if (!email || !email.includes('@') || !firstName) return json({ error: 'Faltan el nombre o el correo' }, 400)

  const recorridoParcial: string[] = Array.isArray(body?.recorrido)
    ? body.recorrido.filter((x: unknown) => typeof x === 'string' && /^[a-z-]{1,24}$/.test(x)).slice(-12)
    : []

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

  // De qué embudo viene (02/10): /proceso-de-admision manda 'admision' y en
  // qué punto del vídeo va. /agendar no manda nada y todo sigue igual. Va en
  // el `extra` del evento, para que Panel → Llamadas lo distinga.
  const embudo = /^[a-z-]{1,20}$/.test((body?.embudo ?? '').toString()) ? body.embudo.toString() : ''
  const video = ['empezado', 'visto'].includes((body?.video ?? '').toString()) ? body.video.toString() : ''
  const marcaEmbudo: Record<string, string> = embudo ? { embudo, ...(video ? { video } : {}) } : {}

  // Modo parcial: la persona acaba de pasar la pantalla de datos (y luego,
  // otra vez con cada respuesta). Se guarda YA en la escuela como evento "agendar-empezado", para que si cierra la
  // pestaña a mitad no se pierda: sale en Panel → Llamadas como "No
  // terminó". Sin CRM, sin solicitud y sin correo al equipo: eso va al
  // terminar. Solo el evento a propósito: /payments/solicitudes tiene un
  // tope de 5 por hora y por IP, y todas las llamadas de la web salen de
  // las IP de Vercel; gastar dos por persona acercaría el tope.
  if (body?.parcial === true) {
    // Lo que lleve contestado hasta ahora, sin las que faltan: si se va a
    // mitad, el closer puede llamarle sabiendo ya su nivel, para qué lo
    // quiere, etc. La escuela reescribe la misma línea en cada respuesta
    // (una persona = una línea en 24 h), no crea una nueva.
    const hechas = puntuar(respuestas, textos).respuestas.filter((r) => r.respuesta !== 'Sin responder')
    const ultima = PREGUNTAS.find((p) => p.clave === (body?.ultima ?? '').toString())?.etiqueta ?? ''
    // Proceso de admisión (02/10, pedido del usuario): quien rellena la
    // ventanita del vídeo YA es una matrícula, aunque no siga. Se crea su
    // solicitud con de dónde viene (recorrido, web de origen y campaña) y,
    // si sigue, la misma solicitud se va completando: la escuela reaprovecha
    // la fila del mismo correo en 24 h, así que al terminar las preguntas no
    // sale otra. Solo con `matricula: true` (la ventanita), no con cada
    // respuesta, para no gastar el tope de la escuela.
    if (body?.matricula === true) {
      const tokenWeb = leerEnv('SCHOOL_WEB_TOKEN')
      await fetch(`${ESCUELA_URL}/api/v1/payments/solicitudes`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', ...(tokenWeb ? { 'X-Web-Token': tokenWeb } : {}) },
        body: JSON.stringify({
          email,
          first_name: firstName,
          last_name: lastName,
          phone,
          source: 'admision',
          recorrido: recorridoParcial,
          referrer: (body?.referrer ?? '').toString().trim().slice(0, 120),
          utm_source: (body?.utmSource ?? '').toString().trim().slice(0, 120),
          utm_medium: (body?.utmMedium ?? '').toString().trim().slice(0, 120),
          utm_campaign: (body?.utmCampaign ?? '').toString().trim().slice(0, 120),
          utm_content: (body?.utmContent ?? '').toString().trim().slice(0, 120),
        }),
        signal: AbortSignal.timeout(6000),
      }).catch((e) => console.error('[cualificacion] matricula:', (e as Error).message))
    }

    // systeme.io, solo en los dos hitos del proceso de admisión (la web los
    // marca con `hito`), no con cada respuesta: así no se gastan llamadas.
    const hito = (body?.hito ?? '').toString()
    // De qué página salió (07/10): /formacion-nawar-fb manda la suya; si no, la
    // de siempre.
    const origen = /^[a-z0-9-]{1,40}$/.test((body?.origen ?? '').toString()) ? body.origen.toString() : 'proceso-de-admision'
    const crmHito =
      embudo === 'admision' && (hito === 'datos' || hito === 'video')
        ? alCRM(
            { email, firstName, lastName, phone },
            [ETIQUETAS_ADMISION[hito]],
            hito === 'datos'
              ? [
                  { slug: 'origen', value: origen },
                  ...(['utm_source', 'utm_medium', 'utm_campaign'] as const)
                    .map((k) => ({ slug: k, value: (body?.[k === 'utm_source' ? 'utmSource' : k === 'utm_medium' ? 'utmMedium' : 'utmCampaign'] ?? '').toString().trim().slice(0, 120) }))
                    .filter((c) => c.value),
                ]
              : []
          )
        : Promise.resolve()

    await avisarEscuela({
      // El proceso de admisión es una MATRÍCULA, no una llamada (02/10,
      // usuario): va con su propio tipo y no sale en Panel → Llamadas hasta
      // que termina las preguntas. En la ficha dice qué vio y dónde se quedó.
      kind: embudo === 'admision' ? 'admision' : 'agendar-empezado',
      email,
      first_name: firstName,
      last_name: lastName,
      phone,
      source: 'llamada',
      recorrido: recorridoParcial,
      referrer: (body?.referrer ?? '').toString().trim().slice(0, 120),
      // La campaña también aquí: si se va a mitad, el "No terminó" dice de
      // qué anuncio venía (desde el 29/09 los anuncios llevan a /agendar).
      utm_source: (body?.utmSource ?? '').toString().trim().slice(0, 120),
      utm_medium: (body?.utmMedium ?? '').toString().trim().slice(0, 120),
      utm_campaign: (body?.utmCampaign ?? '').toString().trim().slice(0, 120),
      utm_content: (body?.utmContent ?? '').toString().trim().slice(0, 120),
      ...(hechas.length || embudo ? { extra: { ...marcaEmbudo, ...(hechas.length ? { respuestas: hechas, ultima } : {}) } } : {}),
    })
    await crmHito
    return json({ ok: true })
  }

  // Modo reserva: Calendly avisó a la página de que ha elegido día y hora.
  // Se apunta como evento "reunion" para que Panel → Llamadas diga "Hora
  // reservada" y no haya que ir a Calendly a comprobarlo. El día exacto lo
  // tiene Calendly (y su correo); aquí solo va el enlace del evento.
  if (body?.reservada === true) {
    const uri = (body?.calendly_evento ?? '').toString().trim()
    await avisarEscuela({
      kind: 'reunion',
      email,
      first_name: firstName,
      last_name: lastName,
      phone,
      source: 'llamada',
      extra: { ...marcaEmbudo, ...(/^https:\/\/api\.calendly\.com\/scheduled_events\/[\w-]{1,80}$/.test(uri) ? { calendly_evento: uri } : {}) },
    })
    return json({ ok: true })
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
    utm_content: (body?.utmContent ?? '').toString().trim().slice(0, 120),
  }

  // 1) La escuela: solicitud (para llamarle) + evento con las respuestas.
  // Con la clave de la web (si está en Vercel) la escuela no le aplica el
  // tope de 5/hora/IP: todas estas peticiones salen de las IP de Vercel.
  const tokenWeb = leerEnv('SCHOOL_WEB_TOKEN')
  const solicitud = fetch(`${ESCUELA_URL}/api/v1/payments/solicitudes`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...(tokenWeb ? { 'X-Web-Token': tokenWeb } : {}) },
    body: JSON.stringify({ email, first_name: firstName, last_name: lastName, phone, source: embudo === 'admision' ? 'admision' : 'llamada', recorrido, referrer, ...utm }),
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
    extra: { ...marcaEmbudo, puntuacion: resultado.puntuacion, apto: resultado.apto, motivo_fuera: resultado.motivo_fuera, respuestas: resultado.respuestas },
  })

  // 2) systeme.io, en blando. Del proceso de admisión, además, su etiqueta.
  const crm = alCRM(
    { email, firstName, lastName, phone },
    embudo === 'admision' ? [ETIQUETA, ETIQUETAS_ADMISION.completada] : [ETIQUETA]
  )

  await Promise.all([solicitud, evento, crm])

  // A dónde agendar: Calendly/Cal.com si está puesto; si no, WhatsApp con el
  // mensaje ya escrito. Así la página funciona desde hoy.
  const agenda = leerEnv('PUBLIC_AGENDA_URL') || 'https://calendly.com/holandesnawar/llamada-de-consultoria'
  const nombre = encodeURIComponent(`${firstName} ${lastName}`.trim())
  const agendaUrl = agenda
    ? `${agenda}${agenda.includes('?') ? '&' : '?'}name=${nombre}&email=${encodeURIComponent(email)}`
    : `https://wa.me/31616084212?text=${encodeURIComponent(`Hola, soy ${firstName}. Quiero agendar la llamada sobre la formación.`)}`

  return json({ ok: true, apto: resultado.apto, puntuacion: resultado.puntuacion, agenda_url: agendaUrl })
}

function json(data: object, status = 200) {
  return new Response(JSON.stringify(data), { status, headers: { 'Content-Type': 'application/json' } })
}
