# Seedance 2.0 prompting (ByteDance Seed / Volcengine guides)

Use this reference when the user asks for a Seedance 2.0 prompt.

Sources:

- Volcengine prompt guide: `https://www.volcengine.com/docs/82379/2222480`
- Seed blog launch post: `https://seed.bytedance.com/en/blog/official-launch-of-seedance-2-0`
- Volcengine SDK tutorial: `https://www.volcengine.com/docs/82379/2291680`
- Seedance 2.0 model page: `https://seed.bytedance.com/en/seedance2_0`

## What Seedance 2.0 is good at

Seedance 2.0 is a unified multimodal audio-video model. The official launch materials emphasize:

- Text, image, audio, and video inputs in one workflow
- Multimodal reference prompting with composition, motion, camera, visual style, and sound taken from reference assets
- Stronger motion stability and physical plausibility in complex multi-subject scenes
- Up to `15-second` high-quality multi-shot audio-video output
- Stereo / two-channel audio generation with dialogue, ambience, music, and sound effects aligned to picture

The official blog also says users can combine up to:

- `9` images
- `3` video clips
- `3` audio clips
- natural-language instructions

## Clarify the job first

Ask only what is missing:

1. Are they doing fresh generation, reference-driven generation, editing, or video extension?
2. What reference assets do they have: text only, image(s), video clip(s), audio clip(s), storyboard frames, or a shot list?
3. Do they want a single-shot clip or a multi-shot sequence?
4. What clip length should be set in the generation controls? Default to `15 seconds` only if the user does not specify and they want a full Seedance-style showcase shot.
5. What should happen with audio: silent visuals, ambience only, music, dialogue, voiceover, or layered sound design?

## Core prompting approach

Seedance 2.0 responds well to director-style prompts with explicit references and temporal beats.

The official examples also show that literal labels work well. It is fine to write prompts with short sections such as:

- `Setting:`
- `Action:`
- `Camera:`
- `Style:`
- `Audio:`
- `Shot 1:`, `Shot 2:`, `Final shot:`

Write prompts in this order:

1. Output goal: what kind of clip to create
2. Reference mapping: what each `@Image`, `@Video`, or `@Audio` asset contributes
3. Subject and setting anchors
4. Action progression over time
5. Camera plan
6. Lighting / material / style anchors
7. Audio plan

Prefer concrete visible behavior over abstract mood words.

## Reference-driven prompting

When the user has assets, explicitly map each one to a role, following the official examples:

- `@Image 1`: storyboard / shooting script / composition board
- `@Image 2`: character reference
- `@Image 3`: scene or environment reference
- `@Image 4`: props or costume reference
- `@Video 1`: motion rhythm, camera move, or continuity reference
- `@Audio 1`: music, ambience, voice texture, or timing reference

Use language like:

`Refer to the storyboard and shot progression in @Image 1. Use the character from @Image 2, the location from @Image 3, the props from @Image 4, and the motion rhythm from @Video 1. Match the ambience and pacing cues from @Audio 1.`

If the user is doing image-to-video or edit/extend work, treat the references as anchors and describe only what should change, continue, or be emphasized.

## Motion and scene construction

The official materials highlight complex sports, fight choreography, dance, and multi-character interaction. To exploit that:

- Describe motion in chronological beats
- Call out cause and effect when actions interact
- Specify visible physical outcomes: balance shifts, fabric drag, splashing water, ice shavings, mud spray, recoil, impact
- Keep action readable; do not stack too many simultaneous beats into a short clip

Good Seedance prompts often read like a compact shot breakdown rather than a keyword list.

## Camera language

Seedance 2.0 is explicitly marketed around camera control, so use standard film verbs:

- `slow push-in`
- `fast pan`
- `tracking shot`
- `profile shot`
- `orbit`
- `low-angle follow`
- `close-up`
- `top-lit close-up`

For multi-shot prompts, describe the transition between shots so the sequence feels planned:

- `opening with...`
- `the shot transitions to...`
- `the camera pans to reveal...`
- `the ending shot pushes in on...`

## Audio direction

Audio is a first-class part of the model, not an afterthought. When sound matters, specify:

- Dialogue or exact spoken line
- Background ambience
- Music style
- Foley details
- Sync moments where sound should hit the action

Examples of useful audio phrasing:

- `Only the sound of rain is heard at first.`
- `Pure natural trigger sounds, no background music.`
- `Laughter and cheering rise as the family photo comes together.`
- `Voiceover enters only in the final product close-up.`

If the clip should be silent except for one sound family, say that directly.

## Best practices

- Match prompt complexity to clip length; `15 seconds` can handle 2 to 4 clear beats or a short multi-shot sequence.
- Duration is controlled outside the prompt. Use it only to plan beat complexity; do not write the duration into the prompt prose.
- Do not include the Seedance model name/version, duration, aspect ratio, resolution, or generation settings in the final prompt text.
- For single-shot prompts, keep one main camera move and one main action arc.
- For multi-shot prompts, keep the shot order explicit and coherent.
- For multi-shot prompts, explicit labels like `Shot 1`, `Shot 2`, `Cut to close-up`, and `Final shot` are consistent with the official examples.
- Use references intentionally; name what each asset contributes instead of vaguely saying "use these references."
- Describe motion and camera in visible terms, not abstract intensity words.
- If a prompt includes dialogue, keep it brief so it fits the shot timing.
- If using real human portraits or voices as references, note that official materials say authorization or identity verification may be required.

## Mode-specific guidance

### Text-to-video

- Start with subject, setting, and the visual premise.
- Add the action beats in time order.
- Add the camera plan.
- Add audio layers only if they materially improve the shot.

### Image-to-video

- Ask to see the image if the user can share it.
- Use the image as the anchor for identity, wardrobe, scene, and style.
- Focus your text on motion, camera, and audio changes. Do not describe the input image in depth unless the user asks for analysis or a visible detail must change.

### Edit / extend / reference-to-video

- State what should remain consistent.
- State what should be changed or continued.
- If extending a clip, describe how the next action begins from the current end-state.
- If mixing references, assign one job per asset whenever possible.

## Recommended template

Use a single-line prompt by default unless the user asks for multiline formatting:

Single-shot / continuous-shot pattern:

`[Direct opening sentence, e.g. "Single continuous cinematic shot, no music." or "Vertical ASMR video. No music. Macro details."] Setting: ... Action: ... Camera: ... Style: ... Audio: ... Final shot: ...`

Multi-shot pattern:

`[Direct opening sentence or premise.] Shot 1: ... Shot 2: ... Cut to close-up: ... Final shot: ... Style: ... Audio: ...`

If references are involved, introduce them the way the official examples do, in natural language:

- `Based on the reference image, ...`
- `Make the characters from Image 1 and Image 2 ...`
- `Extend the video. ...`

## Planning checklist

Use this as an internal drafting checklist before writing the final prompt:

- Single-shot or multi-shot goal
- Reference mapping, if any
- Subject and setting
- Action beat 1
- Action beat 2
- Action beat 3
- Camera plan
- Lighting / texture anchors
- Style direction
- Audio plan

## Example prompts

See exact official prompts in the reference file below. Treat them as style anchors only; sanitize any copied pattern so the final prompt does not include model names, clip duration, aspect ratio, resolution, or generation settings.

- `references/models/seedance2/example_prompts/seedance2_examples.md`
