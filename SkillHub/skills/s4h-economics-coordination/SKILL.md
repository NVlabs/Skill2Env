---
name: s4h-economics-coordination
description: "Diagnoses collective action failures, public goods problems, and why individually rational behaviour produces collective irrationality. Triggers: 'collective action problem', 'tragedy of the commons', 'free rider', 'everyone is acting in their own interest but the result is bad for all', 'why won't people contribute', 'public good', 'how do we get people to cooperate', 'commons', any situation where individual rationality produces group-level harm."
---

# Economics: Coordination Failure

Elinor Ostrom won the 2009 Nobel Prize for demonstrating what policymakers and economists had missed for decades: the tragedy of the commons is not inevitable. Communities have developed institutions — rules, monitoring, graduated sanctions, conflict resolution mechanisms — that manage shared resources sustainably without either privatisation or government control. But to solve the problem, you first have to diagnose it correctly.

The tragedy of the commons, formalised by Garrett Hardin in 1968, is a special case of a broader phenomenon: coordination failure. The general structure is this — when the benefits of an action are diffuse (shared by many) and the costs are borne by the individual, rational actors will undercontribute to the collective good. When the benefits of a bad action are private and the costs are shared, rational actors will overuse the commons. Individually rational. Collectively catastrophic.

This manifests in four overlapping problem types:
1. **Public goods problems**: non-excludable, non-rival goods (clean air, public safety, open-source software) are underproduced because producers cannot capture the benefit — free riders consume without contributing.
2. **Common pool resource problems**: depletable shared resources (fisheries, groundwater, shared codebases) are overused because the individual captures the full benefit of taking but shares the cost of depletion with everyone.
3. **Assurance games**: everyone would prefer to cooperate, but only if enough others do too. If you're not sure others will cooperate, defecting is rational — and this suspicion can make cooperation collapse even when everyone prefers it.
4. **Coordination games**: multiple equilibria exist and parties need to agree on which one to use, but have no mechanism to communicate and commit.

Ostrom's institutional analysis provides the solution toolkit. The goal of this skill is to correctly identify which problem type is present — they have different structures and require different solutions.

---

## Your Process

**Step 1: Describe the collective action failure**
What is the group failing to achieve? What individual behaviours are producing the bad collective outcome? Be specific: name the actors, the actions, and the outcome that results when everyone acts individually rationally.

**Framing check:** Confirm the failure before continuing. State what you've identified in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [one-sentence framing — what group is failing to coordinate, and what individually rational behaviour is producing the bad collective outcome]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Diagnose the problem type**
Classify the coordination failure by structure:

- **Public good problem**: Is the good non-excludable (you can't stop people using it) and non-rival (one person's use doesn't deplete it for others)? → The challenge is funding and producing the good; the solution involves either public provision, taxation, or making the good excludable.
- **Common pool resource problem**: Is the resource depletable, and can it be overused? → The challenge is managing depletion; the solution involves defining use rights and monitoring usage.
- **Assurance/threshold game**: Would everyone cooperate if they were sure others would too, but they don't have that assurance? → The challenge is building credible mutual commitment; the solution involves signalling, binding agreements, or critical mass strategies.
- **Pure coordination game**: Multiple equivalent outcomes exist and parties need to agree on one without being able to talk freely? → The challenge is establishing a focal point or convention.

Many real situations have features of multiple types. Name the primary structure and any secondary dimensions.

**Step 3: Map the incentive structure**
For the primary problem type: who gains from defecting? Who bears the cost of others' defection? What is the individual payoff from defecting vs. cooperating, and how does this change as more others cooperate or defect? Is the temptation to defect unconditional (prisoners' dilemma structure) or conditional on what others do (assurance game)?

**Step 4: Assess existing institutions**
What coordination mechanisms, rules, norms, or enforcement structures already exist? Are they working? If not, why? Apply Ostrom's design principles for effective commons governance: Are boundaries clearly defined? Are usage rules matched to local conditions? Do affected parties have voice in rule-making? Is monitoring occurring? Are graduated sanctions in place? Do conflict resolution mechanisms exist?

**Step 5: Generate institutional solutions**
For the specific failure type and context, generate solutions from three categories:
- **State/regulatory solutions**: Regulation, taxation, public provision, privatisation, legal enforcement.
- **Market solutions**: Tradeable permits, property rights assignment (Coase), competitive mechanisms that reveal information.
- **Community/institutional solutions** (Ostrom's third way): Collective governance by the affected community — shared rules, social norms, reputation, peer monitoring, graduated sanctions.

For each solution, assess: Does it change the incentive structure so cooperation becomes individually rational? What are the conditions under which it works? What are the failure modes?

**Step 6: Recommend and sequence**
Select the best institutional solution given the context — scale, existing relationships, political feasibility, monitoring costs. Identify what needs to be in place first: critical mass, trust-building, rule legitimacy, or information sharing. Coordination problems often require sequenced interventions, not single-shot solutions.

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

**The Coordination Failure**
[What the group is failing to achieve; what individual behaviours are producing the bad collective outcome]

**Problem Type**
[Primary classification — public good / common pool / assurance game / coordination game — with structural explanation]

**Incentive Structure**
[Who gains from defecting; who bears the cost; the individual payoff calculation that makes defection rational]

**Existing Institutions**
[Current rules, norms, enforcement mechanisms — what's working and what isn't, assessed against Ostrom's design principles]

**Institutional Solutions**

| Mechanism | Type | Changes incentives how? | Conditions for success | Key risk |
|---|---|---|---|---|
| [e.g., cap-and-trade] | Market | [makes defection costly via permit prices] | [monitoring infrastructure, political buy-in] | [regulatory capture, leakage] |
| [e.g., community governance] | Ostrom | [self-enforcement via reputation and norms] | [small enough group, repeated interaction] | [scale limits, new entrants] |

**Recommended Approach**
[Preferred mechanism, why it fits this specific context, and what implementation requires first]

---

## Notes

Ostrom's core contribution is the demolition of the false binary between "privatise it" and "regulate it." Her extensive field research showed that communities can and do self-govern common resources effectively — often more effectively than either markets or governments — when the right institutional conditions are in place. The key conditions: small enough group for peer monitoring, clear membership, rules with local legitimacy, graduated sanctions, and conflict resolution mechanisms. When these conditions are absent, self-governance fails and external intervention is needed.

The coordination problem is structurally different from the prisoners' dilemma: in a coordination game, everyone prefers to cooperate but needs assurance that others will. In a prisoners' dilemma, the temptation to defect exists even when you know others will cooperate. Correctly distinguishing these is essential — the solutions are different. Assurance games are solvable through credible commitment; prisoners' dilemma structures require changing the payoffs.

Pairs naturally with `/s4h-game-theory-prisoners-dilemma` (the formal analysis of the defection structure), `/s4h-systems-archetype-matching` (tragedy of the commons is a named systems archetype), and `/s4h-economics-externalities` (the underlying mechanism: individual decision-maker externalises costs onto the group). For the design side — how to create the rules that make cooperation individually rational — see `/s4h-game-theory-mechanism-design`.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Coordination failure diagnosed. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-game-theory-prisoners-dilemma` — Analyse the defection structure and find paths to cooperation
  - `/s4h-game-theory-mechanism-design` — Design the rules that make cooperation individually rational
  - `/s4h-economics-externalities` — The coordination failure is driven by unpriced external costs
  - **Done** — Wrap up and synthesise what we have so far
