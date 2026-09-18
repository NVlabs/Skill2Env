---
name: s4h-economics-margin
description: "Applies marginal thinking: the relevant decision is the next unit, not the average or the sunk cost. Triggers: 'should we do more of this', 'should we expand', 'should we cut', 'marginal cost', 'sunk cost', 'we've already invested so much', 'average cost', 'is this worth continuing', 'how much should we produce', 'at what point should we stop', any decision about quantity, scale, or whether to continue an existing commitment."
---

# Economics: Marginal Thinking

The most important word in economics is *marginal*. Not average. Not total. Not what we have spent. The relevant question is always: what happens at the *next unit*? Should we hire one more engineer? Produce one more batch? Add one more feature? Run one more campaign? The answer depends on the marginal cost (what that next unit costs) compared to the marginal benefit (what that next unit produces). When marginal benefit exceeds marginal cost, do more. When it doesn't, stop.

This sounds obvious. In practice, organisations almost universally fail to apply it. They use average cost when they should use marginal cost. They treat past expenditure as a reason to continue when it is economically irrelevant. They ask "should we have done this?" instead of "should we do more?" Alfred Marshall embedded marginal analysis at the heart of neoclassical economics precisely because pre-marginal thinking — evaluating the total or average rather than the increment — systematically produces wrong decisions.

The sunk cost fallacy is the most costly failure of marginal thinking. Resources already spent cannot be recovered — they are irreversible. They therefore cannot and should not influence forward decisions. Yet Kahneman's research confirms that people weight sunk costs heavily: the pain of a loss already incurred motivates continued investment in failing projects far more than forward-looking analysis would justify. This skill's core move is to strip sunk costs from the analysis and restate the decision in purely forward-looking marginal terms.

---

## Your Process

**Step 1: Identify the margin**
Clarify what the decision is actually about. Is it: (a) whether to do one more unit of something, (b) how many units to produce/do/hire, (c) whether to continue an existing project or commitment, (d) how to allocate resources across competing uses? The answer determines what "marginal" means in this context.

**Framing check:** Confirm the decision and the relevant margin before continuing. State what you've identified in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [one-sentence framing — the decision and what unit is being considered at the margin]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Identify and isolate sunk costs**
Before any forward analysis, identify all costs already committed that cannot be recovered: capital already spent, time already invested, contracts already signed, decisions already made. Label these explicitly as sunk costs. They are real — they happened — but they are economically irrelevant to the forward decision. State this clearly: "These costs have been incurred. They cannot be recovered. They will not appear in the forward analysis."

If the user is anchored on sunk costs (using past investment as a reason to continue), name this directly: this is the sunk cost fallacy. The question is not whether the past investment was good. The question is whether the next unit of investment produces a return.

**Step 3: Calculate marginal cost**
What does the *next unit* cost? Marginal cost includes all costs that change with the next unit — variable costs, additional labour, materials, time — but excludes fixed costs that are unchanged by the decision (these are already being borne regardless). Note: marginal cost often differs from average cost. For many activities, marginal cost is initially lower than average cost (economies of scale) but eventually rises as capacity constraints are reached.

**Step 4: Estimate marginal benefit**
What does the next unit produce? This might be: revenue, impact, risk reduction, optionality, information value. Be specific about the unit and the increment. Where marginal benefit is uncertain, use expected value (probability-weighted). Where marginal benefit is qualitative, use an explicit scale.

**Step 5: Make the marginal comparison**
Compare marginal benefit to marginal cost at the relevant unit. The rule:
- If marginal benefit > marginal cost → do more
- If marginal benefit < marginal cost → do less (or stop)
- If marginal benefit = marginal cost → you are at the optimum

Repeat this comparison across units if the decision involves quantity: where does the curve cross? At what level of output does marginal cost begin to exceed marginal benefit?

**Step 6: Apply the stopping rule**
Formulate the explicit stopping rule: under what conditions should this activity expand, maintain, or be cut? What signal indicates that marginal cost has exceeded marginal benefit? This forward-looking rule is the deliverable — it guides future decisions, not just the current one.

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

**The Decision at the Margin**
[What is being decided; what unit is under consideration]

**Sunk Costs (Isolated)**
[All past, irrecoverable costs — labelled as economically irrelevant to the forward decision]

**Marginal Analysis**

| Unit / scenario | Marginal cost | Marginal benefit | Net marginal value | Decision |
|---|---|---|---|---|
| Current level | [cost] | [benefit] | [benefit − cost] | [continue / stop] |
| +1 unit / next increment | [cost] | [benefit] | [benefit − cost] | [expand / maintain / cut] |
| [additional rows as needed] | | | | |

**Marginal Cost vs. Average Cost**
[Where these diverge, and why it matters for this decision]

**Stopping Rule**
[The explicit condition under which this activity should stop expanding, or be cut entirely]

**Recommendation**
[Forward-looking: what to do next, stripped of sunk cost reasoning]

---

## Notes

The most common error this skill corrects is treating average cost as if it were marginal cost. "Our average cost per unit is £X, so we should keep producing at this level" may be right or wrong depending on where marginal cost sits — and they frequently diverge, especially in businesses with high fixed costs. A software company with high fixed development costs and near-zero marginal distribution costs should price based on marginal cost (near zero), not average cost (high).

The second most common error: continuance arguments grounded in sunk costs. "We've invested £5m, we can't stop now" is not an economic argument — it is a psychological one. The correct question is always "what does the next pound of investment produce?" If the answer is "less than a pound of value," stop.

Marginal thinking pairs with `/s4h-economics-opportunity-cost` when the relevant comparison is between doing this and doing something else (opportunity cost) vs. doing this and doing less of it (marginal analysis). They address different decision structures. For decisions about whether to continue a commitment that may have been misconceived from the start, pair with `/s4h-decision-premortem-analysis`.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Marginal analysis done. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-economics-opportunity-cost` — The deeper question is what else we could do with these resources
  - `/s4h-decision-premortem-analysis` — Test whether the forward commitment is sound before making it
  - `/s4h-economics-incentive-mapping` — Someone's incentives may be driving the sunk cost thinking
  - **Done** — Wrap up and synthesise what we have so far
