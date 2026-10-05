import "./index.css";
import { Composition } from "remotion";
import { HelloWorld } from "./HelloWorld";
import { Logo } from "./HelloWorld/Logo";
import { calculateGuiaBasesMetadata, GuiaBases } from "./GuiaBases/GuiaBases";
import { guiaBasesSchema, type Clip } from "./GuiaBases/schema";
import { FPS, HEIGHT, WIDTH } from "./GuiaBases/theme";

// Montaje de la guía con la toma IMG_6678, sin zoom. En cada paso de página se
// corta la parte en la que la mano llega y coge la hoja: el tramo empieza con
// la hoja ya en el aire, cae y se ve la página nueva. También se cortan los
// ratos en que la mano ronda por abajo después. Donde la página limpia dura
// poco, su último fotograma se queda quieto un momento (`hold`).
const SRC = "hd/IMG_6678.mp4";
const tramo = (from: number, to: number, hold = 0): Clip => ({
  src: SRC,
  from,
  to,
  entry: "corte",
  zoom: 1,
  push: 1,
  hold,
});

const guiaClips: Clip[] = [
  tramo(0, 1.1), // portada
  tramo(3.7333, 4.6333, 0.5), // hoja al aire → 01 Introducción
  tramo(7.4333, 8.7), // hoja al aire → 02 Artículos
  tramo(11.8667, 12.1), // hoja al aire → 03
  tramo(14.1, 14.3333, 0.8), // 03 Pronombres
  tramo(15.9333, 16.6), // hoja al aire → 04
  tramo(16.9667, 17.6667), // 04 Verbos
  tramo(19.5667, 19.9333), // hoja al aire → 05
  tramo(20.8, 21.0, 0.6), // 05 Vocabulario (solo asoma la sombra de la mano)
  tramo(22.2667, 22.5), // hoja al aire → 06
  tramo(23.1667, 23.8667), // 06 Gramática
  tramo(24.9333, 25.3333, 1.8), // hoja al aire → contraportada
];

// Each <Composition> is an entry in the sidebar!

export const RemotionRoot: React.FC = () => {
  return (
    <>
      {/* Reel 9:16 de la guía gratuita. Los clips van en public/clips/. */}
      <Composition
        id="GuiaBases"
        component={GuiaBases}
        schema={guiaBasesSchema}
        calculateMetadata={calculateGuiaBasesMetadata}
        durationInFrames={1}
        fps={FPS}
        width={WIDTH}
        height={HEIGHT}
        defaultProps={{
          clips: guiaClips,
          cta: "",
          transitionSeconds: 0.3,
        }}
      />

      <Composition
        // You can take the "id" to render a video:
        // npx remotion render HelloWorld
        id="HelloWorld"
        component={HelloWorld}
        durationInFrames={150}
        fps={30}
        width={1920}
        height={1080}
        // You can override these props for each render:
        // https://www.remotion.dev/docs/parametrized-rendering
        defaultProps={{
          titleText: "Welcome to Remotion",
          titleColor: "#000000",
          logoColor1: "#91EAE4",
          logoColor2: "#86A8E7",
        }}
      />

      {/* Mount any React component to make it show up in the sidebar and work on it individually! */}
      <Composition
        id="OnlyLogo"
        component={Logo}
        durationInFrames={150}
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{
          logoColor1: "#91dAE2",
          logoColor2: "#86A8E7",
        }}
      />
    </>
  );
};
