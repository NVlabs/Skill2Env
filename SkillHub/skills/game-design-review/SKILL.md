---
name: "game-design-review"
description: >
  Invoke when the user wants feedback on a game design document, GDD review, design
  evaluation, or consistency check on an existing design. Triggers on: "review my GDD",
  "design feedback", "evaluate design", "design document review", "GDD critique".
  Do NOT invoke for brainstorming new ideas (use game-brainstorm) or balance tuning
  (use game-balance-check). Part of the AlterLab GameForge collection.
argument-hint: "[path to design document]"
effort: medium
context: fork
allowed-tools: Read, Glob, Grep, Write, AskUserQuestion
version: 1.3.0
---

# AlterLab GameForge -- Design Document Review Workflow

A game design document is a living contract between your ambitions and your execution capacity. A bad GDD is not poorly formatted -- it is one that lets the team build confidently in the wrong direction for weeks before anyone notices. Hollow Knight's design doc worked because Team Cherry kept it tight, falsifiable, and obsessively focused on three pillars. Most GDDs fail because they describe a game without constraining it -- anything goes, so nothing works.

This is not a checklist review. A checklist confirms sections exist. This review confirms sections are good -- internally consistent, psychologically grounded, scope-honest, and specific enough to guide implementation decisions. Disco Elysium's systems-narrative integration did not happen by accident -- it happened because the design document specified exactly how every skill check connected to every dialogue branch. That level of specificity is what this review demands.

### Purpose & Triggers

Use this workflow when:
- A designer says "review my GDD" or "give feedback on my design document"
- Before starting implementation, to catch problems while they are cheap to fix
- After significant design changes, to re-validate internal consistency
- When a playtest reveals problems and you suspect the root cause is in the design
- When team members disagree about what the game is supposed to be

Problems this solves:
- Mechanics that do not serve any design pillar (orphan features)
- Target aesthetics that contradict the actual mechanics (MDA misalignment)
- Scope estimates that ignore reality (optimism masquerading as planning)
- Design documents that describe a game but do not constrain it (anything goes = nothing works)
- Systems that interact in unintended ways (emergent conflict)
- Missing sections that will cause confusion during implementation

### Critical Rules

1. **Read the whole document before commenting.** Context matters. A mechanic that seems
   orphaned in Section 3 might be justified by the progression system in Section 7. Read
   everything first, then analyze.

2. **Severity matters.** Not all findings are equal. A missing core loop definition is
   Critical. A vague art style reference is Minor. Assign severity explicitly so the
   designer knows where to spend time.

3. **Be specific, not vague.** "The combat system could be better" is useless feedback. "The combat system describes player attacks but never specifies enemy behavior patterns, making it impossible to tune difficulty" is actionable. Name the problem, cite the section, propose the fix.

4. **Propose, do not prescribe.** Offer alternative approaches with reasoning, not mandates. The designer owns the vision. Your job is to identify problems and suggest directions -- "Disco Elysium solved this by tying skill checks to dialogue, not combat" is a reference that opens thinking. "Just copy Disco Elysium" is lazy.

5. **Reference the theory.** When flagging an issue, connect it to established design
   principles from `docs/game-design-theory.md`. "This violates Flow Theory because the
   difficulty spike at Stage 3 has no skill-building ramp" is stronger than "Stage 3 is
   too hard."

6. **Check alignment across the document.** The biggest GDD failures are not missing
   sections but contradictions between sections. A pillar that says "player freedom" and
   a level design section that describes linear corridors is a critical contradiction.

### Workflow

**Step 1: Document Intake**

Read the complete design document. Note the structure, length, and overall organization.
Identify which of the 8 required GDD sections are present:

```
REQUIRED GDD SECTIONS
-------------------------------------------------
1. Game Overview (concept, genre, platform, audience)
2. Core Mechanics (player actions, systems, interactions)
3. Game Flow / Core Loop (30-sec to full-game timescales)
4. Level / World Design (spaces, progression through space)
5. Art Direction (visual style, references, asset requirements)
6. Audio Design (music, SFX, adaptive audio approach)
7. UI / UX Design (menus, HUD, accessibility considerations)
8. Technical Requirements (engine, platforms, performance targets)

OPTIONAL BUT VALUABLE
- Narrative Design (story, characters, dialogue systems)
- Monetization Model (if applicable)
- Multiplayer Design (if applicable)
- Accessibility Plan
- Competitive Analysis
-------------------------------------------------
```

**Step 2: Pillar Alignment Review**

This is the most important dimension. If the game has defined design pillars, every
mechanic and system must trace back to at least one pillar. If no pillars are defined,
flag this as a Critical finding.

```
PILLAR ALIGNMENT MATRIX
-------------------------------------------------
Mechanic/System        | Pillar 1 | Pillar 2 | Pillar 3 | Orphan?
-------------------------------------------------
[combat system]        | Yes      | --       | Yes      | No
[crafting system]      | --       | --       | --       | YES - flag
[dialogue choices]     | Yes      | Yes      | --       | No
[inventory management] | --       | --       | --       | YES - flag
-------------------------------------------------

Orphan mechanics are red flags. They either:
a) Should be cut (they serve no pillar, so they dilute focus)
b) Reveal a missing pillar (add a pillar that justifies them)
c) Are described poorly (clarify how they connect to pillars)
```

**Step 3: MDA Consistency Review**

Check whether the described mechanics actually deliver the target aesthetics. This
requires understanding the MDA Framework as documented in `docs/game-design-theory.md`.

```
MDA CONSISTENCY CHECK
-------------------------------------------------
Target Aesthetic | Required Dynamics        | Mechanics That Deliver | Gap?
-------------------------------------------------
Discovery        | Exploration, revelation  | Fog of war, hidden areas | OK
Challenge        | Skill testing, escalation| [none described]         | GAP
-------------------------------------------------

Common MDA misalignments:
- Target "Discovery" but linear level progression (no exploration mechanics)
- Target "Challenge" but no difficulty scaling or mastery curve
- Target "Expression" but no player-facing creative tools
- Target "Fellowship" but single-player-only design
```

**Step 4: Player Psychology Review**

Evaluate through the lens of Self-Determination Theory and Flow Theory.

SDT Check -- Does the design support the three basic psychological needs?

```
SDT ASSESSMENT
-------------------------------------------------
Need         | Evidence in Design       | Threats in Design     | Rating
-------------------------------------------------
Autonomy     | [choices described]      | [forced linearity]    | [A/B/C/F]
Competence   | [skill expression]       | [unfair difficulty]   | [A/B/C/F]
Relatedness  | [social features]        | [isolation by design] | [A/B/C/F]
-------------------------------------------------
```

Flow Check -- Can the player maintain a flow state?

```
FLOW ASSESSMENT
-------------------------------------------------
Flow Element  | Present? | Notes
-------------------------------------------------
Clear goals   | Y/N      | [does the player always know what to do next?]
Immediate feedback | Y/N | [does every action produce visible response?]
Challenge/skill balance | Y/N | [does difficulty scale with player growth?]
Sense of control | Y/N   | [does the player feel agency?]
Loss of self-consciousness | Y/N | [can they forget they are playing?]
Time distortion | Y/N    | [does the design support losing track of time?]
-------------------------------------------------
```

**Step 5: Internal Consistency Review**

Look for contradictions between different sections of the document.

```
CONSISTENCY CROSS-CHECK
-------------------------------------------------
Check                        | Status | Finding
-------------------------------------------------
Pillars vs. mechanics        | OK/CONFLICT | [detail]
Core loop vs. progression    | OK/CONFLICT | [detail]
Art style vs. tone          | OK/CONFLICT | [detail]
Difficulty curve vs. target audience | OK/CONFLICT | [detail]
Feature scope vs. team capacity | OK/CONFLICT | [detail]
Platform vs. control scheme  | OK/CONFLICT | [detail]
-------------------------------------------------
```

**Step 6: Scope Feasibility Review**

Can this game actually be built with the stated resources?

- Count the number of unique systems described
- Estimate content volume (levels, enemies, items, dialogue)
- Compare against team size and timeline
- Flag any system that requires technology the team has not proven they can build
- Check for "hidden complexity" -- features that sound simple but are engineering nightmares
  (pathfinding, procedural generation, multiplayer netcode, physics-based gameplay)

**Step 7: Edge Case Coverage**

What happens when players do unexpected things?

- What if the player breaks the intended sequence?
- What if the player exhausts a resource the design assumes is renewable?
- What if the player refuses to engage with a system the design treats as mandatory?
- What if two systems interact in an unintended way?
- What happens at the extremes (maximum level, zero resources, impossible speed)?

**Step 8: Onboarding Assessment**

Can a new player learn this game without external help?

- Is the tutorial approach described?
- Does the complexity ramp match the teaching sequence?
- Are advanced mechanics introduced only after basic ones are mastered?
- Is there a "just play" entry point for players who skip tutorials?
- Does the game teach through play or through text walls?

**Step 9: Competitive Differentiation**

Is the unique hook actually unique? Hollow Knight's hook was not "metroidvania" -- that genre was already crowded. Its hook was the atmosphere: melancholy insect civilization, tight combat feel, and a world that rewarded patient exploration. The differentiation was experiential, not categorical.

- Identify the 3 closest comparable games
- For each comparable, define what makes THIS game different at the experience level, not the feature level
- Check whether the differentiators are mechanical or cosmetic (cosmetic differentiation is not real differentiation -- "our zombies are blue" is not a hook)
- Assess whether the unique hook is prominent enough to communicate in a 30-second trailer

### Output Format

The workflow produces a **Design Review Report**:

```markdown
# Design Review Report
**Document:** [GDD title]
**Version:** [if specified]
**Reviewer:** GameForge Design Review
**Date:** [date]

## Executive Summary
[2-3 sentences: overall assessment, biggest strength, most critical issue]

## Section Completeness
| Section | Present | Completeness | Notes |
|---------|---------|-------------|-------|
| Game Overview | Y/N | [%] | |
| Core Mechanics | Y/N | [%] | |
| ... | | | |

## Findings

### Critical (must fix before implementation)
- **[CRIT-01]** [Title]: [Detailed finding with specific references to the document]
  **Recommendation:** [specific suggested fix]

### Major (fix soon, will cause significant problems if ignored)
- **[MAJ-01]** [Title]: [Detailed finding]
  **Recommendation:** [specific suggested fix]

### Minor (improve when convenient)
- **[MIN-01]** [Title]: [Detailed finding]
  **Recommendation:** [specific suggested fix]

### Suggestions (not problems, but opportunities)
- **[SUG-01]** [Title]: [Idea for improvement]

## Pillar Alignment Matrix
[From Step 2]

## MDA Consistency Report
[From Step 3]

## Strengths
[What the document does well -- always include positives]

## Recommended Next Actions
1. [Priority action]
2. [Second action]
3. [Third action]

## Suggested Workflows
- [ ] [e.g., game-brainstorm to develop underdeveloped areas]
- [ ] [e.g., game-balance-check for tuning concerns]
```

### Quality Criteria

A successful design review meets all of these:
- Every finding cites specific text or sections from the reviewed document
- Severity ratings are justified and proportional
- Pillar alignment is checked for every described mechanic
- At least one finding relates to player psychology (SDT or Flow)
- The review identifies strengths, not just problems
- Recommendations are specific enough to act on immediately
- The scope assessment is grounded in real-world development effort
- Internal contradictions are caught and explained clearly
- The review distinguishes between design quality and document quality
  (a brilliant design can be poorly documented and vice versa)

### Example Use Cases

1. **"Review my GDD before we start coding."**
   Full 9-step review. Emphasize Critical findings that must be resolved before
   a single line of code is written.

2. **"Our playtest went badly. Is the problem in the design?"**
   Focus on Steps 3 (MDA consistency), 4 (player psychology), and 7 (edge cases).
   The playtest feedback points toward which dimensions to scrutinize hardest.

3. **"I think our scope is too big. Can you confirm?"**
   Focus on Step 6 (scope feasibility). Count systems, estimate content volume,
   compare against team capacity, and deliver an honest verdict.

4. **"We're arguing about whether to add a crafting system. Help us decide."**
   Focus on Step 2 (pillar alignment). If crafting serves a pillar, it belongs.
   If it does not, it is scope creep wearing a feature-shaped disguise.

5. **"I wrote this GDD in one sitting. What did I miss?"**
   Full review with emphasis on Step 1 (section completeness) and Step 5 (internal
   consistency). Documents written quickly often have implicit assumptions that need
   to be made explicit and contradictions that need resolution.
