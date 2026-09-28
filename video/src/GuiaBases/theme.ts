import "@fontsource/poppins/700.css";
import "@fontsource/poppins/800.css";
import type { Crop } from "./schema";

// Mismos colores que la web (src/styles/global.css)
export const BRAND = "#1D0084";
export const BLUE = "#025dc7";
export const ORANGE = "#F58220";
export const OFF = "#F0F5FF";

export const FONT = "Poppins, system-ui, sans-serif";

export const FPS = 30;
export const WIDTH = 1080;
export const HEIGHT = 1920;

// Los clips de public/clips/hd/ están pasados a 1080×1920 (vertical).
export const SRC_WIDTH = 1080;
export const SRC_HEIGHT = 1920;

// Panel donde se ve el vídeo, por debajo de la barra superior de Reels.
export const PANEL_WIDTH = 1000;
export const PANEL_TOP = 200;

export const panelHeight = (crop: Crop) =>
  Math.round(
    (PANEL_WIDTH * (crop.y1 - crop.y0) * SRC_HEIGHT) /
      ((crop.x1 - crop.x0) * SRC_WIDTH),
  );
