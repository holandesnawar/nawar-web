/**
 * El teléfono tal cual lo escribe la persona, solo limpio: sin espacios ni
 * guiones, y el 00 de delante pasado a +.
 *
 * NO se adivina el país (29/09, el usuario: "a veces son números de otros
 * países"). Un 06… puede no ser holandés; ponerle +31 a ciegas manda el
 * WhatsApp a otra persona. Por eso el formulario pide el prefijo.
 */
export function normalizarTelefono(entrada: string): string {
  const texto = (entrada ?? '').toString().trim()
  const d = texto.replace(/\D/g, '')
  if (!d) return texto
  if (texto.startsWith('+')) return `+${d}`
  if (d.startsWith('00')) return `+${d.slice(2)}`
  return texto
}
