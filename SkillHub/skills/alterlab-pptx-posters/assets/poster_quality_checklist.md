# Research Poster Quality Checklist (HTML / PDF / PPTX)

Use this checklist before exporting, printing, or presenting an HTML-based research poster.
For LaTeX posters, use the **alterlab-latex-posters** skill's own checklist instead.

## Pre-Export Checks

### Content Completeness
- [ ] Title is concise and descriptive (10-15 words)
- [ ] All author names spelled correctly
- [ ] Affiliations complete and accurate
- [ ] Contact email address included
- [ ] All sections present: Introduction, Methods, Results, Conclusions
- [ ] References cited (5-10 key citations)
- [ ] Acknowledgments included (funding, collaborators)
- [ ] No placeholder text remaining (TODO, Lorem ipsum, "Your Research Title Here", etc.)
- [ ] Total word count 300-800 (hard cap 1000)

### Visual Content
- [ ] All figures generated and saved under `figures/`
- [ ] Image paths in the HTML resolve (no broken `<img>` placeholders)
- [ ] Figures high resolution (300+ DPI for print)
- [ ] Figure text readable from distance (poster-format prompts used)
- [ ] Logos available (university, funding agencies)
- [ ] QR codes generated and tested (if used)

### HTML/CSS Configuration
- [ ] `@page { size: ...; margin: 0 }` matches the intended poster size
- [ ] `body` width/height (in pt) matches that size (e.g. 36in = 2592pt)
- [ ] Correct orientation (portrait/landscape)
- [ ] Font sizes appropriate (title 72pt+, body 24pt+)
- [ ] Color scheme defined and consistent
- [ ] `print-color-adjust: exact` set so backgrounds/gradients survive export

## Browser Preview Checks

Open `poster.html` in Chrome and inspect before exporting.

- [ ] No content overflows the poster bounds (no horizontal scrollbar at 100%)
- [ ] No text or images clipped at the four edges
- [ ] Columns balanced; no single column dramatically longer
- [ ] All images load (check the console / network tab for 404s)
- [ ] Layout matches intent at 25% zoom (readability sanity check)

## Exported PDF Quality Checks

After print-to-PDF or `chrome --headless=new --print-to-pdf`:

#### Page Specifications
```bash
pdfinfo poster.pdf | grep "Page size"
```
- [ ] Page size matches the poster dimensions exactly (e.g. 2592 x 3456 pt)
- [ ] Single page document (not split across multiple pages)
- [ ] Correct orientation

#### Image Quality
```bash
pdfimages -list poster.pdf
```
- [ ] Embedded images at least 300 DPI at final size
- [ ] No visible JPEG artifacts in figures

#### File Size
```bash
ls -lh poster.pdf
```
- [ ] Reasonable size (2-50 MB typical)
- [ ] Not too large for email (<50 MB) if sharing digitally
- [ ] Not suspiciously small (<1 MB - backgrounds may have been dropped; re-enable "Background graphics")

## Visual Inspection (100% Zoom)

### Layout and Spacing
- [ ] Content fills entire page (no excessive white margins)
- [ ] Consistent spacing between columns (1-2cm)
- [ ] Consistent spacing between blocks (1-2cm)
- [ ] All elements aligned to grid
- [ ] No overlapping text or figures
- [ ] White space evenly distributed (30-40% total)
- [ ] Visual balance across poster (no heavy/empty areas)

### Typography
- [ ] Title readable and prominent (72-120pt)
- [ ] Section headers clear (48-72pt)
- [ ] Body text large enough (24-36pt minimum, 30pt+ recommended)
- [ ] Captions readable (18-24pt)
- [ ] No text running off edges
- [ ] Consistent font usage throughout
- [ ] Line spacing adequate (1.2-1.5×)
- [ ] No awkward hyphenation or word breaks
- [ ] All special characters render correctly (Greek, math symbols)

### Visual Elements
- [ ] All figures display correctly
- [ ] No pixelated or blurry images
- [ ] Figure resolution high (zoom to 200% to verify)
- [ ] Figure labels large and clear
- [ ] Graph axes labeled with units
- [ ] Color schemes consistent across figures
- [ ] Legends readable and well-positioned
- [ ] Logos crisp and professional
- [ ] QR codes sharp and high-contrast (minimum 2×2cm)
- [ ] No visual artifacts or rendering errors

### Colors
- [ ] Colors render as intended (not washed out)
- [ ] High contrast between text and background (≥4.5:1)
- [ ] Color scheme harmonious
- [ ] Colors appropriate for printing (not too bright/neon)
- [ ] Institutional colors used correctly
- [ ] Color-blind friendly palette (avoid red-green only)

### Content
- [ ] Title complete and correctly positioned
- [ ] All author names and affiliations visible
- [ ] All sections present and labeled
- [ ] Results section has figures/data
- [ ] Conclusions clearly stated
- [ ] References formatted consistently
- [ ] Contact information clearly visible
- [ ] No missing content

## Reduced-Scale Print Test (CRITICAL)

### Test Print Preparation
Print poster at 25% scale:
- A0 poster → Print on A4 paper
- 36×48" poster → Print on Letter paper
- A1 poster → Print on A5 paper

### Readability from Distance

**From 6 feet (2 meters):**
- [ ] Title clearly readable
- [ ] Authors identifiable
- [ ] Main figures visible

**From 4 feet (1.2 meters):**
- [ ] Section headers readable
- [ ] Figure captions readable
- [ ] Key results visible

**From 2 feet (0.6 meters):**
- [ ] Body text readable
- [ ] References readable
- [ ] All details clear

### Print Quality
- [ ] Colors accurate (match screen expectations)
- [ ] No banding or color shifts
- [ ] Sharp edges (not blurry)
- [ ] Consistent print density
- [ ] No printer artifacts

## Content Proofreading

### Text Accuracy
- [ ] Spell-checked all text
- [ ] Grammar checked
- [ ] All author names spelled correctly
- [ ] All affiliations accurate
- [ ] Email address correct
- [ ] No typos in title or headers

### Scientific Accuracy
- [ ] All numbers and statistics verified
- [ ] Units included and correct
- [ ] Statistical significance correctly indicated
- [ ] Sample sizes (n=) reported
- [ ] Figure numbering consistent
- [ ] Citations accurate and complete
- [ ] Methodology accurately described
- [ ] Results match figures/data
- [ ] Conclusions supported by data

### Consistency
- [ ] Terminology consistent throughout
- [ ] Abbreviations defined at first use
- [ ] Consistent notation (italics for genes, etc.)
- [ ] Consistent units (don't mix metric/imperial)
- [ ] Consistent decimal places
- [ ] Consistent citation format

## Accessibility Checks

### Color Contrast
Test at: https://webaim.org/resources/contrastchecker/

- [ ] Title-background contrast ≥ 7:1
- [ ] Body text-background contrast ≥ 4.5:1
- [ ] All text meets WCAG AA standard minimum

### Color Blindness
Test with simulator: https://www.color-blindness.com/coblis-color-blindness-simulator/

- [ ] Information not lost with deuteranopia (red-green)
- [ ] Key distinctions visible with protanopia
- [ ] Patterns/shapes used in addition to color
- [ ] No critical info conveyed by color alone

### Visual Clarity
- [ ] Clear visual hierarchy (size, weight, position)
- [ ] Logical reading order
- [ ] Grouping of related elements obvious
- [ ] Important info emphasized appropriately

## Peer Review

### 30-Second Test
Show poster to colleague for 30 seconds, then ask:
- [ ] They can identify the research topic
- [ ] They can state the main finding
- [ ] They remember the key figure

### 5-Minute Review
Ask colleague to read poster (5 minutes), then ask:
- [ ] They understand the research question
- [ ] They can explain the approach
- [ ] They can summarize the conclusions
- [ ] They identify what makes it novel/important

### Feedback
- [ ] Noted any confusing elements
- [ ] Identified any unclear figures
- [ ] Checked for jargon that needs definition
- [ ] Verified logical flow

## Pre-Printing Final Checks

### Technical Specifications
- [ ] PDF size exactly matches conference requirements
- [ ] Orientation correct (portrait vs landscape)
- [ ] Color space correct (RGB for screen; ask printer if CMYK required)
- [ ] Resolution adequate (300+ DPI for all images)
- [ ] Bleed area added if required (typically 3-5mm)
- [ ] Crop marks visible if required
- [ ] File naming convention followed

### Printer Communication
- [ ] Confirmed paper type (matte vs glossy)
- [ ] Confirmed poster size
- [ ] Provided color profile if required
- [ ] Verified delivery deadline
- [ ] Confirmed shipping/pickup arrangements
- [ ] Discussed backup plan if issues arise

### Backup and Storage
- [ ] PDF saved with clear filename: `LastName_Conference_Poster.pdf`
- [ ] Source `poster.html` (and any CSS) backed up
- [ ] All figure files backed up
- [ ] Copy saved to cloud storage
- [ ] Copy saved on USB drive for conference
- [ ] Digital version ready to email if requested

## Digital Presentation Checks

If presenting digitally or sharing online:

### File Optimization
- [ ] PDF compressed if >10MB (for email)
- [ ] Test opens in Adobe Reader
- [ ] Test opens in Preview (Mac)
- [ ] Test opens in browser PDF viewers
- [ ] Test on mobile devices

### Interactive Elements
- [ ] All QR codes tested and functional
- [ ] QR codes link to correct URLs
- [ ] Hyperlinks work (if included)
- [ ] Links open in new tabs/windows appropriately

### Alternative Formats
- [ ] PNG version created for social media (if needed)
- [ ] Thumbnail image created
- [ ] Poster description/abstract prepared
- [ ] Hashtags and social media text ready

## Conference-Specific

### Requirements Verification
- [ ] Poster size matches conference specifications exactly
- [ ] Orientation matches requirements
- [ ] File format correct (usually PDF)
- [ ] Submission deadline met
- [ ] File naming convention followed
- [ ] Abstract/description submitted if required

### Physical Preparation
- [ ] Poster printed and inspected
- [ ] Backup printed copy prepared
- [ ] Push pins/mounting materials ready
- [ ] Poster tube or flat portfolio for transport
- [ ] Business cards/handouts prepared
- [ ] Digital backup on laptop/phone

### Presentation Preparation
- [ ] 30-second elevator pitch prepared
- [ ] 2-minute summary prepared
- [ ] 5-minute detailed explanation prepared
- [ ] Anticipated questions considered
- [ ] Follow-up materials ready (QR code to paper, etc.)

## Final Sign-Off

Date: ________________

Poster Title: _______________________________________________

Conference: _______________________________________________

Reviewed by: _______________________________________________

All critical items checked: [ ]

Ready for printing: [ ]

Ready for presentation: [ ]

Notes/Issues to address:
_________________________________________________________
_________________________________________________________
_________________________________________________________

---

## Quick Reference: Common Issues

| Issue | Quick Fix |
|-------|-----------|
| PDF exported at Letter/A4, poster cropped | Add/fix `@page { size: 36in 48in; margin: 0 }` to match the body |
| Backgrounds/gradients missing in PDF | Enable "Background graphics" in print dialog; ensure `print-color-adjust: exact` |
| Header/footer (date, URL) on the PDF | Add `--no-pdf-header-footer` (headless) or uncheck "Headers and footers" in dialog |
| Text too small | Bump the `font-size` values in the template `<style>` |
| Blurry figures | Regenerate at higher resolution (300+ DPI at final size) |
| Content cut off at edges | Reduce sections/word count; check for overflow in the browser at 100% |
| Colors wrong on print | Screen is RGB; ask the print shop whether CMYK conversion is needed |
| QR codes don't scan | Increase size (min 2×2cm), ensure high contrast |
| File too large | Re-export figures as compressed PNG/WebP; downscale oversized images |

## Checklist Version
Version 2.0 - For HTML/CSS posters exported to PDF or converted to PPTX

