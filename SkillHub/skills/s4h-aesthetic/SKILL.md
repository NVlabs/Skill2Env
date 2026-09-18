---
name: s4h-aesthetic
description: "Entry point for the aesthetic toolkit. Routes to the right aesthetic skill based on your situation. Use when you say 'aesthetic', 'check the design', 'does this feel right', 'is this elegant', 'is this too complex', 'what pattern is this', 'find the simpler version', or want an aesthetic lens applied without knowing which specific tool fits."
---

# Aesthetic

Applies aesthetic reasoning to any artifact — design, writing, code, product, argument. Diagnoses what kind of aesthetic question is being asked and applies the right tool.

## Which tool fits

| You need to... | Tool |
|---|---|
| Check whether parts form a unified whole | coherence-check |
| Test whether something is more complex than it needs to be | elegance-testing |
| Name the underlying structural pattern at work | pattern-detection |
| Find the simpler version while preserving what matters | simplicity-analysis |

## Routing Decision

- **Something feels off, jarring, or inconsistent** → coherence-check
- **Something feels over-engineered or baroque** → elegance-testing
- **You want to understand *why* something works (or doesn't)** → pattern-detection
- **You want to strip something back to its core** → simplicity-analysis
- **Unclear** → start with coherence-check; it usually surfaces which other question needs answering

**Framing check:** Confirm the specific artifact before routing. State what you've identified — the actual object being analyzed and the aesthetic question being asked — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the artifact and the aesthetic question]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

---

## Confirm Direction

After diagnosing which tool fits, use the `AskUserQuestion` tool to confirm direction. Construct the question dynamically to include your diagnosis:

- **Question:** "My read: **[diagnosed tool]** — [one sentence on why it fits]. How would you like to proceed?"
- **Header:** "Direction"
- **Options:**
  - **Yes, run that tool** — Execute the diagnosed skill immediately using the context already provided
  - **Show all options** — List every skill in this category with one-line descriptions
  - **Quick version** — Run a lighter-weight alternative if one exists for this situation
  - **Re-diagnose** — Revisit the situation description for a different read

Proceed based on their selection.

---

## Coherence Check

*Tests whether the parts form a unified whole.*

Map all major elements of the artifact. For each: what design decision does it express? Ask: are these decisions speaking the same language — or were they made independently, without reference to each other? Name each incoherence specifically. Classify: surface incoherence (fixable with small changes) vs. structural incoherence (requires rethinking something fundamental).

**Output:** List of incoherences ranked by severity. For each: what it is, where it appears, what it conflicts with, and how to resolve it.

---

## Elegance Testing

*Tests whether something is more complex than it needs to be.*

Separate necessary complexity (required by the problem) from accidental complexity (accreted over time, added as hedging, or left over from old requirements). For each layer of complexity: could the same job be done without it? What would be lost? Apply the minimum surface principle — is every part earning its place?

**Output:** Complexity audit — each complex element classified as necessary or accidental, with a cost estimate for removing it.

---

## Pattern Detection

*Identifies the underlying formal pattern.*

Look past the surface. What structural form does this follow? Name candidate patterns. Test each: does the structure actually match, or just superficially resemble it? Once identified: what does naming the pattern unlock? What's the established playbook for this form?

**Output:** Named pattern, evidence for the identification, what the pattern predicts or implies, and the playbook it suggests.

---

## Simplicity Analysis

*Finds the simpler version while preserving what matters.*

First: what is the core? The irreducible thing this artifact must do or be. Now audit everything else against that core: does each element serve it, or distract from it? For everything that doesn't serve the core, ask whether it was added for a reason that's still valid.

**Output:** What the core is. What can go. What should stay but be simplified. The simplest version that still does the full job.
