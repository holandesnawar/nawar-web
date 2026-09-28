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
  // Encuadre: zoom >= 1 y desplazamiento en % para dejar fuera dedos y bordes.
  zoom: z.number().min(1),
  x: z.number(),
  y: z.number(),
  entry: transitionSchema,
});

export const guiaBasesSchema = z.object({
  clips: z.array(clipSchema),
  // Lo que va entre comillas sale resaltado.
  cta: z.string(),
  transitionSeconds: z.number().min(0.1).max(1.5),
});

export type Clip = z.infer<typeof clipSchema>;
export type GuiaBasesProps = z.infer<typeof guiaBasesSchema>;
