import type { APIRoute } from 'astro'
import nodemailer from 'nodemailer'

export const prerender = false

export const POST: APIRoute = async ({ request }) => {
  try {
    const body = await request.json().catch(() => null)
    const nombre  = body?.nombre?.trim()  ?? ''
    const email   = body?.email?.trim()   ?? ''
    const asunto  = body?.asunto?.trim()  ?? '(sin asunto)'
    const mensaje = body?.mensaje?.trim() ?? '(sin mensaje)'

    if (!email || !email.includes('@')) {
      return json({ error: 'Email inválido' }, 400)
    }

    const gmailPass = import.meta.env.GMAIL_APP_PASSWORD

    if (!gmailPass) {
      console.error('[contact] GMAIL_APP_PASSWORD no configurada')
      // Devolver éxito — no mostrar error al usuario
      return json({ success: true })
    }

    try {
      const transporter = nodemailer.createTransport({
        service: 'gmail',
        auth: {
          user: 'holandesnawar@gmail.com',
          pass: gmailPass,
        },
      })

      await transporter.sendMail({
        from:    '"Nawar Academia" <holandesnawar@gmail.com>',
        to:      'info@holandesnawar.com',
        replyTo: email,
        subject: `Nueva consulta: ${asunto}`,
        html: `
          <div style="font-family:sans-serif;max-width:600px;margin:0 auto;padding:32px;">
            <h2 style="color:#1D0084;margin-bottom:4px;">Nueva consulta desde holandesnawar.com</h2>
            <hr style="border:none;border-top:1px solid #e5e7eb;margin:16px 0;">

            <table style="width:100%;border-collapse:collapse;">
              <tr>
                <td style="padding:10px 0;color:#6b7280;font-size:13px;width:100px;">Nombre</td>
                <td style="padding:10px 0;color:#111827;font-size:15px;font-weight:600;">${escapeHtml(nombre) || '—'}</td>
              </tr>
              <tr style="background:#f9fafb;">
                <td style="padding:10px 8px;color:#6b7280;font-size:13px;">Email</td>
                <td style="padding:10px 8px;">
                  <a href="mailto:${escapeHtml(email)}" style="color:#1D0084;font-size:15px;">${escapeHtml(email)}</a>
                </td>
              </tr>
              <tr>
                <td style="padding:10px 0;color:#6b7280;font-size:13px;">Asunto</td>
                <td style="padding:10px 0;color:#111827;font-size:15px;">${escapeHtml(asunto)}</td>
              </tr>
            </table>

            <div style="margin-top:20px;">
              <p style="color:#6b7280;font-size:13px;margin-bottom:8px;">Mensaje</p>
              <div style="background:#f3f4f6;border-radius:12px;padding:20px;font-size:15px;color:#111827;line-height:1.65;white-space:pre-wrap;">${escapeHtml(mensaje)}</div>
            </div>

            <div style="margin-top:28px;padding-top:20px;border-top:1px solid #e5e7eb;">
              <a href="mailto:${escapeHtml(email)}?subject=Re: ${encodeURIComponent(asunto)}"
                 style="display:inline-block;background:#1D0084;color:#fff;padding:12px 24px;border-radius:8px;text-decoration:none;font-weight:600;font-size:14px;">
                Responder a ${escapeHtml(nombre || email)}
              </a>
            </div>
          </div>
        `,
      })

      console.log('[contact] email sent from:', email)

    } catch (emailErr) {
      // Loguear el error internamente pero no bloquearlo al usuario
      console.error('[contact] email send failed:', emailErr)
    }

    // Siempre éxito — el usuario nunca debe ver errores del servicio de email
    return json({ success: true })

  } catch (e) {
    console.error('[contact] exception:', e)
    return json({ success: true })
  }
}

function json(data: object, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json' },
  })
}

function escapeHtml(str: string) {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
}
