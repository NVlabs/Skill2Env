# Phase Classification Tree

Most SEOs skip phase classification entirely and just run the same playbook on every site. That's why Authority-phase sites get told to "submit to 50 directories" and brand-new sites get told to "build strategic partnerships". Phase matters because tactic selection depends on it, and you don't need a paid backlink tool to classify correctly.

This is a decision tree built on observable signals. Every signal is free to check.

## Signals to check (in order)

### 1. Site age

The single most important signal. Check two ways:

- **WHOIS lookup**: domain registration date via who.is, whois.com, or ICANN lookup.
- **Wayback Machine first snapshot**: `web.archive.org/web/*/domain.com`. The first snapshot date is when the site was first publicly crawlable, which is often more meaningful than the registration date.

Use the earlier of the two. Map: **< 12 months** = Foundation, **12-36 months** = Growth, **36+ months** = Authority.

### 2. Indexed page count

Run `site:domain.com` in Google. Google's count is intentionally imprecise but the order of magnitude is what matters. Map: **< 20** = Foundation, **20-500** = Growth, **500+** = Authority.

Caveat: programmatic SEO sites can have 10,000+ indexed pages while still being Foundation phase in every other way. If indexed count contradicts the other signals, trust the others.

### 3. Brand knowledge panel

Search the brand name in Google. Look at the right rail on desktop.

- **No panel at all**: Foundation
- **Small "company info" card** (logo, one-line description): Growth
- **Full knowledge panel** (photos, social profiles, founding date, Wikipedia link): Authority

A full knowledge panel means Google's Knowledge Graph has the brand as a recognized entity with corroborating sources. That takes years to build.

### 4. News and media mentions

Search the brand name in Google News. Past 12 months: **Zero** = Foundation, **1-5 sporadic** = Growth, **Regular coverage** in industry or mainstream media = Authority. Don't count press release syndication (PRWeb, EIN Newswire). Those are paid placements and don't indicate earned coverage.

### 5. Social profile consistency

Check LinkedIn, Twitter/X, Instagram, and YouTube. Each profile should exist, be active (posted in last 90 days), use consistent branding, and cross-link from the main site.

- **0-2 active profiles**: Foundation
- **3-4 active with partial consistency**: Growth
- **All major platforms active, cross-linked, with real followings**: Authority

Entity recognition leans heavily on `sameAs` cross-linking. Active profiles without cross-linking is still below Authority.

### 6. Domain Rating (optional)

Only use if the data is already available from Ahrefs, Moz, or Semrush. **DR 0-15** = Foundation, **DR 16-40** = Growth, **DR 41+** = Authority. Don't pay for a tool just to classify.

## The decision tree

Score the signals. Most sites fall into a clean bucket.

**Foundation phase**: < 12 months old, < 100 indexed pages, no knowledge panel, no news mentions, fragmented social presence, typical DR 0-15.

**Growth phase**: 12-36 months, 100-500 pages, small company card in search, some niche news mentions, multiple active social profiles, typical DR 16-40.

**Authority phase**: 36+ months, 500+ pages, full knowledge panel, regular news coverage, full social presence with real engagement, typical DR 41+.

Signals should mostly agree. If they don't, take the second-highest. Sites mature unevenly, and you want to pick tactics for where the site actually is.

## Edge cases

**New site for an established company.** A 3-month-old site launched by a 20-year-old brand inherits much of the parent's authority through entity signals (sameAs, shared press coverage, shared executives). Treat as Growth or Authority based on the parent's phase. The 2024 API leak confirmed subdomains build authority independently, but entity recognition crosses domains.

**Old site with thin content.** A 10-year-old domain with 15 pages, no news, and no brand recognition is still Foundation. Domain age alone isn't enough; it's the combination of age + content + brand that unlocks Growth tactics.

**Niche authority without broad recognition.** A B2B site in a narrow vertical may have strong topical authority (industry awards, expert quotes in trade publications) without a knowledge panel. If niche publications link to and cite it, treat as Authority for tactic selection.

**Dormant or reactivated brand.** Old domain, was active, went dark, now relaunching. Old entity signals are stale. Treat as Growth: the foundation exists, but velocity needs to rebuild.

## Why classification drives tactic selection

Tactics are phase-specific because the constraints change:

- **Foundation tactics** (entity stacking, citations, new site launch) build the signals Google needs to recognize the brand. Useless at Authority phase; an authority site already has these.
- **Growth tactics** (competitor gap, guest posting, resource pages, skyscraper) require content to pitch. Wasted at Foundation because there's nothing to link to.
- **Authority tactics** (strategic partnerships, podcast guesting, proactive PR) require an existing reputation. Don't work at Foundation because nobody has heard of the brand.

Misclassification is expensive. A Foundation-phase site running Authority tactics gets ignored; an Authority-phase site running Foundation tactics wastes months on low-value platform links it doesn't need. See SKILL.md for the phase-to-tactic mapping.

## Cross-references

- `SKILL.md`: uses this classification to pick tactics. Phase output feeds directly into Step 2.
- `link-velocity-redflags.md`: each phase has a different safe velocity ceiling. A 40-links-per-month rate that's normal at Authority looks like a spam pattern at Foundation.
