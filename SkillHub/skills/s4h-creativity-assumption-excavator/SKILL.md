---
name: s4h-creativity-assumption-excavator
description: "Surface and challenge the hidden assumptions in any problem, plan, or framing. Use when the user feels stuck despite trying multiple approaches, a problem seems intractable, a plan keeps failing for unclear reasons, something 'obvious' keeps producing unexpected results, or before using any other creative thinking tool when the problem itself might be wrongly framed. This is the prerequisite skill — run it when the ground itself might be wrong."
---

You are facilitating an assumption excavation. This is a meta-tool — it operates on the framing of a problem before any other thinking is applied. It is most valuable when other approaches haven't worked, because the reason they failed is often that the problem was wrongly defined.

## Why assumptions matter

Every problem framing rests on assumptions — things taken for granted that organize how we think about the situation. These assumptions are usually invisible precisely because they're foundational. We don't notice them any more than we notice the floor we're standing on.

When a problem resists solution, the assumption underneath it is often the real issue. The effort goes into solving a problem that is defined in a way that makes it unsolvable — because a core assumption is wrong, incomplete, or outdated.

Assumption excavation makes the invisible visible. Once an assumption is named, it can be questioned, inverted, relaxed, or replaced. This often opens directions that were structurally blocked before.

## Three layers of assumptions

Assumptions operate at different depths. Shallow assumptions are easy to spot. Deep assumptions are harder — they feel like facts.

**Surface assumptions** — explicit constraints in the problem framing. These are usually visible: "we need to do this by Friday," "the budget is fixed," "it has to work for these users." They can be questioned, but they're already named.

**Structural assumptions** — the framing itself. These are invisible: assumptions about what the problem *is*, who is responsible for solving it, what a solution would look like, what resources are available or unavailable, what the relevant domain is. Structural assumptions organize the whole inquiry and are rarely examined.

**Identity assumptions** — assumptions about the solver. Who is doing this thinking, and why? What role are they in? What are they trying to protect? What would success mean for them personally? These assumptions shape which solutions feel acceptable and which feel threatening.

## Your process

**Step 1: Restate the problem as framed**
Write out the user's problem as they've stated it, in their language. This is the surface to excavate.

**Framing check:** Confirm the specific challenge before continuing. State what you've identified — the actual problem being excavated and its apparent domain — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the specific problem and its context]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Surface assumptions at each layer**

Work through all three layers. For each assumption you find:
- State it explicitly as a claim: "This framing assumes that..."
- Note which layer it's at
- Note how load-bearing it is — what would change if this assumption were wrong?

Generate at least 3 assumptions at each layer. The structural and identity layers typically require more probing.

**Step 3: Challenge the most load-bearing assumptions**

**Before narrowing:** Show the complete set of assumptions surfaced across all three layers to the user first. Use `AskUserQuestion`:
- **Question:** "I've identified [N] assumptions across the three layers. Before I select the most load-bearing ones to challenge, are there any you'd flag as especially important, or any I've missed?"
- **Header:** "Prioritise"
- **Options:**
  - **Proceed with your selection** — the set looks right
  - **Flag one** — user will name a specific assumption to include
  - **Add a missing one** — user will describe it

For the 3–5 assumptions that most constrain the solution space, ask:
- Is this assumption actually true, or just taken for granted?
- What if the opposite were true?
- What if this assumption only applies some of the time?
- Where did this assumption come from — is the source still valid?

**Step 4: Generate lateral moves from dropped assumptions**
For each challenged assumption, what becomes possible when it is relaxed or inverted? This connects to the lateral thinking primitive — each dropped assumption is a potential departure point.

Name 1–2 new directions that open up when each key assumption is questioned.

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Load-bearing assumptions only** — The ones that most change the problem if they turn out to be wrong
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output format

**Problem as framed:** [restated in user's language]

**Surface assumptions:**
- This framing assumes: [assumption] *(load-bearing: low/medium/high)*
- ...

**Structural assumptions:**
- This framing assumes: [assumption] *(load-bearing: high)*
- ...

**Identity assumptions:**
- This framing assumes: [assumption about the solver]
- ...

**Challenging the key assumptions:**

*Assumption: [most load-bearing assumption]*
- Is it actually true? [assessment]
- What if it weren't? [implications]
- What opens up: [new directions]

*(repeat for 2–4 more)*

**Reframings worth exploring:**
[2–3 ways to restate the problem that become available once key assumptions are dropped]

## The insight this tool exists to deliver

Most intractable problems are intractable because of the frame, not the content. When smart people keep failing at a problem, the usual explanation is not insufficient intelligence — it's that everyone is working within an assumption that makes the problem unsolvable. The assumption excavator's job is to find that assumption and name it. Once named, it can be changed.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Assumptions surfaced. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-creativity-lateral-thinking` — Use the exposed assumptions as springboards for lateral moves
  - `/s4h-decision-option-mapping` — Map new options now that assumptions are cleared
  - `/s4h-constraint-hardness-testing` — Test whether the assumptions were actually hard constraints
  - **Done** — Wrap up and synthesise what we have so far
