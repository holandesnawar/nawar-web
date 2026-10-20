/**
 * El precio de la formación en un pago, con Klarna incluido (20/10/2026:
 * "397 se va fuera, el precio base es 435"). Lo pintan las landings con precio
 * y el píxel de la compra. Un solo sitio para que no vuelvan a separarse.
 *
 * El que se cobra de verdad lo decide la escuela (`precio_base_cents` en
 * learnhouse/apps/api/src/services/payments/payments.py): si cambia allí,
 * cambiarlo aquí. Los plazos propios (3 pagos de 165,67 € o 4 de 135 €) solo
 * los ofrece el equipo por enlace; la web no los enseña.
 */
export const PRECIO_FORMACION = 435
