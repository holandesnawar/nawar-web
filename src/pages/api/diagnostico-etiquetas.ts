/**
 * Las etiquetas que hay de verdad en systeme.io.
 *
 * Existe porque "la etiqueta no se pone" tiene tres causas que por fuera se ven
 * igual y llevan a arreglos distintos:
 *
 *   1. La etiqueta se llama parecido pero no igual ("Nuevo Bases" contra
 *      "Nuevos Bases"), así que el código creó una SEGUNDA y los contactos
 *      caen en la que nadie mira.
 *   2. La etiqueta existe pero la búsqueda no llegaba a ella (solo se miraban
 *      las dos primeras páginas).
 *   3. La etiqueta está bien y lo que pasa es que nadie llegó nuevo.
 *
 * Adivinar cuál de las tres es sale caro: el lead ya pasó y no vuelve. Con esta
 * lista se ve en diez segundos.
 *
 * Solo lee. No crea, no borra y no toca ningún contacto. Devuelve nombres de
 * etiqueta, nunca correos ni datos de nadie.
 *
 * Se abre con la misma clave que el webhook de Inrō (`NAWAR_WEBHOOK_SECRET`),
 * en la URL para poder mirarlo desde el móvil:
 *   /api/diagnostico-etiquetas?clave=...&buscar=bases     → las etiquetas
 *   /api/diagnostico-etiquetas?clave=...&email=x@y.com    → un contacto y las suyas
 */
import type { APIRoute } from 'astro'
import { createHash, timingSafeEqual } from 'node:crypto'

export const prerender = false

const SYSTEME_BASE = 'https://api.systeme.io/api'

function leerEnv(nombre: string): string {
  return (
    ((import.meta.env as any)[nombre] as string | undefined) ||
    (typeof process !== 'undefined' ? process.env[nombre] : undefined) ||
    ''
  )
}

function mismaClave(a: string, b: string): boolean {
  const ha = createHash('sha256').update(a, 'utf8').digest()
  const hb = createHash('sha256').update(b, 'utf8').digest()
  return timingSafeEqual(ha, hb)
}

/** Mismo criterio que waitlist.ts: sin acentos, sin mayúsculas, guiones = espacios. */
function normalizar(nombre: string): string {
  return (nombre || '')
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '')
    .toLowerCase()
    .replace(/[-_]+/g, ' ')
    .replace(/\s+/g, ' ')
    .trim()
}

function json(data: object, status = 200) {
  return new Response(JSON.stringify(data, null, 2), {
    status,
    headers: { 'Content-Type': 'application/json; charset=utf-8' },
  })
}

export const GET: APIRoute = async ({ url }) => {
  const claveBuena = leerEnv('NAWAR_WEBHOOK_SECRET')
  if (!claveBuena) return json({ error: 'NAWAR_WEBHOOK_SECRET no está puesta' }, 503)

  const claveDada = url.searchParams.get('clave') || ''
  if (!claveDada || !mismaClave(claveDada, claveBuena)) {
    return json({ error: 'No autorizado' }, 401)
  }

  const apiKey = leerEnv('SYSTEME_API_KEY')
  if (!apiKey) return json({ error: 'SYSTEME_API_KEY no está puesta' }, 503)

  const headers = {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
    accept: 'application/json',
  }

  // ── Un contacto concreto: ?email=… ──
  //
  // Es la pregunta que de verdad cierra el caso: "esta persona que se apuntó
  // ayer, ¿está?, ¿y con qué etiquetas?". Si sale con "Guía Bases" y sin la de
  // lead nuevo, es que systeme.io ya la conocía y el código hizo lo correcto;
  // si sale con las dos, funciona; si no sale, el alta no llegó.
  //
  // Va detrás de la clave como todo lo demás: preguntar si un correo está en la
  // lista es precisamente lo que no puede quedar abierto.
  const email = (url.searchParams.get('email') || '').trim()
  if (email) {
    try {
      const res = await fetch(`${SYSTEME_BASE}/contacts?email=${encodeURIComponent(email)}`, { headers })
      if (!res.ok) return json({ error: `systeme.io respondió ${res.status} al buscar el contacto` }, 502)
      const data = await res.json().catch(() => null)
      const items: any[] = data?.items ?? (Array.isArray(data) ? data : [])
      if (!items.length) {
        return json({ email, existe: false, nota: 'systeme.io no tiene ese correo.' })
      }
      const c = items[0]
      const etiquetas = (c?.tags ?? []).map((t: any) => t?.name).filter(Boolean)
      // Los campos tal cual los tiene systeme.io, con su slug: es la manera de
      // ver dónde vive el nombre de verdad (first_name / surname) y si llegó.
      const campos = (c?.fields ?? []).map((f: any) => ({ slug: f?.slug, valor: f?.value ?? null }))
      return json({
        email,
        existe: true,
        id: c?.id ?? null,
        registrado: c?.registeredAt ?? c?.createdAt ?? null,
        etiquetas,
        campos,
        // Por si la API los devolviera como propiedades sueltas (que es como
        // se mandaban antes y no servía): para comparar.
        propiedades_sueltas: { firstName: c?.firstName ?? null, surname: c?.surname ?? null, phone: c?.phone ?? null },
      })
    } catch (e) {
      return json({ error: `No se pudo hablar con systeme.io: ${(e as Error).message}` }, 502)
    }
  }

  const todas: { id: number; nombre: string }[] = []
  let paginas = 0
  try {
    for (let page = 1; page <= 20; page++) {
      const res = await fetch(`${SYSTEME_BASE}/tags?itemsPerPage=100&page=${page}`, { headers })
      if (!res.ok) {
        return json(
          { error: `systeme.io respondió ${res.status} en la página ${page}`, hasta_ahora: todas.length },
          502
        )
      }
      paginas = page
      const data = await res.json().catch(() => null)
      const items: any[] = data?.items ?? []
      for (const t of items) todas.push({ id: t.id, nombre: t.name })
      if (items.length < 100) break
    }
  } catch (e) {
    return json({ error: `No se pudo hablar con systeme.io: ${(e as Error).message}` }, 502)
  }

  // Duplicados "de persona": los que solo se diferencian en acentos, mayúsculas
  // o guiones. Son los que parten una campaña en dos sin avisar.
  const porNombre = new Map<string, { id: number; nombre: string }[]>()
  for (const t of todas) {
    const k = normalizar(t.nombre)
    porNombre.set(k, [...(porNombre.get(k) ?? []), t])
  }
  const duplicadas = [...porNombre.entries()]
    .filter(([, v]) => v.length > 1)
    .map(([k, v]) => ({ normalizado: k, etiquetas: v }))

  // Un filtro para no leerse la lista entera: ?buscar=bases
  const buscar = normalizar(url.searchParams.get('buscar') || '')
  const coinciden = buscar ? todas.filter((t) => normalizar(t.nombre).includes(buscar)) : null

  return json({
    total: todas.length,
    paginas_leidas: paginas,
    duplicadas,
    ...(coinciden ? { buscando: buscar, coinciden } : { etiquetas: todas }),
  })
}
