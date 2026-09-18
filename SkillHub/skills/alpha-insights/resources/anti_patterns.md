# Anti-Pattern Firewall

> **Role in quality system**: Self-check tool -- standard library of known error patterns (execution manual for the "Error Pattern Detector" reviewer role)
> **Purpose**: Identify and avoid common error patterns in business analysis
>
> **Scope boundaries**:
> - This file = "what not to do" (error pattern identification + firewall)
> - `judgment_rules.md` = "how to judge" (8 rules, Insight generation process)
> - `report_standards.md` = "how to write" (report structure, language, format standards)
>
> **Loading timing**: Loaded at Stage 5 start (as background constraints for Rules 1-7, not as an independent execution step); loaded during Stage 6 report generation (using the self-check checklist below)

---

## Anti-Pattern Checklist (10 patterns to avoid)

---

## Anti-Pattern 1: Correct but Useless Truisms

**Symptoms**:
- Conclusions are correct but contain no information
- Universally applicable to any situation
- Cannot guide specific actions

**Examples**:
```
❌ "The new energy vehicle market is growing rapidly"
✅ "China's NEV penetration exceeded 50% in 2025, but growth decelerated from 87% to 32%, entering a zero-sum competition phase"

❌ "Companies need digital transformation"
✅ "This retailer's online channel accounts for only 12% of revenue, well below the industry average of 35% — the gap must be closed within 18 months"
```

**Detection method**:
- Replace the subject with another industry -- does it still hold true?
- Can this statement tell a decision-maker exactly what to do?

---

## Anti-Pattern 2: Data Dumping Without Insights

**Symptoms**:
- Lists large amounts of data
- No "So What"
- Reader doesn't know what it means

**Examples**:
```
❌ "The coffee market is worth 320B RMB in 2024, Luckin Coffee has 18,000 stores, per capita consumption is 12 cups..."
✅ "Luckin Coffee's 18,000 stores → density already exceeds convenience stores → the barrier to entry has shifted from 'opening stores' to 'operational efficiency'"
```

**Detection method**:
- Does every data point have a "So What" interpretation?
- What action recommendations can the reader derive from the data?

---

## Anti-Pattern 3: Ignoring Counter-Evidence

**Symptoms**:
- Only collects evidence supporting the hypothesis
- Ignores/downplays contradictory evidence
- One-sided conclusions

**Examples**:
```
❌ Only highlighting that a brand's user base grew 200%, while ignoring that CAC doubled and M1 retention is only 15%
✅ Analyzing both the growth curve and deteriorating unit economics to assess whether growth is sustainable
```

**Detection method**:
- Was counter-evidence actively sought?
- Was counter-evidence discussed thoroughly?

---

## Anti-Pattern 4: Disconnected from User Context

**Symptoms**:
- Generic template-style report
- Fails to answer "Relevance to Us"
- Recommendations cannot be applied to the user's scenario

**Examples**:
```
❌ "The insurance industry should increase technology investment" (no distinction between large and mid-size insurers)
✅ "As a mid-size insurer with 5B RMB in premiums, prioritize intelligent auto-claim assessment (highest ROI) rather than full-scale digitalization"
```

**Detection method**:
- Replace "companies" in the report with a specific company name -- does it still read well?
- Do the recommendations consider the user's specific constraints?

---

## Anti-Pattern 5: Causal Confusion

**Symptoms**:
- Treating correlation as causation
- Ignoring third variables
- Reversing causal direction

**Examples**:
```
❌ "Livestream e-commerce drove the brand's sales growth" (ignoring the role of promotional discounts)
✅ "Livestreaming contributed 30% of sales growth, but 70% came from discounts below 50% off — channel effect and price effect must be distinguished"
```

**Detection method**:
- Are there alternative explanations?
- Is the causal mechanism clear?

---

## Anti-Pattern 6: Static Analysis

**Symptoms**:
- Ignoring dynamic changes
- Assuming the current state persists
- Not considering competitive responses

**Examples**:
```
❌ "The company holds 25% market share, ranking first in the industry"
✅ "The company holds 25% market share, but it has declined steadily from 32% over the past three years, while the No.2 player rose from 15% to 22% — the gap is now only 3pp"
```

**Detection method**:
- Does the analysis consider the time dimension?
- Does it consider competitors' responses?

---

## Anti-Pattern 7: False Precision

**Symptoms**:
- Providing precise numbers from unreliable sources
- Over-quantifying vague concepts
- Using precision to mask uncertainty

**Examples**:
```
❌ "This market will reach 584.73B RMB by 2027" (a precise figure with no basis)
✅ "This market is projected at 400-600B RMB by 2027 (median of three analyst forecasts), with a growth rate range of 15-25%"
```

**Detection method**:
- Is the data source reliable?
- Is uncertainty annotated?

---

## Anti-Pattern 8: Non-Actionable Recommendations

**Symptoms**:
- Recommendations too abstract
- Lacking resource/time constraints
- No clear responsible party

**Examples**:
```
❌ "Strengthen brand building"
✅ "Invest 8M RMB by Q3 to sign 3 top-tier KOLs, targeting a 40% increase in brand search index"
```

**Detection method**:
- Do recommendations include specific actions, responsible parties, and timeframes?
- Does the user know what to do tomorrow after receiving the recommendation?

---

## Anti-Pattern 9: Framework Abuse

**Symptoms**:
- Using Frameworks for the sake of using them
- Frameworks disconnected from analysis
- Forced application

**Examples**:
```
❌ Analyzing a restaurant chain's expansion by forcing all six PESTEL dimensions, padding Political/Legal with filler
✅ Focusing on Economic (consumer downtrading trend) and Social (rise of solo dining) for deep analysis
```

**Detection method**:
- Does the Framework serve the analytical purpose?
- If you remove the Framework name, does the analysis still hold?

---

## Anti-Pattern 10: Ignoring Implementation Barriers

**Symptoms**:
- Only discussing "what should be done"
- Not discussing "how to achieve it"
- Ignoring organizational resistance

**Examples**:
```
❌ "Should expand into overseas markets"
✅ "Should expand into Southeast Asia, but must overcome: 1) Building a local team (6-12 months) 2) Payment and logistics infrastructure gaps 3) Incumbent competitors' first-mover advantage"
```

**Detection method**:
- Are implementation barriers discussed?
- Are there specific recommendations for overcoming barriers?

---

## Report Self-Check Checklist (for Stage 6)

> Stage 5 Insight generation self-checks are covered by the eight rules in `judgment_rules.md`.

**Stage 6 Report Generation Self-Check**:
- [ ] No "correct but useless truisms"
- [ ] Every data point has a "So What" interpretation
- [ ] Recommendations are specific and actionable (action/responsible party/timeline)
- [ ] Anchored to user context
- [ ] Implementation barriers are discussed
