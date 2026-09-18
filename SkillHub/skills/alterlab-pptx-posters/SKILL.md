---
name: alterlab-pptx-posters
description: Creates research posters in HTML/CSS with responsive layouts and easy visual integration, exportable to PDF or PPTX. Use ONLY when the user explicitly requests a PowerPoint/PPTX/PPT poster, an HTML/web-based poster, or a poster they will edit in PowerPoint, or when LaTeX is unavailable. For a standard/conference research poster with no format named, use alterlab-latex-posters instead; for a slide deck/oral-talk presentation, use alterlab-scientific-slides. Part of the AlterLab Academic Skills suite.
allowed-tools: Read Write Edit Bash
license: MIT
compatibility: Authors HTML/CSS posters with no external service; exporting to PDF or PPTX requires a headless Chrome browser (and python-pptx for PPTX)
metadata:
    skill-author: AlterLab
    version: "1.0.0"
---

# PPTX Research Posters (HTML-Based)

## Overview

**⚠️ USE THIS SKILL ONLY WHEN USER EXPLICITLY REQUESTS PPTX/POWERPOINT POSTER FORMAT.**

For standard research posters, use the **latex-posters** skill instead, which provides better typographic control and is the default for academic conferences.

This skill creates research posters using HTML/CSS, which can then be exported to PDF or converted to PowerPoint format. The web-based approach offers:
- Modern, responsive layouts
- Easy integration of AI-generated visuals
- Quick iteration and preview in browser
- Export to PDF via browser print function
- Conversion to PPTX if specifically needed

## When to Use This Skill

**ONLY use this skill when:**
- User explicitly requests "PPTX poster", "PowerPoint poster", or "PPT poster"
- User specifically asks for HTML-based poster
- User needs to edit poster in PowerPoint after creation
- LaTeX is not available or user requests non-LaTeX solution

**DO NOT use this skill when:**
- User asks for a "poster" without specifying format → Use latex-posters
- User asks for "research poster" or "conference poster" → Use latex-posters
- User mentions LaTeX, tikzposter, beamerposter, or baposter → Use latex-posters

## Visual Element Generation

If a diagram or figure would aid comprehension, invoke the **alterlab-scientific-schematics** skill (diagrams/schematics) or the **alterlab-generate-image** skill (images). Figures are optional — add them only where they improve clarity.

A practical workflow for a visual poster:
1. Plan the visual elements that would help (hero image, intro, methods, results, conclusions)
2. Generate any needed figures via the skills above
3. Assemble the figures in the HTML template
4. Add text content around the visuals

Posters generally read best when visuals carry much of the message and text stays concise.

---

### Poster-Size Font Requirements

Text within poster visualizations needs to be poster-readable. Poster graphics are viewed from 4-6 feet away, so text must be large. When generating a figure, describe these readability constraints in the prompt:

```
POSTER FORMAT GUIDELINES:
- Keep to 3-4 elements per graphic (3 is ideal)
- Around 10 words total in the entire graphic
- Avoid complex workflows with 5+ steps (split into 2-3 simple graphics instead)
- Avoid multi-level nested diagrams (flatten to a single level)
- One key point per case study (not multiple sub-sections)
- Large bold text (80pt+ for labels, 120pt+ for key numbers)
- High contrast (dark on white OR white on dark; avoid gradients behind text)
- Generous white space (around 50%)
- Thick lines (5px+), large icons (200px+)
- One single message per graphic
```

**Before generating, review the prompt and count elements:**
- If the description has 5+ items, split into multiple graphics
- If the workflow has 5+ stages, show only 3-4 high-level steps
- If the comparison has 4+ methods, show only the top 3 or Ours vs Best Baseline

**Example — too dense (7-stage workflow):** "Drug discovery workflow: Target ID, Synthesis, Screening, Lead Opt, Validation, Clinical Trial, FDA Approval with metrics" — this crams in too many stages and renders as tiny, unreadable text.

**Example — readable (3 mega-stages):** "POSTER FORMAT for A0. Ultra-simple 3-box workflow: 'DISCOVER' → 'VALIDATE' → 'APPROVE'. Each word in giant bold (120pt+). Thick arrows (10px). 60% white space. Only these 3 words, no substeps. Readable from 12 feet." — same content, simplified to a readable poster format.

---

### CRITICAL: Preventing Content Overflow

**⚠️ POSTERS MUST NOT HAVE TEXT OR CONTENT CUT OFF AT EDGES.**

**Prevention Rules:**

**1. Limit Content Sections (MAXIMUM 5-6 sections):**
```
✅ GOOD - 5 sections with room to breathe:
   - Title/Header
   - Introduction/Problem
   - Methods
   - Results (1-2 key findings)
   - Conclusions

❌ BAD - 8+ sections crammed together
```

**2. Word Count Limits:**
- **Per section**: 50-100 words maximum
- **Total poster**: 300-800 words MAXIMUM
- **If you have more content**: Cut it or make a handout

---

## Core Capabilities

### 1. HTML/CSS Poster Design

The HTML template (`assets/poster_html_template.html`) provides:
- Fixed poster dimensions (36×48 inches = 2592×3456 pt)
- Professional header with gradient styling
- Three-column content layout
- Block-based sections with modern styling
- Footer with references and contact info

### 2. Poster Structure

**Standard Layout:**
```
┌─────────────────────────────────────────┐
│  HEADER: Title, Authors, Hero Image     │
├─────────────┬─────────────┬─────────────┤
│ Introduction│   Results   │  Discussion │
│             │             │             │
│   Methods   │   (charts)  │ Conclusions │
│             │             │             │
│  (diagram)  │   (data)    │   (summary) │
├─────────────┴─────────────┴─────────────┤
│  FOOTER: References & Contact Info      │
└─────────────────────────────────────────┘
```

### 3. Visual Integration

Each section should prominently feature AI-generated visuals:

**Hero Image (Header):**
```html
<img src="figures/hero.png" class="hero-image">
```

**Section Graphics:**
```html
<div class="block">
  <h2 class="block-title">Methods</h2>
  <div class="block-content">
    <img src="figures/workflow.png" class="block-image">
    <ul>
      <li>Brief methodology point</li>
    </ul>
  </div>
</div>
```

### 4. Generating Visual Elements

Generate figures via **alterlab-scientific-schematics** (diagrams) or **alterlab-generate-image** (images), as noted above. Example prompts that keep poster graphics simple and readable (save into a `figures/` directory):

- **Hero image** — "POSTER FORMAT for A0. Hero banner: '[TOPIC]' in huge text (120pt+). Dark blue gradient background. One iconic visual. Minimal text. Readable from 15 feet."
- **Introduction visual** — "POSTER FORMAT for A0. Simple visual with only 3 icons: [icon1] → [icon2] → [icon3]. One-word labels (80pt+). 50% white space. Readable from 8 feet."
- **Methods flowchart** — "POSTER FORMAT for A0. Simple flowchart with only 4 boxes: STEP1 → STEP2 → STEP3 → STEP4. Giant labels (100pt+). Thick arrows. 50% white space. No sub-steps."
- **Results visualization** — "POSTER FORMAT for A0. Simple bar chart with only 3 bars: BASELINE (70%), EXISTING (85%), OURS (95%). Giant percentages on bars (120pt+). No axis, no legend. 50% white space."
- **Conclusions** — "POSTER FORMAT for A0. Exactly 3 cards: '95%' (150pt) 'ACCURACY' (60pt), '2X' (150pt) 'FASTER' (60pt), checkmark 'READY' (60pt). 50% white space. No other text."

---

## Workflow for PPTX Poster Creation

### Stage 1: Planning

1. **Confirm PPTX is explicitly requested**
2. **Determine poster requirements:**
   - Size: 36×48 inches (most common) or A0
   - Orientation: Portrait (most common)
3. **Develop content outline:**
   - Identify 1-3 core messages
   - Plan 3-5 visual elements
   - Draft minimal text (300-800 words total)

### Stage 2: Generate Visual Elements (AI-Powered)

**CRITICAL: Generate SIMPLE figures with MINIMAL content.**

```bash
mkdir -p figures

# Generate each element with POSTER FORMAT specifications
# (See examples in Section 4 above)
```

### Stage 3: Create HTML Poster

1. **Copy the template** from this skill's `assets/` directory:
   ```bash
   cp assets/poster_html_template.html poster.html
   ```

2. **Update content:**
   - Replace placeholder title and authors
   - Insert AI-generated images
   - Add minimal supporting text
   - Update references and contact info

3. **Preview in browser:**
   ```bash
   open poster.html  # macOS
   # or
   xdg-open poster.html  # Linux
   ```

### Stage 4: Export to PDF

The template's `@page` rule (added in the template `<style>`) fixes the PDF page to the poster size, so exports come out at full dimensions instead of being cropped to Letter/A4.

**Browser Print Method:**
1. Open poster.html in Chrome
2. Print (Cmd/Ctrl + P)
3. Select "Save as PDF"
4. Paper size: leave on the size the `@page` rule sets, or pick a custom size matching the poster
5. Margins: None
6. Enable "Background graphics" (otherwise the gradients and block backgrounds are dropped)

**Command Line (Chrome headless):**
```bash
# Use the new headless mode (Chrome 132+ ships old --headless only as the
# separate chrome-headless-shell binary). On macOS the binary lives at:
#   /Applications/Google Chrome.app/Contents/MacOS/Google Chrome
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless=new \
  --no-pdf-header-footer \
  --print-to-pdf=poster.pdf \
  "file://$PWD/poster.html"
```
`--no-pdf-header-footer` replaces the older `--print-to-pdf-no-header`; on Chrome versions before ~118 fall back to the old flag name. Page size and zero margin come from the template's `@page` rule, not a CLI flag.

### Stage 5: Convert to PPTX (If Required)

**Pick the path based on what "PPTX" needs to be:**

**Option 1 — Single-image slide (fast, NOT editable).** Convert the exported PDF page (or a rasterized PNG of it) into one full-bleed picture on a poster-sized slide. This is the right choice when the user just wants a `.pptx` *container* to project or submit. LibreOffice's PDF import treats the PDF as a drawing, so the slide content is effectively a flattened image — text is **not** editable in PowerPoint.
```bash
# Rasterize the PDF to a PNG, then place it as one slide (see python-pptx below).
# A direct `libreoffice --convert-to pptx poster.pdf` produces a non-editable,
# image-like slide and often misplaces content — prefer the python-pptx path.
magick -density 150 poster.pdf poster.png
```

**Option 2 — Native PPTX with python-pptx (editable).** Use this when the user actually wants to *edit the poster in PowerPoint*. Build the slide from the same `figures/` and text so each element is a real, movable PowerPoint object. Match the slide size to the poster orientation — the template is **portrait 36in wide × 48in tall**:
```python
from pptx import Presentation
from pptx.util import Inches, Pt

prs = Presentation()
prs.slide_width = Inches(36)   # portrait: width < height (match the template)
prs.slide_height = Inches(48)

slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank

# Add images from figures/ (positions in inches from top-left)
slide.shapes.add_picture("figures/hero.png", Inches(0), Inches(0), width=Inches(36))
# ... add text boxes and other images for each section

prs.save("poster.pptx")
```
Install with `uv pip install python-pptx` (or `uvx`); `magick` is ImageMagick.

---

## HTML Template Structure

The provided template (`assets/poster_html_template.html`) includes:

### CSS Variables for Customization

```css
/* Poster dimensions */
body {
  width: 2592pt;   /* 36 inches */
  height: 3456pt;  /* 48 inches */
}

/* Color scheme - customize these */
.header {
  background: linear-gradient(135deg, #1a365d 0%, #2b6cb0 50%, #3182ce 100%);
}

/* Typography */
.poster-title { font-size: 108pt; }
.authors { font-size: 48pt; }
.block-title { font-size: 52pt; }
.block-content { font-size: 34pt; }
```

### Key Classes

| Class | Purpose | Font Size |
|-------|---------|-----------|
| `.poster-title` | Main title | 108pt |
| `.authors` | Author names | 48pt |
| `.affiliations` | Institutions | 38pt |
| `.block-title` | Section headers | 52pt |
| `.block-content` | Body text | 34pt |
| `.key-finding` | Highlight box | 36pt |

---

## Quality Checklist

### Step 0: Pre-Generation Review

**For EACH planned graphic, verify:**
- [ ] Can describe in 3-4 items or less? (NOT 5+)
- [ ] Is it a simple workflow (3-4 steps, NOT 7+)?
- [ ] Can describe all text in 10 words or less?
- [ ] Does it convey ONE message (not multiple)?

**Reject these patterns:**
- ❌ "7-stage workflow" → Simplify to "3 mega-stages"
- ❌ "Multiple case studies" → One case per graphic
- ❌ "Timeline 2015-2024 annual" → "ONLY 3 key years"
- ❌ "Compare 6 methods" → "ONLY 2: ours vs best"

### Step 2b: Post-Generation Review

**For EACH generated figure at 25% zoom:**

**✅ PASS criteria (ALL must be true):**
- [ ] Can read ALL text clearly
- [ ] Count: 3-4 elements or fewer
- [ ] White space: 50%+ empty
- [ ] Understand in 2 seconds
- [ ] NOT a complex 5+ stage workflow
- [ ] NOT multiple nested sections

**❌ FAIL criteria (regenerate if ANY true):**
- [ ] Text small/hard to read → Regenerate with "150pt+"
- [ ] More than 4 elements → Regenerate "ONLY 3 elements"
- [ ] Less than 50% white space → Regenerate "60% white space"
- [ ] Complex multi-stage → SPLIT into 2-3 graphics
- [ ] Multiple cases cramped → SPLIT into separate graphics

### After Export

- [ ] NO content cut off at ANY of the 4 edges (check carefully)
- [ ] All images display correctly
- [ ] Colors render as expected
- [ ] Text readable at 25% scale
- [ ] Graphics look SIMPLE (not like complex 7-stage workflows)

---

## Common Pitfalls to Avoid

**AI-Generated Graphics Mistakes:**
- ❌ Too many elements (10+ items) → Keep to 3-5 max
- ❌ Text too small → Specify "GIANT (100pt+)" in prompts
- ❌ No white space → Add "50% white space" to every prompt
- ❌ Complex flowcharts (8+ steps) → Limit to 4-5 steps

**HTML/Export Mistakes:**
- ❌ Content exceeding poster dimensions → Check overflow in browser
- ❌ Missing background graphics in PDF → Enable in print settings
- ❌ Wrong paper size in PDF → Match poster dimensions exactly
- ❌ Low-resolution images → Use 300 DPI minimum

**Content Mistakes:**
- ❌ Too much text (over 1000 words) → Cut to 300-800 words
- ❌ Too many sections (7+) → Consolidate to 5-6
- ❌ No clear visual hierarchy → Make key findings prominent

---

## Integration with Other Skills

This skill works with:
- **alterlab-scientific-schematics**: poster diagrams and flowcharts
- **alterlab-generate-image**: hero images and stylized graphics
- **alterlab-latex-posters**: DEFAULT skill for poster creation (use it instead unless PPTX/PowerPoint or HTML is explicitly requested)

---

## Template Assets

Available in `assets/` directory:

- `poster_html_template.html`: Main HTML poster template (36×48 inches)
- `poster_quality_checklist.md`: Pre-submission validation checklist

## References

Available in `references/` directory:

- `poster_content_guide.md`: Content organization and writing guidelines
- `poster_design_principles.md`: Typography, color theory, and visual hierarchy
- `poster_layout_design.md`: Layout principles and grid systems

