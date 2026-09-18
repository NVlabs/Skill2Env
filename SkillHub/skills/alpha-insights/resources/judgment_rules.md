# Judgment Rules

> **Role in Quality System**: Stage 5 execution flow — generation rules (Rules 1-7 "Rules Executor") + adversarial review (Rule 8a "Adversarial Challenger" + Rule 8b "Blind Spot Scanner")
> **Purpose**: Decision engine for Stage 5 insight generation
>
> **Core Value**: Encoding seasoned analysts' "intuitive judgment" into executable rules
>
> **Related Modules**:
> - [`hypothesis_driven.md`](../methodology/hypothesis_driven.md) - Hypothesis-driven method
> - [`pre_mortem.md`](../methodology/pre_mortem.md) - Pre-mortem analysis
> - [`first_principles.md`](../methodology/first_principles.md) - First Principles thinking
> - [`triangulation.md`](../methodology/triangulation.md) - Triangulation (verification level standards)

---

## ⛔ Stage 5 Execution Instructions (Mandatory, Cannot Be Skipped)

> **Stage 5 is a pure introspection phase — no external actions like search/fetch.**
> **Historical lesson**: Stage 4 is time-consuming, and AI tends to jump directly to "write the report," causing Stage 5 to be entirely skipped.
> **Therefore, this section uses Agent Subagents to make Stage 5 a "tool-call-intensive" phase, ensuring execution.**

### Execution Flow (Strict Sequential Order)

```
Input: Stage 4's evidence_base.md

Step 1: Execute Rules 1-7 sequentially (all tiers execute the full generation rule set; Rules 8a/8b run in Steps 3-4)
   ⛔ After each rule completes, broadcast a one-line progress summary to the user (see format below)
   ↓
Step 2: User confirms insight direction (after Rule 7 ranking, before Red/Blue Team review)
   → A-class core insights (18-20 points): Use AskUserQuestion to discuss one by one
   → B-class core insights (16-17 points): Use AskUserQuestion for batch confirmation
   ⛔ This step cannot be skipped. Only start Red/Blue Team review after user confirms direction, to avoid reviewing insights the user doesn't endorse
   ⚠️ When AskUserQuestion is unavailable: display the insight list directly in conversation and request confirmation — equivalent effect
   ⚠️ When user rejects all insights: discuss points of disagreement → fall back to Stage 4 for additional data / fall back to Stage 2 to redefine the problem
   ↓
Step 3: Launch Red-Team Subagent (Rule 8a)
   → Use Agent tool, prompt template below
   → Receive challenge results, evaluate and correct insights
   ⚠️ Red Team corrections happen in session context (no file writes). Corrected insights are passed directly to Step 4 Blue Team. Blue Team scans for blind spots based on the Red Team-corrected version. Final version is written to insights.md in one batch in Step 5.
   ⚠️ When Agent tool is unavailable: execute Red Team prompt sequentially in the main session, output challenges role by role
   ↓
Step 4: Launch Blue-Team Subagent (Rule 8b)
   → Use Agent tool, prompt template below
   → Receive blind spot scan results, decide whether to supplement research
   ⚠️ When Agent tool is unavailable: execute Blue Team prompt in the main session
   ↓
Step 5: Output insights.md (must include complete structure, see template below)
   → If Red/Blue Team had major corrections (fatal challenges/high-impact blind spots), briefly inform user of changes
   ↓
Step 6: Stage transition output
   ━━━ Stage 5 Complete ━━━
   📦 Deliverable: insights.md [Generated]
   ☑️ User confirmation: Insight confirmation [Completed / Partially modified]
   ➡️ Next: Stage 6 Report Generation
```

### Rule Execution Broadcast Format (Step 1 Mandatory)

After each rule execution, output a one-line progress summary so the user sees the process rather than a black box. Format:

```
🔧 Rule N/Total — {Rule Name}: {One-sentence result summary}
```

Example (Tier 3, Step 1 executes Rules 1-7; Rule 8 in Steps 3-4 via Subagent):
```
🔧 Rule 1/7 — So What Chain: Applied ≥3-layer reasoning to 6 core findings ✅
🔧 Rule 2/7 — Insight Filter: 14 candidates → 4-dimension scoring → 8 retained (A-class: 3, B-class: 5)
🔧 Rule 3/7 — Key Variables: Identified 3 key variables (regulatory policy, competitive landscape, technology iteration)
🔧 Rule 4/7 — Contrarian Test: Challenged 4 industry consensus views, found 1 evidence-backed contrarian insight
🔧 Rule 5/7 — Actionability: 5 recommendations SMART-tested, 4 passed, 1 needs timeline added
🔧 Rule 6/7 — Pre-mortem: Identified Top 5 failure causes, 3 addressable, 2 flagged as external risks
🔧 Rule 7/7 — Priority Ranking: P1 core insights 3 · P2 background insights 3 · P3 supplementary 2
→ Entering Step 2: Please confirm insight direction. After confirmation, Red/Blue Team review (Rules 8a/8b) will begin
```

⛔ Do not merge Rules 1-7 into a single output. Each rule must be broadcast independently so the user can judge process quality.

### ⛔ Gate Rule

**The first step of Stage 6 must be**: Read `insights.md`. If the file doesn't exist, **must return to Stage 5 for execution**.

### Red-Team Subagent Prompt Template

```
Launch a subagent using the Agent tool with the following prompt:

You are a seasoned Red Team reviewer. Your mission is to challenge the reliability of the following business analysis insights.
You must think like a genuine adversary trying to disprove these conclusions — not nitpicking, but genuinely believing the analysis may be wrong.

## Context
[Paste the research topic description and context]

## Insights Under Review
[Paste all core insights, including scores and evidence support]

## Your Task
For each core insight, assume the following 4 roles and challenge it. Each role has unique review preferences — you must challenge from that role's values and experience, not with generic questioning.

### Role 1: Competitor CEO
> Background: You are the CEO of the #2 player in the industry. Over the past 5 years, you've seen too many "moats" get disrupted. What you despise most is competitors treating first-mover advantage as a barrier.
> Review bias: Business model replicability, true strength of resource barriers, whether network effects genuinely exist
> Core question: If I threw 3x the resources to replicate this strategy, could I do it in 6 months? Is the moat maintained by technology, data, network effects, or merely a time gap?

### Role 2: Regulatory Policy Advisor
> Background: You have 15 years of policy research experience with the NDRC and market regulators. You've witnessed multiple industry overhauls (education "Double Reduction" policy, platform antitrust, Data Security Law). Your professional instinct asks: "Can this model survive regulatory tightening?"
> Review bias: Policy compliance, data privacy risks, changes in industry entry barriers, antitrust risks
> Core question: If a targeted policy drops tomorrow, does the business model immediately fail? What's the most likely regulatory direction?

### Role 3: Skeptical Investor
> Background: You manage a $700M fund and once lost 40% by trusting a founder's optimistic assumptions. Now you're instinctively wary of any "high growth projection." You only trust verifiable data, not narratives.
> Review bias: Assumption sensitivity, data reliability, valuation reasonableness, exit mechanisms
> Core question: Which core assumption is most fragile? If key data deviates by 30%, does the conclusion flip? Where does the evidence chain for growth projections break?

### Role 4: Execution-Level COO
> Background: You've led 500-person teams and experienced 3 cases of "strategically correct but execution failure." You know organizational inertia, talent gaps, and cross-departmental coordination are the real reasons most good strategies fail.
> Review bias: Execution feasibility, organizational capability match, resource sufficiency, timeline reasonableness
> Core question: Does the team have the capability to execute? What key capabilities are currently missing? Who internally will resist, and why?

## Output Format
For each insight:
| Role | Sharpest Challenge | Challenge Intensity (Fatal/Substantive/Manageable/Weak) | Recommended Handling |
Each insight needs at least 1 substantive challenge. If all 4 roles can't find a substantive challenge, the insight may be too conservative.
```

### Blue-Team Subagent Prompt Template

```
Launch a subagent using the Agent tool with the following prompt:

You are a seasoned Blue Team reviewer — a quality director who has seen too many "appears complete but actually has blind spots" analysis reports.
Your career: 8 years as an engagement manager at McKinsey, then 5 years as head of corporate strategy. You've seen the best analysis reports and the most polished garbage — the difference isn't what they analyzed, but what they missed.
Your review mindset: Not looking for errors, but looking for "didn't think of that." An analyst's biggest blind spot isn't mistakes — it's the boundary of their vision.

## Context
[Paste the research topic description and context]

## Current Insight Set
[Paste all insights, including the Red Team-corrected version]

## Your Task
Scan across the following 5 dimensions, checking for analysis gaps. For each dimension, you must give a definitive judgment — no hedging.

1. **Stakeholder Coverage**: Are key stakeholder perspectives missing?
   > Checklist: Customers/users, suppliers, channel partners, employees/unions, regulators, community/public, competitor ecosystem partners — which didn't appear in the analysis?

2. **Temporal Dimension Coverage**: Does the analysis only look at a current snapshot, ignoring dynamic changes?
   > Checklist: Path dependency (how historical decisions constrain the future), rate of change (is the trend accelerating or decelerating), time windows (how big is the opportunity window), seasonality/cyclical factors

3. **Data Blind Spots**: Does the evidence base have systematic biases?
   > Checklist: Survivorship bias (only successful cases analyzed), geographic bias (Tier 1 cities ≠ national), metric bias (same indicator defined differently across sources), silent data (no data ≠ not important)

4. **Causal Chain Completeness**: Are there logical leaps from evidence to conclusions?
   > Checklist: Correlation treated as causation, implicit assumptions not made explicit, intermediate variables ignored, reverse causality possibility

5. **Second-Order Effects**: Does the analysis only cover direct impacts?
   > Checklist: How will competitors react, cascading changes in supply chain upstream/downstream, second-order user behavior adaptation, policy spillover effects

## Output Format
| # | Dimension | Gap Found? | Gap Description | Impact Level (High/Medium/Low) | Recommended Action |
High-impact blind spots must include recommended research directions. If a dimension truly has no gaps, write "✅ Adequately covered" with explanation — do not write "no findings at this time" as a cop-out.
```

### insights.md Output Template

```markdown
# Insight Summary

> Research topic: [Topic]
> Tier: Tier [X]
> Generated: [Date]

## A-Class Core Insights (18-20 points)

### Insight 1: [Title]
- **Score**: Specificity X + Uniqueness X + Actionability X + Impact X = XX points
- **Data support**: [Evidence ID, verification level]
- **Evidence Reasoning Chain** (A-class mandatory):
  - Evidence [ID]: [one-line content] → Supports this conclusion because [specific logic]
  - Evidence [ID]: [one-line content] → Supports this conclusion because [specific logic]
- **So What Chain**: Phenomenon → Implication → Strategy → Action
- **User confirmation status**: ⏳ Pending / ✅ Confirmed / ✏️ Modified

## B-Class Core Insights (16-17 points)
[Same format, but presented in batch]

## Recommendations
### Recommendation 1: [SMART description]
- **Risk alert**: [Pre-mortem result]

## Red Team Review Record
[Red-Team Subagent output + handling results]

## Blue Team Review Record
[Blue-Team Subagent output + handling results]

## Key Variable Monitoring Checklist
| Variable | Current Status | Trigger Condition | Contingency Plan |
```

---

## Problem This Module Solves

After Stage 4 research execution, the AI collects extensive evidence and data. But:
- Which data are **key signals** and which are **noise**?
- Which insights are worth pursuing and which are **correct platitudes**?
- Which recommendations are **actionable** and which are **generic platitudes**?

Judgment Rules = **eight rules**, executed in sequence:

```
Evidence Base → [Rule 1] So What Chain
             → [Rule 2] Insight Filter
             → [Rule 3] Key Variable Identification
             → [Rule 4] Contrarian Test
             → [Rule 5] Actionability Test
             → [Rule 6] Pre-mortem Risk Check
             → [Rule 7] Priority Ranking
             → [Rule 8] Dual Review (8a Red-Team + 8b Blue-Team)
             → Output insights.md
```

---

## Rule 1: So What Chain

### Purpose

Dig from surface data to business essence. Prevent stopping at "describing phenomena."

### Operation

For each core finding, ask So What repeatedly, **at least 3 layers, until landing on a specific action**:

```
Layer 1 (Phenomenon): Market size 50B, growing at 25%
  → So What?
Layer 2 (Implication): Market is in rapid growth phase, the pie is expanding
  → So What?
Layer 3 (Strategy): First-mover advantage may be diluted by new entrants
  → So What?
Layer 4 (Action): Should pivot from C-end scoring to B-end solutions, build new moats
```

### Judgment Criteria

| Characteristic | Good So What Chain | Bad So What Chain |
|----------------|-------------------|-------------------|
| Depth | ≥ 3 layers | Stops at 1-2 layers |
| Landing point | Specific action | Platitudes like "strengthen competitiveness" |
| Logic | Progressive, causal | Jumps, missing intermediate reasoning |

---

## Rule 2: Insight Filter

### Purpose

Not every finding deserves a place in the report. Filter out low-quality insights.

### Four-Dimension Scoring

Score each candidate insight (1-5 points):

| Dimension | Definition | 5 points | 3 points | 1 point |
|-----------|-----------|----------|----------|---------|
| **Specificity** | Has specific data/cases | "B-end customer count trails competitor by 6x" | Has industry data but not directly mapped | "The market is changing" |
| **Uniqueness** | Contrarian/non-public/new finding | Uncovered hidden competitive dynamics | New angle but publicly available data | Common knowledge everyone knows |
| **Actionability** | Can translate to specific action | Points to clear product/org decision | Has direction but needs refinement | Cannot be acted upon |
| **Impact** | Influences key decisions | Changes strategic direction | Affects medium-scale decisions | Affects marginal decisions |

### Filter Rules

```
Total = Specificity + Uniqueness + Actionability + Impact (max 20)

18-20 → A-class core insight (discuss one by one, major coverage)
16-17 → B-class core insight (batch confirmation, moderate coverage)
11-15 → Supporting insight (optional inclusion)
 6-10 → Filter out
```

### Tiered Confirmation Mechanism

| Insight Tier | Score Range | Interaction Method | Report Coverage |
|-------------|-------------|-------------------|-----------------|
| **A-class core insight** | 18-20 | Use AskUserQuestion to discuss one by one | Major expansion |
| **B-class core insight** | 16-17 | Batch confirmation, single pass | Moderate coverage |
| Supporting insight | 11-15 | No separate confirmation | Brief mention or omit |

### Comparison Examples

**Insight A**: "China's SaaS market is growing rapidly"
→ Specificity 2 + Uniqueness 1 + Actionability 2 + Impact 3 = **8 points, filter out**

**Insight B**: "Leading vendor dominates C-end, but B-end customer count is only 1/6 of competitor's, and the gap is widening"
→ Specificity 5 + Uniqueness 4 + Actionability 5 + Impact 5 = **19 points, core insight**

### ⛔ Evidence Reasoning Chain (A-class mandatory, write immediately after scoring)

For each A-class insight (18-20 points), write out how each key piece of evidence **supports** the conclusion — not "related to," but "logically points in the same direction":

```
Evidence [ID]: [one-line content]
→ Supports this conclusion because: [specific logic — what direction does this evidence point, and why is it aligned with the conclusion]
```

⛔ If you cannot articulate a clear "supports because," the logical chain between evidence and conclusion is broken — either the conclusion direction needs revision, or different evidence is needed.

**Counter-example 1 — Direction reversed** (real error from test case):
```
Conclusion: "AI cannot replace McKinsey's trust premium"
Evidence: "Client said 'won't keep paying $500K for a report we suspect was generated by AI'"
→ ❌ This evidence actually supports: McKinsey's trust premium is being eroded by its own AI adoption (opposite direction)
```

**Counter-example 2 — Tautological** (common but worthless):
```
Conclusion: "AI consulting market has a huge opportunity"
Evidence: "Market CAGR 30%"
→ ❌ "Market growth validates the opportunity" — This just restates the evidence in different words without explaining why growth = opportunity (growth could be captured entirely by incumbents)
→ ✅ "30% growth rate means the market is not yet consolidated, leaving a window for new entrants — compare mature markets at 5% CAGR already divided among CR5"
```

---

## Rule 3: Key Variable Identification (80/20 Rule)

### Purpose

Among the many variables affecting conclusions, find the 20% key variables that determine 80% of outcomes. Focus energy, avoid spreading too thin.

### Operation

**Step 1**: List all variables affecting the decision

**Step 2**: Evaluate on two dimensions

| Variable | Impact (1-5) | Uncertainty (1-5) | Classification |
|----------|-------------|-------------------|----------------|
| Regulatory policy | 5 | 4 | **Key variable** |
| Competitive landscape | 5 | 3 | **Key variable** |
| Market size | 4 | 1 | Background variable (confirmed) |
| User awareness | 2 | 2 | Non-key variable |

**Step 3**: Focus rule

```
Key variable = Impact ≥ 4 AND Uncertainty ≥ 2
```

- **Key variables** (high impact + high uncertainty): Core discussion focus of the report, requires deep research
- **Background variables** (high impact + low uncertainty): Stated as context, no deep dive needed
- **Non-key variables** (low impact): Briefly mentioned or omitted

---

## Rule 4: Contrarian Test

### Purpose

Truly valuable insights often differ from consensus. Proactively challenge consensus to find overlooked opportunities and risks.

### Operation

**Step 1: List industry consensus** ("everyone thinks this" viewpoints)

**Step 2: Challenge each one**

| Consensus | Contrarian Perspective | Evidence Support? |
|-----------|----------------------|-------------------|
| "Massive market opportunity" | Addressable market may be small (data silos, regulatory restrictions) | To be verified |
| "Tighter regulation is negative" | Long-term positive for compliant leaders (clears small players) | Partial evidence |
| "First-mover advantage is unbreakable" | Technology iteration may let latecomers leapfrog | To be verified |

**Step 3: Verify**

For each evidence-backed contrarian perspective:
- Is the logic self-consistent?
- If true, what are the business implications?
- Is it worth being a core insight?

### Four Types of Contrarian Insights

| Type | Description | Example |
|------|------------|---------|
| **Consensus error** | Everyone is wrong | "You think the market is huge, but the addressable market is actually small" |
| **Reversed causation** | Cause and effect are reversed | "It's not subsidies driving growth, it's growth attracting subsidies" |
| **Second-order effect** | Ignoring indirect impacts | "Cracking down on fraud causes short-term pain but long-term benefits for compliant platforms" |
| **Hidden trend** | Inconspicuous but important trend | "Young people are proactively checking credit scores — a new behavioral trend" |

### Judgment Criteria

**Worth being a core insight**: Evidence-backed + logically consistent + significant business implications
**Should be dropped**: No evidence + speculation only + minor impact

---

## Rule 5: Actionability Test

### Purpose

Ensure output recommendations are actionable, not "correct platitudes."

### SMART Test

Each recommendation must answer 5 questions:

| Dimension | Question | Failing Example | Passing Example |
|-----------|----------|-----------------|-----------------|
| **Specific** | What exactly to do? | "Strengthen B-end expansion" | "Build a 10-person B-end sales team" |
| **M**easurable | How to measure success? | "Increase market share" | "Sign 20 bank clients" |
| **A**chievable | Is it achievable? | "Become global #1" | "Increase domestic B-end share to 30%" |
| **R**elevant | Related to core question? | Off-topic recommendation | Directly addresses core hypothesis |
| **T**ime-bound | When to complete? | "ASAP" | "Before Q2" |

### Quick Assessment

```
Pass 5 items → Actionable recommendation, include in report
Pass 3-4 items → Needs supplementary detail
Pass ≤ 2 items → Rewrite or delete
```

### Comparison Examples

❌ **Not actionable**: "Strengthen B-end business expansion to increase market share"
→ S ❌ M ❌ A ? R ✅ T ❌

✅ **Actionable**: "Before Q2, build a 10-person B-end sales team focused on banks and consumer finance companies, targeting 20 signed clients and 5M revenue contribution"
→ S ✅ M ✅ A ✅ R ✅ T ✅

---

## Rule 6: Pre-mortem Risk Check

### Purpose

Before outputting recommendations, predict "if the recommendation fails after execution, what's the most likely cause."

### Operation

Reference [`pre_mortem.md`](../methodology/pre_mortem.md) for the complete methodology. Here is the simplified version:

**Step 1**: Assume the recommendation fails 1 year after execution

**Step 2**: List Top 5 failure causes

**Step 3**: Evaluate and label

| Failure Cause | Probability (1-5) | Impact (1-5) | Addressable? | Mitigation |
|--------------|-------------------|-------------|-------------|------------|
| B-end market smaller than expected | 3 | 5 | Yes | Small-scale pilot validation first |
| Competitor moats too deep | 4 | 4 | Yes | Differentiated positioning |
| Team lacks capability | 5 | 5 | Yes | Hiring + training |
| Regulatory policy change | 2 | 5 | No | Uncontrollable, flag as risk |

**Step 4**: Write high-probability + addressable risks into the recommendation's "Risk Mitigation" section

### Output Format

After each core recommendation:

```markdown
**Risk Alert**:
1. [Risk 1]: [Mitigation]
2. [Risk 2]: [Mitigation]
3. [Uncontrollable risk]: Flagged as external risk, cannot be fully mitigated
```

---

## Rule 7: Priority Ranking

### Purpose

When there are multiple insights, rank by priority to ensure report focus.

### Ranking Matrix

```
              Impact High
                 │
     ┌───────────┼───────────┐
     │  P1 Core Insight │ P2 Background  │
     │ (High Impact+    │  Insight       │
     │  High Uniqueness)│ (High Impact+  │
Uniqueness ├──────────┼──────────┤
     │  P3 Supplementary│  P4 Filter Out │
     │  Insight         │                │
     │ (Low Impact+     │ (Low Impact+   │
     │  High Uniqueness)│  Low Uniqueness│
     └───────────┼───────────┘
                 │
              Impact Low
```

### Report Allocation Rules

| Priority | Report Share | Handling |
|----------|------------|---------|
| P1 Core Insight | 60-70% | Deep expansion, maximum coverage |
| P2 Background Insight | 20-25% | Brief background, supports core insights |
| P3 Supplementary Insight | 5-10% | Brief mention, or place in appendix |
| P4 | 0% | Do not include in report |

---

## Rule 8: Dual Review (Red-Team + Blue-Team)

### Purpose

After Rules 1-7, insights and recommendations are formed. But "formed" doesn't mean "reliable." Dual review is the final quality gate:

- **Red-Team (8a)**: Challenge "what was said" — do the conclusions hold up?
- **Blue-Team (8b)**: Check "what wasn't said" — are there analysis gaps?

Both must be **executed sequentially**: Red Team attacks first, corrections made, then Blue Team scans.

### Division of Labor

| Dimension | Red-Team (8a) | Blue-Team (8b) |
|-----------|--------------|----------------|
| Core question | Are conclusions correct? | Is the vision complete? |
| Challenge target | Existing insights and recommendations | Uncovered analysis gaps |
| Perspective source | 4 adversarial roles | 5 blind spot dimensions |
| Output | Weaken/correct/overturn insights | Supplement missing insights or flag known blind spots |

---

### 8a: Red-Team Adversarial Challenge

#### Core Logic

For each **core insight (Tier 1) and key recommendation**, assume 4 adversarial roles in sequence, each raising 1-2 sharpest challenges.

#### Four Adversarial Roles

| Role | Stance | Core Challenge Question | Attack Target |
|------|--------|----------------------|---------------|
| **Competitor** | "Your opportunity is my threat" | If I were the competitor CEO, what would I do in response? Does your moat truly exist? | Sustainability of competitive advantage |
| **Regulator** | "Compliance is the baseline" | Does this plan carry policy risk? If regulation tightens, does the business model hold? | Compliance and policy dependence |
| **Skeptical Investor** | "Data convinces me" | Which core assumption is most fragile? If key data deviates 30%, does the conclusion flip? | Data reliability and assumption sensitivity |
| **Execution-Level Manager** | "Good idea but can't be done" | Does the team have the ability to execute? Are resources sufficient? Will the organization resist? | Executability and organizational reality |

#### Execution Steps

**Step 1**: Select attack targets
- All A-class core insights (18-20 points)
- All P0-level recommendations
- Report core conclusions

**Step 2**: Challenge role by role

For each attack target, 4 roles each raise 1-2 sharpest challenges:

```
🔴 Red Team Challenge — Insight X: [Insight Title]

Competitor perspective: [Challenge content]
Regulator perspective: [Challenge content]
Skeptical Investor perspective: [Challenge content]
Execution-Level Manager perspective: [Challenge content]
```

**Step 3**: Evaluate and handle each challenge

For each challenge, determine:

| Challenge Intensity | Judgment Criteria | Handling |
|-------------------|-------------------|---------|
| **Fatal** | Evidence-backed, can overturn core logic | Correct or overturn insight, return to Rule 1 for re-analysis. **Inform user**: explain the fatal challenge + correction plan; user may accept correction or retain original insight (requires explicit confirmation flagged as "user overrode Red Team fatal challenge") |
| **Substantive** | Reasonable, weakens but doesn't overturn the conclusion | Correct insight wording, lower confidence level, add qualifying conditions |
| **Manageable** | Valid point, but clear mitigation exists | Add mitigation measures to recommendations |
| **Weak** | Theoretically possible but extremely low probability | Flag as "tail risk," no conclusion modification |

**Step 4**: Record Red Team review results

**Key principle**:
- Red Team is not a formality. If all 4 roles can't find a substantive challenge, the insight may be too conservative (lacking sharpness), not "perfect"
- Each core insight **must have at least 1 substantive or higher-level challenge** recorded and responded to
- **Non-compliance handling**: If a core insight has no substantive challenge → report to user → fall back to Rule 1 to dig deeper into the So What chain, increase sharpness, then re-submit to Red Team
- This is a **hard requirement**, not a suggestion. Insights without substantive challenges may not be written to the final insights.md

#### Output Format

```markdown
## Red Team Review

### Insight 1: [Title]

| Role | Challenge | Intensity | Finding Type | Handling |
|------|-----------|-----------|-------------|---------|
| Competitor | [Challenge content] | Substantive | Conclusion issue / Evidence gap / Direction gap / Scoring issue | Corrected wording / Needs supplementary search / ... |
| Skeptical Investor | [Challenge content] | Manageable | [Type] | [Handling] |

> **Finding Type Legend**: Conclusion issue (misinterpretation) → rewrite on the spot | Evidence gap (missing data) → submit to triage checklist for user decision | Direction gap (framework/sub-question bias) → submit to triage checklist for user decision | Scoring issue (confidence level mismatch) → adjust on the spot

### Correction Record

- Insight 1: Original "..." → Corrected to "...", Reason: Red Team challenge XX
- Recommendation 2: Added risk mitigation clause, Reason: Red Team challenge XX
```

---

### 8b: Blue-Team Blind Spot Review

#### Core Logic

Red Team attacks existing conclusions; Blue Team scans for **analysis gaps** — things "not in the field of vision."

#### Five Blind Spot Detection Dimensions

Scan across the following 5 dimensions, answering "are there gaps" for each:

**Dimension 1: Stakeholder Coverage**

Detection question: Does the analysis cover all key stakeholder perspectives?

| Stakeholder | Typical Omission |
|------------|-----------------|
| End users/consumers | Only looked at supply side, ignored real demand-side pain points |
| Competitors (non-leaders) | Only analyzed Top 3, ignored mid-tail innovators |
| Upstream/downstream suppliers | Ignored supply chain bargaining power shifts |
| Regulators/policymakers | Ignored how policy direction fundamentally constrains business models |
| Employees/internal organization | Ignored organizational capability and willingness at execution level |
| Investors/shareholders | Ignored how capital market expectations constrain strategic freedom |

**Dimension 2: Temporal Dimension Coverage**

Detection question: Does the analysis only look at a current snapshot, ignoring temporal dynamics?

| Time Blind Spot | Typical Omission |
|----------------|-----------------|
| Historical path dependency | Ignored "why things are the way they are" path analysis |
| Rate of change | Only looked at absolute values, ignored acceleration/deceleration trends |
| Time windows | Didn't assess urgency of opportunity/threat timing |
| Competitive reaction delay | Assumed competitors won't react, ignored game-theoretic dynamics |

**Dimension 3: Data Blind Spots**

Detection question: Does the evidence base have systematic gaps?

| Data Blind Spot | Detection Method |
|----------------|-----------------|
| Survivorship bias | Were only successful cases analyzed? Where's the failure case data? |
| Geographic bias | Are data sources concentrated in one region? |
| Temporal bias | Is the data time span sufficient? Could it be at a cyclical high/low point? |
| Metric bias | Do different sources define "market size" the same way? |
| Silent data | What data should exist but couldn't be found? What does the absence itself indicate? |

**Dimension 4: Causal Chain Completeness**

Detection question: Are there logical leaps in the reasoning chain from evidence to conclusions?

```
Check method: For each core insight, trace backward from conclusion to data —

Data A → [Reasoning 1] → Intermediate conclusion → [Reasoning 2] → Core insight → [Reasoning 3] → Recommendation

Check each [Reasoning] node:
- Is this reasoning step explicitly stated? Or assumed "the reader will naturally figure it out"?
- Are there implicit assumptions? If assumptions don't hold, does the conclusion still stand?
- Are there alternative explanations?
```

**Dimension 5: Second-Order Effects**

Detection question: Does the analysis only cover direct impacts, ignoring chain reactions?

| Effect Layer | Description | Example |
|-------------|------------|---------|
| First-order (analyzed) | Direct impact | "Tighter regulation → compliance costs rise" |
| Second-order (often missed) | Indirect impact | "→ Small players exit → industry concentration increases → leader pricing power strengthens" |
| Third-order (high value) | Systemic impact | "→ Leader profit margins improve → attract more capital → accelerate industry consolidation" |

#### Execution Steps

**Step 1**: Scan the current insight set across all 5 dimensions

**Step 2**: For each dimension, answer:
- Are there gaps? (Yes/No)
- If yes, what was missed?
- How significant is the impact? (High/Medium/Low)

**Step 3**: Handle based on impact level

| Impact Level | Handling |
|-------------|---------|
| **High** | Supplement research → generate new insights → re-enter Rules 1-7 flow |
| **Medium** | Flag in the report's "Research Limitations" section, noting possible impact direction |
| **Low** | Record but don't expand, note as future research direction |

**Step 4**: Append blind spot review results to the dedicated section in `insights.md`

#### Output Format

```markdown
## Blind Spot Review (Blue-Team)

### Identified Blind Spots

| # | Dimension | Blind Spot Description | Impact | Finding Type | Handling |
|---|-----------|----------------------|--------|-------------|---------|
| 1 | Stakeholder | XX perspective not covered | High | Evidence gap / Direction gap | Needs supplementary search → submit to triage checklist |
| 2 | Data | XX data has survivorship bias | Medium | Conclusion issue | Corrected insight on the spot |

### Supplementary Insights (Added Due to Blind Spot Review)

(If high-impact blind spots exist, supplementary insights go here, same format as core insights)

### Known Limitations

(Medium/low impact blind spot explanations for reader reference)
```

---

### Dual Review Judgment Criteria

| Characteristic | Good Dual Review | Poor Dual Review |
|----------------|-----------------|-----------------|
| **Red Team sharpness** | Each core insight has at least 1 substantive challenge | "No issues found" in one sentence |
| **Red Team honesty** | Fatal challenges lead to corrected conclusions | Knows there's a problem but covers for it |
| **Blue Team coverage** | All 5 dimensions scanned | Some dimensions skipped |
| **Blue Team depth** | Found specific gaps with impact assessment | "No obvious gaps" as a brush-off |
| **Closed loop** | All high-impact findings have remedial actions | Lists problems without handling them |
| **Transparency** | Candidly flags research limitations and correction records | Avoids acknowledging limitations |

---

## Complete Execution Flow

> Identical to the "⛔ Stage 5 Execution Instructions" Steps 1-6 at the top of this file. Not repeated here.

## insights.md Output Format

> The authoritative template is in the "insights.md Output Template" section above (Rule 2 scoring → Rule 7 ranking → Rule 8 dual review → final output). Not repeated here.

---

## Common Mistakes

| Mistake | Symptom | Prevention |
|---------|---------|-----------|
| So What too shallow | Stops at "market is growing, seize the opportunity" | Force ≥ 3 layers of questioning |
| Correct platitudes | "Need to strengthen competitiveness" | SMART test, all 5 items must pass |
| Ignoring contrarian perspectives | Only outputs consensus-aligned insights | Force contrarian test execution |
| Skipping Pre-mortem | Only talks about benefits, not risks | Every core recommendation must include risks |
| Spreading too thin | 10 insights with equal coverage | Use priority matrix to focus on P1 |
| No data support | Insights based on speculation | Filter out if "Specificity" ≤ 2 in four-dimension scoring |
| Red Team going through motions | All 4 roles "found no issues" | Every core insight needs at least 1 substantive challenge; otherwise insight may lack sharpness |
| Blue Team perfunctory | All 5 dimensions "no gaps" in one sentence | Every dimension must have a specific judgment; high-impact blind spots must have remediation |

---

## Module Interfaces

### Input

| Upstream | Input Content | Corresponding Rule |
|----------|-------------|-------------------|
| Stage 4 Evidence Base | Evidence list + verification levels + Framework-Evidence Map + framework analysis conclusions (including cross-framework findings) | Analytical basis for Rules 1-4 + cross-dimension pattern recognition (SKILL.md prerequisite step) |
| `hypothesis_driven.md` | Hypothesis verification status | Starting point for Rule 1 |
| `triangulation.md` | Verification level standards (A/B/C/D) | Evidence reliability assessment |

### Output

| Downstream | Output Content | Usage |
|-----------|---------------|-------|
| Stage 6 Report Generation | insights.md (insights + recommendations) | Report core content |
| `pyramid_principle.md` | Ranked insight structure | Pyramid Principle-organized report |
