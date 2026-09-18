---
name: "game-scope-check"
description: >
  Evaluate project scope against timeline and resources. Triggers on: "scope creep",
  "feature list", "can we fit this in", "timeline pressure", "resource constraints",
  "cut list", "scope evaluation". Do NOT invoke for sprint planning (use game-sprint-plan)
  or general project status (use game-producer). Part of the AlterLab GameForge collection.
argument-hint: "[feature-list or milestone to evaluate]"
effort: medium
context: fork
allowed-tools: Read, Glob, Grep, Write, AskUserQuestion
version: 1.3.0
---

# AlterLab GameForge -- Scope Check Workflow

Scope creep is the number one killer of indie games. Not lack of talent, not bad ideas, not engine limitations. Games die because they grow past the team's capacity to finish them. It happens one "small" addition at a time, each individually reasonable, collectively fatal. The danger is that scope creep feels like progress -- adding a feature feels productive, cutting feels like failure. This workflow exists to invert that psychology: cutting is the skill, and a tight scope is the achievement.

Team Cherry shipped Hollow Knight with 3 people. ConcernedApe shipped Stardew Valley alone. Neither project was small in ambition -- they were ruthlessly disciplined about what to include and what to cut. The games that ship are not the ones with the longest feature lists. They are the ones where every feature earned its place through honest scope accounting.

The core principle: **a finished game with 8 great features beats an abandoned game with 20 half-built ones.** This workflow enforces that principle with concrete tools, not wishful thinking.

### Purpose & Triggers

Use this workflow when:
- The feature list has grown since the last scope check
- Someone says "can we fit this in?" or "what if we also added..."
- A milestone deadline is approaching and confidence is low
- The team feels overwhelmed but cannot articulate why
- Sprint velocity is consistently below planned capacity
- Any stakeholder (including yourself) pushes back on cutting features
- The project has never had a formal scope check

Problems this solves:
- Feature lists that only grow, never shrink
- The "just one more thing" pattern that compounds into missed deadlines
- All features labeled "Must Have" because nobody wants to prioritize
- No clear connection between features and available work hours
- Teams afraid to cut features because they lack a framework for deciding what goes
- Scope discussions that devolve into opinion battles instead of data-driven decisions

### Critical Rules

1. **One In, One Out.** Adding a feature requires cutting a feature of equivalent effort. No exceptions. No "we'll work harder." No "we'll figure it out." The budget is fixed. Moving a feature from Won't Have to Should Have means moving something from Should Have to Won't Have. Team Cherry cut entire areas from Hollow Knight to ship on time -- and the game is better for it because every surviving area is polished to a mirror shine.

2. **Percentages are law.** MoSCoW allocation must hold: Must Have occupies 60% of total
   effort, Should Have 25%, Could Have 15%. If Must Have exceeds 60%, the project is at
   risk regardless of how important each individual feature feels.

3. **Score, don't debate.** The Feature Scoring Matrix replaces opinion with arithmetic.
   Features are scored on Impact, Feasibility, and Risk. The math decides. If a team member
   disagrees, they challenge the individual scores, not the outcome.

4. **Buffer is not optional.** A schedule with less than 20% buffer is a schedule that will
   miss its deadline. Buffer absorbs the unexpected, and in game development, the unexpected
   is the expected. Treat buffer as sacred -- it is not "extra time for features."

5. **Freeze dates are real.** Feature additions freeze 3 days before any milestone. After
   the freeze, only bug fixes and polish are permitted. Breaking the freeze requires
   Producer-level sign-off and a corresponding cut elsewhere.

6. **Honest estimates only.** If you have never built a system like this before, double
   the estimate. If the tech is unfamiliar, triple it. Optimistic estimates are the
   fertilizer that scope creep grows in.

### Workflow

---

🧠 **PHASE 1: Feature Inventory**

*Goal: Catalog every feature currently planned, in progress, or requested.*

Before you can assess scope, you need a complete picture. This phase produces an exhaustive
list. Do not filter yet -- even features you suspect will be cut go on the list.

```
FEATURE INVENTORY
-------------------------------------------------
ID   | Feature             | Status        | Requestor    | Est. Hours
-------------------------------------------------
F01  | [feature name]      | [planned/     | [who asked]  | [honest
F02  | [feature name]      |  in-progress/ |              |  estimate]
F03  | [feature name]      |  complete/    |              |
...  |                     |  requested]   |              |
-------------------------------------------------

Capture rules:
- Include features already in progress (sunk cost does not protect them)
- Include features someone mentioned casually ("wouldn't it be cool if...")
- Include features assumed but never written down (save system, settings menu)
- Estimate in hours, not days. Hours force specificity.
- If you cannot estimate a feature, mark it [UNKNOWN] -- that is itself a red flag
```

Ask the user to walk through every planned feature. Probe for hidden features: "Is there
a settings menu? A save system? A tutorial? An options screen? Controller support?" These
assumed features often consume significant time but never appear on lists.

---

🎯 **PHASE 2: MoSCoW Classification**

*Goal: Sort every feature into four priority tiers with enforced percentages.*

MoSCoW is not a wishlist exercise. It is a resource allocation framework. The percentages
are constraints, not guidelines.

```
MoSCoW CLASSIFICATION
-------------------------------------------------
MUST HAVE (60% of total effort)
  The game literally does not function or ship without these.
  Test: "If this feature is missing, is the product broken?"
  - F01: [feature] -- [hours] -- Reason: [why it's essential]
  - F03: [feature] -- [hours] -- Reason: [why it's essential]
  Subtotal: [X hours] / Target: [60% of total hours]

SHOULD HAVE (25% of total effort)
  Significantly improves the game but it ships without them.
  Test: "Would a reviewer notice this is missing?"
  - F04: [feature] -- [hours] -- Reason: [why it matters]
  Subtotal: [X hours] / Target: [25% of total hours]

COULD HAVE (15% of total effort)
  Nice to have. First to be cut when time runs short.
  Test: "Would anyone outside the team notice this?"
  - F07: [feature] -- [hours] -- Reason: [what it adds]
  Subtotal: [X hours] / Target: [15% of total hours]

WON'T HAVE (0% -- explicitly deferred)
  Documented and deferred. Not forgotten, just not now.
  These protect the team from revisiting already-made decisions.
  - F09: [feature] -- Reason: [why it's deferred]
  - F10: [feature] -- Reason: [why it's deferred]
-------------------------------------------------

RED FLAGS:
- Won't Have is empty --> Every feature cannot be essential. Be honest.
- Must Have exceeds 60% --> Either the game is too ambitious or the
  classification is too generous. Demote features.
- All features are "Must Have" --> This is not prioritization. Start over.
  Force-rank the Must Haves against each other.
```

---

🚨 **PHASE 3: Feature Scoring Matrix**

*Goal: Replace subjective debate with a quantified score for each feature.*

Every feature above the Won't Have line gets scored. The formula is:
**Score = (Impact x Feasibility) / Risk**

```
FEATURE SCORING MATRIX
-------------------------------------------------
Feature    | Impact | Feasibility | Risk  | Score  | Verdict
           | (1-5)  | (1-5)       | (1-5) |        |
-------------------------------------------------
[F01]      | [  ]   | [  ]        | [  ]  | [  ]   | [Keep/Evaluate/Cut]
[F02]      | [  ]   | [  ]        | [  ]  | [  ]   | [Keep/Evaluate/Cut]
...        |        |             |       |        |
-------------------------------------------------

SCORING GUIDE:
  Impact (1-5):
    5 = Core loop depends on it. Game is broken without it.
    4 = Major enhancement to player experience.
    3 = Noticeable improvement. Reviewers would mention it.
    2 = Minor polish. Players might notice if told.
    1 = Developer-facing. Players never see it directly.

  Feasibility (1-5):
    5 = Team has built this exact thing before. Hours are certain.
    4 = Similar to past work. Minor unknowns.
    3 = New territory but understood conceptually. Moderate unknowns.
    2 = Significant unknowns. Requires research or prototyping.
    1 = Nobody on the team has done this. Major technical risk.

  Risk (1-5):
    5 = Could derail the project if it goes wrong.
    4 = Could delay the milestone significantly.
    3 = Could cause a sprint to slip.
    2 = Might need rework but recoverable.
    1 = Low consequence if it fails.

VERDICT THRESHOLDS:
  Score >= 3.0  -->  KEEP. Feature earns its place.
  Score 2.0-3.0 -->  EVALUATE. Discuss. Can risk be reduced? Can scope shrink?
  Score < 2.0   -->  CUT. Move to Won't Have. Do not negotiate.
```

---

📋 **PHASE 4: Timeline Sanity Check**

*Goal: Compare remaining work to remaining time. Calculate buffer.*

This is where optimism meets arithmetic. The numbers do not care about ambition.

```
TIMELINE SANITY CHECK
-------------------------------------------------
CAPACITY CALCULATION:
  Team members:           [N]
  Available hours/week:   [X hours per person]
  Weeks remaining:        [Y weeks to milestone]
  Gross capacity:         [N x X x Y] hours
  Overhead deduction:     [-15% for meetings, admin, context switching]
  Net capacity:           [result] hours

WORK REMAINING:
  Must Have (incomplete):  [hours]
  Should Have (planned):   [hours]
  Could Have (planned):    [hours]
  Total planned work:      [hours]

BUFFER CALCULATION:
  Available buffer:        [Net capacity - Total planned work]
  Buffer percentage:       [buffer / net capacity x 100]%

  >= 30% buffer  🟢  HEALTHY. Room for surprises. Ship with confidence.
  20-30% buffer  🟡  CAUTION. Tight but manageable if no major surprises.
  10-20% buffer  🟠  WARNING. One surprise away from missing the deadline.
  < 10% buffer   🔴  CRITICAL. The deadline will be missed. Cut scope now.
  Negative buffer 💀  OVER-COMMITTED. The math says this is impossible.
                      Cut aggressively or extend the deadline.
-------------------------------------------------

REALITY ADJUSTMENTS:
  - Solo dev? Multiply estimates by 1.5 (context-switching overhead)
  - First game? Multiply estimates by 2.0 (learning curve)
  - Part-time team? Use actual committed hours, not aspirational hours
  - Unfamiliar engine? Add 15-25% to all estimates
```

---

📊 **PHASE 5: Scope Creep Detection**

*Goal: Identify patterns that signal scope is growing uncontrolled.*

Scope creep has telltale symptoms. Check for these warning signs:

```
SCOPE CREEP DETECTION CHECKLIST
-------------------------------------------------
Signal                                          | Present?
-------------------------------------------------
Feature list has grown since last check         | [Y/N]
No items in Won't Have category                 | [Y/N]
All features are classified "Must Have"         | [Y/N]
"Just one more thing" has been said recently    | [Y/N]
Features added without equivalent cuts          | [Y/N]
Estimates trending upward on existing features  | [Y/N]
New features appearing from casual conversation | [Y/N]
Buffer percentage decreasing sprint over sprint | [Y/N]
Team morale declining despite "progress"        | [Y/N]
Milestone dates have shifted more than once     | [Y/N]
-------------------------------------------------

SEVERITY:
  0-2 signals  🟢  Healthy scope management.
  3-4 signals  🟡  Early warning. Address now before it compounds.
  5-7 signals  🟠  Active scope creep. Immediate intervention needed.
  8-10 signals 🔴  Project at risk. Full scope reset required.
```

---

🛠️ **PHASE 6: Change Freeze Protocol**

*Goal: Establish hard boundaries around milestone deadlines.*

Feature additions freeze 3 days before any milestone. This is not optional.

```
CHANGE FREEZE PROTOCOL
-------------------------------------------------
Milestone:          [name]
Milestone date:     [date]
Freeze date:        [milestone date - 3 days]

AFTER FREEZE, PERMITTED:
  - Bug fixes for existing features
  - Polish on existing features (animation, juice, audio)
  - Documentation and store page updates
  - Build and deployment pipeline work

AFTER FREEZE, PROHIBITED:
  - New features of any size
  - "Small" additions ("it'll only take an hour")
  - Scope changes to existing features
  - New art assets for unreleased features

FREEZE BREAK PROCEDURE (emergency only):
  1. Producer (or project lead) formally approves
  2. Equivalent-effort feature is cut simultaneously
  3. Decision is documented with rationale
  4. This counts as a scope creep signal in the next detection check
-------------------------------------------------
```

### Output Format

The workflow produces a **Scope Assessment Report**:

```markdown
# Scope Assessment Report

## Traffic Light Status
[🟢 HEALTHY / 🟡 CAUTION / 🟠 WARNING / 🔴 CRITICAL]

## Summary
[2-3 sentences: overall assessment, key concern, recommended action]

## Feature Inventory
[Total features: N | Scored: N | Cut: N | Deferred: N]

## MoSCoW Breakdown
| Category    | Features | Hours | % of Total | Target % | Status |
|-------------|----------|-------|------------|----------|--------|
| Must Have   | [N]      | [X]   | [Y%]       | 60%      | [OK/OVER] |
| Should Have | [N]      | [X]   | [Y%]       | 25%      | [OK/OVER] |
| Could Have  | [N]      | [X]   | [Y%]       | 15%      | [OK/OVER] |
| Won't Have  | [N]      | --    | --         | --       | [populated/empty] |

## Feature Scores
[Sorted by score descending. Features below 2.0 marked for cut.]

## Timeline Assessment
- **Net capacity:** [hours]
- **Planned work:** [hours]
- **Buffer:** [hours] ([X%])
- **Buffer status:** [🟢/🟡/🟠/🔴]

## Scope Creep Signals
[N of 10 signals detected. List active signals.]

## Change Freeze
- **Next milestone:** [name] on [date]
- **Freeze date:** [date]
- **Days until freeze:** [N]

## Recommended Actions
1. [Most urgent action]
2. [Second priority]
3. [Third priority]

## Features to Cut (Recommended)
[List with rationale for each cut]

## Features to Keep (Confirmed)
[List with score and pillar alignment for each]
```

### Quality Criteria

A successful scope check meets all of these:
- Every planned feature has an honest hour estimate
- MoSCoW percentages are within 5% of targets (60/25/15)
- Won't Have category contains at least 2 items (if it is empty, the check was not honest)
- Buffer percentage is calculated and reported with traffic light status
- No feature scored below 2.0 remains in Must Have or Should Have
- The One In, One Out rule was enforced for any additions during the session
- Scope creep signals were checked and the count is reported
- A change freeze date is established for the next milestone
- The report is actionable -- the team knows exactly what to build and what to skip
- All scope decisions trace back to scores and capacity math, not opinions

### Cross-References

- `@docs/game-design-theory.md` -- Design pillars that features should align with
- `@docs/collaboration-protocol.md` -- How to communicate scope changes across roles
- `@docs/coordination-rules.md` -- Escalation paths when scope conflicts arise
- `@templates/sprint-plan.md` -- Sprint plan template that consumes scope check output
- Workflow handoffs: receives input from `game-brainstorm` or `game-design-review`,
  feeds into `game-sprint-plan` for execution planning

### Anti-Patterns

Scope checks fail when they exhibit these patterns:

- **The Rubber Stamp:** Everything passes because nobody wants conflict. If the check does not cut at least one feature, it was not rigorous enough.
- **The Hostage Feature:** "We already started this so we can't cut it." Sunk cost is not a reason to continue. If the remaining work exceeds the feature's value, cut it. Supergiant killed the original shield mechanic in Hades mid-development and replaced it with the cast system. The shield had months of work behind it. The cast made the game better.
- **The Stealth Add:** Features sneak in without going through MoSCoW classification. Every feature, no matter how small, goes through the matrix.
- **The Infinite Must Have:** All features are "Must Have" because the team conflates "I want this" with "the game needs this." Force-rank ruthlessly.
- **The Missing Buffer:** "We don't need buffer, we'll just work harder." Buffer is not laziness insurance. It is reality insurance. ConcernedApe's multi-year Stardew Valley development timeline included massive buffer -- and he used every hour of it.

Part of the AlterLab GameForge -- Indie Game Development Skills suite.
