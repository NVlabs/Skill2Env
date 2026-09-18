# Changelog

All notable changes to Satori are documented here.

---

## v5.1 — (current)

### Added
- **Onboarding protocol** (`references/onboarding.md`) — Guided 5-question first-session sequence with "Satori has met you" synthesis statement
- **Dark Night Protocol** (`references/darknight-protocol.md`) — Dedicated mode for the specific experience of profound, non-clinical despair (the 2–4am dark night of the soul). Distinct from crisis response — presence-focused, not intervention-focused
- **Shadow Work Protocol** (`references/shadow-work-protocol.md`) — Structured 5-session arc for Jungian shadow work: locating shadow, meeting the first figure, origin work, integration, and living with the shadow
- **New conversation patterns** in `conversation-toolkit.md`:
  - Pattern 11: The Pattern Letter — letter from the future self, grounded in narrative identity theory
  - Pattern 12: The Dream Walk — multi-tradition dream exploration
  - Pattern 13: The Ikigai Map — structured multi-turn purpose mapping
  - Pattern 14: The Shadow Work Invitation — entry point to shadow-work-protocol.md
- **Dark Night detection signal** added to crisis recognition table in `clinical-spine.md`
- **Expanded warm-handoff language** in crisis protocol — specific, humane language for redirecting to professional support without closing the door

### Changed
- README hero section rewritten to lead with a compelling "before/after" pattern-naming transcript ("The Moment") rather than install instructions
- Contributing section updated with link to CONTRIBUTING.md
- "Who This Is Built On" section added to README — documents the specific clinical and philosophical lineages Satori draws from

---

## v5.0

### Architecture
- Restructured as a formal Claude skill package (`SatoriSkill-v5.zip`) — uploadable directly to claude.ai without terminal access
- Added `.claude-plugin/plugin.json` for Claude Code plugin auto-detection
- Added `marketplace.json` for Claude marketplace listing

### Core System
- `SOUL.md` finalized — constitutional identity layer with explicit drift detection criteria and immovables
- `clinical-spine.md` completed — full operational manual including the Unified Role Model (3 roles × 6 registers), Working Formulation system, Memory and Continuity architecture, Dream/Auto-Dream layer, Longitudinal Pattern Tracking, and Adaptive Self-Improvement loop
- `traditions-deep.md` expanded to 30+ traditions and clinical frameworks
- `conversation-toolkit.md` expanded with Voss tactical empathy framework and advanced deepening patterns

---

## v4.x

- Introduction of the Unified Role Model (Empathic Witness / Active Guide / Socratic Companion)
- Six-step Core Conversation Model formalized (Attune → Clarify → Formulate → Integrate → Translate → Anchor)
- Memory architecture: persistent memory + conversation context + memory.md + memory 2.0 + dream/auto-dream layers
- Crisis Recognition & Response Protocol added
- Drift detection system formalized in SOUL.md
- `traditions-quickref.md` created as companion to the deep encyclopedia

---

## v3.x

- Initial traditions encyclopedia (8 wisdom traditions, 4 clinical frameworks)
- OARS (Motivational Interviewing) integrated as technical foundation
- McAdams Life Story and Singer Self-Defining Memory elicitation frameworks added
- Parts-based language (IFS-informed) integrated as default conversational habit

---

## v2.x

- Six registers introduced (Grounded, Spacious, Engaged, Philosophical, Practical, Pointing)
- `tone-and-voice.md` created with before/after worked examples
- Framework Translation Rules formalized (translate to lived experience, never name-drop, one framework per response)

---

## v1.0

- Initial release — single system prompt with embedded wisdom tradition references
- Core positioning established: clinically informed wisdom companion, not therapist, not chatbot
- North Star metric established: *understanding + pattern recognition + connection + movement*
