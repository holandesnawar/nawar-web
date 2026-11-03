import { useState, useEffect, useCallback, useRef } from 'react'

// El botón "Matricularme" (los tres: escritorio, tablet y menú móvil) sale del
// mismo sitio que los demás botones de la web, en src/lib/cta.ts. Antes tenía
// aquí su propia constante y eso hacía que el menú y el cuerpo de la página
// pudieran apuntar a destinos distintos sin que nadie se diera cuenta.
//
// ⚠️ Si algún día vuelve a apuntar a la landing, la ruta es '/formacion-a0-a1',
// SIN el "-sept": aquélla se renombró y ahora redirige (302) a la lista de
// espera. Con el nombre viejo el botón seguiría funcionando pero llevaría a la
// lista de espera sin que nadie se diera cuenta.
import { CTA_PRINCIPAL } from '../lib/cta'
import { ESCUELA_URL } from '../lib/escuela'
import { bfRuta, bfTerminado } from '../lib/blackFriday'

// «Acceso a alumnos» va DIRECTO a la entrada de la escuela (14/10/2026). Antes
// llevaba a /acceso, un formulario de entrar que solo era diseño: contestaba
// siempre «Correo o contraseña incorrectos» y los alumnos nuevos creían que su
// contraseña no valía. /acceso y /login redirigen ahora a la escuela.
const ACCESO_ALUMNOS = `${ESCUELA_URL}/login`

const NAV_LINKS = [
  { label: 'Inicio',         href: '/' },
  { label: 'Nuestra visión', href: '/nuestra-vision' },
  { label: 'Blog',           href: '/blog' },
  { label: 'Contacto',       href: '/contacto' },
]

type NavTheme = 'dark' | 'light'

/** La barra de Black Friday de arriba (02/11, como la de YouTalk): lleva a
 *  la lista prioritaria (blackfriday.holandesnawar.com) con sus utm, para
 *  saber desde qué página de la web llegó. `utm_medium=barra`, nunca de pago:
 *  la portada mandaría a /ebook-ads y la ficha diría «Ads». Desaparece sola
 *  pasado el 30/11 (`bfTerminado`). */
const enlaceBarraBF = (desde: string) =>
  `${bfRuta('/')}?utm_source=web&utm_medium=barra&utm_campaign=black-friday&utm_content=barra-${encodeURIComponent(desde)}`

/** `ctaHref`: a dónde lleva «Matricularme» en esta página. Por defecto, el de
 *  toda la web (CTA_PRINCIPAL); /formacion lo usa para bajar a su propio
 *  formulario (09/10).
 *  `barraBF`: enseña la barra de Black Friday encima del menú; el valor dice
 *  qué página es (va en `utm_content`). Sin él, no sale (guías, legales,
 *  /formacion: ahí distraería). */
export default function NavbarLanding({ ctaHref = CTA_PRINCIPAL, barraBF = '' }: { ctaHref?: string; barraBF?: string } = {}) {
  const [menuOpen,    setMenuOpen]    = useState(false)
  const [menuClosing, setMenuClosing] = useState(false)
  const [conBarra,    setConBarra]    = useState(() => !!barraBF && !bfTerminado())
  const headerRef = useRef<HTMLElement>(null)
  const barraRef  = useRef<HTMLAnchorElement>(null)

  useEffect(() => {
    if (barraBF && bfTerminado()) setConBarra(false)
  }, [barraBF])

  const r = (href: string) => {
    if (!href.startsWith('#')) return href
    if (typeof window !== 'undefined' && window.location.pathname === '/') return href
    return `/${href}`
  }

  const update = useCallback(() => {
    const header = headerRef.current
    if (!header) return
    const sy  = window.scrollY
    const vh  = window.innerHeight

    const readTheme = (el: Element | null): NavTheme | null => {
      let node: Element | null = el
      while (node) {
        const t = node.getAttribute('data-navbar')
        if (t === 'light' || t === 'dark') return t as NavTheme
        node = node.parentElement
      }
      return null
    }

    // Con la barra de Black Friday, el menú empieza más abajo.
    const alto = barraRef.current?.offsetHeight ?? 0
    const themeBottom = readTheme(document.elementFromPoint(window.innerWidth / 2, 72 + alto))
    const themeTop    = readTheme(document.elementFromPoint(window.innerWidth / 2, 4 + alto))

    if (themeBottom === 'light') {
      header.style.transition = 'background-color 0.55s ease'
      header.style.backgroundColor = 'rgba(29,0,132,1)'
    } else if (themeTop === 'dark' && sy > vh * 0.9) {
      header.style.transition = 'background-color 0.55s ease'
      header.style.backgroundColor = 'rgba(29,0,132,0)'
    } else {
      const fadeStart = vh * 0.38
      const fadeEnd   = vh * 0.84
      const opacity   = Math.min(1, Math.max(0, (sy - fadeStart) / (fadeEnd - fadeStart)))
      header.style.transition = 'none'
      header.style.backgroundColor = `rgba(29,0,132,${opacity.toFixed(3)})`
    }
  }, [])

  useEffect(() => {
    update()
    window.addEventListener('scroll', update, { passive: true })
    return () => window.removeEventListener('scroll', update)
  }, [update])

  useEffect(() => {
    const handler = () => { if (window.innerWidth >= 1024) closeMenu() }
    window.addEventListener('resize', handler)
    return () => window.removeEventListener('resize', handler)
  }, [])

  useEffect(() => {
    document.body.style.overflow = menuOpen ? 'hidden' : ''
    return () => { document.body.style.overflow = '' }
  }, [menuOpen])

  const openMenu  = () => { setMenuClosing(false); setMenuOpen(true) }
  const closeMenu = () => {
    if (!menuOpen) return
    setMenuClosing(true)
    setTimeout(() => { setMenuOpen(false); setMenuClosing(false) }, 420)
  }
  const handleLink = () => closeMenu()
  const isMenuVisible = menuOpen || menuClosing

  return (
    <>
      {/* El hueco de la barra en la página: así la cabecera de cada página
          empieza debajo, como si la barra no estuviera. */}
      {conBarra && <div aria-hidden className="h-11 lg:h-12" style={{ background: '#1D0084' }} />}
      <header
        ref={headerRef}
        className="fixed top-0 inset-x-0 z-50"
        style={{ backgroundColor: 'rgba(29,0,132,0)' }}
      >
        {conBarra && (
          <a
            ref={barraRef}
            href={enlaceBarraBF(barraBF)}
            className="group relative flex h-11 lg:h-12 items-center justify-center gap-3 px-4 text-white"
            style={{ background: '#1D0084' }}
          >
            {/* En Inter, la letra del menú y los botones de al lado (03/11,
                usuario: "la misma letra que usamos en home"). Antes iba en
                Poppins y desentonaba con el menú. */}
            <span className="text-[13.5px] sm:text-[15px] font-semibold tracking-[-0.01em] whitespace-nowrap">
              Adelántate al <span className="font-bold text-[#4da3ff]">BLACK FRIDAY</span><span className="hidden sm:inline"> de Holandés Nawar</span>
            </span>
            <span className="inline-flex shrink-0 items-center gap-1.5 rounded-md bg-[#4da3ff] px-3 py-1.5 text-[12.5px] sm:text-[13px] font-bold text-[#0a1656] transition-colors group-hover:bg-[#5eb4ff]">
              <span className="sm:hidden">Apúntate</span>
              <span className="hidden sm:inline">Accede a la lista prioritaria</span>
              <svg className="w-3 h-3" fill="none" stroke="currentColor" strokeWidth={2.75} viewBox="0 0 24 24" aria-hidden>
                <path strokeLinecap="round" strokeLinejoin="round" d="M17 8l4 4m0 0l-4 4m4-4H3" />
              </svg>
            </span>
            {/* En el azul de la marca, no en negro (02/11, usuario: "con fondo
                negro queda feo"), con la línea roja y azul del logo debajo,
                como la barra de /oferta. */}
            <span aria-hidden className="absolute inset-x-0 bottom-0 h-[2px]" style={{ background: 'linear-gradient(90deg, #AE1C28 0 30%, #21468C 30% 100%)' }} />
          </a>
        )}
        <div className="max-w-6xl mx-auto px-6">
          <div className="h-[72px] flex items-center justify-between gap-8">

            {/* Logo */}
            <a href="/" className="shrink-0">
              <img
                src="https://d1yei2z3i6k35z.cloudfront.net/9533860/671a9c9265e23_Logo_Nawar_2.png"
                alt="Nawar"
                className="h-12 lg:h-11 w-auto object-contain"
              />
            </a>

            {/* Desktop links */}
            <nav className="hidden lg:flex items-center gap-1">
              {NAV_LINKS.map((link) => (
                <a
                  key={link.href}
                  href={r(link.href)}
                  className="px-4 py-2 text-[15px] font-bold text-white/88 hover:text-white/50 transition-colors duration-200"
                >
                  {link.label}
                </a>
              ))}
            </nav>

            {/* Desktop CTAs */}
            <div className="hidden lg:flex items-center gap-3">
              <a
                href={ACCESO_ALUMNOS}
                className="px-4 py-2 text-[15px] font-bold text-white/88 hover:text-white/50 transition-colors duration-200"
              >
                Acceso a alumnos
              </a>
              <a
                href={ctaHref}
                className="inline-flex items-center gap-2 px-7 py-3 text-[15px] font-semibold rounded-lg bg-[#4da3ff] text-[#1D0084] transition-colors duration-200"
              >
                Matricularme
                <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" strokeWidth={2.5} viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M17 8l4 4m0 0l-4 4m4-4H3" />
                </svg>
              </a>
            </div>

            {/* Mobile */}
            <div className="lg:hidden flex items-center gap-2">
              <a
                href={ctaHref}
                className="inline-flex items-center gap-1.5 px-5 py-2.5 rounded-lg bg-[#4da3ff] text-[#1D0084] text-[14px] font-semibold hover:bg-[#5eb4ff] transition-all duration-200"
              >
                Matricularme
                <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" strokeWidth={2.5} viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M17 8l4 4m0 0l-4 4m4-4H3" />
                </svg>
              </a>
              <button
                onClick={openMenu}
                className="w-10 h-10 flex items-center justify-center text-white/80 hover:text-white transition-colors duration-200"
                aria-label="Abrir menú"
              >
                <span className="flex flex-col gap-[5px] w-5">
                  <span className="block h-[1.5px] bg-current rounded-full" />
                  <span className="block h-[1.5px] bg-current rounded-full w-[70%]" />
                  <span className="block h-[1.5px] bg-current rounded-full" />
                </span>
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Mobile fullscreen overlay */}
      {isMenuVisible && (
        <div
          className={`fixed inset-0 z-[100] bg-[#1D0084] flex flex-col ${menuClosing ? 'menu-lift' : 'menu-drop'}`}
        >
          <div
            aria-hidden
            className="absolute inset-0 pointer-events-none"
            style={{ background: 'radial-gradient(ellipse 90% 55% at 50% -5%, rgba(11,109,240,0.30) 0%, transparent 65%)' }}
          />
          <div aria-hidden className="absolute inset-0 dots-dark pointer-events-none opacity-35" />

          <div className="relative z-10 flex-1 flex flex-col items-center justify-center px-8">
            <nav className="w-full">
              {NAV_LINKS.map((link, i) => (
                <a
                  key={link.href}
                  href={r(link.href)}
                  onClick={handleLink}
                  className="block py-3.5 text-[21px] font-semibold text-white hover:text-white/80 text-center transition-colors duration-200"
                  style={{
                    fontFamily: 'var(--font-poppins), system-ui, sans-serif',
                    animation: `link-reveal 0.55s cubic-bezier(0.16,1,0.3,1) ${0.10 + i * 0.065}s forwards`,
                    opacity: 0,
                  }}
                >
                  {link.label}
                </a>
              ))}
            </nav>

            <div
              className="w-full mt-5 space-y-3"
              style={{
                animation: `link-reveal 0.55s cubic-bezier(0.16,1,0.3,1) ${0.10 + NAV_LINKS.length * 0.065 + 0.05}s forwards`,
                opacity: 0,
              }}
            >
              <a
                href={ACCESO_ALUMNOS}
                onClick={handleLink}
                className="flex w-full items-center justify-center px-6 py-4 text-[15px] font-semibold rounded-lg bg-transparent border border-white/35 text-white hover:border-white/70 transition-all duration-200"
              >
                Acceso a alumnos
              </a>
              <a
                href={ctaHref}
                onClick={handleLink}
                className="flex w-full items-center justify-center gap-2.5 px-6 py-4 text-[16px] font-semibold rounded-lg bg-[#4da3ff] text-[#1D0084] hover:bg-[#5eb4ff] transition-all duration-200 shadow-[0_4px_20px_rgba(77,163,255,0.30)]"
              >
                Matricularme
                <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth={2.5} viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M17 8l4 4m0 0l-4 4m4-4H3" />
                </svg>
              </a>
            </div>

            <div
              className="mt-8 flex justify-center"
              style={{
                animation: `link-reveal 0.55s cubic-bezier(0.16,1,0.3,1) ${0.10 + NAV_LINKS.length * 0.065 + 0.15}s forwards`,
                opacity: 0,
              }}
            >
              <button
                onClick={closeMenu}
                className="w-10 h-10 flex items-center justify-center text-white hover:text-white/70 transition-colors duration-200"
                aria-label="Cerrar menú"
              >
                <svg className="w-7 h-7" fill="none" stroke="currentColor" strokeWidth={1.8} viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  )
}
