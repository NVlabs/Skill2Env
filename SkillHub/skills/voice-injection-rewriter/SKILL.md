---
name: voice-injection-rewriter
description: Use when rewriting AI-generated text to match a specific person's or brand's authentic voice. Use when AI output sounds generic, corporate, or detectable. Unlike generic "humanizers," this skill requires voice analysis input and produces voice-consistent output, not fake imperfections.
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Voice Injection Rewriter

> Transform AI-generated text into authentic, voice-consistent content — not by faking humanity, but by applying real voice patterns from a specific person or brand.

## When to Use This Skill

Use this skill when you need to:

- **Rewrite AI drafts** to match a specific person's voice
- **Strip AI fingerprints** from generated content before publishing
- **Enforce voice consistency** across AI-assisted content production
- **Bridge the gap** between AI efficiency and authentic brand expression
- **Post-process any AI output** (blog posts, emails, social, landing pages)

This skill is NOT a generic "humanizer." It requires voice input — either from `brand-voice-learner` output, ClawFu brand memory, or voice samples you provide.

**Why this matters:** Generic humanizers add fake imperfections (random typos, forced contractions) to trick detectors. That's an arms race you lose. This skill applies YOUR voice patterns — which produces naturally human text because it IS the voice of a real human.

---

## Methodology Foundation

**Core Principle:** AI text sounds artificial not because it lacks typos, but because it lacks a specific person's vocabulary, rhythm, opinions, and structural habits. The fix is voice injection, not cosmetic imperfection.

**Sources:**
- NN/g Voice and Tone research
- Brand voice analysis methodology (ClawFu `brand-voice-learner`)
- AI detection pattern research (GPTZero, Originality.ai signal analysis)
- WhatsApp IA NDD Camp community insights on AI content workflows

**The 201 insight:** Most people try to make AI text "sound human" (generic). The actual skill is making AI text "sound like ME" (specific). The first is commodity. The second is craft.

---

## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Applies voice patterns to rewrite text | Which voice profile to use |
| Strips AI detection signals | How far to deviate from the original |
| Identifies voice mismatches | Final approval of tone and accuracy |
| Suggests voice-consistent alternatives | Where factual precision overrides voice |
| Runs enforcement checklists | Publication context and audience |

---

## Instructions

### Prerequisites

Before using this skill, you need ONE of these:

| Voice Source | How to Get It | Quality |
|-------------|---------------|---------|
| **ClawFu brand memory** | `get_brand [name]` — pre-stored voice profile | Best |
| **brand-voice-learner output** | Run the analysis skill on 10+ writing samples | Very good |
| **3-5 writing samples** | Paste examples of the target voice | Good |
| **Voice description** | "Analytical, dry, French, no buzzwords, short sentences" | Minimum viable |

---

### Phase 1: Voice Profile Load

Start by establishing the voice you're targeting.

**If using ClawFu brand memory:**
```
Load brand voice for [name]. Apply it to rewrite the following text.
```

**If providing samples:**
```
Here are 3 examples of my writing voice:
[Sample 1]
[Sample 2]
[Sample 3]

Extract the voice patterns, then rewrite this AI-generated text to match:
[AI text]
```

**If describing voice:**
```
My voice profile:
- Register: [analytical/casual/authoritative/conversational]
- Sentence length: [short punchy / mixed / long flowing]
- Contractions: [always / sometimes / never]
- Opinions: [strong and stated / subtle / neutral]
- Vocabulary: [technical / accessible / mixed]
- Signature moves: [specific habits — e.g., "Ce n'est pas X. C'est Y."]
- Forbidden words: [list any words you never use]

Rewrite this to match:
[AI text]
```

---

### Phase 2: AI Fingerprint Detection

Before rewriting, identify what makes the text sound AI-generated.

#### AI Detection Signals (What to Flag)

**Structural signals:**
- Uniform sentence length (AI defaults to 15-20 words per sentence)
- Predictable paragraph structure (topic sentence → 3 supporting points → transition)
- Symmetrical lists (every bullet same length, same grammatical structure)
- Perfect parallelism in headers

**Vocabulary signals:**
- Corporate buzzwords nobody actually says: "delve," "landscape," "leverage," "robust," "streamline," "facilitate," "comprehensive"
- Filler openings: "In today's rapidly evolving...", "It's important to note that...", "In order to..."
- Over-hedging: "It's worth noting," "One might argue," "It could be said"
- Transition addiction: "Moreover," "Furthermore," "Additionally," "However" (every paragraph)

**Tonal signals:**
- No opinions (AI stays neutral by default)
- No contractions (AI under-uses them)
- Equal weight to everything (AI doesn't emphasize or deprioritize)
- Sanitized language (no edge, no personality, no risk)

**Flag template:**
```
AI FINGERPRINT SCAN:
□ Uniform sentence length? [yes/no]
□ Buzzword count: [N] instances
□ Transition density: [N] per paragraph
□ Contractions present? [yes/no]
□ Opinions/personality present? [yes/no]
□ Any sentence you'd never actually say? [list]
```

---

### Phase 3: Voice Injection Rewrite

Apply the voice profile to the flagged text. This is the core operation.

#### The 5-Pass Rewrite

**Pass 1 — Kill AI vocabulary**

Replace every AI-default word with the voice-appropriate equivalent:

| AI Default | Generic Human | Voice-Specific (example) |
|------------|--------------|-------------------------|
| "Delve into" | "dig into" | Depends on voice — could be "creuser," "regarder de plus près," "explorer" |
| "Leverage" | "use" | Voice may prefer "exploiter," "utiliser," or "s'appuyer sur" |
| "Landscape" | "space" | Voice may prefer "marché," "écosystème," or just name the thing |
| "Robust" | "strong" | Voice may prefer "solide," "fiable," or a domain-specific term |
| "Moreover" | "Plus" | Voice may prefer "Et," "D'ailleurs," or nothing at all |
| "Ensure" | "make sure" | Voice may prefer "vérifier," "s'assurer," or just drop it |
| "Comprehensive" | "full" | Voice may prefer "complet," "exhaustif," or cut the word entirely |
| "It is important to note" | (cut) | Replace with direct statement of the thing |

**Pass 2 — Break rhythm uniformity**

- Find the longest streak of same-length sentences. Break it.
- Add 2-3 short punches per section (under 8 words). "That's the point." "Not even close."
- Allow 1-2 longer flowing sentences if the voice uses them
- Fragments are OK if the voice uses fragments
- Dashes—for emphasis—if the voice does that
- Parentheticals (if the voice thinks while writing)

**Pass 3 — Inject voice-specific patterns**

Pull from the voice profile:
- Signature phrases or rhetorical moves
- Preferred sentence openers
- Opinion-stating patterns ("Ce n'est pas X. C'est Y." / "Here's the thing" / "Look,")
- Domain-specific vocabulary the voice always uses
- Structural habits (bullets vs. flowing prose, numbered lists vs. paragraphs)

**Pass 4 — Contraction and register pass**

- Apply contraction level matching the voice (some voices never contract, some always do)
- Check register: is the formality level consistent with the voice?
- Verify pronoun usage matches (some voices are "nous," some are "je," some are "on")

**Pass 5 — Read-aloud test**

Read the full text aloud. For each sentence ask:
- Would [person] actually say this?
- Does it flow at their pace?
- Is there any word they'd never use?

If any sentence fails, rewrite that sentence from scratch in the voice.

---

### Phase 4: Output Format

#### Standard Output

```markdown
## Original (AI-generated)
> [The input text]

## Rewritten (Voice: [Name/Brand])
[The rewritten text]

## Changes Made
- **Vocabulary**: [3-5 key word swaps]
- **Rhythm**: [What changed structurally]
- **Voice markers**: [What was injected from the voice profile]
- **Removed**: [What AI signals were stripped]

## Voice Consistency Score
[High/Medium/Low] — [one-line explanation]
```

#### Quick Mode (For batch processing)

If rewriting multiple pieces, skip the detailed output:

```markdown
[Rewritten text only]

---
*Voice: [Name] | Swaps: [N] | Score: [H/M/L]*
```

---

## Examples

### Example 1: LinkedIn Post — Analytical French Voice

**Voice Profile:** Matthieu Credou — Analytical-first, dry, short sentences, "Ce n'est pas X. C'est Y." recadrage, no buzzwords, no emojis, 201 level

**AI Input:**
> "In today's rapidly evolving digital landscape, leveraging AI-powered tools has become essential for businesses seeking to maintain their competitive edge. Moreover, organizations that fail to adopt these comprehensive solutions risk falling behind in an increasingly automated marketplace."

**Rewritten (Voice: Matthieu):**
> Tout le monde dit qu'il faut "adopter l'IA" pour rester compétitif. Ce n'est pas un problème d'adoption. C'est un problème de savoir quoi en faire.
>
> La plupart des boîtes installent des outils IA comme on installe un ERP — par obligation, sans stratégie. Résultat : elles automatisent leurs erreurs plus vite.

**Changes Made:**
- **Vocabulary**: "landscape" → cut, "leveraging" → cut, "comprehensive solutions" → cut, "competitive edge" → reframed as the actual problem
- **Rhythm**: Broke uniform long sentences into short punch + development
- **Voice markers**: "Ce n'est pas X. C'est Y." recadrage, opinion ("par obligation, sans stratégie"), concrete metaphor (ERP)
- **Removed**: "In today's...", "Moreover", hedging, the entire premise (flipped it)

**Voice Consistency Score:** High — matches analytical register, uses signature recadrage, no buzzwords

---

### Example 2: Product Email — Casual Brand Voice

**Voice Profile:** Startup brand — casual, contractions always, "Here's the thing" opener, short paragraphs, second person, anti-corporate

**AI Input:**
> "We are pleased to announce that our platform now offers a comprehensive suite of analytics tools designed to empower teams to make data-driven decisions. These robust features include real-time dashboards, automated reporting, and customizable metrics tracking."

**Rewritten (Voice: Brand):**
> Here's the thing — we just shipped analytics. Real dashboards, automated reports, and metrics you actually set up yourself.
>
> No more exporting CSVs at 11pm to make a chart for Monday's meeting. Your data's right there. Live.

**Changes Made:**
- **Vocabulary**: "pleased to announce" → "just shipped," "comprehensive suite" → cut, "empower" → cut, "robust" → cut, "customizable" → "you actually set up yourself"
- **Rhythm**: Long formal sentences → short punchy + one fragment ("Live.")
- **Voice markers**: "Here's the thing" opener, contractions (we're, that's, your data's), relatable scenario (CSVs at 11pm)
- **Removed**: All corporate filler, passive construction, feature-first framing (replaced with problem-first)

**Voice Consistency Score:** High — casual, direct, anti-corporate, relatable

---

### Example 3: Blog Post — Technical but Accessible

**Voice Profile:** Tech consultant — uses analogies, explains jargon inline, mixed sentence length, "In practice" as a pivot phrase, occasional rhetorical questions

**AI Input:**
> "Implementing a microservices architecture requires careful consideration of service boundaries, inter-service communication protocols, and data consistency patterns. Organizations should ensure that their teams possess the requisite expertise to manage the increased operational complexity inherent in distributed systems."

**Rewritten (Voice: Consultant):**
> Microservices sound great in conference talks. In practice, they mean your team now manages 40 tiny services instead of one big app — and every service needs to talk to every other service without losing data along the way.
>
> The question isn't whether microservices are better. It's whether your team can handle the operational overhead. If you're struggling with one monolith, splitting it into 40 pieces doesn't fix the problem. It multiplies it.

**Changes Made:**
- **Vocabulary**: "requisite expertise" → "whether your team can handle," "inherent in" → cut, "ensure" → cut
- **Rhythm**: Dense abstract sentences → analogy + rhetorical question + concrete scenario
- **Voice markers**: "In practice" pivot, rhetorical question, analogy (40 tiny services), opinion in closing line
- **Removed**: Passive voice, abstract recommendations, jargon without explanation

**Voice Consistency Score:** High — explains by analogy, rhetorical questions, "In practice" pivot present

---

## Skill Boundaries

### What This Skill Does Well
- Rewriting AI text to match a specific documented voice
- Stripping AI detection signals systematically
- Enforcing voice consistency across content types
- Bridging AI efficiency with authentic voice expression

### What This Skill Cannot Do
- Create a voice from nothing (you need samples or a profile)
- Guarantee undetectable output (detectors evolve, and the goal isn't deception anyway)
- Replace genuine expertise (voice-matched text that's factually wrong is still wrong)
- Work well with minimal voice input (garbage in → generic out)

### Important Distinction

This skill makes AI output sound like a specific human — not "human in general." Generic humanization (adding random typos, forced slang, fake imperfections) is:
1. An arms race with detectors you'll lose
2. Not what good writing looks like
3. Unnecessary if you have a real voice to inject

The goal is **authenticity**, not **deception**.

---

## Iteration Guide

**Follow-up prompts:**
- "Tighten the voice — it's still too formal for [name]"
- "Rewrite just paragraph 3, the rest is good"
- "Switch to [channel] register (social instead of blog)"
- "The opinion isn't strong enough — [name] would take a harder stance here"
- "Run the AI fingerprint scan on this new draft"

---

## References

**Methodology:**
- NN/g Voice and Tone Guidelines
- ClawFu `brand-voice-learner` skill (voice analysis methodology)
- AI detection research: GPTZero, Originality.ai signal patterns

**Community Input:**
- WhatsApp IA NDD Camp — Cyril Frémont's "mega prompt" for AI text humanization (inspiration for the kill list, reframed from deception to authenticity)

---

## Related Skills

- **brand-voice-learner** — Extract voice patterns from existing content (prerequisite)
- **copywriting-ogilvy** — Writing craft foundations
- **seo-content-writer** — SEO content that needs voice enforcement post-generation
- **llm-optimized-content** — GEO content that needs voice injection for E-E-A-T
- **storytelling-storybrand** — Narrative voice framework

---

## Skill Metadata

```yaml
name: voice-injection-rewriter
category: content
subcategory: voice
version: 1.0.0
author: GUIA
source_expert: NN/g Voice Research + ClawFu brand-voice-learner methodology + Cyril Frémont (WhatsApp IA NDD Camp community)
difficulty: intermediate
mode: cyborg
tags: [voice, rewriting, ai-detection, brand-voice, authenticity, humanization, content-editing]
created: 2026-02-10
updated: 2026-02-10
```
