# Veo 3 / Veo 3.1 prompting (Google Cloud guide)

Use this reference when the user asks for a Veo 3 / Veo 3.1 prompt.

Source: Google Cloud blog `The ultimate prompting guide for Veo 3.1` (`https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1`).

## Core model capability to leverage

Veo 3.1 supports video generation with audio, so you can direct:

- Dialogue (what is said)
- Sound effects (SFX)
- Ambient noise / soundscape

## A prompt formula that works

Use this five-part structure for consistent control:

`[Cinematography] + [Subject] + [Action] + [Context] + [Style & Ambiance]`

- Cinematography: camera work + shot composition
- Subject: main character/focal point
- Action: what the subject does (prefer clear beats)
- Context: environment/background elements
- Style & ambiance: aesthetic + mood + lighting

## Cinematography language (high leverage)

Be explicit about camera and optics using standard terms:

- Camera movement: `dolly shot`, `tracking shot`, `crane shot`, `aerial view`, `slow pan`, `POV shot`
- Composition: `wide shot`, `close-up`, `extreme close-up`, `low angle`, `two-shot`
- Lens & focus: `shallow depth of field`, `wide-angle lens`, `soft focus`, `macro lens`, `deep focus`

## Direct the soundstage (audio)

Use clear, literal audio instructions:

- Dialogue: use quotation marks for exact speech.
  - Example: `A woman says, "We have to leave now."`
- Sound effects: call out effects explicitly.
  - Example: `SFX: thunder cracks in the distance.`
- Ambient noise: define the background soundscape.
  - Example: `Ambient noise: the quiet hum of a starship bridge.`

If you want no dialogue, say so directly and specify only SFX/ambience.

## Negative prompts (exclude by describing the desired absence)

Instead of abstract “no X”, describe the scene including the exclusion:

- Prefer: `a desolate landscape with no buildings or roads`
- Over: `no man-made structures`

## Prompt enhancement workflow (expand a rough prompt)

If the user provides a short idea, expand it by adding:

- Cinematography choices (shot + movement + lens/focus)
- Concrete subject details (wardrobe/props/age range/materials)
- Action beats (2–4 timed steps)
- Lighting and mood anchors
- Audio cues (dialogue/SFX/ambient)

Do not include the Veo model name/version, duration, aspect ratio, resolution, or generation settings in the final prompt text. Keep those as external parameters when needed.

## Advanced workflow: “first and last frame” transition

For controlled transformations/camera moves between two endpoints:

1. Create a starting frame image.
2. Create an ending frame image (different POV or end-state).
3. Prompt Veo to transition from the first frame to the last frame, describing the camera move/transformation and key beats.

## If i2v / “first frame provided”: ask to see the image (optional but helpful)

If the user is doing image-to-video (or providing a starting frame), ask them to share the image (optional, but it will help you generate a better prompt). Use the image to anchor the subject identity, wardrobe/props, and the environment, then describe motion, camera, and the soundstage additions.
Do not describe the input image in depth unless the user asks for analysis or a visible detail must change.
