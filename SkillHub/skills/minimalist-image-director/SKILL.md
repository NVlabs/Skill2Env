# Minimalist Image Director

> Art direction framework for generating warm minimalist photography via AI image generators (Flux, Midjourney, DALL-E). Separates compositional minimalism from emotional minimalism to avoid the "beautiful but sad" trap.

## When to Use This Skill

- Generating hero images, card images, or blog illustrations for a website
- Creating a cohesive visual identity across 10+ AI-generated images
- Briefing AI image generators (Replicate/Flux, Midjourney, DALL-E) with emotional precision
- When previous minimalist attempts came back "too cold" or "too sad"
- Building a visual style guide for a brand's AI-generated photography

## Methodology Foundation

**Sources**:
- Editorial photography principles (Annie Leibovitz, minimal lifestyle photography trend 2024-2026)
- Emotional Design (Don Norman, 2004) — visceral, behavioral, reflective processing
- Color psychology research — warm tones (2700-3000K) activate approach behaviors, cool tones trigger avoidance
- Neuroscience of visual-thermal perception — 80% of experiments show visual environment manipulation affects thermal perception (red-orange = warmth, green-blue = cold)
- Black Forest Labs official prompting guides (Flux 1.1 Pro, Flux 2)
- Kodak Portra 400 color science — the gold standard for warm skin tones in AI photography

**Core Principle**: Minimalism is about what you KEEP, not what you REMOVE. The fewer elements in a frame, the more each one must carry emotional weight. Empty space amplifies — it amplifies warmth just as easily as coldness.

**Why This Matters**: AI image generators default to "aesthetic minimalism" which reads as cold, clinical, lonely. The skill teaches how to direct warmth INTO minimal compositions, getting the clean look without the emotional void.

**The Neuroscience**: Warm colors trigger approach behaviors and lower cognitive vigilance — the viewer feels safe. Cool colors trigger alertness and avoidance. This is not aesthetic preference; it's how photoreceptors and neural pathways process visual information.

---

## What Claude Does vs What You Decide

> "Claude handles the prompt engineering. You bring the emotional truth."

| Claude handles | You provide |
|---------------|-------------|
| Translating emotional intent into Flux/MJ prompt syntax | The emotion each image must convey |
| Applying the 4-layer prompt architecture consistently | Brand palette and visual identity |
| Flagging prompt anti-patterns that produce sad/cold images | Validation — does this FEEL right? |
| Generating batch-consistent style prefixes | Subject matter and context for each image |
| Optimizing aspect ratios and technical parameters | Final selection between generated options |

**Remember**: AI can generate technically perfect minimalist images that feel completely wrong. Your gut reaction to the emotion is the quality gate, not the composition.

---

## What This Skill Does

1. **Emotional Calibration** - Defines the target emotion BEFORE writing any prompt
2. **4-Layer Prompt Architecture** - Style + Subject + Emotion + Anti-patterns in every prompt
3. **Batch Consistency** - Creates a shared style prefix for visual cohesion across sets
4. **Anti-Pattern Detection** - Flags words/directions that trigger cold/sad/clinical outputs
5. **Brand Alignment** - Maps brand voice to visual language (warm brand = warm photos)

## How to Use

### Generate images for website cards
```
I need 3 card images for a child development psychologist website.
Brand palette: cream, coral, warm earth tones.
Cards: Motor Development, Emotional Development, Cognitive Development.
Target emotion: hopeful, warm, possibility.
Generator: Replicate Flux 1.1 Pro, 3:4 aspect ratio.
```

### Create a cohesive blog image set
```
Generate prompts for 13 blog articles about parenting and child psychology.
All images must feel like they're from the same photo shoot.
Brand: warm, approachable, Latin American families.
Avoid: clinical, sad, isolated figures, stock photo poses.
```

### Fix images that came back too cold
```
These minimalist images came back sad/cold. Here's the original prompt: [prompt].
Keep the minimalist composition but make it emotionally warm.
The image should make a parent feel "I want to be that parent" not "that's beautiful but lonely."
```

## Instructions

When generating minimalist image prompts, follow this methodology precisely:

### Step 1: Define the Emotional Target

Before writing ANY prompt, answer:

```
## Emotional Brief

**This image should make the viewer feel:** ________________
**The viewer should want to:** ________________
**This is NOT about:** ________________

**Emotional quadrant:**
        WARM
         |
ACTIVE --+-- CALM
         |
        COLD

Target: [e.g., Warm + Calm = nurturing serenity]
```

**Key principle**: If you can't name the emotion in 2 words, the image will be vague.

**Emotional vocabulary for warm minimalism:**

| Warm + Active | Warm + Calm |
|--------------|-------------|
| Delight, play, discovery | Serenity, connection, trust |
| Courage, determination, pride | Presence, intimacy, safety |
| Freedom, possibility, wonder | Patience, tenderness, focus |

| Cold + Active (AVOID) | Cold + Calm (AVOID) |
|----------------------|---------------------|
| Anxiety, urgency, pressure | Loneliness, melancholy, void |
| Frustration, anger, defeat | Isolation, clinical, sterile |

**Color psychology for emotional targeting:**

| Color range | Emotional effect | Use when... |
|-------------|-----------------|-------------|
| Cream/ivory (#FAF8F5) | Soft, approachable, comfortable base | Every warm minimalist image (background) |
| Terracotta (#C2704F) | Earthy warmth, trustworthiness, permanence | Brands in family, wellness, coaching |
| Warm pink (#FFC0CB) | Nurturing, gentleness, calming | Child development, early childhood |
| Golden/yellow (2700K) | Happiness, energy, sunlight, cozy | Golden hour shots, living room scenes |
| Orange tones | Friendly, fights depression, inviting | Social/community-oriented images |
| Sage/olive (muted green) | Natural, grounded, trustworthy | Earthy brand palettes alongside terracotta |

---

### Step 2: Build the 4-Layer Prompt

Every prompt has exactly 4 layers:

```
## Prompt Architecture

[LAYER 1: STYLE] Technical photography direction
[LAYER 2: SUBJECT] Who/what is in the frame
[LAYER 3: EMOTION] Specific emotional cues
[LAYER 4: ANTI-PATTERNS] What to explicitly exclude
```

**Layer 1 — Style Prefix** (reuse across batch):
```
Warm minimalist photography. Soft natural light, shallow depth of field,
[BRAND PALETTE TONES]. Candid moment, not posed. [DEMOGRAPHIC].
Shot on 85mm f/1.8 lens, Kodak Portra 400 film look, natural skin texture.
No text, no logos, no watermarks. Warm color temperature.
```

**Film stock trick**: Adding "Kodak Portra 400" or "Kodak Portra 800" instantly introduces organic warmth, fine grain, and natural skin tones. This single phrase fights AI's default plastic/clinical rendering better than any other modifier.

**HEX color precision** (Flux 2+): Associate HEX codes with specific objects — `"The wall is #FAF8F5 cream"` works better than `"use #FAF8F5 in the image"`. Always pair HEX with a color name.

Key style levers:
| Lever | Warm direction | Cold direction (avoid) |
|-------|---------------|----------------------|
| Light | Soft natural, golden hour, window light | Studio flash, overhead fluorescent |
| Background | Cream, warm wood, sunlit room | White void, concrete, gray |
| Depth of field | Shallow (f/1.8) — intimacy | Deep (f/11) — documentary |
| Color temp | Warm (2700-3000K golden, 3200-4500K daylight) | Cool (6500K+) |
| Framing | Close, eye-level, inclusive | Wide, above, distant |
| Film stock | Kodak Portra 400, Fujifilm Pro 400H | No film reference (digital default) |
| Texture | "natural skin texture, pores, freckles" | "smooth skin, flawless" (= plastic) |

**Layer 2 — Subject:**
```
A [age] [demographic] child [action verb + specific detail].
[Body language cue]. [One environmental detail].
```

Rules:
- One action verb, one detail (not a paragraph)
- Body language > facial expression for Flux
- One environmental detail grounds the scene (wooden floor, sunlit garden)
- "Mid-action" > "posing" (hands placing a block > holding a block)
- **Always specify demographics** — Flux has training biases and will default if unspecified

**Body language science** — warm vs cold signals:

| Warm signals (USE) | Cold signals (AVOID) |
|-------------------|---------------------|
| Duchenne smile (eyes squeezing + mouth) | Fake smile (mouth only, no eye engagement) |
| Direct eye contact, maintained gaze | Eyes turned to side or downward |
| Open posture, arms uncrossed | Arms crossed over chest (barrier) |
| Relaxed, self-assured stance | Rigid posture, head tilted back |
| Physical proximity or gentle touch | Distance between subjects |
| Leaning in, at eye level | Leaning away, looking from above |

**Layer 3 — Emotion Injection:**
```
[Mood word]. [Light descriptor that reinforces mood].
```

Proven emotion-to-prompt mappings:
| Target emotion | Prompt language |
|---------------|-----------------|
| Joy/delight | "pure delight", "laughing", "arms wide" |
| Connection | "eye contact", "faces close", "at eye level" |
| Curiosity | "deeply focused", "hands mid-action", "slight smile" |
| Safety | "gentle touch", "both at ease", "calm conversation" |
| Pride | "standing tall", "determination", "just accomplished" |
| Possibility | "looking up/ahead", "about to", "the moment before" |

**Layer 4 — Anti-Pattern Blockers:**

Words that trigger cold/sad in AI generators:

| NEVER use | Use instead |
|-----------|-------------|
| `alone`, `solitary`, `quiet room` | `single subject, clean background` |
| `studio lighting`, `white background` | `soft natural light, warm background` |
| `looking at camera`, `posing` | `candid moment`, `mid-action` |
| `dark`, `moody`, `dramatic` | `warm`, `soft`, `gentle` |
| `black and white`, `monochrome` | `warm tones`, `earth tones` |
| `empty`, `vast`, `sparse` | `minimal`, `clean`, `uncluttered` |
| `pensive`, `thoughtful` (alone) | `focused`, `curious`, `engaged` |
| `sitting alone` | `sitting with [object/activity]` |
| `perfect`, `flawless`, `symmetry` | `natural`, `authentic`, `organic` |
| `smooth skin`, `airbrushed` | `natural skin texture`, `pores`, `subtle imperfections` |
| `3D render`, `CGI`, `hyperrealistic` | `photography`, `candid`, `film look` |

**Negative prompt suffix** (append to every prompt for Flux):
```
--no plastic skin, glossy surfaces, artificial lighting, airbrushed,
sterile, clinical, 3D render, CGI, harsh shadows, cool tones
```

---

### Step 3: Validate Before Generating

Before sending to the API, run this checklist:

```
## Pre-Generation Checklist

- [ ] Can I name the target emotion in 2 words?
- [ ] Does the subject have an ACTION (not just a state)?
- [ ] Is there at least one warmth signal (light, touch, smile, color)?
- [ ] Are there zero isolation signals (alone, empty, quiet)?
- [ ] Is the demographic consistent with the brand?
- [ ] Does the style prefix match the batch?
```

---

### Step 4: Evaluate Generated Images

Rate each generated image:

```
## Image Evaluation

**Emotional hit?** [Yes/No] — Does it trigger the target emotion within 2 seconds?
**Warmth level:** [1-5] — 1=clinical, 3=neutral, 5=cozy
**Brand fit:** [Yes/No] — Does it feel like it belongs on the brand's site?
**Minimalism quality:** [Clean/Busy] — Is the composition uncluttered?
**Stock photo test:** [Pass/Fail] — Would you mistake this for generic stock?

If emotional hit = No → rewrite Layer 3 (emotion) first
If warmth < 3 → add warm lighting/color cues to Layer 1
If stock photo test = Fail → make Layer 2 more specific (exact age, exact action)
```

---

### Step 5: Iterate on Failures

Common failure patterns and fixes:

| Problem | Root cause | Fix |
|---------|-----------|-----|
| Image is beautiful but sad | Isolation signals in prompt | Add connection (person+person or person+activity) |
| Image is warm but generic | Subject too vague | Add one hyper-specific detail ("wooden blocks" not "toys") |
| Image feels like stock | "Looking at camera" or "smiling" | Switch to candid mid-action |
| Inconsistent batch style | Style prefix varies | Copy-paste exact same Layer 1 |
| Wrong age/demographic | Generator defaults | Be explicit: "4-year-old", "Latin American" |

## Platform-Specific Guide: Flux 1.1 Pro

> Flux is the primary recommended generator for warm minimalist photography. These rules are Flux-specific.

### Syntax Rules
- **Write like you're talking to a photographer**, not typing keywords into a search engine
- Flux uses natural language — full sentences, NOT comma-separated keyword lists
- **30-80 words is the sweet spot** — under 200 tokens for optimal quality
- **NO prompt weights** — `(text:1.5)` is ignored. Use "with emphasis on X" instead
- **Specify demographics explicitly** — Flux has training biases and will default to Western/white/young if unspecified

### Recommended Structure
```
[Subject + specific details] performing [action] in [environment],
[lighting: direction + quality + time of day],
shot on [camera/lens], [film stock reference],
[composition note], [emotional tone],
natural skin texture, candid moment
--no [anti-patterns]
```

### Camera Filename Trick (Raw Mode)
For hyper-realistic results, prefix the prompt with a camera filename:
- `IMG_2847.HEIC` — iPhone snapshot realism
- `IMG_5847.CR2` — Canon DSLR raw aesthetic
- `DSC03291.ARW` — Sony camera look

**Example**: `IMG_2847.HEIC A mother and child laughing together at a café table, soft window light, slightly grainy, Kodak Portra 400 warmth, authentic moment`

### Raw Mode
Flux Raw Mode adds natural imperfections: skin texture, realistic lighting, natural asymmetry. Best for portraits and lifestyle. Use minimal prompts — let the realism engine do its work.

### Aspect Ratios
- **3:4** — Portrait cards, service pages (recommended for website cards)
- **4:5** — Instagram, vertical lifestyle
- **16:9** — Blog headers, hero images
- **1:1** — Social media, profile images

---

## Examples

### Example 1: Child Development Website Cards

**Context**: 3 service area cards for a child psychologist's website. Brand is warm, approachable, cream/coral palette. Target: parents who want to understand their child's development.

**Input**:
> Generate 3 card images for Desarrollo Motor, Emocional, Cognitivo. Warm minimalist, Flux 1.1 Pro, 3:4 ratio.

**Output**:

**Style prefix (shared):**
```
Warm minimalist photography. Soft natural light, shallow depth of field,
warm cream and beige tones. Candid moment, not posed. Latin American family.
Shot on 85mm f/1.8 lens. No text, no logos, no watermarks.
Warm color temperature, hopeful joyful mood.
```

**Card 1 — Desarrollo Motor** (Emotion: joyful possibility)
```
[STYLE PREFIX] A 4-year-old child mid-jump on warm wooden floor, arms wide
open, barefoot. Pure delight and concentration on face. Soft motion blur on
hands. Single subject, clean warm background. The moment right before
landing — suspended possibility.
```

**Card 2 — Desarrollo Emocional** (Emotion: intimate connection)
```
[STYLE PREFIX] A mother crouching at eye level with her 5-year-old daughter,
faces close, gentle smiles, eye contact. Golden hour light. Intimate
connection between adult and child. Minimal warm background, soft cream tones.
```

**Card 3 — Desarrollo Cognitivo** (Emotion: serene curiosity)
```
[STYLE PREFIX] A 6-year-old child sitting cross-legged on the floor, deeply
focused building a tall wooden block tower. Hands mid-action placing a block.
Calm concentration on face, slight smile. Soft overhead natural light,
earth tones.
```

**Why this works**: Each image has one clear emotion, one specific action, warm lighting, and no isolation signals. The shared style prefix ensures visual cohesion across the set.

---

### Example 2: Fixing a "Beautiful but Sad" Image

**Context**: A minimalist illustration of a woman crouching alone was generated for a "limits without yelling" blog post. The art direction was "minimalist" but the result felt melancholy.

**Input**:
> The line art minimalist image came back too sad. It's a woman crouching alone in black and white. Fix it.

**Analysis of failure:**
- `alone` → isolation signal
- `black and white` → removes warmth
- `crouching` with no context → reads as defeated
- No other person or activity → loneliness

**Fixed prompt:**
```
Warm minimalist photography. Soft natural light, shallow depth of field,
warm cream and beige tones. Candid moment, not posed.
Shot on 85mm f/1.8 lens. No text, no logos, no watermarks.
Warm color temperature.

A mother and 4-year-old child sitting face to face on a couch, mother
holding both of child's hands gently, calm conversation. Both at ease.
Warm living room light filtering through curtains.
```

**What changed:**
- Solo → pair (connection defeats loneliness)
- B&W → warm tones (color = life)
- Crouching → sitting face to face (equals, not defeated)
- Added environmental warmth (couch, living room light)

---

## Skill Boundaries (Frontier Recognition)

### This skill excels for:
- Generating cohesive sets of 3-20+ images with consistent style
- Warm/approachable brands (family, wellness, education, coaching)
- Photorealistic AI generators (Flux, Midjourney v6+, DALL-E 3)

### This skill is NOT ideal for:
- Brands that WANT cold/clinical aesthetics (tech, luxury, medical) → Adjust Layer 1 accordingly
- Abstract/conceptual images (infographics, diagrams) → Use `data-visualizer` skill instead
- Product photography → Requires different prompt architecture
- Illustration styles (watercolor, vector, line art) → Adapt Layer 1 for illustration-specific generators

### Quality Checkpoints

Before accepting the output, verify:
- [ ] 2-second gut check: does the image make you feel the target emotion?
- [ ] Warmth score >= 4 out of 5
- [ ] No accidental isolation signals in the composition
- [ ] Consistent with the rest of the batch (same light, same tones)
- [ ] Would NOT be mistaken for generic stock photography

---

## Iteration Guide

> "The first output is a starting point, not a destination."

### Recommended Iteration Pattern

| Pass | Focus | Questions to Ask |
|------|-------|------------------|
| **1st** | Emotion | "Does this FEEL right within 2 seconds?" |
| **2nd** | Specificity | "Is this too generic? What one detail would make it unique?" |
| **3rd** | Consistency | "Does this match the rest of the set?" |
| **4th** | Brand | "Would the client recognize this as THEIR brand?" |

### Useful Follow-up Prompts

- "The image is warm but feels generic. Add one hyper-specific detail to the subject."
- "The emotion is too [intense/subtle]. Dial it [down/up] by adjusting the body language."
- "The background is too busy. Simplify to [one element] and increase the bokeh."
- "This looks like stock. Make the child's action more specific — what exactly are their hands doing?"

---

## Checklists & Templates

### Batch Brief Template

```
## Image Batch Brief

**Brand:** ________________
**Palette:** ________________
**Demographic:** ________________
**Generator:** Flux 1.1 Pro / Midjourney v6 / DALL-E 3
**Aspect ratio:** ________________
**Number of images:** ________________

### Style Prefix (copy-paste for ALL prompts)
[Write once, use everywhere]

### Per-Image Briefs
| # | Subject | Target emotion (2 words) | Specific action |
|---|---------|--------------------------|-----------------|
| 1 | | | |
| 2 | | | |
| 3 | | | |
```

### Red Flags Checklist

```
## Warning Signs in Your Prompts

- [ ] Any word from the "NEVER use" list (alone, empty, dark, moody, studio)
- [ ] Subject has no action verb (just standing/sitting with no activity)
- [ ] No warmth signal (no mention of light quality, color temperature, or human connection)
- [ ] Demographic not specified (generator will default to its biases)
- [ ] More than 3 adjectives in a row (over-direction = generic output)
- [ ] Prompt longer than 80 words (Flux sweet spot is 30-80 words, degrades past 200 tokens)
```

## References

### Core Methodology
- Norman, Don. "Emotional Design" (2004) - Three levels of design processing (visceral, behavioral, reflective)
- Annie Leibovitz. Masterclass on Portrait Photography - Light as emotion
- Kittl x Savee. "2026 Design Trends Report" - Warm minimalism as dominant trend

### Flux & AI Image Generation
- [Black Forest Labs Prompting Guide](https://docs.bfl.ai/guides/prompting_summary) - Official Flux prompt best practices
- [Flux 2 Prompting Guide (fal.ai)](https://fal.ai/learn/devs/flux-2-prompt-guide) - JSON/HEX color structured prompts
- [Flux Raw Mode Guide (Segmind)](https://blog.segmind.com/flux-1-1-pro-raw-mode-for-creating-natural-realistic-images/) - Natural imperfections
- [Official BFL Skills Repo](https://github.com/black-forest-labs/skills) - Prompting patterns per AgentSkills spec
- [Kodak Portra 400 Midjourney Style (Midlibrary)](https://midlibrary.io/styles/kodak-portra-400) - Film stock reference

### Color Psychology & Neuroscience
- [Color Psychology in Photography (Skylum)](https://skylum.com/blog/color-psychology-for-photographers) - Warm/cold tones and emotional response
- [Visual Environment & Thermal Perception (ScienceDirect)](https://www.sciencedirect.com/science/article/pii/S0306456523000293) - 80% of experiments show visual → thermal link
- [Cold Temperatures in Photos Increase Cognitive Control (ScienceDaily)](https://www.sciencedaily.com/releases/2017/04/170410085010.htm) - Warm → relaxed, cool → alert

### Photography Technique
- [Photographer's Essential Guide to Body Language (SLR Lounge)](https://www.slrlounge.com/photographers-essential-guide-body-language/) - Warm/cold posture cues
- [Photography Composition Definitive Guide (Anton Gorlin)](https://antongorlin.com/blog/photography-composition-definitive-guide/) - Frame-within-frame for intimacy
- [Fixing Plastic AI Skin (Rezience)](https://andyhtu.com/fixing-plastic-ai-skin/) - Negative prompts for realistic texture
- [120+ Stable Diffusion Negative Prompts (ClickUp)](https://clickup.com/blog/stable-diffusion-negative-prompts/) - Anti-pattern word lists

### Warm Minimalism Trend
- [Warm Minimalism Trend 2026 (Good Housekeeping)](https://www.goodhousekeeping.com/home/decorating-ideas/a69926948/new-warm-minimalism-trend/) - "Less but better"
- [Earthy Color Palette Ideas (Rose Benedict Design)](https://rosebenedictdesign.com/2025/01/31/earthy-color-palettes/) - Brand application of earth tones

### Art Direction Methodology
- [How to Write a Photoshoot Brief (Milanote)](https://milanote.com/guide/photoshoot-brief) - Emotional objectives in briefs
- [Creative Briefs for Photographers (VSCO)](https://www.vsco.co/learn/creative-photography-briefs) - SMART emotional criteria

## Related Skills

- [design-trends-2026](../design-trends-2026/) - Current visual trends to align with
- [brand-strategy](../../branding/brand-strategy/) - Brand foundation before visual direction
- [image-batch](../../automation/image-batch/) - Post-processing (resize, compress, WebP)

---

## Skill Metadata

```yaml
name: minimalist-image-director
category: ai-design
subcategory: art-direction
version: 2.0
author: GUIA
source_expert: Editorial Photography + Don Norman (Emotional Design) + Color Psychology + Neuroscience of Visual Perception + Black Forest Labs (Flux)
source_work: null
difficulty: intermediate
mode: centaur
estimated_value: Art director day rate (~500-800 EUR/day)
tags: [image-generation, art-direction, minimalism, flux, replicate, midjourney, brand-photography, emotional-design, color-psychology, warm-minimalism, kodak-portra]
created: 2026-02-12
updated: 2026-02-12
```

---

*This skill is part of the GUIA Premium Marketing Skills Library — the 201 layer that bridges AI basics and technical implementation.*
