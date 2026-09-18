---
name: s4h-economics-incentive-mapping
description: "Maps who benefits, who pays, and what behaviours the incentive structure actually produces. Triggers: 'what's the incentive here', 'why do people keep doing this', 'incentives are misaligned', 'who benefits from this', 'why isn't this working despite the policy', 'what does the structure reward', 'people say one thing but do another', any situation where behaviour diverges from stated intent."
---

# Economics: Incentive Mapping

Charlie Munger's dictum: "Show me the incentive and I'll show you the outcome." The most reliable predictor of behaviour is not what people intend, say they'll do, or are instructed to do — it is what the structure rewards them for doing. People are not irrational or immoral when they respond to incentives; they are responding rationally to the environment they're in. If behaviour is wrong, the problem is usually the incentive structure, not the people.

Incentive mapping is systematic: identify every party whose behaviour matters, determine what each party gains and loses under the current arrangement, predict the behaviours those incentives produce, and compare predicted behaviour to desired behaviour. The gap between predicted and desired is the misalignment — and misalignment is almost always the source of dysfunction in organisations, policies, and markets.

This framework draws on classical price theory but its most influential modern application is in principal-agent analysis: what happens when the person making decisions (the agent) has different incentives from the person bearing the consequences (the principal)? Kahneman's work on loss aversion adds a further layer — people respond more strongly to potential losses than to equivalent gains, so incentive systems that rely on upside alone are systematically weaker than those that also activate loss aversion.

---

## Your Process

**Step 1: Map the parties**
Identify every party in the system whose behaviour matters to the outcome. This includes: decision-makers, implementers, beneficiaries, those who bear costs, and third parties who are affected but have no formal role. Do not limit the list to the obvious actors — the most important incentives often belong to parties one step removed from the main action.

**Framing check:** Confirm the system and the parties before continuing. State what you've identified in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [one-sentence framing — the system being examined and the parties whose behaviour matters]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Map each party's incentives**
For each party, answer: what do they gain by taking the desired action? What do they lose? What do they gain by *not* taking the desired action, or by taking an alternative action? Capture both formal incentives (salary, bonus, promotion, penalty, fine, contract terms) and informal incentives (reputation, status, relationships, fear of blame, habit).

**Step 3: Predict behaviours**
Based on the incentives mapped in Step 2, predict what each party will actually do — independent of what they are asked or instructed to do. Where there is a conflict between formal requirements and personal incentives, rational actors usually follow the incentives, not the requirements. Name these conflicts explicitly. Note where loss aversion will strengthen an incentive (threats of loss produce stronger responses than equivalent rewards).

**Step 4: Identify misalignments**
Compare predicted behaviour (Step 3) to desired behaviour (what the system needs each party to do). For every gap, ask: is the problem that the right behaviour isn't rewarded? That the wrong behaviour is? That the incentive exists but its magnitude is too small? That the incentive signal is delayed or unclear? Name the specific misalignment precisely.

**Step 5: Design realignment options**
For each misalignment, generate at least two redesign options. These may involve: changing who pays or benefits, changing the timing of incentive signals, introducing new consequences (positive or negative), making incentives more transparent, or restructuring the relationship between parties. Evaluate each option: does it align incentives without creating new misalignments elsewhere?

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences, then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Specific focus** — Zoom in on one aspect of this analysis
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

**System Overview**
[The system being examined, what it is trying to achieve, and the current behavioural problem]

**Incentive Map**

| Party | Desired behaviour | Formal incentive | Informal incentive | Predicted behaviour | Misalignment? |
|---|---|---|---|---|---|
| [Party 1] | [what we want] | [formal reward/penalty] | [social, reputational] | [what they'll actually do] | [Yes/No — why] |
| [Party 2] | ... | ... | ... | ... | ... |

**Key Misalignments**
[Numbered list of the most significant gaps between predicted and desired behaviour, with root cause for each]

**Redesign Options**
[For each misalignment: 2+ redesign options with trade-offs]

**Recommended Interventions**
[Prioritised list: which realignments have the highest expected impact and lowest implementation cost]

---

## Notes

The principal-agent problem is the most common form of incentive misalignment: the person taking action (agent) has different interests from the person bearing the consequences (principal). It appears in employment, contracting, professional services, politics, and financial intermediation. The solution set is well-studied: monitoring, performance-based pay, reputation mechanisms, aligning time horizons, and skin-in-the-game structures.

Incentive mapping is not about assuming people are greedy or calculating — it is about acknowledging that all people respond to the environment they are in, and that environments can be better or worse designed. A finding that "the incentive structure pushes toward X" does not mean people are bad; it means the structure needs redesign.

Pairs with `/s4h-game-theory-mechanism-design` when you want to formally design a system that aligns incentives — mechanism design is the rigorous version of redesign. Pairs with `/s4h-systems-feedback-mapping` when the incentive problem is embedded in a larger feedback dynamic. When the misalignment is driving visible conflict, `/s4h-social-incentive-analysis` addresses the political and relational dimensions.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Incentives mapped. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-game-theory-mechanism-design` — Formally design a system where the right incentives are built into the rules
  - `/s4h-economics-externalities` — Some of the costs or benefits are falling on parties outside this map
  - `/s4h-economics-coordination` — The misalignment is producing collective action failure, not just individual dysfunction
  - **Done** — Wrap up and synthesise what we have so far
