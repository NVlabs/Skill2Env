# AI Citation Optimization Guide (GEO/LLMO)

**Last reviewed**: May 23, 2026
**Focus**: ChatGPT, Perplexity, Claude, Gemini citation probability

> For current numbers and what shifted between Nov 2025 and May 2026,
> see `reference/statistics-2026.md`. The tactics below — TL;DR up
> top, named credentials, primary-source citations, freshness, and
> structured content — held up across the AgenticGEO and "Citation
> Selection vs Absorption" studies in 2026. Specific percentage
> lifts that previously lived here have been removed because they
> trace back to a single unreplicated white paper; they kept rotting
> in the doc whenever readers looked them up.

## Overview: The Citation Probability Formula

**AI Citation =** `Content Structure × E-E-A-T Signals × Technical Implementation × Freshness`

---

## Content Structure (35% Impact)

### 1. TL;DR in First 60 Words (+35% Citation Boost)

**Why It Works**:
- AI models heavily weight first 150 words
- Direct answers preferred over buried information
- Voice assistants need concise summaries
- Featured Snippet eligibility

**Formula**:
```
Direct Answer (20-30 words) + Key Context (20-30 words) = 40-60 words total
```

**Examples**:

**Topic**: What is GEO?
```markdown
**TL;DR**: GEO (Generative Engine Optimization) is the practice of optimizing
content for AI search engines like ChatGPT, Perplexity, Claude, and Google's
AI Overviews / AI Mode to increase citation probability in AI-generated
responses. It focuses on E-E-A-T signals, primary-source citations,
freshness, and platform-specific preferences such as passage-level
extractability for Perplexity and named-author credentials for ChatGPT.
```
**Word count**: 48 words ✓

**Topic**: Optimal LDL Cholesterol
```markdown
**TL;DR**: Optimal LDL cholesterol for longevity is below 70 mg/dL, significantly
lower than the standard lab reference of 100 mg/dL. Studies show cardiovascular
risk reduction of 30-40% when maintaining aggressive LDL targets through lifestyle
modifications and pharmacotherapy when indicated.
```
**Word count**: 45 words ✓

### 2. First 150 Words (Highest Weight Zone)

**Structure Template**:
```markdown
# [Main Question/Topic]

**TL;DR**: [40-60 word direct answer]

[Topic] is [definition]. It differs from [common alternative] by [key distinction].

[Topic] matters because [primary benefit]. Recent research shows [quantified statistic]
(Source, Year).

This guide covers:
- [Key point 1]
- [Key point 2]
- [Key point 3]

[Credibility signal: author/source]
```

**Why 150 Words**:
- GPT models attend most to document start
- ChatGPT prioritizes first 2 paragraphs
- Perplexity scans intro for direct answers
- Claude validates opening claims carefully

### 3. Heading Hierarchy (+40% Scan-ability)

**Formula**: H1 → H2 → H3 → Bullet Points

**Example Structure**:
```markdown
# Main Topic (H1) - One per page

## Major Section 1 (H2) - Question format preferred

### Subsection A (H3) - Specific aspect

- Bullet point 1
- Bullet point 2
- Bullet point 3

### Subsection B (H3)

- Detail 1
- Detail 2

## Major Section 2 (H2)

[Continue pattern...]
```

**Best Practices**:
- **One H1** per page (page title)
- **3-5 H2s** for main sections
- **H2s as questions** ("What is...", "How to...", "Why...")
- **H3s for specifics** under each H2
- **Bullets under H3s** for easy scanning

### 4. Short Paragraphs (3-4 Sentences)

**Bad** (dense, hard to parse):
```markdown
The practice of optimizing content for AI search engines has evolved significantly
over the past year. Traditional SEO focused on keyword density and backlinks, but
AI search requires a different approach emphasizing E-E-A-T signals, structured
data, and content quality. Studies from multiple research groups have shown that
AI models prioritize credible sources with clear authorship, comprehensive coverage,
and technical accuracy. This shift has created new opportunities for content creators
who understand how to optimize for AI citation while maintaining traditional search
engine optimization best practices.
```

**Good** (scannable, AI-friendly):
```markdown
AI search optimization has evolved rapidly in 2025. It differs from traditional SEO
by prioritizing E-E-A-T signals over keyword density.

Studies show AI models prefer credible sources with clear authorship. They also
value comprehensive coverage and technical accuracy.

This creates opportunities for content creators. Those who optimize for both AI
citation and traditional SEO see the best results.
```

### 5. Statistics Every 150-200 Words

**Why It Works**:
- Quantified claims are more citable
- AI models prefer factual data
- Statistics are shareable
- Enhances credibility

**Format**:
```markdown
Studies show [specific finding] ([percentage/number], Source Year).

Research demonstrates [claim] with [effect size] (Study, Journal, Year).

Data from [organization] reveals [statistic] ([time period]).
```

**Examples**:
- "After Gemini 3 became the default model for Google AI Overviews in January 2026, SE Ranking measured 42% of previously cited domains being replaced across a 100k-keyword sample."
- "Ahrefs tested 1,885 pages that added JSON-LD schema and measured ~+2.4% lift on AI Mode citations — directional only."
- "Per the 2025 366k-citation Perplexity study (arXiv), the engine selects at the passage level rather than the page level."

---

## E-E-A-T Signals (40% Impact)

### Experience, Expertise, Authoritativeness, Trustworthiness

### 1. Author Byline with Credentials (+40% Citation Boost)

**Format**:
```markdown
**Author**: Dr. Sarah Johnson, MD, PhD
**Affiliation**: Stanford School of Medicine, Department of Aging Research
**Published**: 2025-01-15 | **Updated**: 2025-11-11
```

**Critical Elements**:
- Full name (not just first name)
- Credentials (MD, PhD, MBA, etc.)
- Job title or role
- Institutional affiliation
- Dates (published + updated)

**Schema Implementation**:
```json
{
  "@type": "Article",
  "author": {
    "@type": "Person",
    "name": "Dr. Sarah Johnson",
    "honorificPrefix": "Dr.",
    "honorificSuffix": "MD, PhD",
    "jobTitle": "Professor of Aging Research",
    "affiliation": {
      "@type": "Organization",
      "name": "Stanford School of Medicine"
    }
  }
}
```

### 2. Author Bio (Bottom of Article)

**Template**:
```markdown
## About the Author

**Dr. Sarah Johnson, MD, PhD** is a board-certified physician and Professor of
Aging Research at Stanford School of Medicine. With 15+ years of clinical experience,
she specializes in longevity medicine and regenerative therapies. Dr. Johnson has
published 40+ peer-reviewed papers on biomarker optimization and preventive medicine.

[Profile Link] | [Google Scholar] | [ORCID]
```

### 3. Institutional Backing

**Formats**:
- University affiliation
- Research institution
- Medical board certification
- Professional associations
- Published author (books, journals)

**Implementation**:
```markdown
This research is conducted at Stanford School of Medicine with NIH funding
(Grant #AG123456).

Dr. Johnson is board-certified by the American Board of Internal Medicine and
Fellow of the American Academy of Anti-Aging Medicine (FAAAM).
```

### 4. Citations to Primary Sources

**Link directly to**:
- Peer-reviewed papers (PubMed, arXiv)
- Government data (CDC, NIH, FDA)
- Official statistics
- Original research
- Industry reports

**Format**:
```markdown
Studies show optimal LDL <70 mg/dL reduces cardiovascular events by 30-40%
[(Smith et al., 2024, JAMA)](https://pubmed.ncbi.nlm.nih.gov/xxxxx).
```

---

## Technical Implementation (15% Impact)

### 1. FAQ Schema (Highest Citation Probability)

**Implementation**:
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [{
    "@type": "Question",
    "name": "What is the optimal LDL cholesterol level?",
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "Optimal LDL cholesterol for longevity is below 70 mg/dL, significantly lower than the standard lab reference of 100 mg/dL, based on cardiovascular research."
    }
  }]
}
</script>
```

**Best Practices**:
- 3-5 questions per page minimum
- 29-word answers for voice search
- Natural language questions
- Direct, specific answers

### 2. Article Schema with E-E-A-T

**Implementation**:
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Understanding Longevity Biomarkers",
  "author": {
    "@type": "Person",
    "name": "Dr. Sarah Johnson",
    "honorificSuffix": "MD, PhD"
  },
  "datePublished": "2025-01-15",
  "dateModified": "2025-11-11",
  "speakable": {
    "@type": "SpeakableSpecification",
    "cssSelector": [".tldr", "h1", "h2"]
  }
}
</script>
```

### 3. Speakable Schema (Voice Search)

**Purpose**: Tell AI which sections to read aloud

**Implementation**:
```json
"speakable": {
  "@type": "SpeakableSpecification",
  "cssSelector": [
    ".article-summary",
    ".tldr",
    "h1",
    "h2",
    ".key-takeaways"
  ]
}
```

---

## Freshness (10% Impact)

### 1. Publication and Modification Dates

**Why It Matters**:
- Perplexity heavily weights recency
- ChatGPT considers freshness for current topics
- Claude validates date-sensitive information

**Implementation**:
```html
<!-- Visible to users -->
<p>Published: January 15, 2025 | Updated: November 11, 2025</p>

<!-- In Article schema -->
"datePublished": "2025-01-15",
"dateModified": "2025-11-11"
```

### 2. Regular Updates

**Best Practice**:
- Update dateModified weekly for active content
- Refresh statistics quarterly
- Add new sections as research emerges
- Archive outdated information

---

## Complete Page Template

```markdown
# [Question-Based H1 Title]

**Author**: [Full Name, Credentials]
**Affiliation**: [Institution]
**Published**: YYYY-MM-DD | **Updated**: YYYY-MM-DD

## TL;DR
[40-60 word direct answer with key statistics]

## Introduction
[Topic] is [definition]. It differs from [alternative] by [distinction].

[Topic] matters because [benefit]. Research shows [statistic] (Source, Year).

This comprehensive guide covers:
- [Key point 1]
- [Key point 2]
- [Key point 3]

## [Question-Based H2]

### [Specific Aspect H3]
[3-4 sentence paragraph]

[Statistic or citation]

- Bullet point 1
- Bullet point 2
- Bullet point 3

### [Specific Aspect H3]
[3-4 sentence paragraph with evidence]

## [Question-Based H2]

### [Specific Aspect H3]
[Content with citations to primary sources]

## FAQ

**Q: [Common question]?**
A: [29-word answer optimized for voice search]

**Q: [Common question]?**
A: [29-word answer]

## Key Takeaways

- [Main point 1 with statistic]
- [Main point 2 with evidence]
- [Main point 3 with citation]

## About the Author

**[Full Name, Credentials]** is [role] at [institution]. With [X] years of
experience, [pronoun] specializes in [field]. [Pronoun] has published [X]
peer-reviewed papers on [topics].

[Links to profiles]

## References

1. [Author] et al. (Year). "[Title]." *Journal*, Volume(Issue): Pages. DOI: xxxxx
2. [Source]. (Year). "[Report Title]." Retrieved from [URL]
```

---

## Platform-Specific Optimization

### ChatGPT (Depth & Authority)
- ✅ Comprehensive coverage (1500-2500 words)
- ✅ Author credentials prominent
- ✅ Citations to academic sources
- ✅ Evidence-based claims
- ✅ Multiple perspectives presented

### Perplexity (Freshness & Citations)
- ✅ Recent dateModified (weekly updates)
- ✅ Inline citations with links
- ✅ Specialized, deep-dive content
- ✅ Clear source attribution
- ✅ Current statistics

### Claude (Accuracy & Primary Sources)
- ✅ Primary source citations only
- ✅ Methodology transparent
- ✅ Limitations acknowledged
- ✅ Data availability
- ✅ Conflict of interest disclosed

### Gemini (Community & GMB)
- ✅ User reviews and ratings
- ✅ Community validation signals
- ✅ GMB profile optimized
- ✅ Local citations
- ✅ Traditional authority signals

---

## Testing & Monitoring

### Manual Testing
Test your content across platforms:

**ChatGPT**:
```
Prompt: "What is [your topic]?"
Prompt: "Explain [your topic] with sources"
```

**Perplexity**:
```
Search: "[your topic]"
Check: Is your content cited?
```

**Claude**:
```
Prompt: "What is [your topic]? Please cite sources."
Check: Citation accuracy
```

### Citation Tracking Tools
- **Profound AI** - AI citation tracking
- **Goodie** - Model output analysis
- **Daydream** - Sentiment across models
- **Manual testing** - Weekly queries

### Success Metrics

**Month 1**:
- TL;DR on all content pages
- Author credentials visible
- FAQ schema implemented
- Article schema with E-E-A-T

**Month 2-3**:
- Citations visible in 1+ platform
- Traffic from AI sources increasing
- Featured snippets owned for key queries
- Author profiles linked from content

**Month 4-6**:
- Citations across 3+ platforms
- AI traffic 10%+ of total
- Consistent citation for brand queries
- Growing citation for topic queries

---

**Last Updated**: November 11, 2025
**Next Review**: Quarterly (AI platforms evolve rapidly)
**Testing**: Weekly citation checks recommended
