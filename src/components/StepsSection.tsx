import { useRef, useState, useEffect } from 'react'

interface Step {
  number: string
  title: string
  description: string
}

interface Props {
  steps: Step[]
}

const N       = 5
const STEP_VH = 50
const PAD_VH  = 25
const SECTION_VH = 2 * PAD_VH + N * STEP_VH

/* ── Per-step visual elements ── */
const StepVisual01 = () => (
  <div className="glass rounded-2xl p-4 max-w-[280px] space-y-3">
    <p className="text-[10px] text-white/40 uppercase tracking-widest font-semibold">Tu ruta de aprendizaje</p>
    <div className="flex items-center gap-1.5">
      {(['A1','A2','B1','B2'] as const).map((level, i) => (
        <div key={level} className="flex items-center gap-1.5">
          <div className={`px-2.5 py-1 rounded-lg text-[11px] font-bold ${i === 0 ? 'bg-[#4da3ff] text-white' : 'bg-white/8 text-white/35'}`}>
            {level}
          </div>
          {i < 3 && <div className="w-3 h-px bg-white/15" />}
        </div>
      ))}
    </div>
    <p className="text-[11px] text-white/35">Módulo A1 · Lección 1 de 8</p>
  </div>
)

const StepVisual02 = () => (
  <div className="flex gap-2 max-w-[280px]">
    {[{nl:'goedemorgen',es:'buenos días'},{nl:'tot ziens',es:'hasta luego'}].map(v => (
      <div key={v.nl} className="glass rounded-xl p-3 flex-1">
        <p className="text-white text-[12px] font-bold">{v.nl}</p>
        <p className="text-[#4da3ff] text-[11px] mt-0.5">{v.es}</p>
      </div>
    ))}
  </div>
)

const StepVisual03 = () => (
  <div className="glass rounded-2xl p-4 max-w-[280px] space-y-3">
    <p className="text-[10px] text-white/40 uppercase tracking-widest font-semibold">Ejercicio</p>
    <p className="text-[13px] text-white/80">Ik ___ naar school.</p>
    <div className="flex gap-2">
      {['ga','gaat','gaan'].map((opt, i) => (
        <div key={opt} className={`px-3 py-1.5 rounded-lg text-[12px] font-semibold ${i === 0 ? 'bg-[#4da3ff] text-white' : 'bg-white/8 text-white/40'}`}>
          {opt}
        </div>
      ))}
    </div>
  </div>
)

const StepVisual04 = () => (
  <div className="space-y-2 max-w-[260px]">
    <div className="glass rounded-2xl rounded-tl-sm px-4 py-2.5">
      <p className="text-[12px] text-white/70">¿Por qué 'de' y cuándo 'het'?</p>
    </div>
    <div className="bg-[#4da3ff]/15 border border-[#4da3ff]/22 rounded-2xl rounded-tr-sm px-4 py-2.5 ml-6">
      <p className="text-[12px] text-white/75">En neerlandés hay dos géneros: común y neutro. Te lo explico con ejemplos del español…</p>
    </div>
  </div>
)

const StepVisual05 = () => (
  <div className="glass rounded-2xl p-4 flex items-center gap-4 max-w-[260px]">
    <div className="w-12 h-12 shrink-0 rounded-2xl bg-[#4da3ff]/15 border border-[#4da3ff]/22 flex items-center justify-center text-2xl">🏆</div>
    <div>
      <p className="text-white font-bold text-[14px]">Nivel B1</p>
      <p className="text-[11px] text-white/45 mt-0.5">Base sólida alcanzada</p>
    </div>
  </div>
)

const STEP_VISUALS = [StepVisual01, StepVisual02, StepVisual03, StepVisual04, StepVisual05]

export default function StepsSection({ steps }: Props) {
  const desktopRef = useRef<HTMLDivElement>(null)
  const [ty,       setTy]       = useState(0)
  const [progress, setProgress] = useState(0)

  useEffect(() => {
    const onScroll = () => {
      const el = desktopRef.current
      if (!el) return
      const { top, height } = el.getBoundingClientRect()
      const travel = height - window.innerHeight
      if (travel <= 0) return
      const prog = Math.min(Math.max(-top / travel, 0), 1)
      setProgress(prog)
      setTy(-prog * travel)
    }
    window.addEventListener('scroll', onScroll, { passive: true })
    onScroll()
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  const dotPct = 15 + progress * 70

  const stepOpacity = (i: number): number => {
    if (typeof window === 'undefined') return 1
    const wh     = window.innerHeight
    const stepPx = (STEP_VH / 100) * wh
    const padPx  = (PAD_VH  / 100) * wh
    const centerInViewport = padPx + (i + 0.5) * stepPx + ty
    const dist     = Math.abs(centerInViewport - wh / 2)
    const distNorm = dist / stepPx
    return Math.max(0.15, 1 - distNorm * 0.85)
  }

  const stepTranslate = (i: number): number => {
    if (typeof window === 'undefined') return 0
    const wh     = window.innerHeight
    const stepPx = (STEP_VH / 100) * wh
    const padPx  = (PAD_VH  / 100) * wh
    const centerInViewport = padPx + (i + 0.5) * stepPx + ty
    const offsetFromCenter = centerInViewport - wh / 2
    const normalizedOffset = offsetFromCenter / stepPx
    return Math.max(-50, Math.min(50, normalizedOffset * 45))
  }

  return (
    <section id="metodo" data-navbar="dark" className="relative bg-[#1D0084]">
      <div
        aria-hidden
        className="absolute inset-0 pointer-events-none"
        style={{ background: 'radial-gradient(ellipse 70% 45% at 50% 0%, rgba(11,109,240,0.22) 0%, transparent 70%)' }}
      />
      <div aria-hidden className="absolute inset-0 dots-dark pointer-events-none opacity-38" />

      {/* Mobile */}
      <div className="lg:hidden relative z-10 max-w-xl mx-auto px-6 py-28">
        <div className="mb-16 space-y-4">
          <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-[#025dc7] text-[#e0f2ff] eyebrow">
            <svg className="w-3 h-3 shrink-0" viewBox="0 0 12 12" fill="none"><path d="M2 6.5l2.5 2.5 5.5-6" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"/></svg>
            El proceso
          </span>
          <h2 className="title text-white">
            Así avanzas dentro{' '}
            <span className="text-[#4da3ff]">de la academia</span>
          </h2>
        </div>

        <div className="relative pl-8 border-l border-white/10 space-y-16">
          {steps.map((step) => (
            <div key={step.number} className="relative">
              <div
                className="absolute -left-[32px] top-2 w-3.5 h-3.5 rounded-full bg-[#4da3ff] border-2 border-[#1D0084]"
                style={{ boxShadow: '0 0 0 4px rgba(77,163,255,0.18)' }}
              />
              <div className="inline-flex items-center px-3 py-1 rounded-full border border-white/20 bg-white/6 mb-3">
                <span className="text-[11px] font-bold tracking-[0.15em] text-white/55" style={{ fontFamily: 'monospace' }}>
                  {step.number}
                </span>
              </div>
              <h3
                className="text-[20px] font-semibold text-white leading-snug mb-3"
                style={{ fontFamily: 'var(--font-poppins), system-ui, sans-serif' }}
              >
                {step.title}
              </h3>
              <p className="text-[15px] text-white/70 leading-relaxed">{step.description}</p>
            </div>
          ))}
        </div>

        <div className="pt-16">
          <a
            href="/lista-de-espera"
            className="inline-flex items-center gap-2.5 px-7 py-3.5 rounded-xl bg-[#4da3ff] text-white text-[15px] font-semibold hover:bg-[#5eb4ff] transition-all duration-200 shadow-[0_4px_20px_rgba(77,163,255,0.28)]"
          >
            Únete a la lista de espera
            <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth={2.5} viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" d="M17 8l4 4m0 0l-4 4m4-4H3" />
            </svg>
          </a>
        </div>
      </div>

      {/* Desktop — scroll-driven */}
      <div
        ref={desktopRef}
        className="hidden lg:block relative"
        style={{ height: `${SECTION_VH}vh` }}
      >
        <div className="sticky top-0 h-screen overflow-hidden flex">

          {/* Left strip */}
          <div className="w-1/2 overflow-hidden relative">
            <div
              className="absolute top-0 left-0 right-0 z-10 pl-24 pr-10 pt-12 pb-6"
              style={{ opacity: Math.max(0, 1 - progress * 6) }}
            >
              <span className="eyebrow text-[#4da3ff]/55">El proceso</span>
            </div>

            <div style={{ transform: `translateY(${ty}px)`, paddingTop: `${PAD_VH}vh`, paddingBottom: `${PAD_VH}vh` }}>
              {steps.map((step, i) => (
                <div
                  key={step.number}
                  className="flex flex-col justify-center pl-24 pr-10 border-b border-white/6 last:border-0"
                  style={{
                    height: `${STEP_VH}vh`,
                    opacity: stepOpacity(i),
                    transform: `translateY(${stepTranslate(i)}px)`,
                    transition: 'opacity 0.12s ease, transform 0.12s ease',
                  }}
                >
                  <div className="inline-flex items-center px-3 py-1 rounded-full border border-white/20 bg-white/6 mb-5 self-start">
                    <span className="text-[11px] font-bold tracking-[0.15em] text-white/55" style={{ fontFamily: 'monospace' }}>
                      {step.number}
                    </span>
                  </div>
                  <h2 className="title-sm text-white leading-snug max-w-xs">{step.title}</h2>
                </div>
              ))}
            </div>
          </div>

          {/* Center line */}
          <div
            aria-hidden
            className="absolute top-0 bottom-0 pointer-events-none"
            style={{ left: '50%', transform: 'translateX(-50%)', width: '24px' }}
          >
            <div
              className="absolute"
              style={{
                left: '50%', transform: 'translateX(-50%)',
                width: '1px', top: '15%', bottom: '15%',
                background: 'linear-gradient(to bottom, transparent 0%, rgba(255,255,255,0.10) 8%, rgba(255,255,255,0.10) 92%, transparent 100%)',
              }}
            />
            <div
              className="absolute"
              style={{ left: '50%', top: `${dotPct}%`, transform: 'translate(-50%, -50%)', transition: 'top 0.06s linear' }}
            >
              <div
                className="w-[18px] h-[18px] rounded-full bg-[#4da3ff] border-2 border-[#1D0084]"
                style={{ boxShadow: '0 0 0 5px rgba(77,163,255,0.18), 0 0 18px rgba(77,163,255,0.55)' }}
              />
            </div>
          </div>

          {/* Right strip */}
          <div className="w-1/2 overflow-hidden relative">
            <div style={{ transform: `translateY(${ty}px)`, paddingTop: `${PAD_VH}vh`, paddingBottom: `${PAD_VH}vh` }}>
              {steps.map((step, i) => {
                const Visual = STEP_VISUALS[i] || STEP_VISUALS[0]
                return (
                  <div
                    key={step.number}
                    className="flex flex-col justify-center pl-10 pr-24 border-b border-white/6 last:border-0"
                    style={{
                      height: `${STEP_VH}vh`,
                      opacity: stepOpacity(i),
                      transform: `translateY(${stepTranslate(i)}px)`,
                      transition: 'opacity 0.12s ease, transform 0.12s ease',
                    }}
                  >
                    <p className="text-[17px] text-white/85 leading-[1.75] max-w-sm mb-6">{step.description}</p>
                    <Visual />
                    {i === steps.length - 1 && (
                      <a
                        href="/lista-de-espera"
                        className="mt-7 inline-flex items-center gap-2.5 px-6 py-3 rounded-xl bg-[#4da3ff] text-white text-[14px] font-semibold hover:bg-[#5eb4ff] transition-all duration-200 shadow-[0_4px_20px_rgba(77,163,255,0.28)] self-start"
                      >
                        Únete a la lista de espera
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth={2.5} viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" d="M17 8l4 4m0 0l-4 4m4-4H3" />
                        </svg>
                      </a>
                    )}
                  </div>
                )
              })}
            </div>
          </div>

        </div>
      </div>
    </section>
  )
}
