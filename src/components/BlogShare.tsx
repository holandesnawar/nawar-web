import { useState } from 'react'

export default function BlogShare({ title }: { title: string }) {
  const [copied, setCopied] = useState(false)

  const url = typeof window !== 'undefined' ? window.location.href : ''

  const copy = () => {
    navigator.clipboard.writeText(url).then(() => {
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    })
  }

  return (
    <div className="sticky top-28 flex flex-col items-center gap-3 pt-1">
      <p className="text-[10px] font-semibold text-[#9CA3AF] uppercase tracking-[0.14em] mb-1">
        Compartir
      </p>

      {/* X / Twitter */}
      <a
        href={`https://twitter.com/intent/tweet?text=${encodeURIComponent(title)}&url=${encodeURIComponent(url)}`}
        target="_blank"
        rel="noopener noreferrer"
        title="Compartir en X"
        className="w-9 h-9 flex items-center justify-center rounded-full border border-[#DDE6F5] bg-white text-[#374151] hover:bg-[#F0F5FF] hover:border-[#025dc7]/40 hover:text-[#025dc7] transition-all duration-200"
      >
        <svg className="w-[15px] h-[15px]" fill="currentColor" viewBox="0 0 24 24">
          <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-4.714-6.231-5.401 6.231H2.747l7.73-8.835L1.254 2.25H8.08l4.262 5.633 5.9-5.633Zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
        </svg>
      </a>

      {/* LinkedIn */}
      <a
        href={`https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(url)}`}
        target="_blank"
        rel="noopener noreferrer"
        title="Compartir en LinkedIn"
        className="w-9 h-9 flex items-center justify-center rounded-full border border-[#DDE6F5] bg-white text-[#374151] hover:bg-[#F0F5FF] hover:border-[#025dc7]/40 hover:text-[#025dc7] transition-all duration-200"
      >
        <svg className="w-[15px] h-[15px]" fill="currentColor" viewBox="0 0 24 24">
          <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 0 1-2.063-2.065 2.064 2.064 0 1 1 2.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
        </svg>
      </a>

      {/* Copy link */}
      <button
        onClick={copy}
        title={copied ? '¡Copiado!' : 'Copiar enlace'}
        className="w-9 h-9 flex items-center justify-center rounded-full border border-[#DDE6F5] bg-white text-[#374151] hover:bg-[#F0F5FF] hover:border-[#025dc7]/40 hover:text-[#025dc7] transition-all duration-200"
      >
        {copied
          ? <svg className="w-[15px] h-[15px] text-emerald-500" fill="none" stroke="currentColor" strokeWidth={2.5} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7"/></svg>
          : <svg className="w-[15px] h-[15px]" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"/></svg>
        }
      </button>
    </div>
  )
}
