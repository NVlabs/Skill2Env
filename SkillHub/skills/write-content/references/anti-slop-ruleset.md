# Technique 02: Anti-AI-Slop Defense System

## What It Is

A multi-layered detection and rewriting system that identifies and eliminates AI writing patterns from generated content. Based on research from 6+ GitHub anti-slop skills, Wikipedia's WikiProject AI Cleanup (24+ patterns), academic research on semantic ablation, and StyloAI's 31+ stylometric markers. This is not a post-processing "humanizer" -- it is a quality standard built into the writing process from the start.

**Framing note:** Never label this as "humanization" or "AI detection avoidance." Frame it as quality writing standards. The goal is not to trick detection -- it is to produce writing that is genuinely better than default AI output.

## Why It Works

AI content is detectable because of **semantic ablation** -- RLHF training systematically strips high-entropy information (unique metaphors, specific details, strong opinions), producing text with low burstiness (uniform sentence rhythm) and low perplexity (predictable word choice). These are the exact signals that both human readers and detection algorithms use to identify AI content.

Google's NavBoost system (confirmed in antitrust trial) demotes content that fails to engage users. Bland, detectable AI content drives pogo-sticking (users bouncing back to SERP), which directly hurts rankings.

**Key insight:** Post-processing (running text through a "humanizer") is detectable itself -- it creates a different statistical signature that is distinct from both pure AI and pure human writing. The solution is to generate human-like text from the start, not to fix it after.

## The Science of Detection

### Perplexity (How predictable each word is)
- **AI text**: Low perplexity -- the model picks the statistically most likely next word. "The results clearly demonstrate the significant impact..."
- **Human text**: Higher perplexity -- humans choose unexpected words, use slang, make idiosyncratic choices. "The numbers surprised us. Not because they were good -- they weren't -- but because they were exactly wrong."
- **Fix**: Instruct the model to use less common phrasings, domain-specific jargon, and unexpected vocabulary choices

### Burstiness (Sentence length variation)
- **AI text**: Remarkably uniform -- 15-25 words per sentence, consistent complexity
- **Human text**: Wild variation. Like this. And then suddenly a sentence that stretches across multiple clauses, connecting ideas that might not obviously belong together but make sense when you follow the writer's train of thought. Then short again.
- **Fix**: Explicitly vary sentence length between 3 and 40+ words per section

### Stylometric Patterns (31+ markers per StyloAI research)
- Function word frequency, sentence complexity distribution, vocabulary richness, syntactic diversity
- **AI text**: Clusters tightly in a predictable zone across all markers
- **Human text**: Much wider distribution with more variation

## The Tiered Banned Phrase System

### Tier 1: Always Remove (+3 points each)

These words and phrases are so strongly associated with AI that their presence alone flags content:

**Vocabulary:**
delve, tapestry, realm, landscape (metaphorical), multifaceted, nuanced, testament, cutting-edge, revolutionary, comprehensive (as adjective), crucial, compelling, vibrant, game-changer, leverage (verb), unlock potential, harness, endeavour, embark, navigate (metaphorical), pivotal, intricate, innovative, seamless, robust, transformative, meticulous, facilitate, utilize, commence, paramount, plethora, myriad, culminate, underscore, bolster, spearhead

**Phrases:**
- "It's worth noting that..."
- "In today's [anything] landscape"
- "Moreover" / "Furthermore" / "Additionally" (as sentence starters)
- "Let's dive in" / "Without further ado"
- "In conclusion" / "In summary" / "In essence"
- "It's important to note that..."
- "Stands as a testament to..."
- "Plays a vital/crucial/pivotal role"
- "In the realm of..."
- "It goes without saying"
- "Buckle up" / "Strap in"
- "The landscape is ever-evolving"
- "Marking a pivotal moment in the evolution of..."

**Replacements:**
| AI Word | Human Alternative |
|---------|------------------|
| leverage | use |
| utilize | use |
| commence | start, begin |
| facilitate | help, enable |
| endeavor | try, attempt |
| robust | strong, solid |
| seamless | smooth, easy |
| innovative | new, original |
| comprehensive | full, complete, thorough |
| paramount | critical, key |
| plethora | many, lots of |
| culminate | end in, lead to |
| underscore | show, highlight |
| delve | dig into, look at |
| testament | proof, sign |
| landscape | space, market, field |
| showcase | show |

### Tier 2: Flag When Clustered (+2 points each, flag at 3+ per article)

These are acceptable in isolation but signal AI when they cluster:

- however (more than 2x per article)
- here's the thing
- at the end of the day
- paired adjectives ("comprehensive and thorough", "innovative and cutting-edge")
- template openings ("In this article, we'll cover...")
- firstly / secondly / thirdly
- moving forward
- arguably
- notably
- essentially
- that said
- on the other hand
- it's no secret that

### Tier 3: Flag at High Density (+2 points per cluster of 3+)

- Transition words when overused (however, therefore, consequently, meanwhile)
- Corporate buzzwords (scalable, streamlined, optimize, synergy)
- Excessive qualifiers (quite, rather, somewhat, fairly, relatively)
- Hedging language (perhaps, might, could potentially, to some extent)

## Structural Pattern Detection

### Patterns to Flag and Rewrite

1. **Uniform sentence length** (+4 points): Three or more consecutive sentences within 3 words of each other in length. Fix: vary dramatically -- mix 5-word punches with 30-word complexes.

2. **Rule-of-three addiction** (+3 points): Habitual grouping of three examples, adjectives, or list items. Fix: use 2, 4, or 5 items instead.

3. **Topic-sentence-support pattern** (+3 points): Every paragraph starting with a topic sentence followed by supporting detail. Fix: start some paragraphs with an example, a question, or a statement that only makes sense after reading on.

4. **Binary contrast pattern** (+3 points): "It's not X, it's Y" or "No X, no Y, just Z." Fix: make the actual argument without the rhetorical frame.

5. **Staccato fragments** (+3 points): "Short. Punchy. Exhausting." -- dramatic fragmentation that feels manufactured. Fix: use fragments sparingly, for genuine emphasis only.

6. **Compulsive summarizing** (+2 points): Summary paragraph at the end of every section. Fix: only summarize if the section is genuinely complex (3+ subsections).

7. **Copula avoidance** (+2 points): "serves as" instead of "is", "functions as" instead of "is". Fix: just say "is" when that's what you mean.

8. **Synonym cycling** (+2 points): Using different words for the same concept in adjacent sentences to appear varied. Fix: repeat the same word if clarity demands it.

9. **Participial tack-ons** (+2 points): "...highlighting the importance of X" or "...underscoring the need for Y" at the end of sentences. Fix: delete or make a separate sentence.

10. **Em dash overuse** (+1 point per em dash beyond 1 per 500 words): AI uses em dashes far more frequently than humans. Fix: use commas, parentheses, or separate sentences.

### Additional Structural Patterns

11. **The hourglass structure**: AI structures text as synthesis -> detail -> synthesis. Humans start with a specific story, zoom out, dive into details in uneven bursts, and end with something specific again. **Break the hourglass.**

12. **Asymmetric coverage absence**: AI distributes word count evenly across all subtopics. Humans spend 500 words on the interesting part and 50 on the boring-but-necessary part. If every section is roughly the same length, flag it.

## The Two-Pass Audit System

### Pass 1: Detection and Rewrite

Scan the complete text against all three tiers plus structural patterns. For each detection:
1. Quote the flagged text
2. Explain why it's flagged (tier + specific pattern)
3. Provide a rewrite that preserves meaning while eliminating the pattern
4. Apply the rewrite

### Pass 2: Surviving Pattern Check

After Pass 1 rewrites, re-scan the full text. First-pass rewrites sometimes introduce new AI patterns (the model's natural tendency reasserts). Specifically check for:
- Recycled transitions that survived the first edit
- Lingering vocabulary inflation (replaced one AI word with another)
- Copula swaps that crept back in
- New structural uniformity introduced by the rewrites

### The Horoscope Test (Final Check)

For each paragraph, ask: "Could anyone have written this, for anyone, about anything?" If the answer is yes, the paragraph fails regardless of passing the phrase checks. Every paragraph must contain at least one element that is specific to THIS topic, THIS audience, THIS moment.

Score: +5 points for each paragraph failing the Horoscope Test.

## Risk Scoring

| Score | Risk Level | Action |
|-------|-----------|--------|
| 0-5 | Low | Content passes |
| 6-12 | Medium | Flag specific issues for human review |
| 13-20 | High | Auto-revise flagged sections |
| 21+ | Critical | Full rewrite required |

## Content Patterns to Eliminate

Beyond vocabulary and structure, eliminate these content-level patterns:

1. **No formulaic challenges**: "Despite facing challenges, the company continues to thrive" -- name the actual challenge or cut it
2. **No vague attributions**: "Studies show..." -> "A 2024 Ahrefs study of 100K pages found..."
3. **No significance inflation**: "Marking a pivotal moment in the evolution of..." -> Cut the entire phrase. Start with what actually happened.
4. **Use contractions**: "doesn't" not "does not." "We've found" not "We have found."
5. **Use colloquial transitions**: "Thing is," "Here's the catch," "The weird part?" instead of "Furthermore," "Moreover," "Additionally"
6. **Repeat the clearest word** instead of cycling synonyms: If the subject is "customers," don't alternate between "clients," "users," "patrons," and "consumers"

## Tips

- **The "bar conversation" test**: Would you say this sentence to a colleague at a bar? If not, it's too formal or AI-sounding. "The implementation demonstrated significant improvements in key performance indicators" -> "The thing actually worked. Revenue went up 18%."

- **The Horoscope Test**: Could this paragraph appear in any article, about any topic, for any audience? If yes, it has zero specificity. Every paragraph needs at least one element unique to THIS topic.

- **Self-correction is human**: "At first I thought this was a branding problem -- turns out it was pricing all along" shows the writer's actual thought process. AI does not self-correct mid-argument.

- **Tangential value**: Brief tangents that add context but aren't strictly necessary: "Side note: we tested this during Black Friday, which might have skewed results upward." AI stays rigidly on-topic. Humans digress when the digression adds value.

- **Asymmetric coverage**: Spend 500 words on the interesting part and 50 on the boring-but-necessary part. AI distributes word count evenly. Humans allocate attention where it matters.

- **Imperfections are features**: One slightly awkward phrasing, one mild redundancy, one sentence that could be tighter -- these are signals of human writing. Perfect prose = AI prose.

- **Domain convention awareness**: Academic writing IS more formal than blog writing. Match the expected register for the content type. Don't make an academic paper sound like a blog post, and don't make a blog post sound like a dissertation.

- **The rhythm check**: Count sentence lengths in each paragraph. If standard deviation is < 5 words, rewrite for more variation.

## Common Mistakes

1. **Thinking "more editing" = more human** -- Over-humanizing creates its own detectable pattern. Don't make every sentence a fragment or start every paragraph with "Look,". One technique used excessively becomes its own signature.

2. **Using "humanizer" tools** -- These are detectable as post-processed text. The statistical signature is different from both pure AI and pure human writing. They solve the wrong problem.

3. **Thinking typos = human** -- Intentional typos are a different pattern than natural typos. Don't add them deliberately.

4. **Ignoring domain conventions** -- Academic writing IS more formal than blog writing. A technical whitepaper should not read like a casual blog post. Match the expected register for the content type.

5. **Removing patterns without adding personality** -- Anti-slop auditing alone produces sterile text. Voice injection (Technique 03) must happen BEFORE anti-slop auditing.

6. **Thinking "different words" = fixed** -- Replacing one AI word with another AI word (e.g., "leverage" -> "harness") accomplishes nothing. Replace with genuinely plain language ("use").

## Implementation Notes

- The tiered system allows the writing phase to use Tier 2/3 words occasionally (natural) while the audit phase catches clusters
- Pass 2 is essential -- research shows first-pass rewrites retain 15-20% of AI patterns
- The Horoscope Test catches generic content that avoids banned words but remains soulless
- Voice injection (Technique 03) must happen BEFORE anti-slop auditing -- removing patterns without adding personality produces sterile text
- Anti-detection instructions should be included IN the writing prompt, not as a separate post-processing step

## Key Sources

- [blader/humanizer](https://github.com/blader/humanizer) -- 1,600+ stars, based on Wikipedia's 24 patterns
- [conorbronsdon/avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing) -- 102-entry tiered replacement table
- [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop) -- 8 rules, 50-point scoring
- [aplaceforallmystuff/the-antislop](https://github.com/aplaceforallmystuff/the-antislop) -- Horoscope Test
- [DonAldente-AI/anti-slop-system](https://github.com/DonAldente-AI/anti-slop-system) -- Naive drafter + ruthless critic pattern
- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
- [Semantic Ablation (The Register)](https://www.theregister.com/2026/02/16/semantic_ablation_ai_writing/)
