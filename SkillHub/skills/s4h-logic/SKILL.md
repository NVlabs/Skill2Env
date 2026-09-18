---
name: s4h-logic
description: "Entry point for the logic toolkit. Routes to the right logic skill based on your situation. Use when you say 'logic', 'is this sound', 'check my reasoning', 'find the flaw', 'fix this argument', 'find contradictions', 'map the dependencies', 'map the constraints', or want logical analysis applied without knowing which specific tool fits."
---

# Logic

Applies logical analysis to arguments, plans, reasoning, and systems. Diagnoses what kind of logical work is needed and applies the right tool.

## Which tool fits

| You need to... | Tool |
|---|---|
| Full council pressure-test with peer review | logic-council |
| Fast comprehensive logic report | logic-check |
| Validate whether premises support a conclusion | argument-validation |
| Find internal contradictions in a document or spec | consistency-check |
| Map causal relationships and dependencies | causality-mapping |
| Map the constraint landscape for a decision or plan | constraint-mapping |
| Fix broken reasoning — not just diagnose, but repair | logic-fixer |

## Routing Decision

**Framing check:** Confirm the argument or reasoning being examined before routing. State the argument being examined and the claim at stake in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the specific argument or reasoning and what's at stake]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

- **Complex argument worth thorough pressure-testing** → logic-council (multi-advisor + peer review)
- **Need a complete logic review quickly** → logic-check (all dimensions, no overhead)
- **Specific argument with a conclusion that needs validating** → argument-validation
- **Document or spec that might contain contradictions** → consistency-check
- **Need to understand what causes what, or what breaks if X changes** → causality-mapping
- **Unclear what's actually negotiable or fixed in a situation** → constraint-mapping
- **Have broken reasoning and want it repaired** → logic-fixer
- **Unclear** → logic-check (comprehensive starting point that surfaces which deeper tool is needed)

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

## Logic Check

*Fast comprehensive logic report on any argument, plan, or reasoning.*

Apply a complete logical assessment in a single pass: (1) Premises — are they stated clearly and are they true? (2) Inference — do the conclusions actually follow from the premises? (3) Fallacies — which informal fallacies (if any) are present? (4) Hidden assumptions — what unstated premises is the reasoning relying on? (5) Verdict — is this reasoning sound, and if not, what specifically is wrong?

**Output:** Five-section assessment with a final verdict: sound / unsound with specific diagnosis.

---

## Logic Council

*Full five-advisor reasoning council — use for complex arguments where the conclusion matters.*

See `logic-council` for the full multi-agent process with 5 independent reasoning framework advisors, peer review, and chair synthesis. Route here when the argument is complex, has non-obvious dependencies, or is reasoning you've invested in and want stress-tested by independent perspectives.

---

## Argument Validation

*Checks whether an argument's premises support its conclusion.*

Identify the argument structure: premises → conclusion. Test each premise: is it true, and does the argument assume it without justification? Test the inference: do the premises actually entail the conclusion, or is there a gap? Identify any logical fallacies present. Distinguish between deductive validity (the structure holds) and soundness (the premises are also true).

**Output:** Argument map (premises, inference, conclusion), validity assessment, soundness assessment, fallacies identified, and the specific repair needed.

---

## Consistency Check

*Surfaces internal contradictions in a document, spec, or plan.*

Read for conflict, not comprehension. For each claim or requirement: does any other part of the document contradict it? Are there requirements that can't all be satisfied simultaneously? Are there edge cases that expose a hidden conflict? Documents that grew incrementally frequently have internal contradictions that no single author introduced but no one caught.

**Output:** Contradictions inventory, classified by severity (surface vs. structural), with specific locations and suggested resolutions.

---

## Causality Mapping

*Maps causal relationships, traces dependencies, and reasons about consequences.*

Build the causal chain: A causes B because [mechanism]. B enables/requires C. If X changes, what else must change? What has to be true for the plan to work — what are the causal prerequisites? Where are the dependencies that, if broken, break everything downstream? Causal maps reveal the leverage points and the fragile assumptions.

**Output:** Causal chain diagram (in text), key dependencies, critical path, and the assumptions the whole structure rests on.

---

## Constraint Mapping

*Maps the full constraint landscape for a decision, design, or plan.*

Inventory all constraints: (1) Classify each as hard (physical/legal), soft (organizational/political), or assumed (may not be real). (2) Find conflicts between constraints — requirements that can't all be satisfied. (3) Find the constraint boundary — the actual solution space that remains. (4) Identify which constraints, if relaxed, would most expand the solution space.

**Output:** Constraint inventory classified by type, conflict map, solution space definition, and highest-value constraints to challenge.

---

## Logic Fixer

*Takes broken reasoning and produces a corrected version.*

Diagnose the specific failure: which premise is false? Where does the inference fail? What fallacy is present? What's the circular dependency? Then repair: restate the argument in a form that is valid, where every premise is defensible and the conclusion actually follows. The goal is not just to identify what's wrong — it's to produce reasoning that works.

**Output:** Diagnosis of the specific logical failure(s). Repaired argument that is valid and sound. If the conclusion cannot be saved, a clear statement of what conclusion *is* supportable.
