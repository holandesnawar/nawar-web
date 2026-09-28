import { Fragment } from "react";
import {
  AbsoluteFill,
  interpolate,
  useCurrentFrame,
  useVideoConfig,
  type CalculateMetadataFunction,
} from "remotion";
import { linearTiming, TransitionSeries } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import { slide } from "@remotion/transitions/slide";
import { Cta } from "./Cta";
import type { Clip, GuiaBasesProps } from "./schema";
import { SlideClip } from "./SlideClip";
import {
  BLUE,
  BRAND,
  FPS,
  PANEL_TOP,
  PANEL_WIDTH,
  WIDTH,
  panelHeight,
} from "./theme";

const clipFrames = (clip: Clip, fps: number) =>
  Math.max(1, Math.round((clip.to - clip.from) * fps));

// Las transiciones solapan los dos clips, así que restan de la duración.
export const calculateGuiaBasesMetadata: CalculateMetadataFunction<
  GuiaBasesProps
> = ({ props }) => {
  const transition = Math.round(props.transitionSeconds * FPS);
  const total = props.clips.reduce(
    (sum, clip, i) =>
      sum +
      clipFrames(clip, FPS) -
      (i > 0 && clip.entry !== "corte" ? transition : 0),
    0,
  );
  return { durationInFrames: Math.max(1, total) };
};

export const GuiaBases: React.FC<GuiaBasesProps> = ({
  clips,
  crop,
  cta,
  transitionSeconds,
}) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const timing = linearTiming({
    durationInFrames: Math.round(transitionSeconds * FPS),
  });

  // Acercamiento lento a lo largo de todo el vídeo: da vida a las pausas y,
  // al ser continuo, no salta entre un tramo y el siguiente.
  const zoom = interpolate(frame, [0, durationInFrames], [1, 1.05]);

  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(circle at 50% 38%, ${BLUE} 0%, ${BRAND} 62%)`,
      }}
    >
      <div
        style={{
          position: "absolute",
          top: PANEL_TOP,
          left: (WIDTH - PANEL_WIDTH) / 2,
          width: PANEL_WIDTH,
          height: panelHeight(crop),
          borderRadius: 36,
          overflow: "hidden",
          boxShadow: "0 40px 90px rgba(5,0,40,.55)",
        }}
      >
        <AbsoluteFill style={{ transform: `scale(${zoom})` }}>
          <TransitionSeries>
            {clips.map((clip, i) => (
              <Fragment key={i}>
                {i > 0 && clip.entry !== "corte" ? (
                  <TransitionSeries.Transition
                    timing={timing}
                    presentation={
                      clip.entry === "deslizar"
                        ? slide({ direction: "from-right" })
                        : fade()
                    }
                  />
                ) : null}
                <TransitionSeries.Sequence
                  durationInFrames={clipFrames(clip, FPS)}
                >
                  <SlideClip clip={clip} crop={crop} index={i} />
                </TransitionSeries.Sequence>
              </Fragment>
            ))}
          </TransitionSeries>
        </AbsoluteFill>
      </div>
      <Cta text={cta} />
    </AbsoluteFill>
  );
};
