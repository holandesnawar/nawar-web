import "./index.css";
import { Composition } from "remotion";
import { HelloWorld } from "./HelloWorld";
import { Logo } from "./HelloWorld/Logo";
import { calculateGuiaBasesMetadata, GuiaBases } from "./GuiaBases/GuiaBases";
import { guiaBasesSchema, type Clip } from "./GuiaBases/schema";
import { FPS, HEIGHT, WIDTH } from "./GuiaBases/theme";

// Mientras no estén los clips, tarjetas de muestra de 2,5 s.
const sampleClips: Clip[] = Array.from({ length: 6 }, (_, i) => ({
  src: "",
  from: 0,
  to: 2.5,
  zoom: 1,
  x: 0,
  y: 0,
  entry: i === 0 ? "corte" : "deslizar",
}));

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
          clips: sampleClips,
          cta: 'Responde "BASES" y te la envío',
          transitionSeconds: 0.4,
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
