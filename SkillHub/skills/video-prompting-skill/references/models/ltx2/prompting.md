# LTX-2 Prompting Guide

Use this reference when the user asks for an LTX2 prompt.

Sources:

- Prompting Guide for LTX-2 at https://ltx.io/model/model-blog/prompting-guide-for-ltx-2.
- Prompt Instructions in https://github.com/Lightricks/ComfyUI-LTXVideo/tree/master/system_prompts

## Overview

LTX-2 responds best to story-driven prompts that flow from start to end. Use clear cinematography language, describe the scene and action sequence, and keep it readable and grounded.
If the user asks for chaotic or fast-twisting motion, warn them about likely artifacts and suggest simpler motion.

## Required Prompt Style

- Write a single flowing paragraph.
- Use present tense verbs.
- Aim for 4 to 8 descriptive sentences.
- Match detail to shot scale (closeups need more specific detail than wide shots).
- Describe motion as a sequence (beginning -> middle -> end).
- Always put style first using the system prompt format: `Style: <style>, <rest of prompt>`. Default to cinematic-realistic when no style is specified.
- Follow the style cue with a scene header like "INT." or "EXT." to anchor the setting.
- For special styles, reinforce with a short style tag at the end (e.g., "pixar style acting and timing" or "sci-fi style cinematic scene").
- Do not include timestamps, scene cuts, or section headings. Start directly with the scene content.
- Do not include the LTX-2 model name/version, clip duration, aspect ratio, resolution, or generation settings in the prompt text.

## Key Aspects to Include

1. Establish the shot: shot type, genre, or cinematography style.
2. Set the scene: lighting, color palette, textures, atmosphere.
3. Describe the action: a clear, natural sequence.
4. Define characters: age, hairstyle, clothing, distinguishing details.
5. Express emotion via physical cues (posture, gesture, facial expression).
6. Camera movement: how the camera moves relative to the subject.
7. Audio and dialogue: ambient sound, music, speech; put spoken lines in quotation marks and mention language/accent if needed.

## Mode-Specific Guidance

### Image to Video (I2V)

- Analyze the input image for subject, setting, elements, style, and mood.
- If the user's request conflicts with the image, describe a plausible transition while preserving visual continuity.
- Describe only what changes from the starting image; avoid re-listing established details to prevent hard cuts. Do not describe the image in depth unless the user asks for analysis or a visible detail must change.
- Use present-progressive action verbs and a chronological flow ("as," "then," "while").
- Integrate audio throughout the scene, aligned to actions (ambient sounds, effects, speech, music when requested).
- Describe only what is seen and heard; avoid smell, taste, or touch.
- Format: DO NOT use phrases like "The scene opens with..." / "The video starts...". Start directly with `Style: <style>,` and chronological scene description.

### Text to Video (T2V)

- Include concrete visual details (lighting, textures, setting).
- Use present-progressive verbs and a chronological flow.
- Integrate audio throughout the scene, aligned to actions; be specific (e.g., "soft footsteps on tile").
- For any speech-related request, include exact quoted dialogue and voice characteristics; specify language/accent if relevant.
- Describe only what is seen and heard; avoid smell, taste, or touch.
- Format: Start directly with `Style: <style>,` and chronological scene description. Avoid "The scene opens with...".

### Lip Sync (Audio to Video)

- Include that the person/character moves its mouth to the words.

## For Best Results

- Keep the prompt cohesive and focused on one primary shot.
- Be specific about camera movement and what is revealed after the move.
- Warn the user when requested motion is likely to produce artifacts (e.g., chaotic or fast-twisting actions like jumping or juggling).

## What Works Well With LTX-2

- Cinematic compositions with thoughtful lighting and natural motion.
- Single-subject emotional moments and subtle gestures.
- Atmosphere and setting details (fog, mist, rain, reflections, ambient textures).
- Clean, readable camera directions (slow dolly in, handheld tracking, over-the-shoulder).
- Stylized aesthetics named early (noir, analog film, painterly, surreal).
- Lighting and mood control (backlighting, soft rim light, color palettes).
- Voice: characters can talk and sing in various languages.

## What to Avoid

- Internal state labels without visual cues ("sad", "confused").
- Readable text or logos; avoid signage or brand names.
- Complex physics or chaotic motion (non-linear, fast-twisting actions like jumping or juggling).
- Too many characters or layered actions.
- Conflicting lighting logic unless clearly motivated.
- Overly complicated prompts; keep it simple and add detail in later iterations.
- Ambiguous acronyms in dialogue. Spell them the way you want them pronounced (e.g., "V-RAM").

## Helpful Terms (Optional)

Use only as needed to support clarity.

- Categories: stop-motion, 2D/3D animation, claymation, hand-drawn, comic book, cyberpunk, pixel art, surreal, minimalist, painterly.
- Visual details: flickering candles, neon glow, natural sunlight, dramatic shadows, rough stone, glossy surfaces, fog, rain, dust.
- Sound and voice: ambient cafe noise, rain and wind, forest ambience, resonant voice, robotic monotone, quiet whisper, mutter, shout.
- Technical style markers: pans, tracks, tilts, pushes in, pulls back, handheld, wide establishing shot, static frame, film grain, motion blur, slow motion, time-lapse.

## Example Prompts

Use the reference examples when drafting or refining prompts: `references/models/ltx2/example_prompts/ltx2_examples.md`.
