---
name: "game-postmortem"
description: >
  Run a structured post-mortem analyzing what went well, what went wrong, and extractable
  lessons. Pulls git history, milestone data, and retrospective notes automatically.
  Triggers on: "post-mortem", "project review", "what did we learn", "lessons learned",
  or when a major milestone or project is complete. Do NOT invoke for sprint-level
  retrospectives (use game-retrospective) or design reviews (use game-design-review).
  Part of the AlterLab GameForge collection.
argument-hint: "[milestone-name or 'project']"
effort: medium
allowed-tools: Read, Glob, Grep, Edit, Write, Bash
version: 1.3.0
---

# AlterLab GameForge -- Post-Mortem Analysis Workflow

Every shipped game has a story behind it that is more valuable than the game itself. The
post-mortem is where that story gets extracted, structured, and turned into reusable
knowledge. Without a post-mortem, the team repeats the same mistakes on the next project --
not because they are incompetent, but because memory is selective and unstructured reflection
gravitates toward narratives rather than patterns.

The GDC Vault is filled with post-mortems from studios that learned this the hard way.
Supergiant documented every Hades development cycle with structured retrospectives, and that
institutional knowledge directly informed the Hades II production pipeline. Obsidian's
post-mortem on Fallout: New Vegas identified the "18-month death march" anti-pattern that
they deliberately avoided in The Outer Worlds' production. ConcernedApe's Stardew Valley
post-mortem revealed that the solo dev's biggest risk was not technical -- it was the absence
of external feedback loops for 3.5 years.

A good post-mortem is not a blame session. It is not a victory lap. It is a structured data
extraction process that produces actionable knowledge for the next project, the next sprint,
or the next team.

### Purpose and Triggers

Use this workflow when:
- A project ships and the team wants to capture what they learned
- A major milestone completes (vertical slice, alpha, beta, launch)
- A sprint cycle ends and the team wants deeper analysis than a retrospective provides
- A project is cancelled and the team needs to extract salvageable lessons
- A new team member asks "what went wrong last time?"

Problems this solves:
- Repeating the same production mistakes across projects
- Survivorship bias where only successes get remembered
- Blame-oriented culture where failures are hidden rather than analyzed
- Lost institutional knowledge when team members leave
- Vague "lessons learned" lists that are too abstract to act on

### Relationship to game-retrospective

The `game-retrospective` skill handles sprint-level and milestone-level reflections --
shorter, more focused, with immediate actionable outputs for the next sprint. The
post-mortem is broader and deeper: it analyzes the entire project or a major phase,
looking for systemic patterns rather than sprint-specific issues.

Use `game-retrospective` for: "What should we do differently next sprint?"
Use `game-postmortem` for: "What should we do differently next project?"

If retrospective data exists from previous sprints, the post-mortem ingests it as input data
for pattern analysis (see Phase 3).

### Project Data (Auto-populated)

These values are injected automatically via shell preprocessing. They provide quantitative
project data that grounds the post-mortem in facts rather than feelings.

- Total commits: !`git rev-list --count HEAD 2>/dev/null || echo "No git history"`
- Project duration: !`echo "First commit: $(git log --reverse --format='%ai' 2>/dev/null | head -1 || echo 'unknown') / Latest commit: $(git log -1 --format='%ai' 2>/dev/null || echo 'unknown')"`
- Commit frequency (last 12 weeks): !`git log --since="12 weeks ago" --format="%aW" 2>/dev/null | sort | uniq -c | sort -rn | head -12 || echo "No recent history"`
- Contributors: !`git shortlog -sn --no-merges 2>/dev/null || echo "No contributor data"`
- File churn (most changed files): !`git log --pretty=format: --name-only 2>/dev/null | sort | uniq -c | sort -rn | head -15 || echo "No file history"`
- Tag/milestone history: !`git tag -l --sort=-creatordate --format='%(refname:short) %(creatordate:short)' 2>/dev/null | head -10 || echo "No tags"`
- Open issues: !`gh issue list --limit 20 --state open 2>/dev/null || echo "No GitHub issues accessible"`
- Closed issues: !`gh issue list --limit 20 --state closed 2>/dev/null || echo "No GitHub issues accessible"`
- Retrospective notes: !`ls production/sprints/*retro* production/sprints/*retrospective* 2>/dev/null || echo "No retrospective files found"`
- Sprint data: !`ls production/session-state/last-sprint.json production/session-state/velocity.json 2>/dev/null || echo "No sprint state data"`

### Critical Rules

1. **No blame, only patterns.** A post-mortem that names individuals as the cause of
   failures is a post-mortem that will never be honest. Attribute problems to processes,
   decisions, and systemic conditions -- never to people. "The rendering pipeline had no
   code review gate" is actionable. "Dave wrote bad shaders" is toxic and useless.

2. **Data before feelings.** Start with the quantitative data (commit history, velocity
   trends, bug counts) before moving to subjective reflection. Numbers anchor the
   conversation and prevent revisionist memory. The auto-populated data above is the
   starting point, not decoration.

3. **Equal weight to successes and failures.** Teams that only analyze failures develop
   learned helplessness. Teams that only celebrate successes develop blind spots. The
   post-mortem allocates structured time to both.

4. **Concrete over abstract.** "We should communicate better" is not a lesson. "We should
   hold a 15-minute sync at the start of each sprint to align art and code priorities" is
   a lesson. Every finding must produce a specific, implementable action item.

5. **Archive the output.** The post-mortem document is stored in `production/milestones/`
   or `design/postmortems/` and referenced in future project setup. A post-mortem that
   sits in a folder and is never read again has zero value.

### Workflow

The post-mortem runs in five phases. Each phase has specific inputs, activities, and
outputs. The phases build on each other -- do not skip phases or reorder them.

---

**Phase 1: Data Collection**

Gather quantitative and qualitative data about the project or milestone period.

Quantitative data (from auto-populated fields and manual collection):
- Total development time (first commit to release/milestone)
- Commit frequency patterns (were there crunch periods? Dead zones?)
- File churn analysis (which files changed most? These are complexity hotspots)
- Bug trajectory (did bug count trend up or down over time?)
- Sprint velocity history (if available from `production/session-state/velocity.json`)
- Scope changes (features added after initial plan, features cut)

Qualitative data (collected from team or solo dev reflection):
- What was the original vision? How does the shipped product compare?
- What were the stated design pillars? Were they followed?
- What decisions felt right at the time but proved wrong later?
- What external factors affected development (market shifts, personal, tooling)?
- What was the team's morale trajectory across the project?

For solo developers, qualitative data comes from self-reflection. The developer should
review their own commit messages, TODO comments, and any personal development logs.

---

**Phase 2: Team Reflection**

Structured reflection using specific, answerable questions. These questions are designed
to extract signal from noise.

**What went well (preserve and amplify):**
1. What single decision had the most positive impact on the project?
2. What tool, process, or practice would you definitely use again?
3. What was the best collaboration moment between disciplines?
4. What feature shipped closer to the original vision than expected? Why?
5. What risk did the team identify early and mitigate successfully?

**What went wrong (understand and fix):**
1. What single decision caused the most rework or wasted time?
2. What problem was visible early but addressed too late?
3. Where did communication break down between disciplines or team members?
4. What feature drifted furthest from the original design? What caused the drift?
5. What technical debt was accumulated deliberately? Was the tradeoff worth it?

**What was surprising (learn from the unexpected):**
1. What task took dramatically longer (or shorter) than estimated? Why?
2. What player/tester feedback was most unexpected?
3. What tool or technology did not perform as expected (better or worse)?
4. What external event most affected the project timeline or scope?
5. What assumption turned out to be wrong?

For each answer, ask the follow-up: "What specific change would address this for next
time?" Vague answers get vague follow-ups until they produce concrete actions.

---

**Phase 3: Pattern Analysis**

Cross-reference the data from Phase 1 with the reflections from Phase 2 to identify
systemic patterns. Individual incidents are symptoms. Patterns are diseases.

Pattern categories to look for:

**Estimation patterns:**
- Were tasks consistently underestimated? By what factor?
- Were certain disciplines worse at estimation than others?
- Did estimation accuracy improve over the project, or stay flat?
- Compare sprint velocity data if available: was the team's estimation bias stable?

**Dependency patterns:**
- Which cross-discipline handoffs caused the most delays?
- Were there recurring bottlenecks (always waiting on art, always waiting on code review)?
- Did the team identify dependencies early or discover them mid-sprint?

**Scope patterns:**
- How much feature creep occurred? Track features added after initial scope lock.
- Were cuts made proactively (before pressure) or reactively (under pressure)?
- Did cut features stay cut, or did they creep back in?

**Quality patterns:**
- When were bugs introduced vs. when were they found? What is the lag?
- Were certain systems consistently buggier? Why? (Complexity? Unclear spec? New tech?)
- Did quality gates (code review, playtest, QA) catch issues, or did they reach players?

**Communication patterns:**
- Were decisions documented or communicated verbally?
- How often were decisions revisited or reversed?
- Did all team members have the context they needed, or were there information silos?

If retrospective notes exist from previous sprints (from the auto-populated data), read
them and look for recurring themes. A problem that appeared in three consecutive sprint
retrospectives and was never resolved is a systemic failure, not a sprint-level issue.

---

**Phase 4: Lesson Extraction**

Transform patterns into lessons. Each lesson follows a specific format:

```
LESSON FORMAT
---------------------------------------------------------------
Pattern observed: [what happened, with supporting data]
Root cause: [why it happened, traced to a process or decision]
Impact: [what it cost in time, quality, morale, or scope]
Lesson: [one sentence statement of what was learned]
Action item: [specific, implementable change for next project]
Owner: [who is responsible for implementing the change]
Verification: [how to check if the change was implemented]
---------------------------------------------------------------
```

Aim for 5-10 high-quality lessons rather than 20 shallow ones. Each lesson should be
something the team can point to in six months and say "we changed this because of the
post-mortem, and here is what happened."

Categorize lessons by domain:
- **Process lessons** (how the team works)
- **Technical lessons** (architecture, tools, engine choices)
- **Design lessons** (mechanics, content, player experience)
- **Production lessons** (scope, scheduling, resource allocation)
- **Communication lessons** (handoffs, documentation, decision-making)

---

**Phase 5: Action Items and Archival**

Convert lessons into a concrete action plan and archive the post-mortem.

Action item format:
```
ACTION ITEM
---------------------------------------------------------------
ID: PM-[project]-[number]
Lesson: [reference to lesson from Phase 4]
Action: [specific change to implement]
Owner: [responsible person or role]
Deadline: [when this should be in place — ideally before next project]
Status: [ ] Not started / [ ] In progress / [ ] Complete
Verification: [how to confirm it was done]
---------------------------------------------------------------
```

Archival:
- Store the completed post-mortem in `production/milestones/postmortem-[name].md`
- Reference `@templates/post-mortem.md` for the output template
- Add a summary entry to the project's README or design doc index
- If lessons affect shared processes, update `@docs/collaboration-protocol.md` or
  `@docs/coordination-rules.md` accordingly

### Output Format

The workflow produces a **Post-Mortem Report** structured as follows. Reference
`@templates/post-mortem.md` for the full template.

```markdown
# Post-Mortem Report: [Project/Milestone Name]

**Date:** [date]
**Period covered:** [start date] to [end date]
**Team size:** [number]
**Project duration:** [weeks/months]
**Scope:** [project | milestone: name]

## Executive Summary
[3-5 sentences: what was built, whether it met its goals, and the top 3 lessons]

## Quantitative Overview
| Metric | Planned | Actual | Delta |
|--------|---------|--------|-------|
| Duration | [weeks] | [weeks] | [+/- weeks] |
| Features | [count] | [count] | [+/- count] |
| Bugs at ship | [target] | [actual] | [+/- count] |
| Sprint velocity avg | [planned] | [actual] | [+/- %] |

## What Went Well
1. [Finding with supporting evidence]
2. [Finding with supporting evidence]
3. [Finding with supporting evidence]

## What Went Wrong
1. [Finding with root cause analysis]
2. [Finding with root cause analysis]
3. [Finding with root cause analysis]

## Surprises
1. [Unexpected finding and what it revealed]
2. [Unexpected finding and what it revealed]

## Pattern Analysis
### Estimation Accuracy
[Analysis with data]

### Dependency Bottlenecks
[Analysis with data]

### Scope Management
[Analysis with data]

### Quality Trajectory
[Analysis with data]

## Lessons Learned
### Lesson 1: [Title]
- **Pattern:** [what happened]
- **Root cause:** [why]
- **Impact:** [cost]
- **Action:** [what to change]

### Lesson 2: [Title]
[repeat format]

## Action Items
| ID | Action | Owner | Deadline | Status |
|----|--------|-------|----------|--------|
| PM-001 | [action] | [owner] | [date] | Not started |

## Appendix
- Sprint retrospective summaries (if available)
- Commit frequency charts
- File churn analysis
- Bug trajectory data
```

### Quality Criteria

A successful post-mortem meets all of these:
- Quantitative data is present and supports the qualitative analysis
- At least 3 "went well" and 3 "went wrong" findings with evidence
- At least 2 systemic patterns identified (not just isolated incidents)
- Every lesson produces a specific, implementable action item with an owner
- No blame language targeting individuals
- The document is archived in a findable location
- Action items have deadlines and verification criteria
- The post-mortem is honest about what was surprising or uncomfortable

### Example Use Cases

1. **"We just shipped our game. Let's do a post-mortem."**
   Full 5-phase workflow. Ingest all available git data, sprint histories, and
   retrospective notes. Produce a comprehensive project-level post-mortem with
   lessons that inform the next project's setup.

2. **"Our alpha milestone is done. What did we learn?"**
   Milestone-scoped post-mortem. Focus the data collection on the period between
   project start and alpha. Compare the alpha deliverable against the original
   alpha goals. Extract lessons that can be applied before beta.

3. **"This project was cancelled. Was anything salvageable?"**
   Cancellation post-mortem. Extra emphasis on Phase 3 (pattern analysis) to
   understand why the project failed. The action items focus on what to change
   in the next project to avoid the same fate. Be honest but constructive.

4. **"I'm a solo dev and I just finished my first game. What should I do differently?"**
   Solo dev post-mortem. Phase 2 becomes self-reflection. Commit frequency patterns
   reveal work habits (was there crunch? burnout gaps?). Estimation accuracy across
   tasks reveals personal bias patterns. Action items are personal process changes.

5. **"We're about to start a new project. What did last project's post-mortem say?"**
   Post-mortem retrieval and application. Read the archived post-mortem, review the
   action items, check which ones were implemented, and flag any that were not.
   Feed the unaddressed lessons into the new project's `game-start` workflow.

### Agentic Protocol

- Load `@docs/collaboration-protocol.md` for interaction standards
- Load `@docs/coordination-rules.md` for escalation paths
- Reference `@templates/post-mortem.md` for the output template
- Store completed post-mortem in `production/milestones/postmortem-[name].md`
- If sprint retrospective data exists, ingest it during Phase 3
- If velocity data exists, include it in the quantitative overview
- When run after `game-retrospective`, use the retrospective output as Phase 2 input

Part of the AlterLab GameForge -- Indie Game Development Skills suite.
