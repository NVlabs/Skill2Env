# LTX-2.3 Prompting Guide

Use this reference when the user asks for an LTX-2.3 prompt.

Source:

- LTX official post: `https://x.com/ltx_model/status/2029927683539325332`

## Overview

LTX-2.3 improves prompt understanding, motion quality, detail fidelity, audio reliability, and native portrait support. Prompting should be more direct and specific than older LTX checkpoints.
Even with these improvements, motion direction should stay scoped to clip length so the shot remains coherent.

## Duration First (required behavior)

- Default to `10 seconds` as the external duration setting when duration is not specified.
- Ask the user: do you want a shorter or longer clip?
- Scale motion complexity to duration:
  - `<= 6 seconds`: 1 main action beat + 1 simple camera move
  - `10 seconds` (default): 2 to 3 clear action beats + 1 camera move
  - `> 10 seconds`: up to 4 action beats, added in clear sequence
- Do not stack too many simultaneous motions (subject + camera + environment) in short clips.
- Prefer fewer, readable beats over dense micro-actions.
- Never include the duration or the LTX-2.3 model name/version in the final prompt text. Duration is only for planning beat complexity and for external generation settings.

## Core Prompting Principles

### 1) Be specific (detail is now rewarded)

LTX-2.3 can reliably handle:

- Multiple subjects
- Spatial relationships
- Stylistic constraints
- Detailed action steps

Prefer concrete descriptors over short generic prompts.

### 2) Direct the layout like blocking

Explicitly describe spatial relationships:

- Left/right
- Foreground/background
- Facing toward/away
- Relative distance between subjects

Treat scene layout as direction, not just description.

### 3) Describe texture and material

Include fine visual details when relevant:

- Fabric and surface finish
- Hair texture
- Environmental wear
- Edge highlights/backlight detail

### 4) Drive motion with verbs (especially i2v)

For image-to-video and motion-heavy prompts, specify:

- Who moves
- What moves
- How movement happens
- What camera movement occurs

Prefer explicit verbs and clear chronology over abstract phrases like "comes alive."

### 5) Avoid still-photo phrasing

Static prompts often yield static outputs. Include visible action and at least one motion cue (subject or camera).

### 6) Compose portrait natively when vertical

LTX-2.3 supports native portrait generation up to `1080x1920`. For vertical outputs, write framing and composition intentionally for portrait, not as cropped landscape.

### 7) Be explicit about audio

When sound matters, describe:

- Environmental ambience
- Tone and intensity
- Dialogue clarity and placement

Specific audio language improves controllability.

### 8) Use higher complexity deliberately

LTX-2.3 can maintain structure better with layered direction. You can combine:

- Multiple actions in one shot
- Detailed environment + character performance
- Style constraints + camera direction

Complexity works best when instructions are coherent and non-conflicting.
Do not over-pack short clips; fit complexity to duration.

## Mode-Specific Guidance

### Text to Video (T2V)

- Start with scene setup and subject details.
- Add clear spatial structure.
- Describe actions in chronological beats that fit the clip length.
- Add camera movement only when it supports the shot.
- Include audio cues if desired.

### Image to Video (I2V)

- Use the image as the anchor; describe what changes.
- Focus on action verbs and camera verbs.
- Keep motion instructions explicit, sequential, and scoped to clip duration.
- Avoid restating static visual details already fixed by the image unless they need to change. Do not describe the input image in depth; write only the new motion, performance, camera, and audio directions the model should add.

## Recommended Prompt Structure

Write as one coherent clip:

1. Subject + setting (specific details)
2. Spatial layout (where subjects/elements are placed)
3. Material/texture anchors
4. Action progression (start -> middle -> end)
5. Camera movement
6. Audio cues (optional)

## Output Formatting

- Return the final prompt as a single line with no line breaks by default.
- Only use multiline formatting when the user explicitly asks for it.

## Example Rewrites (from the source guidance)

- Weak: `A woman in a cafe`
- Strong: `A woman in her 30s sits by the window of a small Parisian cafe. Rain runs down the glass behind her. Warm tungsten interior lighting. She slowly stirs her coffee while glancing at her phone. Background softly out of focus.`

- Weak: `Two people talking outside`
- Strong: `Two people stand facing each other on a quiet suburban sidewalk. The taller man stands on the left, hands in pockets. The woman stands on the right, holding a bicycle. Houses blurred in the background.`

- Weak: `A dramatic portrait of a man standing`
- Strong: `A man stands on a windy rooftop. His coat flaps in the wind. He adjusts his collar and steps forward as the camera tracks right.`
