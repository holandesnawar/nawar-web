import {
  AbsoluteFill,
  OffthreadVideo,
  staticFile,
  useVideoConfig,
} from "remotion";
import type { Clip, Crop } from "./schema";
import { BRAND, FONT, OFF, PANEL_WIDTH, SRC_HEIGHT, SRC_WIDTH } from "./theme";

// Un tramo de un clip, colocado para que la zona `crop` llene el panel.
export const SlideClip: React.FC<{ clip: Clip; crop: Crop; index: number }> = ({
  clip,
  crop,
  index,
}) => {
  const { fps } = useVideoConfig();

  if (!clip.src) {
    return <Placeholder index={index} />;
  }

  const scale = PANEL_WIDTH / ((crop.x1 - crop.x0) * SRC_WIDTH);

  return (
    <AbsoluteFill style={{ backgroundColor: BRAND }}>
      <OffthreadVideo
        src={staticFile(`clips/${clip.src}`)}
        trimBefore={Math.round(clip.from * fps)}
        trimAfter={Math.round(clip.to * fps)}
        muted
        style={{
          position: "absolute",
          width: SRC_WIDTH * scale,
          height: SRC_HEIGHT * scale,
          left: -crop.x0 * SRC_WIDTH * scale,
          top: -crop.y0 * SRC_HEIGHT * scale,
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
