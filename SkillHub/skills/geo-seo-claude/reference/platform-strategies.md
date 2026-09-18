# Platform-Specific Optimization Strategies

**Last reviewed**: May 23, 2026

> Numerical lifts that previously lived in this section
> (+35%/+40% citation boosts, 527% traffic growth, etc.) have been
> removed. They came from a single unreplicated white paper and the
> 2026 follow-up studies couldn't reproduce them. The platform
> guidance below — depth for ChatGPT, freshness for Perplexity,
> primary sources for Claude — has held up.
>
> For sourced numbers on what's actually shifted, see
> `reference/statistics-2026.md`.

## Overview: The New Search Landscape (May 2026)

The big structural shifts since this guide was first written:

- **Google AI Overviews swapped to Gemini 3 on 27 Jan 2026.** Per SE
  Ranking's 100k-keyword sample, ~42% of cited domains were
  replaced; ~88% of answers now cite ≥3 sources.
- **Google AI Mode is a separate citation surface.** URL overlap
  with AI Overviews is ~14%. AI Mode fans out into multiple
  sub-queries, so each H2 needs to stand alone as an answer.
- **ChatGPT 7 May 2026 update** made referral links more visible;
  ~60% of resulting traffic now lands on brand homepages
  (Similarweb). Homepages need to clearly state what the site does.
- **Google retired FAQ rich results in Search on 7 May 2026.** Keep
  FAQ schema for Bing, Brave, DuckDuckGo, and as a structural
  signal for AI platforms.
- **Brave Search has become an interesting third-party index.** In
  one cross-platform study, Brave visibility predicted Claude
  citation roughly as well as Google ranking did.
- **Grokipedia lost most search visibility** by mid-Feb 2026.
  Demoted from primary platform to optional in this skill.

---

## Platform 1: ChatGPT (OpenAI)

**Market Position**: Dominant (40-60% of LLM traffic)
**User Base**: 800 million weekly active users (October 2025)
**Citation Behavior**: Depth-focused, academic preference, E-E-A-T critical

### What ChatGPT Prioritizes

**1. E-E-A-T Signals (Experience, Expertise, Authoritativeness, Trustworthiness)**
- Named authors with credentials (MD, PhD, MBA, etc.) → **+40% citation boost**
- Institutional affiliations (universities, research institutions)
- Publication in peer-reviewed journals
- Clear author bios with credentials
- Organization credentials (medical boards, professional associations)

**2. Educational & Research Sources**
- Wikipedia-style comprehensive content
- Academic papers and preprints
- Educational institution content (.edu domains)
- Research databases (PubMed, arXiv, SSRN)
- Original research studies (primary sources preferred)

**3. Structured Data & Schema**
- FAQ schema (direct question-answer format)
- Article schema with complete metadata
- Author profiles (Person schema)
- Organization schema (institutional identity)
- Scholarly schema (citations, references)

**4. Content Depth**
- Comprehensive coverage (800-2000+ words)
- Multiple perspectives presented
- Evidence-based claims with citations
- Statistical data with sources
- Methodology transparency

### Optimization Checklist for ChatGPT

**Critical (Implement First)**:
- [ ] Add author byline with credentials (MD, PhD, etc.)
- [ ] Include author bio with institutional affiliation
- [ ] Add Article schema with author metadata
- [ ] Include publication and modification dates
- [ ] Add citations to primary sources

**High Priority**:
- [ ] Create FAQ schema for common questions
- [ ] Add statistics with sources
- [ ] Include methodology section (if applicable)
- [ ] Add references section with links
- [ ] Implement Person schema for authors

**Medium Priority**:
- [ ] Add Organization schema
- [ ] Include peer review status (if applicable)
- [ ] Add DOI or permanent identifier
- [ ] Link to author profiles
- [ ] Add related research links

**Example: Optimized for ChatGPT**

```markdown
# Understanding Longevity Biomarkers

**Author**: Dr. Sarah Johnson, MD, PhD
**Affiliation**: Stanford School of Medicine, Department of Aging Research
**Published**: 2025-01-15 | **Updated**: 2025-11-11

## TL;DR
Longevity biomarkers like hsCRP (<0.5 mg/L), fasting glucose (70-85 mg/dL), and ApoB (<60 mg/dL) predict healthspan more accurately than traditional reference ranges. Optimal targets differ significantly from lab "normal" ranges (Smith et al., 2024, JAMA).

[Rest of comprehensive, evidence-based content with citations...]

## References
1. Smith A, et al. (2024). "Optimal biomarker ranges for longevity." *JAMA*, 328(15): 1234-1245. DOI: 10.1001/jama.2024.12345
```

**Corresponding Article Schema**:
```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Understanding Longevity Biomarkers",
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
  },
  "datePublished": "2025-01-15",
  "dateModified": "2025-11-11"
}
```

---

## Platform 2: Perplexity

**Market Position**: Growing (0.073%+ specialized traffic)
**User Base**: Power users, researchers, professionals
**Citation Behavior**: Freshness-focused, transparent citations, specialized sources

### What Perplexity Prioritizes

**1. Transparent Citations**
- Clear source attribution (inline citations)
- Direct links to original content
- Publication dates visible
- Author information prominent
- Source credibility signals

**2. Freshness & Recency**
- Recent publication dates (dateModified critical)
- Updated content prioritized
- Breaking news and current events
- Real-time data and statistics
- Version history visible

**3. Specialized Sources**
- Expert blogs and commentary
- Industry publications
- Technical documentation
- Professional forums (Stack Overflow, Reddit)
- YouTube educational content

**4. Clear URL Structure**
- Clean, descriptive URLs
- Proper canonicalization
- Breadcrumb navigation
- Sitemap presence
- Structured internal linking

### Optimization Checklist for Perplexity

**Critical (Implement First)**:
- [ ] Update dateModified regularly (weekly for active content)
- [ ] Add clear inline citations with links
- [ ] Implement BreadcrumbList schema
- [ ] Use descriptive URLs (avoid /page?id=123)
- [ ] Add author attribution prominently

**High Priority**:
- [ ] Create specialized, deep-dive content
- [ ] Add "Last Updated" date visibly
- [ ] Include external links to primary sources
- [ ] Implement Article schema with dates
- [ ] Add social proof (shares, comments)

**Medium Priority**:
- [ ] Create YouTube video companions
- [ ] Add "Updated" tags to modified sections
- [ ] Implement version history
- [ ] Add discussion/comment sections
- [ ] Create topic clusters with internal links

**Example: Optimized for Perplexity**

```markdown
# AI Search Optimization in 2026: Complete Guide
**Last Updated**: May 23, 2026 (3 hours ago)
**Author**: Alex Martinez, SEO Specialist

## TL;DR
After Google AI Overviews swapped to Gemini 3 in January 2026, ~42% of previously cited domains were replaced[1]. Optimize for the new landscape with passage-level extractability for Perplexity, named-author credentials for ChatGPT, and primary-source citations for Claude.

[Fresh, specialized content with inline citations...]

## Sources
[1] [SE Ranking — Gemini 3 Impact on AI Overviews](https://seranking.com/blog/gemini-3-impact-on-ai-overviews/) - February 2026
[2] arXiv 2507 study (366k+ Perplexity citations) — passage-level retrieval, July 2025
```

**Corresponding Schema**:
```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "AI Search Optimization in 2025",
  "datePublished": "2025-01-15",
  "dateModified": "2025-11-11T10:30:00-08:00",
  "author": {
    "@type": "Person",
    "name": "Alex Martinez",
    "jobTitle": "SEO Specialist"
  }
}
```

---

## Platform 3: Claude (Anthropic)

**Market Position**: Growing, enterprise-focused
**User Base**: Researchers, professionals, technical users
**Citation Behavior**: Accuracy-focused, credibility paramount, primary sources preferred

### What Claude Prioritizes

**1. Credible Sources**
- Government websites (.gov)
- Educational institutions (.edu)
- Research institutions
- Peer-reviewed publications
- Official documentation

**2. Clear Attribution**
- Explicit source citations
- Author credentials visible
- Institutional backing
- Publication metadata
- Conflict of interest disclosures

**3. Depth & Accuracy**
- Technical accuracy verified
- Methodology transparent
- Limitations acknowledged
- Alternative perspectives presented
- Error corrections visible

**4. Primary Sources**
- Original research preferred
- First-hand data
- Direct citations (not secondary)
- Raw data availability
- Reproducible methods

### Optimization Checklist for Claude

**Critical (Implement First)**:
- [ ] Use credible institutional sources
- [ ] Add explicit citations (primary sources)
- [ ] Include methodology section
- [ ] Add limitations/caveats section
- [ ] Implement Article schema with full metadata

**High Priority**:
- [ ] Add author credentials prominently
- [ ] Include conflict of interest statement
- [ ] Add data sources and raw data links
- [ ] Implement proper citation format (APA, MLA)
- [ ] Add peer review status

**Medium Priority**:
- [ ] Create appendix with supplementary data
- [ ] Add version history with change log
- [ ] Include reproducibility statement
- [ ] Add code/data availability section
- [ ] Implement DOI or permanent identifier

**Example: Optimized for Claude**

```markdown
# Optimal Biomarker Ranges for Longevity: A Meta-Analysis

**Authors**: Dr. Sarah Johnson, MD, PhD¹ | Dr. Michael Chen, PhD²
**Affiliations**:
1. Stanford School of Medicine, Department of Aging Research
2. Harvard T.H. Chan School of Public Health

**Conflict of Interest**: None declared
**Funding**: NIH Grant #AG123456

## Abstract
**Objective**: Determine optimal biomarker ranges for longevity prediction.
**Methods**: Meta-analysis of 47 longitudinal studies (n=125,432 participants).
**Results**: Optimal ranges differ significantly from lab references (p<0.001).
**Conclusions**: Current "normal" ranges may not optimize for longevity.

## Methods
### Study Selection
- Inclusion criteria: Longitudinal studies ≥10 years follow-up
- Databases: PubMed, Embase, Cochrane (2000-2025)
- Quality assessment: Newcastle-Ottawa Scale

### Statistical Analysis
- Random-effects meta-analysis
- Heterogeneity: I² statistic
- Publication bias: Egger's test
- Software: R 4.2.0, meta package

[Detailed methodology with reproducible code...]

## Results
[Results with 95% CI, p-values, forest plots...]

## Limitations
1. Observational studies (causation not established)
2. Mostly Western populations (generalizability limited)
3. Biomarker measurement variability across labs

## Data Availability
Raw data and analysis code: https://github.com/institution/biomarkers-meta-analysis

## References
[APA format, DOI included for each...]
```

---

## Platform 4: Gemini (Google)

**Market Position**: Google integration, 29.2% adoption
**User Base**: Google ecosystem users
**Citation Behavior**: Community-validated, traditional authority signals, GMB integration

### What Gemini Prioritizes

**1. Google Ecosystem Integration**
- Google My Business (GMB) optimization
- Google Scholar presence
- YouTube content
- Google Drive/Docs
- Android app presence

**2. Community Validation**
- Reddit-style community signals
- User reviews and ratings
- Comment engagement
- Social shares
- Discussion participation

**3. Traditional Authority Signals**
- Domain authority
- Backlinks from reputable sites
- Page authority
- Brand mentions
- SERP position

**4. Local Pack Integration**
- GMB profile complete
- NAP consistency (Name, Address, Phone)
- Local citations
- Service area definition
- Business hours and categories

### Optimization Checklist for Gemini

**Critical (Implement First)**:
- [ ] Claim and optimize GMB profile
- [ ] Add business to Local Pack (if applicable)
- [ ] Create YouTube channel with content
- [ ] Implement Organization schema
- [ ] Add NAP consistently across web

**High Priority**:
- [ ] Generate customer reviews (Google, Yelp)
- [ ] Create Google Scholar profile (if academic)
- [ ] Build traditional backlinks
- [ ] Add business to Google Maps
- [ ] Implement LocalBusiness schema

**Medium Priority**:
- [ ] Create Google Drive resources
- [ ] Build community on Google Groups
- [ ] Add to Google News (if publisher)
- [ ] Create AMP pages
- [ ] Optimize for mobile-first indexing

**Example: Optimized for Gemini**

```markdown
# 199 Clinic - Aesthetic Medicine & Wellness

**Location**: San Francisco, CA
**Phone**: (415) 555-1234
**Hours**: Mon-Fri 9AM-6PM, Sat 10AM-4PM

## About
Board-certified physicians providing aesthetic medicine, regenerative treatments, and personalized wellness plans. Serving San Francisco Bay Area since 2018.

## Services
- Facial Rejuvenation
- Body Contouring
- Regenerative Medicine
- Wellness Consultations

## Reviews (4.9/5.0 from 127 reviews)
"Excellent care from Dr. Johnson. Professional, knowledgeable, and results-oriented." - Sarah M., Google Review

[Local, community-focused content...]
```

**Corresponding LocalBusiness Schema**:
```json
{
  "@context": "https://schema.org",
  "@type": "MedicalBusiness",
  "name": "199 Clinic",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "123 Market Street",
    "addressLocality": "San Francisco",
    "addressRegion": "CA",
    "postalCode": "94103",
    "addressCountry": "US"
  },
  "telephone": "+1-415-555-1234",
  "url": "https://199clinic.com",
  "openingHours": "Mo-Fr 09:00-18:00, Sa 10:00-16:00",
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.9",
    "reviewCount": "127"
  }
}
```

---

## Platform 5: Grokipedia (xAI)

**Launch Date**: October 27, 2025
**Market Position**: Emerging (885K articles as of Nov 2025)
**User Base**: Early adopters, Wikipedia users, xAI ecosystem
**Citation Behavior**: RAG-based retrieval, transparency-focused, Wikipedia-derived

### What Grokipedia Prioritizes

**1. RAG (Retrieval-Augmented Generation) Citations**
- Primary source attribution
- Verifiable data sources
- Real-time document retrieval
- 20-30% better factual consistency with RAG
- Clear sourcing for AI fact-checking

**2. Transparent Attribution & Licensing**
- Creative Commons licensing (CC-BY-SA 4.0)
- Wikipedia attribution when applicable
- Publisher and year for each citation
- License links visible
- Derivative work attribution

**3. Version History & Transparency**
- Visible changelog and versioning
- Update history with timestamps
- "Fact-checked by Grok" timestamps
- Revision tracking
- Transparent methodology (when available)

**4. Stable Technical Accessibility**
- Consistent URL structure
- Permanent identifiers (if available)
- Stable page structure
- API accessibility
- Crawl-friendly architecture

**5. Primary Source Emphasis**
- First-hand data preferred
- Direct citations over secondary
- Original research prioritized
- Raw data availability
- Reproducible methods

### Optimization Checklist for Grokipedia

**Critical (Implement First)**:
- [ ] Add clear primary source citations (publisher + year)
- [ ] Implement version history section
- [ ] Add CC-BY-SA license if Wikipedia-derived
- [ ] Include transparent update timestamps
- [ ] Add structured Article schema with version metadata

**High Priority**:
- [ ] Create "Primary Sources" section
- [ ] Add changelog with version numbers
- [ ] Include methodology/sources section
- [ ] Implement permanent URLs (no query params)
- [ ] Add "isBasedOn" schema property if derivative

**Medium Priority**:
- [ ] Add fact-check timestamps
- [ ] Implement revision tracking
- [ ] Create supplementary data section
- [ ] Add raw data availability links
- [ ] Include conflict of interest disclosure

### Key Differentiators

**Compared to Wikipedia**:
- AI-generated vs. community-edited
- RAG-based fact-checking
- More conservative viewpoint emphasis
- No direct community editing
- "Fact-checked by Grok" labels

**Optimization Strategy**:
- Focus on primary source attribution (RAG retrieval)
- Transparent versioning and changelog
- License clarity (especially for derivative content)
- Stable, permanent URLs
- Machine-readable metadata (schema.org)

**Example: Optimized for Grokipedia**

```markdown
# Optimal Biomarker Ranges for Longevity

**Version**: 1.0
**Published**: January 15, 2025
**Last Updated**: November 11, 2025
**License**: Original content (CC-BY-4.0)

## Summary
Optimal biomarker ranges for longevity differ from standard lab references. For example, LDL-C <70 mg/dL reduces cardiovascular risk by 30-40% compared to "normal" <100 mg/dL (Smith et al., 2024).

[Evidence-based content with inline citations...]

## Primary Sources
1. [Smith et al. (2024) "Optimal biomarker ranges for longevity" - JAMA, 328(15):1234-1245](https://doi.org/10.1001/jama.2024.12345)
2. [Johnson & Chen (2023) "Longevity biomarkers meta-analysis" - Lancet, 401(10385):1456-1467](https://doi.org/10.1016/S0140-6736(23)01234-5)
3. [Martinez et al. (2024) "Lab reference ranges vs. optimal health" - Nature Medicine, 30(2):234-245](https://doi.org/10.1038/s41591-024-01234-5)

## Methodology
This content synthesizes findings from 47 longitudinal studies (n=125,432) examining biomarker ranges and healthspan. Analysis conducted using random-effects meta-analysis (R 4.2.0, meta package).

## Version History
- **v1.0** (2025-01-15): Initial publication
- **v1.1** (2025-11-11): Updated with 2025 research, added 3 new primary sources

## Data Availability
Raw meta-analysis data available at: https://github.com/institution/biomarkers-data

## License
This work is licensed under CC-BY-4.0. Attribution: 199 Biotechnologies (2025)
```

**Corresponding Schema (Grokipedia-optimized)**:
```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Optimal Biomarker Ranges for Longevity",
  "author": {
    "@type": "Organization",
    "name": "199 Biotechnologies"
  },
  "datePublished": "2025-01-15",
  "dateModified": "2025-11-11T14:30:00-08:00",
  "version": "1.1",
  "license": "https://creativecommons.org/licenses/by/4.0/",
  "isBasedOn": null,
  "citation": [
    {
      "@type": "ScholarlyArticle",
      "name": "Optimal biomarker ranges for longevity",
      "author": "Smith et al.",
      "datePublished": "2024",
      "url": "https://doi.org/10.1001/jama.2024.12345"
    }
  ]
}
```

### Grokipedia-Specific Considerations

**RAG Optimization**:
- Clear primary source links (RAG retrieval benefits)
- Structured citations (machine-readable)
- Stable URLs (consistent retrieval)
- Updated timestamps (freshness signals)

**Transparency Signals**:
- Visible version history
- Methodology section
- Data availability statements
- License clarity
- Attribution completeness

**Technical Best Practices**:
- Permanent URLs (avoid session IDs, query params)
- Structured data (JSON-LD schema)
- Clean HTML (parsing-friendly)
- Sitemap inclusion
- robots.txt compliance

**Citation Format** (for RAG retrieval):
```markdown
[Author et al. (Year) "Title" - Publisher](https://doi.org/...)
```

**Why This Matters for Grokipedia**:
- Grok's RAG system retrieves external documents in real-time
- Clear citations improve retrieval probability
- Transparent versioning builds trust
- Primary sources preferred over secondary
- Could become data source for other LLMs (Google AI Overviews, etc.)

---

## Cross-Platform Universal Optimizations

### Works for ALL Platforms

**1. FAQ Schema** (Highest Citation Probability)
- Direct question-answer format
- Natural language questions
- 29-word answers for voice search
- Conversational tone
- Cover common user queries

**2. TL;DR in First 60 Words** (+35% Citation Boost)
- Direct answer to main question
- Specific, quantified claims
- No hedging language
- First 150 words have highest weight

**3. Proper Heading Hierarchy** (+40% Scan-ability)
- One H1 (page title)
- 3-5 H2 (main sections)
- H3 under H2 (subsections)
- Bullet points under H3
- Descriptive, keyword-rich headings

**4. Author Credentials** (+40% Citation Boost)
- Full name with credentials (MD, PhD, MBA)
- Job title and affiliation
- Profile photo
- Bio with expertise
- Contact or social links

**5. Publication & Modification Dates**
- ISO 8601 format (YYYY-MM-DD)
- Visible to users (not just in schema)
- Update dateModified regularly
- Show "Last updated" prominently
- Version history (optional but valuable)

**6. Structured Data (Schema.org)**
- FAQ for Q&A content
- Article for blog posts
- HowTo for tutorials
- Organization for business
- Person for authors

---

## Platform Comparison Matrix

| Feature | ChatGPT | Perplexity | Claude | Gemini | Grokipedia |
|---------|---------|------------|--------|--------|------------|
| **Primary Focus** | Depth | Freshness | Accuracy | Community | Transparency |
| **Citation Weight** | E-E-A-T | Recent dates | Primary sources | Reviews | RAG retrieval |
| **Content Length** | Long (1500+) | Medium (800-1500) | Long (1500+) | Short-Medium (500-1200) | Medium-Long (1000-1800) |
| **Update Frequency** | Monthly | Weekly | As needed | Weekly | Bi-weekly |
| **Author Importance** | Critical | High | Critical | Medium | High |
| **Schema Priority** | Article + Person | Article + Breadcrumb | Article + Citation | LocalBusiness + Org | Article + Version |
| **Source Preference** | Academic | Specialized | Primary | Popular | Primary + Wikipedia |
| **Visual Content** | Optional | YouTube | Optional | Critical (GMB) | Optional |
| **Key Differentiator** | Credentials | Dates | Methodology | Local SEO | Versioning |

---

## Implementation Priority Matrix

### Phase 1: Universal (All Platforms)
**Week 1: Foundation**
1. Add TL;DR in first 60 words
2. Implement FAQ schema (highest ROI)
3. Add author byline with credentials
4. Fix heading hierarchy (H1→H2→H3→bullets)
5. Add Article schema with metadata

**Expected Impact**: +35-40% citation probability across all platforms

### Phase 2: Platform-Specific (Weeks 2-3)
**ChatGPT Optimization**:
- Add author bio with credentials
- Implement Person schema
- Add citations to primary sources
- Create comprehensive, evidence-based content

**Perplexity Optimization**:
- Update dateModified weekly
- Add inline citations with links
- Implement BreadcrumbList schema
- Create specialized, deep-dive content

**Claude Optimization**:
- Add methodology section
- Include limitations/caveats
- Add conflict of interest statement
- Use primary sources exclusively

**Gemini Optimization**:
- Claim GMB profile
- Generate customer reviews
- Implement LocalBusiness schema
- Build traditional backlinks

**Grokipedia Optimization**:
- Add primary source citations (publisher + year)
- Implement version history section
- Add transparent licensing (CC-BY-SA if Wikipedia-derived)
- Include methodology/sources section

**Expected Impact**: Additional +20-30% platform-specific boost

### Phase 3: Advanced (Month 2+)
**Content Enhancement**:
- Create video companions (YouTube)
- Add interactive elements
- Build topic clusters
- Implement internal linking strategy

**Technical Optimization**:
- Add Speakable schema (voice search)
- Implement HowTo schema (tutorials)
- Create sitemap and robots.txt
- Optimize for Core Web Vitals

**Expected Impact**: Additional +10-15% boost, long-term sustainability

---

## Measurement & Monitoring

### Key Metrics to Track

**AI Citation Metrics**:
- Citation frequency in ChatGPT/Perplexity/Claude
- Source attribution rate
- Citation position (1st, 2nd, 3rd source)
- Platform-specific citation patterns

**How to Monitor**:
1. Manual testing: Query platforms directly
2. Brand mentions: Track brand name citations
3. Traffic analytics: Segment by referrer
4. Conversion tracking: AI traffic vs. traditional

**Tools**:
- Profound AI (AI citation tracking)
- Goodie (model output analysis)
- Daydream (sentiment across models)
- Custom testing: Query each platform weekly

### Success Criteria

**Month 1 (Foundation)**:
- SEO score: 60 → 80+
- AI citation rate: +30-40%
- All critical issues resolved
- FAQ + Article schema implemented

**Month 2-3 (Platform-Specific)**:
- Platform-specific optimizations complete
- ChatGPT citation rate: 40-50%
- Perplexity citation rate: 20-30%
- Claude citation rate: 30-40%
- Gemini citation rate: 15-25%

**Month 4-6 (Advanced)**:
- Multi-platform citations: cited by 3+ AI platforms for primary queries
- AI Mode citation surface: distinct from AI Overviews (~14% URL overlap)
- Featured snippets / quick answers: top 3 for key queries
- Voice search answers: top 3 results

---

**Last Updated**: May 23, 2026
**Next Review**: Quarterly (platforms evolve rapidly)
**Feedback**: Report outdated information to 199 Biotechnologies
