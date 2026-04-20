// ─────────────────────────────────────────────────────────────
// Migración: Sanity → Markdown (Astro Content Collections)
// Uso: node scripts/migrate-sanity-to-markdown.mjs
// ─────────────────────────────────────────────────────────────
import fs from 'node:fs/promises'
import path from 'node:path'
import https from 'node:https'
import { fileURLToPath } from 'node:url'

const __dirname   = path.dirname(fileURLToPath(import.meta.url))
const ROOT        = path.resolve(__dirname, '..')
const EXPORT_FILE = path.join(__dirname, 'sanity-posts-export.json')
const CONTENT_DIR = path.join(ROOT, 'src/content/blog')
const IMAGES_DIR  = path.join(ROOT, 'public/blog/images')
const PROJECT_ID  = 't0qvkil8'
const DATASET     = 'production'

// ────── utils ──────
async function ensureDir(dir) { await fs.mkdir(dir, { recursive: true }) }

function downloadImage(url, dest) {
  return new Promise((resolve, reject) => {
    const file = require('node:fs').createWriteStream(dest)
    https.get(url, (res) => {
      if (res.statusCode !== 200) return reject(new Error(`HTTP ${res.statusCode} for ${url}`))
      res.pipe(file)
      file.on('finish', () => file.close(resolve))
    }).on('error', reject)
  })
}

// Versión sin require (import dinámico)
async function downloadImageFS(url, dest) {
  const { createWriteStream } = await import('node:fs')
  return new Promise((resolve, reject) => {
    const file = createWriteStream(dest)
    https.get(url, (res) => {
      if (res.statusCode !== 200) {
        res.resume()
        return reject(new Error(`HTTP ${res.statusCode} for ${url}`))
      }
      res.pipe(file)
      file.on('finish', () => file.close(() => resolve(dest)))
      file.on('error', reject)
    }).on('error', reject)
  })
}

// Convierte una ref "image-abc...-1920x1080-jpg" a URL del CDN de Sanity
function refToUrl(ref) {
  if (!ref) return null
  const [, id, dims, ext] = ref.match(/^image-([a-f0-9]+)-(\d+x\d+)-(\w+)$/) || []
  if (!id) return null
  return `https://cdn.sanity.io/images/${PROJECT_ID}/${DATASET}/${id}-${dims}.${ext}`
}

// ────── parser del export ──────
function parseExport(raw) {
  const outer = JSON.parse(raw)
  // outer = [{type: 'text', text: '... <documents>{...}</documents><documents>{...}</documents> <count>6</count>...'}]
  const fullText = outer.map((c) => c.text).join('')
  const docs = []
  const re = /<documents>([\s\S]*?)<\/documents>/g
  let m
  while ((m = re.exec(fullText)) !== null) {
    try {
      docs.push(JSON.parse(m[1]))
    } catch (e) {
      console.error('⚠️  No pude parsear un documento:', e.message)
    }
  }
  return docs
}

// ────── portable-text → markdown ──────
function renderSpans(children = [], markDefs = []) {
  return children
    .map((span) => {
      if (span._type !== 'span') return ''
      let t = span.text || ''
      if (!span.marks || span.marks.length === 0) return t

      // Aplicar marks en orden
      for (const mark of span.marks) {
        if (mark === 'strong') t = `**${t}**`
        else if (mark === 'em') t = `*${t}*`
        else if (mark === 'code') t = `\`${t}\``
        else if (mark === 'underline') t = `<u>${t}</u>`
        else if (mark === 'strike-through') t = `~~${t}~~`
        else {
          // ¿es ref a link?
          const def = markDefs.find((d) => d._key === mark)
          if (def && def._type === 'link' && def.href) t = `[${t}](${def.href})`
        }
      }
      return t
    })
    .join('')
}

function blockToMd(block) {
  if (block._type === 'image') {
    const url = block.asset?.url || refToUrl(block.asset?._ref) || ''
    const alt = block.alt || ''
    return url ? `![${alt}](${url})` : ''
  }
  if (block._type !== 'block') return ''

  const text = renderSpans(block.children, block.markDefs)
  const style = block.style || 'normal'

  // Listas
  if (block.listItem) {
    const indent = '  '.repeat(Math.max(0, (block.level || 1) - 1))
    const marker = block.listItem === 'number' ? '1.' : '-'
    return `${indent}${marker} ${text}`
  }

  // Headings / blockquote
  if (style === 'h1') return `# ${text}`
  if (style === 'h2') return `## ${text}`
  if (style === 'h3') return `### ${text}`
  if (style === 'h4') return `#### ${text}`
  if (style === 'h5') return `##### ${text}`
  if (style === 'h6') return `###### ${text}`
  if (style === 'blockquote') return `> ${text}`

  return text
}

function portableTextToMarkdown(blocks = []) {
  const lines = []
  let prevWasList = false
  for (const block of blocks) {
    const md = blockToMd(block)
    const isList = !!block.listItem

    // Líneas de lista se agrupan sin línea en blanco intermedia
    if (isList && prevWasList) {
      lines.push(md)
    } else if (md) {
      if (lines.length) lines.push('') // separador
      lines.push(md)
    }
    prevWasList = isList
  }
  return lines.join('\n')
}

// ────── frontmatter helpers ──────
function escapeYaml(s = '') {
  // comillas dobles si hay ':' o caracteres especiales
  const needsQuote = /[:#\-@`\[\]\{\}|>*&!%?\n]/.test(s) || /^\s|\s$/.test(s)
  const escaped = s.replace(/"/g, '\\"')
  return needsQuote ? `"${escaped}"` : escaped
}

function estimateReadingMinutes(blocks = []) {
  const text = blocks
    .filter((b) => b._type === 'block')
    .map((b) => (b.children || []).map((c) => c.text || '').join(''))
    .join(' ')
  return Math.max(1, Math.round(text.length / 1000))
}

function buildFrontmatter(post, imagePath) {
  const lines = ['---']
  lines.push(`title: ${escapeYaml(post.title)}`)
  if (post.publishedAt) lines.push(`publishedAt: ${post.publishedAt}`)
  if (post.excerpt) lines.push(`excerpt: ${escapeYaml(post.excerpt)}`)
  if (post.category) lines.push(`category: ${post.category}`)
  if (imagePath) {
    lines.push(`mainImage:`)
    lines.push(`  src: ${imagePath}`)
    if (post.mainImage?.alt) lines.push(`  alt: ${escapeYaml(post.mainImage.alt)}`)
  }
  lines.push(`readingMinutes: ${estimateReadingMinutes(post.body)}`)
  if (post.seo?.title || post.seo?.description) {
    lines.push('seo:')
    if (post.seo.title) lines.push(`  title: ${escapeYaml(post.seo.title)}`)
    if (post.seo.description) lines.push(`  description: ${escapeYaml(post.seo.description)}`)
  }
  lines.push('---')
  lines.push('')
  return lines.join('\n')
}

// ────── main ──────
async function main() {
  console.log('🚀 Migración Sanity → Markdown')

  await ensureDir(CONTENT_DIR)
  await ensureDir(IMAGES_DIR)

  const raw = await fs.readFile(EXPORT_FILE, 'utf8')
  const docs = parseExport(raw)
  console.log(`📦 Encontrados ${docs.length} posts`)

  for (const post of docs) {
    const slug = post.slug
    if (!slug) {
      console.warn(`⚠️  Post sin slug: ${post._id} — saltado`)
      continue
    }
    console.log(`\n📝 ${slug}`)

    // 1. Descargar imagen principal
    let imagePath = null
    const imageUrl = post.mainImage?.asset?.url
    if (imageUrl) {
      const ext = imageUrl.split('.').pop().split('?')[0]
      const imgFile = `${slug}.${ext}`
      const dest = path.join(IMAGES_DIR, imgFile)
      try {
        await downloadImageFS(imageUrl, dest)
        imagePath = `/blog/images/${imgFile}`
        console.log(`   ✓ imagen: ${imagePath}`)
      } catch (e) {
        console.warn(`   ⚠️  imagen no descargada: ${e.message}`)
      }
    }

    // 2. Convertir body
    const bodyMd = portableTextToMarkdown(post.body || [])

    // 3. Generar .md
    const fm = buildFrontmatter(post, imagePath)
    const md = fm + bodyMd + '\n'
    const outFile = path.join(CONTENT_DIR, `${slug}.md`)
    await fs.writeFile(outFile, md, 'utf8')
    console.log(`   ✓ ${outFile.replace(ROOT + '/', '')}`)
  }

  console.log('\n✅ Migración completada')
}

main().catch((e) => {
  console.error('💥 Error:', e)
  process.exit(1)
})
