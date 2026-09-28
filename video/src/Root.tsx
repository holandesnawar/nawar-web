import "./index.css";
import { Composition } from "remotion";
import { HelloWorld } from "./HelloWorld";
import { Logo } from "./HelloWorld/Logo";
import { calculateGuiaBasesMetadata, GuiaBases } from "./GuiaBases/GuiaBases";
import { guiaBasesSchema, type Clip } from "./GuiaBases/schema";
import { FPS, HEIGHT, WIDTH } from "./GuiaBases/theme";

// Montaje de la guía con la toma IMG_6678, todo con el mismo encuadre: un
// zoom suave fijo de 1.15 anclado arriba (deja fuera la mano, que espera en la
// esquina de abajo a la derecha). Cada página quieta y corte seco a la
// siguiente, sin paso de página. Tramos comprobados fotograma a fotograma sin
// mano en cuadro; 05, 06 y la contraportada alargan su último fotograma.
const SRC = "hd/IMG_6678.mp4";
const pagina = (from: number, to: number, hold = 0): Clip => ({
  src: SRC,
  from,
  to,
  entry: "corte",
  zoom: 1.15,
  push: 1,
  hold,
});

const guiaClips: Clip[] = [
  pagina(0.1, 1.25), // portada
  pagina(4.2, 5.6), // 01 Introducción
  pagina(7.9, 9.3), // 02 Artículos
  pagina(12.4, 13.8), // 03 Pronombres
  pagina(16.8, 18.2), // 04 Verbos
  pagina(20.9, 21.7, 0.5), // 05 Vocabulario
  pagina(23.1333, 23.9, 0.5), // 06 Gramática
  pagina(25.2, 25.3333, 1.8), // contraportada
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
