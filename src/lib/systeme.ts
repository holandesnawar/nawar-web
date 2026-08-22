/**
 * Cliente mínimo de la API de systeme.io.
 *
 * Las formas de esta API no están adivinadas: salen de `src/pages/api/waitlist.ts`,
 * que lleva meses dando de alta gente de verdad en la cuenta de Nawar. Lo que
 * aquí se añade encima es lo que aquel no tenía: presupuesto de tiempo,
 * reintentos y caché de etiquetas.
 *
 * Un detalle que se nota al mirar las respuestas: `items` + `itemsPerPage` es la
 * firma de API Platform (el estándar de APIs de Symfony). Por eso el PATCH pide
 * `application/merge-patch+json` y no el `application/json` de siempre — con el
 * normal contesta 415. El código prueba los tres en cascada por si acaso.
 */

const BASE = 'https://api.systeme.io/api'

/** Tope por llamada, como pide el encargo. */
const TIMEOUT_MS = 8_000
/** Reintentos SOLO ante 5xx o timeout. Un 4xx es un "no" definitivo. */
const REINTENTOS = 2
/** Espera entre reintentos: 400 ms, luego 800 ms. */
const ESPERA_BASE_MS = 400
/** Cuánto vale la caché de etiquetas. Diez minutos: si renombras una en el
 *  panel, el webhook se entera solo sin tener que redesplegar. */
const TAG_CACHE_MS = 10 * 60_000

// ── Utilidades ───────────────────────────────────────────────────────────────

const dormir = (ms: number) => new Promise((r) => setTimeout(r, ms))

function jsonSeguro(texto: string): any {
  try {
    return JSON.parse(texto)
  } catch {
    return null
  }
}

/** Lee una variable de entorno en desarrollo y en el serverless de Vercel. */
export function leerEnv(nombre: string): string | undefined {
  const desdeVite = (import.meta.env as Record<string, unknown>)[nombre]
  if (typeof desdeVite === 'string' && desdeVite) return desdeVite
  if (typeof process !== 'undefined') return process.env[nombre]
  return undefined
}

/**
 * Reloj de la petición.
 *
 * Existe porque una función serverless de Vercel se muere sola a los 10 s por
 * defecto. Si la matáramos a mitad, Inrō vería un fallo y reintentaría — justo
 * lo que el encargo quiere evitar. Así que hay un presupuesto global: cuando se
 * acaba, se deja de llamar a systeme.io y se contesta igual, dejando escrito en
 * el log qué se quedó sin hacer.
 *
 * Efecto secundario a tener presente: si la primera llamada agota los 8 s, no
 * queda tiempo para el reintento. Es a propósito — contestar vale más que
 * reintentar. Si quieres la escalera de reintentos entera, sube el `maxDuration`
 * del adaptador de Vercel y con él este presupuesto.
 */
export interface Reloj {
  restante(): number
}

export function relojDe(presupuestoMs: number): Reloj {
  const fin = Date.now() + presupuestoMs
  return { restante: () => Math.max(0, fin - Date.now()) }
}

export interface Ctx {
  apiKey: string
  reloj: Reloj
}

export interface Respuesta<T = any> {
  ok: boolean
  /** 0 = no llegó a haber respuesta (timeout, red caída o sin presupuesto). */
  status: number
  data: T | null
  error?: string
}

async function pedir<T = any>(path: string, init: RequestInit, ctx: Ctx): Promise<Respuesta<T>> {
  let ultima: Respuesta<T> = { ok: false, status: 0, data: null, error: 'sin presupuesto de tiempo' }

  for (let intento = 0; intento <= REINTENTOS; intento++) {
    if (intento > 0) {
      const espera = ESPERA_BASE_MS * 2 ** (intento - 1)
      if (ctx.reloj.restante() <= espera) return ultima
      await dormir(espera)
    }

    const margen = Math.min(TIMEOUT_MS, ctx.reloj.restante())
    if (margen <= 0) return ultima

    try {
      const res = await fetch(`${BASE}${path}`, {
        ...init,
        headers: {
          'X-API-Key': ctx.apiKey,
          accept: 'application/json',
          ...((init.headers as Record<string, string> | undefined) ?? {}),
        },
        signal: AbortSignal.timeout(margen),
      })
      const texto = await res.text()
      ultima = {
        ok: res.ok,
        status: res.status,
        data: texto ? jsonSeguro(texto) : null,
        error: res.ok ? undefined : texto.slice(0, 300),
      }
      // 4xx no se reintenta: repetir la misma petición daría el mismo "no".
      if (res.ok || res.status < 500) return ultima
    } catch (e) {
      ultima = { ok: false, status: 0, data: null, error: (e as Error).message }
    }
  }

  return ultima
}

const jsonHeaders = { 'Content-Type': 'application/json' }

// ── Etiquetas ────────────────────────────────────────────────────────────────

/**
 * Deja el nombre de una etiqueta en su forma comparable.
 *
 * Inrō manda `lista-de-espera` y en systeme.io la etiqueta se llama
 * `Lista de espera`. Son la misma, y queremos que todo el mundo caiga en ella
 * venga de Instagram o de la web, así que se comparan sin mayúsculas, sin
 * acentos y tratando guiones y guiones bajos como espacios.
 */
export function normalizarEtiqueta(nombre: string): string {
  return nombre
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .replace(/[\s_-]+/g, ' ')
    .trim()
}

/** Caché de proceso. En serverless cada instancia tiene la suya, que es justo
 *  lo que queremos: sirve para no listar etiquetas en cada mensaje y no
 *  necesita almacén compartido. */
let cacheEtiquetas: { mapa: Map<string, number>; expira: number } | null = null

async function listarEtiquetas(ctx: Ctx): Promise<Map<string, number> | null> {
  if (cacheEtiquetas && Date.now() < cacheEtiquetas.expira) return cacheEtiquetas.mapa

  const mapa = new Map<string, number>()
  // Tope de 10 páginas (1.000 etiquetas). Es un cortafuegos, no un límite real:
  // si alguna vez se superara, mejor una etiqueta sin encontrar que un bucle.
  for (let pagina = 1; pagina <= 10; pagina++) {
    const res = await pedir<{ items?: { id: number; name: string }[] }>(
      `/tags?itemsPerPage=100&page=${pagina}`,
      { method: 'GET' },
      ctx
    )
    if (!res.ok) return mapa.size ? mapa : null
    const items = res.data?.items ?? []
    for (const t of items) {
      if (t?.name && typeof t.id === 'number') mapa.set(normalizarEtiqueta(t.name), t.id)
    }
    if (items.length < 100) break
  }

  cacheEtiquetas = { mapa, expira: Date.now() + TAG_CACHE_MS }
  return mapa
}

export interface EtiquetaResuelta {
  id: number | null
  /** 'cache' | 'encontrada' | 'creada' | 'fallo' — para el log. */
  via: string
}

/**
 * Nombre de etiqueta → id. Si no existe en la cuenta, la crea.
 *
 * La creación es best-effort a propósito: si la API no dejara crear etiquetas,
 * el contacto igualmente se da de alta y el fallo queda en el log.
 */
export async function resolverEtiqueta(nombre: string, ctx: Ctx): Promise<EtiquetaResuelta> {
  const clave = normalizarEtiqueta(nombre)
  if (!clave) return { id: null, via: 'nombre vacío' }

  const enCache = cacheEtiquetas && Date.now() < cacheEtiquetas.expira
  const mapa = await listarEtiquetas(ctx)
  if (mapa?.has(clave)) return { id: mapa.get(clave)!, via: enCache ? 'cache' : 'encontrada' }
  if (!mapa) return { id: null, via: 'fallo listando' }

  const res = await pedir<{ id?: number }>(
    '/tags',
    { method: 'POST', headers: jsonHeaders, body: JSON.stringify({ name: nombre }) },
    ctx
  )
  const id = typeof res.data?.id === 'number' ? res.data.id : null
  if (id !== null) {
    mapa.set(clave, id)
    return { id, via: 'creada' }
  }
  return { id: null, via: `fallo creando (${res.status})` }
}

/** Pone la etiqueta al contacto. Un 409 es "ya la tenía" → también es éxito. */
export async function asignarEtiqueta(contactId: number, tagId: number, ctx: Ctx): Promise<Respuesta> {
  const res = await pedir(
    `/contacts/${contactId}/tags`,
    { method: 'POST', headers: jsonHeaders, body: JSON.stringify({ tagId }) },
    ctx
  )
  if (res.status === 409) return { ...res, ok: true }
  return res
}

// ── Contactos ────────────────────────────────────────────────────────────────

export interface ContactoResuelto {
  id: number | null
  /** 'creado' | 'ya existía' | 'fallo'. */
  via: string
  status: number
  error?: string
}

/**
 * Da de alta el contacto, y si ya estaba lo recupera por email.
 *
 * Se crea **sin campos personalizados** a propósito. Si un slug estuviera mal
 * escrito o el campo no existiera todavía en la cuenta, un POST con `fields`
 * fallaría entero y perderíamos el contacto; separándolo, lo peor que pasa es
 * que la persona entra sin las UTMs y el fallo queda escrito en el log.
 */
export async function crearOBuscarContacto(
  email: string,
  firstName: string,
  surname: string,
  ctx: Ctx
): Promise<ContactoResuelto> {
  const body: Record<string, string> = { email }
  if (firstName) body.firstName = firstName
  if (surname) body.surname = surname

  const creado = await pedir<{ id?: number }>(
    '/contacts',
    { method: 'POST', headers: jsonHeaders, body: JSON.stringify(body) },
    ctx
  )
  if (creado.ok && typeof creado.data?.id === 'number') {
    return { id: creado.data.id, via: 'creado', status: creado.status }
  }

  // La API contesta 4xx si el email ya está. Eso no es un error: es la vía
  // normal cuando alguien vuelve a escribir por el DM.
  const buscado = await pedir<any>(`/contacts?email=${encodeURIComponent(email)}`, { method: 'GET' }, ctx)
  if (buscado.ok) {
    const d = buscado.data
    const items = d?.items ?? d?.contacts ?? (Array.isArray(d) ? d : null)
    const id = Array.isArray(items) && items.length ? items[0]?.id : d?.id
    if (typeof id === 'number') return { id, via: 'ya existía', status: creado.status }
  }

  return {
    id: null,
    via: 'fallo',
    status: creado.status,
    error: creado.error ?? buscado.error,
  }
}

/**
 * Escribe los campos personalizados del contacto.
 *
 * PATCH en tres pasadas: `merge-patch+json` (lo que pide API Platform), luego
 * `application/json` por si acaso, y `PUT` si contesta 405 — la misma cascada
 * que ya hacía falta en la ruta de la lista de espera.
 */
export async function escribirCampos(
  contactId: number,
  campos: { slug: string; value: string }[],
  ctx: Ctx
): Promise<Respuesta> {
  if (!campos.length) return { ok: true, status: 204, data: null }
  const cuerpo = JSON.stringify({ fields: campos })

  let res = await pedir(
    `/contacts/${contactId}`,
    { method: 'PATCH', headers: { 'Content-Type': 'application/merge-patch+json' }, body: cuerpo },
    ctx
  )
  if (!res.ok && res.status === 415) {
    res = await pedir(`/contacts/${contactId}`, { method: 'PATCH', headers: jsonHeaders, body: cuerpo }, ctx)
  }
  if (!res.ok && res.status === 405) {
    res = await pedir(`/contacts/${contactId}`, { method: 'PUT', headers: jsonHeaders, body: cuerpo }, ctx)
  }
  return res
}
