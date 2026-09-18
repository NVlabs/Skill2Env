---
name: s4h-aesthetic-pattern-detection
description: "Identifies the underlying formal pattern at work — because most successful designs, arguments, and solutions share deep structural patterns, and naming the pattern unlocks the playbook. TRIGGERS: 'what pattern is this', 'pattern recognition', 'why does this work', 'identify the form', 'what structure is at play', 'what archetype is this'."
---

# Aesthetic Pattern Detection

Surface features differ — colours, words, technologies, industries. Formal patterns
recur across all of them. The same structural moves that make a symphony compelling
make a strategy compelling. The same tension-and-resolution arc that drives a thriller
drives a great pitch. Naming the pattern reveals options that surface-level analysis
cannot, because once the pattern is named, its full playbook becomes available.

---

## Your Process

**Step 1: Describe the Thing**
What does it do and how does it feel to engage with it? Focus on behaviour and
effect, not surface features — not "it uses blue and white" but "it creates calm
authority that builds confidence incrementally." Describe the experience of it.

**Framing check:** Confirm the specific artefact before continuing. State what you've identified — the actual object being analyzed and its medium or domain — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the specific artefact and its context]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different artefact or context than read; incorporate the correction before proceeding

**Step 2: Identify Formal Patterns Present**
Work through this list systematically — multiple patterns often operate simultaneously:
- **Repetition/Rhythm** — recurring elements that create expectation, then satisfy
  or productively subvert it
- **Symmetry/Asymmetry** — balance creates stability and trust; deliberate
  asymmetry creates tension and dynamism
- **Hierarchy** — clear ordering from most to least important, large to small,
  general to specific; guides attention
- **Contrast** — sharp differences that create definition, focus attention, and
  make meaning by comparison
- **Tension/Resolution** — a problem introduced and resolved, a question posed and
  answered; the engine of narrative
- **Figure/Ground** — a subject made vivid and clear by what surrounds and recedes
- **Part/Whole** — components that build into something greater than their sum

**Step 3: Match to Domain Archetypes**
Which archetypes from design, storytelling, architecture, or music does this
resemble? The hero's journey. The fugue. The golden section. Thesis-antithesis-
synthesis. Call and response. Name the archetype and its source domain.

**Step 4: Name the Pattern**
**Before narrowing:** Show the complete set of patterns identified in Step 2 to the user first. Use `AskUserQuestion`:
- **Question:** "I've identified [N] patterns at work. Before I select the dominant one, are there any you'd flag as especially significant, or any I've missed?"
- **Header:** "Prioritise"
- **Options:**
  - **Proceed with your selection** — the set looks right
  - **Flag one** — user will name a specific pattern to treat as dominant
  - **Add a missing one** — user will describe a pattern not yet identified

Give the dominant pattern a precise name. Test: does naming it make the thing more
legible? Does it reveal why certain elements work and why others feel off? A good
pattern name is generative — it produces new options, not just descriptions.

**Step 5: Apply the Pattern**
What does the pattern imply for what should come next? What is currently in the
artefact that violates the pattern — and is that violation intentional (productive
tension) or accidental (incoherence)?

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Pattern name only** — Identify and name the underlying structure, skip full analysis
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

**Formal Patterns Present:** [list each pattern with one sentence on how it manifests]

**Archetype Match:** [closest domain archetype + which domain it comes from]

**Pattern Name:** [precise name for the dominant pattern]

**What Naming It Reveals:** [what becomes visible or legible that wasn't before]

**Pattern Implications**

| Implication | Description |
|---|---|
| What should come next | [the move the pattern calls for] |
| What is violating the pattern | [specific elements that break it] |
| Intentional or accidental | [productive subversion or incoherence] |

---

## Notes

Not every successful thing follows a single pattern cleanly — most operate with
several simultaneously. Identify the dominant pattern first; note secondary patterns
separately. The test of a good pattern name is whether it generates new options
rather than just describing what's already there.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Patterns detected. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-aesthetic-coherence-check` — Check that detected patterns cohere
  - `/s4h-systems-archetype-matching` — Match aesthetic patterns to systemic archetypes
  - `/s4h-aesthetic-elegance-testing` — Test the elegance of the patterns
  - **Done** — Wrap up and synthesise what we have so far
