# Pyramid Principle

> Core value: Ensure clear expression with logical progression

---

## Definition

The Pyramid Principle is a **top-down** expression structure:

1. **Conclusion-first**: The most important conclusion comes first
2. **Layered support**: Upper-level conclusions are supported by lower-level arguments
3. **Logical progression**: Items at the same level have a logical relationship

```
        +---------------+
        | Core Conclusion|  <-- Say first
        +---------------+
              |
    +---------+---------+
    v         v         v
+-------+ +-------+ +-------+
|Arg 1  | |Arg 2  | |Arg 3  |  <-- Say next
+-------+ +-------+ +-------+
    |         |         |
    v         v         v
+-------+ +-------+ +-------+
|Detail1| |Detail2| |Detail3|  <-- Say last
+-------+ +-------+ +-------+
```

---

## When to Use

**Typical application scenarios**:
- Report structure design
- PPT narrative logic
- Executive summary writing
- Oral presentation preparation

**Usage principles**:
- Conclusion-first: Core viewpoint comes first
- Top-down: Upper level summarizes the lower level
- Grouped by category: Items in the same group belong to the same category
- Logical progression: Arranged in logical order

**Structure template**:
1. Core conclusion (1 sentence)
2. Key arguments (3-5 points)
3. Supporting data (facts/numbers/cases)

---

## Why It Matters

| Expression Style | Reader Experience | Problem |
|-----------------|-------------------|---------|
| Details first, conclusion last | Don't know what you're saying | Information overload, can't find the key point |
| Conclusion first, arguments after | Core viewpoint visible at a glance | Clear and efficient, easy to understand |

Business report readers are typically decision-makers with limited time who need to grasp the core quickly.

---

## Core Principles

### Principle 1: Conclusion-first

**Every expression should lead with the conclusion.**

❌ "We researched the market, found the scale is large, competitors are also growing, user demand is rising, so we think we should enter."

✅ "Recommend entering this market. Three reasons: large market size, low competition intensity, strong user demand."

### Principle 2: Top-down

**The upper level summarizes the lower level; the lower level supports the upper level.**

Each level should answer "why is the upper-level conclusion valid."

```
Conclusion: Should enter this market
|
+-- Argument 1: Large market size (10 billion, 30% annual growth)
+-- Argument 2: Low competition intensity (CR3 only 40%)
+-- Argument 3: Strong user demand (survey shows 80% of users have demand)
```

### Principle 3: Grouped by Category

**Arguments at the same level should belong to the same category and be MECE.**

❌ Disorganized arguments:
```
Conclusion: Should enter
+-- Large market size
+-- Competitor A is subsidizing
+-- Users are young
+-- We have technical advantages
```
(Mixed argument categories: market, competitor, user, and ourselves mixed together)

✅ Grouped arguments:
```
Conclusion: Should enter
|
+-- Market opportunity
|   +-- Large size (10 billion)
|   +-- Fast growth (30% annually)
|
+-- Competitive landscape
|   +-- Low competition intensity (CR3 only 40%)
|   +-- Competitors have weaknesses (subsidies unsustainable)
|
+-- Our advantages
    +-- Technical leadership
    +-- High user overlap
```

### Principle 4: Logical Progression

**Arguments at the same level should follow a logical order.**

Common orderings:
- Chronological: Past -> Present -> Future
- Structural: Whole -> Parts
- Importance: Most important -> Less important -> Other
- Deductive: Major premise -> Minor premise -> Conclusion

---

## Application in Reports

### Executive Summary

The report's first page (Executive Summary) is the top of the pyramid:

```markdown
## Core Conclusion

Recommend entering Market X, projected to achieve Y revenue within 3 years.

## Key Findings

1. **Clear market opportunity**: Market size 10 billion, 30% annual growth
2. **Favorable competitive landscape**: Top players haven't formed monopoly, differentiation space exists
3. **We have advantages**: Technical capabilities match, user base overlaps

## Recommended Actions

- Short-term: Small-scale pilot validation
- Medium-term: Key city expansion
- Long-term: Nationwide rollout
```

### Chapter Structure

Each chapter is also a small pyramid:

```markdown
## Chapter 2: Market Analysis

### Core Conclusion
Market is large and fast-growing, but segmented opportunities exist.

### Key Arguments
1. Overall size 10 billion, 30% annual growth
2. Sub-market A is growing faster (50%), with less competition
3. User demand is shifting from X to Y

### Detailed Analysis
[Data and cases supporting the above arguments]
```

### Paragraph Structure

Each paragraph is also a small pyramid:

❌ "Competitor A did a lot of marketing in 2023, invested in Douyin and Xiaohongshu, also partnered with KOLs, the effect was good, users grew 50%."

✅ "Competitor A's user base grew 50%, primarily driven by aggressive marketing strategy. Specific actions include: Douyin advertising, Xiaohongshu operations, and KOL partnerships."

---

## Common Mistakes

### Mistake 1: No Conclusion

❌ Only data and arguments, no clear conclusion

✅ Every chapter and paragraph has a clear conclusion statement

### Mistake 2: Conclusion at the End

❌ "In summary, we believe..."

✅ Conclusion at the beginning, arguments follow

### Mistake 3: Mixed Levels

❌ Jumping expression, inconsistent argument levels

✅ Arguments at the same level belong to the same level of abstraction

### Mistake 4: Missing Support

❌ Has conclusion but no arguments

✅ Every conclusion is supported by 2-3 arguments

---

## Self-check List

After completing a report, check level by level:

- [ ] Does the report have a clear Executive Summary?
- [ ] Does each chapter have a clear core conclusion?
- [ ] Does each paragraph have a clear conclusion statement?
- [ ] Are upper-level conclusions supported by lower-level arguments?
- [ ] Are arguments at the same level MECE?
- [ ] Do arguments at the same level follow a logical order?

---

## Relationship with Other Methodologies

- **MECE Principle**: Arguments at the same level should be MECE
- **Issue Tree**: The Issue Tree is the underlying logic of pyramid structure
- **Hypothesis-driven method**: Hypothesis validation results should be presented in pyramid structure
