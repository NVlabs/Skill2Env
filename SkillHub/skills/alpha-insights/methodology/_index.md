# Methodology Index & Rules

> **Purpose**: The single source of truth for methodologies — file list, usage rules, trigger conditions, checkpoints
>
> **Architecture**: Tier 1 (Base OS, bound to Stages, always active) + Tier 2 (Scenario Enhancement, auto-triggered)
>
> **Usage**:
> - Tier 1: Auto-loaded when the corresponding Stage is reached, no judgment needed
> - Tier 2: Auto-referenced when a research scenario matches the trigger conditions, with user notification
> - All methodology loading and referencing must be transparently shown to the user (core design principle)

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│               Methodology Two-Tier Architecture           │
├─────────────────────────────────────────────────────────┤
│                                                          │
│   Tier 1: Base OS (Always Active)                        │
│   ┌──────────┬──────────┬──────────┬──────────┐         │
│   │ MECE +   │Hypothesis│Triangu-  │ Pyramid  │         │
│   │Issue Tree│ -driven  │ lation   │ Principle│         │
│   ├──────────┼──────────┼──────────┼──────────┤         │
│   │ Stage 2  │ Stage 3-4│ Stage 4-5│ Stage 6  │         │
│   └──────────┴──────────┴──────────┴──────────┘         │
│                                                          │
│   Tier 2: Scenario Enhancement (Auto-triggered)          │
│   ┌──────────┬──────────┬──────────┐                     │
│   │  First   │   ACH    │Pre-mortem│                     │
│   │Principles│          │          │                     │
│   ├──────────┼──────────┼──────────┤                     │
│   │Scenario  │Scenario  │Scenario  │                     │
│   │ 3,4,5,7  │ 5,6,7    │2,6,7,8,9│                     │
│   └──────────┴──────────┴──────────┘                     │
│                                                          │
│   Independent Process (outside mapping system)           │
│   ┌──────────┐                                           │
│   │ Interview│ → Triggered by Stage 3.5 interview flow   │
│   └──────────┘                                           │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## Tier 1: Base OS (Always Active)

> **Definition**: Regardless of research scenario or framework combination, the following methodologies **must be used** at their corresponding Stage — they are the analysis "operating system."

### 1. MECE Principle + Issue Tree — Stage 2

| Item | Description |
|------|-------------|
| **Load Files** | `mece.md` + `issue_tree.md` |
| **Bound Stage** | Stage 2: Issue Intake |
| **Core Function** | Ensure problem decomposition is complete (no overlaps, no gaps), forming a structured sub-question tree |
| **Checkpoints** | 1) Are dimensions exhaustive? (Reference the selected framework's dimension structure for coverage) 2) Are dimensions mutually exclusive? 3) Decomposed to an analyzable level? 4) Are N/A dimensions explicitly marked? |

### 2. Hypothesis-driven Method — Stage 3-4

| Item | Description |
|------|-------------|
| **Load Files** | `hypothesis_driven.md` |
| **Bound Stage** | Stage 3: Hypotheses & Plan → Stage 4: Research Execution |
| **Core Function** | Guide analysis with testable hypotheses, avoiding information overload and aimless exploration |
| **Checkpoints** | 1) Have clear hypotheses been formed? 2) Are hypotheses falsifiable? 3) Is data collection organized around hypotheses? |

### 3. Triangulation — Stage 4-5

| Item | Description |
|------|-------------|
| **Load Files** | `triangulation.md` |
| **Bound Stage** | Stage 4: Research Execution → Stage 5: Insight Synthesis |
| **Core Function** | Verify data credibility through multi-source cross-validation, ensuring reliable conclusions |
| **Checkpoints** | 1) Do core data points have 2+ independent sources? 2) Are sources truly independent? 3) Is verification level marked (A/B/C/D)? |

### 4. Pyramid Principle — Stage 6

| Item | Description |
|------|-------------|
| **Load Files** | `pyramid_principle.md` |
| **Bound Stage** | Stage 6: Report Generation |
| **Core Function** | Ensure report structure is clear, conclusion-first, logically progressive |
| **Checkpoints** | 1) Is the conclusion first? 2) Are arguments layered in support? 3) Is logic clear without gaps? |

---

## Tier 2: Scenario Enhancement (Auto-triggered)

> **Definition**: When trigger conditions are met → **auto-reference**, notifying the user of the reference + brief explanation of the reason and key analytical dimensions. No user opt-in/opt-out needed.

### 1. First Principles

| Item | Description |
|------|-------------|
| **Load Files** | `first_principles.md` |
| **Applied Stage** | Stage 5: Insight Synthesis |
| **Core Function** | Return to fundamentals, strip away assumptions and conventions, break through "everyone does it this way" thinking |
| **Trigger Scenarios** | Scenario 3 (Product Analysis), Scenario 4 (Business Model), Scenario 5 (Opportunity Discovery), Scenario 7 (Investment Decision) |
| **Trigger Logic** | Auto-referenced when involving innovation opportunity identification, business model essence analysis, or value innovation space exploration |
| **Notification Template** | `🧠 Auto-referencing methodology: First Principles — This research involves [innovation opportunity/model essence] analysis, requiring fundamental thinking. Key dimensions: Strip industry conventions → Identify root assumptions → Reconstruct value logic` |

### 2. ACH (Analysis of Competing Hypotheses)

| Item | Description |
|------|-------------|
| **Load Files** | `ach.md` |
| **Applied Stage** | Stage 3: Hypothesis Formation + Stage 5: Insight Validation |
| **Core Function** | Systematically compare multiple competing hypotheses, overcoming confirmation bias |
| **Trigger Scenarios** | Scenario 5 (Opportunity Discovery), Scenario 6 (Market Entry), Scenario 7 (Investment Decision) |
| **Trigger Logic** | Auto-referenced when multiple plausible directions/options need comparative evaluation |
| **Notification Template** | `🧠 Auto-referencing methodology: ACH — This research involves [multi-option comparison/key decision], requiring systematic hypothesis comparison to avoid bias. Key dimensions: List competing hypotheses → Evaluate evidence against each → Identify most likely hypothesis` |

### 3. Pre-mortem

| Item | Description |
|------|-------------|
| **Load Files** | `pre_mortem.md` |
| **Applied Stage** | Stage 5: After Insight Synthesis |
| **Core Function** | Assume the recommendation has already failed, reverse-identify critical risk factors |
| **Trigger Scenarios** | Scenario 2 (Competitive Analysis), Scenario 6 (Market Entry), Scenario 7 (Investment Decision), Scenario 8 (Strategic Planning), Scenario 9 (Due Diligence) |
| **Trigger Logic** | Auto-referenced when core strategic recommendations/action plans are produced |
| **Notification Template** | `🧠 Auto-referencing methodology: Pre-mortem — This research produced [core recommendations/action plans], requiring reverse risk validation. Key dimensions: Assume failure → Identify failure causes → Develop preventive measures` |

---

## Interview Method — Independent Process

> **Important**: The interview method is NOT in the Tier 1/Tier 2 mapping system — it follows the Stage 3.5 interview workflow trigger.

| Item | Description |
|------|-------------|
| **Load Files** | `interview.md` |
| **Trigger Mechanism** | Stage 3 Step 3.4 assesses interview necessity → User confirms interview needed → Stage 3.5 activated → Load file |
| **Reason Not Mapped** | Interviews are an information acquisition method with an independent workflow (outline design → user execution → Track C integration), not an analytical methodology |

---

## Dual-Scenario Methodology Rules

> When `frameworks/_index.md` identifies a dual-scenario match (purpose scenario + method scenario), Tier 2 methodologies take the **union of both scenarios**.
>
> Example: Scenario 5 (Opportunity Discovery) + Scenario 2 (Competitive Analysis) → Tier 2 = First Principles + ACH + Pre-mortem

---

## Scenario x Methodology Overview

| Scenario | Tier 1 (Always Active) | Tier 2 (Auto-triggered) |
|----------|----------------------|------------------------|
| 1. Industry Research | MECE+Issue Tree, Hypothesis-driven, Triangulation, Pyramid Principle | — |
| 2. Competitive Analysis | MECE+Issue Tree, Hypothesis-driven, Triangulation, Pyramid Principle | **Pre-mortem** |
| 3. Product Analysis | MECE+Issue Tree, Hypothesis-driven, Triangulation, Pyramid Principle | **First Principles** |
| 4. Business Model | MECE+Issue Tree, Hypothesis-driven, Triangulation, Pyramid Principle | **First Principles** |
| 5. Opportunity Discovery | MECE+Issue Tree, Hypothesis-driven, Triangulation, Pyramid Principle | **First Principles** + **ACH** |
| 6. Market Entry | MECE+Issue Tree, Hypothesis-driven, Triangulation, Pyramid Principle | **ACH** + **Pre-mortem** |
| 7. Investment Decision | MECE+Issue Tree, Hypothesis-driven, Triangulation, Pyramid Principle | **First Principles** + **ACH** + **Pre-mortem** |
| 8. Strategic Planning | MECE+Issue Tree, Hypothesis-driven, Triangulation, Pyramid Principle | **Pre-mortem** |
| 9. Due Diligence | MECE+Issue Tree, Hypothesis-driven, Triangulation, Pyramid Principle | **Pre-mortem** |
| 10. Ad-hoc Topics | MECE+Issue Tree, Hypothesis-driven, Triangulation, Pyramid Principle | Dynamically matched to topic |

---

## Stage x Methodology Loading Sequence

```
Stage 2: Issue Intake
    📚 Auto-load: mece.md + issue_tree.md
    🔧 Apply: Structurally decompose the problem, form Issue Tree

Stage 3: Hypotheses & Plan
    📚 Auto-load: hypothesis_driven.md
    📚 Conditional load: ach.md (auto-triggered for Scenarios 5/6/7)
    🔧 Apply: Form falsifiable Hypothesis List

Stage 3.5: Interview (Optional)
    📚 Conditional load: interview.md (when user chooses to conduct interviews)
    🔧 Apply: Design interview outline, link to hypotheses

Stage 4: Research Execution
    📚 Auto-load: triangulation.md (continues if already loaded in Stage 3)
    🔧 Apply: Multi-source data cross-validation

Stage 5: Insight Synthesis
    📚 Auto-load: triangulation.md (continues validation)
    📚 Conditional load: first_principles.md (auto-triggered for Scenarios 3/4/5/7)
    📚 Conditional load: pre_mortem.md (auto-triggered for Scenarios 2/6/7/8/9)
    📚 Conditional continue: ach.md (Scenarios 5/6/7, continues Stage 3 hypothesis validation)
    🔧 Apply: Generate insights → First Principles deep dive → Pre-mortem risk validation

Stage 6: Report Generation
    📚 Auto-load: pyramid_principle.md
    🔧 Apply: Conclusion-first, logically progressive
```

---

## Embedded Methodology Elements

The following methodology elements are **not standalone files** but are embedded within related files:

| Element | Embedded In | Description |
|---------|-------------|-------------|
| Falsification thinking | `hypothesis_driven.md` | Actively seek counterexamples |
| Bayesian thinking | `hypothesis_driven.md` | Probabilistic judgment, dynamic updating |
| 5 Whys analysis | `research_engine.md` | Technique for root cause investigation |

---

## Quality Checklist

### After Stage 2 Completion
- [ ] Was MECE used to check problem decomposition completeness?
- [ ] Was an Issue Tree formed?
- [ ] Are sub-questions decomposed to an analyzable level?

### After Stage 3 Completion
- [ ] Was a hypothesis-driven research plan formed?
- [ ] Are hypotheses falsifiable?
- [ ] (Scenarios 5/6/7) Was ACH auto-referenced?

### After Stage 4-5 Completion
- [ ] Were core data points triangulated?
- [ ] Was data verification level marked?
- [ ] (Scenarios 3/4/5/7) Was First Principles auto-referenced?
- [ ] (Scenarios 2/6/7/8/9) Was Pre-mortem auto-referenced?

### After Stage 6 Completion
- [ ] Does the report follow the Pyramid Principle?
- [ ] Is the conclusion first, with layered arguments?
