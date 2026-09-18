# Reviewing Presentations and Slide Decks

Image-based review workflow and evaluation criteria for scientific presentations
(PowerPoint, Beamer, slide decks). The SKILL.md body routes here when a submission is a
presentation rather than a manuscript.

**⚠️ CRITICAL: For presentations, NEVER read the PDF directly. ALWAYS convert to images first.**

## Mandatory Image-Based Review Workflow

**NEVER attempt to read presentation PDFs directly** - this causes buffer overflow errors and doesn't show visual formatting issues.

**Required Process:**
1. Convert PDF to images using Python:
   ```bash
   python skills/writing-tools/alterlab-scientific-slides/scripts/pdf_to_images.py presentation.pdf review/slide --dpi 150
   # Creates: review/slide-001.jpg, review/slide-002.jpg, etc.
   ```
2. Read and inspect EACH slide image file sequentially
3. Document issues with specific slide numbers
4. Provide feedback on visual formatting and content

## Presentation-Specific Evaluation Criteria

**Visual Design and Readability:**
- [ ] Text is large enough (minimum 18pt, ideally 24pt+ for body text)
- [ ] High contrast between text and background (4.5:1 minimum, 7:1 preferred)
- [ ] Color scheme is professional and colorblind-accessible
- [ ] Consistent visual design across all slides
- [ ] White space is adequate (not cramped)
- [ ] Fonts are clear and professional

**Layout and Formatting (Check EVERY Slide Image):**
- [ ] No text overflow or truncation at slide edges
- [ ] No element overlaps (text over images, overlapping shapes)
- [ ] Titles are consistently positioned
- [ ] Content is properly aligned
- [ ] Bullets and text are not cut off
- [ ] Figures fit within slide boundaries
- [ ] Captions and labels are visible and readable

**Content Quality:**
- [ ] One main idea per slide (not overloaded)
- [ ] Minimal text (3-6 bullets per slide maximum)
- [ ] Bullet points are concise (5-7 words each)
- [ ] Figures are simplified and clear (not copy-pasted from papers)
- [ ] Data visualizations have large, readable labels
- [ ] Citations are present and properly formatted
- [ ] Results/data slides dominate the presentation (40-50% of content)

**Structure and Flow:**
- [ ] Clear narrative arc (introduction → methods → results → discussion)
- [ ] Logical progression between slides
- [ ] Slide count appropriate for talk duration (~1 slide per minute)
- [ ] Title slide includes authors, affiliation, date
- [ ] Introduction cites relevant background literature (3-5 papers)
- [ ] Discussion cites comparison papers (3-5 papers)
- [ ] Conclusions slide summarizes key findings
- [ ] Acknowledgments/funding slide at end

**Scientific Content:**
- [ ] Research question clearly stated
- [ ] Methods adequately summarized (not excessive detail)
- [ ] Results presented logically with clear visualizations
- [ ] Statistical significance indicated appropriately
- [ ] Conclusions supported by data shown
- [ ] Limitations acknowledged where appropriate
- [ ] Future directions or broader impact discussed

## Common Presentation Issues to Flag

**Critical Issues (Must Fix):**
- Text overflow making content unreadable
- Font sizes too small (<18pt)
- Element overlaps obscuring data
- Insufficient contrast (text hard to read)
- Figures too complex or illegible
- No citations (completely unsupported claims)
- Slide count drastically mismatched to duration

**Major Issues (Should Fix):**
- Inconsistent design across slides
- Too much text (walls of text, not bullets)
- Poorly simplified figures (axis labels too small)
- Cramped layout with insufficient white space
- Missing key structural elements (no conclusion slide)
- Poor color choices (not colorblind-safe)
- Minimal results content (<30% of slides)

**Minor Issues (Suggestions for Improvement):**
- Could use more visuals/diagrams
- Some slides slightly text-heavy
- Minor alignment inconsistencies
- Could benefit from more white space
- Additional citations would strengthen claims
- Color scheme could be more modern

## Review Report Format for Presentations

**Summary Statement:**
- Overall impression of presentation quality
- Appropriateness for target audience and duration
- Key strengths (visual design, content, clarity)
- Key weaknesses (formatting issues, content gaps)
- Recommendation (ready to present, minor revisions, major revisions)

**Layout and Formatting Issues (By Slide Number):**
```
Slide 3: Text overflow - bullet point 4 extends beyond right margin
Slide 7: Element overlap - figure overlaps with caption text
Slide 12: Font size - axis labels too small to read from distance
Slide 18: Alignment - title not centered
```

**Content and Structure Feedback:**
- Adequacy of background context and citations
- Clarity of research question and objectives
- Quality of methods summary
- Effectiveness of results presentation
- Strength of conclusions and implications

**Design and Accessibility:**
- Overall visual appeal and professionalism
- Color contrast and readability
- Colorblind accessibility
- Consistency across slides

**Timing and Scope:**
- Whether slide count matches intended duration
- Appropriate level of detail for talk type
- Balance between sections

**Remember:** For presentations, the visual inspection via images is MANDATORY. Never attempt to read presentation PDFs as text - it will fail and miss all visual formatting issues.
