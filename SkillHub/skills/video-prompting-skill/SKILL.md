---
name: video-prompting
description: Draft and refine prompts for video generation models (text-to-video and image-to-video), and create character-sheet prompts for image models when the goal is character consistency before image-to-video. Use when a user asks for a "video prompt", a model-specific prompt such as Seedance 2.0, Ovi, Sora, Veo 3, Wan 2.2, LTX-2, or LTX-2.3, or a consistent-character prompt such as "character sheet prompt", "character turnaround", "character reference sheet", or "photographic identity sheet".
---

# Video Prompting

## Overview

Turn a user’s intent into either:

- a strong, model-compliant video prompt, or
- a strong image-model prompt for a character sheet that will later support image-to-video consistency.

Model-specific video guidance lives in `references/models/`. Character-sheet guidance lives in `references/workflows/character-sheets.md`.
This file is the entry point: route to the right path, ask the minimum clarifying questions, then draft the prompt in the expected format.

## Model Index

- Ovi: `references/models/ovi/prompting.md`
- Sora (Sora 2): `references/models/sora/prompting.md`
- Veo 3 / 3.1: `references/models/veo3/prompting.md`
- Wan 2.2: `references/models/wan22/prompting.md`
- Seedance 2.0: `references/models/seedance2/prompting.md`
- LTX-2: `references/models/ltx2/prompting.md`
- LTX-2.3: `references/models/ltx2-3/prompting.md`

## Workflow Index

- Character sheets for consistent characters: `references/workflows/character-sheets.md`

To add a new model later: create `references/models/<model>/prompting.md`, then add it to this index.

To add a new workflow later: create `references/workflows/<workflow>.md`, then add it to the Workflow Index.

## Global video-prompt rules

These rules apply to every video model reference:

- Never include the model name, model version, duration, aspect ratio, resolution, or API/control parameter names in the final prompt text. Those are selected outside the prompt.
- Use duration only as internal planning context for how many action beats the prompt can support.
- If the user asks for parameters or the model requires them, provide them outside the prompt in a separate recommended-parameters line.
- For image-to-video, treat the image as the visual anchor. Do not describe the image in depth unless the user asks for an image analysis or a detail must change. Focus the prompt on motion, camera, emotion/performance, and audio.

## Workflow

### Step 1 — Route the request

Decide whether the user wants:

- a video-generation prompt, or
- a character-sheet prompt for an image model

Route to the character-sheet workflow when the user wants a reusable reference sheet, turnaround, expression sheet, costume sheet, photographic identity sheet, or a consistent-character starting point for a longer image-to-video project.

If the user is asking for both, do them in this order:

1. Character sheet
2. Scene still / anchor frame
3. Video prompt

### Step 2 — If it is a video prompt, identify the model and input mode

If the user did not name a model, ask which model they are using (or offer supported options from the Model Index).

Then confirm the input mode:

- Text-to-video (t2v), or
- Image-to-video (i2v)

If i2v: ask the user to share the image (optional, but it will help you generate a better prompt). Use the image as an anchor according to the chosen model’s guidance (e.g., keep identity/wardrobe/composition stable; focus your text on motion/camera/what changes).

If the chosen model has versions, duration constraints, or required parameters, ask the minimum questions needed to select the right format (see the model guide).
For LTX-2.3 specifically: default to 10 seconds as the external duration setting when duration is missing, ask if the user wants shorter or longer, and scale motion complexity to match that duration. Do not write the duration into the prompt itself.

### Step 3 — Load the correct reference and follow its format

For video prompts: open the model’s `prompting.md` from the Model Index and follow its rules strictly.

For character sheets: open `references/workflows/character-sheets.md` and follow its structure strictly. Treat this as an image-model prompt, not a video-model prompt.

### Step 4 — Draft the prompt in the right form

Draft the prompt using the structure and constraints from the markdown file you selected in Step 3.

For video prompts: follow the chosen model’s `prompting.md` exactly, including its preferred section order, dialogue/audio format, and any shot-structure guidance.
Before returning a video prompt, remove any prompt-internal references to model name/version, clip length, aspect ratio, resolution, or generation settings.

For character sheets: follow `references/workflows/character-sheets.md` exactly, including layout, consistency constraints, and expression-row guidance.

### Step 5 — Output

Default: output only the final prompt text.
Default formatting: output prompts as a single line with no line breaks unless the user explicitly requests multiline formatting.

If the user asks for options: provide 2–3 distinct prompt variants, each fully self-contained and compliant with the model’s formatting.

If the model uses required API parameters (e.g., duration/size), include a short “Recommended parameters” line only when the user has specified them or explicitly asks for them.

If the user wants the full consistency workflow, after the character-sheet prompt also provide:

- one prompt for a first scene still that uses the character sheet as reference, and
- one prompt for the follow-on image-to-video shot
