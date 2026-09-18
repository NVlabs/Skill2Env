# Sora prompting (Sora 2 guide)

Use this reference when the user asks for a Sora prompt.

Source: OpenAI Cookbook `Sora 2 Prompting Guide` (`https://cookbook.openai.com/examples/sora/sora2_prompting_guide`).

## First: confirm what must be set outside the prompt (API parameters)

Some attributes are controlled by API parameters, not prose:

- `model`: `sora-2` or `sora-2-pro`
- `size`:
  - `sora-2`: `1280x720`, `720x1280`
  - `sora-2-pro`: `1280x720`, `720x1280`, `1024x1792`, `1792x1024`
- `seconds`: `"10"` or `"15"`

If the user asks for length or resolution, reflect it in recommended parameters in addition to writing the prompt.
Do not include the model name, duration, aspect ratio, resolution, or API parameter names in the prompt text itself. Keep them only in recommended parameters when needed.

## What to clarify (ask only if missing)

1. Input mode: t2v vs i2v (if i2v, confirm they will provide an image)
2. Duration: 10 or 15 seconds
3. Aspect ratio / size: choose an allowed `size` above
4. Style target: documentary / cinematic / anime / commercial / etc.

Tip from the guide: the model follows instructions more reliably in shorter clips; if needed, stitch multiple 10-second clips rather than generating a longer single shot.

## Prompt anatomy that works

Write as if briefing a cinematographer; be specific about what the shot should achieve.

A strong prompt:

- States camera framing and (optionally) depth of field
- Describes action in beats (timed/stepwise)
- Specifies lighting and palette (name 3–5 palette anchors if you need consistency)
- Anchors the subject with a few distinctive details
- Avoids “keyword soup”; uses concrete nouns and verbs that map to visible outcomes

If describing multiple shots in one prompt, keep each shot block distinct: one camera setup, one subject action, and one lighting recipe at a time.

## Motion and timing (beats)

Keep motion simple: one clear camera move and one clear subject action per shot. Use counts/beats for timing.

- Weak: `Actor walks across the room.`
- Strong: `Actor takes four steps to the window, pauses, and pulls the curtain in the final second.`

## Lighting and color consistency

Instead of “brightly lit room”, specify source mix and palette anchors:

- `Lighting + palette: soft window light with warm lamp fill, cool rim from hallway`
- `Palette anchors: amber, cream, walnut brown`

## Image input for more control (i2v)

An image input can lock composition/style (character design, wardrobe, set dressing). Use the image as the first-frame anchor; the text describes what happens next.

If the user is doing i2v, ask them to share the image (optional, but it will help you generate a better prompt). Use it to anchor character identity, wardrobe/props, and scene composition, then write the motion/actions that occur over time.
Do not describe the input image in depth unless the user asks for analysis or a visible detail must change.

### Important: images of real people may require an authorized cameo

Sora i2v workflows may restrict using a photo of a real person unless you use an authorized “cameo”/approved likeness for that person. If the user’s i2v reference is a real-person photo and they don’t have an authorized cameo, warn them that it may be blocked and suggest:

- Use a non-identifying reference image (no recognizable person), or
- Use an authorized cameo/approved likeness, then proceed

When drafting the prompt anyway, phrase it so it works with either a cameo or a generic subject (e.g., “anchored on the provided reference image or the subject’s authorized cameo”).

Guide constraints:

- Image must match the target video `size`
- Formats: `image/jpeg`, `image/png`, `image/webp`

## Dialogue and audio

Dialogue should be written directly and separated from visual prose so it’s unambiguous. Put it in a block below the description.

Example:

```text
[Prose scene description...]

Dialogue:
- Character A: "..."
- Character B: "..."
```

Keep dialogue short so it fits the clip: 10 seconds usually supports 2–3 brief lines; 15 seconds supports a few more; long speeches tend to desync.

If the scene is silent, you can add a minimal background sound note as a rhythm cue (e.g., “distant traffic hiss”).

## Iteration (remix mindset)

Change one thing at a time (“same shot, switch to 85 mm”; “same lighting, new palette: teal, sand, rust”). If a shot misfires, strip it back (freeze camera, simplify action, clear background), then layer complexity.

## Recommended prompt template

```text
[Prose scene description in plain language. Describe characters, costumes, scenery, weather, etc.]

Cinematography:
Camera shot: [framing and angle]
Mood: [overall tone]

Actions:
- [Beat 1]
- [Beat 2]
- [Beat 3]

Dialogue:
- [Optional, short lines]
```
