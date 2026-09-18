# Technique 03: Voice & Personality Injection

## What It Is

A system for injecting genuine human voice, personality, and specificity into AI-generated content. Removing AI patterns (Technique 02) is necessary but insufficient -- "sterile, voiceless writing is just as obvious as slop" (blader/humanizer). This technique adds the human qualities that make content engaging, trustworthy, and undetectable.

## Why It Works

AI content is detectable primarily because it regresses to the mean of all writing. A specific voice has specific word preferences, sentence rhythms, opinions, and reference domains that break the low-perplexity pattern. Voice injection also directly addresses Google's E-E-A-T "Experience" signal -- content with genuine personality signals a real author with real opinions.

Voice consistency is one of the strongest anti-AI-detection signals AND brand trust signals. Readers recognize when content "sounds different" -- it breaks trust. AI-generated content without voice injection sounds like every other AI-generated piece, which is detectable by both humans and algorithms.

Google's EEAT framework implicitly rewards voice consistency: content from a recognizable, consistent voice signals a real author with real expertise. Generic AI voice signals generic AI.

## Step-by-Step Process

### Step 1: Voice Sample Collection
1. Gather 3-5 real articles written by the brand's actual writer(s)
2. Include variety: a formal piece, a casual piece, a technical piece
3. Each sample should be 500-1,500 words minimum
4. These samples are the SINGLE most important input for quality output
5. **Capture negative examples too**: "We NEVER say 'leverage'" or "We NEVER use bullet points for everything" is just as important as positive guidelines

### Step 2: Voice Analysis
6. Analyze the samples for:
   - **Sentence length patterns**: Does the writer use short, punchy sentences? Long, flowing ones? A mix?
   - **Vocabulary level**: Technical jargon? Plain language? Industry-specific terms?
   - **Tone markers**: Humorous? Direct? Academic? Conversational? Provocative?
   - **Structural preferences**: Lists vs prose? Subheadings frequency? Paragraph length?
   - **Personal pronouns**: "We" (corporate)? "I" (personal)? "You" (direct address)?
   - **Opening style**: Start with a story? A statistic? A question? A bold statement?
   - **Transition style**: Formal ("Furthermore")? Conversational ("But here's the thing")?
   - **Quirks**: Any distinctive patterns? Parenthetical asides? Rhetorical questions? Specific metaphors?

### Step 3: Voice Profile Creation
7. Create a voice profile document with this structure:

```
VOICE PROFILE: [Brand Name]

Tone: [e.g., "Direct and slightly irreverent. Not afraid to call out bad advice."]
Register: [e.g., "Professional but conversational -- like explaining to a smart colleague"]
Perspective: [e.g., "First person plural ('we') for company content, first person singular ('I') for author-attributed pieces"]

DO: [e.g., "Use short paragraphs, ask rhetorical questions, include specific numbers"]
DON'T: [e.g., "Don't use corporate jargon, don't hedge everything, don't use emojis"]

Vocabulary preferences:
- Say "customers" not "clients"
- Say "build" not "develop"
- Say "test" not "validate"

Example phrases that capture the voice:
- "Here's the thing nobody talks about..."
- "We tested this. The results surprised us."
- "Skip the theory. Here's what actually works."
```

### Step 4: Voice Integration in Prompts
8. Include the voice profile in every writing prompt
9. Include 1-2 voice sample excerpts as few-shot examples
10. Instruct the model: "Write as if you ARE [writer name]. Match their sentence patterns, vocabulary, and tone exactly."
11. After generation, compare output against samples for voice drift

### Step 5: Voice Consistency Audit
12. Read the draft next to a real sample -- do they sound like the same person?
13. Check for AI voice bleeding through (formality spikes, generic transitions)
14. Verify vocabulary consistency (using the brand's specific terms)
15. Check opening and closing style matches the brand pattern
16. **Update samples regularly**: If the brand's voice evolves (it will), update the samples. Stale samples produce dated-sounding content.

## The 10 Voice Injection Techniques

### 1. Named Persona

**What:** Give the AI a specific writer identity with documented quirks, opinions, and speech patterns.

**Mechanism:** Forces the model away from the statistical mean. A specific voice has specific word preferences, sentence rhythms, and opinions that break predictability.

**Implementation:**
```
You are writing as [Name], a [role] who has been doing this for [X years].
They are known for: [specific trait, e.g., "blunt honesty about what doesn't work"]
They frequently reference: [domain, e.g., "cooking analogies to explain technical concepts"]
They dislike: [specific pet peeve, e.g., "vague advice without data"]
They would never say: [banned phrases specific to this persona]
Example of their voice: "[2-3 example sentences]"
```

**Not:** "Write in an engaging, conversational tone." This is too vague and produces generic "friendly" AI writing.

### 2. Burstiness Enforcement

**What:** Explicitly vary sentence length dramatically.

**Mechanism:** Directly addresses the low-burstiness detection signal. Humans naturally produce "bursts" of complexity followed by simple punchy lines.

**Implementation:**
```
Vary sentence length dramatically. Follow a long, complex sentence with
a short punchy one. Some paragraphs should be a single sentence. Others
should be five or six sentences. Never let three consecutive sentences
be similar in length. Mix 5-word fragments with 35-word complex sentences.
```

**Example transformation:**
- AI: "Email marketing remains one of the most effective digital marketing strategies available to businesses today. It provides a direct line of communication with potential customers. The return on investment is consistently high across industries."
- Human: "Email marketing works. Not in the vague, 'it's part of a balanced strategy' way consultants love. I mean: for every euro you spend, you get 36 back. That's DKG's 2025 data across 4,000 campaigns, and it's been consistent for five years running."

### 3. Specificity Over Generality

**What:** Replace every general claim with a specific example, number, name, date, or anecdote.

**Mechanism:** Specific details are high-entropy tokens that break predictability. They also signal E-E-A-T (Experience, Expertise) to Google.

**Implementation:**
```
Never write a general claim without a specific example. Instead of
"many companies struggle with this," write "When Coolblue's marketing
team hit this wall in Q3 2025, they..." Every abstraction must be
grounded in a concrete particular. If you don't have a real example,
make the specificity about the scenario: exact numbers, exact steps,
exact consequences.
```

**The "30% Rule":** At least 30% of every page should contain details no generic AI could produce: proprietary data, original analysis, first-hand testing results, specific case studies, or named examples.

### 4. Contrarian/Opinionated Writing

**What:** Take clear stances. Disagree with conventional wisdom when appropriate.

**Mechanism:** AI is trained via RLHF to be balanced and inoffensive. Strong opinions are high-entropy by definition. They also drive engagement (comments, shares, backlinks) which are ranking signals via NavBoost.

**Implementation:**
```
Take a strong position on every topic. Don't hedge with "it depends"
unless you genuinely mean it. If something is bad, say it's bad. If
the conventional wisdom is wrong, say so and explain why with evidence.
You are allowed to be wrong -- that's what makes you interesting.

When appropriate, include phrases like:
- "Here's what most guides get wrong about this..."
- "I've tested this and the data says the opposite..."
- "Everyone recommends X but in my experience Y works better because..."
```

### 5. Cultural References & Temporal Anchoring

**What:** Reference specific cultural moments, current events, or shared experiences.

**Mechanism:** Real cultural references signal an author who lives in the world. They create "information gain" that generic content cannot replicate. They anchor content in a specific time and place.

**Implementation:**
```
Reference specific cultural touchstones where relevant -- recent news,
industry events, widely-known examples. Not as decoration but as genuine
analogies that illuminate your point. Use references your target audience
would know. For Dutch audiences: reference Prinsjesdag, Black Friday NL,
specific Dutch companies, known media personalities, etc.
```

### 6. Show Don't Tell

**What:** Demonstrate claims through mini-narratives and scenarios instead of stating them.

**Mechanism:** "Telling" produces low-perplexity text ("Page speed affects rankings"). "Showing" produces high-perplexity, engaging text ("You click a search result. Three seconds pass. Still loading. You hit back. Google noticed.").

**Implementation:**
```
Never just state a fact. Show it through a brief scenario. Instead of
"page speed affects rankings," write a mini-narrative: "You click a
search result. Three seconds pass. The page is still loading. You hit
back and click the next result. Google tracked every millisecond of that
interaction -- and it just cost the slow site a ranking position."
```

### 7. Read-Aloud Test (Paul Graham Method)

**What:** Every sentence should sound natural when spoken aloud to a friend.

**Mechanism:** Paul Graham claims this puts you "ahead of 95% of writers." Conversational language has naturally higher burstiness, uses contractions, and avoids the formal register AI defaults to.

**Implementation:**
```
Write as if talking to a smart friend over coffee. Use contractions
(don't, isn't, won't). Start sentences with "And" or "But" when natural.
Drop unnecessary qualifiers. If you wouldn't say it out loud, rewrite it.

Test: read every paragraph back. If it sounds like a textbook, rewrite
it until it sounds like a person.
```

### 8. Strategic Imperfection

**What:** Include deliberate human markers -- fragments, parenthetical asides, self-corrections.

**Mechanism:** AI produces unnaturally perfect grammar and structure. Human writing has quirks that increase both burstiness and perplexity.

**Implementation:**
```
You are allowed to be imperfect. Use sentence fragments for emphasis.
Start sentences with conjunctions. Use parenthetical asides (like this)
when you have a tangential thought. Occasionally correct yourself
mid-paragraph ("well, actually..." or "that's not quite right --").
Real writers do this naturally.
```

### 9. Register Shifts

**What:** Shift between formal and casual register within the same piece.

**Mechanism:** AI maintains a uniform register. Humans naturally shift -- a technical explanation followed by a casual aside, a formal point followed by a joke.

**Implementation:**
```
Shift between registers naturally. After a technical paragraph,
drop in something casual. After making a serious point, add a human
aside. The contrast is what makes writing feel alive.

Example: "The algorithm processes 12 trillion signals per query.
(Yes, trillion. With a T. And it does this in under 0.5 seconds.
Makes you feel productive, doesn't it?)"
```

### 10. The Gary Halbert "One Person" Principle

**What:** Write to one specific person, not an audience.

**Mechanism:** "Write your copy as if you're having a conversation with one reader." Using "I" and "you" creates intimacy. Specific, seemingly irrelevant details build trust.

**Implementation:**
```
Write to one specific person who already cares about this topic.
Use "you" and "I" (or "we" for brand content). Include specific,
concrete details even when they seem tangential -- they build trust.
Don't persuade; serve. Imagine the reader is sitting across from
you at a table, asking a real question.
```

## Voice Document Structure

The writing skill should load a Voice Document (from your saved business context or user-provided) with this structure:

```markdown
## Brand Voice Profile

### Identity
- Writer role/title:
- Years of experience:
- Known for:
- Industry perspective:

### Voice Characteristics
- Formality level: [casual / conversational / professional / formal]
- Uses contractions: [yes / no]
- Uses humor: [yes / sparingly / no]
- Takes strong positions: [yes / sometimes / rarely]
- Sentence length tendency: [short and punchy / mixed / flowing]

### Reference Domains
- Analogies drawn from: [e.g., cooking, sports, construction]
- Cultural references: [e.g., Dutch media, tech industry, specific era]

### Pet Peeves (things this voice NEVER does)
- [e.g., "never says 'at the end of the day'"]
- [e.g., "never hedges when they have data"]
- [e.g., "never uses business jargon"]

### Example Paragraphs (2-3 samples of the target voice)
[Actual writing samples that demonstrate the voice]

### Audience
- Writing for: [specific person description]
- Their knowledge level: [beginner / intermediate / expert]
- What they care about: [specific concerns]
```

**Voice varies by channel**: A brand's blog voice differs from their product page voice differs from their social media voice. Capture voice per content type if possible. The voice document should indicate which register applies to which content format.

## Copywriting Frameworks by Content Type

| Content Type | Best Framework | Why |
|-------------|---------------|-----|
| Service pages, landing pages | PAS (Problem-Agitate-Solve) | Forces emotional engagement |
| Commercial content, reviews | AIDA (Attention-Interest-Desire-Action) | Drives decision-making |
| Brand content, about pages | StoryBrand | Positions reader as hero |
| News, definitions, how-tos | Inverted Pyramid | Answer first, expand second |
| Email-style, newsletters | Gary Halbert "One Person" | Maximum intimacy |
| Data pages, comparisons | David Ogilvy "Facts First" | Specifics over superlatives |

## Tips

- **The "swap test"**: Put a paragraph from the AI draft next to a paragraph from a real sample. If a colleague could tell which is which, the voice is not matched yet.
- **Capture negative examples too**: "We NEVER say 'leverage'" or "We NEVER use bullet points for everything" is just as important as positive voice guidelines. What the brand avoids defines the voice as much as what it does.
- **Voice varies by channel**: A brand's blog voice differs from their product page voice differs from their social media voice. Capture voice per content type.
- **Update samples regularly**: If the brand's voice evolves (it will), update the samples. Stale samples produce dated-sounding content.
- **The "30% Rule"**: At least 30% of every page should contain details no generic AI could produce.
- **Voice before anti-slop**: Apply voice injection BEFORE running anti-slop audits (Technique 02). Removing patterns without adding personality produces sterile text.

## Common Mistakes

1. **"Write engagingly"** -- too vague, produces generic friendly AI. Specify exact voice characteristics.
2. **Using generic voice descriptions**: "Professional and friendly" describes 90% of brands. Be specific: "Slightly sarcastic, data-obsessed, uses 'actually' a lot"
3. **Adding personality to every sentence** -- exhausting; let some sentences be plain
4. **Forcing humor** -- bad jokes are worse than no jokes
5. **Overusing fragments** -- occasional fragments add punch; constant fragments are a new AI pattern
6. **Fake specificity** -- inventing plausible-sounding but false examples is worse than being general
7. **Voice inconsistency** -- voice should be consistent throughout; load voice document before EVERY section
8. **Over-constraining**: Too many rules make writing stiff. Focus on 5-7 key voice markers, not 50
9. **Ignoring audience awareness**: The writer's voice adjusts to audience. A piece for CTOs sounds different than a piece for marketers, even in the same brand voice
10. **One voice for all content**: Product descriptions, thought leadership, and technical docs require different registers within the same brand voice

## Key Sources

- [Paul Graham: Write Like You Talk](https://paulgraham.com/talk.html)
- [Gary Halbert: The Boron Letters (Enchanting Marketing)](https://www.enchantingmarketing.com/gary-halbert-boron-letters/)
- [David Ogilvy's 7 Principles (Cult Method)](https://cultmethod.com/articles/ogilvys-principles/)
- [StoryBrand Framework](https://storybrand.com/)
- [blader/humanizer](https://github.com/blader/humanizer) -- "Sterile, voiceless writing is just as obvious as slop"
- [haowjy/creative-writing-skills](https://github.com/haowjy/creative-writing-skills) -- Style learning from samples
- [viktorbezdek/definitive-llm-writing-style-guide](https://github.com/viktorbezdek/definitive-llm-writing-style-guide)
