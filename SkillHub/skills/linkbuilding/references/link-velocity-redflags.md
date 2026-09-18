# Link Velocity Red Flags

Link velocity is the rate at which a site acquires new backlinks. Google evaluates the pattern, not the count. Fast velocity isn't bad in itself (a product launch can earn 500 press mentions in a week), but fast velocity combined with suspicious patterns is exactly what SpamBrain is trained to detect.

## Safe pace by phase

**Foundation (DR 0-15, new site)**
- Month 1: 15-25 links from entity stacking and citations. One-time setup on high-authority platforms (Google Business, LinkedIn, Crunchbase, Wikidata, industry directories). The burst is explained by the launch.
- Months 2-3: 5-10 quality links per month.
- Months 4-6: 8-15 per month as momentum builds.

The Month 1 spike is fine because entity stacking is a pattern Google has seen a million times: new legitimate business sets up its profiles. All branded, all low-risk.

**Growth (DR 16-40)**: 8-15 per month sustained. Consistency matters more than total count. 10/month every month looks healthier than 40 one month and 0 the next.

**Authority (DR 41+)**: 10-30 per month with higher tolerance for spikes. Established brands earn links unevenly, so a research report or viral post can spike to 100+ in a week and look normal. A DR 5 site showing the same pattern looks suspicious because there's no organic reason for it.

## Red flags that trigger SpamBrain attention

Sourced from John Mueller's public statements, Penguin algorithm documentation, and the 2024 API leak that confirmed signals like `phraseAnchorSpamDays` for measuring anchor velocity patterns.

**1. 50+ new links in a single month, especially for a new domain.** The absolute number isn't the trigger; it's the ratio to the site's established pattern. A new domain jumping from 5 links in Month 2 to 80 in Month 3 has no earned explanation. Google's `hostAge` signal (confirmed in the API leak) exists to "sandbox fresh spam", so new sites get extra scrutiny on sudden link acquisition.

**2. Monoculture of country or TLD.** All new links from .ru, .in, or .info clusters, or from one country when the business isn't based there. This is the classic PBN signature: link networks are registered in batches through the same provider. A small US-based B2B SaaS suddenly getting 40 links from Ukrainian and Indonesian directories is the obvious version.

**3. Identical or near-identical anchor text.** Five new links in a month all using "best email marketing software" is obviously coordinated. SpamBrain catches this trivially. Real editorial linking produces varied anchors.

**4. Spike in exact-match anchors.** What Penguin was built to detect in 2012 and still the most reliable spam signal. A site going from 3% exact match to 20% over a month is the textbook spam pattern. See `anchor-text-safety-guide.md` for distribution math.

**5. All links in footer, sidebar, or comment sections.** Editorial in-body links are the gold standard. Footer and sidebar links are template-wide (one placement = every page links to you), which looks like a paid or reciprocal deal. 80% footer/sidebar/comment placement is a monoculture signal even if each individual link looks okay.

**6. Links from sites with no real traffic regardless of DR.** A DR 60 site with 200 monthly visitors is almost certainly a PBN or an abandoned domain bought to resell links. Google's NavBoost (confirmed in the API leak) cross-references traffic against link profiles. Check with any free traffic estimator (Similarweb, Ubersuggest).

**7. Sudden flood from similar-template sites.** Five new links from sites that share the same WordPress theme, similar registration dates, and near-identical content structure: a PBN being emptied into a client. Google's infrastructure analysis cross-references hosting, registration, and design patterns.

## The velocity drop

A sudden stop in link acquisition is milder than a spike but still a signal. If a site averaging 12 links per month drops to 1 per month for three months, Google reads it as: a manual action scaring prospects off, the outreach team stopping (often a quality-drop tell), or the site becoming less link-worthy. Not a penalty, but it slows the trust curve. Steady wins over spiky: prefer 10 per month for a year over 120 in the first month and nothing after.

## What to do if you get caught

Symptoms of SpamBrain classification: rankings drop without a manual action, new links stop moving rankings, and the site loses ground against similar competitors.

1. **Slow down immediately.** No new outreach for 30 days.
2. **Switch to branded anchors only.** Next 10-15 placements use brand name or naked URL.
3. **Disavow the worst offenders.** Sort a backlink export for red flags (low-quality, footer-only, foreign spam) and disavow in Search Console. Be conservative; disavowing legitimate links makes it worse.
4. **Wait 3-6 months.** SpamBrain re-evaluates continuously but normalization takes time.
5. **Rebuild with Foundation-phase tactics** (entity stacking, citations). Safest way back.

## Tracking without paid tools

A simple spreadsheet is enough. Track monthly: date acquired, source domain, source country, source type, anchor text, anchor category, traffic estimate.

At month end, check the category breakdowns. If exact match is creeping up, stop asking for those. If one source type is dominating, diversify next month. If the country column goes monoculture, pull back. No paid velocity tool is needed for sites under 500 referring domains.

## Cross-references

- `anchor-text-safety-guide.md`: Anchor category breakdown and safe distribution ranges. Velocity and anchor patterns interact; a spike in both at once is twice as dangerous as either alone.
- `phase-classification-tree.md`: Safe velocity varies by phase. A 40-per-month rate that's suspicious at Foundation is normal at Authority.
