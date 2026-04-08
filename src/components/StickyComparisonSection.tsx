import { useRef, useState, useEffect } from 'react'

interface ComparisonItem {
  icon: string
  title: string
  nawarText: string
  classicText: string
}

interface Props {
  items: ComparisonItem[]
}

export default function StickyComparisonSection({ items }: Props) {
  const sectionRef = useRef<HTMLElement>(null)
  const [progress,     setProgress]     = useState(0)
  const [visibleItems, setVisibleItems] = useState<number[]>([])

  useEffect(() => {
    const onScroll = () => {
      const el = sectionRef.current
      if (!el) return
      const { top, height } = el.getBoundingClientRect()
      const travel = height - window.innerHeight
      const raw = travel > 0 ? (-top) / travel : 0
      const p = Math.min(Math.max(raw, 0), 1)
      setProgress(p)
      const visibleCount = Math.floor(p * items.length)
      setVisibleItems(Array.from({ length: visibleCount + 1 }, (_, i) => i))
    }
    window.addEventListener('scroll', onScroll, { passive: true })
    onScroll()
    return () => window.removeEventListener('scroll', onScroll)
  }, [items.length])

  return (
    <section ref={sectionRef} data-navbar="light" className="relative bg-white">
      <div aria-hidden className="absolute inset-0 dots-light pointer-events-none" />

      <div className="relative max-w-6xl mx-auto px-6">

        {/* Timeline — desktop only */}
        <div
          aria-hidden
          className="hidden lg:block absolute top-32 bottom-32 pointer-events-none"
          style={{ left: '50%', transform: 'translateX(-50%)', width: '20px' }}
        >
          <div
            className="absolute inset-y-0"
            style={{
              left: '50%', transform: 'translateX(-50%)', width: '2px',
              background: 'linear-gradient(to bottom, transparent 0%, #DDE6F5 15%, #DDE6F5 85%, transparent 100%)',
            }}
          />
          <div
            className="absolute w-4 h-4 rounded-full"
            style={{
              left: '50%', top: `${12 + progress * 76}%`,
              transform: 'translate(-50%, -50%)',
              background: 'linear-gradient(135deg, #4da3ff 0%, #025dc7 100%)',
              boxShadow: '0 0 0 4px rgba(77,163,255,0.20), 0 0 20px rgba(77,163,255,0.40)',
              transition: 'top 0.12s cubic-bezier(0.25, 1, 0.5, 1)',
            }}
          />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-0 items-start">

          {/* Left — sticky */}
          <div className="lg:sticky lg:top-[88px] pt-20 pb-20 lg:pr-16">
            <div className="space-y-6">
              <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-[#dde8f8] text-[#1D0084] eyebrow">
                <svg className="w-3 h-3 shrink-0" viewBox="0 0 12 12" fill="none"><path d="M2 6.5l2.5 2.5 5.5-6" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"/></svg>
                Nawar vs academias clásicas
              </span>

              <h2 className="title text-[#1D0084]">
                Lo que marca la{' '}
                <span className="text-[#025dc7]">diferencia</span>
              </h2>

              <p className="text-[17px] text-[#5A6480] leading-relaxed">
                No es solo un curso de idiomas. Es el método que debería haber existido desde el principio para cualquier hispanohablante que quiere aprender neerlandés.
              </p>

              <div className="flex items-center gap-4 pt-4">
                <div className="flex -space-x-2">
                  {['AG','CM','LP','RV'].map(ini => (
                    <div key={ini} className="w-9 h-9 rounded-full bg-[#1D0084] border-2 border-white flex items-center justify-center text-white text-[10px] font-bold">
                      {ini}
                    </div>
                  ))}
                </div>
                <p className="text-[14px] text-[#9CA3AF]">
                  <span className="text-[#1D0084] font-semibold">+600 estudiantes</span> ya lo han comprobado
                </p>
              </div>

              <a
                href="#lista-espera"
                className="inline-flex items-center gap-2 text-[#025dc7] font-semibold text-[15px] hover:text-[#1D0084] transition-colors group pt-2"
              >
                Ver todos los cursos
                <svg className="w-4 h-4 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" strokeWidth={2.5} viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M17 8l4 4m0 0l-4 4m4-4H3" />
                </svg>
              </a>
            </div>
          </div>

          {/* Right — scrolling rows */}
          <div className="pt-20 pb-20 lg:pl-8 space-y-5">
            {items.map((item, i) => {
              const isVisible = visibleItems.includes(i)
              return (
                <div
                  key={item.title}
                  className="p-6 rounded-2xl bg-[#F8FAFC] border border-[#E8EBF4] transition-all duration-500 ease-out"
                  style={{
                    opacity: isVisible ? 1 : 0.35,
                    transform: isVisible ? 'translateX(0)' : 'translateX(20px)',
                  }}
                >
                  <div className="flex gap-5 items-start">
                    <div className="w-12 h-12 shrink-0 rounded-2xl bg-white border border-[#DDE6F5] flex items-center justify-center text-2xl shadow-sm">
                      {item.icon}
                    </div>
                    <div className="space-y-3 flex-1">
                      <h3
                        className="text-[15px] font-semibold text-[#1D0084] leading-snug"
                        style={{ fontFamily: 'var(--font-poppins), system-ui, sans-serif' }}
                      >
                        {item.title}
                      </h3>
                      <div className="flex gap-3 items-start">
                        <span className="mt-0.5 w-5 h-5 shrink-0 rounded-full bg-[#025dc7] flex items-center justify-center">
                          <svg className="w-3 h-3 text-white" fill="none" stroke="currentColor" strokeWidth={3} viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                          </svg>
                        </span>
                        <p className="text-[13px] text-[#374151] leading-relaxed">{item.nawarText}</p>
                      </div>
                      <div className="flex gap-3 items-start">
                        <span className="mt-0.5 w-5 h-5 shrink-0 rounded-full bg-[#F0F5FF] border border-[#DDE6F5] flex items-center justify-center">
                          <svg className="w-3 h-3 text-[#9CA3AF]" fill="none" stroke="currentColor" strokeWidth={2.5} viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                          </svg>
                        </span>
                        <p className="text-[13px] text-[#9CA3AF] leading-relaxed">{item.classicText}</p>
                      </div>
                    </div>
                  </div>
                </div>
              )
            })}
          </div>

        </div>
      </div>
    </section>
  )
}
