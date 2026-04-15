// Pure CSS sticky — left column fixed while right scrolls naturally through the section.
// Both columns start at the same visual height.

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
  return (
    <section data-navbar="light" className="sc-section relative bg-[#F0F5FF]" style={{ overflowX: 'clip' }}>
      <div aria-hidden className="absolute inset-0 dots-light pointer-events-none opacity-40" />

      <div className="relative max-w-6xl mx-auto px-6">
        {/* align-items: flex-start so both columns begin at the same top */}
        <div className="flex flex-col lg:flex-row lg:items-start">

          {/* Left — sticky, align-self:start is required for sticky inside flex */}
          <div
            className="lg:w-[42%] shrink-0 lg:sticky lg:top-[72px] lg:h-[calc(100vh-72px)]"
            style={{ display: 'flex', alignItems: 'flex-start', alignSelf: 'flex-start' }}
          >
            <div className="space-y-6 w-full py-10 lg:py-16 lg:pr-16">
              <span className="badge-light eyebrow">
                <svg className="check-icon" fill="none" viewBox="0 0 12 12">
                  <path d="M2 6.5l2.5 2.5 5.5-6" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
                Nawar vs academias clásicas
              </span>

              <h2 className="title text-[#1D0084]" style={{ fontSize: 'clamp(26px, 3.2vw, 42px)' }}>
                Lo que nos hace<br />diferente al resto
              </h2>

              <p className="text-[15px] text-[#1D0084] leading-relaxed" style={{ opacity: 0.85 }}>
                No es solo un curso de idiomas. Es el método que debería haber existido desde el principio.
              </p>
            </div>
          </div>

          {/* Right — normal scroll, cards flow naturally */}
          <div className="lg:w-[58%] pt-2 pb-10 lg:py-20 space-y-5">
            {items.map((item) => (
              <div key={item.title} className="bg-white rounded-3xl p-8">
                <div className="flex items-center gap-4 mb-6">
                  <div className="w-14 h-14 shrink-0 rounded-2xl bg-[#F0F5FF] flex items-center justify-center text-3xl">
                    {item.icon}
                  </div>
                  <h3
                    className="text-[18px] font-semibold text-[#1D0084] leading-snug"
                    style={{ fontFamily: 'var(--font-poppins), system-ui, sans-serif' }}
                  >
                    {item.title}
                  </h3>
                </div>

                <div className="mb-3 p-4 rounded-2xl bg-[#F0F8FF]">
                  <p className="text-[11px] font-bold uppercase tracking-wider text-[#025dc7] mb-2">Con Nawar</p>
                  <div className="flex gap-3 items-start">
                    <span className="mt-0.5 w-5 h-5 shrink-0 rounded-full bg-[#025dc7] flex items-center justify-center">
                      <svg className="w-3 h-3 text-white" fill="none" stroke="currentColor" strokeWidth={3} viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                      </svg>
                    </span>
                    <p className="text-[14px] text-[#1D0084] leading-relaxed font-medium">{item.nawarText}</p>
                  </div>
                </div>

                <div className="p-4 rounded-2xl bg-[#F8FAFC]">
                  <p className="text-[11px] font-bold uppercase tracking-wider text-[#9CA3AF] mb-2">Academia clásica</p>
                  <div className="flex gap-3 items-start">
                    <span className="mt-0.5 w-5 h-5 shrink-0 rounded-full bg-[#E8EBF4] flex items-center justify-center">
                      <svg className="w-3 h-3 text-[#9CA3AF]" fill="none" stroke="currentColor" strokeWidth={2.5} viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                      </svg>
                    </span>
                    <p className="text-[14px] text-[#9CA3AF] leading-relaxed">{item.classicText}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>

        </div>
      </div>
    </section>
  )
}
