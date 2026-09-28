import { Fragment } from "react";
import { AbsoluteFill, type CalculateMetadataFunction } from "remotion";
import { linearTiming, TransitionSeries } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import { slide } from "@remotion/transitions/slide";
import { Cta } from "./Cta";
import type { Clip, GuiaBasesProps } from "./schema";
import { SlideClip } from "./SlideClip";
import { BRAND, FPS } from "./theme";

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
  cta,
  transitionSeconds,
}) => {
  const timing = linearTiming({
    durationInFrames: Math.round(transitionSeconds * FPS),
  });

  return (
    <AbsoluteFill style={{ backgroundColor: BRAND }}>
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
            <TransitionSeries.Sequence durationInFrames={clipFrames(clip, FPS)}>
              <SlideClip clip={clip} index={i} />
            </TransitionSeries.Sequence>
          </Fragment>
        ))}
      </TransitionSeries>
      <Cta text={cta} />
    </AbsoluteFill>
  );
};
