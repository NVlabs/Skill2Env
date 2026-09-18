---
name: s4h-epistemology
description: "Entry point for the epistemology toolkit. Routes to the right skill based on your situation. Use when you say 'what do I actually know here', 'is this knowable', 'how certain should I be', 'what would justify believing this', 'what kind of claim is this', 'am I confusing assumption with knowledge', 'what are the limits of what we can establish', or want philosophical rigor applied to questions of knowledge without knowing which specific tool fits."
---

# Epistemology

Applies philosophical analysis to the nature, structure, and limits of knowledge. Diagnoses what kind of epistemic work is needed and routes to the right tool.

Epistemology is the meta-layer: not "is this claim true?" but "what kind of truth could this claim even have? What would justify believing it? How certain can we actually be?" It's most useful when you've hit a wall with ordinary investigation — when more evidence-gathering won't settle things, when you're not sure what *kind* of knowing is in play, or when you want honest calibration rather than confident-sounding output.

## Which tool fits

| You need to... | Tool |
|---|---|
| Map what *kind* of knowing is in play | epistemology-knowledge-types |
| Work out what would actually *justify* believing something | epistemology-justification |
| Get honest calibration: what do I know vs. believe vs. assume vs. hope? | epistemology-epistemic-status |
| Find out what can't be known, and why — and what *can* be established | epistemology-limits |

## Routing Decision

- **"What kind of claim is this?" / "Am I reasoning from evidence, intuition, testimony, or something else?"** → knowledge-types (classify the epistemic mode before testing the claim)
- **"What would it take to actually know this?" / "What would justify believing X?"** → justification (map the justification structure and find the weakest link)
- **"How certain should I be?" / "Give me an honest read of what we know vs. assume"** → epistemic-status (calibrate and map confidence across a domain)
- **"Can this even be known?" / "We keep investigating and nothing settles it"** → limits (classify the type of limit and reframe into the answerable)
- **Unclear** → epistemic-status (starts with honest inventory of what's known, naturally surfaces which deeper question matters)

## Confirm Direction

After diagnosing which tool fits, use the `AskUserQuestion` tool to confirm direction. Construct the question dynamically to include your diagnosis:

- **Question:** "My read: **[diagnosed tool]** — [one sentence on why it fits]. How would you like to proceed?"
- **Header:** "Direction"
- **Options:**
  - **Yes, run that tool** — Execute the diagnosed skill immediately using the context already provided
  - **Show all options** — List every skill in this category with one-line descriptions
  - **Quick version** — Run a lighter-weight pass if one fits this situation
  - **Re-diagnose** — Revisit the situation description for a different read

Proceed based on their selection.

---

## Knowledge Types

*Map what kind of knowing is actually in play — before testing whether the claim is true.*

Identify the claim → classify what kind of knowing it invokes (a priori vs. a posteriori; propositional vs. procedural vs. acquaintance; sourced from perception, inference, testimony, or intuition) → assess what can and can't be established by that type. Different kinds of knowing have different standards of justification and different failure modes.

**Output:** Claim classified by knowledge type, with implications for what evidence is relevant and what the claim can and can't establish.

---

## Justification

*What would actually justify believing this?*

Identify the belief → ask what would need to be true for it to be justified → classify the justification structure (foundationalist, coherentist, or reliabilist) → identify the weakest link in the chain. A belief can feel well-supported while resting on an unjustified foundation — justification analysis makes the load-bearing structure visible.

**Output:** Justification map with the belief's foundational support structure, classification of the justification type, and the specific point where the chain is weakest.

---

## Epistemic Status

*Honest, rigorous calibration: what do you know vs. believe vs. assume vs. hope?*

Inventory all claims in a domain → assign each an epistemic status (known, reasonably believed, assumed, hoped, unknown) → trace dependencies: which high-confidence claims rest on lower-confidence foundations? Draws from the rationalist tradition of explicit epistemic labeling to replace confident-sounding vagueness with precise, honest calibration.

**Output:** Structured epistemic status map across the domain, with dependency chains flagged where confident claims rest on shakier ground.

---

## Limits

*What can't be known here, and why — and what *can* be established within those limits?*

Identify what you're trying to know → classify the type of limit if one exists (fundamental: Gödel-style, underdetermination, observer effects; practical: evidence unavailable, destroyed, or counterfactual; conceptual: the question may be malformed) → clarify what *can* be established within those limits → reframe the question into the answerable part. The point is not to conclude "we can't know" — it's to be precise about what kind of knowing is and isn't available.

**Output:** Limit classification, what remains establishable, and a reframed question targeting the knowable.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Epistemology applied. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-investigation` — Apply practical investigation methods to what epistemology clarified
  - `/s4h-probability-confidence-calibration` — Calibrate your confidence given the epistemic analysis
  - `/s4h-logic-check` — Validate reasoning built on the epistemic foundations
  - **Done** — Wrap up and synthesise what we have so far
