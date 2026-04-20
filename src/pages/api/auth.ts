// ─────────────────────────────────────────────────
// OAuth handler para Decap CMS (paso 1/2):
// Redirige al usuario a GitHub para que autorice
// ─────────────────────────────────────────────────
import type { APIRoute } from 'astro'

export const prerender = false

function resolvePublicHost(request: Request, fallbackHost: string): { proto: string; host: string } {
  // Vercel/proxies inyectan estos headers con el host y protocolo externos
  const xfHost  = request.headers.get('x-forwarded-host')
  const xfProto = request.headers.get('x-forwarded-proto')
  const host    = xfHost || fallbackHost
  const proto   = xfProto || (host.includes('localhost') ? 'http' : 'https')
  return { proto, host }
}

export const GET: APIRoute = ({ url, redirect, request }) => {
  const clientId = import.meta.env.GITHUB_CLIENT_ID || process.env.GITHUB_CLIENT_ID
  if (!clientId) {
    return new Response('Missing GITHUB_CLIENT_ID env var', { status: 500 })
  }

  const { proto, host } = resolvePublicHost(request, url.host)
  const redirectUri = `${proto}://${host}/api/callback`

  const params = new URLSearchParams({
    client_id: clientId,
    redirect_uri: redirectUri,
    scope: 'repo,user',
  })

  return redirect(`https://github.com/login/oauth/authorize?${params.toString()}`)
}
