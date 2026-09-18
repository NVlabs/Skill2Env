---
name: s4h-investigation-claim-decomposition
description: "Breaks a complex claim into its smallest independently verifiable parts, classifies each sub-claim, and identifies which parts carry the most logical load. Use when a claim feels too big to verify as a unit — 'what exactly is this claiming', 'break this down', 'what are the hidden assumptions in this statement', 'this seems like multiple claims at once', 'what would I need to verify to believe this'."
---

# Investigation: Claim Decomposition

Complex claims are bundles. "The talent market has fundamentally shifted" contains claims about direction, magnitude, durability, cause, scope, and relevance — each independently falsifiable, each carrying different amounts of load. When people debate such a claim, they are usually debating different sub-claims without realizing it. Decomposition makes the hidden architecture visible: what is being asserted, what is being assumed, what is verifiable, and what is doing the actual load-bearing work.

---

## Your Process

**Step 1: State the Master Claim**
Write out the claim in its current form. If it was stated imprecisely, note that — but trace it faithfully. Do not pre-interpret; decompose what was actually asserted.

**Framing check:** Confirm the specific claim before continuing. State what you've identified — the actual claim being decomposed and its apparent domain (factual, causal, normative, etc.) — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the claim and its domain]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different claim than read; incorporate the correction before proceeding

**Step 2: Decompose into Atomic Sub-Claims**
Break the master claim into the smallest independently assessable statements. Each sub-claim should be:
- A single, specific assertion
- Independently falsifiable (you could in principle evaluate it separately from the others)
- Not a combination of two ideas that are themselves separable

Common decomposition dimensions:
- **Factual claims** — assertions about what is true right now
- **Causal claims** — assertions about what causes what
- **Trend claims** — assertions about direction, rate, or duration of change
- **Comparative claims** — assertions about relative magnitude (more than, better than)
- **Definitional claims** — assertions about what a term means or what counts as X
- **Normative claims** — assertions about what should be done or what is good
- **Scope claims** — how broadly the main claim applies (always, usually, in some contexts)

Aim for completeness: a claim with 3 surface sub-claims usually has 6-10 once decomposed carefully.

**Step 3: Classify Each Sub-Claim**
For each sub-claim, assign a classification:

| Classification | Meaning |
|---|---|
| **Verified** | Well-established, supported by strong independent evidence |
| **Checkable** | Testable in principle; evidence exists or could be gathered |
| **Contested** | Active disagreement in the relevant domain; competing evidence |
| **Uncheckable** | Unfalsifiable by design (definitional, philosophical, or unprovable) |
| **Assumed** | Treated as true without being argued; load-bearing but unexamined |

**Step 4: Identify the Load-Bearing Sub-Claims**
**Before narrowing:** Show the complete list of classified sub-claims to the user first. Use `AskUserQuestion`:
- **Question:** "I've identified [N] sub-claims. Before I select the most load-bearing ones, are there any you'd flag as especially critical, or any I've missed?"
- **Header:** "Prioritise"
- **Options:**
  - **Proceed with your selection** — the set looks right
  - **Flag one** — user will name a specific sub-claim to include as load-bearing
  - **Add a missing one** — user will describe a sub-claim not yet listed

Not all sub-claims carry equal weight. Determine:
- Which sub-claims, if false, would cause the master claim to fail?
- Which sub-claims are doing heavy lifting that isn't acknowledged?
- Which assumed sub-claims are most at risk of being wrong?

These are the critical nodes: the sub-claims where investigation effort should concentrate.

**Step 5: Map the Dependency Structure**
Do some sub-claims depend on others being true first? Build a simple dependency map: "Sub-claim C requires sub-claim A and B to hold." This reveals whether the whole claim stands or falls on a single contested premise.

**Step 6: Recommend Verification Priorities**
Given the load map and classifications, what should be verified first? Rank by:
- How much load it carries (does the master claim fail if this is false?)
- How checkable it is (is verification feasible?)
- How likely it is to be wrong (is this an assumption that has been examined?)

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full decomposition** — Complete all steps: decompose, classify, map dependencies, recommend priorities
  - **Decompose and classify only** — List all sub-claims with classifications; skip dependency mapping
  - **Load-bearing claims only** — Focus on identifying which sub-claims are doing the most work
  - **Refine the claim first** — Clarify what exactly we're decomposing before starting

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

---

## Output Format

### Master Claim
[The claim as stated]

### Sub-Claim Decomposition

| # | Sub-Claim | Type | Classification | Notes |
|---|-----------|------|---------------|-------|
| 1 | [sub-claim] | Factual / Causal / Trend / Comparative / Definitional / Normative / Scope | Verified / Checkable / Contested / Uncheckable / Assumed | [Brief note] |
| 2 | ... | | | |

### Load-Bearing Sub-Claims
**Highest load:**
- [Sub-claim #] — [Why it's load-bearing: what fails if it's false]

**Critical assumptions:**
- [Sub-claim #] — [What is being taken as given; what would have to be true]

### Dependency Structure
- [Sub-claim C] depends on [Sub-claim A] and [Sub-claim B]
- [The whole claim collapses if [sub-claim X] is false]

### Verification Priorities
1. **[Sub-claim #]** — High load, checkable, hasn't been examined: [how to verify]
2. **[Sub-claim #]** — Assumed; likely the weakest point: [what would falsify it]
3. **[Sub-claim #]** — Contested in domain; worth checking current state: [what the debate is]

---

## Notes

Use investigation-evidence-audit once you've identified the load-bearing sub-claims and want to evaluate the evidence for those specific parts. Use investigation-source-trace when you want to know who first made the master claim and how it has changed. Claim decomposition is specifically about the internal architecture of a claim — not whether its evidence is good, but what it is actually asserting.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Claims decomposed. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-investigation-source-trace` — Trace each component claim to its source
  - `/s4h-investigation-evidence-audit` — Audit evidence for each component claim
  - `/s4h-logic-check` — Validate the inference structure between claims
  - **Done** — Wrap up and synthesise what we have so far
