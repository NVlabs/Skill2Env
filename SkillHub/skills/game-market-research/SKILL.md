---
name: "game-market-research"
description: >
  Conduct market research for a game concept -- competitive landscape, market sizing,
  audience analysis, trend detection, and positioning strategy. Triggers on: "market
  research", "competitive analysis", "market sizing", "audience analysis", "is this game
  viable", "similar games", "market validation". Do NOT invoke for brainstorming ideas
  (use game-brainstorm) or economy monetization design (use game-economy-designer). Part
  of the AlterLab GameForge collection.
argument-hint: "[game-concept or genre]"
effort: medium
context: fork
allowed-tools: Read, Glob, Grep, Write, WebSearch, WebFetch
version: 1.3.0
---

# AlterLab GameForge -- Market Research Workflow

Making a game nobody wants to play is easy. Making a game that finds its audience requires
understanding where that audience lives, what they are already playing, what they wish
existed, and how saturated the space is. Market research for games is not about copying
what sells -- it is about finding the gap between what players want and what currently
exists, then positioning your game to fill that gap.

The indie games that succeed commercially almost always have a clear answer to "who is this
for and why would they choose this over the alternatives?" Hollow Knight launched into a
crowded Metroidvania market but differentiated on atmosphere, difficulty curve, and sheer
content density. Vampire Survivors created an entirely new micro-genre by stripping the
bullet-hell formula down to its most addictive core. Balatro took the poker roguelike concept
that nobody knew they wanted and executed it with such precision that it outsold games with
100x the budget.

None of these were accidents. Each team understood their market position, even if
informally. This workflow makes that understanding systematic.

### Purpose and Triggers

Use this workflow when:
- A developer has a game concept and wants to validate its market viability
- A team is choosing between multiple game concepts and needs data to decide
- A studio wants to understand the competitive landscape before committing to production
- A solo dev wants to know if their niche has an audience large enough to sustain them
- After `game-brainstorm` produces a concept and before `game-start` commits to building it
- A game is approaching launch and needs positioning against current competitors

Problems this solves:
- Building a game in an oversaturated genre without differentiation
- Underestimating or overestimating the target audience size
- Missing competitor moves that change the market during development
- Pricing the game incorrectly for the genre and audience expectations
- Launching without a clear positioning statement for store pages and marketing
- Spending 2+ years on a game concept that has no viable commercial audience

### Critical Rules

1. **Research is not validation bias.** The goal is to find the truth about the market, not
   to confirm that the developer's idea is brilliant. If the research reveals a saturated
   market or a tiny audience, that is a valuable finding -- not a failure of the research.

2. **Quantitative where possible.** Steam revenue estimates, player counts, wishlists,
   review volumes, and similar games' performance data are more useful than subjective
   market assessments. Use tools like SteamDB, itch.io trending, and App Store charts
   to ground the analysis in numbers.

3. **Recency matters.** A genre that was hot 3 years ago may be oversaturated now. A genre
   that was dead 3 years ago may be experiencing a revival. Always check the publication
   dates of market data and prioritize data from the last 12 months.

4. **Indie scale, not AAA scale.** Market sizing for a solo dev making a $15 game is
   fundamentally different from market sizing for a 200-person studio making a $70 game.
   Always contextualize findings to the team's actual scale, budget, and timeline.

5. **Positioning is not features.** A game's market position is defined by what it does
   differently, not by what it does at all. "A Metroidvania with combat" is not
   positioning. "A Metroidvania where every ability is a musical instrument" is positioning.

### Workflow

---

**Phase 1: Genre Analysis**

Define the genre space and its current state.

Questions to answer:
- What genre(s) does this game concept belong to? (Primary and secondary)
- What are the defining characteristics of this genre that players expect?
- What is the genre's current lifecycle stage? (Emerging, growing, mature, oversaturated)
- What sub-genres or hybrid genres exist within this space?
- What was the last major commercial success in this genre? How recent was it?

Research methodology:
- Search for "[genre] games [current year]" to find recent releases
- Check Steam tag pages for the relevant genre tags -- note total game counts
- Look at itch.io genre categories for indie-specific saturation data
- Review recent gaming press coverage: is this genre being talked about?
- Check YouTube and Twitch viewership for the genre: are people watching?

Output:
```
GENRE ANALYSIS
---------------------------------------------------------------
Primary genre: [genre]
Secondary genre(s): [genre, genre]
Lifecycle stage: [emerging | growing | mature | oversaturated]
Key genre expectations: [what players assume the game will have]
Recent notable releases: [game (year), game (year), game (year)]
Genre health signals: [viewer interest, press coverage, release volume]
---------------------------------------------------------------
```

---

**Phase 2: Competitive Landscape**

Map the competitive field using three tiers of competitors.

**Direct competitors** -- Games in the same genre targeting the same audience with similar
mechanics and price points. These are the games your potential players are already playing
or considering. A direct competitor to a cozy farming sim is another cozy farming sim.

**Indirect competitors** -- Games that satisfy the same player need through different
mechanics or genres. An indirect competitor to a cozy farming sim might be a cozy life
sim or a relaxing crafting game. These compete for the same emotional niche.

**Aspirational competitors** -- Games that achieved the quality bar or market position
you are aiming for, even if they are not in the same genre. These set the benchmark for
execution quality and help calibrate expectations.

For each competitor, analyze:

```
COMPETITOR ANALYSIS
---------------------------------------------------------------
Game: [name]
Type: [direct | indirect | aspirational]
Platform: [Steam, console, mobile, etc.]
Price: [$]
Release date: [date]
Review score: [Steam %, Metacritic, etc.]
Review volume: [total reviews — proxy for sales]
Estimated revenue: [use SteamDB estimates or review-to-sales multipliers]
Differentiator: [what makes this game stand out in the market]
Weakness: [what players commonly criticize]
Relevance: [why this game matters for your positioning]
---------------------------------------------------------------
```

Analyze at least:
- 3-5 direct competitors
- 2-3 indirect competitors
- 1-2 aspirational competitors

Reference `@templates/competitive-analysis.md` for the full competitive analysis template.

---

**Phase 3: Market Sizing**

Estimate the addressable market for the game concept.

**Total Addressable Market (TAM):** All players who play games in this genre on any
platform. Use Steam tag player estimates, mobile download data, and console install bases.

**Serviceable Addressable Market (SAM):** Players who play this genre on the platforms
you are targeting, at your price point, in your supported languages. This is TAM minus
the players you cannot reach.

**Serviceable Obtainable Market (SOM):** The realistic subset of SAM you can capture
given your marketing budget, launch visibility, and competitive positioning. For most
indie games, this is 0.1-1% of SAM in the first year.

Estimation methods:
- **Review multiplier method:** Steam reviews x 30-80 (varies by genre and price) gives
  approximate unit sales. Apply this to similar games to estimate genre demand.
- **Wishlist conversion method:** If you have wishlist data, typical conversion rates
  are 10-20% within the first week of launch.
- **Comparable title method:** Find 3-5 games most similar to yours. Average their
  estimated sales. Discount by 50% for a conservative estimate (survivorship bias).

Output:
```
MARKET SIZING
---------------------------------------------------------------
TAM: [estimate] players across all platforms
SAM: [estimate] players on target platforms at target price
SOM: [estimate] realistic year-1 capture
Revenue estimate (conservative): SOM x price x 0.7 (platform cut)
Revenue estimate (moderate): SOM x 1.5 x price x 0.7
Break-even requirement: [units at price point after platform cut]
Comparable titles' performance:
  - [game]: [estimated units] at [$price]
  - [game]: [estimated units] at [$price]
  - [game]: [estimated units] at [$price]
---------------------------------------------------------------
```

---

**Phase 4: Audience Profiling**

Define who the target player is with enough specificity to guide design and marketing
decisions.

**Demographics:** Age range, platform preference, spending habits, session length
expectations. Use Steam hardware survey data, platform demographics reports, and genre
community analysis.

**Psychographics (using Bartle's taxonomy and motivational frameworks):**
- What player motivations does this game serve? (Achievement, exploration, social,
  competition, creativity, relaxation)
- Reference `@docs/game-design-theory.md` for Bartle taxonomy and SDT framework
- What emotional state are players seeking? (Thrill, calm, mastery, wonder, connection)

**Behavioral patterns:**
- Where does this audience discover new games? (Steam browse, YouTube, TikTok, Reddit,
  Discord, word-of-mouth, streamers)
- What influences their purchase decision? (Reviews, trailers, demos, price, streamer
  coverage, friend recommendations)
- What is their tolerance for early access, bugs, and incomplete content?
- How long do they typically engage with a game in this genre?

**Community signals:**
- Are there active subreddits, Discord servers, or forums for this genre?
- What do players in those communities say they want but cannot find?
- What are the most common complaints about existing games in the genre?

Output:
```
AUDIENCE PROFILE
---------------------------------------------------------------
Primary audience: [description in 1-2 sentences]
Age range: [range]
Platform preference: [platforms in order]
Session length: [typical session]
Motivations: [Bartle type(s) + emotional needs]
Discovery channels: [where they find new games]
Purchase drivers: [what convinces them to buy]
Community hubs: [where they gather online]
Unmet needs: [what they want but current games don't provide]
---------------------------------------------------------------
```

---

**Phase 5: Trend Detection**

Identify market trends that will affect the game during its development and launch window.

**Genre trends:**
- Is this genre growing or contracting? What is the trajectory?
- Are there emerging sub-genres or hybrid genres forming?
- What mechanics or themes are gaining traction?

**Platform trends:**
- Is the target platform growing or stable?
- Are there platform-specific opportunities (Steam Deck portability, mobile cross-play)?
- Are platform policies changing in ways that affect this game?

**Technology trends:**
- Are there new tools or engines making this genre easier to develop?
- Are AI-generated content tools changing player expectations?
- Are there hardware trends that affect the game (VR adoption, haptic feedback)?

**Cultural trends:**
- Are there cultural moments that could boost or harm this genre?
- Is there media (movies, TV, books) creating interest in related themes?
- Are there political or social sensitivities that affect the game's theme?

**Timing analysis:**
- What games are launching in the same window? (Check Steam upcoming releases)
- Are there major platform sales events to align with or avoid?
- Is there a seasonal pattern for this genre? (e.g., cozy games peak in Q4)

---

**Phase 6: Positioning Strategy**

Synthesize all previous phases into a clear market positioning statement and strategy.

**Positioning statement format:**
```
For [target audience] who want [core need/desire],
[game name] is a [genre] that [unique value proposition].
Unlike [primary competitor], it [key differentiator].
```

**Positioning validation checklist:**
- Does the positioning statement pass the "so what?" test? Would a player care?
- Is the differentiator real and defensible, or is it a feature that competitors could
  easily add?
- Does the positioning align with the game's design pillars?
- Can the positioning be communicated in a single store page screenshot?
- Would a streamer be able to explain the positioning in one sentence?

**Pricing strategy:**
- What do direct competitors charge?
- What is the price expectation for this genre and content volume?
- Should the game launch at a discount, full price, or use early access pricing?
- What is the minimum price that sustains development at the estimated SOM?

**Launch window recommendation:**
- Based on competitor release schedules and seasonal patterns
- Avoid launching within 2 weeks of a major competitor
- Consider platform sales calendar (Steam seasonal sales)

### Output Format

The workflow produces a **Market Research Brief** structured as follows:

```markdown
# Market Research Brief: [Game Concept]

**Date:** [date]
**Concept:** [1-2 sentence description]
**Primary genre:** [genre]
**Target platforms:** [platforms]

## Executive Summary
[3-5 sentences: Is this concept viable? What is the opportunity? What are the risks?]

## Genre Analysis
[Phase 1 output]

## Competitive Landscape
### Direct Competitors
[Competitor analyses]
### Indirect Competitors
[Competitor analyses]
### Aspirational Competitors
[Competitor analyses]

## Market Sizing
[Phase 3 output with TAM/SAM/SOM]

## Audience Profile
[Phase 4 output]

## Trend Analysis
[Phase 5 output]

## Positioning Strategy
**Positioning statement:** [formatted statement]
**Key differentiator:** [what makes this game different]
**Pricing recommendation:** [$X based on analysis]
**Launch window recommendation:** [timing]

## Risk Assessment
| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| [market risk] | H/M/L | H/M/L | [plan] |

## Recommendation
[Go / Go with modifications / Pivot / No-go — with supporting rationale]
```

### Quality Criteria

A successful market research brief meets all of these:
- At least 5 direct or indirect competitors analyzed with real data
- Market sizing uses at least one quantitative estimation method
- Audience profile is specific enough to guide marketing decisions
- Positioning statement passes the "so what?" test
- Trend analysis covers the expected development timeline
- The recommendation is honest, even if it is "no-go"
- All data sources are recent (within 12 months where possible)
- The brief is calibrated to indie scale, not AAA assumptions

### Example Use Cases

1. **"I want to make a roguelike deckbuilder. Is the market too crowded?"**
   Full 6-phase analysis focused on saturation risk. Direct competitor analysis
   includes Slay the Spire, Balatro, Inscryption, Monster Train. Market sizing
   reveals a large but increasingly crowded SAM. Positioning must be sharp.

2. **"We're choosing between a farming sim and a horror game. Which is more viable?"**
   Run the workflow twice (abbreviated) for each concept. Compare market sizes,
   competition levels, and development costs. Present a side-by-side comparison
   with a recommendation.

3. **"Our game launches in 3 months. Help us position against competitors."**
   Emphasis on Phase 2 (competitive landscape) and Phase 6 (positioning). Check
   competitor release schedules for the launch window. Produce a positioning
   statement and pricing recommendation.

4. **"I'm a solo dev making a niche game. Is there enough audience?"**
   Market sizing calibrated to solo dev break-even ($20K-50K revenue). Audience
   profiling focused on niche community detection. SOM estimation at indie scale.

5. **"What genres are trending for indie games right now?"**
   Abbreviated workflow focused on Phase 1 (genre analysis) and Phase 5 (trend
   detection). Survey multiple genres rather than deep-diving one. Produce a
   trend report rather than a full market brief.

### Agentic Protocol

- Reference `@docs/game-design-theory.md` for player motivation frameworks
- Reference `@templates/competitive-analysis.md` for competitive analysis template
- Use WebSearch to retrieve current market data, Steam statistics, and press coverage
- Use WebFetch to access store pages, review aggregators, and industry reports
- Store completed research in `design/market-research/`
- When run before `game-start`, pass the positioning statement as context
- When run before `game-brainstorm`, use trend data to inform ideation directions

Part of the AlterLab GameForge -- Indie Game Development Skills suite.
