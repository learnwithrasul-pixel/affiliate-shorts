import React from "react";
import {
  AbsoluteFill,
  Audio,
  Img,
  Sequence,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

// One scene = one image + big headline + optional small line + its voiceover clip.
export type Scene = {
  image: string; // path under public/
  headline: string;
  sub?: string;
  voice?: string; // narration text; scripts/make_voice.py turns it into `audio` + `seconds`
  audio?: string; // path under public/
  seconds: number;
  highlight?: boolean; // price scene: accent box around headline
};

export type ProductShortProps = {
  scenes: Scene[];
  label: string; // "Werbung" / "Anzeige" / "Eigenes Angebot" — shown the whole video
  footer: string; // e.g. "Link in Bio · *Affiliate-Link"
  accent: string;
};

export const FPS = 30;

export const totalFrames = (scenes: Scene[]) =>
  scenes.reduce((sum, s) => sum + Math.round(s.seconds * FPS), 0);

const font = '"Helvetica Neue", Helvetica, Arial, sans-serif';

const SceneView: React.FC<{ scene: Scene; accent: string }> = ({ scene, accent }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const dur = Math.round(scene.seconds * fps);

  const pop = spring({ frame, fps, config: { damping: 14, mass: 0.6 } });
  const zoom = interpolate(frame, [0, dur], [1.0, 1.08]);
  const textIn = spring({ frame: frame - 6, fps, config: { damping: 16 } });
  const fadeOut = interpolate(frame, [dur - 6, dur], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={{ opacity: fadeOut }}>
      {scene.audio ? <Audio src={staticFile(scene.audio)} /> : null}
      <AbsoluteFill
        style={{
          top: 220,
          height: 980,
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        <div
          style={{
            width: 940,
            height: 940,
            borderRadius: 48,
            overflow: "hidden",
            background: "#f2f2f4",
            transform: `scale(${0.85 + 0.15 * pop})`,
            boxShadow: `0 30px 80px rgba(0,0,0,0.5)`,
          }}
        >
          <Img
            src={staticFile(scene.image)}
            style={{
              width: "100%",
              height: "100%",
              objectFit: "cover",
              transform: `scale(${zoom})`,
            }}
          />
        </div>
      </AbsoluteFill>
      <AbsoluteFill
        style={{
          top: 1250,
          paddingLeft: 70,
          paddingRight: 70,
          alignItems: "center",
          textAlign: "center",
          transform: `translateY(${(1 - textIn) * 60}px)`,
          opacity: textIn,
        }}
      >
        <div
          style={{
            fontFamily: font,
            fontWeight: 800,
            fontSize: scene.highlight ? 120 : 78,
            lineHeight: 1.1,
            color: "#fff",
            padding: scene.highlight ? "10px 40px" : 0,
            borderRadius: 24,
            background: scene.highlight ? accent : "transparent",
          }}
        >
          {scene.headline}
        </div>
        {scene.sub ? (
          <div
            style={{
              fontFamily: font,
              fontWeight: 500,
              fontSize: 44,
              marginTop: 28,
              color: "rgba(255,255,255,0.8)",
            }}
          >
            {scene.sub}
          </div>
        ) : null}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

export const ProductShort: React.FC<ProductShortProps> = ({ scenes, label, footer, accent }) => {
  let start = 0;
  return (
    <AbsoluteFill
      style={{ background: "radial-gradient(circle at 50% 35%, #2a2d36 0%, #0d0e12 70%)" }}
    >
      {scenes.map((scene, i) => {
        const from = start;
        const dur = Math.round(scene.seconds * FPS);
        start += dur;
        return (
          <Sequence key={i} from={from} durationInFrames={dur}>
            <SceneView scene={scene} accent={accent} />
          </Sequence>
        );
      })}
      {/* Ad label must stay visible for the whole video (German labelling rules). */}
      <div
        style={{
          position: "absolute",
          top: 90,
          left: 60,
          fontFamily: font,
          fontWeight: 700,
          fontSize: 40,
          color: "#111",
          background: "#fff",
          padding: "8px 22px",
          borderRadius: 12,
        }}
      >
        {label}
      </div>
      <div
        style={{
          position: "absolute",
          bottom: 110,
          width: "100%",
          textAlign: "center",
          fontFamily: font,
          fontWeight: 600,
          fontSize: 38,
          color: "rgba(255,255,255,0.75)",
        }}
      >
        {footer}
      </div>
    </AbsoluteFill>
  );
};
