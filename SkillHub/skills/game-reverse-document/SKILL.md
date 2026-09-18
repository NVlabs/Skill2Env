---
name: "game-reverse-document"
description: >
  Generate documentation from existing code or prototypes. Triggers on: "document this",
  "reverse document", "generate docs from code", "onboard to codebase", "document existing
  system". Do NOT invoke for writing new design docs from scratch (use game-brainstorm or
  game-design-review). Part of the AlterLab GameForge collection.
argument-hint: "[path to code or 'project' for full scan]"
effort: medium
context: fork
allowed-tools: Read, Glob, Grep, Write, AskUserQuestion
version: 1.3.0
---

# AlterLab GameForge -- Reverse Documentation Workflow

Most game projects start with passion, not paperwork. A developer prototypes, iterates, and builds. Weeks later, the codebase works but nobody -- including the original author -- can explain its architecture without reading every file. There is no design document because the design emerged from code. There is no architecture decision record because decisions were made in the moment and never written down. This is the normal state of indie development, and pretending otherwise is dishonest.

This workflow reverses the traditional documentation flow. Instead of document-then-build, it reads existing code and produces the documentation that should have existed from the start. The output is not auto-generated API docs -- it is human-readable design documentation that captures intent, architecture, and game systems in the language of game development, not the language of code.

Reverse documentation serves three critical needs: onboarding (a new team member understands the project in hours, not weeks of code archaeology), preservation (the original developer's decisions are captured before they forget why), and diagnosis (inconsistencies between systems become visible when documented side by side).

### Purpose & Triggers

Use this workflow when:
- A prototype works but has zero documentation
- A new team member needs to understand an existing codebase
- The original developer is leaving and knowledge must be transferred
- The project has grown complex enough that the author loses track of systems
- Someone says "document this" or "what does this code do?"
- A game jam prototype is being promoted to a full project and needs formal docs
- An existing project needs a design document for publishers, investors, or team alignment

Problems this solves:
- Working code that nobody can explain or safely modify
- Onboarding that takes weeks of code-reading instead of hours of doc-reading
- Architectural decisions that are invisible -- embedded in code but never recorded
- Game mechanics that exist in code but are not described in any design document
- Systems that contradict each other because nobody mapped their interactions
- Orphaned code that does nothing but nobody is confident enough to delete

### Critical Rules

1. **Read before writing.** Do not generate documentation from assumptions. Scan the actual
   codebase first. Every claim in the output must trace back to a specific file or code
   pattern. Include file paths and line references.

2. **Intent over implementation.** Capture WHY the code does something, not just WHAT it does. A function that applies gravity is not "applies downward force" -- it is "enforces the movement constraint that prevents infinite jumping." Celeste's codebase is full of intent-documenting comments like "coyote time: player can still jump for 6 frames after leaving a ledge." That level of intent documentation is the target.

3. **Flag uncertainty.** When the code's intent is ambiguous, say so. Mark sections with `[UNVERIFIED]` and ask the developer to clarify. Guessing intent and documenting the guess as fact is worse than leaving a gap.

4. **Systems, not files.** Organize documentation around game systems (movement, combat, inventory, UI), not around file structure. A movement system might span 5 files across 3 directories. The documentation describes the system, then lists the files. Dead Cells' internal documentation organized everything by game system -- combat, biomes, progression, enemies -- because that is how designers think about the game, not how the file tree is structured.

5. **Detect, do not ignore, inconsistencies.** If the movement code assumes tile-based movement but the collision code assumes continuous movement, that is a documentation finding, not something to paper over. Flag it. Factorio's codebase is a model of internal consistency -- every system agrees on what a "tick" means, what a "belt" can carry, and how entities interact. When your documentation reveals that two systems disagree on fundamentals, you have found the bug before it ships.

6. **Three modes, one pipeline.** The code analysis pipeline is shared across all three
   modes. The output format changes, not the analysis depth.

### Workflow

---

🧠 **PHASE 1: Project Scan**

*Goal: Understand the project structure, engine, and organization before reading code.*

```
PROJECT SCAN PROTOCOL
-------------------------------------------------
Step 1: Detect engine and framework
  Scan for:
  - project.godot, *.gd, *.tscn         --> Godot
  - *.unity, *.cs, ProjectSettings/      --> Unity
  - *.uproject, *.cpp/*.h with UE macros --> Unreal Engine
  - package.json with game libs          --> Web/JS game framework
  - Cargo.toml with game crates          --> Rust game framework
  - None of the above                    --> Custom engine or unknown

Step 2: Map directory structure
  Produce a tree of the project with annotations:
  /project-root/
    /src/ or /scripts/    -- Game logic
    /assets/ or /art/     -- Visual and audio assets
    /scenes/ or /levels/  -- Level/scene data
    /ui/                  -- User interface
    /data/ or /config/    -- Game data, settings
    /tests/               -- Test files (if any)
    /docs/                -- Existing documentation (if any)

Step 3: Measure project scale
  - Total source files: [N]
  - Total lines of code: [approximate]
  - Number of scenes/levels: [N]
  - Number of asset files: [N]
  - Estimated project complexity: [small / medium / large]

Step 4: Check for existing documentation
  - README present: [Y/N]
  - Design document present: [Y/N]
  - Inline comments density: [sparse / moderate / thorough]
  - Architecture docs present: [Y/N]
-------------------------------------------------
```

---

🎯 **PHASE 2: System Detection**

*Goal: Identify distinct game systems from code patterns.*

Game systems leave recognizable fingerprints in code regardless of engine or language. This
phase identifies which systems exist by scanning for characteristic patterns.

```
SYSTEM DETECTION HEURISTICS
-------------------------------------------------
MOVEMENT SYSTEM:
  Signals: velocity variables, position updates per frame, input axis
  reading, acceleration/deceleration curves, ground detection, gravity
  application, jump state machines, character controller references
  Common files: Player.*, CharacterController.*, Movement.*, Locomotion.*

COMBAT SYSTEM:
  Signals: damage calculation functions, health/HP variables, hit detection,
  attack state machines, weapon data structures, damage types/resistances,
  invincibility frames, knockback vectors
  Common files: Combat.*, Weapon.*, DamageSystem.*, Health.*, Attack.*

INVENTORY SYSTEM:
  Signals: item data structures, add/remove item functions, capacity limits,
  item stacking logic, equipment slots, item categories/types
  Common files: Inventory.*, Item.*, Equipment.*, ItemDatabase.*

UI SYSTEM:
  Signals: UI element references, menu state machines, HUD update functions,
  button callbacks, screen transition logic, UI animation triggers
  Common files: UIManager.*, HUD.*, Menu.*, Screen.*, Panel.*

AUDIO SYSTEM:
  Signals: sound effect triggers, music track management, volume controls,
  audio bus routing, spatial audio positioning, adaptive music states
  Common files: AudioManager.*, SoundManager.*, Music.*, SFX.*

SAVE/LOAD SYSTEM:
  Signals: serialization logic, file I/O operations, data persistence,
  save slot management, auto-save triggers, data migration
  Common files: SaveManager.*, SaveLoad.*, GameData.*, Persistence.*

AI SYSTEM:
  Signals: state machines (enemy states), pathfinding calls, behavior trees,
  decision-making logic, perception/detection systems, patrol patterns
  Common files: AI.*, Enemy.*, Behavior.*, StateMachine.*, NPC.*

PROGRESSION SYSTEM:
  Signals: XP/level calculations, unlock conditions, skill trees,
  achievement tracking, milestone checks, difficulty scaling
  Common files: Progression.*, Level.*, Unlock.*, Achievement.*, XP.*

PHYSICS/COLLISION:
  Signals: collision callbacks, physics material references, raycast
  usage, trigger zones, force application, rigid body management
  Common files: Physics.*, Collision.*, Trigger.*, WorldInteraction.*

CAMERA SYSTEM:
  Signals: camera follow logic, zoom controls, screen shake, camera
  bounds, cinematic camera paths, split-screen management
  Common files: Camera.*, CameraController.*, CameraManager.*
-------------------------------------------------
```

For each detected system, record:

```
SYSTEM INVENTORY
-------------------------------------------------
System          | Files Involved     | Complexity | Dependencies
-------------------------------------------------
[Movement]      | [file1, file2]     | [low/med/  | [depends on Physics,
[Combat]        | [file1, file2]     |  high]     |  Input, etc.]
[UI]            | [file1, file2]     |            |
...             |                    |            |
-------------------------------------------------

ORPHANED CODE (files that do not belong to any detected system):
  - [file] -- Purpose: [unclear / deprecated / utility / unknown]

MISSING SYSTEMS (expected but not found):
  - [e.g., "No save system detected -- game state is not persisted"]
  - [e.g., "No audio management -- sounds may be ad-hoc or missing"]
```

---

🚨 **PHASE 3: Mechanics Extraction**

*Goal: Identify game mechanics from code behavior, not just structure.*

A mechanic is a rule that governs interaction. Code implements mechanics, but the mechanic
itself is a design concept. This phase bridges the gap.

```
MECHANICS EXTRACTION
-------------------------------------------------
For each identified system, extract:

MECHANIC: [name, e.g., "Double Jump"]
  Implementation: [file:line -- brief code description]
  Rule: [the game design rule, e.g., "Player may jump once in the air
         after a ground jump. Air jump has 80% of ground jump force."]
  Parameters: [tunable values -- jump force, gravity, cooldown, etc.]
  Interactions: [how this mechanic connects to other mechanics]
  Design intent: [VERIFIED: developer confirmed / INFERRED: based on
                  code behavior / UNVERIFIED: unclear, needs clarification]
-------------------------------------------------
```

Look for:
- **State machines** -- Each state is likely a distinct player or enemy behavior
- **Input handlers** -- Each input binding reveals a player action
- **Collision responses** -- Each collision callback reveals an interaction rule
- **Timers and cooldowns** -- Each timer reveals a pacing or balance decision
- **Constants and config values** -- Each tunable number reveals a balance parameter

---

📋 **PHASE 4: Dependency Mapping**

*Goal: Visualize how systems interact with each other.*

```
DEPENDENCY MAP
-------------------------------------------------
[Movement] ---uses---> [Physics/Collision]
[Movement] ---reads--> [Input]
[Combat]   ---uses---> [Physics/Collision]
[Combat]   ---modifies-> [Health (in Movement entity)]
[UI]       ---reads--> [Health]
[UI]       ---reads--> [Inventory]
[Save]     ---reads--> [all systems with persistent state]
-------------------------------------------------

TIGHT COUPLINGS (potential refactoring targets):
  - [System A] directly modifies internal state of [System B]
    instead of using events/signals. Fragile if either changes.

CIRCULAR DEPENDENCIES:
  - [System A] depends on [System B] which depends on [System A].
    May cause initialization order bugs.

ISOLATED SYSTEMS:
  - [System X] has no dependencies and nothing depends on it.
    Verify: is this intentional or orphaned code?
```

---

🛠️ **MODE 1: Design Document Generation (design)**

*Output: A reverse-engineered Game Design Document.*

Reference `@templates/game-design-document.md` for the canonical GDD template.

```markdown
# Reverse-Engineered Game Design Document

## Project Overview
- **Project name:** [from project config or directory name]
- **Engine:** [detected engine and version]
- **Genre:** [inferred from mechanics -- e.g., platformer, RPG, puzzle]
- **Estimated scope:** [small/medium/large based on file count and systems]

## Core Mechanics
[For each mechanic extracted in Phase 3, described in design language]

### [Mechanic Name]
**What the player experiences:** [description from player perspective]
**How it works:** [design-level explanation, not code]
**Tunable parameters:** [list of values that affect feel/balance]
**Design intent:** [VERIFIED/INFERRED/UNVERIFIED]

## Game Systems
[For each system detected in Phase 2]

### [System Name]
**Purpose:** [what this system contributes to the player experience]
**Components:** [files and classes involved]
**Key behaviors:** [bullet list of what this system does]
**Dependencies:** [what it needs from other systems]
**Provides to others:** [what other systems consume from it]

## System Interaction Map
[Dependency map from Phase 4, in readable format]

## Identified Gaps
[Missing systems, orphaned code, inconsistencies]

## Balance Parameters
[All tunable values extracted from code, organized by system]

## Recommendations
[Suggestions for design documentation that should be written manually
 to supplement what code analysis can provide -- narrative design,
 art direction, audio design, player onboarding]
```

---

📊 **MODE 2: Architecture Decision Record (architecture)**

*Output: An Architecture Decision Record documenting code patterns and architectural choices.*

Reference `@templates/architecture-decision-record.md` for the canonical ADR template.

```markdown
# Architecture Overview: [Project Name]

## Technology Stack
- **Engine:** [name and version]
- **Language:** [primary language]
- **Key libraries/plugins:** [detected dependencies]

## Project Structure
[Annotated directory tree from Phase 1]

## Architectural Patterns Detected

### Pattern: [e.g., "Singleton Manager Pattern"]
**Where:** [files using this pattern]
**Purpose:** [why this pattern was likely chosen]
**Trade-offs:** [benefits and risks of this pattern in this context]
**ADR:** We use [pattern] for [reason]. This was likely chosen because
[inferred rationale]. Alternative approaches include [alternatives].

### Pattern: [e.g., "Component-Based Architecture"]
[Same structure]

## System Architecture
[For each system, describe its internal architecture]

### [System Name]
**Architecture:** [pattern used -- state machine, event-driven, etc.]
**Entry points:** [where execution starts for this system]
**Data flow:** [how data moves through the system]
**Extension points:** [where new behavior can be added]
**Coupling assessment:** [tight/loose, and to what]

## Cross-Cutting Concerns
- **State management:** [how game state is managed globally]
- **Event system:** [how systems communicate -- direct calls, signals, events]
- **Error handling:** [how errors are handled -- or not]
- **Configuration:** [how game parameters are stored and loaded]
- **Testing:** [test coverage, testability of architecture]

## Technical Debt Register
[Issues identified during code analysis]
| Area | Issue | Severity | Suggested Fix |
|------|-------|----------|---------------|
| [system] | [problem] | [high/med/low] | [recommendation] |

## Recommendations
[Architectural improvements, refactoring opportunities, scalability concerns]
```

---

🎭 **MODE 3: Concept Document Generation (concept)**

*Output: A game concept document extracted from a playable prototype.*

Reference `@templates/game-concept.md` for the canonical concept template.

```markdown
# Game Concept Document: [Project Name]
*Reverse-engineered from playable prototype*

## Core Concept
**One-sentence pitch:** [inferred from core mechanics and theme]
**Core verb:** [the primary action the player performs]
**Core loop:** [the repeating cycle of play identified from code]

## Player Experience
**What the player does:** [moment-to-moment gameplay from mechanics]
**What the player feels:** [inferred emotional experience]
**What makes it interesting:** [unique mechanical interactions found]

## Mechanics Summary
[Condensed from Phase 3 -- design-language descriptions only]

## Visual Style
**Art approach:** [inferred from assets -- pixel art, 3D, vector, etc.]
**Color palette:** [extracted from art assets or UI if present]
**Visual complexity:** [minimalist / moderate / detailed]

## Audio Profile
**Music:** [present/absent, style if detectable]
**SFX:** [present/absent, coverage of mechanics]
**Audio completeness:** [placeholder / partial / complete]

## Scope Assessment
**Current state:** [prototype / alpha / beta / near-complete]
**Content volume:** [levels, items, enemies, etc. counted from data]
**Estimated completion:** [what remains to be built for a shippable game]

## Strengths (from code evidence)
[What the prototype does well -- tight mechanics, clean architecture, etc.]

## Gaps (from code evidence)
[What is missing or incomplete -- no save system, no audio, no UI, etc.]

## Recommendations for Full Development
[What to prioritize if taking this prototype to a full game]
```

### Quality Checks

Every reverse documentation pass must verify:

```
QUALITY CHECKLIST
-------------------------------------------------
[ ] Every documented system traces to specific source files
[ ] Ambiguous intent is marked [UNVERIFIED], not guessed
[ ] Orphaned code is identified and listed
[ ] System dependencies are mapped, including circular dependencies
[ ] Inconsistencies between systems are flagged (not hidden)
[ ] All tunable parameters are extracted and listed
[ ] The documentation is organized by game system, not file structure
[ ] Missing expected systems are noted (no save, no audio, etc.)
[ ] The output matches the requested mode (design/architecture/concept)
[ ] File paths are absolute and accurate
[ ] The documentation is useful to someone who has never seen the code
-------------------------------------------------
```

### Cross-References

- `@templates/game-design-document.md` -- Template for design mode output
- `@templates/architecture-decision-record.md` -- Template for architecture mode output
- `@templates/game-concept.md` -- Template for concept mode output
- `@docs/coding-standards.md` -- Code conventions to check against during analysis
- `@docs/game-design-theory.md` -- Design vocabulary for describing mechanics
- `@docs/collaboration-protocol.md` -- How to share reverse-documented findings with team
- Workflow handoffs: output feeds into `game-design-review` for validation,
  `game-code-review` for architecture assessment, or `game-scope-check` for
  scope evaluation of documented systems

### Example Use Cases

1. **"I have a game jam prototype and want to turn it into a real project."**
   Run in **concept** mode. Scan the prototype, extract the core concept, identify what
   works and what is missing, produce a concept document that can guide full development.

2. **"A new developer is joining and needs to understand the codebase."**
   Run in **architecture** mode. Produce an architecture overview that maps systems,
   patterns, dependencies, and extension points. The new developer reads the doc instead
   of spelunking through every file.

3. **"We've been building for months but never wrote a design doc."**
   Run in **design** mode. Extract mechanics, systems, and parameters from code. Produce
   a GDD that captures the current state of the game's design, including gaps and
   inconsistencies that emerged from building without a document.

4. **"Document this module so I can refactor it safely."**
   Run in **architecture** mode on a specific path. Map the module's internal structure,
   dependencies, and coupling points. The resulting ADR tells you what is safe to change
   and what will break if touched.

5. **"I forgot why I built this system this way."**
   Run in **design** mode on the specific system path. Extract the mechanics and parameters
   to reconstruct the design intent. Flag anything marked [UNVERIFIED] for the developer
   to confirm or correct while the memory is still partially fresh.

Part of the AlterLab GameForge -- Indie Game Development Skills suite.
