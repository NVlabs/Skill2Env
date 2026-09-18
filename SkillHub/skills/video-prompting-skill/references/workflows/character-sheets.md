# Character-sheet prompting for image models

Use this reference when the user wants a reusable character sheet or turnaround to keep a character consistent across multiple generated images and later image-to-video shots.

This workflow is for prompting an image model, not a video model.

## Goal

Produce a sheet that makes the character easy to reuse:

- stable face, build, hair, outfit, and silhouette
- multiple angles on one sheet
- optional expressions, hands, props, and costume details
- minimal ambiguity before generating a first in-scene still

Recommended downstream order:

1. Generate the character sheet
2. Generate a scene still using the sheet as reference
3. Generate image-to-video shots from that scene still

## Clarify the job first

Ask only what is missing:

1. Visual style: photoreal identity sheet, cinematic photoreal, anime, 3D, painterly, comic, etc.
2. Character basics: age range, gender presentation, ethnicity or skin tone if relevant, body type, height impression
3. Hair and face anchors: hairstyle, color, facial structure, eye color, notable features
4. Wardrobe anchors: outfit, shoes, outerwear, accessories, props
5. Sheet scope: turnaround only, turnaround plus expressions, or full production sheet
6. Intended use: general reference, scene-still generation, or direct reference for image-to-video

If the user has an existing image, treat it as the identity anchor and describe the sheet around that anchor instead of reinventing the character.

For photoreal or real-person requests, also pin down whether the user wants:

- a design-oriented character sheet, or
- a photographic identity sheet that should feel like real reference photography

## Core prompting approach

Character-sheet prompts work best when they are explicit about layout and consistency constraints.

Write prompts in this order:

1. State that the output is a character sheet / turnaround / model sheet
2. Define the character identity in concrete visual terms
3. Lock the outfit and silhouette
4. Specify the required views or panels
5. Specify rendering constraints that preserve sameness across panels
6. Specify the background and presentation style

Prefer one character per sheet. If the user needs multiple characters, write a separate sheet prompt for each one.

## Photoreal identity-sheet mode

Use this mode when the user wants a real person, documentary realism, actor continuity, or a sheet based on an uploaded portrait.

Priorities in this mode:

- preserve facial asymmetry rather than averaging the face into a generic beauty render
- preserve age cues, skin texture, and small imperfections
- keep posture natural rather than rigidly symmetrical
- make the result feel like the same person photographed repeatedly, not a redesigned digital asset

Useful phrasing for this mode:

- `real-world photographic identity sheet`
- `the same person photographed across multiple angles`
- `natural human asymmetry preserved`
- `real skin texture and age cues`
- `soft neutral documentary lighting`

Avoid overusing negative constraints. Use them only when needed to suppress common failure modes such as a synthetic 3D or over-stylized look.

## What to include

Default panel set:

- full-body front view
- full-body 3/4 view
- side profile
- back view

Optional panel set:

- expression row
- hand poses
- prop close-ups
- fabric or accessory detail callouts

When including an expression row, ask for clearly different emotions rather than subtle near-duplicates. Mix calm, positive, negative, and high-energy states, and explicitly include some open-mouth expressions when the character design supports it, such as speaking, laughing, barking, shouting, panting, or surprise.

Photoreal identity-sheet layout option:

- top row: full-body front, left profile, right profile, back view
- bottom row: closer portrait views for front, left profile, right profile

Use the contact-sheet style layout when face continuity matters as much as full-body wardrobe continuity.

Useful consistency language:

- `the exact same character in every panel`
- `consistent facial proportions across all views`
- `same hairstyle, same outfit, same colors, same body proportions`
- `clean model sheet presentation`
- `full body visible in each main panel`

## Background and composition

For a true production sheet, default to a simple neutral background:

- white
- light gray
- pale beige studio backdrop

Avoid busy scenery unless the user explicitly wants an in-world presentation board. Background simplicity helps the sheet function as a reusable identity reference.

Use even lighting and avoid dramatic cinematic shadows unless the user wants a stylized sheet.

For photoreal identity sheets, favor a studio-wall or indoor neutral backdrop and soft real-world lighting over polished fashion-editorial styling.

## Pose and camera behavior

By default, keep poses readable and repeatable across panels.

For design sheets:

- calm, readable stance
- enough separation from the body to show clothing silhouette
- avoid foreshortening that hides anatomy

For photoreal identity sheets:

- relaxed posture
- natural weight distribution
- arms resting naturally unless a prop must be shown
- slight variation is acceptable if it still reads like a controlled reference-photo session

Keep camera perspective neutral. Avoid extreme lens effects unless the user explicitly wants a stylized presentation.

## What to avoid

Avoid prompt language that encourages the model to redesign the character between panels:

- changing outfits unless variants are requested
- changing hairstyles across views
- dramatic pose variation that hides anatomy
- cropped figures when the user needs a full reference
- story-heavy backgrounds that compete with the sheet

Avoid vague wording like `various looks` or `multiple versions` unless exploration is the goal. For consistency work, you want one locked design.

In photoreal mode, also avoid:

- airbrushed skin or fashion-retouch perfection
- mannequin-like symmetry
- heroic posing
- dramatic key light, colored rim light, or glossy editorial treatment unless explicitly requested

## Prompt patterns

### Basic turnaround sheet

`Create a clean character turnaround sheet for a single [style] character. The character is [identity description]. They wear [outfit description]. Show the exact same character in full body from front view, 3/4 view, side profile, and back view. Keep facial proportions, hairstyle, outfit, colors, and body proportions completely consistent across every panel. Clean model sheet presentation, evenly lit, neutral plain background, no scene elements, no extra characters, high detail.`

### Turnaround plus expressions

`Create a professional character sheet for a single [style] character. The character is [identity description]. They wear [outfit description]. Include full-body front, 3/4, side, and back views, plus a top row of clearly distinct expression studies showing neutral, joy, skepticism, frustration, and surprise, with at least two expressions using an open mouth where appropriate for the character. The same exact character must appear in every panel with identical facial structure, hairstyle, outfit, palette, and body proportions. Clean layout, neutral background, studio lighting, production design sheet style.`

### Full production sheet with props

`Create a detailed production character sheet for a single [style] character intended for consistent downstream image-to-video reference. The character is [identity description]. Core outfit: [outfit description]. Include full-body front, 3/4, side, and back views, an expression row with clearly varied emotions and at least two open-mouth expressions where appropriate, and small callout panels for [props/accessories]. Keep the exact same character design across all panels with consistent anatomy, face, hair, wardrobe, materials, and color palette. Clean presentation board, minimal neutral background, readable spacing, high detail, no environment scene.`

### Photoreal identity sheet from a reference image

`Create a photoreal photographic identity sheet based strictly on the reference image. Preserve the exact real-world appearance of the same person across every panel, including facial structure, age cues, skin texture, natural asymmetry, body proportions, and any distinctive features. Present the result as a clean contact-sheet style layout with full-body front, left profile, right profile, and back views, plus closer portrait views for front, left profile, and right profile. Neutral background, soft realistic lighting, natural posture, consistent wardrobe, and realistic camera perspective. The result should feel like the same person photographed multiple times in one controlled session.`

### Photoreal identity sheet without a reference image

`Create a photoreal photographic identity sheet of a real human with the following attributes: [identity description]. Keep the subject believable and grounded in real-world photography, with natural skin texture, age cues, realistic proportions, and subtle asymmetry. Present the sheet as a clean contact sheet with full-body front, left profile, right profile, and back views, plus closer portrait views for front, left profile, and right profile. Neutral simple background, soft documentary lighting, natural relaxed stance, no stylized rendering.`

### Wardrobe-only update

`Using the established character sheet or identity sheet as reference, keep the exact same person and preserve face, body proportions, hair, age cues, posture, camera setup, and overall presentation. Change only the wardrobe to [outfit description]. The updated images should feel like the same subject in the same controlled session with a new outfit, without redesigning the character or changing the identity.`

## After the sheet

If the user wants to continue into generation, the next deliverable should usually be a scene-still prompt that references the sheet while adding the environment and framing:

- keep the character identity and wardrobe from the sheet fixed
- add the specific setting, lighting, and shot composition
- avoid introducing new costume or hair changes unless requested

Then write the image-to-video prompt from that scene still, focusing on motion and camera rather than identity redesign.

## Output defaults

Default: output only the final prompt text.

If the user asks for a fuller package, provide:

- the character-sheet prompt
- the first scene-still prompt
- the follow-on image-to-video prompt
