import type { APIRoute } from 'astro'

export const prerender = false

export const GET: APIRoute = ({ request, redirect }) => {
  const url = new URL(request.url)
  const redirectTo = url.searchParams.get('redirect') ?? '/'
  return redirect(redirectTo, 307)
}
