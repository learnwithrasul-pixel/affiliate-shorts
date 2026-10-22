import React from "react";
import { Composition, registerRoot } from "remotion";
import { FPS, ProductShort, ProductShortProps, totalFrames } from "./ProductShort";

// Render: npx remotion render src/index.tsx ProductShort out/demo.mp4 --props=public/projects/demo/video.json
const defaults: ProductShortProps = {
  scenes: [{ image: "projects/demo/product.png", headline: "Produkt", seconds: 3 }],
  label: "Werbung",
  footer: "Link in Bio",
  accent: "#E8382F",
};

const Root: React.FC = () => (
  <Composition
    id="ProductShort"
    component={ProductShort}
    fps={FPS}
    width={1080}
    height={1920}
    durationInFrames={totalFrames(defaults.scenes)}
    defaultProps={defaults}
    calculateMetadata={({ props }) => ({ durationInFrames: totalFrames(props.scenes) })}
  />
);

registerRoot(Root);
