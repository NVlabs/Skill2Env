---
name: c-video-edit
description: Programmatic video creation using Remotion (React-based) and Editly (JSON-based declarative). Create, render, and compose videos from code.
tags: [video, editing, remotion, editly, react, rendering, creative]
---

# Video Editing — Remotion & Editly

Create, render, and compose videos programmatically. Use Remotion for React-based dynamic videos or Editly for quick JSON-based assembly.

## Remotion (React-based video creation)

### Project Setup
```bash
# Create a new Remotion project
npx create-video@latest my-video
cd my-video

# Start interactive studio
npx remotion studio
```

### Rendering
```bash
# Render a composition to video
npx remotion render src/index.ts MyComposition out/video.mp4

# Render a still frame (thumbnail)
npx remotion still src/index.ts MyComposition out/thumbnail.png --frame=30

# List available compositions
npx remotion compositions src/index.ts
```

### Render Options
```bash
# Resolution and FPS
npx remotion render src/index.ts MyComp out.mp4 --width 1920 --height 1080 --fps 30

# Codec (h264, h265, vp8, vp9, prores)
npx remotion render src/index.ts MyComp out.mp4 --codec h264

# Quality (CRF 0-51, lower = better)
npx remotion render src/index.ts MyComp out.mp4 --crf 18

# Speed preset
npx remotion render src/index.ts MyComp out.mp4 --x264-preset fast

# Pass data as props
npx remotion render src/index.ts MyComp out.mp4 --props='{"title":"Hello","color":"blue"}'

# Parallel rendering (faster)
npx remotion render src/index.ts MyComp out.mp4 --concurrency 4

# Benchmark render time
npx remotion benchmark src/index.ts MyComp
```

### Composition Structure
```tsx
// src/Root.tsx — register compositions
import { Composition } from "remotion";
import { MyVideo } from "./MyVideo";

export const RemotionRoot = () => (
  <Composition id="MyVideo" component={MyVideo}
    durationInFrames={150} fps={30} width={1920} height={1080} />
);

// src/MyVideo.tsx — video content
import { useCurrentFrame, interpolate, AbsoluteFill, Sequence } from "remotion";

export const MyVideo = () => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 30], [0, 1]);
  return (
    <AbsoluteFill style={{ backgroundColor: "black" }}>
      <Sequence from={0} durationInFrames={60}>
        <h1 style={{ color: "white", opacity }}>Hello World</h1>
      </Sequence>
    </AbsoluteFill>
  );
};
```

## Editly (JSON-based declarative editing)

### Quick Assembly
```bash
# Simple concatenation with titles
editly title:'Intro' clip1.mov clip2.mov title:'THE END' --out output.mp4

# From JSON spec
editly spec.json5 --fast --out output.mp4

# Add background music
editly spec.json5 --audio-file-path music.mp3 --out output.mp4
```

### JSON Spec Format
```json
{
  "width": 1920,
  "height": 1080,
  "fps": 30,
  "outPath": "output.mp4",
  "defaults": {
    "duration": 4,
    "transition": { "name": "fade", "duration": 0.5 }
  },
  "clips": [
    {
      "duration": 3,
      "layers": [{ "type": "title-background", "text": "My Video", "background": { "type": "linear-gradient" } }]
    },
    {
      "layers": [{ "type": "video", "path": "clip1.mp4", "cutFrom": 0, "cutTo": 10 }]
    },
    {
      "layers": [
        { "type": "image", "path": "photo.jpg" },
        { "type": "title", "text": "Caption", "position": "bottom" }
      ]
    }
  ],
  "audioFilePath": "background.mp3",
  "keepSourceAudio": false
}
```

### Layer Types
- `video` — video clip (cutFrom/cutTo for trimming)
- `audio` — audio track
- `image` — static image
- `title-background` — full-screen title card with background
- `title` — text overlay
- `subtitle` — subtitle text
- `gl` — WebGL shader transition/effect

## Guidelines

- **Remotion** — best for complex, data-driven, animated videos (dashboards, branded content, social media)
- **Editly** — best for quick assembly (concatenation, transitions, title cards, slideshows)
- Both require `ffmpeg` (installed automatically with this skill)
- Remotion renders can be CPU-intensive — warn user about duration for long compositions
- Always confirm output path before rendering to avoid overwriting
- Use `--fast` flag with Editly for quick previews before final render
