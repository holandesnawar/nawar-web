/**
 * El teléfono, en formato internacional (+31…), para que el botón de
 * WhatsApp del panel abra el número bueno.
 *
 * Pasó el 29/09: alguien escribió su móvil como se dice en Países Bajos
 * (06 12 34 56 78) y el enlace wa.me/0612345678 no lleva a nadie. WhatsApp
 * necesita el prefijo del país sin el 0 de delante.
 *
 * Solo se completa lo que no tiene duda. Un número de 9 cifras que empieza
 * por 6 puede ser un móvil español o uno holandés sin el 0: ese se deja
 * como está y el closer lo ve.
 */
export function normalizarTelefono(entrada: string): string {
  const texto = (entrada ?? '').toString().trim()
  const d = texto.replace(/\D/g, '')
  if (!d) return texto
  if (texto.startsWith('+')) return `+${d}`
  if (d.startsWith('00')) return `+${d.slice(2)}`
  // Países Bajos: 06 12 34 56 78
  if (/^06\d{8}$/.test(d)) return `+31${d.slice(1)}`
  // Bélgica: 0470 12 34 56
  if (/^04\d{8}$/.test(d)) return `+32${d.slice(1)}`
  // Ya con prefijo, pero sin el +: 31 6…, 32 4…, 34 6/7…
  if (/^316\d{8}$/.test(d) || /^324\d{8}$/.test(d) || /^34[67]\d{8}$/.test(d)) return `+${d}`
  return texto
}
