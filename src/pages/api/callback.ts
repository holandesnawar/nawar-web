// ─────────────────────────────────────────────────
// OAuth handler para Decap CMS (paso 2/2):
// Recibe el ?code= de GitHub, lo intercambia por un
// access_token y se lo envía a Decap vía postMessage
// ─────────────────────────────────────────────────
import type { APIRoute } from 'astro'

export const prerender = false

const CLIENT_ID     = (import.meta.env.GITHUB_CLIENT_ID     || process.env.GITHUB_CLIENT_ID) as string | undefined
const CLIENT_SECRET = (import.meta.env.GITHUB_CLIENT_SECRET || process.env.GITHUB_CLIENT_SECRET) as string | undefined

function renderMessage(status: 'success' | 'error', payload: Record<string, unknown>) {
  const content =
    status === 'success'
      ? `authorization:github:success:${JSON.stringify(payload)}`
      : `authorization:github:error:${JSON.stringify(payload)}`

  return `<!doctype html>
<html>
<head><meta charset="utf-8"><title>Autorizando…</title></head>
<body>
<p>Autorizando con GitHub…</p>
<script>
  (function() {
    function receive(e) {
      if (!window.opener) return;
      window.opener.postMessage(${JSON.stringify(content)}, e.origin || '*');
    }
    window.addEventListener('message', receive, false);
    // Decap inicia el handshake enviando "authorizing:github"
    if (window.opener) {
      window.opener.postMessage('authorizing:github', '*');
    } else {
      document.body.innerText = 'Error: no hay ventana padre (window.opener es null). ¿Lo abriste en una pestaña nueva en vez de popup?';
    }
  })();
</script>
</body>
</html>`
}

export const GET: APIRoute = async ({ url }) => {
  const code = url.searchParams.get('code')

  if (!CLIENT_ID || !CLIENT_SECRET) {
    return new Response(
      renderMessage('error', { message: 'Missing GitHub OAuth env vars on server' }),
      { status: 500, headers: { 'Content-Type': 'text/html; charset=utf-8' } },
    )
  }
  if (!code) {
    return new Response(
      renderMessage('error', { message: 'No code parameter received from GitHub' }),
      { status: 400, headers: { 'Content-Type': 'text/html; charset=utf-8' } },
    )
  }

  try {
    const tokenRes = await fetch('https://github.com/login/oauth/access_token', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'User-Agent': 'nawar-web-decap-oauth',
      },
      body: JSON.stringify({
        client_id: CLIENT_ID,
        client_secret: CLIENT_SECRET,
        code,
      }),
    })

    const data = (await tokenRes.json()) as { access_token?: string; error?: string; error_description?: string }

    if (!data.access_token) {
      return new Response(
        renderMessage('error', { message: data.error_description || data.error || 'No access_token received' }),
        { status: 400, headers: { 'Content-Type': 'text/html; charset=utf-8' } },
      )
    }

    return new Response(
      renderMessage('success', { token: data.access_token, provider: 'github' }),
      { status: 200, headers: { 'Content-Type': 'text/html; charset=utf-8' } },
    )
  } catch (e) {
    return new Response(
      renderMessage('error', { message: (e as Error).message || 'Unknown error exchanging code' }),
      { status: 500, headers: { 'Content-Type': 'text/html; charset=utf-8' } },
    )
  }
}
