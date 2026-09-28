import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { BRAND, FONT, ORANGE } from "./theme";

// Línea fija abajo, por encima de la zona que tapan el texto y los botones
// de Reels/TikTok. Lo que va entre comillas sale en una etiqueta naranja.
export const Cta: React.FC<{ text: string }> = ({ text }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const enter = spring({ frame: frame - 6, fps, config: { damping: 14 } });
  const pulse = 1 + 0.04 * Math.max(0, Math.sin((frame / fps) * Math.PI * 1.2));

  const parts = text.split(/["«»“”]/);

  return (
    <AbsoluteFill
      style={{
        justifyContent: "flex-end",
        alignItems: "center",
        paddingBottom: 400,
      }}
    >
      <div
        style={{
          opacity: enter,
          transform: `translateY(${interpolate(enter, [0, 1], [60, 0])}px)`,
          maxWidth: 940,
          padding: "22px 36px",
          borderRadius: 999,
          backgroundColor: "white",
          boxShadow: "0 18px 50px rgba(12,12,30,.35)",
          fontFamily: FONT,
          fontWeight: 700,
          fontSize: 44,
          lineHeight: 1.2,
          color: BRAND,
          textAlign: "center",
          whiteSpace: "nowrap",
        }}
      >
        {parts.map((part, i) =>
          i % 2 === 1 ? (
            <span
              key={i}
              style={{
                display: "inline-block",
                margin: "0 12px",
                padding: "4px 16px",
                borderRadius: 16,
                backgroundColor: ORANGE,
                color: "white",
                fontWeight: 800,
                letterSpacing: "0.04em",
                transform: `scale(${pulse})`,
              }}
            >
              {part}
            </span>
          ) : (
            <span key={i}>{part.trim()}</span>
          ),
        )}
      </div>
    </AbsoluteFill>
  );
};
