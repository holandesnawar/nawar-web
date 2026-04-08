import { useState } from 'react'

const BENEFITS = [
  'Diseñado para hispanohablantes',
  'Sin experiencia previa necesaria',
  'Garantía 15 días, reembolso completo',
]

export default function FooterLanding() {
  const [email, setEmail] = useState('')
  const [sent,  setSent]  = useState(false)
  const [error, setError] = useState(false)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!email.includes('@')) { setError(true); return }
    setError(false)
    setSent(true)
    setEmail('')
  }

  return (
    <footer data-navbar="dark" className="bg-[#F0F5FF]">
      {/* Email signup */}
      <div className="relative overflow-hidden">
        <div aria-hidden className="absolute inset-0 pointer-events-none">
          <div
            className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[600px]"
            style={{ background: 'radial-gradient(ellipse at center, rgba(77,163,255,0.15) 0%, transparent 60%)' }}
          />
        </div>

        <div className="relative max-w-2xl mx-auto px-6 py-20 md:py-24 text-center">
          <h2
            className="text-[32px] md:text-[40px] font-bold text-[#1D0084] leading-tight mb-4"
            style={{ fontFamily: 'var(--font-poppins), system-ui, sans-serif' }}
          >
            Aprende como el 1%
          </h2>
          <p className="text-[16px] text-[#5A6480] leading-relaxed mb-8 max-w-md mx-auto">
            Únete a la lista de espera y sé el primero en saber cuando abramos plazas.
          </p>

          <div className="flex flex-col items-center gap-3 mb-8">
            {BENEFITS.map((benefit, i) => (
              <div key={i} className="flex items-center gap-3">
                <span className="w-5 h-5 rounded-full bg-[#1D0084]/10 flex items-center justify-center shrink-0">
                  <svg className="w-3 h-3 text-[#1D0084]" fill="none" stroke="currentColor" strokeWidth={3} viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                  </svg>
                </span>
                <span className="text-[15px] text-[#374151]">{benefit}</span>
              </div>
            ))}
          </div>

          {sent ? (
            <div className="inline-flex items-center gap-3 px-6 py-4 rounded-2xl bg-[#1D0084]/8 border border-[#1D0084]/15">
              <svg className="w-5 h-5 text-[#025dc7] shrink-0" fill="none" stroke="currentColor" strokeWidth={2.5} viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
              </svg>
              <span className="text-[15px] font-medium text-[#1D0084]">¡Apuntado! Te avisaremos pronto.</span>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row gap-3 max-w-md mx-auto">
              <input
                type="email"
                value={email}
                onChange={(e) => { setEmail(e.target.value); setError(false) }}
                placeholder="Introduce tu email"
                className={`flex-1 px-5 py-4 rounded-xl bg-white border text-[#1D0084] placeholder:text-[#9CA3AF] text-[15px] outline-none transition-all shadow-sm ${
                  error ? 'border-red-400' : 'border-[#DDE6F5] focus:border-[#025dc7]/50'
                }`}
              />
              <button
                type="submit"
                className="px-6 py-4 rounded-xl bg-[#1D0084] text-white text-[15px] font-semibold hover:bg-[#025dc7] transition-colors duration-200 shadow-[0_4px_14px_rgba(29,0,132,0.20)] whitespace-nowrap inline-flex items-center justify-center gap-2"
              >
                Lista de espera
                <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth={2.5} viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M17 8l4 4m0 0l-4 4m4-4H3" />
                </svg>
              </button>
            </form>
          )}

          {error && <p className="text-[13px] text-red-500 mt-3">Introduce un email válido.</p>}

          <p className="text-[12px] text-[#9CA3AF] mt-5">
            Al apuntarte, aceptas recibir emails sobre cursos de neerlandés.
          </p>
        </div>
      </div>

      {/* Minimal bottom */}
      <div className="border-t border-[#DDE6F5] bg-white">
        <div className="max-w-6xl mx-auto px-6 py-8">
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
            <img
              src="https://d1yei2z3i6k35z.cloudfront.net/9533860/671a9c9265e23_Logo_Nawar_2.png"
              alt="Nawar"
              className="h-7 w-auto object-contain opacity-70"
            />
            <div className="flex items-center gap-6 text-[13px] text-[#9CA3AF]">
              <a href="#" className="hover:text-[#1D0084] transition-colors">Privacidad</a>
              <a href="#" className="hover:text-[#1D0084] transition-colors">Términos</a>
              <a href="mailto:hola@holandesnawar.com" className="hover:text-[#1D0084] transition-colors">Contacto</a>
            </div>
            <p className="text-[12px] text-[#9CA3AF]">© {new Date().getFullYear()} Nawar</p>
          </div>
        </div>
      </div>
    </footer>
  )
}
