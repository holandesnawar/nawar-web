import "./index.css";
import { Composition } from "remotion";
import { HelloWorld } from "./HelloWorld";
import { Logo } from "./HelloWorld/Logo";
import { calculateGuiaBasesMetadata, GuiaBases } from "./GuiaBases/GuiaBases";
import { guiaBasesSchema, type Clip } from "./GuiaBases/schema";
import { FPS, HEIGHT, WIDTH } from "./GuiaBases/theme";

// Montaje de la guía con la toma IMG_6678 (la más limpia y con mejor luz).
// Cada tramo empieza con la página ya en el aire (el corte se salta el momento
// de cogerla), la deja caer y enseña la página nueva un par de segundos.
// Todos los tramos están comprobados fotograma a fotograma sin mano en cuadro
// con el zoom de 1.25. La toma acaba al caer la contraportada, así que ese
// último fotograma se alarga (IMG_6678_fin.mp4) con un acercamiento suave.
const tramo = (from: number, to: number): Clip => ({
  src: "hd/IMG_6678.mp4",
  from,
  to,
  entry: "corte",
  push: 1,
});

const guiaClips: Clip[] = [
  tramo(0.8, 2.0), // portada
  tramo(3.55, 5.55), // 01 Introducción
  tramo(7.37, 9.4), // 02 Artículos
  tramo(11.7, 13.7), // 03 Pronombres
  tramo(15.83, 17.8), // 04 Verbos
  tramo(19.4, 21.2), // 05 Vocabulario
  tramo(22.1, 23.9), // 06 Gramática
  tramo(24.75, 25.3333), // contraportada
  { src: "hd/IMG_6678_fin.mp4", from: 0, to: 2, entry: "corte", push: 1.04 },
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
          // Deja fuera la parte de abajo del cuadro, por donde entra la mano.
          zoom: 1.25,
          cta: 'Responde "BASES" y te la envío',
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
