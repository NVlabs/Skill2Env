---
name: s4h-cognition-cognitive-load
description: "Manages the limits of working memory — chunking, offloading, and reducing unnecessary complexity to free capacity for what matters. Use when asked 'this is too complex to hold in my head', 'I keep losing track of where I am', 'how do I make this simpler to think about', 'the design is overwhelming', 'people aren't retaining this', or when information architecture, learning design, or communication complexity needs to be optimised for working memory limits."
---

# Cognition: Cognitive Load

Working memory is where thinking happens — and it is brutally limited. George Miller's landmark 1956 paper "The Magical Number Seven, Plus or Minus Two" established that the human working memory holds roughly seven chunks of information simultaneously. John Sweller's Cognitive Load Theory, developed in the 1980s and 1990s, gave this biological limit practical teeth: not all cognitive demands are equal, and the way information is presented and structured has a direct, measurable effect on whether working memory is overwhelmed or just well-used.

Sweller identified three types of cognitive load. **Intrinsic load** is the inherent complexity of the material itself — the number of interacting elements you must hold simultaneously to understand it. This is not reducible without changing what you're learning or deciding. **Extraneous load** is imposed by poor presentation, bad design, or unnecessary complexity — the information architecture overhead that has nothing to do with the actual task. This is waste, and it should be eliminated. **Germane load** is the productive cognitive effort that builds new schemas — the mental work of genuinely learning and integrating new material. The goal of cognitive load management is to eliminate extraneous, manage intrinsic through chunking, and protect germane.

This matters beyond education and training design. Any time you're trying to think clearly about something complex — designing a system, explaining a strategy, making a high-stakes decision — you are operating under cognitive load constraints. The person whose whiteboard is chaotic is not failing at organisation; they are failing at working memory management. The strategic plan that no one can remember after the meeting is not a communication failure; it is a cognitive load failure.

---

## Your Process

**Step 1: Define the Cognitive Task and User**
What is the specific cognitive task — what must be held in working memory to accomplish it? And who is doing it — what is their likely baseline expertise in this domain? (Expert schemas compress intrinsic load dramatically; novices experience raw element interactivity.)

**Framing check:** Confirm the specific cognitive task and the person performing it before continuing. State what you've identified — the task, the domain complexity, and who is trying to hold it — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the specific cognitive task, its complexity, and who needs to perform it]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Diagnose Load Type Distribution**
Analyse what's currently contributing to cognitive load and classify each source:

- **Intrinsic load sources:** the genuinely complex elements that must be held simultaneously (number of interacting variables, depth of dependency, novel concepts without existing schemas)
- **Extraneous load sources:** presentation and design overhead — split attention (related information in separate places), redundancy (same information presented multiple times in slightly different forms), poor sequencing (concepts introduced before their prerequisites), and unnecessary detail
- **Germane load sources:** the productive schema-building work — the genuine cognitive effort of integrating and understanding the material

**Step 3: Assess Overload Risk**
Where is the total load (intrinsic + extraneous) approaching or exceeding working memory capacity? Signs of overload: task switching increases, errors cluster, retention drops, the person starts losing track of earlier steps while working on later ones. Identify the bottleneck — the point where load spikes and capacity is most strained.

**Before narrowing:** Use `AskUserQuestion` to share the diagnosis before prescribing solutions:
- **Question:** "I've mapped the load sources. The primary pressure point is [brief summary — the highest-load moment and its type]. Before I recommend interventions, does this match your experience of where the difficulty is concentrated?"
- **Header:** "Load Diagnosis"
- **Options:**
  - **Yes — that's the pressure point** — proceed to interventions
  - **Different pressure point** — user will describe where difficulty actually clusters
  - **Add a load source** — user will identify something missing from the map

**Step 4: Apply Load Reduction Strategies**
For each load type, apply the appropriate strategy:

**For extraneous load (eliminate):**
- *Contiguity:* Move related information adjacent to each other — spatially and temporally. Eliminate split-attention effects.
- *Redundancy reduction:* Remove re-statements of the same information in different forms. Redundancy feels helpful but costs working memory.
- *Segmentation:* Break continuous streams of complexity into discrete segments with natural completion points.
- *Signalling:* Make structure explicit — headings, numbering, explicit transitions — so orientation doesn't consume working memory.

**For intrinsic load (manage through chunking):**
- *Chunking:* Group related elements into a single labelled unit. Instead of holding 7 variables, hold 3 chunks. Miller's "magical number" applies to chunks, not individual elements.
- *Sequencing:* Introduce prerequisite concepts before dependent ones. Never make the learner hold a concept they can't yet connect to anything.
- *Worked examples:* Provide complete examples before asking for application. Reduces the load of problem-solving while building schema.

**For germane load (protect and scaffold):**
- *Variability:* Expose the same concept in multiple contexts to build robust schemas.
- *Self-explanation prompts:* Encourage active processing — "what does this imply?" rather than passive absorption.
- *Progressive complexity:* Start with simplified models; add complexity once the core schema is formed.

**Step 5: Design the Offloading Strategy**
Extend effective working memory beyond its biological limit by externalising:
- **What to offload:** intermediate results, lists, diagrams, decision trees, annotated examples — anything that can be represented externally rather than held mentally
- **When to offload:** at every natural completion point — don't carry completed work forward in working memory; record it and clear it
- **How to design the external representation:** the offload system should reduce retrieval load, not add it; well-designed notation or diagrams should let the eye do some of the work that would otherwise fall to working memory

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what the primary cognitive load problem is and where the working memory ceiling is being hit — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Load type breakdown, bottleneck diagnosis, full intervention set, offloading strategy
  - **Quick wins** — Identify the two or three highest-impact extraneous load reductions
  - **Redesign the structure** — Focus on chunking and sequencing the material for maximum learnability or usability
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

**Load Type Breakdown**

| Source | Load Type | Severity | Reducible? |
|---|---|---|---|
| | Intrinsic / Extraneous / Germane | High / Medium / Low | Yes / No |

**Bottleneck:** [The point where load peaks and what causes it]

**Interventions**

| Load Type | Strategy | Specific Action |
|---|---|---|
| | | |

**Offloading Plan:** [What to externalise, when, and in what form]

**Redesigned Structure (if applicable):** [Chunked, sequenced version of the material or task]

---

## Notes

Cognitive load management is not about making things simpler than they are — it is about not making them harder than they need to be. The goal is to eliminate extraneous load (which serves no cognitive purpose) while protecting the intrinsic and germane load that is doing real work.

The nearest neighbor is `/s4h-cognition-attention` — which addresses whether sustained focus is possible at all. Attention is the gateway (can you engage?); cognitive load is the capacity question (can you hold the complexity once you're engaged?). For complex problems, both need addressing.

For communication and presentation design specifically, pair with `/s4h-communication-clarity-audit` — which evaluates whether the message structure is serving or taxing the audience.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Cognitive load analysis complete. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-cognition-attention` — Ensure sustained attention is protected so reduced load can be used effectively
  - `/s4h-communication-clarity-audit` — Apply cognitive load principles to a specific communication or document
  - `/s4h-cognition-metacognition` — Assess whether your monitoring of your own comprehension is keeping pace with the complexity
  - **Done** — Wrap up and synthesise what we have so far
