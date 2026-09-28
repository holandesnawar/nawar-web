import { z } from "zod";

// Cómo entra cada clip: "corte" deja el paso de página real del vídeo;
// "deslizar" y "fundido" tapan un paso de página en el que se ve la mano.
export const transitionSchema = z.enum(["corte", "deslizar", "fundido"]);

export const clipSchema = z.object({
  // Archivo dentro de public/clips/. Vacío = tarjeta de muestra.
  src: z.string(),
  // Tramo del clip original, en segundos.
  from: z.number().min(0),
  to: z.number().min(0),
  entry: transitionSchema,
});

// Zona del clip original (en fracciones del cuadro) que se ve en el panel.
// Deja fuera la parte de abajo, que es por donde entra la mano al pasar página.
export const cropSchema = z.object({
  x0: z.number().min(0).max(1),
  y0: z.number().min(0).max(1),
  x1: z.number().min(0).max(1),
  y1: z.number().min(0).max(1),
});

export const guiaBasesSchema = z.object({
  clips: z.array(clipSchema),
  crop: cropSchema,
  // Lo que va entre comillas sale resaltado.
  cta: z.string(),
  transitionSeconds: z.number().min(0.1).max(1.5),
});

export type Clip = z.infer<typeof clipSchema>;
export type Crop = z.infer<typeof cropSchema>;
export type GuiaBasesProps = z.infer<typeof guiaBasesSchema>;
