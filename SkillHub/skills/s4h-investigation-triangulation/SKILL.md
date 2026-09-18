---
name: s4h-investigation-triangulation
description: "Verifies a claim across genuinely independent sources, distinguishing amplification from true corroboration. Use when you want to know if multiple sources actually confirm something — 'can I verify this from multiple angles', 'do independent sources agree', 'is this confirmed by more than one source', 'are these sources actually independent', 'how well-corroborated is this claim'."
---

# Investigation: Triangulation

More sources does not mean better verification. If ten publications all cite the same original study, you have one data point with ten references — not ten data points. True triangulation requires genuinely independent sources: different methods, different investigators, different populations, different time periods. Convergence among truly independent sources is strong evidence. Convergence among sources that all trace back to the same origin is amplification, not corroboration. This skill teaches the difference and makes it operational.

---

## Your Process

**Step 1: State the Claim**
Write out the claim you want to triangulate, precisely. Vague claims are hard to triangulate because different sources may be speaking to different aspects.

**Framing check:** Confirm the specific claim before continuing. State what you've identified — the actual claim being triangulated and its scope — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the claim and its scope]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different claim than read; incorporate the correction before proceeding

**Step 2: Collect Candidate Sources**
List all sources that appear to speak to the claim:
- Studies, papers, reports
- Expert statements
- Data sets or statistics
- News reports or analyses
- Firsthand accounts or observations

Do not filter for independence yet — that's the next step.

**Step 3: Classify Independence**
For each source, trace its origin and classify its independence from other sources on your list:

| Independence Level | Definition |
|---|---|
| **Fully independent** | Different investigators, methods, population, and time period; no data sharing or cross-referencing |
| **Methodologically independent** | Different methods and investigators but applied to the same data set or population |
| **Structurally dependent** | Cites a common primary source; draws from shared underlying data |
| **Direct derivative** | Is a summary, report, or commentary on another source on the list |
| **Unknown** | Origin cannot be traced; independence cannot be assessed |

The critical question for each source: does it trace back to any other source on the list? If so, classify it as structurally dependent or derivative, not independent.

**Step 4: Identify the Independent Evidence Base**
**Before narrowing:** Show the complete classification table to the user first. Use `AskUserQuestion`:
- **Question:** "I've classified [N] sources. Before I identify the genuinely independent ones, are there any you'd flag as especially important, or any I've missed?"
- **Header:** "Prioritise"
- **Options:**
  - **Proceed with your selection** — the set looks right
  - **Flag one** — user will name a specific source to include
  - **Add a missing one** — user will describe it

After classification, identify the sources that are genuinely independent. How many truly independent sources support this claim? One? Three? Zero?

A common finding: a claim appears to have "many sources" but has only 1-2 independent studies, with the rest being summaries, citations, commentaries, or amplifications of those originals.

**Step 5: Assess Convergence and Divergence**
Among the genuinely independent sources:
- Do they converge on the same conclusion?
- Do any diverge, contradict, or express uncertainty the others don't?
- When sources diverge, is it about the main claim or about scope, magnitude, or conditions?

Convergence pattern classifications:
- **Strong convergence** — Multiple fully independent sources agree on core claim
- **Partial convergence** — Independent sources agree on direction but diverge on magnitude, scope, or conditions
- **Divergence** — Independent sources reach different conclusions
- **Insufficient independent evidence** — Too few independent sources to triangulate

**Step 6: Assess Method Independence**
Even among independent sources, do they use different enough methods to constitute genuine triangulation? A claim supported by three independent surveys is less robustly triangulated than a claim supported by a survey, an observational study, and a field experiment — because the methods have different failure modes. Methodological diversity strengthens triangulation.

**Step 7: Issue a Triangulation Verdict**
Based on the genuine independent evidence base and its convergence pattern, issue a verdict:
- How reliably is this claim established by triangulation?
- What would adequate triangulation look like if it doesn't currently exist?
- Is the apparent corroboration real, or is it amplification of a single origin?

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full triangulation** — All steps: collect sources, classify independence, assess convergence, evaluate method diversity, verdict
  - **Independence classification only** — Classify each source's independence; stop before convergence assessment
  - **Convergence verdict only** — Assume I've classified the sources; just assess whether they genuinely converge
  - **Refine the claim** — Clarify what exactly we're triangulating before starting

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

---

## Output Format

### Claim Being Triangulated
[The claim, stated precisely]

### Source Classification

| # | Source | Description | Independence Level | Notes |
|---|--------|-------------|-------------------|-------|
| 1 | [Source name/type] | [What it says about the claim] | Fully independent / Methodologically independent / Structurally dependent / Direct derivative / Unknown | [Traces back to source #? Uses same data?] |
| 2 | ... | | | |

### Independent Evidence Base
**Number of genuinely independent sources:** [N]
**Sources:** [List of the fully and methodologically independent sources]
**Non-independent sources:** [Count of structurally dependent and derivative sources — "X sources appear independent but trace back to [Source #]"]

### Convergence Assessment
**Among independent sources:**
- Core claim: [Converge / Diverge — describe]
- Magnitude/scope: [Converge / Diverge — describe if divergence matters]
- Conditions: [Do sources agree on when or where the claim holds?]

**Convergence pattern:** Strong convergence / Partial convergence / Divergence / Insufficient independent evidence

### Method Diversity
[Do the independent sources use meaningfully different methods? Does methodological diversity strengthen or weaken the triangulation?]

### Triangulation Verdict
**Reliability:** [Strong / Moderate / Weak / Insufficient] triangulation

**Reasoning:** [Why: how many genuine independent sources, what their convergence looks like]

**What adequate triangulation would look like:** [What sources or methods are missing that would genuinely strengthen confidence]

---

## Notes

Triangulation is about independence, not volume. Use investigation-evidence-audit to evaluate the quality of the independent sources once you've identified them. Use investigation-source-trace to establish whether sources you thought were independent actually trace back to a common origin. Triangulation answers the question "do multiple genuinely independent lines of evidence point to the same conclusion?" — not "how many times has this been said?"

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Sources triangulated. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-probability-confidence-calibration` — Calibrate confidence from the triangulated sources
  - `/s4h-investigation-counter-hypothesis` — Test triangulation findings against alternative hypotheses
  - `/s4h-logic-check` — Check that triangulated conclusions are logically valid
  - **Done** — Wrap up and synthesise what we have so far
