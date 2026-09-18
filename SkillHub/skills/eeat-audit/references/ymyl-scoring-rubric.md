# YMYL Scoring Rubric

Elevated E-E-A-T standards for Your Money or Your Life content. Use this rubric instead of the main 40-point rubric when the topic can affect a reader's health, finances, safety, legal standing, or civic participation.

## Google's YMYL definition

Google's Search Quality Rater Guidelines define YMYL as topics that "could significantly impact the health, financial stability, or safety of people, or the welfare or well-being of society." The guidelines break this into three harm categories:

- **YMYL Health or Safety.** Mental, physical, or emotional health, or any form of safety.
- **YMYL Financial Security.** Anything that could damage a person's ability to support themselves or their family.
- **YMYL Government, Civics & Society.** Public institutions, election and voting information, anything that shapes how groups of people are treated.

If a topic fits any of those three, the rater is instructed to apply stricter E-E-A-T standards. This rubric encodes what "stricter" means in practice.

## What makes a topic YMYL

If you're not sure, lean toward YMYL. False positives cost you nothing; false negatives publish harmful content under a standard rubric. The buckets that almost always trigger YMYL:

- **Medical.** Health conditions, symptoms, medications, dosages, treatments, drug interactions, pregnancy, mental health, nutrition for a specific condition.
- **Financial.** Investment advice, tax advice, credit scores, loans, mortgages, retirement planning, crypto, insurance, bankruptcy.
- **Legal.** Contracts, family law, criminal defense, immigration, tenant rights, employment law, wills and estates.
- **Safety-critical.** DIY electrical, gas appliances, chemicals, firearms, child safety (car seats, cribs, medication dosing), home structural work, food safety.
- **Parenting.** Infant care, vaccination, developmental milestones, discipline methods.
- **Civic and news.** Elections, voting procedures, government benefits, public-health guidance.
- **E-commerce with material consequence.** Reviews where the purchase is non-trivial (a mattress, a car, a SaaS contract, a loan product).

Note on e-commerce: a review of a $4 kitchen gadget isn't YMYL. A review of a $40,000 car, a $3,000/year SaaS contract, or a mortgage product is. The test is whether a bad decision materially hurts the reader.

## The YMYL adjustment

Each E-E-A-T dimension gets a stricter interpretation when the topic is YMYL. The point weights shift, and the scoring anchors move.

### Experience (YMYL weighting: 10 pts, unchanged)

On non-YMYL topics, a first-person story is usually enough. On YMYL, the story has to be backed by primary-source evidence of hands-on work, not just "I tried this once." A medical writer saying "I had this condition" is weak. A medical writer saying "I had this condition, here's the treatment protocol my endocrinologist put me on, here's the lab value I was tracking, here's what changed at month three" is strong.

The rubric rewards evidence of *repeated* hands-on engagement: multiple cases, documented outcomes, a track record visible in the writing itself.

### Expertise (YMYL weighting: 12 pts, elevated from 10)

This is the biggest shift. On non-YMYL topics, a smart generalist can write credibly about, say, pour-over coffee. On YMYL topics, the reader needs to know the author has externally verifiable credentials in the specific field: medical license, CFA, bar admission, licensed electrician. Lily Ray's public writing on YMYL has emphasized this point repeatedly: for financial or medical advice content, credentials should be substantiated and revealed, with content published under a byline including those credentials rather than anonymous.

Verifiable means the reader can click through and confirm. A bio that says "Dr. Smith, MD" with no link and no institution is worse than no bio at all, because it's claiming authority without letting the reader check.

### Authoritativeness (YMYL weighting: 8 pts, unchanged)

On YMYL the domain needs to have a defensible position in the vertical. A random blog publishing a tax guide scores low even if the post itself is accurate. A site that's been publishing tax content for years, has a topical cluster, and is cited by other sites in the space scores high.

### Trustworthiness (YMYL weighting: 10 pts, elevated from 8)

Factual accuracy is non-negotiable on YMYL. A single factual error drops the Trust score below the "do not publish" threshold. Sources must be linked, not just named. Disclaimers are required where the content could be misread as professional advice ("this is not medical advice, consult your doctor"). Conflict-of-interest disclosure is required, and cannot be buried in a footer.

## The 40-point YMYL rubric

### Experience: 10 pts

- **10.** Author narrates multiple hands-on cases with specific details (dates, values, outcomes, what went wrong). Includes primary-source artifacts: screenshots, photos, records, case notes with identifying info redacted. A reviewer can tell within 30 seconds the author has done this repeatedly.
- **6.** One first-person story, reasonably specific, but no repeated evidence. The author has probably done the thing once.
- **2.** No first-person engagement. Author writes as if summarizing other sources. No artifacts, no specific moments, no failure stories.

### Expertise: 12 pts (elevated)

- **12.** Byline includes specific credentials relevant to the YMYL topic (MD for medical, CFP for financial, licensed attorney in the jurisdiction for legal). The credentials link externally to a verifiable profile (state medical board, FINRA BrokerCheck, state bar directory, ORCID, university faculty page). The content displays technical depth consistent with the credential: correct terminology, edge cases, acknowledgment of when advice doesn't apply.
- **6.** Author is credentialed but the link isn't there, OR the link is there but the content reads like a generalist summary. Accurate but shallow.
- **2.** No credentials visible, or credentials are in the wrong field (a marketing writer publishing medical advice). Content contains factual errors or outdated guidance.

### Authoritativeness: 8 pts

- **8.** Site has a clear topical cluster in the YMYL vertical, with 20+ related pages, internal linking between them, and external citations from other sites in the space. The author is cited externally via speaking engagements, other publications, or professional listings.
- **5.** Topical cluster exists but is thin. Some internal linking. Limited external validation.
- **2.** Isolated post on a general-interest site. No cluster, no external citations, no topical focus.

### Trustworthiness: 10 pts (elevated)

- **10.** Every factual claim has a linked primary source (peer-reviewed study, government agency, official guidance, named expert with credentials). Page has a visible last-updated date. Disclaimer present where appropriate. Conflict-of-interest disclosure is prominent if any exists. Methodology disclosed for original data. Correction log if the page has been updated after errors.
- **6.** Most claims are sourced, but some are asserted without citation. Update date present. Disclaimer missing or buried.
- **2.** Unsourced claims, factual errors, no disclaimers, undisclosed affiliate or sponsored relationships, no update date on time-sensitive content.

### Score thresholds

- **35+.** YMYL-ready. Publish.
- **30 to 34.** Needs Trust fixes. Add sources, link credentials, add disclaimer. Fix before publishing.
- **25 to 29.** Needs major revision. Multiple dimensions are weak. Rework the piece before considering publication.
- **Below 25.** Do not publish until rewritten. On YMYL, a low-scoring page can actively harm readers and will drag down site-level trust signals.

## Topic-cluster cross-reference

Six of the YMYL-adjacent content types already have structural templates in `eeat-audit/references/content-types/`:

- `product-reviews.md` for e-commerce YMYL reviews
- `pricing-pages.md` for commercial intent with financial consequence
- `service-pages.md` for professional services (legal, financial, medical)
- `case-studies.md`, the strongest E-E-A-T content type for service YMYL
- `about-pages.md` where credentials get substantiated
- `thought-leadership.md` for authoritative long-form opinion in a YMYL vertical

Use those templates for structure. Use this rubric for scoring.
