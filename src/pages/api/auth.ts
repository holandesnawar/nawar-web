// ─────────────────────────────────────────────────
// OAuth handler para Decap CMS (paso 1/2):
// Redirige al usuario a GitHub para que autorice
// ─────────────────────────────────────────────────
import type { APIRoute } from 'astro'

export const prerender = false

export const GET: APIRoute = ({ url, redirect }) => {
  const clientId = import.meta.env.GITHUB_CLIENT_ID || process.env.GITHUB_CLIENT_ID
  if (!clientId) {
    return new Response('Missing GITHUB_CLIENT_ID env var', { status: 500 })
  }

  // Construimos el redirect_uri a partir del host actual
  // Así funciona en producción, previews y localhost sin configuración extra
  const proto = url.hostname === 'localhost' ? 'http' : 'https'
  const redirectUri = `${proto}://${url.host}/api/callback`

  const params = new URLSearchParams({
    client_id: clientId,
    redirect_uri: redirectUri,
    scope: 'repo,user',
  })

  return redirect(`https://github.com/login/oauth/authorize?${params.toString()}`)
}
