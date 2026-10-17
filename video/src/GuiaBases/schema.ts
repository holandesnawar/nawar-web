import { z } from "zod";

// Cómo entra cada tramo: "corte" es un corte seco (lo normal: se salta el
// momento de coger la página); "deslizar" y "fundido" quedan por si acaso.
export const transitionSchema = z.enum(["corte", "deslizar", "fundido"]);

export const clipSchema = z.object({
  // Archivo dentro de public/clips/. Vacío = tarjeta de muestra.
  src: z.string(),
  // Tramo del clip original, en segundos.
  from: z.number().min(0),
  to: z.number().min(0),
  entry: transitionSchema,
  // Zoom anclado arriba (1 = encuadre natural); deja fuera la parte de abajo
  // del cuadro, que es por donde asoma la mano.
  zoom: z.number().min(1),
  // Acercamiento durante el tramo (1 = nada).
  push: z.number().min(1),
  // Segundos que se queda quieto el último fotograma del tramo (0 = nada).
  hold: z.number().min(0),
});

export const guiaBasesSchema = z.object({
  clips: z.array(clipSchema),
  // Línea de abajo; lo que va entre comillas sale resaltado. Vacía = sin línea.
  cta: z.string(),
  transitionSeconds: z.number().min(0.1).max(1.5),
});

export type Clip = z.infer<typeof clipSchema>;
export type GuiaBasesProps = z.infer<typeof guiaBasesSchema>;
