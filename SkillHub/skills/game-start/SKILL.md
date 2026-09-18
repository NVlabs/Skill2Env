---
name: "game-start"
description: >
  Invoke when the user wants to start a new game project, set up project scaffolding,
  onboard into an existing codebase, or initialize GameForge session state. Triggers on:
  "start a game", "new game project", "set up project", "project onboarding", "initialize
  project". Do NOT invoke for brainstorming ideas (use game-brainstorm) or prototyping
  mechanics (use game-prototype). Part of the AlterLab GameForge collection.
argument-hint: "[engine: godot|unity|unreal]"
effort: medium
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, AskUserQuestion
version: 1.3.0
---

# AlterLab GameForge -- Project Onboarding Workflow

Every game project has a beginning, but not every beginning looks the same. You might be standing in front of an empty folder with nothing but ambition. You might have a thick design document but zero lines of code. You might be stepping into a codebase someone else started six months ago. This workflow detects where you are and gets you moving without wasting time on steps you have already completed.

The core philosophy: meet the project where it lives. Diagnose the current state, fill in the gaps, point toward the next meaningful action. Hollow Knight started as a game jam sketch. Stardew Valley started as a learning exercise. Undertale started as an EarthBound-inspired demo. None followed a textbook "correct" beginning -- but each had a moment where scattered ambition became structured execution. This workflow is that moment.

### Purpose & Triggers

Use this workflow when:
- A developer says "I want to start a new game" or "help me set up my project"
- Someone joins an existing project and needs to get oriented
- A team wants a health check on their current project structure
- A solo dev has scattered files and wants to organize into a production-ready layout
- Anyone asks "where do I even begin?" in a game development context

Problems this solves:
- Analysis paralysis at the start of a new project
- Disorganized file structures that become unmanageable at scale
- Missing documentation that causes confusion later
- Skipped foundational decisions that create technical debt from day one
- New team members spending days figuring out where things live

### Critical Rules

1. **Never overwrite existing work.** If the project already has files, structures, or docs,
   preserve them. Suggest reorganization, never deletion without explicit confirmation.

2. **Detect before prescribing.** Always scan the project state before recommending actions.
   Do not assume an empty project. Do not assume an existing one is well-organized.

3. **Engine-agnostic until confirmed.** If no engine is detected from project files, ask.
   Do not guess. The wrong engine assumption wastes enormous time.

4. **Documents are not optional.** Every project needs at minimum: a concept document, a technical architecture note, and a task tracking system. These are not bureaucracy -- they are the memory your future self will desperately need. ConcernedApe kept a running design doc throughout Stardew Valley's development, even as a solo dev. That document prevented drift across four years of work.

5. **Scope honesty from minute one.** If someone describes a 200-hour project and says they have 3 weekends, flag it immediately. Kindly, but immediately. The graveyard of abandoned indie games is filled with projects that were "almost done" for two years.

6. **Reference shared standards.** All structural decisions should align with the conventions
   documented in `docs/collaboration-protocol.md`. All design terminology should follow
   `docs/game-design-theory.md`.

### Project Detection (Auto-populated)

These values are injected automatically via shell preprocessing before the skill content
reaches Claude. They provide real-time project data so state detection starts from facts,
not assumptions.

- Engine: !`ls project.godot *.unity *.uproject 2>/dev/null | head -1 || echo "No engine project file detected"`
- Git status: !`git log --oneline -5 2>/dev/null || echo "No git history"`
- Source file count: !`find . -name "*.gd" -o -name "*.cs" -o -name "*.cpp" -o -name "*.h" -o -name "*.rs" -o -name "*.js" 2>/dev/null | wc -l`
- Existing docs: !`ls -1 docs/ 2>/dev/null || echo "No docs directory"`
- Design directory: !`ls -1 design/ 2>/dev/null || echo "No design directory"`
- Test directory: !`ls -1 tests/ 2>/dev/null || echo "No tests directory"`
- Build config: !`ls Makefile CMakeLists.txt SConstruct *.sln package.json Cargo.toml 2>/dev/null | head -3 || echo "No build config detected"`
- Project age: !`git log --reverse --format="%ar" 2>/dev/null | head -1 || echo "Unknown — no git history"`
- Active contributors: !`git shortlog -sn --no-merges 2>/dev/null | head -5 || echo "Unknown — no git history"`
- TODO/FIXME count: !`grep -r "TODO\|FIXME\|HACK\|XXX" src/ 2>/dev/null | wc -l || echo "0"`

Use this auto-populated data to shortcut Step 0 below. If the engine field shows a detected
project file, skip the engine detection prompts. If source file count is zero, you are in
State 1 (Empty Project). If source file count is nonzero but docs directory is empty, the
project likely has documentation gaps. The git history age and contributor count help
distinguish solo dev projects from team projects, which affects recommended workflow
complexity.

### Workflow

**Step 0: Project State Detection**

Before any recommendations, assess the current state by scanning for these signals.
Cross-reference against the auto-populated data above — much of this may already be answered.

```
STATE DETECTION MATRIX
---------------------------------------------------------------
Signal                          | Indicates
---------------------------------------------------------------
No files / empty directory      | State 1: Empty Project
Design docs but no source code  | State 2: Concept Exists
Source code + design docs       | State 3: In-Progress
Mature codebase + CI + tests    | State 4: Existing Project
---------------------------------------------------------------

Engine Detection Signals:
- project.godot, *.gd, *.tscn        --> Godot Engine
- *.unity, *.cs, ProjectSettings/     --> Unity
- *.uproject, *.cpp + UE macros       --> Unreal Engine
- package.json + Phaser/PixiJS        --> Web-based engine
- Cargo.toml + Bevy/macroquad         --> Rust-based engine
- No recognizable engine files        --> Ask the user
```

Run the detection, report findings, then branch to the appropriate state handler.

---

**State 1: Empty Project**

The blank canvas. This is where most solo devs and small teams start.

Step 1.1 -- Choose your engine (if not already decided):
- Present tradeoffs honestly, not engine fanboyism
- For 2D pixel art: Godot is lightweight and fast to prototype -- Cassette Beasts and Dome Keeper prove it ships commercial-quality games
- For 3D with asset store needs: Unity has the broadest ecosystem and the largest pool of learning resources
- For AAA-quality visuals: Unreal delivers but demands more hardware and expertise
- For web distribution: Phaser, PixiJS, or PlayCanvas
- The best engine is the one your team already knows. Switching engines mid-project kills more games than bad engine choices do
- Route to the appropriate engine specialist skill after selection

Step 1.2 -- Define the concept (route to `game-brainstorm` if needed):
- At minimum capture: working title, genre, platform, core mechanic, target audience
- If the user already has a concept, capture it in structured format
- If the user has no concept, route them to `game-brainstorm` before continuing

Step 1.3 -- Create the initial file structure:

The following is the recommended generic starting point. Adapt it to your engine.

```
project-root/
  design/
    gdd/                  -- Game Design Document and sub-documents
    narrative/            -- Story outlines, dialogue scripts, lore bibles
    levels/               -- Level layouts, progression maps, zone designs
    balance/              -- Economy spreadsheets, difficulty curves, tuning tables
  docs/
    architecture/         -- Technical architecture decisions and diagrams
    api/                  -- Internal API documentation for game systems
  src/
    core/                 -- Engine initialization, main loop, global managers
    gameplay/             -- Player mechanics, enemy behaviors, interaction systems
    ai/                   -- NPC behavior trees, pathfinding, decision-making
    ui/                   -- Menus, HUD, in-game UI components
    tools/                -- Editor extensions, debug tools, dev utilities
  assets/
    art/                  -- Sprites, textures, models, animations
    audio/                -- Music tracks, sound effects, ambient loops
    vfx/                  -- Particle systems, shader effects, post-processing
    shaders/              -- Custom shader files
    data/                 -- JSON/XML config files, localization strings, data tables
  tests/
    unit/                 -- Isolated component tests
    integration/          -- System interaction tests
    playtest/             -- Playtest session logs and feedback forms
  production/
    sprints/              -- Sprint plans, retrospectives, velocity charts
    milestones/           -- Milestone definitions and completion criteria
  prototypes/             -- Throwaway prototypes (never promote to production code)
```

**Engine-specific alternatives:**

- **Godot projects:** The standard Godot layout applies: `scripts/`, `scenes/`, `resources/`, `addons/`. The `design/`, `docs/`, and `production/` directories overlay on top at the project root alongside `project.godot`.
- **Unity projects:** `Assets/Scripts/`, `Assets/Prefabs/`, `Assets/Scenes/`. The `design/`, `docs/`, and `production/` directories go at the project root alongside `Assets/`.
- **Unreal projects:** `Source/`, `Content/`, `Config/`. The `design/`, `docs/`, and `production/` directories go at the project root.

This structure is a recommendation, not a requirement. GameForge hooks detect source code across multiple conventional locations (`src/`, `scripts/`, `Scripts/`, `Source/`, `Assets/Scripts/`, `lib/`). If your project already has a structure, keep it -- add the `design/`, `docs/`, and `production/` overlays where they make sense.

Step 1.4 -- Generate starter documents:
- Create a minimal Game Concept Document (reference `templates/game-concept.md`)
- Create a Technical Architecture Note with engine choice rationale
- Create a `TODO.md` with immediate next steps
- Set up a basic `.gitignore` appropriate for the chosen engine

Step 1.5 -- Suggest next steps:
- Run `game-brainstorm` to flesh out the concept if it is thin
- Define 3-5 design pillars (reference `docs/game-design-theory.md` for methodology)
- Build the first throwaway prototype to test the core mechanic
- Estimate scope and plan a first sprint with `game-sprint-plan`

---

**State 2: Concept Exists (Docs, No Code)**

The user has thought about their game but has not started building it yet.

Step 2.1 -- Review existing documentation:
- Read all design docs and assess completeness
- Check against the 8 required GDD sections (reference `docs/game-design-theory.md`)
- Identify what is well-defined and what has gaps

Step 2.2 -- Gap analysis:
- Flag missing sections: core loop definition, pillar statements, scope estimate,
  technical requirements, art style reference, audio direction, UI wireframes, progression
- Rate each gap as Critical (blocks development), Important (causes confusion later),
  or Nice-to-have (polish item)

Step 2.3 -- Structural assessment:
- Are the docs organized in the standard structure, or scattered?
- If scattered, propose reorganization into the `design/` hierarchy
- Check for contradictions between documents

Step 2.4 -- Recommend next actions:
- Fill critical gaps first (usually: core loop and technical architecture)
- Route to `game-design-review` for a thorough design document review
- Create the file structure from State 1, Step 1.3 if it does not exist
- Identify the right moment to start coding (usually: after core loop is defined and
  one pillar mechanic is well-specified)

---

**State 3: In-Progress (Code and Docs)**

Development is underway. The goal is to assess health and recommend priorities.

Step 3.1 -- Codebase scan:
- Count source files, estimate project size
- Identify the primary language and engine
- Check for test files (any testing at all?)
- Look for configuration files, build scripts, CI setup
- Scan for TODOs, FIXMEs, HACKs in the codebase and report counts

Step 3.2 -- Documentation coverage:
- Does a GDD exist? How complete is it?
- Is there technical documentation?
- Are there inline code comments on complex systems?
- Is there a README that helps a new contributor get started?

Step 3.3 -- Structural health:
- Does the file structure follow a logical organization?
- Are there any massive god-files that need decomposition?
- Is there separation between gameplay logic and engine-specific code?
- Are assets organized or dumped in flat directories?

Step 3.4 -- Priority recommendations:
- Rank findings by impact: what is most likely to cause pain next?
- Suggest specific refactoring targets if the structure is problematic
- Recommend documentation tasks that will save time in the next month
- If testing is absent, recommend starting with the most critical system

---

**State 4: Existing Project (Mature Codebase)**

A well-established project. The goal is an honest audit, not a rubber stamp.

Step 4.1 -- Architecture audit:
- Map the high-level architecture: what systems exist and how do they communicate?
- Check dependency directions: are there circular dependencies?
- Assess the state management pattern: clean state machines or boolean soup?
- Evaluate the data pipeline: are gameplay values data-driven or hardcoded?

Step 4.2 -- Documentation audit:
- Rate doc coverage from 0-100%: what percentage of systems have documentation?
- Check doc freshness: are docs up to date or describing the game from 6 months ago?
- Identify the most dangerous undocumented system (highest complexity, lowest docs)

Step 4.3 -- Technical health check:
- Test coverage assessment: what is tested, what is not?
- Performance scan: any obvious hot-path concerns?
- Dependency audit: outdated packages, security issues?
- Build health: does the project build cleanly? Any warnings being ignored?

Step 4.4 -- Recommendations:
- Produce a prioritized action list organized by effort vs. impact
- Focus on risks: what is most likely to cause a production incident?
- Suggest process improvements (CI, testing, code review practices)
- Identify technical debt that should be addressed before the next major feature

### Output Format

The workflow produces a **Project State Report** structured as follows:

```markdown
# Project State Report
**Project:** [name]
**Date:** [date]
**Detected State:** [Empty / Concept / In-Progress / Existing]
**Engine:** [detected or user-specified]

## Current State Assessment
[Summary of what was found]

## Completed Items
- [What is already in good shape]

## Gaps & Issues
| Item | Severity | Category | Recommended Action |
|------|----------|----------|-------------------|
| ...  | Critical | Docs     | ...               |

## File Structure
[Current structure vs. recommended structure, with specific changes needed]

## Recommended Next Steps
1. [Highest priority action]
2. [Second priority]
3. [Third priority]

## Suggested Workflow Sequence
- [ ] [First workflow to run, e.g., game-brainstorm]
- [ ] [Second workflow, e.g., game-design-review]
- [ ] [Third workflow, e.g., game-sprint-plan]
```

### Quality Criteria

A successful project onboarding meets all of these:
- The detected state accurately reflects reality (no false assumptions)
- Every critical gap is identified and has a concrete recommended action
- The file structure is either created or a reorganization plan is provided
- The user knows exactly what to do next -- no ambiguity
- Engine-specific guidance matches the actual engine in use
- The recommended workflow sequence is logical and actionable
- Time estimates for next steps are honest, not optimistic
- The report is specific to this project, not generic boilerplate

### Example Use Cases

1. **"I want to make my first game."**
   Detects empty project, asks about engine preference and concept, scaffolds the full
   directory structure, creates starter documents, and routes to `game-brainstorm`.

2. **"I have a GDD but haven't started coding yet. What now?"**
   Detects State 2, reviews the GDD for completeness, identifies gaps, recommends filling
   critical sections before writing code, and suggests when to start prototyping.

3. **"I inherited this project from a teammate who left. Help me understand it."**
   Detects State 4, performs a full architecture audit, maps the systems, identifies
   undocumented areas, and produces an orientation guide for the new developer.

4. **"We have a prototype but it's getting messy. Should we restructure?"**
   Detects State 3, scans the codebase for structural issues, counts TODOs and FIXMEs,
   assesses test coverage, and recommends specific refactoring priorities.

5. **"Set up a new Godot project for a 2D roguelike."**
   Detects empty project with a known engine and genre, creates the directory structure
   with Godot-specific conventions, generates a concept doc stub with roguelike-relevant
   sections, and routes to the Godot engine specialist for setup guidance.
