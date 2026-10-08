/**
 * Los datos de la persona para la API de conversiones de Meta (CAPI): cómo se
 * normalizan y su huella SHA-256. 08/10.
 *
 * Sirve igual en el navegador y en el servidor (los dos tienen
 * `crypto.subtle`; el servidor va con Node 22), así que el mismo correo da la
 * misma huella venga de donde venga.
 *
 * ⚠️ A Meta NUNCA le llegan datos sin cifrar: `metaCapi.ts` solo deja pasar
 * valores con forma de huella (64 caracteres hexadecimales) y tira cualquier
 * otra cosa, aunque alguien la mande a propósito.
 */

/** Correo, teléfono y nombre ya cifrados (SHA-256 en hexadecimal). */
export type UsuarioHash = { em?: string; ph?: string; fn?: string }

export const esHash = (v: unknown): v is string => typeof v === 'string' && /^[a-f0-9]{64}$/.test(v)

/**
 * Como los pide Meta antes de cifrar:
 *  - correo: sin espacios y en minúsculas;
 *  - teléfono: solo cifras, con el prefijo del país y sin ceros delante
 *    (+31 6 12… → 31612…);
 *  - nombre: en minúsculas, sin signos de puntuación.
 * Lo que no tiene pinta de dato de verdad se deja vacío y no se manda.
 */
export function normalizarUsuario(email = '', telefono = '', nombre = '') {
  const em = email.trim().toLowerCase()
  const ph = telefono.replace(/\D/g, '').replace(/^0+/, '')
  const fn = nombre
    .normalize('NFC')
    .toLowerCase()
    .replace(/[\p{P}\p{S}]/gu, '')
    .replace(/\s+/g, ' ')
    .trim()
  return {
    em: /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(em) ? em : '',
    ph: ph.length >= 7 ? ph : '',
    fn,
  }
}

async function sha256(texto: string): Promise<string> {
  const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(texto))
  return Array.from(new Uint8Array(buf), (b) => b.toString(16).padStart(2, '0')).join('')
}

/** Normaliza y cifra. Sin `crypto.subtle` (navegador muy viejo o página sin
 *  https) devuelve vacío: mejor no mandar nada que mandarlo en claro. */
export async function hashUsuario(email = '', telefono = '', nombre = ''): Promise<UsuarioHash> {
  if (typeof crypto === 'undefined' || !crypto.subtle) return {}
  const n = normalizarUsuario(email, telefono, nombre)
  const out: UsuarioHash = {}
  for (const k of ['em', 'ph', 'fn'] as const) {
    if (n[k]) out[k] = await sha256(n[k])
  }
  return out
}
