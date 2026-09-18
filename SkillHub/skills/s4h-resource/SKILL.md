---
name: s4h-resource
description: "Entry point for the resource toolkit. Routes to the right resource skill based on your situation. Use when you say 'resource', 'capacity', 'bottleneck', 'allocation', 'where should we focus', 'where are we wasting', 'highest leverage', 'what's slowing us down', or want resource reasoning applied without knowing which specific tool fits."
---

# Resource

Applies resource reasoning to allocation, constraints, leverage, and waste. Diagnoses what kind of resource work is needed and applies the right tool.

## Which tool fits

| You need to... | Tool |
|---|---|
| Distribute limited resources across competing needs | allocation-analysis |
| Find what is actually constraining throughput | bottleneck-analysis |
| Find the highest-leverage use of available resources | leverage-mapping |
| Find where resources are being lost, duplicated, or underused | waste-audit |

## Routing Decision

- **Have limited resources and competing priorities — need to allocate** → allocation-analysis
- **Things are moving slowly — need to find the actual constraint** → bottleneck-analysis
- **Want to maximize impact with what you have** → leverage-mapping
- **Sense that effort isn't producing commensurate output** → waste-audit
- **Unclear** → bottleneck-analysis; finding the constraint usually determines how to allocate and where the leverage is

**Framing check:** Confirm the specific resource situation before routing. State what you've identified — the system or context under analysis and the core resource tension (scarcity, blockage, inefficiency, or leverage) — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the resource situation and what kind of problem it is]. Is that right?"
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

## Allocation Analysis

*Distributes limited resources across competing needs.*

Make the trade-offs explicit rather than implicit. Map all competing claims on the resource. For each: what is the expected return on investment? What is the cost of under-resourcing? Are any allocations producing diminishing returns? Are any starved below a minimum threshold for effectiveness? Allocation decisions made without explicit trade-off analysis tend to satisfy the loudest voice rather than the best use.

**Output:** Allocation map with expected returns, identified diminishing returns, minimum thresholds, and the recommended distribution with explicit trade-off reasoning.

---

## Bottleneck Analysis

*Identifies what is actually constraining throughput.*

Apply Theory of Constraints logic: the system can only move as fast as its slowest point. Adding resources anywhere except the bottleneck doesn't improve throughput. Identify the current bottleneck: where does work queue up, where does it wait, where is output consistently below demand? Verify it's the actual bottleneck and not a symptom. Once identified: what would it take to elevate it?

**Output:** Bottleneck identified with evidence, verification that it's the system constraint (not a symptom), and the options to elevate it with effort estimates.

---

## Leverage Mapping

*Finds the highest-leverage use of available resources.*

Leverage is where the same input produces the most output. Not all investments are equal — some create multiplying effects (better systems, better people, better tools) while others are purely linear. For each candidate use of resources: is the return linear (1 unit in → 1 unit out) or multiplying (1 unit in → many units out over time)? Prioritize multiplying investments, especially those that unblock other work.

**Output:** Candidate uses of resources mapped by leverage type (linear vs. multiplying), with the highest-leverage options ranked and reasoning for each.

---

## Waste Audit

*Finds where resources are being lost, duplicated, or underused.*

Apply the seven wastes to knowledge work: (1) Overproduction — work done before it's needed, (2) Waiting — time spent blocked or idle, (3) Transport — handoffs that add no value, (4) Over-processing — more work than the task requires, (5) Inventory — work in progress that isn't being acted on, (6) Motion — effort that doesn't produce output, (7) Defects — rework from problems earlier in the process. Find the biggest waste category and its source.

**Output:** Waste audit across all seven categories, the biggest waste sources, and the highest-impact reductions.
