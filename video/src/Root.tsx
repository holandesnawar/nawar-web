import "./index.css";
import { Composition } from "remotion";
import { HelloWorld } from "./HelloWorld";
import { Logo } from "./HelloWorld/Logo";
import { calculateGuiaBasesMetadata, GuiaBases } from "./GuiaBases/GuiaBases";
import { guiaBasesSchema, type Clip } from "./GuiaBases/schema";
import { FPS, HEIGHT, WIDTH } from "./GuiaBases/theme";

// Montaje de la guía con la toma IMG_6675 (IMG_6675_fix.mp4: la misma toma con
// unas rayas de tinta de la tabla de la página 04 limpiadas).
// Cada página: la hoja volando (zoom 1.25, así la mano que la sujeta queda
// fuera) y corte a la página nueva quieta con el encuadre natural. Los cortes
// se saltan el momento de coger la página y la espera. Todos los tramos están
// comprobados fotograma a fotograma sin mano en cuadro. La toma acaba al caer
// la contraportada, así que ese fotograma se alarga (IMG_6675_fin.mp4).
const SRC = "hd/IMG_6675_fix.mp4";
const vuelo = (from: number, to: number): Clip => ({
  src: SRC,
  from,
  to,
  entry: "corte",
  zoom: 1.25,
  push: 1,
});
const pagina = (from: number, to: number): Clip => ({
  src: SRC,
  from,
  to,
  entry: "corte",
  zoom: 1,
  push: 1,
});

const guiaClips: Clip[] = [
  pagina(0.1, 1.4667), // portada
  vuelo(3.4, 3.8667),
  pagina(3.8667, 5.1), // 01 Introducción
  vuelo(8.0333, 8.2667),
  pagina(8.2667, 9.75), // 02 Artículos
  vuelo(11.9667, 12.5333),
  pagina(12.5333, 14.0), // 03 Pronombres
  vuelo(16.0333, 16.6),
  pagina(16.6, 18.3), // 04 Verbos
  vuelo(20.1667, 20.4333),
  pagina(20.4333, 22.1), // 05 Vocabulario
  vuelo(24.2333, 24.4),
  pagina(24.4, 26.1), // 06 Gramática
  vuelo(27.3, 27.9),
  pagina(27.9, 28.1667), // contraportada
  {
    src: "hd/IMG_6675_fin.mp4",
    from: 0,
    to: 2,
    entry: "corte",
    zoom: 1,
    push: 1.04,
  },
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
