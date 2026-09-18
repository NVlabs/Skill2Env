# First-Link Weight: What the Evidence Actually Says

This unpacks the common claim that "the first link from a spoke to the hub is what Google weights most heavily," where it comes from, and what's still load-bearing in 2026.

## The claim, stated precisely

"First-link priority" is the rule that when a single page contains multiple links pointing to the same destination URL, Google historically counted only the anchor text of the *first* link it encountered in the HTML. All subsequent anchors to that URL were ignored for ranking the destination page. PageRank still flowed through every link (that part was never in dispute), but the anchor signal collapsed to the first one.

Note what this is *not*: it's not a claim that only the first link passes link equity. It's a narrower claim about *which anchor text Google uses* when the same destination is linked twice from the same source page.

## Primary sources

**Rand Fishkin, 2008.** The test that popularized the rule. Fishkin ran a controlled experiment with two links on the same page pointing to the same URL with different anchors, and observed that the destination page ranked for the first anchor's keyword but not the second. The test was clean enough that the rule entered SEO gospel ([Search Engine Journal summary](https://www.searchenginejournal.com/ranking-factors/first-link-priority/)).

**Matt Cutts, 2014.** Google's then-head of webspam confirmed the mechanism on video but added a time stamp. Cutts said that *as of 2009*, Google "only counted the anchor text from the first link," but cautioned "it may not work that way now." On PageRank he was clearer: "PageRank flows to each link individually as it would any other link on the page, at least according to the original PageRank document" ([Search Engine Land, May 2014](https://searchengineland.com/googles-matt-cutts-one-page-two-links-page-counted-first-link-192718)).

**John Mueller, 2018 and later.** Mueller walked the rule back. He said Google hasn't formally defined first-link priority, and behavior "can change and it's not something they have defined," which means "even if you figure out how Google currently does it, that's not necessarily how they'll do it tomorrow or how it always is across all websites" ([Search Engine Journal](https://www.searchenginejournal.com/ranking-factors/first-link-priority/)).

**Cyrus Shepard / Zyppy, 2023.** The most recent primary source. Shepard set up a Search Console property containing pages with no external links anywhere on the internet, then linked to those pages from a single source with specific anchor texts, and used the Top Linking Text report to see which anchors Google had indexed. His finding: Google doesn't always pick the first link, but it does pick *selectively*, hence "selective link priority" rather than strict "first link priority." Hash-fragment links (`#section`) can sometimes slip past the de-duplication and get counted independently ([Niche Pursuits write-up](https://www.nichepursuits.com/cyrus-shepard-internal-links-study/)).

## What "contextual" means and why it matters

The first-link rule is about *which anchor counts*. A separate and more durable finding is about *where on the page the link sits*. In-body contextual links carry more weight than links in navigation, footers, or sidebars. Not because Google has published a rule, but because split tests keep showing it.

SearchPilot's published internal-linking split tests consistently land in the 5-25% organic-uplift range for contextual additions. Their flagship e-commerce test added button links between category levels and produced a 25% uplift in organic sessions on the affected pages ([SearchPilot case study](https://www.searchpilot.com/resources/case-studies/seo-split-test-lessons-increasing-internal-linking)). A separate SearchPilot footer test produced a much weaker 5% uplift ([SearchPilot footer test](https://www.searchpilot.com/resources/case-studies/adding-internal-links-to-home-page-footer)). Same company, same methodology. The placement was the variable.

The intuition: template links (nav, footer, sidebar) appear identically on every page of a site, so Google discounts them as boilerplate. Contextual links inside the body of a specific article are relevance signals about *this page's topic*, not *this site's structure*.

## The practical rule for cluster planning

When a spoke points to its hub, make sure **the first mention of the hub URL is a contextual in-body link with a descriptive anchor.** Not "learn more," not "click here," not a button in a sitewide footer, not a hub tile at the bottom of a template. An actual sentence in the body text like "the broader picture is covered in our [complete guide to email deliverability](/email-deliverability)."

This matters twice over:
1. If first-link priority still applies in some form, the in-body anchor is the one Google uses for the hub's relevance.
2. Even if it doesn't apply anymore, the in-body placement carries more weight by itself (SearchPilot evidence).

A sitewide footer link to the hub is fine as a secondary signal (it doesn't hurt), but it should never be the *only* link from a spoke to the hub, and it should never appear in the HTML before the body link on the page.

## What if first-link priority is outdated?

Assume it is. The contextual-placement rule still holds. You're not losing anything by putting your best anchor in the body; you *are* losing something by burying the hub link in a template block.

The planning rules stand regardless:
- Descriptive anchor text (not "read more")
- One primary body-text anchor per spoke pointing to the hub
- Placement in the first half of the article
- Don't link the hub URL ten times from a single spoke. Two or three is plenty.

## Cross-reference

The page-audit skill cites SearchPilot's 5-25% uplift range when scoring a page's internal linking dimension. This file uses the same evidence base but applies it one layer up, at the cluster-architecture level rather than the page level.
