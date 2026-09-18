# GEO/AEO Optimization: AI Citation Strategies

## Core GEO Research

### Princeton GEO Paper (KDD 2024)
GEO methods boost AI visibility by up to 40%.

| Technique | Improvement |
|-----------|-------------|
| Citing authoritative sources | +115.1% visibility (5th-ranked sites, main experiment) |
| Quotation addition | +28% (main experiment); +37% (Perplexity.ai validation, Table 7) |
| Statistics addition | +41% (main experiment); +22% (Perplexity.ai validation, Table 7) |
| FAQ schema | +28% (sponsored article on SEL; not editorial research) |

Traditional keyword stuffing performs **worse than baseline** in generative engines.

### Cross-Platform Citation Divergence

- Only 11% of domains are cited by both ChatGPT and Perplexity (Digital Bloom, 2025;
  domain-level, not URL-level; AI Overviews not included in that study)
- 80% of LLM citations don't rank in Google's top 100 (Ahrefs, Aug 2025) - traditional
  SEO rankings are a poor predictor of AI citation
- Brands are 6.5x more likely to be cited through third-party sources than their own
  domains (AirOps, Oct 2025) - earned media dominates AI visibility

### Kevin Indig's AI Search Pipeline (Jan 5, 2026)
Three critical stages:

1. **Retrieval**: Which pages enter the candidate set
   - Server response time under 200ms TTFB
   - Metadata relevance
   - Content must be in HTML (not behind JS)
2. **Citation**: Which sources get mentioned
   - Content freshness dominates (70%+ cited pages updated within 12 months)
   - Content within 3 months performs best
3. **Trust**: Which citations users click
   - Brand recognition
   - Source authority

## Content Format Impact on Citations

| Format | Impact | Source |
|--------|--------|--------|
| Listicles | 50% of top AI citations (Onely/nobori.ai; Wix/Peec 75K-answer study found 21.9%) |
| Tables/structured data | 2.5x more citations (Onely citing Averi AI) |
| Long-form (2,000+ words) | ~3x more citations (Moz 2025 found 3.2x; SE Ranking found 1.6x) |
| FAQ schema | +28% (sponsored SEL article, not editorial research) |
| Content with statistics | +40% higher citation rates | Onely |
| Sections of 120-180 words between headings | 70% more ChatGPT citations | SE Ranking, Nov 2025 |
| Comparison tables with `<thead>` | 47% higher AI citation rates (SEL; primary source unlocatable) |

## Platform-Specific Citation Patterns

Each AI platform has distinct content preferences:

| Platform | Favored Content Type | Key Bias |
|----------|---------------------|----------|
| ChatGPT | "Best X" listicles | 43.8% of citations are list-format content |
| Perplexity | Reddit discussions | 6.6% of all citations come from Reddit |
| AI Overviews | Google properties | 23% of citations favor Google-owned sources |

**Perplexity content decay**: Citation relevance begins declining 2-3 days
post-publication - Perplexity heavily weights recency, making it the most
freshness-dependent platform. Content older than 1 week sees sharp citation drops.

## Content Freshness Requirements

- 76.4% of ChatGPT's most-cited pages updated within 30 days (Ahrefs, ~17M citations)
- URLs cited in AI results are 25.7% fresher than traditional search
- Content < 3 months old is 3x more likely to get cited
- **Action**: Update critical content quarterly with at least 30% changes

## Off-Site Signals (Dominate AI Visibility)

### Ahrefs Study (Dec 2025, 75,000 brands)

| Factor | Correlation with AI Visibility |
|--------|-------------------------------|
| YouTube mentions | 0.737 (strongest) |
| Branded web mentions | 0.656-0.709 |
| Domain Rating | 0.266-0.326 |
| Backlinks | 0.218 (dramatically weaker than expected) |

### Platform-Specific Citation Rates

**YouTube**:
- Citations in AI Overviews up 414% (Q1 2025, NP Digital, 10K+ AIO analysis)
- How-to videos up 651%
- Visual demos up 592%
- 200x more cited than any other video platform
- Optimization: keywords in titles/transcripts, Q&A-style, 10+ min, public transcripts

**Reddit**:
- Citations surged 1.30% → 7.15% (450% growth)
- Google's $60M annual API deal
- 2.2-21% of AI Overview citations by query type
- Strategy: Authentic participation in 3-5 subreddits BEFORE any promotional content

**Review Platforms (B2B)**:
- G2 accounts for 22-23% of review-platform citations (Radix via G2's own blog;
  self-reported - Hall.com's independent analysis found G2 at only 8.25% of B2B
  software citations in ChatGPT)
- 33% of review citations come from G2 (Profound via G2's blog; treat as directional)
- Multi-platform presence: 4.6-6.3 citations vs 1.8 without (2.6-3.5x multiplier)

**Wikipedia/Wikidata**:
- 7.8% of all ChatGPT citations (Profound)
- Used as "credibility tiebreaker" when sources conflict

### Budget Allocation
Recommended: **40% owned content / 60% earned media**
(Most companies allocate 90/10 - this is wrong for GEO)

88-92% of AI citations come from off-site signals, not on-page optimization alone.

## AI Crawler Technical Requirements

| Crawler | JavaScript Rendering |
|---------|---------------------|
| GPTBot (OpenAI) | No |
| ChatGPT-User | No |
| ClaudeBot | No |
| PerplexityBot | No |
| Googlebot | Yes |
| Google-Extended | Yes |

**Critical**: Content behind JavaScript is invisible to ChatGPT, Claude, Perplexity.
Use SSR, SSG, or ISR. Test by disabling JS and reloading.

### AI Crawler Traffic Growth

- Cloudflare AI crawling rose 32% YoY across all monitored sites
- GPTBot traffic grew 305% YoY
- PerplexityBot traffic grew 157,490% YoY (from near-zero baseline)
- 65% of AI bot hits target content published within the past year (Seer Interactive)
  - freshness is a retrieval signal, not just a citation signal

### Performance Requirements for AI Retrieval
- Server response time under 200ms TTFB (Kevin Indig pipeline)
- Maximum 600ms TTFB before AI crawlers time out and skip the page
- Crawlers implement 3-5 second hard timeouts (Getpassionfruit)
- Core Web Vitals are a constraint, not a growth lever - good CWV doesn't reliably
  outperform, but severe LCP failure creates disadvantage (Search Engine Land, 107,352 pages)
- Top 10 domains capture 46% of all ChatGPT citations per topic (Growth Memo, Mar 2026)
- Slow pages are excluded from AI citation candidate pools entirely
- Vercel analysis of 500+ million GPTBot fetches found zero evidence of JS execution

### robots.txt for AI Visibility
```
User-agent: GPTBot
Allow: /
User-agent: ChatGPT-User
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: PerplexityBot
Allow: /
```

### llms.txt Standard
Markdown file at site root helping LLMs understand content at inference time.
Keep under 10KB, plain URLs with brief comments.

## Attribution Gaps

Perplexity visits ~10 pages per query but cites only 3-4. Not all AI responses
include citations - optimizing for retrieval is critical. Content must enter the
candidate set before citation is possible.

## GEO Case Study Results

| Company | Results | Timeframe |
|---------|---------|-----------|
| Go Fish Digital | +43% AI traffic, +83% conversions, 25x conversion rate | 3 months |
| Netpeak USA | +120% revenue, +693% AI visits | Ongoing |
| Nine Peaks Media | 36% visibility improvement, first ChatGPT citations | Ongoing |
| ABM Agency/Chemours | 82% ChatGPT mention rate, $90M+ pipeline | Ongoing |
| Smart Rent | 32% SQL increase, 40% faster pipeline | Ongoing |

## Entity-First SEO

Every page should unambiguously represent ONE canonical entity.
Google Knowledge Graph: 800B facts about 8B entities.

Entity building timeline (3-6 months):
1. Create entity map with Wikidata Q-IDs
2. Establish Wikipedia/Wikidata presence
3. Build entity consistency across all platforms (exact same name)
4. Practice "controlled co-occurrence" via third-party mentions
5. Earn external citations from recognized publications

## Readability-GEO Connection

Readability directly impacts AI citation rates. Content in the Flesch 60-75
band receives significantly more AI citations across all major platforms.

### Flesch Score & AI Citation Rates
- **Flesch 60-75 = 31% more AI citations** (Spotlight, 18,000 monitored prompts;
  self-reported internal data from a commercial platform, no independent verification)
- Teams improving Flesch from 52→68 saw parallel citation lifts within two
  crawl windows
- Content that is too complex (Flesch <50) or too simple (Flesch >80) gets
  fewer citations - AI systems prefer fluent, authoritative writing

### Citation Position Bias
- **44.2% of all LLM citations come from the first 30% of text** (Growth Memo,
  Feb 2026, Kevin Indig). Answer-first formatting is critical for citation capture.
- Direct answers in the first 1-2 sentences of each section maximize
  extractability for AI systems

### GEO Tactic Combinations
Princeton GEO paper (KDD 2024) findings on readability-related tactics:
- **Fluency optimization** = 15-30% visibility boost
- **Statistics addition** = up to 41% visibility boost
- **Fluency + Statistics combined** outperforms any single tactic by 5.5%
- Keyword stuffing performs -10% WORSE than baseline

**FLOW evidence triple is mandatory for AI-citation readiness.** AI assistants extract claims that have year anchor in prose, inline publisher + title, and URL with retrieval date. Stats without the triple are less likely to surface in citations. See `flow-alignment.md`.

### Schema & Structure for AI Citation
- Comparison tables with proper HTML (`<thead>`, `<tbody>`) = **47% higher**
  AI citation rates (attributed to SEL; primary source unlocatable - treat as directional)
- SearchVIU confirmed ChatGPT, Claude, Perplexity, and Gemini all process
  Schema Markup during citation selection

### Platform-Specific Citation Behaviors
| Platform | Key Behavior | Readability Preference |
|----------|-------------|----------------------|
| ChatGPT | Wikipedia = 7.8% of citations; SearchGPT: 87% match Bing top 10 | Prefers well-structured, fluent content |
| Perplexity | Reddit = 46.7% of top-10 sources; strongest depth correlation (0.191) | 2-3 day content decay; heavily weights recency |
| AI Overviews | 93.67% from top-10 organic; avg 10.2 links per response | Prefers established authority + clear answers |

Only 11% of domains are cited by both ChatGPT and Perplexity (Digital Bloom). Only 12%
of URLs cited by ChatGPT, Perplexity, and Copilot rank in Google's top 10 (Ahrefs).

### Content Freshness for AI Citation
- **65%** of AI bot hits target content published within the past year (Seer Interactive)
- **85%** of AI Overview citations come from content <2 years old
- **44%** of AI Overview citations come from 2025 content specifically
- **50%** of Perplexity citations come from 2025 alone
- Content older than 3 months sees 3x fewer citations
