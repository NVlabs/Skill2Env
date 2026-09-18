---
name: s4h-linguistics-semantic-drift
description: "Tracks how meanings shift over time or across groups — concept creep, definition drift, and what it costs when words change. Use when you say 'this word doesn't mean what it used to', 'people are using this term differently now', 'this definition has been captured', 'concept creep', 'the word has been weaponised', 'we need to define our terms', or when a key term is contested or means different things to different audiences."
---

# Linguistics: Semantic Drift

Words do not hold still.

"Literally" now means "figuratively" in common usage. "Decimate" originally meant to kill one in ten; it now means to devastate. "Woke" migrated from an African-American vernacular expression of political awareness to a mainstream progressive identity marker to a political pejorative — in roughly fifteen years. These shifts are not merely interesting: they change what arguments are available, which coalitions are possible, and what policies feel legitimate.

Ludwig Wittgenstein's later philosophy provides the theoretical grounding: words do not have fixed meanings determined by their reference to the world. They have meanings determined by use — by the language games people play with them in particular contexts and communities. When the community changes, the game changes, and the word changes with it.

Semantic drift takes several forms. Natural drift is organic evolution through changing usage — inevitable, mostly benign, occasionally confusing. Concept creep, identified by Nick Haslam, is the expansion of a concept's boundaries, typically in psychology and social discourse: "trauma", "addiction", and "abuse" have all expanded substantially from their clinical origins, gaining explanatory power and losing diagnostic precision simultaneously. Deliberate semantic capture is strategic: political and commercial actors invest in changing what a word means because the word controls a contested domain. "Freedom", "natural", "sustainable", and "wellness" are all sites of ongoing definitional struggle.

This skill traces a word's semantic trajectory, identifies the mechanism of drift, and assesses the consequences of the shift.

---

## Your Process

**Step 1: Establish the Starting Point**
Identify the term or concept under analysis. Establish its origin meaning:
- The technical or etymological original (if relevant)
- The commonly understood meaning at a specific historical moment
- The formal or disciplinary definition if one exists

If the drift is cross-group rather than historical (the word means different things to different communities simultaneously), establish the different meanings currently in play and who holds each.

**Framing check:** Confirm the term and the semantic analysis task before continuing. State what you've identified — the term being analyzed and whether the drift is historical, cross-community, or both — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [one-sentence description of the term and the drift situation — historical shift, cross-group divergence, or active definitional contest]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Map the Semantic Trajectory**
Trace how the meaning has changed. For historical drift, identify the key moments of change and what drove them. For cross-group divergence, map the different current meanings and the communities that hold them. The trajectory should include:
- **Original meaning:** Denotation, connotation, and typical usage context
- **Intermediate states:** Key shifts along the way, with approximate dating and cause
- **Current meaning(s):** What the word denotes and connotes now, and for which audiences
- **Trajectory direction:** Expansion (concept creep), narrowing, value inversion, polysemy (multiple stable meanings in use simultaneously)

**Step 3: Identify the Mechanism**
How did the drift occur? Name the mechanism:
- **Organic evolution:** Natural change through use, generational shift, cultural mixing — no identifiable agent
- **Concept creep:** Boundary expansion, typically in normative domains, often driven by motivated extension of a powerful or legally relevant category
- **Strategic capture:** Deliberate investment by political or commercial actors in shifting a term to control the domain it covers
- **Domain transfer:** A technical term moves to general use and loses precision (or gains expressive power)
- **Irony/reclamation:** A community takes a pejorative term applied to them and revalues it; the pejorative often persists among its original users

**Before assessing consequences:** Present the trajectory and mechanism mapping. Use `AskUserQuestion`:
- **Question:** "I've traced the semantic trajectory and identified the mechanism. Before assessing consequences: is there a specific context you care about — a field, an audience, a decision — where the drift has particular stakes for you?"
- **Header:** "Stakes"
- **Options:**
  - **Full consequences assessment** — map the costs and benefits of the drift across contexts
  - **Focus on a specific context** — user will name the domain or audience; focus there
  - **Focus on practical implications** — how to communicate clearly given the current state of drift
  - **Proceed as read** — assess across the full range

**Step 4: Assess the Consequences**
The drift is a fact; its consequences depend on context. Assess:
- **What the drift enables:** New arguments, new policies, new categories of people or actions that can now be named — or dismissed
- **What the drift costs:** Precision lost, coalitions fractured, concepts that can no longer do the analytical work they once did
- **Who benefits from the drift:** Which parties gain from the new meaning? Which lose?
- **Whether the drift is stable:** Is the meaning settling, or is the term currently in active definitional contest? A term in contest is a term where the battle is still winnable.

**Step 5: Identify the Strategic Implications**
Given the trajectory and the consequences, what should someone do with this information?
- If using the term: which meaning should they signal, and how? Which audiences require disambiguation?
- If contesting the drift: is definitional rollback possible, or is the new meaning entrenched? What is the counter-strategy?
- If designing communication: should they use the term at all, define it explicitly, or find an alternative that carries less contested freight?

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences, then ask:

- **Question:** "My read: [your 1–2 sentence interpretation of the term, the type of drift, and what you'll analyze]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete trajectory, mechanism, consequences, and strategic implications
  - **Key findings only** — The bottom line: what the drift is, what caused it, and what it costs
  - **Strategic focus** — What to do about the drift, given my context
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

**Term:** [the word or phrase under analysis]

**Semantic Trajectory**

| Stage | Meaning | Context | Timeframe/Community |
|---|---|---|---|
| Original | | | |
| [Shift 1] | | | |
| Current | | | |

**Mechanism:** [named mechanism with one-paragraph explanation of how it operated in this case]

**Consequences**

- **What the drift enables:** [specific argument, policy, or category made available or closed]
- **What the drift costs:** [precision lost, coalitions fractured, analytical capacity reduced]
- **Who benefits:** [parties advantaged by the new meaning]
- **Stability:** [is the meaning settled or actively contested?]

**Strategic Implications**
What to do with this analysis — whether using the term, contesting the drift, or designing around it.

---

## Notes

Semantic drift analysis sits at the intersection of linguistics, political theory, and strategic communication. The key Wittgensteinian insight — that meaning is use — means that no term is permanently secured. This is both a vulnerability (terms you rely on can be captured) and an opportunity (terms that have been captured can sometimes be reclaimed).

The nearest-neighbor trap: confusing semantic drift with euphemism. Euphemism is a deliberate act of renaming to soften; semantic drift is a structural change in meaning that happens to a term regardless of intention. A word can drift without anyone intending to euphemize it, and a euphemism can be introduced without causing drift if it doesn't enter the semantic system.

This skill pairs naturally with `/s4h-linguistics-framing` (the drift often reflects a frame change) and `/s4h-epistemology-epistemic-status` (when a drifted term is being used as a knowledge claim that relies on one of its contested meanings).

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Semantic trajectory mapped. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-linguistics-framing` — Examine the framing shift that drove or followed the semantic drift
  - `/s4h-linguistics-connotation` — Audit the current connotative freight of the term in detail
  - `/s4h-epistemology-epistemic-status` — Assess whether arguments relying on this term are using a consistent or contested meaning
  - **Done** — Wrap up and synthesise what we have so far
