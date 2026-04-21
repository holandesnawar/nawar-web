import { useState } from 'react'

type Variant = 'sidebar' | 'inline'

export default function BlogShare({ title, variant = 'sidebar' }: { title: string; variant?: Variant }) {
  const [copied, setCopied] = useState(false)

  const url = typeof window !== 'undefined' ? window.location.href : ''

  const copy = () => {
    navigator.clipboard.writeText(url).then(() => {
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    })
  }

  const isSidebar = variant === 'sidebar'

  const wrapperClass = isSidebar
    ? 'sticky top-28 flex flex-col items-center gap-3 pt-1'
    : 'flex items-center gap-3 flex-wrap'

  const iconBtn =
    'w-10 h-10 flex items-center justify-center rounded-full border border-[#DDE6F5] bg-white text-[#374151] hover:bg-[#F0F5FF] hover:border-[#025dc7]/40 hover:text-[#025dc7] transition-all duration-200'

  const shareText = encodeURIComponent(`${title} — Holandés Nawar`)
  const shareUrl  = encodeURIComponent(url)

  return (
    <div className={wrapperClass}>
      {isSidebar && (
        <p className="text-[10px] font-semibold text-[#9CA3AF] uppercase tracking-[0.14em] mb-1">
          Compartir
        </p>
      )}

      {/* WhatsApp */}
      <a
        href={`https://wa.me/?text=${shareText}%20${shareUrl}`}
        target="_blank"
        rel="noopener noreferrer"
        title="Compartir en WhatsApp"
        aria-label="Compartir en WhatsApp"
        className={iconBtn}
      >
        <svg className="w-[17px] h-[17px]" fill="currentColor" viewBox="0 0 24 24">
          <path d="M.057 24l1.687-6.163a11.867 11.867 0 01-1.587-5.946C.16 5.335 5.495 0 12.05 0a11.817 11.817 0 018.413 3.488 11.824 11.824 0 013.48 8.414c-.003 6.557-5.338 11.892-11.893 11.892a11.9 11.9 0 01-5.688-1.448L.057 24zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884-.001 2.225.651 3.891 1.746 5.634l-.999 3.648 3.742-.981zm11.387-5.464c-.074-.124-.272-.198-.57-.347-.297-.149-1.758-.868-2.031-.967-.272-.099-.47-.149-.669.149-.198.297-.768.967-.941 1.165-.173.198-.347.223-.644.074-.297-.149-1.255-.462-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.297-.347.446-.521.151-.172.2-.296.3-.495.099-.198.05-.372-.025-.521-.075-.148-.669-1.611-.916-2.206-.242-.579-.487-.501-.669-.51l-.57-.01c-.198 0-.52.074-.792.372s-1.04 1.016-1.04 2.479 1.065 2.876 1.213 3.074c.149.198 2.095 3.2 5.076 4.487.709.306 1.263.489 1.694.626.712.226 1.36.194 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.695.248-1.29.173-1.414z"/>
        </svg>
      </a>

      {/* X / Twitter */}
      <a
        href={`https://twitter.com/intent/tweet?text=${shareText}&url=${shareUrl}`}
        target="_blank"
        rel="noopener noreferrer"
        title="Compartir en X"
        aria-label="Compartir en X"
        className={iconBtn}
      >
        <svg className="w-[15px] h-[15px]" fill="currentColor" viewBox="0 0 24 24">
          <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-4.714-6.231-5.401 6.231H2.747l7.73-8.835L1.254 2.25H8.08l4.262 5.633 5.9-5.633Zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
        </svg>
      </a>

      {/* LinkedIn */}
      <a
        href={`https://www.linkedin.com/sharing/share-offsite/?url=${shareUrl}`}
        target="_blank"
        rel="noopener noreferrer"
        title="Compartir en LinkedIn"
        aria-label="Compartir en LinkedIn"
        className={iconBtn}
      >
        <svg className="w-[15px] h-[15px]" fill="currentColor" viewBox="0 0 24 24">
          <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 0 1-2.063-2.065 2.064 2.064 0 1 1 2.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
        </svg>
      </a>

      {/* Copy link */}
      <button
        onClick={copy}
        title={copied ? '¡Copiado!' : 'Copiar enlace'}
        aria-label={copied ? 'Enlace copiado' : 'Copiar enlace'}
        className={iconBtn}
      >
        {copied
          ? <svg className="w-[15px] h-[15px] text-emerald-500" fill="none" stroke="currentColor" strokeWidth={2.5} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7"/></svg>
          : <svg className="w-[15px] h-[15px]" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"/></svg>
        }
      </button>
    </div>
  )
}
