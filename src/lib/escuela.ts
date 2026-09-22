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


/**
 * Avisa a la escuela de algo que hizo una persona (descargó una guía,
 * escribió por Instagram…), para que salga en Panel → Estadísticas →
 * Contactos con lo que se sabía en ese momento.
 *
 * Existe porque durante meses las altas de las guías iban SOLO a
 * systeme.io, y cuando systeme.io tiró los nombres no quedó rastro en
 * ningún sitio nuestro. Esto es la copia.
 *
 * Nunca lanza y nunca bloquea: si la escuela está reiniciando, la persona
 * sigue su camino igual y el fallo va al log. Presupuesto corto (4 s) para
 * no comerse el de Vercel.
 *
 * Candado opcional: si en Vercel está SCHOOL_WEB_TOKEN, va en la cabecera
 * X-Web-Token (con guiones: nginx tira las que llevan `_`) y la escuela la
 * exige si tiene LEARNHOUSE_WEB_TOKEN con el mismo valor.
 */
export interface EventoEscuela {
  kind: string
  email: string
  first_name?: string
  last_name?: string
  phone?: string
  source?: string
  tag?: string
  recorrido?: string[]
  referrer?: string
  utm_source?: string
  utm_medium?: string
  utm_campaign?: string
  extra?: Record<string, unknown>
}

export async function avisarEscuela(evento: EventoEscuela): Promise<boolean> {
  const token =
    (import.meta.env.SCHOOL_WEB_TOKEN as string | undefined) ||
    (typeof process !== 'undefined' ? process.env.SCHOOL_WEB_TOKEN : undefined)
  const control = new AbortController()
  const reloj = setTimeout(() => control.abort(), 4000)
  try {
    const res = await fetch(`${ESCUELA_URL}/api/v1/contactos/evento`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { 'X-Web-Token': token } : {}),
      },
      body: JSON.stringify(evento),
      signal: control.signal,
    })
    if (!res.ok) console.error('[escuela] evento rechazado:', evento.kind, res.status)
    return res.ok
  } catch (e) {
    console.error('[escuela] no se pudo avisar del evento', evento.kind, (e as Error).message)
    return false
  } finally {
    clearTimeout(reloj)
  }
}
