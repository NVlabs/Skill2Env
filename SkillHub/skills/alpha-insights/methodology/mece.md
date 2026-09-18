# MECE Principle

> Source: McKinsey & Company
> Core value: Ensure analysis is complete and non-overlapping

---

## Definition

**MECE** = **M**utually **E**xclusive, **C**ollectively **E**xhaustive

- **Mutually Exclusive**: No overlap between parts, no intersection
- **Collectively Exhaustive**: All parts together cover the whole, no gaps

---

## When to Use

**Typical application scenarios**:
- Problem decomposition and Issue Tree construction
- Market/user/product segmentation
- Data classification and organization
- Report structure design

**Usage principles**:
- Use early in analysis to ensure clear problem definition
- Use a single classification dimension, avoid mixing multiple dimensions
- Choose the appropriate decomposition method based on the analysis purpose

**Common decomposition patterns**:
- Dichotomy (internal/external, online/offline)
- Trichotomy (past/present/future, upstream/midstream/downstream)
- Process method (process step decomposition)
- Element method (key element decomposition)

---

## Why It Matters

Analysis without MECE produces two types of problems:

| Problem | Manifestation | Consequence |
|---------|---------------|-------------|
| Not exclusive | Overlapping categories | Double counting, logical confusion |
| Not exhaustive | Gaps exist | Missing key factors, incomplete analysis |

---

## Operating Steps

### Step 1: Define the Object to Classify

Define what you're decomposing in one sentence.

Examples:
- "Competitor's competitive strategies" — Too vague
- "Competitor's strategies in customer acquisition" — Clear

### Step 2: Choose the Classification Dimension

Choose a **single dimension** for segmentation, avoid mixing multiple dimensions.

Common classification dimensions:
- Time: past/present/future, or Q1/Q2/Q3/Q4
- Geography: domestic/international, or Tier 1/Tier 2/lower-tier cities
- Entity: enterprise/user/competitor/regulator
- Level: strategic/tactical/operational
- Attribute: high/medium/low, large/medium/small, core/non-core

### Step 3: Verify Exclusivity

Ask: **Is there overlap between these categories?**

Verification method:
- Each element should belong to only one category
- If an element can belong to two categories simultaneously, the classification dimension has a problem

❌ Incorrect example:
```
User classification:
- Young users
- High-spending users
- Tier 1 city users

Problem: A user can simultaneously be "young," "high-spending," and "Tier 1 city" — overlapping categories
```

✅ Correct example:
```
User classification (by age):
- 18-25 years old
- 26-35 years old
- 36-45 years old
- 46 and above

Each user belongs to only one age group, no overlap
```

### Step 4: Verify Exhaustiveness

Ask: **Do these categories together cover everything?**

Verification method:
- Are there elements that don't belong to any category?
- Is there an "other" category as a catch-all?

❌ Incorrect example:
```
User classification (by age):
- 18-25 years old
- 26-35 years old
- 36-45 years old

Problem: Where do users 46 and above go? Not exhaustive
```

✅ Correct example:
```
User classification (by age):
- 18-25 years old
- 26-35 years old
- 36-45 years old
- 46 and above

All age groups covered, exhaustive
```

### Step 5: Iterate and Optimize

If you find non-exclusivity or non-exhaustiveness:
1. Adjust the classification dimension
2. Add or merge categories
3. Re-verify

---

## Common MECE Frameworks

### 2x2 Matrix

Two dimensions cross to form four quadrants:

```
           High growth
              |
    Star      |  Question Mark
              |
--------------+--------------
              |
    Cash Cow  |  Dog
              |
           Low growth
    Low share         High share
```

### Tree Structure

Level-by-level decomposition, each level MECE:

```
Revenue
+-- User count
|   +-- New users
|   +-- Existing users
+-- Per-user value
    +-- Average order value
    +-- Purchase frequency
```

### Process Structure

In chronological order, each step MECE:

```
User journey
+-- Awareness
+-- Consideration
+-- Purchase
+-- Usage
+-- Referral
```

---

## Output Format

```markdown
## MECE Decomposition

### Object
[The whole to be decomposed]

### Classification Dimension
[Chosen single dimension] — Rationale: [Why this dimension]

### Decomposition Result
1. [Category 1]
2. [Category 2]
3. [Category 3]
...

### MECE Verification
- Exclusivity: [Any overlap? If so, how it's handled]
- Exhaustiveness: [Any gaps? If there's an "other" category, describe its content]
```

---

## Application in This Skill

### Stage 2 Issue Intake

Using MECE to decompose the research question:

1. Decompose the core question into sub-questions
2. Ensure sub-questions don't overlap
3. Ensure sub-questions cover all aspects of the core question
4. Visualize with an Issue Tree

### Verification Standards

After each decomposition, ask yourself:
- [ ] Does each sub-question belong to only one category?
- [ ] Do all sub-questions together cover the core question?
- [ ] Are there any important dimensions missing?

---

## Common Mistakes

### Mistake 1: Mixing Multiple Dimensions

❌ "Users are divided into: young users, high-spending users, Tier 1 city users"
✅ "Users by age are divided into: 18-25, 26-35, 36-45, 46 and above"

### Mistake 2: Missing the "Other" Category

❌ "Competitor strategies are: price wars, product innovation, marketing campaigns"
✅ "Competitor strategies are: price wars, product innovation, marketing campaigns, channel expansion, other"

### Mistake 3: Mixed Levels

❌ "Revenue sources: B2B clients, B2C clients, enterprise clients"
✅ "Revenue sources: B2B clients, B2C clients; B2B clients further divided into: enterprise clients, SMBs"

---

## Relationship with Other Methodologies

- **Issue Tree**: MECE's visualization tool
- **Hypothesis-driven method**: The Hypothesis List should be MECE
- **Pyramid Principle**: Report structure should be MECE
