---
name: s4h-investigation-source-trace
description: "Traces a claim back to its origin: who first made it, what evidence it rested on, and how it has been distorted in transmission. Use when you've heard something and want to know where it actually came from — 'where does this claim come from', 'who first said this', 'I've heard that X is true', 'trace the source', 'is this just a rumor', 'how did this become conventional wisdom'."
---

# Investigation: Source Trace

Most claims arrive pre-laundered. By the time you encounter them, they have passed through blog posts, conference talks, secondhand summaries, and the compression of repetition. The original source has been forgotten, the caveats dropped, and the scope quietly expanded. Source tracing is the discipline of reversing that process: going back upstream to find what was actually said, by whom, with what evidence, in what context — and assessing how faithfully the current claim represents that original.

---

## Your Process

**Step 1: Capture the Claim as Received**
Write out the claim exactly as you have encountered it. Note: who is asserting it now, in what context, and what confidence level they are expressing ("studies show" vs. "I've heard" vs. "it's well established that").

**Framing check:** Confirm the specific claim before continuing. State what you've identified — the actual claim being traced and the current form it takes — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the claim and its current form]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different claim than read; incorporate the correction before proceeding

**Step 2: Identify Potential Origin Points**
Work backward. What is the earliest source you can find for this claim? Strategies:
- Search for the earliest publication or statement you can locate
- Look for the claim's attributed origin (is someone cited? Is that citation accurate?)
- Check whether the claim appears in academic literature, a specific study, a book, a news report, or originated as someone's opinion
- Note any "citation laundering" — claims that cite a secondary source which itself doesn't cite a primary source

**Step 3: Evaluate the Origin Source**
Once you have the earliest traceable source, assess it:
- **Who** made the claim? What are their credentials, institutional affiliation, and potential biases?
- **When** was it made? What was the context at the time?
- **What was the original evidence?** Was it a study (what kind?), a data analysis, an observation, an opinion, a hypothesis?
- **What caveats did the original source include** that have since been dropped?
- **What did the original claim actually assert** — is it narrower, broader, or different from the current form?

**Step 4: Map the Transmission Chain**
Trace how the claim moved from origin to present form. For each major step in transmission:
- What changed? (scope, confidence level, caveats, specificity)
- Was the change a reasonable simplification, or a distortion?
- At what point did the claim acquire the form you encountered?

Classify each change:
- **Faithful summarization** — the meaning is preserved with reasonable compression
- **Scope expansion** — a specific finding generalized beyond its evidence
- **Caveat stripping** — conditions or limitations removed
- **Inversion** — the meaning actually reversed
- **Fabrication** — something added that wasn't in the original

**Step 5: Assess Credibility of the Origin**
Apply a credibility test to the original source:
- Is the evidence type appropriate to the claim being made? (A single case study shouldn't support a universal claim)
- Is there independent replication or corroboration?
- Are there known rebuttals or contradictory findings?
- Does the source have a conflict of interest (commercial, ideological, reputational)?

**Step 6: Issue a Verdict**
Compare the claim as received with the claim at its origin. Answer:
1. Does the current claim accurately represent what the original source established?
2. How strong is the original evidence?
3. What is the most defensible version of this claim given the actual evidence?

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full trace** — Complete all steps: origin identification, transmission map, credibility assessment, verdict
  - **Just find the origin** — Identify the earliest traceable source and assess its credibility; skip transmission mapping
  - **Transmission distortion only** — Focus on how the claim changed; assume I've identified the source
  - **Refine the claim** — Clarify what exactly we're tracing before starting

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

---

## Output Format

### Claim as Received
[The claim, as encountered, with the current asserter's confidence level]

### Earliest Traceable Source
**Source:** [Author, publication, date, type]
**Original claim:** [What was actually said — verbatim if possible]
**Original evidence:** [What the source based it on]
**Original caveats:** [Conditions or limitations stated in the original]

### Transmission Map
| Step | Source | Change Made | Change Type |
|------|--------|-------------|-------------|
| Origin | [Source] | [Original form] | — |
| Step 2 | [Source] | [What changed] | Faithful / Scope expansion / Caveat stripping / Inversion / Fabrication |
| ... | | | |
| Current form | [Current asserter] | [Final form] | |

### Source Credibility Assessment
- **Evidence type:** [RCT / observational / case study / expert opinion / anecdote / assertion]
- **Replication:** [Independently replicated / single study / no replication known]
- **Conflicts of interest:** [None apparent / Potential / Clear]
- **Known contradictions:** [Yes — describe / None found]

### Verdict
**Faithfulness:** The current claim [faithfully represents / partially represents / significantly distorts / inverts] the original.

**Original evidence strength:** [Strong / Moderate / Weak / No real evidence at origin]

**Most defensible version of this claim:** [The narrower, more accurate formulation that the actual evidence supports]

---

## Notes

Use investigation-triangulation when you want to verify a claim across multiple sources (rather than trace a single claim's origin). Use investigation-evidence-audit when the source is known and the question is whether the evidence itself is good enough. Source trace is specifically about the genealogy of a claim — where it came from and how it changed.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Sources traced. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-investigation-evidence-audit` — Audit the quality of sources now that they're identified
  - `/s4h-epistemology-justification` — Assess the justification quality of each traced source
  - `/s4h-logic-argument-validation` — Validate arguments built on these sources
  - **Done** — Wrap up and synthesise what we have so far
