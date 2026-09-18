---
name: s4h-temporal-horizon-mapping
description: "Maps consequences of a decision across short, medium, and long time horizons. Use when asked about 'time horizons', 'what does this look like in 5 years', 'short-term vs long-term', 'map the implications over time', or 'think through the long-term'."
---

# Temporal Horizon Mapping

Decisions that look good now often look very different at 1, 3, or 10 years. The most consequential errors in judgment come not from bad reasoning in the moment but from evaluating a decision at the wrong time horizon — optimizing for the immediate while the real costs land later. Making all three horizons explicit forces the tradeoff into view rather than leaving it implicit.

---

## Your Process

**Step 1: State the Decision**
Name the decision being evaluated and the current context in which it is being made. Clarity here prevents analysis drifting to adjacent decisions.

**Framing check:** Confirm the specific decision before continuing. State what you've identified — the actual decision being evaluated and the context in which it is being made — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the specific decision and its context]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Map Immediate Consequences (0–3 months)**
What is the likely state immediately after acting? What resources are committed or freed? Who is affected and how? What has this enabled or closed off in the near term?

**Step 3: Map Medium-Term Consequences (6–24 months)**
What does the situation look like after the initial effects have compounded? What second-order effects emerge? Who gains or loses standing? What dependencies or path-dependencies have formed?

**Step 4: Map Long-Term Consequences (3+ years)**
What has the decision made likely or unlikely at scale and over time? What is the structural change — to capabilities, relationships, markets, culture? What would be very difficult to reverse by this point?

**Step 5: Flag Reversals**
Identify decisions that look positive short-term but create long-term problems — and the reverse. These reversals are the highest-value output of this analysis.

**Step 6: Identify the Governing Horizon**
**Before narrowing:** Show the consequences mapped across all three horizons to the user first. Use `AskUserQuestion`:
- **Question:** "I've mapped consequences across all three horizons. Before I identify the governing horizon, are there any consequences you'd flag as especially significant, or any I've missed?"
- **Header:** "Prioritise"
- **Options:**
  - **Proceed with your selection** — the mapped consequences look right
  - **Flag one** — user will name a specific consequence to weight more heavily
  - **Add a missing one** — user will describe a consequence not yet captured

At which horizon do the most significant consequences actually land? Is that the horizon currently being used to evaluate this decision? Mismatched horizons are the primary source of poor long-term decisions made in good faith.

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Long-term consequences only** — What emerges beyond the obvious timeframe, skip near-term
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

**Horizon Table**

| Horizon | Timeframe | Likely State | Enabled / Foreclosed | Who Is Better / Worse Off |
|---------|----------|-------------|---------------------|--------------------------|
| Immediate | 0–3 months | | | |
| Medium | 6–24 months | | | |
| Long | 3+ years | | | |

**Reversal Flags:** [decisions that look good short-term but create long-term problems, or vice versa]

**Governing Horizon:** [which horizon should drive this decision + why it differs from current evaluation horizon if applicable]

---

## Notes

Short-term and long-term are not automatically in conflict — some decisions improve all horizons. Identify those as high-confidence choices; the real analysis is needed where horizons diverge.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Horizons mapped. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-temporal-futures-mapping` — Map futures at each horizon
  - `/s4h-temporal-timing-analysis` — Time actions across the horizons
  - `/s4h-strategy-timing` — Align strategy with the horizon structure
  - **Done** — Wrap up and synthesise what we have so far
