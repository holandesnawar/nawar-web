import "./index.css";
import { Composition } from "remotion";
import { HelloWorld } from "./HelloWorld";
import { Logo } from "./HelloWorld/Logo";
import { calculateGuiaBasesMetadata, GuiaBases } from "./GuiaBases/GuiaBases";
import { guiaBasesSchema, type Clip } from "./GuiaBases/schema";
import { FPS, HEIGHT, WIDTH } from "./GuiaBases/theme";

// Montaje de la guía: una sola toma (IMG_6678, la más limpia y con mejor luz)
// de la portada a la contraportada, empezando cuando la cámara ya está quieta.
// La toma acaba justo al caer la contraportada, así que ese último fotograma
// se alarga (IMG_6678_fin.mp4). Los clips se pasan a hd/ con ffmpeg (README).
const guiaClips: Clip[] = [
  { src: "hd/IMG_6678.mp4", from: 0.8, to: 25.3333, entry: "corte" },
  { src: "hd/IMG_6678_fin.mp4", from: 0, to: 2.5, entry: "corte" },
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
          crop: { x0: 0.02, y0: 0.12, x1: 0.98, y1: 0.72 },
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
