import {
  AbsoluteFill,
  interpolate,
  OffthreadVideo,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import type { Clip } from "./schema";
import { BRAND, FONT, OFF } from "./theme";

// Un tramo de un clip a pantalla completa, con el zoom anclado arriba para
// que la parte de abajo (donde está la mano) quede fuera del cuadro.
export const SlideClip: React.FC<{
  clip: Clip;
  zoom: number;
  index: number;
}> = ({ clip, zoom, index }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  if (!clip.src) {
    return <Placeholder index={index} />;
  }

  const push = interpolate(frame, [0, durationInFrames], [1, clip.push], {
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={{ backgroundColor: BRAND }}>
      <OffthreadVideo
        src={staticFile(`clips/${clip.src}`)}
        trimBefore={Math.round(clip.from * fps)}
        trimAfter={Math.round(clip.to * fps)}
        muted
        style={{
          width: "100%",
          height: "100%",
          objectFit: "cover",
          transformOrigin: "50% 0%",
          transform: `scale(${zoom * push})`,
        }}
      />
    </AbsoluteFill>
  );
};

const Placeholder: React.FC<{ index: number }> = ({ index }) => (
  <AbsoluteFill
    style={{
      backgroundColor: OFF,
      alignItems: "center",
      justifyContent: "center",
      fontFamily: FONT,
      fontWeight: 800,
      fontSize: 96,
      color: BRAND,
    }}
  >
    Slide {index + 1}
  </AbsoluteFill>
);
