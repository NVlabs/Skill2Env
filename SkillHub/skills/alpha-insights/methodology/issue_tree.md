# Issue Tree (Problem Tree / Logic Tree)

> Source: Management consulting industry standard
> Core value: Visually decompose complex problems

---

## Definition

An Issue Tree is a tool for **hierarchically decomposing** complex problems into manageable sub-questions.

- Each level is an expansion of the level above
- Items at the same level are MECE
- The bottom level consists of specific, actionable, verifiable questions

---

## When to Use

**Typical application scenarios**:
- Complex problem decomposition
- Research scope definition
- Team division of work
- Analysis progress tracking

**Usage principles**:
- Start from the core question and decompose level by level
- Each level follows the MECE principle
- Decompose to an actionable/analyzable granularity

**Usage flow**:
1. Define the core question (problem statement)
2. First-level decomposition (2-4 key issues)
3. Progressive refinement (down to an actionable level)
4. Priority ranking (label P0/P1/P2)

---

## Types of Issue Trees

### 1. Why Tree

Used to **find root causes**, reasoning backward from the result.

```
Why are sales declining?
+-- New user decrease
|   +-- Channel traffic decline
|   +-- Conversion rate decline
+-- Existing user churn
    +-- Product experience issues
    +-- Competitor poaching
```

### 2. How Tree

Used to **find solutions**, reasoning forward from the goal.

```
How to improve user retention?
+-- Increase product value
|   +-- Add core features
|   +-- Optimize user experience
+-- Increase switching costs
    +-- Membership system
    +-- Social relationships
```

### 3. Hypothesis Tree

Used to **validate hypotheses**, listing possible answers.

```
Why is the competitor growing fast?
+-- Hypothesis 1: Aggressive subsidy strategy
+-- Hypothesis 2: Better product experience
+-- Hypothesis 3: Successful channel expansion
```

---

## Operating Steps

### Step 1: Define the Root Question

Define the tree's root node with a clear problem statement.

Good root questions:
- Specific and measurable
- Have a clear subject and scope
- Can be decomposed

❌ "How is the competitor doing" — Too vague
✅ "What are the drivers behind Competitor A's 50% user growth in 2023" — Specific

### Step 2: Choose the Decomposition Dimension

Choose a **single dimension** for the first-level decomposition.

Common decomposition dimensions:
- Components: Whole = Part 1 + Part 2 + Part 3
- Process steps: Process = Step 1 -> Step 2 -> Step 3
- Driving factors: Result = Factor 1 x Factor 2 x Factor 3
- Possible causes: Phenomenon = Cause 1 or Cause 2 or Cause 3

### Step 3: Expand Level by Level

Continue decomposing each node until:
- It can be directly answered or verified
- It can be assigned to a specific person/team
- A corresponding data source can be found

### Step 4: Verify MECE

At each level, verify:
- [ ] Are items at the same level independent of each other?
- [ ] Do items at the same level collectively exhaust the whole?

### Step 5: Label Priorities

Not all branches are equally important. Label:
- 🔴 High priority: Core driving factors
- 🟡 Medium priority: Secondary factors
- 🟢 Low priority: Can be temporarily ignored

---

## Example: Competitor Growth Analysis

```
Why is Competitor A growing fast?
|
+-- User growth 🔴
|   +-- New user acquisition 🔴
|   |   +-- Channel expansion (Douyin, Xiaohongshu)
|   |   +-- KOL partnerships
|   |   +-- Viral campaigns
|   +-- Existing user retention 🟡
|       +-- Product stickiness
|       +-- Membership system
|
+-- Revenue growth 🟡
|   +-- User base growth
|   +-- Per-user value increase
|
+-- Market share 🔴
    +-- Overall industry growth
    +-- Capturing competitor share
```

---

## Common Mistakes

### Mistake 1: Mixed Levels

❌ Questions from different levels mixed together
```
Why is the competitor growing?
+-- Price cuts
+-- Good marketing
|   +-- Heavy Douyin advertising
+-- Product optimization
```
("Douyin advertising" is a sub-item of "marketing" and shouldn't be at the same level as other items)

### Mistake 2: Insufficient Decomposition Depth

❌ Stopping at the abstract level
```
Why is the competitor growing?
+-- Good product
+-- Good marketing
+-- Good channels
```
(What does "good" mean? Needs further decomposition)

### Mistake 3: Excessive Decomposition Depth

❌ Jumping straight to details
```
Why is the competitor growing?
+-- Spent $5M on Douyin ads in Q1 2023
+-- Partnered with 20 KOLs on Xiaohongshu in Q2 2023
+-- ...
```
(Missing intermediate levels, hard to see the big picture)

---

## Application in This Skill

### Stage 2 Issue Intake

1. Transform the user's research question into an Issue Tree
2. Confirm with the user whether the decomposition is appropriate
3. Label priorities and determine research focus
4. Output to `research_definition.md`

### Output Format

```markdown
## Issue Decomposition (Issue Tree)

### Root Question
[User's original question]

### Decomposition Tree
[Issue Tree diagram]

### Priority Labels
- 🔴 High priority: [List]
- 🟡 Medium priority: [List]
- 🟢 Low priority: [List]

### Research Scope Confirmation
This research focuses on: [List high-priority branches]
Not covered this time: [List low-priority branches]
```

---

## Relationship with Other Methodologies

- **MECE Principle**: Each level of the Issue Tree must be MECE
- **Hypothesis-driven method**: An Issue Tree can be transformed into a Hypothesis List
- **Pyramid Principle**: The Issue Tree is the underlying logic of pyramid structure
