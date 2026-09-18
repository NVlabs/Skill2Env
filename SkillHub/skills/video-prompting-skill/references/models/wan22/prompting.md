# Wan 2.2 prompting (Wan AI guide)

Use this reference when the user asks for a Wan 2.2 prompt.

Primary source: `https://www.wan-ai.co/blog/wan-22-whats-new-how-to-write-killer-prompts` (focuses on Wan 2.2).

## Choose the right Wan 2.2 variant (ask if missing)

Wan 2.2 provides multiple model variants:

- Text-to-video (T2V): `Wan2.2-T2V-A14B`
- Image-to-video (I2V): `Wan2.2-I2V-A14B`
- Hybrid (text + image): `Wan2.2-TI2V-5B` (lighter, good for local prototyping)

If the user says “Wan 2.2” but doesn’t specify, ask whether they’re doing:

- T2V, I2V, or TI2V
- And whether they have a starting image (for I2V/TI2V)

Use the chosen variant only to guide drafting. Do not include the Wan model name/version, variant name, duration, aspect ratio, resolution, or generation settings in the final prompt text.

## Prompt writing formulas

### Basic formula

`Subject + Scene + Motion`

- Subject: main object (person/animal/object)
- Scene: environment/background details
- Motion: movement of subjects and non-subjects

### Advanced formula

`Subject (Description) + Scene (Description) + Motion (Description) + Aesthetic Control + Stylization`

- Subject description: detailed appearance (wardrobe/materials/distinctive features)
- Scene description: environment adjectives and anchors
- Motion description: speed, amplitude, effects
- Aesthetic control: lighting, camera, lens, time of day
- Stylization: art direction (e.g., cyberpunk, watercolor)

### Image-to-video (I2V) formula

Because subject/style are anchored by the input image, focus on:

`Motion + Camera movement`

If the user is doing I2V/TI2V, ask them to share the starting image (optional, but it will help you generate a better prompt). Use the image to anchor subject identity and style; avoid re-specifying details that are already clearly present in the image, and focus your text on what changes over time (motion + camera).
Do not describe the input image in depth unless the user asks for analysis or a visible detail must change.

## Shot order (helps coherence)

Use a simple shot progression:

`Opening shot → Camera motion → Pay-off`

Keep it as one coherent clip unless the user asks for multiple shots.

## Camera language

Use explicit camera verbs:

- `pan`, `tilt`, `dolly`, `orbit`, `crane`

And specify movement direction and pace when it matters (e.g., “slow dolly-in”, “pull back”, “orbit 360°”).

## Motion modifiers

Add small, observable motion anchors for stability:

- `slow-motion`, `whip-pan`
- Foreground/background stability cues (e.g., “foreground reeds sway; background mountains remain fixed”)

## Aesthetic tags (cinematic control)

This is the **Aesthetic Control** part of the Wan 2.2 advanced formula:

`Subject (Description) + Scene (Description) + Motion (Description) + Aesthetic Control + Stylization`

Use a compact set of anchors (2–6 total) and keep them consistent across retries/variants to reduce drift.

Common categories:

- Shot size: `wide shot`, `medium shot`, `medium close-up`, `close-up`, `extreme close-up`
- Angle/composition: `eye level`, `low angle`, `high angle`, `over-the-shoulder`, `POV`, `center composition`, `rule of thirds`, `clean single shot`
- Lens/focus/texture: `shallow depth of field`, `deep focus`, `wide-angle lens`, `macro lens`, `soft focus`, `anamorphic bokeh`, `16mm grain`
- Lighting: `volumetric dusk`, `neon rim light`
- Color/tone: `teal-and-orange`, `Kodak Portra`, `warm tone`, `cold tone`, `low saturation`, `high contrast`
- Atmosphere: `overcast`, `rainy`, `fog`, `steam`, `dust motes`
- Emotion beats (optional): `hesitates`, `smiles`, `anxious glance`, `contemplative`

- Lighting: `volumetric dusk`, `neon rim light`
- Color: `teal-and-orange`, `Kodak Portra`
- Lens/texture: `anamorphic bokeh`, `16mm grain`

Prefer a few strong anchors over long adjective lists.

## Negative prompts

Use a short negative list to reduce common artifacts:

`bright colors, overexposed, static, blurred details, low quality, extra fingers, malformed limbs, cluttered background`

Keep negatives focused on failure modes you actually see.

## Examples (style anchors)

### Cyberpunk tracking shot

`A rainy night in a dense cyberpunk market, neon signs flicker overhead. Camera tracks behind a hooded courier weaving through crowds. Volumetric pink-blue backlight cuts through steam vents, puddles reflect the glow.`

### Pull-back reveal

`Extreme close-up of a mountaineer’s ice axe biting into frozen rock. Camera pulls back to reveal the climber and a vast sunrise-lit alpine ridge.`

### Slow-motion orbit

`An orca breaches in crystal-clear Arctic waters. Slow 360° orbital shot around the whale, droplets hang suspended. Pastel polar sunset lighting.`
