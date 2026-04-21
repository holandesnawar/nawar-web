import { useState, useEffect } from 'react'

interface Heading { id: string; text: string; level: string }

export default function BlogTOC() {
  const [headings, setHeadings] = useState<Heading[]>([])
  const [activeId, setActiveId]   = useState<string>('')

  useEffect(() => {
    const article = document.querySelector('article.blog-article')
    if (!article) return

    const els = article.querySelectorAll('h2, h3')
    const hs: Heading[] = []
    els.forEach((el, i) => {
      if (!el.id) el.id = `h-${i}`
      hs.push({ id: el.id, text: el.textContent || '', level: el.tagName.toLowerCase() })
    })
    setHeadings(hs)

    const obs = new IntersectionObserver(
      (entries) => {
        const visible = entries.filter(e => e.isIntersecting)
        if (visible.length > 0) setActiveId(visible[0].target.id)
      },
      { rootMargin: '-15% 0% -70% 0%', threshold: 0 }
    )
    els.forEach(el => obs.observe(el))
    return () => obs.disconnect()
  }, [])

  if (headings.length === 0) return null

  return (
    <nav className="sticky top-28 max-h-[calc(100vh-8rem)] overflow-y-auto">
      <p className="text-[10px] font-semibold text-[#9CA3AF] uppercase tracking-[0.14em] mb-4">
        En este artículo
      </p>
      <ul className="space-y-0.5">
        {headings.map(h => (
          <li key={h.id}>
            <a
              href={`#${h.id}`}
              onClick={e => {
                e.preventDefault()
                document.getElementById(h.id)?.scrollIntoView({ behavior: 'smooth', block: 'start' })
              }}
              className={[
                'flex items-start gap-2.5 py-[5px] text-[12.5px] leading-snug transition-all duration-200 group',
                h.level === 'h3' ? 'pl-3.5' : '',
                activeId === h.id
                  ? 'text-[#1D0084] font-semibold'
                  : 'text-[#9CA3AF] hover:text-[#374151]',
              ].join(' ')}
            >
              <span className={[
                'mt-[6px] w-[5px] h-[5px] rounded-full shrink-0 transition-all duration-200',
                activeId === h.id ? 'bg-[#1D0084] scale-[1.4]' : 'bg-[#D1D5DB] group-hover:bg-[#9CA3AF]',
              ].join(' ')} />
              <span>{h.text}</span>
            </a>
          </li>
        ))}
      </ul>
    </nav>
  )
}
