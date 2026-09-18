# POP Test On-Page Factor Hierarchy

The page-audit skill loads this when scoring Dimension 5 (Technical On-Page SEO). It settles arguments about which on-page fix is actually worth your time.

## Where this comes from

Kyle Roof spent more than half a decade running 400+ controlled single-variable experiments on Google. The kind where you build a test page that ranks for a made-up keyword, then change one thing at a time and watch what happens. The methodology was granted [US Patent 10,540,263 B1](https://patents.google.com/patent/US10540263B1) in January 2020 and is the engine behind [PageOptimizer Pro](https://www.pageoptimizer.pro/bestplacestoputakeyword). This is the only on-page factor dataset we trust that isn't correlational. It's causal.

## The four groups

**Group A (critical). Get these wrong and nothing else matters.**
- Meta title (the undisputed #1 signal)
- Body content
- URL
- H1

**Group B (important). Worth fixing once Group A is clean.**
- H2
- H3
- H4
- Anchor text of internal links pointing TO the page

**Group C (supporting). Small wins, not differentiators.**
- Bold text
- Italic text
- Image alt text

**Group D (minimal or zero ranking impact).**
- Schema markup (affects SERP features and rich results, NOT rankings directly)
- HTML tags
- Open Graph
- Meta description (affects CTR in the SERP, not ranking)
- Meta keyword tag (ignored)

## Counter-intuitive findings to remember

**1. Keyword position within the title tag does not matter.** Inclusion matters. "First-half placement" is folklore from correlation studies, not causation. When Roof tested beginning vs middle vs end placement, there was no meaningful ranking delta. So when auditing a title tag: check that the primary keyword is *present* and the title *earns the click*. Don't waste a recommendation on "move the keyword to the front."

**2. Schema markup does not directly affect rankings.** Roof's test pages with and without schema ranked identically. Schema drives SERP features (rich results, How-To panels, FAQ accordions, Product cards, Review stars) and those SERP features drive CTR. That's a real lever, just not a ranking lever. When auditing: flag missing schema as a "rich result eligibility" issue in Dimension 6, not as a Dimension 5 ranking problem.

**3. Meta description does not affect rankings at all.** Roof's test pages with keyword-stuffed meta descriptions and those with none ranked identically. The meta description test page never even indexed on the metric he was measuring. Meta description is a 100% CTR instrument. When auditing: judge it on clickability, not keyword inclusion.

## Practical prioritization (this is the load-bearing part)

When the audit surfaces issues across multiple groups, fix them **in strict Group A → B → C → D order**, regardless of how many issues are in lower groups. The math is simple: one Group A fix outweighs ten Group C fixes.

Concretely:

- A page with a weak title tag (Group A) and 14 missing alt tags (Group C): fix the title first. Don't even mention the alt tags until the title is clean.
- A page with a clean title, missing H2 with the keyword variant (Group B), and no schema (Group D): fix the H2. Schema goes in the "consider later if you want rich results" pile.
- A page where Group A is already clean: that's when image alt text, internal anchor text, and bolded phrases actually matter. This is also where most audits *should* land, because Group A is usually obvious.

The inversion to watch for: most generic SEO checklists over-weight Group C/D because those are the factors easiest to scan programmatically. Don't do this. If you surface 15 recommendations and 12 of them are schema and alt text, your audit is telling the author to rearrange deck chairs while the title tag is on fire.

## When to break the rule

One exception: if the page is in YMYL territory (medical, financial, legal) and has zero schema + zero author E-E-A-T signals, schema + author markup belongs higher in the priority stack. Not because it affects rankings directly, but because it's the substrate Google's Quality Raters and automated trust classifiers read. Score that as a Dimension 3 (E-E-A-T) problem rather than a Dimension 5 problem and you'll route it correctly.

## Sources

- [Kyle Roof, The TOP 10 on-page factors from top to bottom (pageoptimizer.pro)](https://www.pageoptimizer.pro/bestplacestoputakeyword): the source-of-truth page for the grouping
- [US Patent 10,540,263 B1](https://patents.google.com/patent/US10540263B1): Roof's test methodology patent
- [Kyle Roof HCU interview (Niche Pursuits)](https://www.nichepursuits.com/kyle-roof-hcu/): Roof's position on E-E-A-T as defensive-not-offensive
- Cyrus Shepard's 4,000-site case study ([zyppy.com](https://zyppy.com/seo/google-update-case-study/)): correlational follow-up that confirms Group A dominance at scale
