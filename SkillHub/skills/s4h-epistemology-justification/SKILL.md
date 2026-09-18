---
name: s4h-epistemology-justification
description: "Analyzes what would actually justify believing a claim. Maps the justification structure (foundationalist, coherentist, reliabilist) and identifies the weakest link in the chain. Use when you say 'what would it actually take to know this', 'is this belief actually justified', 'what's the foundation for this assumption', 'we keep citing the same evidence for everything', 'I believe this but I can't say why', 'what would change my mind', or when a claim feels supported but you want to make the support structure explicit and test it."
---

# Epistemology: Justification

A belief can feel well-supported without actually being justified. The feeling of certainty is not evidence of justification — it's evidence of confidence, which is a psychological state, not an epistemic one. Justification analysis makes the load-bearing structure of a belief explicit so it can be examined and tested.

Three main structures for how beliefs get justified:
- **Foundationalism**: beliefs are justified by tracing back to basic beliefs that are self-evident, incorrigible, or empirically certain. The chain has a floor.
- **Coherentism**: beliefs are justified by fitting into a mutually supporting web of other beliefs. No single foundation — the whole web holds itself up.
- **Reliabilism**: beliefs are justified if they were produced by a reliable cognitive process (careful observation, valid inference, calibrated expert judgment) — regardless of whether the believer can articulate why.

Most real belief systems are hybrid. The point of analysis is not to pick the right theory of justification — it's to find where the specific belief's justification structure is weakest.

---

## Your Process

**Step 1: Identify the Belief**
State the belief precisely. What exactly is being claimed to be known or justifiably believed? Strip away hedges and weasel words to get the core claim.

**Framing check:** Confirm the specific belief before continuing. State what you've identified — the actual claim being analyzed and the domain or context it comes from — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the specific belief and its context]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different belief than read; incorporate the correction before proceeding

**Step 2: Trace the Justification Chain**
Ask: "What makes you think that?" Recursively trace the answer until you hit one of three stopping points:
- A basic belief that seems self-evident or foundational (foundationalism)
- A cluster of mutually supporting beliefs with no clear floor (coherentism)
- "This is the output of a process I trust" — e.g., experiment, calibrated expert judgment (reliabilism)

Write out the chain explicitly. Many chains are assumed rather than traced — making them explicit is half the work.

**Step 3: Classify the Justification Structure**

| Structure | Signature | Key question to test it |
|-----------|-----------|------------------------|
| **Foundationalist** | Chain traces back to a basic belief | Is that basic belief actually self-evident, or just assumed? |
| **Coherentist** | Beliefs support each other mutually | Is the web genuinely independent, or are all the beliefs downstream of one hidden assumption? |
| **Reliabilist** | Justified by process quality | Is the process actually reliable in this domain? Are there known failure modes? |

Most real cases are hybrid — identify which structure dominates at each link.

**Step 4: Test Each Link**

For each step in the justification chain, ask:
- Is this link actually supported, or is it assumed?
- Could a reasonable skeptic deny this link while granting everything else?
- If this link fails, does the whole chain fail?

Classify each link: **sound** / **shaky** / **unsupported** / **circular**.

Special flag: **circular justification** — where A justifies B and B justifies A, without either being independently grounded. Common in self-reinforcing organizational beliefs ("our strategy is working because our metrics are up; our metrics are up because our strategy is working").

**Step 5: Identify the Weakest Link**

**Before narrowing:** Show the complete link assessment to the user first. Use `AskUserQuestion`:
- **Question:** "I've assessed [N] links in the justification chain. Before I identify the most critical weakest link, are there any you'd flag as especially important, or any I've missed?"
- **Header:** "Prioritise"
- **Options:**
  - **Proceed with your selection** — the link assessment looks right
  - **Flag one** — user will name a specific link to treat as critical
  - **Add a missing one** — user will describe a link not yet in the chain

Which link, if removed, would most damage justification for the belief? This is the critical point — the place where effort to strengthen or challenge the belief will have the most leverage.

**Step 6: Assess Overall Justification**
Given the chain and its weakest link:
- Is the belief *justified* — i.e., does the chain hold well enough that believing it is reasonable?
- Is the belief *unjustified* — the chain has a critical break?
- Is the belief *underdetermined* — there's a chain, but alternative beliefs could be equally well justified on the same evidence?

**Step 7: What Would Change the Justification?**
What evidence, argument, or process change would most improve justification? What would undermine it? The mark of a well-justified belief is that you can say precisely what would change it.

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Trace the full chain, classify each link, identify weakest point
  - **Weakest link only** — Skip full classification, go directly to where the justification is most vulnerable
  - **What would change this belief** — Focus on the update conditions, not the chain structure
  - **Refine the belief** — Sharpen what we're analyzing before starting

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

---

## Output Format

### The Belief
[Precise statement of what's being analyzed]

### Justification Chain
1. [Belief] is justified by → [Justification 1]
2. [Justification 1] is justified by → [Justification 2]
3. [Continue until the chain terminates]

**Chain terminates at:** [Basic belief / Mutual coherence web / Process trust]

### Structure Classification
**Primary structure:** Foundationalist / Coherentist / Reliabilist / Hybrid
**Notes:** [One sentence on why]

### Link Assessment
| Link | Type | Assessment | Notes |
|------|------|------------|-------|
| [Link 1] | Foundation / Inference / Process | Sound / Shaky / Unsupported / Circular | [Why] |
| [Link 2] | ... | ... | ... |

### Weakest Link
**The critical point:** [Specific link]
**Why it's critical:** [What depends on it; what breaks if it fails]

### Overall Justification
**Assessment:** Justified / Unjustified / Underdetermined
**Reasoning:** [One paragraph]

### What Would Change This
**Would strengthen:** [Specific evidence, argument, or process]
**Would undermine:** [Specific evidence, argument, or process]

---

## Notes

Use `epistemology-knowledge-types` first if you're not sure what *kind* of claim you're dealing with — the justification structure depends on the knowledge type. Use `epistemology-epistemic-status` when you need to assess confidence across many claims in a domain, not just one belief. Use `logic-check` when the issue is inference validity (does the conclusion follow?) rather than justification (is the belief grounded?).

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Justifications assessed. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-logic-argument-validation` — Validate the logical structure of the justifications
  - `/s4h-investigation-source-trace` — Trace justifications back to their original sources
  - `/s4h-epistemology-limits` — Find where justification runs out and uncertainty begins
  - **Done** — Wrap up and synthesise what we have so far
