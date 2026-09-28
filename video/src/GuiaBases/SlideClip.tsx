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

// Un tramo de un clip, encuadrado para que no se vean dedos ni bordes.
// Un zoom muy suave le da algo de vida cuando la página está quieta.
export const SlideClip: React.FC<{ clip: Clip; index: number }> = ({
  clip,
  index,
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  const drift = interpolate(frame, [0, durationInFrames], [1, 1.03], {
    extrapolateRight: "clamp",
  });
  const transform = `translate(${clip.x}%, ${clip.y}%) scale(${clip.zoom * drift})`;

  if (!clip.src) {
    return <Placeholder index={index} transform={transform} />;
  }

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
          transform,
        }}
      />
    </AbsoluteFill>
  );
};

const Placeholder: React.FC<{ index: number; transform: string }> = ({
  index,
  transform,
}) => (
  <AbsoluteFill
    style={{
      backgroundColor: BRAND,
      alignItems: "center",
      justifyContent: "center",
    }}
  >
    <div
      style={{
        width: 820,
        height: 1160,
        borderRadius: 24,
        backgroundColor: OFF,
        boxShadow: "0 40px 80px rgba(0,0,0,.35)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        fontFamily: FONT,
        fontWeight: 800,
        fontSize: 96,
        color: BRAND,
        transform,
      }}
    >
      Slide {index + 1}
    </div>
  </AbsoluteFill>
);
