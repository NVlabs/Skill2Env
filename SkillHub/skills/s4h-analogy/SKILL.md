---
name: s4h-analogy
description: "Entry point for the analogy toolkit. Routes to the right analogy skill based on your situation. Use when you say 'analogy', 'is this like that', 'find a comparison', 'import a solution from elsewhere', 'fresh eyes on this', 'where does this metaphor break', or want analogical reasoning applied without knowing which specific tool fits."
---

# Analogy

Applies analogical reasoning to any problem. Diagnoses what kind of analogy work is needed and applies the right tool.

## Which tool fits

| You need to... | Tool |
|---|---|
| Find where an existing analogy or metaphor breaks down | boundary-testing |
| Import solutions from a completely different domain | domain-transfer |
| Approach a problem through a different field's lens | perspective-shifting |
| Test the structural correspondence between two situations | structure-mapping |

## Routing Decision

- **Already using an analogy and want to stress-test it** → boundary-testing
- **Stuck on a problem, want to find who's solved something like it elsewhere** → domain-transfer
- **Need fresh eyes from an expert in a different field** → perspective-shifting
- **Want to know if two situations are genuinely structurally similar** → structure-mapping
- **Unclear** → structure-mapping first (establishing the analogy rigorously), then boundary-testing (finding where it fails)

**Framing check:** Confirm the specific analogy situation before routing. State what you've identified — the analogy or problem being examined and the goal (stress-test, import solutions, shift perspective, or validate structure) — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the analogy situation and goal]. Is that right?"
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

## Boundary Testing

*Finds where an analogy breaks down before it's relied upon.*

Name the analogy explicitly: A is like B because [shared properties]. Now systematically test each dimension of the comparison. For each shared property: does it actually hold? What differences exist? Find the dimension where the analogy fails in a way that matters for the decision at hand. Analogies fail silently — the damage happens when decisions are made on a mapping that doesn't hold in the relevant dimension.

**Output:** Analogy map (what holds, what doesn't), the specific dimension of failure, and what decisions should not rely on this analogy.

---

## Domain Transfer

*Imports solutions from unrelated domains by finding structural similarities.*

Name the core structure of the problem: what kind of challenge is this underneath the surface details? Search for domains that have solved structurally similar problems — often in completely unrelated fields (biology for network design, military strategy for resource constraints, jazz for improvisational systems). For each candidate domain: what was the solution? How does it map back?

**Output:** Core problem structure, candidate domains with solved analogues, and specific solutions mapped back to the original problem.

---

## Perspective Shifting

*Approaches a problem through a completely different field's lens.*

Name the home domain — the expertise lens being applied by default. Now select 2-3 radically different fields: what would a [biologist / game designer / urban planner / etc.] see when looking at this? Apply each lens genuinely, not superficially. The goal is to surface assumptions invisible from inside the home domain.

**Output:** Per-lens analysis — what each field notices, what assumptions it challenges, what solutions it suggests that the home domain wouldn't.

---

## Structure Mapping

*Identifies the deep structural correspondence between two situations.*

List the elements of situation A. List the elements of situation B. For each element in A: does a corresponding element exist in B? Are the relationships between elements preserved? Test whether the mapping is genuine isomorphism or just surface similarity. Surface similarity fails on deeper structure; genuine isomorphism predicts behavior accurately.

**Output:** Element-by-element correspondence table, relationship preservation check, verdict on whether the analogy is structurally valid, and what the mapping predicts.
