# Web Design Director

> Visual design direction framework organized by emotional intent (Warm/Cold x Active/Calm). The first design reference system that categorizes sites by what they make you FEEL, not how they look. Includes 48 annotated public website references.

## When to Use This Skill

- Starting a new website project and deciding the visual direction before coding
- A client says "I want it to feel professional but warm" and you need to translate that into concrete design decisions
- You have a brand positioning (Dunford, StoryBrand) and need to map it to visual language
- Choosing between design approaches (dark mode vs light, minimal vs rich, editorial vs product)
- Building a mood board from references that match the brand's emotional territory
- When AI-generated designs come back looking "template-y" because they lack intentional direction

## Methodology Foundation

**Sources**:
- Emotional Design (Don Norman, 2004) — visceral, behavioral, reflective processing
- Brand positioning theory (April Dunford, "Obviously Awesome") — competitive alternatives define visual territory
- Color psychology research — warm/cool spectrum and behavioral response
- Web design pattern analysis — 48 public sites analyzed across 4 emotional quadrants
- Gap analysis of 12 design inspiration platforms (Awwwards, Dribbble, Godly, Mobbin, etc.)

**Core Insight**: Every existing design inspiration platform (Awwwards, Dribbble, Behance, Godly, Mobbin, SiteInspire, Lapa.ninja) categorizes by visual style, industry, platform, or color. ZERO platforms organize by emotional intent. This is the gap. A "minimal dark site" can feel luxurious (Cartier) or threatening (CrowdStrike) — the visual style is the same, the emotional effect is opposite. Style without intent is decoration. Intent without style is a wireframe.

**The Emotional Quadrant**:
```
              WARM
         (approach, trust)
               |
    Warm+Active | Warm+Calm
    (energy,    | (comfort,
     delight)   |  safety)
               |
ACTIVE --------+-------- CALM
(momentum,     |    (restraint,
 disruption)   |     authority)
               |
    Cold+Active | Cold+Calm
    (innovation,| (luxury,
     power)     |  exclusivity)
               |
              COLD
         (distance, precision)
```

**Why This Matters**: Brand positioning determines which quadrant you design in. A child psychologist belongs in Warm+Calm. A developer tool belongs in Cold+Active. Designing a child psychologist's site with Vercel's aesthetic is a positioning mismatch — no matter how "clean" it looks.

---

## What Claude Does vs What You Decide

> "Claude selects the references and patterns. You validate the emotional fit."

| Claude handles | You provide |
|---------------|-------------|
| Mapping brand positioning to emotional quadrant | Brand values, target audience, competitive alternatives |
| Selecting relevant references from the library | Gut-check: does this reference FEEL like my brand? |
| Extracting design patterns (typography, spacing, color, motion) | Budget and technical constraints |
| Generating a design direction document with rationale | Final approval on direction before coding begins |
| Flagging positioning mismatches (warm brand + cold design) | Client context Claude can't see |

**Remember**: The reference library is a starting point for conversation, not a prescription. The best design direction often comes from combining elements across quadrants — a Warm+Calm palette with Cold+Active typography, for example.

---

## What This Skill Does

1. **Emotional Positioning** — Maps brand positioning to the correct emotional quadrant
2. **Reference Selection** — Surfaces 3-5 annotated public websites that match the target feeling
3. **Pattern Extraction** — Identifies the specific design mechanics that create each emotional effect
4. **Direction Document** — Generates a design brief with palette, typography, spacing, motion, and layout decisions
5. **Mismatch Detection** — Flags when design choices contradict brand positioning
6. **Cross-Quadrant Blending** — Guides intentional mixing of elements from different quadrants

## How to Use

### Get design direction for a new website
```
I'm designing a website for [brand/business type].
Target audience: [who].
Brand feeling: [2-3 emotional words].
Competitive alternatives: [what they'd use instead of this brand].
Load the web-design-director skill.
```

### Find references for a specific feeling
```
I need website references that feel [emotional description].
Not [what to avoid]. The brand is in [industry].
Show me 5 annotated references from the library.
```

### Audit an existing design against brand positioning
```
Here's our current site: [URL or screenshot].
Our brand positioning is: [positioning statement].
Does the design match the emotional intent? What's misaligned?
```

---

## Instructions

### Step 1: Determine the Emotional Quadrant

Ask these questions to place the brand:

```
## Brand Emotional Mapping

**1. What should a visitor feel in the first 3 seconds?**
   [ ] Safe, welcomed, at ease (→ Warm)
   [ ] Impressed, curious, intrigued (→ Cold)

**2. What should the site's energy level be?**
   [ ] Dynamic, forward-moving, "things are happening" (→ Active)
   [ ] Restrained, spacious, "take your time" (→ Calm)

**3. What's the brand's relationship with the visitor?**
   [ ] Peer/friend/guide (→ Warm)
   [ ] Expert/authority/institution (→ Cold)

**4. Competitive alternatives — what would people use instead?**
   (This determines your visual territory — you must look DIFFERENT from alternatives)
```

**Quadrant determination**:

| Combination | Quadrant | Signature feeling |
|-------------|----------|-------------------|
| Warm + Active | **Energetic Warmth** | "This is exciting AND friendly" |
| Warm + Calm | **Nurturing Comfort** | "I feel safe and understood here" |
| Cold + Active | **Innovative Power** | "This is cutting-edge and serious" |
| Cold + Calm | **Refined Authority** | "This is elevated and exclusive" |

---

### Step 2: Select References from the Library

Choose 3-5 references from the matching quadrant. For each, note:
- What specific design mechanic creates the emotional effect
- Which section/page demonstrates it best
- What to borrow vs what to leave behind

**Cross-quadrant blending rules**:
- Borrow ONE element from an adjacent quadrant for contrast (e.g., Cold+Active typography on Warm+Calm palette)
- NEVER borrow from the opposite quadrant (Cold+Calm elements on a Warm+Active site = confusion)
- Adjacent quadrants share one axis: Warm+Calm and Warm+Active share warmth; Cold+Calm and Cold+Active share precision

---

### Step 3: Extract Design Decisions

For each design dimension, reference the library to make a specific choice:

```
## Design Direction Document

**Quadrant**: [Warm+Calm / Warm+Active / Cold+Active / Cold+Calm]
**Primary references**: [3 sites from library]
**Cross-quadrant accent**: [1 element from adjacent quadrant, if any]

### Color Palette
- **Background**: [specific color + reference site that uses it]
- **Primary accent**: [specific color + emotional rationale]
- **Text**: [dark/light + contrast ratio reasoning]
- **System**: [monochromatic / complementary / analogous]

### Typography
- **Headings**: [serif/sans/display + weight + specific font suggestion]
- **Body**: [font + size + line-height + rationale from reference]
- **Personality**: [what the type says about the brand]

### Spacing & Layout
- **Density**: [generous/moderate/compact + reference]
- **Grid**: [columns + max-width + rationale]
- **White space**: [aggressive/balanced/minimal]
- **Section rhythm**: [alternating/consistent/progressive]

### Motion & Interaction
- **Animation style**: [subtle/expressive/none + reference]
- **Scroll behavior**: [smooth/standard/parallax]
- **Hover states**: [transform type + timing]
- **Page transitions**: [type or none]

### Photography & Imagery
- **Style**: [photography/illustration/abstract/mixed]
- **Emotional direction**: [reference to minimalist-image-director quadrant]
- **Treatment**: [full-color/muted/duotone/grain]

### Layout Pattern
- **Hero**: [full-bleed/contained/split/text-only]
- **Cards**: [bordered/borderless/elevated/flat]
- **Navigation**: [top/side/minimal/hidden]
```

---

### Step 4: Validate Against Positioning

Before finalizing, run the mismatch check:

```
## Positioning Mismatch Check

- [ ] Does the color temperature match the brand warmth? (warm brand = warm colors)
- [ ] Does the animation level match the brand energy? (calm brand ≠ aggressive animations)
- [ ] Does the typography match the brand authority level? (playful brand ≠ all-caps sans-serif)
- [ ] Would a visitor from the target audience feel welcomed or intimidated?
- [ ] Does this look DIFFERENT from the competitive alternatives?
- [ ] Would this design work for the brand's WORST day? (not just launch day)
```

---

## Reference Library — 48 Annotated Public Websites

### WARM + CALM — Nurturing Comfort
*"I feel safe and understood here"*

Sites in this quadrant use: warm color palettes, generous spacing, soft imagery, approachable typography, gentle transitions. They prioritize readability and emotional comfort over visual impact.

| # | Site | Industry | Key Design Mechanic | Best Page to Study | Anti-Pattern Warning |
|---|------|----------|--------------------|--------------------|---------------------|
| 1 | **[Headspace](https://headspace.com)** | Wellness/Meditation | Rounded shapes + warm illustration + pastel palette. Feels like a gentle hug. | Homepage hero + onboarding flow | Illustrations can tip into childish if not carefully balanced |
| 2 | **[Allbirds](https://allbirds.com)** | Sustainable Fashion | Earth tone photography + natural textures + clean grid. Product-first but warm. | Product detail pages | Can feel too "eco-corporate" without personality |
| 3 | **[Wildling Shoes](https://wildling.shoes)** | Children's Footwear | Nature photography + warm neutrals + organic flow. Feels like a forest walk. | Homepage scroll narrative | Easy to lose product focus in the nature imagery |
| 4 | **[Kinfolk](https://kinfolk.com)** | Lifestyle Editorial | Typography-led + generous whitespace + warm photography. Quiet confidence. | Article layouts | Can feel too sparse if content is thin |
| 5 | **[Cereal Magazine](https://readcereal.com)** | Travel/Design | Muted warm palette + editorial grid + contemplative imagery. Slow-paced. | Travel guides | Low contrast can hurt readability |
| 6 | **[Aesop](https://aesop.com)** | Beauty/Skincare | Warm-toned product photography + serif typography + restrained layout. Sophisticated warmth. | Store locator + product pages | Walks the line between Warm+Calm and Cold+Calm |
| 7 | **[Everlane](https://everlane.com)** | Ethical Fashion | Clean layout + warm lifestyle photography + transparent pricing. Honest warmth. | "About" page + factory stories | Transparency messaging can feel preachy if overdone |
| 8 | **[Patagonia](https://patagonia.com)** | Outdoor/Purpose | Bold warm photography + purpose-driven content + editorial depth. Activist warmth. | Environmental stories | Activism-forward design may alienate non-activist audiences |
| 9 | **[Nurture Life](https://nurturelife.com)** | Children's Meals | Soft pastels + rounded UI + warm food photography. Parent-friendly. | Meal plan page | Pastel overuse can feel generic "baby brand" |
| 10 | **[Organic Basics](https://organicbasics.com)** | Sustainable Essentials | Neutral tones + breathing space + minimal navigation. Calm commerce. | Product category pages | Too minimal can feel like "nothing to see here" |
| 11 | **[Ritual](https://ritual.com)** | Wellness/Supplements | Warm yellow accent + clean layout + scientific warmth. Trust through transparency. | Ingredient traceability page | Yellow accent can feel clinical if overdone |
| 12 | **[Mejuri](https://mejuri.com)** | Accessible Jewelry | Warm lifestyle photography + soft gold accents + clean e-commerce grid. Approachable luxury. | Collection pages | Balancing luxury feel with accessible pricing |

**Cross-quadrant pattern**: All Warm+Calm sites share generous line-height (1.6-1.8), muted/earthy palettes, and photography featuring real humans in natural environments. Navigation is always simple. Animations are always subtle.

---

### WARM + ACTIVE — Energetic Warmth
*"This is exciting AND friendly"*

Sites in this quadrant use: bold colors, dynamic animations, playful illustrations, energetic typography, interactive elements. They feel like an enthusiastic friend showing you something amazing.

| # | Site | Industry | Key Design Mechanic | Best Page to Study | Anti-Pattern Warning |
|---|------|----------|--------------------|--------------------|---------------------|
| 1 | **[Notion](https://notion.so)** | Productivity | Warm illustrations + clean product UI + friendly micro-interactions. Organized enthusiasm. | Templates gallery + homepage | Illustration style is heavily copied — find your own |
| 2 | **[Figma](https://figma.com)** | Design Tool | Vibrant gradients + collaborative energy + bold type. Design-forward without being cold. | Community/plugins page | Gradient-heavy design ages fast |
| 3 | **[Mailchimp](https://mailchimp.com)** | Email Marketing | Distinctive illustration + warm brand yellow + playful UI. Personality-driven. | Homepage + pricing page | Quirky illustration style requires strong brand commitment |
| 4 | **[Loom](https://loom.com)** | Video Communication | Warm purple + approachable UI + product-led animations. Tech that doesn't feel techy. | Product demo sections | Purple warmth can feel corporate if oversaturated |
| 5 | **[Intercom](https://intercom.com)** | Customer Comms | Bold colors + conversational copy + dynamic layout. Friendly authority. | Product tour pages | Bold palette can overwhelm without whitespace discipline |
| 6 | **[Monday.com](https://monday.com)** | Work Management | Vibrant multi-color + energetic animations + bold grid. High energy, high clarity. | Homepage product demo | Color explosion needs strict hierarchy or it's chaos |
| 7 | **[Miro](https://miro.com)** | Collaboration | Warm yellow + collaborative imagery + dynamic canvas previews. Creative energy. | Use case pages | Collaboration-focused imagery can feel generic |
| 8 | **[Webflow](https://webflow.com)** | Web Builder | Bold typography + empowering copy + creative showcases. Builder energy. | Showcase gallery + homepage | "Empowerment" messaging is crowded territory |
| 9 | **[Framer](https://framer.com)** | Design/Publish | Design-forward + bold motion + dark-warm hybrid. Creative tool confidence. | Templates + homepage | Motion-heavy design can slow page loads |
| 10 | **[Shopify](https://shopify.com)** | E-commerce Platform | Warm green + entrepreneurial energy + success stories. Optimistic commerce. | Success stories + homepage | Entrepreneurial energy can feel "hustle culture" |
| 11 | **[Asana](https://asana.com)** | Project Management | Warm coral/gradient + clean product UI + purposeful animation. Organized delight. | Product features page | Gradient overuse dates quickly |
| 12 | **[Canva](https://canva.com)** | Design Platform | Vibrant purple + accessible design + template showcases. Creative democratization. | Template gallery | Accessibility focus can lower perceived quality |

**Cross-quadrant pattern**: All Warm+Active sites use bold primary colors (not pastels), dynamic scroll animations, product-in-action demonstrations, and copy that speaks directly to the user ("you"). Typography is sans-serif, medium-to-heavy weight. Illustrations are distinctive, not generic.

---

### COLD + CALM — Refined Authority
*"This is elevated and exclusive"*

Sites in this quadrant use: restrained palettes (black/white/grey + one accent), generous negative space, serif or refined sans-serif typography, minimal animation, large-scale imagery. They communicate through what they DON'T show.

| # | Site | Industry | Key Design Mechanic | Best Page to Study | Anti-Pattern Warning |
|---|------|----------|--------------------|--------------------|---------------------|
| 1 | **[Cartier](https://cartier.com)** | Luxury Jewelry | Gold + black + cinematic photography + restrained interaction. Pure luxury. | High jewelry collections | Luxury codes translate poorly to non-luxury brands |
| 2 | **[Givenchy](https://givenchy.com)** | High Fashion | All-black + full-bleed photography + minimal type. Fashion authority. | Campaign pages | Dark + minimal = intimidating for mass-market brands |
| 3 | **[Monocle](https://monocle.com)** | Global Editorial | Clean editorial grid + restrained palette + typographic hierarchy. Intellectual confidence. | Magazine features | Editorial density requires deep content to justify |
| 4 | **[Herzog & de Meuron](https://herzogdemeuron.com)** | Architecture | Pure white + project photography + minimal navigation. Architecture as interface. | Project pages | Ultra-minimal navigation frustrates casual visitors |
| 5 | **[White Cube](https://whitecube.com)** | Gallery | Gallery-white + art-first + invisible UI. The content IS the design. | Exhibition pages | Works only when content is visually stunning |
| 6 | **[Eleven Madison Park](https://elevenmadisonpark.com)** | Fine Dining | Dark + restrained + cinematic food photography. Culinary theater. | Menu/experience pages | Restaurant-level restraint only works at prestige price points |
| 7 | **[Apple](https://apple.com)** | Technology | Heroic product photography + clean sections + precise typography. Controlled reveal. | Product launch pages | Apple's resources are unreplicable — adapt principles, not execution |
| 8 | **[Porsche](https://porsche.com)** | Automotive | Dark + performance photography + precise grid + controlled motion. Engineered elegance. | Model configurator | Automotive drama requires studio-quality photography |
| 9 | **[Bang & Olufsen](https://bang-olufsen.com)** | Audio/Design | Product-as-sculpture + neutral backgrounds + design-led layout. Object worship. | Product detail pages | Requires genuinely beautiful physical products |
| 10 | **[Bottega Veneta](https://bottegaveneta.com)** | Luxury Fashion | Green accent + editorial photography + dramatic scale shifts. Confident restraint. | Digital journal | Bold restraint requires creative director-level judgment |
| 11 | **[Ace & Tate](https://aceandtate.com)** | Eyewear | Clean photography + muted palette + editorial storytelling. Accessible refinement. | Stories/editorial section | Can feel "trying too hard" for luxury if product doesn't match |
| 12 | **[The Row](https://therow.com)** | Luxury Fashion | Near-invisible navigation + maximal whitespace + whisper-quiet typography. Peak restraint. | Homepage | Extreme minimalism only works with strong brand recognition |

**Cross-quadrant pattern**: All Cold+Calm sites use serif or thin sans-serif type, monochromatic or near-monochromatic palettes, full-bleed imagery, and a high content-to-chrome ratio. Navigation is minimized. Animation is rare and subtle. Copy is sparse — the imagery carries the message.

---

### COLD + ACTIVE — Innovative Power
*"This is cutting-edge and serious"*

Sites in this quadrant use: dark backgrounds, sharp typography, bold gradients, technical demonstrations, fast-paced scroll animations, code/data visualizations. They communicate speed, precision, and technical authority.

| # | Site | Industry | Key Design Mechanic | Best Page to Study | Anti-Pattern Warning |
|---|------|----------|--------------------|--------------------|---------------------|
| 1 | **[Vercel](https://vercel.com)** | Infrastructure | Dark mode + sharp type + speed metrics visualization. Performance as brand. | Homepage + framework pages | Dark mode developer aesthetic alienates non-technical audiences |
| 2 | **[Linear](https://linear.app)** | Issue Tracking | Dark + precise animations + product-first UI. Tool confidence. | Homepage scroll sequence | Ultra-refined dark UI requires significant engineering investment |
| 3 | **[Stripe](https://stripe.com)** | Payments | Deep gradients + technical elegance + interactive demos. Beautiful complexity. | Documentation + payment flows | Stripe's production quality is a benchmark but requires dedicated design team |
| 4 | **[Supabase](https://supabase.com)** | Database Platform | Dark green + developer-friendly + open source aesthetic. Technical warmth. | Dashboard preview + docs | Open-source aesthetic can feel "unfinished" to enterprise buyers |
| 5 | **[Railway](https://railway.com)** | Cloud Platform | Dark purple + clean deployment UI + minimal friction design. Developer delight. | Dashboard + deploy flow | Purple dark mode is becoming cliche in dev tools |
| 6 | **[Anthropic](https://anthropic.com)** | AI Research | Clean white + research depth + restrained authority. Scientific confidence. | Research papers page | Borders Cold+Calm — uses restraint over aggression |
| 7 | **[Plaid](https://plaid.com)** | Financial API | Structured layout + technical diagrams + clean documentation. Fintech precision. | API documentation + use cases | Financial/API aesthetic can feel dry without product visualization |
| 8 | **[Wiz](https://wiz.io)** | Cloud Security | Dark + bold gradients + threat visualization. Security authority. | Platform overview | Security aesthetic (dark+aggressive) can feel threatening |
| 9 | **[CrowdStrike](https://crowdstrike.com)** | Cybersecurity | Dark red-black + aggressive typography + threat intelligence dashboards. Protective power. | Platform pages | Aggressive design repels non-security audiences |
| 10 | **[Raycast](https://raycast.com)** | Developer Productivity | Dark + smooth animations + keyboard-first design. Speed culture. | Extensions store + homepage | Keyboard-first aesthetic limits mobile appeal |
| 11 | **[Arc Browser](https://arc.net)** | Browser | Bold gradients + playful-dark hybrid + product innovation showcase. Tech with personality. | Homepage + feature reveals | Playful-dark is hard to maintain across an entire site |
| 12 | **[Resend](https://resend.com)** | Email API | Dark + minimal + typographic focus + code-first. Developer minimalism. | Homepage + documentation | Ultra-minimal dev sites can feel empty to non-developers |

**Cross-quadrant pattern**: All Cold+Active sites use dark backgrounds (#000-#1a1a1a), monospace or geometric sans-serif type, gradient accents (purple/blue/green), product demos as hero elements, and performance/speed messaging. Copy is technical and precise. Motion is deliberate and fast.

---

## Cross-Quadrant Pattern Analysis

### Design Dimensions by Quadrant

| Dimension | Warm+Calm | Warm+Active | Cold+Calm | Cold+Active |
|-----------|-----------|-------------|-----------|-------------|
| **Background** | Cream/warm white (#FAF5F0-#FFF) | White + bold accent sections | Pure white or black | Dark (#000-#111) |
| **Typography** | Rounded sans or warm serif | Bold sans, medium-heavy weight | Thin sans or elegant serif | Geometric/monospace sans |
| **Primary color** | Earth tones, muted | Bold primaries (yellow, coral, purple) | Black/white + 1 accent | Gradients (purple, blue, green) |
| **Spacing** | Very generous (64-128px) | Generous but dynamic (48-96px) | Maximal (80-160px) | Moderate (32-64px) |
| **Animation** | Subtle fades, gentle scroll | Dynamic, playful, interactive | Rare, restrained | Fast, precise, technical |
| **Imagery** | Warm photography, natural light | Illustrations + product demos | Full-bleed cinematic photography | Product UI, code, data viz |
| **Copy tone** | Warm, empathetic, "we understand" | Energetic, "let's build", "you can" | Sparse, "the work speaks" | Technical, precise, "built for speed" |
| **Navigation** | Simple, visible | Rich, product-organized | Minimal, hidden | Minimal, keyboard-friendly |
| **Cards** | Borderless, soft shadow | Bold borders or colorful | Full-bleed or framed | Dark with subtle borders |
| **CTA style** | Soft, rounded, warm color | Bold, filled, high-contrast | Understated, text-link style | Sharp, outlined or gradient |
| **Line-height** | 1.6-1.8 (breathing room) | 1.4-1.6 (balanced) | 1.4-1.6 (elegant) | 1.3-1.5 (dense, efficient) |
| **Max-width** | 1100-1200px | 1200-1400px | 1200-1400px | 1000-1200px |

### The "Adjacent Quadrant" Blending Guide

Borrow ONE element from an adjacent quadrant to add tension and interest:

| Your quadrant | Adjacent options | Blending example |
|---------------|-----------------|-----------------|
| Warm+Calm | Warm+Active OR Cold+Calm | Calm site + one bold CTA color (from Active) |
| Warm+Active | Warm+Calm OR Cold+Active | Active site + generous spacing (from Calm) |
| Cold+Calm | Warm+Calm OR Cold+Active | Luxury site + warm accent color (from Warm) |
| Cold+Active | Warm+Active OR Cold+Calm | Dev tool + refined serif headlines (from Calm) |

**NEVER blend opposites**: Warm+Calm + Cold+Active = confused identity. Cold+Calm + Warm+Active = schizophrenic.

---

## Skill Boundaries (Frontier Recognition)

### This skill excels for:
- New website projects where visual direction hasn't been decided
- Brand repositioning (mapping new positioning to new visual language)
- Design audits (is the current design aligned with brand intent?)
- Creative briefs for designers or AI coding tools
- Cross-functional alignment (giving non-designers vocabulary for design feedback)

### This skill is NOT ideal for:
- Specific UI component design (use `/frontend-design` for implementation)
- Typography pairing details (this provides direction, not font selection)
- Design system creation (this is strategic, not systematic)
- Animation engineering (this defines intent, not keyframes)
- Sites that intentionally subvert expectations (anti-design, brutalism) — those require breaking these rules deliberately

### Quality Checkpoints

Before accepting the design direction:
- [ ] The quadrant selection matches the brand positioning (not just personal taste)
- [ ] The reference sites match the client's ASPIRATIONAL identity, not their current state
- [ ] The cross-quadrant blend is intentional and limited (1 element max)
- [ ] The direction document is specific enough to implement without further interpretation
- [ ] A non-designer on the team could understand and validate the direction

---

## Iteration Guide

> "Direction before decoration. Feel before font."

### Recommended Iteration Pattern

| Pass | Focus | Questions to Ask |
|------|-------|------------------|
| **1st** | Quadrant | "Does this quadrant match the brand's emotional territory?" |
| **2nd** | References | "Do these sites FEEL like my brand should feel?" |
| **3rd** | Extraction | "Are the design decisions specific enough to implement?" |
| **4th** | Mismatch | "Would a visitor from our target audience feel at home?" |

### Useful Follow-up Prompts

- "The references feel right but the palette doesn't translate to our industry. Find references with the same energy but in [industry]."
- "We're between Warm+Calm and Cold+Calm. Show me 3 sites that straddle that border."
- "The direction is too safe. What would an adjacent-quadrant accent do to this design?"
- "Our competitor uses [X quadrant]. How do we differentiate visually while staying in the same emotional territory?"
- "Translate this design direction into a brief for the `/frontend-design` skill."

---

## Integration with Other ClawFu Skills

| Skill | Integration Point |
|-------|------------------|
| **[design-trends-2026](../design-trends-2026/)** | Use AFTER quadrant selection — filter trends by emotional fit |
| **[minimalist-image-director](../minimalist-image-director/)** | Use for photography direction within Warm+Calm and Warm+Active quadrants |
| **[landing-page-copy](../../content/landing-page-copy/)** | Use for copy structure — then match copy tone to quadrant voice |
| **[landing-page-optimizer](../../content/landing-page-optimizer/)** | Use for conversion mechanics — layer on top of emotional direction |
| **`/frontend-design`** | Hand off the design direction document as input for code generation |
| **[brand-strategy](../../branding/brand-strategy/)** | Use BEFORE this skill — brand strategy determines the quadrant |

**Workflow sequence**:
```
brand-strategy → web-design-director → design-trends-2026 → minimalist-image-director → /frontend-design
(positioning)    (direction)           (trend filter)        (image generation)           (code)
```

---

## Checklists & Templates

### Design Direction Brief Template

```
## Design Direction Brief

**Brand**: ________________
**Target audience**: ________________
**Brand positioning statement**: ________________
**Competitive alternatives**: ________________

### Emotional Quadrant
**Selected**: [Warm+Calm / Warm+Active / Cold+Active / Cold+Calm]
**Rationale**: ________________
**Adjacent accent**: [element from adjacent quadrant, if any]

### Primary References (3-5 sites)
| Site | What to borrow | What to leave behind |
|------|---------------|---------------------|
| [site 1] | [specific mechanic] | [what doesn't fit] |
| [site 2] | [specific mechanic] | [what doesn't fit] |
| [site 3] | [specific mechanic] | [what doesn't fit] |

### Design Decisions
- **Background**: ________________
- **Primary color**: ________________
- **Typography headings**: ________________
- **Typography body**: ________________
- **Spacing density**: ________________
- **Animation style**: ________________
- **Photography direction**: ________________
- **Card style**: ________________
- **CTA style**: ________________
- **Hero pattern**: ________________

### Validation
- [ ] Matches brand quadrant
- [ ] Different from competitive alternatives
- [ ] Target audience would feel welcomed
- [ ] Specific enough to implement
```

---

## References

### Core Methodology
- Norman, Don. "Emotional Design" (2004) - Visceral, behavioral, reflective processing
- Dunford, April. "Obviously Awesome" (2019) - Competitive alternatives define positioning territory
- Kittl x Savee. "2026 Design Trends Report" - Warm minimalism as dominant trend

### Design Inspiration Platforms (Gap Analysis)
- [Awwwards](https://awwwards.com) - Categories: industry, technology, style. No emotional classification.
- [Dribbble](https://dribbble.com) - Categories: color, media type. No emotional classification.
- [Behance](https://behance.net) - Categories: field, tools. No emotional classification.
- [Godly](https://godly.website) - Categories: style, type. No emotional classification.
- [Mobbin](https://mobbin.com) - Categories: platform, flow type. No emotional classification.
- [SiteInspire](https://siteinspire.com) - Categories: style, type, subject. No emotional classification.
- [Lapa.ninja](https://lapa.ninja) - Categories: color, category. No emotional classification.
- [Landbook](https://land-book.com) - Categories: type, color, style. No emotional classification.

### Color Psychology & Neuroscience
- [Visual Environment & Thermal Perception (ScienceDirect)](https://www.sciencedirect.com/science/article/pii/S0306456523000293) - Visual warmth affects perception
- [Color Psychology in Photography (Skylum)](https://skylum.com/blog/color-psychology-for-photographers) - Warm/cool behavioral response
- [Cold Temperatures in Photos Increase Cognitive Control (ScienceDaily)](https://www.sciencedaily.com/releases/2017/04/170410085010.htm) - Warm → approach, cool → alert

### Web Design Analysis
- [Web Design Trends 2026 (Webflow)](https://webflow.com/blog/web-design-trends) - Industry trend survey
- [The Best SaaS Websites (2025-2026)](https://www.saasframe.io) - SaaS design pattern library

---

## Related Skills

- [minimalist-image-director](../minimalist-image-director/) - AI photography within the emotional quadrant system
- [design-trends-2026](../design-trends-2026/) - Current visual trends filtered by quadrant
- [landing-page-copy](../../content/landing-page-copy/) - Copy structure matching quadrant voice
- [landing-page-optimizer](../../content/landing-page-optimizer/) - Conversion mechanics on top of emotional direction
- [brand-strategy](../../branding/brand-strategy/) - Brand foundation that determines the quadrant

---

## Skill Metadata

```yaml
name: web-design-director
category: ai-design
subcategory: art-direction
version: 1.0
author: GUIA
source_expert: Don Norman (Emotional Design) + April Dunford (Positioning) + Web Design Pattern Analysis (48 sites)
source_work: null
difficulty: intermediate
mode: centaur
estimated_value: Creative director engagement (~2000-5000 EUR per project)
tags: [web-design, art-direction, emotional-design, design-references, brand-positioning, UI-direction, design-system, mood-board, warm-minimalism]
created: 2026-02-12
updated: 2026-02-12
```

---

*This skill is part of the GUIA Premium Marketing Skills Library — the 201 layer that bridges AI basics and technical implementation.*
