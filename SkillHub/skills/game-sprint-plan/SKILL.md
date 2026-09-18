---
name: "game-sprint-plan"
description: >
  Invoke when the user needs to plan a development sprint, break down tasks, schedule
  game work, or organize a sprint with cross-discipline dependencies. Triggers on:
  "sprint plan", "task breakdown", "development planning", "scheduling", "sprint
  backlog". Do NOT invoke for scope evaluation (use game-scope-check) or retrospectives
  (use game-retrospective). Part of the AlterLab GameForge collection.
argument-hint: "[milestone or focus area]"
model: opus
effort: high
disable-model-invocation: true
allowed-tools: Read, Glob, Grep, Write, AskUserQuestion
version: 1.3.0
---

# AlterLab GameForge -- Sprint Planning Workflow

Game development sprints fail for different reasons than software sprints. A SaaS team struggles with unclear requirements and shifting priorities. A game team struggles with cross-discipline dependencies and the fundamental unpredictability of "fun." You can spec out an inventory system perfectly, build it to spec, and discover in playtest that it makes the game worse. Supergiant's sprint model (documented in their GDC talks) accounts for this by reserving explicit "discovery time" in every sprint -- time allocated to test whether what they built actually feels good, not just whether it works.

Sprint planning for games must build in structured discovery time, explicit scope tiers that flex without chaos, and a dependency model that respects the sequential nature of art-to-integration pipelines. This workflow produces a concrete sprint plan document a team can execute against.

### Purpose & Triggers

Use this workflow when:
- A team is about to start a new development sprint
- A solo developer wants to structure their next 1-2 weeks of work
- After a sprint retrospective, when planning the next iteration
- When a milestone is approaching and work needs to be decomposed
- The user finished `game-brainstorm` or `game-design-review` and needs to turn
  design decisions into executable tasks

Problems this solves:
- Sprints with vague goals that cannot be evaluated as done or not done
- Tasks estimated at "a few days" that actually take two weeks
- Art and code tasks planned in parallel when art must finish first
- Teams that commit to more work than their capacity allows every sprint
- Risks that were obvious in retrospect but invisible in planning
- No velocity tracking, so every sprint's estimates are guesses
- Scope creep disguised as small additions that accumulate into missed deadlines

### Critical Rules

1. **One goal per sprint.** The sprint goal is a single sentence that defines success. If the sprint achieves this goal and nothing else, it was a successful sprint. If the sprint ships everything on the task list but misses the goal, it failed. Hades' sprint goals during Early Access were experience-focused: "players feel the narrative progressing even when they die." That clarity prevents the "we did a lot of stuff but nothing feels finished" anti-pattern.

2. **Tasks max 1 day.** Any task estimated at more than 1 day must be decomposed further. Large tasks hide complexity and create false confidence in estimates. If a task seems irreducible at more than 1 day, it is either too vague or the developer does not yet understand the work well enough (which is itself a discovery task). Dead Cells' development at Motion Twin used day-sized tasks for everything -- even major features like new biomes were decomposed into dozens of single-day tasks with clear done criteria.

3. **The 20% buffer is non-negotiable.** After calculating raw capacity, subtract 20%. This
   covers meetings, code reviews, unexpected bugs, build issues, hardware problems, and the
   general friction of collaborative work. Teams that skip the buffer consistently
   overcommit and consistently underdeliver. Solo devs are not exempt; context switching,
   research tangents, and "I'll just refactor this one thing" all eat time.

4. **Dependencies are first-class concerns.** A task that is blocked by another task is not
   ready to be worked. Map dependencies explicitly, identify the critical path, and ensure
   blocking tasks are scheduled first. The most common game-dev dependency chain:
   design spec --> art/audio asset creation --> code integration --> QA verification.

5. **Scope tiers enable flexibility.** Not everything in a sprint has equal priority. Use
   Must/Should/Could/Won't tiers so the team knows what to cut first when reality intrudes.
   Cutting a Could-Have on Wednesday is healthy scope management. Cutting a Must-Have on
   Friday is a crisis.

6. **Velocity honesty over velocity aspirations.** If the team has completed an average of 30 story points in each of the last 3 sprints, planning 45 points this sprint is not ambition -- it is delusion. Use actual historical velocity, not hoped-for velocity. Larian's milestone-based development for BG3 worked because they tracked velocity obsessively and adjusted scope accordingly -- not because they crunched harder.

7. **Align with pillars.** Every sprint goal traces to a design pillar. If a sprint goal does not serve any pillar, the team is either working on infrastructure (acceptable but call it out) or drifting from the vision (flag for discussion). Supergiant's sprint goals are always framed as player experience statements, not feature lists -- "players feel the weight of their weapon choices" not "implement weapon system." Reference `docs/game-design-theory.md` for pillar methodology and `docs/collaboration-protocol.md` for cross-discipline coordination rules.

### Sprint Context (Auto-populated)

These values are injected automatically via shell preprocessing before the skill content
reaches Claude. They provide real-time project data so sprint planning starts from the
actual state of the codebase, not from memory or assumption.

- Recent commits: !`git log --oneline -20 2>/dev/null || echo "No git history"`
- Open issues: !`gh issue list --limit 10 --state open 2>/dev/null || echo "No GitHub issues accessible"`
- Last sprint: !`cat production/session-state/last-sprint.json 2>/dev/null || echo "No previous sprint data"`
- Team velocity: !`cat production/session-state/velocity.json 2>/dev/null || echo "No velocity data"`
- Active branches: !`git branch --list 2>/dev/null | head -10 || echo "No branches detected"`
- Uncommitted changes: !`git status --short 2>/dev/null | wc -l || echo "0"`
- Days since last tag: !`git log --tags --simplify-by-decoration --pretty="format:%ar" 2>/dev/null | head -1 || echo "No tags — no milestone history"`
- Current milestone files: !`ls production/milestones/ 2>/dev/null | tail -3 || echo "No milestone directory"`

Use this auto-populated data to inform sprint planning decisions. The recent commits reveal
what work was recently completed and what areas of the codebase are active. Open issues
provide the backlog candidates. Previous sprint data and velocity JSON enable data-driven
capacity planning (see Step 5 and Step 7). Active branches reveal work in progress that may
carry over into this sprint. Days since last tag indicates how long since the last formal
milestone, which helps calibrate sprint scope.

If velocity data is unavailable (first sprint), plan conservatively and use this sprint to
establish a baseline. If last sprint data is available, compare planned vs. completed to
calibrate this sprint's commitments.

### Workflow

**Step 1: Sprint Goal Definition**

A sprint goal is not a task list summary. It is the strategic purpose of the sprint,
connected to the game's design pillars and current milestone.

```
SPRINT GOAL FRAMEWORK
-------------------------------------------------
Format: "By the end of this sprint, [specific deliverable] is [specific state]
         so that [specific value to the project]."

GOOD EXAMPLES:
- "By the end of this sprint, the core combat loop is playable with 3 enemy
   types so that we can run our first combat-focused playtest."
- "By the end of this sprint, the save/load system handles all current game
   state so that playtesters can resume sessions."
- "By the end of this sprint, the tutorial sequence covers movement, combat,
   and inventory so that new players can learn without external instructions."

BAD EXAMPLES:
- "Work on combat stuff." (vague, not evaluable)
- "Fix bugs and add features." (two goals, not one)
- "Make the game better." (not falsifiable)

PILLAR ALIGNMENT:
Sprint goal: [goal statement]
Serves pillar: [which pillar this advances]
Milestone: [which milestone this contributes to]
-------------------------------------------------
```

**Step 2: Task Decomposition**

Break the sprint goal into implementable tasks. Each task must be small enough for one
person to complete in one day or less.

```
TASK DECOMPOSITION PROCESS
-------------------------------------------------
Step 2.1: List features needed to achieve the sprint goal
Step 2.2: For each feature, list the technical tasks
Step 2.3: For each technical task, break into sub-tasks until each is <= 1 day
Step 2.4: Add non-feature tasks (bug fixes, tech debt, reviews, meetings)
Step 2.5: Identify tasks that require discovery/research (estimate separately)

TASK FORMAT:
- ID: [SPRINT-001]
- Title: [clear, action-oriented name]
- Description: [what "done" looks like for this task]
- Estimate: [hours, max 8 for a full day]
- Owner: [person responsible]
- Discipline: [code / art / audio / design / QA]
- Dependencies: [list of task IDs this is blocked by]
- Scope tier: [Must / Should / Could]

ESTIMATION GUIDELINES:
- 1-2 hours: small, well-understood change (fix a known bug, add a config value)
- 3-4 hours: moderate task with clear requirements (implement a simple system)
- 5-6 hours: significant task with some unknowns (new feature with defined spec)
- 7-8 hours: full-day task at the complexity ceiling (decompose further if possible)
- > 8 hours: must be broken down into smaller tasks

DISCOVERY TASKS:
When a task involves unknown technology or untested approaches, create a
discovery task first: "Spike: determine if [approach] is feasible (max 4h)."
The spike produces information, not features. Schedule it before the
implementation task it informs.
-------------------------------------------------
```

**Step 3: Dependency Mapping**

Dependencies in game development are more complex than in most software because multiple
disciplines contribute to a single feature.

```
DEPENDENCY CHAIN ANALYSIS
-------------------------------------------------
TYPICAL GAME DEV DEPENDENCY CHAINS:

Design --> Art:
  Game designer defines enemy behavior --> Artist creates enemy sprite/model
  Level designer creates layout --> Environment artist builds the space

Art --> Code:
  Artist delivers character sprites --> Programmer integrates animations
  UI artist creates mockups --> Programmer implements interactive UI

Design --> Code:
  Designer specifies mechanic --> Programmer implements system
  Designer tunes values --> Programmer exposes tuning parameters

Code --> QA:
  Programmer completes feature --> QA verifies correct behavior
  Programmer fixes bug --> QA confirms fix and checks for regressions

Audio --> Code:
  Audio designer creates sounds --> Programmer integrates audio triggers

MAPPING FORMAT:
[SPRINT-001] Design enemy patrol pattern
  |
  v (blocks)
[SPRINT-005] Create enemy patrol animation
  |
  v (blocks)
[SPRINT-009] Implement enemy patrol AI
  |
  v (blocks)
[SPRINT-012] QA: verify enemy patrol behavior

CRITICAL PATH:
The longest dependency chain determines the minimum sprint duration for
that feature. If the critical path is longer than the sprint, the feature
cannot be completed this sprint. Either rescope or split across sprints.
-------------------------------------------------
```

**Step 4: Scope Tiering**

Assign every task to a scope tier. This is the pressure-release valve that keeps
sprints from failing when reality diverges from plans.

```
SCOPE TIER DEFINITIONS
-------------------------------------------------
MUST-HAVE (sprint goal depends on this)
- If these tasks are not done, the sprint goal is not met
- These are scheduled first and protected from cuts
- Estimated effort for Must-Haves should not exceed 60% of capacity

SHOULD-HAVE (significantly enhances the sprint goal)
- The sprint goal is technically met without these, but weakened
- These are scheduled second and cut only under real pressure
- Estimated effort: up to 25% of remaining capacity after Must-Haves

COULD-HAVE (polish, nice-to-have, opportunistic improvements)
- Scheduled last, cut first, no guilt
- These are stretch goals for productive sprints
- Estimated effort: fills remaining capacity

WON'T-HAVE (explicitly deferred)
- Tasks that were considered and deliberately rejected for this sprint
- Writing these down prevents relitigating scope decisions mid-sprint
- "We already decided not to do that this sprint" is a powerful sentence
-------------------------------------------------
```

**Step 5: Capacity Calculation**

Determine how much work the team can actually do, not how much you wish they could do.

```
CAPACITY CALCULATION
-------------------------------------------------
For each team member:
  Available days in sprint:     [total days minus PTO, holidays, sick days]
  Minus overhead (20%):         [meetings, reviews, admin, build issues]
  Effective person-days:        [available * 0.8]
  Effective person-hours:       [person-days * productive hours per day]

  Note: productive hours per day is typically 5-6, not 8.
  The remaining 2-3 hours go to email, Slack, context switching,
  and the unavoidable friction of being a human with a job.

TEAM CAPACITY:
  Total effective hours: [sum of all team members]
  Must-Have tasks:       [total hours]  ([%] of capacity)
  Should-Have tasks:     [total hours]  ([%] of capacity)
  Could-Have tasks:      [total hours]  ([%] of capacity)
  Buffer (20%):          [hours reserved]
  Remaining:             [positive or negative]

  If remaining is negative: cut Could-Haves first, then Should-Haves
  If still negative after cuts: the sprint goal itself is too ambitious.
  Rescope the goal, do not just "try harder."

SOLO DEV ADJUSTMENTS:
  Solo developers face unique overhead:
  - No parallelism (all dependency chains are sequential)
  - Every discipline switch has context-switching cost
  - No rubber-ducking available (allocate more time for debugging)
  - Apply an additional 10% buffer (30% total instead of 20%)
-------------------------------------------------
```

**Step 6: Risk Identification**

Name the top 3-5 risks for this specific sprint and define mitigations.

```
RISK ASSESSMENT
-------------------------------------------------
COMMON GAME DEV SPRINT RISKS:

Technical risks:
- "We've never built [system X] before and don't know the real complexity"
  Mitigation: Schedule a spike task early in the sprint
- "The engine update might break existing functionality"
  Mitigation: Pin the engine version for the sprint duration
- "Performance on target hardware is unknown"
  Mitigation: Schedule a profiling session mid-sprint

Content risks:
- "The art assets won't be ready when code needs them"
  Mitigation: Establish placeholder assets, code against placeholders
- "Level design iteration may require multiple art passes"
  Mitigation: Use blocking geometry first, polish in a later sprint

Scope risks:
- "Stakeholder feedback mid-sprint could change requirements"
  Mitigation: Define a change freeze date within the sprint
- "A Must-Have task is harder than estimated"
  Mitigation: Identify which Should-Have to cut if Must-Have expands

Team risks:
- "Key person might be unavailable for part of the sprint"
  Mitigation: Ensure no single-person bottlenecks on critical path
- "New team member ramp-up time is unpredictable"
  Mitigation: Pair them with a senior member, reduce their capacity estimate

RISK FORMAT:
| Risk | Probability | Impact | Mitigation | Trigger (when to act) |
|------|------------|--------|------------|----------------------|
| [description] | H/M/L | H/M/L | [plan] | [observable signal] |
-------------------------------------------------
```

**Step 7: Velocity Tracking**

Compare planned work against actual completion from previous sprints to calibrate
future estimates.

```
VELOCITY TRACKING
-------------------------------------------------
PREVIOUS SPRINT DATA:
| Sprint | Planned (pts/hrs) | Completed | Completion Rate | Notes |
|--------|-------------------|-----------|-----------------|-------|
| N-3    | [amount]          | [amount]  | [%]             | [context] |
| N-2    | [amount]          | [amount]  | [%]             | [context] |
| N-1    | [amount]          | [amount]  | [%]             | [context] |
| Avg    |                   |           | [avg %]         |       |

CALIBRATION RULES:
- If average completion rate is below 80%: you are chronically overcommitting.
  Reduce this sprint's planned work by the gap percentage.
- If average completion rate is above 95%: you are undercommitting.
  You can safely add a Should-Have or Could-Have item.
- If completion rate swings wildly (50% one sprint, 95% the next):
  your estimation process is unreliable. Focus on improving estimates
  before increasing velocity.
- First sprint (no history): plan conservatively. It is always better
  to finish early and pull in stretch goals than to miss commitments.

ESTIMATION IMPROVEMENT:
After each sprint, compare estimated hours to actual hours for each task.
Track the ratio. Over time, you will learn your personal/team estimation
bias and can pre-correct for it.
-------------------------------------------------
```

**📋 Solo Dev / Kanban Mode**

Not every project needs Scrum. For solo developers or teams of two, the overhead of sprint ceremonies (planning meetings, standups, retrospectives with yourself) often exceeds their value. Kanban provides the same workflow discipline with less process friction.

**When to use Kanban instead of Scrum:**
- Solo developer or team of 2 where sprint ceremonies would be a conversation with yourself
- Projects with unpredictable task sizes (creative work, R&D-heavy prototyping)
- Maintenance phases where work arrives continuously rather than in planned batches
- When the overhead of sprint planning consistently takes longer than the sprint itself

**Kanban Board Structure:**
```
Backlog --> In Progress (WIP limit: 2-3) --> Testing --> Done
```
The WIP (Work In Progress) limit is the critical constraint. For solo devs, a WIP limit of 2-3 prevents the "10 things started, nothing finished" anti-pattern. For a pair, WIP limit of 3-4 is appropriate. If you are tempted to increase the WIP limit, you are avoiding the discipline that makes Kanban work.

**Discipline Swimlanes:**
Organize your board with horizontal swimlanes by discipline: Code, Art, Audio, Design, Business. This makes context-switching visible. If your "In Progress" column has one card in Code, one in Art, and one in Business, you are paying three context-switching penalties simultaneously. Try to batch work by discipline when possible.

**Weekly Review Cadence:**
Instead of sprint retrospectives, hold a weekly review (even if it is just 15 minutes of self-reflection for solo devs):
- What moved to Done this week?
- What has been stuck in In Progress for more than 3 days? Why?
- Is the WIP limit being respected, or are you cheating?
- Does the Backlog still reflect actual priorities, or has it drifted?

**Tool Recommendations:**
- **HacknPlan** -- purpose-built for game development, understands discipline categories
- **Codecks** -- uses a card game metaphor, visually engaging, good for small teams
- **GitHub Projects** -- free, integrates with your repository, good for code-heavy projects
- **Notion** -- flexible, good for solo devs who want kanban + documentation in one place

**MoSCoW Enforcement Percentages**

Every sprint (or weekly kanban review) should verify that the planned work distribution follows these proportions:

| Priority | Target Percentage | Purpose |
|----------|------------------|---------|
| **Must** | 60% of capacity | Core deliverables that define sprint success |
| **Should** | 25% of capacity | High-value enhancements that strengthen the sprint goal |
| **Could** | 15% of capacity | Polish and stretch goals, cut first under pressure |
| **Won't** | 0% of capacity | Explicitly deferred -- not in this sprint, no exceptions |

If your Must-Have tasks exceed 60% of capacity, you are overcommitting on critical work and leaving no room for the unexpected. If Could-Have tasks creep above 15%, you are spending too much time on polish before the foundations are solid. Track these percentages explicitly in your sprint plan and review them during retrospectives.

**Scope-Check Integration**

When sprint velocity data suggests the team is consistently completing less than planned (completion rate below 75% for 3+ consecutive sprints), this is a scope creep signal. Before planning the next sprint:
- Run `/game-scope-check` to assess whether the overall project scope has grown beyond the original estimate
- Compare the current feature list against the original vertical slice definition
- Identify features that were added after the initial plan without corresponding scope reduction elsewhere
- Make an explicit cut/keep decision for each added feature before the next planning session

### Output Format

The workflow produces a **Sprint Plan Document**. Reference `templates/sprint-plan.md`
for the full template.

```markdown
# Sprint Plan

## Sprint Identity
- **Sprint Number:** [N]
- **Dates:** [start] to [end]
- **Duration:** [number of working days]
- **Sprint Goal:** [single sentence, pillar-aligned]
- **Milestone:** [which milestone this sprint serves]

## Team Capacity
| Team Member | Role | Available Days | Effective Hours |
|-------------|------|---------------|----------------|
| [name] | [discipline] | [days] | [hours] |
| **Total** | | | **[total hours]** |

## Task Board

### Must-Have
| ID | Task | Owner | Estimate | Dependencies | Status |
|----|------|-------|----------|-------------|--------|
| SPRINT-001 | [task] | [name] | [hours] | -- | Not Started |

### Should-Have
| ID | Task | Owner | Estimate | Dependencies | Status |
|----|------|-------|----------|-------------|--------|

### Could-Have
| ID | Task | Owner | Estimate | Dependencies | Status |
|----|------|-------|----------|-------------|--------|

### Won't-Have (Explicitly Deferred)
- [feature/task] -- deferred because [reason]

## Dependency Map
[Visual or textual representation of blocking chains]

## Capacity Summary
| Tier | Estimated Hours | % of Capacity |
|------|----------------|--------------|
| Must-Have | [hours] | [%] |
| Should-Have | [hours] | [%] |
| Could-Have | [hours] | [%] |
| Buffer (20%) | [hours] | 20% |
| **Total** | **[hours]** | **[%]** |

## Risk Register
| Risk | Prob | Impact | Mitigation | Trigger |
|------|------|--------|-----------|---------|
| [risk] | H/M/L | H/M/L | [plan] | [signal] |

## Definition of Done (Sprint Level)
- [ ] Sprint goal is achieved and demonstrable
- [ ] All Must-Have tasks are complete and verified
- [ ] No new Critical bugs introduced
- [ ] Updated tasks reflected in project tracking
- [ ] Sprint retrospective notes captured

## Definition of Done (Task Level)
- [ ] Code compiles and runs without errors
- [ ] Feature matches specification / acceptance criteria
- [ ] Tests pass (where testing infrastructure exists)
- [ ] Code reviewed by at least one other developer (teams of 2+)
- [ ] No hardcoded gameplay values (data-driven per coding standards)
- [ ] Known issues documented if task is completed with caveats
```

### Quality Criteria

A successful sprint plan meets all of these:
- The sprint goal is a single sentence that is clearly evaluable as done or not done
- Every task is estimated at 8 hours or less
- Dependencies are mapped and blocking tasks are scheduled before dependent tasks
- Must-Have tasks do not exceed 60% of effective capacity
- The 20% buffer is applied after all estimation, not before
- At least 3 risks are identified with specific mitigation plans
- The plan references previous sprint velocity data (if available)
- Scope tiers are assigned to every task, not just labeled on the categories
- The Definition of Done is specific to this sprint, not a generic template
- A solo developer or any team member can look at the plan and know exactly
  what they should work on first, second, and third

### Example Use Cases

1. **"We need to plan our next 2-week sprint."**
   Full 7-step workflow. Start by defining the sprint goal against the current
   milestone, decompose into tasks, map dependencies, calculate capacity, tier
   scope, identify risks, and produce the sprint plan document.

2. **"I'm a solo dev. Help me plan my next week."**
   Abbreviated workflow: define a focused goal, list 5-8 tasks, apply the solo
   dev buffer (30%), and identify 1-2 risks. Solo sprints should be shorter
   (1 week) to maintain focus and enable frequent course correction.

3. **"We keep missing our sprint commitments. What's wrong?"**
   Focus on Step 7 (velocity tracking). Compare planned vs. actual across the
   last 3-5 sprints. The pattern will reveal whether the problem is estimation,
   scope creep, dependency blocking, or capacity overcommitment.

4. **"We just finished brainstorming. How do we turn this concept into work?"**
   Use the concept document from `game-brainstorm` as input. The vertical slice
   plan becomes the first sprint goal. Feature tiers from the concept map directly
   to sprint scope tiers.

5. **"Our artist is only available 2 days this sprint. How do we plan around that?"**
   Capacity calculation with constrained resources. Map art dependencies explicitly,
   front-load art tasks to the artist's available days, ensure code tasks that depend
   on art are scheduled after art delivery, and prepare placeholder assets as a
   fallback mitigation.
