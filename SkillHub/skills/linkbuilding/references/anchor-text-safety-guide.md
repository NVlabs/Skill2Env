# Anchor Text Safety Guide

Anchor text is the clickable text in a backlink. Google reads it as a strong relevance signal, which is exactly why it's the easiest thing to over-optimize and the first thing Google's spam systems look at. This guide is about avoiding two specific failure modes: the Penguin-era exact-match penalties that still apply today, and the modern SpamBrain classification that treats anchor text patterns as a primary spam signal.

## A short history

On April 24, 2012, Google rolled out Penguin 1.0. It hit around 3.1% of English queries and it was aimed squarely at manipulative link profiles. The pattern was obvious in hindsight: sites using keyword-optimized anchor text on 65%+ of their inbound links took the worst hits. Early Penguin often applied sitewide demotions, so one spammy-looking link profile could tank the whole domain.

Penguin was folded into Google's core algorithm in 2016, which means it runs continuously now rather than rolling out in batches. Then in December 2022, Google's December 2022 Link Spam Update put SpamBrain in charge of link evaluation. SpamBrain is Google's AI classifier for spam, first deployed in 2018. The 2022 update specifically extended it to detect both sites that buy links and sites built to sell them. Google reported catching 50x more link spam than previous updates.

The 2024 API leak confirmed what practitioners had suspected: Google tracks signals like `phraseAnchorSpamDays` to measure anchor text velocity and pattern, and uses them to nullify suspect links. The mechanism is no longer just a penalty. Links can now be silently ignored, which feels like "my outreach stopped working" rather than a clear signal something's wrong.

## The safe distribution

These are the target ranges. Think of them as a budget, not a formula:

| Category | Safe range | What counts |
|---|---|---|
| **Branded** | 40-55% | Your business name, domain name, founder name (e.g., "Acme", "acme.com", "Acme Tools") |
| **Naked URL** | 15-20% | The literal URL as the anchor (e.g., "https://acme.com/blog/post") |
| **Generic** | 15-20% | "click here", "read more", "this article", "check it out", "source" |
| **Partial match** | 10-15% | Anchors containing your target keyword plus other words (e.g., "this guide to email marketing") |
| **Exact match** | 3-5% MAXIMUM | Anchors that are literally your target keyword (e.g., "email marketing software") |

### Why each category matters

**Branded anchors** are the baseline signal that linking is natural. When humans reference a company, they use the company name. A profile with 50% branded anchors looks like organic linking from editorial content and mentions. A profile with 5% branded anchors looks like outreach where the builder controlled the anchor.

**Naked URLs** signal that someone copy-pasted your link into their content without writing custom anchor text. This is normal editorial behavior. Bloggers, forum users, and journalists often just paste URLs. A healthy naked URL percentage is proof of organic mentions.

**Generic anchors** are a normal human pattern. Read any blog post: "check out this article", "see here", "more info". Generic anchors exist because writers don't want to keyword-stuff their own content. Their presence in your backlink profile looks like editorial linking.

**Partial match anchors** are the bulk of real editorial links. When a writer references a tool or a concept, they usually embed the link inside a natural phrase. This is the category where most legitimate SEO value lives.

**Exact match anchors** are the manipulation risk category. Nobody naturally writes "best email marketing software for small business" as a link phrase; that's obviously targeted. Ahrefs' 2020 study of 384,000+ top-ranking pages found the #1 result averaged just 3.7% exact match. Higher than that starts looking unnatural.

## The 5% rule

Over 5% exact match is the widely cited penalty risk threshold. Some practitioners argue the actual ceiling is closer to 1-2% in competitive niches. The Ahrefs research, plus penalty case studies showing 50%+ of manual actions involved aggressive anchor optimization, puts the safe ceiling at 3-5% in normal niches and lower in competitive ones (finance, health, legal).

A useful rule: if exact match is over 5%, stop pursuing exact-match anchors entirely until you've diluted.

## What to do if you're already over

This happens. Someone inherits a site, or they followed bad advice in 2019, or every guest post they published used the target keyword as the anchor. The fix is boring:

1. **Stop asking for exact-match anchors.** All new links for the next 30-60 days should be branded or naked URL. If an outreach partner offers to include a keyword-rich anchor, ask for the brand name instead.
2. **Pursue 10-15 dilution links.** Entity stacking, citations, testimonials, and podcast mentions are all naturally branded. They dilute the exact match ratio without requiring any explaining.
3. **Check for a manual action** in Google Search Console → Manual actions. Manual actions require a reconsideration request. Algorithmic demotion doesn't.
4. **Disavow only if there's a manual action or the bad anchors came from obvious spam sources.** Disavowing legitimate links makes things worse.
5. **Wait 3-6 months** for the exact match ratio to recover. SpamBrain re-evaluates continuously, but the signal needs time.

## Link source diversity

Anchor text isn't the only shape Google watches. Source diversity matters too. A profile where every link comes from one source type looks just as manipulative as one where every link uses the same anchor.

Watch for monocultures:
- **All guest posts**: a site with 80% guest post links and nothing else looks like it's buying placements
- **All directories**: plausible at Foundation phase, suspicious at Authority phase
- **All forum/comment links**: comment spam signature
- **All from the same country or TLD**: e.g., every link from .in or .ru when you're a US business
- **All from the same template**: five "top 10" listicles from sites that share a layout screams PBN

A healthy profile has guest posts, editorial mentions, directory listings, resource page links, podcast mentions, forum participation, and news coverage, roughly in proportions that match the phase of the site. Foundation sites will lean heavier on directories and entity platforms. Authority sites will lean heavier on editorial and news. See `phase-classification-tree.md` for what's appropriate when.

## Cross-references

- `phase-classification-tree.md`: Different phases tolerate slightly different distributions. A brand-new site with 80% branded is normal (nothing else has built up yet). An authority site with 80% branded suggests the brand is strong but the content isn't being linked to on its merits.
- `link-velocity-redflags.md`: Anchor text patterns and velocity patterns interact. A spike of exact-match anchors over a short window is twice as bad as either signal alone.
