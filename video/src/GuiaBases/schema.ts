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
  // Zoom anclado arriba (1 = encuadre natural). Los pasos de página van
  // a 1.25 para que la mano que sujeta la hoja quede fuera del cuadro.
  zoom: z.number().min(1),
  // Acercamiento durante el tramo (1 = nada), para el fotograma final alargado.
  push: z.number().min(1),
});

export const guiaBasesSchema = z.object({
  clips: z.array(clipSchema),
  // Lo que va entre comillas sale resaltado.
  cta: z.string(),
  transitionSeconds: z.number().min(0.1).max(1.5),
});

export type Clip = z.infer<typeof clipSchema>;
export type GuiaBasesProps = z.infer<typeof guiaBasesSchema>;
