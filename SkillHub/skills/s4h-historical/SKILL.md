---
name: s4h-historical
description: "Entry point for the historical reasoning toolkit. Routes to the right historical skill based on your situation. Use when you say 'historical', 'has this happened before', 'what does history say', 'what cycle is this', 'what usually goes wrong', 'what's the lesson', or want historical reasoning applied without knowing which specific tool fits."
---

# Historical

Applies historical reasoning to current situations. Diagnoses what kind of historical analysis is needed and applies the right tool.

## Which tool fits

| You need to... | Tool |
|---|---|
| Identify what recurring cycle this is and where you are in it | cycle-detection |
| Find recurring failure modes from similar past situations | failure-analysis |
| Extract the transferable principle from a specific historical case | lesson-extraction |
| Find genuinely similar historical situations to inform a decision | precedent-analysis |

## Routing Decision

- **Situation feels like it has been seen before, want to know where in the pattern you are** → cycle-detection
- **About to do something and want to know how it typically fails** → failure-analysis
- **Have a specific historical case and want to know what it actually teaches** → lesson-extraction
- **Making a decision and want to know what history says** → precedent-analysis
- **Unclear** → precedent-analysis; finding the analogous situation usually reveals cycles, lessons, and failure modes together

**Framing check:** Confirm the specific historical situation before routing. State what you've identified — the actual situation being examined, what time pressure or decision is attached, and the historical angle being sought — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the situation and what historical lens fits]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

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

## Cycle Detection

*Identifies what recurring cycle this is and where in it you currently are.*

Most situations are instances of known cycles: hype cycles, market cycles, innovation S-curves, boom-bust patterns, political pendulum swings. Name the cycle candidates. Test each: does the current situation match the structural characteristics of that cycle? If so: what phase are you in (early, peak, correction, trough, recovery)? What does the cycle predict comes next?

**Output:** Cycle identification with evidence, current phase assessment, and what the cycle predicts comes next.

---

## Failure Analysis

*Extracts recurring failure modes from similar past situations.*

Most failures have happened before in recognizable patterns. Identify 3-5 historical situations that are structurally similar to the current one. For each: what went wrong? Was the failure caused by overconfidence, resource depletion, misreading the environment, internal conflict, timing, or something else? Look for the failure mode that appears across multiple cases — that's the one most worth preparing for.

**Output:** Historical failure case inventory, recurring failure modes ranked by frequency and severity, and the specific early warning signs to watch for.

---

## Lesson Extraction

*Extracts the transferable principle from a specific historical case.*

Historical cases carry both contingent details (specific to their time and place) and transferable principles (valid across contexts). The challenge is separating them. Take the case and ask: what actually caused the outcome — the surface events or the underlying dynamics? If you removed all the period-specific details, what structural principle remains? Test that principle against at least one other historical case.

**Output:** The contingent surface details set aside. The underlying structural principle. Cross-case validation. How the principle applies to the current situation.

---

## Precedent Analysis

*Finds and applies genuinely similar historical situations.*

Distinguish true precedents from superficial analogies. A true precedent shares the underlying causal structure, not just surface similarity. Find 2-3 candidate precedents. For each: what makes it genuinely similar? What makes it different in ways that matter? What did decision-makers do, and what happened? What would they have done differently in hindsight?

**Output:** Precedent inventory with genuine vs. superficial similarity assessment, decision-outcome analysis for each, and the lessons that most directly apply.
