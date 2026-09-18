---
name: skill-orchestrator
description: "Route multi-step marketing, product, or business challenges to the right sequence of ClawFu skills. Recommends which frameworks to combine, in what order, with handoff outputs between steps. Use when: planning a product launch end-to-end, combining positioning + offers + launch skills, running a customer-validation sprint, creating a content strategy pipeline, deciding which skills to chain for a complex project, or orchestrating a sales-enablement playbook."
license: MIT
metadata:
  author: ClawFu
  version: 1.1.0
  mcp-server: "@clawfu/mcp-skills"
---

# Skill Orchestrator

> Route multi-step challenges to the right sequence of ClawFu skills — recommending which frameworks to combine, in what order, with explicit handoff outputs between steps.

## When to Use This Skill

- **Starting a new project** and need the optimal skill sequence
- **Complex multi-faceted challenges** requiring multiple frameworks
- **Team alignment** on a structured approach across disciplines
- **Overwhelmed by options** — cut through skill paralysis
- **Chaining skills** where outputs from one feed into the next

## Methodology Foundation

| Aspect | Details |
|--------|---------|
| **Source** | ClawFu Skills orchestration system |
| **Core Principle** | The right frameworks in the right order compound insights — sequencing matters more than any single skill |
| **Sequencing Logic** | Foundation → Analysis → Strategy → Creation → Validation → Execution |

## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Recommends skill sequences for a challenge | Which skills to skip or substitute |
| Defines input/output handoffs between steps | Final strategic direction at each step |
| Creates custom workflows from the skill library | Resource allocation and timeline |
| Identifies when to branch or loop back | Go/no-go decisions at validation gates |

## Instructions

### Step 1: Analyze the Challenge

Classify the challenge type and context:

| Factor | Options |
|--------|---------|
| **Type** | Launch · Validation · Content · Positioning · Decision · Sales · Video |
| **Stage** | Idea · Early · Growth · Mature |
| **Resources** | Solo · Small team · Large team |
| **Timeline** | Urgent · Normal · Flexible |

### Step 2: Match to Workflow or Build Custom Sequence

Check pre-built workflows in [WORKFLOWS.md](WORKFLOWS.md). If none fits, build a custom sequence following this phase order:

| Phase | Skill Types | Purpose |
|-------|-------------|---------|
| **1. Foundation** | first-principles, JTBD, audience-research | Understand reality |
| **2. Analysis** | competitive-analysis, inversion, pre-mortem | Identify challenges |
| **3. Strategy** | positioning, category-design, personas | Make strategic choices |
| **4. Creation** | offers, copy, content | Build the deliverable |
| **5. Validation** | six-thinking-hats, pricing-validation | Stress test |
| **6. Execution** | launch-formula, sales-pitch | Go to market |

### Step 3: Execute Step by Step

For each step in the sequence:

1. **State the skill and purpose** — why this step matters now
2. **List inputs** from previous steps
3. **Execute the skill** fully
4. **Capture outputs** — document key deliverables
5. **Validate before proceeding** — verify outputs are sufficient for the next step

**Validation checkpoint:** Before moving to the next skill, confirm the output includes the specific artifacts the next step needs. If not, iterate or add an intermediate step.

### Step 4: Synthesize Cross-Skill Insights

After completing the sequence:

- **Patterns** — themes emerging across multiple frameworks
- **Conflicts** — where Skill A says X but Skill B says Y, and how to resolve
- **Compounding insights** — conclusions that only emerge from the combination

## Examples

### Example: AI Writing Tool Launch

**Challenge:** Launching an AI writing tool for marketers in a competitive market (Jasper, Copy.ai)

**Recommended sequence (modified Product Launch):**

```
1. competitive-analysis → Map landscape (Jasper, Copy.ai, ChatGPT)
2. first-principles → Challenge "AI writing tool" category assumptions
3. persona-generator → Define specific segments (not just "marketers")
4. category-design → Can you own a new category?
5. positioning → Differentiate using competitive gaps
6. grand-slam-offers → Create irresistible offer structure
7. pre-mortem → What could kill the launch?
8. launch-formula → Sequence the mechanics
```

**Handoff example:** Step 3 (personas) feeds into Step 5 (positioning) — persona pain points define which competitive alternatives matter most.

See [WORKFLOWS.md](WORKFLOWS.md) for all pre-built workflows (Product Launch, Customer Validation, Content Strategy, Competitive Positioning, Sales Enablement, Decision Making, AI Video Production).

## Skill Boundaries

### What This Skill Does Well
- Sequencing skills for maximum compounding value
- Defining explicit handoffs between framework stages
- Adapting pre-built workflows to specific contexts

### What This Skill Cannot Do
- Execute the individual skills (it routes to them)
- Make strategic decisions — it structures the decision process
- Guarantee outcomes — quality depends on inputs at each step

## References

- Pre-built workflows: [WORKFLOWS.md](WORKFLOWS.md)
- Christensen, Clayton. "How Will You Measure Your Life?" — Job sequencing
- Rumelt, Richard. "Good Strategy Bad Strategy" — Strategic coherence
- Blank, Steve. "The Startup Owner's Manual" — Customer development sequence

## Related Skills

- [first-principles](../../strategy/first-principles/) — Start here for foundation
- [lean-canvas](../../validation/lean-canvas/) — Start here for validation
- [positioning](../../strategy/positioning/) — Start here for differentiation
- [content-strategy](../../content/content-strategy/) — Start here for content
- [ai-video-concept](../../video/ai-video-concept/) — Start here for AI video production
