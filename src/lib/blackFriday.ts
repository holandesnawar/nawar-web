/**
 * El embudo de Black Friday (29/10 → 30/11/2026), todo en un sitio.
 *
 * Cómo va (28/10, segunda vuelta, "como YouTalk"):
 *  1. La PORTADA (`/`) es solo un formulario para desbloquear la oferta:
 *     nombre, correo y WhatsApp. La escuela lo apunta (`bf-lista`), le manda
 *     el correo de acceso y lo mete en la campaña. Para orgánico, bio y
 *     correos. Recorrido `bf-desbloquear`.
 *  2. La LANDING (`/oferta`), con luz: la formación contada SIN precio,
 *     "acceso anticipado a las condiciones especiales". Las condiciones las
 *     cuenta el closer. Los correos de la campaña llevan aquí con nombre y
 *     correo en la dirección, así que nadie los vuelve a escribir.
 *  3. La página del ebook a 1 € sigue para los anuncios, en dos copias
 *     (/ebook orgánico, /ebook-ads anuncios). Al pagar, Stripe le devuelve a
 *     /oferta?compra=cs_… con la barra roja de "no cierres esta página".
 *  4. Todos los botones, al formulario de admisión (/admision): la edad la
 *     primera, sin pedir lo que ya se sabe, y de ahí a Calendly.
 * La escuela manda el ebook, el correo de acceso y la campaña hasta el 30/11
 * (learnhouse: services/ebook).
 *
 * ⚠️ Dos sitios para las mismas páginas: en producción se sirven en el
 * subdominio blackfriday.holandesnawar.com, en `/`, `/oferta`, `/ebook`,
 * `/ebook-ads` y `/admision` (ver src/lib/integracionSubdominios.ts); en www y en local viven
 * en `/black-friday/…`. Por eso los enlaces entre ellas salen SIEMPRE de
 * `bfRuta()`, nunca escritos a mano. PUBLIC_BLACKFRIDAY_URL lo cambia (en
 * local: http://localhost:<puerto>/black-friday).
 */

export const BF_URL = (
  (import.meta.env.PUBLIC_BLACKFRIDAY_URL as string | undefined) || 'https://blackfriday.holandesnawar.com'
).replace(/\/+$/, '')

/** Una página del embudo: bfRuta('/admision'), bfRuta('/') para la portada. */
export const bfRuta = (p = '/') => `${BF_URL}${p === '/' ? '/' : p.startsWith('/') ? p : `/${p}`}`

/** Cuándo empieza y cuándo acaba (hora de Países Bajos: en noviembre, +01:00). */
export const BF_DESDE = '2026-10-29'
export const BF_HASTA = '2026-11-30T23:59:59+01:00'
/** Para leerlo escrito. El Black Friday es el viernes 27/11; la oferta llega
 *  hasta el LUNES 30 (si algún texto dice el día de la semana, es lunes). */
export const BF_HASTA_TEXTO = 'lunes 30 de noviembre'

/** El ebook: el A0-A1 de siempre con nombre nuevo (usuario: "algo que llame
 *  la atención, no A0-A1 solo"). El PDF sigue siendo el mismo. */
export const EBOOK_NOMBRE = 'Neerlandés sin miedo'
export const EBOOK_SUB = '7 lecciones para arrancar desde cero (nivel A0-A1)'
export const EBOOK_PRECIO = 1

/** Las fotos del ebook, las de la página de siempre (/ebook-a0-a1). */
export const EBOOK_MOCKUP = 'https://d1yei2z3i6k35z.cloudfront.net/9533860/6733be7eb79b8_MOCKUP10.png'
export const EBOOK_MOCKUP_ABIERTO = 'https://d1yei2z3i6k35z.cloudfront.net/9533860/6733c5291da36_MOCKUP7.png'

/** El `content_name` de los eventos de Meta de este embudo. */
export const META_EBOOK = 'Ebook Black Friday'
export const META_BF = 'Black Friday'

/** Lo que se recuerda de la compra en esta visita (el Purchase, una vez). */
export const CLAVE_COMPRA = 'nawar.bf.compra'

/**
 * Que este navegador ya tiene la oferta desbloqueada (se apuntó en la portada
 * o compró el ebook): /oferta le enseña su cabecera aunque vuelva sin nada en
 * la dirección. El script en línea de /oferta lo lee con este mismo nombre.
 */
export const CLAVE_DESBLOQUEADA = 'nawar.bf.desbloqueada'

/**
 * La luz que sigue al ratón en las tarjetas oscuras (`.bf-sigue`): pone
 * --mx/--my y black-friday.css pinta ahí un foco. Solo con ratón (en el móvil
 * no hay "pasar por encima").
 */
export function iluminarAlPasar(): void {
  if (!window.matchMedia?.('(hover: hover) and (pointer: fine)').matches) return
  document.querySelectorAll<HTMLElement>('.bf-sigue').forEach((el) => {
    el.addEventListener('pointermove', (e) => {
      const r = el.getBoundingClientRect()
      el.style.setProperty('--mx', `${e.clientX - r.left}px`)
      el.style.setProperty('--my', `${e.clientY - r.top}px`)
    })
  })
}

/** ¿Ya pasó el 30/11 a las 23:59 en Países Bajos? */
export const bfTerminado = (ahora = Date.now()) => ahora > Date.parse(BF_HASTA)

/** Lo que queda, en días, horas, minutos y segundos (nunca negativo). */
export function quedaHasta(ahora = Date.now()) {
  const ms = Math.max(0, Date.parse(BF_HASTA) - ahora)
  const s = Math.floor(ms / 1000)
  return { dias: Math.floor(s / 86400), horas: Math.floor((s % 86400) / 3600), min: Math.floor((s % 3600) / 60), seg: s % 60 }
}

/**
 * Una dirección del embudo con lo que importa de la de ahora: los utm_*, el
 * fbclid (sin él no hay cookie _fbc y Meta pierde la atribución) y el nombre y
 * el correo para rellenar el formulario. El `compra=cs_…` de Stripe NO pasa:
 * es de esta página, y llevarlo al formulario no sirve de nada.
 */
export function conLaEntradaBF(destino: string, mas: Record<string, string> = {}): string {
  try {
    const actual = new URLSearchParams(window.location.search)
    const u = new URL(destino, window.location.href)
    for (const [k, v] of actual) {
      if (/^utm_[a-z]{1,20}$/.test(k) || k === 'fbclid' || k === 'nombre' || k === 'email') u.searchParams.set(k, v)
    }
    for (const [k, v] of Object.entries(mas)) if (v) u.searchParams.set(k, v)
    return u.toString()
  } catch {
    return destino
  }
}

/**
 * Pinta la cuenta atrás en cada `[data-bf-cuenta]` (con `[data-d]`, `[data-h]`,
 * `[data-m]`, `[data-s]` dentro) y, al llegar a cero, pone la clase
 * `bf-terminado` en <html>: cada página decide qué esconder con ella.
 */
export function arrancarCuentaAtras(): void {
  const dos = (n: number) => String(n).padStart(2, '0')
  const pintar = () => {
    if (bfTerminado()) {
      document.documentElement.classList.add('bf-terminado')
      return false
    }
    const q = quedaHasta()
    document.querySelectorAll<HTMLElement>('[data-bf-cuenta]').forEach((c) => {
      const poner = (sel: string, v: string) => { const el = c.querySelector(sel); if (el && el.textContent !== v) el.textContent = v }
      poner('[data-d]', String(q.dias))
      poner('[data-h]', dos(q.horas))
      poner('[data-m]', dos(q.min))
      poner('[data-s]', dos(q.seg))
    })
    return true
  }
  if (!pintar()) return
  const reloj = window.setInterval(() => { if (!pintar()) window.clearInterval(reloj) }, 1000)
}
