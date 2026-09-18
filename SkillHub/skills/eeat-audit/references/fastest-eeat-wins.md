# Fastest E-E-A-T Wins

The highest-leverage, lowest-effort fixes to materially lift an E-E-A-T score. Every item below takes under 30 minutes and shifts at least one dimension by one point. Ordered by impact-per-minute.

Use this list when the audit surfaces gaps and the user asks "what's the fastest fix?" Don't recommend structural rewrites when one of these will do the job.

## The 12 fastest wins

### 1. Add a first-person anecdote in the intro

**Time:** 10 to 15 min. **Impact:** +2 Experience.

Replace the generic "In this article we'll cover X" opener with a specific moment: "When I first tried X, I expected Y, but what actually happened was Z." The anecdote has to be specific enough that it couldn't have been guessed: a real number, a date, a tool version, an error message. Experience is the dimension most pages fail on, and the intro is where raters decide whether to keep reading.

### 2. Replace "according to studies" with a named primary source + year

**Time:** 5 to 10 min per instance. **Impact:** +1 Expertise per fix.

Every unsourced claim is a Trust hole. Rewrite "studies show that X" as "a 2024 paper in [journal] by [author] found X." Link to the primary source, not to a secondary blog post citing it. This is the single highest-leverage Trust and Expertise fix you can make on research-heavy content, and it scales. Do three instances and you've moved two dimensions.

### 3. Add a "last updated" date header

**Time:** 2 min. **Impact:** +1 Trust.

Add a visible "Last updated: YYYY-MM-DD" line under the byline. On time-sensitive content (pricing, compliance, product specs, YMYL), an undated page is automatically suspect. A dated page that's been updated recently is automatically more trustworthy. This is the cheapest Trust win there is.

### 4. Link the author bio to an external verifiable profile

**Time:** 5 min. **Impact:** +1 Authoritativeness.

Add a link from the author bio to LinkedIn, GitHub, ORCID, Google Scholar, or the professional registry for the credential (state bar, FINRA BrokerCheck, state medical board). The 2024 Google API leak surfaced an `authorReputationScore` on author entities. Google is actively trying to disambiguate authors across the open web, and you help it do that by pointing at profiles it can crawl. A bio with no external link is a dead-end entity.

### 5. Add a methodology section

**Time:** 15 to 20 min. **Impact:** +2 Trust.

Two paragraphs disclosing how the content was produced. On a review: "We tested X for Y weeks, on Z specific setup, tracking [metrics]." On research: "We pulled data from [source], filtered for [criteria], and calculated [method]." On a how-to: "These steps are from our own process across [N] implementations." Methodology is the difference between "this could be true" and "I can see why this is true."

### 6. Add affiliate or conflict-of-interest disclosure

**Time:** 2 min. **Impact:** +1 Trust.

If the page contains affiliate links, paid placements, or a relationship with the thing being reviewed, disclose it at the top, not in the footer. Google's Quality Rater Guidelines treat undisclosed commercial relationships as a Trust violation. Disclosed relationships are not penalised; hidden ones are.

### 7. Replace stock imagery with a screenshot from your own workflow

**Time:** 5 to 10 min. **Impact:** +1 Experience.

Stock photography is an anti-signal on experience-driven content. Swap one hero image for a screenshot from the author's own dashboard, terminal, tool, or physical workspace. Original visuals are one of the hardest signals to fake, which is precisely why they carry weight.

### 8. Add a specific failure story

**Time:** 10 to 15 min. **Impact:** +2 Experience.

One paragraph: "The first time I did X, it didn't work. The reason was [specific mechanism], and I only figured it out after [specific action]." Failure stories are the single strongest Experience signal because nobody who hasn't actually done the thing can invent a plausible failure mode. They also buy goodwill with readers, which reduces bounce rate and compounds on other signals.

### 9. Add 2-3 internal links to related content on the same domain

**Time:** 5 min. **Impact:** +1 Authoritativeness.

Link out to other pages on the same topic, ideally a pillar page plus one or two sibling posts. This builds the topical cluster signal at the page level. Authoritativeness is mostly a domain-level signal, but page-level internal linking is how the domain cluster gets assembled.

### 10. Add Author schema markup

**Time:** 10 min. **Impact:** +1 Trust.

Add a JSON-LD Person + Author block to the page, with `name`, `url`, and a `sameAs` array pointing at external profiles. See `author-schema-templates.md` for copy-paste templates. Schema doesn't substitute for substance, but on a page that already has substance, it makes the author entity legible to Google's knowledge graph.

### 11. Replace generic imagery with original data visualization

**Time:** 20 to 30 min. **Impact:** +2 Experience and Expertise.

One bar chart, one comparison table, or one annotated screenshot built from the author's own data. Original visualisations are nearly impossible to fake and they signal both hands-on engagement (Experience) and synthesis (Expertise). If the page already has numbers in the text, this is usually just a matter of putting them in a chart.

### 12. Add a "Who should NOT follow this advice" section

**Time:** 10 min. **Impact:** +1 Expertise, +1 Trust.

Three or four bullets on who this advice doesn't apply to, and why. This is the expertise paradox in action: real experts narrow their scope, beginners try to cover everyone. Acknowledging edge cases signals that the author understands the boundary of their own advice. It also hedges Trust risk on YMYL-adjacent content.

## Prioritisation

If you have to pick a few fixes, let the current score dictate where to spend the time:

- **Page scoring under 3 on any dimension.** Fix Experience first. Low-experience pages fail the 30-second test, which means nothing else matters. Wins 1, 7, 8, and 11 are all Experience fixes.
- **Page scoring 4 to 6.** Fix Trust. These pages have some substance but are leaking credibility through unsourced claims, missing dates, and missing disclosures. Wins 2, 3, 5, 6, and 10 are all Trust fixes.
- **Page scoring 7 or higher.** Fix Authoritativeness. At the top of the rubric the remaining gaps are usually external: the author isn't linked, the topical cluster isn't assembled, the page is an island. Wins 4 and 9 target this.

Don't fix Expertise with quick wins on a page where the underlying content isn't expert. Expertise is the one dimension that quick fixes can't really move. Either the author knows the thing or they don't, and no amount of formatting lipstick will hide that from a careful reader.
