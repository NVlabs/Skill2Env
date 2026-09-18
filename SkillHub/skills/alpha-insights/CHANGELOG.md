# Changelog

## V4.1 (2026-05-26)

### 2026-06-02 Public Package Boundary Patch (package 4.1.4)
- **Public social-media adapter boundary**: The GitHub build no longer bundles provider-specific Xiaohongshu/RedNote collection scripts.
- **Track E public fallback**: English public runtime docs now route social-media research through public search, browser-readable links, user-provided screenshots/exports, or a separately installed private adapter.
- **GitHub runtime English overlay**: Added `i18n/en_runtime/` overlays for user-visible hook, validator, verifier, report helper, and report template output in the public GitHub build; formal releases continue to enforce the strict runtime CJK gate.
- **English validator compatibility**: Stage keyword matching is now case-insensitive, preventing `Topic` / `Tier` capitalization from being misread by Stage 1.
- **Internal package preservation**: Internal marketplace packages continue to include the private adapter scripts for configured environments.

### 2026-05-27 Installer Patch (package 4.1.2)
- **Single-version Codex install semantics**: `scripts/install_codex.py` now replaces the previous installed directory directly instead of creating `alpha-insights.backup-*` directories, preventing Codex Desktop from loading backup folders as active skills.
- **Active context pollution fix**: The Codex install root now stays unique at `~/.codex/skills/alpha-insights/`; repeated installs leave only the latest version.
- **Reinstall regression coverage**: Added a Codex installer test for repeated installs, unique install roots, and hook wrapper path updates.

### 2026-05-26 Release Refresh
- **Evidence and numeric integrity gates**: Added `resources/evidence_integrity.md` and `validators/evidence_integrity.py`, covering the Evidence Claim Ledger, primary-source requirements, source-laundering risk, key number / chart back-links, and source-grade constraints for strong recommendations.
- **Stage 3/4/5/6 gate hardening**: Stage 3 now detects due-diligence / target-screening primary-source plans; Stage 4 blocks key numbers, chart data, and recommendation-support evidence without a claim ledger; Stage 5 blocks strong recommendations backed only by weak sources; Stage 6 blocks headline/chart claims without evidence back-links.
- **Release pipeline fix**: `build.sh` now tracks code files in source-change detection, and marketplace publishing now uses CLI directory publishing instead of manual zip upload.

### 2026-05-14 Initial V4.1

### Added
- **Agent-first installation contract**: Added `INSTALL_FOR_AGENTS.md`, so users can ask their AI coding agent to install the package instead of following a long platform-specific tutorial.
- **Codex Desktop installer**: Added `scripts/install_codex.py`, which installs to `~/.codex/skills/alpha-insights/`, removes Cloud Code-only frontmatter hooks from the installed `SKILL.md`, rewrites the resume check to an absolute Codex path, and registers wrappers in `~/.codex/hooks.json`.
- **Dual-platform verifiers**: Added `scripts/verify_codex.py` and `scripts/verify_cloudcode.py`, covering Python compile, hook registration, HTML write guard, Stage 1 gate, Stage 3.5 interview gate, and progress logging smoke tests.
- **Codex hook wrappers in source**: `scripts/codex_hooks/` is now part of the product source, so Codex support no longer depends on a manually patched local install.

### Fixed
- **Stage 3.5 gate chain**: `stage_gate.py validate 3.5` now supports decimal stages, with a new `validators/stage3_5.py`.
- **Silent stage gate hook failure**: Removed the local `import json` scope trap in `stage_gate_hook.py`, preventing fail-open silence.
- **Codex PostToolUse payload compatibility**: The Codex wrapper now normalizes `toolName/toolInput`, so progress logs no longer record `tool=unknown`.
- **GitHub credential boundary**: Public GitHub builds must not ship built-in provider-specific default credentials; internal source and internal/local full packages retain the configured private adapter capability.

### Improved
- **Dual-platform README**: README and README_zh now present Codex Desktop and Claude Code compatible paths through the agent-first installer contract.
- **Release build safety**: GitHub build now checks English Markdown output for CJK residue after i18n overlay.

---

## V4.0.1 (2026-04-23)

### Fixed
- **Hook DELIVERABLE_MAP completion**: `interview_guides.md` (Stage 3.5) was missing, so deliverable writes silently skipped validation. It is now registered in `stage_gate_hook.py`.
- **Stage 7 cascade validation**: `stage7.py` was upgraded from file-existence checks to timestamp-chain cascade validation across S1-7.
- **Scenario 10 primary framework routing**: `frameworks/_index.md` now routes subtypes automatically: concept-clarification questions use a lightweight three-step Issue Tree path, while other subtypes keep Playing to Win.
- **i18n/en cleanliness**: Chinese example residue was cleaned from resources, and CJK residue was cleared from `frameworks/*.md` and `methodology/*.md`.

---

## V4.0 (2026-04-23)

> **Core Upgrade**: 4 Weak frameworks strengthened to Strong — all supplemented with deep cases + real financial data anchors + complete analysis workflow demonstrations + methodology takeaways (V3-09)

### Added

- **PESTEL NEV 2025 Deep Case** (+88 lines): 6-dimension detailed analysis (25+ data points), including cross-dimension interaction analysis and 4 actionable So What strategic implications
- **SWOT Dual-Case Deep TOWS Analysis** (+151 lines): Luckin Coffee 2025 (31,048 stores / RMB 49.3B revenue / 4.1B cups) + BYD 2025 (RMB 804B revenue / 4.6M units), each with four-quadrant data anchoring, four TOWS cross-strategies with 2-3 specific actions each, real-world validation table, and methodology takeaways
- **Industry Lifecycle Bike-Sharing Full Lifecycle Review** (+114 lines): 2015–2025 complete four-stage data panorama (firms / deployment / financing / daily orders), with transition signal review and 4 methodology takeaways
- **Cross-Industry Lifecycle Speed Comparison Table**: Bike-sharing 5 years vs. community group buying 3 years vs. US e-commerce 20+ years
- **Disruption Theory Pinduoduo Deep Case** (+107 lines): 2015–2025 low-end + new-market disruption dual paths, 5-dimension score retrospective (23/25 validation), 4-dimension incumbent failure analysis
- **Disruption Boundaries Clarified**: Added 3 "often misjudged as disruption" classic cases (iPhone / Tesla / ByteDance) + 3 "where disruption doesn't apply" scenarios (heavy regulation / strong network effects / safety-critical) + "incumbent defense strategy matrix" with 4-tier responses
- **i18n/en English Version Sync**: All 4 frameworks fully translated and aligned

### Improved

- **SWOT "Why SWOT Is Often Done Poorly"**: Added detailed comparison example (Luckin good vs. bad SWOT), 4 framework enforcement rules made explicit

### Fixed

- SWOT data consistency: Date unified to "end of 2025," Starbucks store count unified to "~7,600 (4.1x)"
- Disruption Theory factual fix: "2021 surpassed Alibaba's 882M" → "approached Alibaba's 882M, officially surpassed in 2022"
- V3-09 task marked as completed

---

## V3.6 (2026-04-21)

### Added
- **Chapter Blueprint Mechanism**: Stage 3 defines required materials for each report chapter per sub-question (referencing 13-type material menu), Stage 4 dual-objective research (hypothesis validation + blueprint material collection), Layer 3 Step 3.5 mandatory blueprint gap check with targeted supplementary search (✅/⚠️/❌ tri-state, ❌ blocks Stage 5 entry)
- **Evidence Reasoning Chain**: A-class insights must articulate "supports this conclusion because [specific logic]" for each key evidence item, with direction-reversal and tautology counter-examples
- **Hosted Discussion Mode**: Post-report interaction guide adds option 5 "walk through together" — AI states position → explains uncertainty → solicits user domain input; ⛔ Question boundary rule (only ask what user can answer, not what research should answer)
- **Evidence Source Traceability Requirement**: Each evidence item must include specific URL (web sources) or query/document ID (database sources); untraceable sources marked C-level
- **Subagent Data Spot-Check**: Main session spot-checks 2-3 key data points per Track return (outliers/high-impact/single-source), failed checks downgraded to C-level

### Improved
- **Stage 5 User Confirmation Enforces AskUserQuestion**: A-class confirmed one by one (✅ Agree / ✏️ Adjust / ❌ Disagree), B-class batch confirmed
- **Post-Report Interaction Guide Reordered**: Interview reminder moved before items 1-5 (completeness first)
- **Blueprint Item Quality Standard**: Each item must specify scope + dimensions + quantity; vague items prohibited
- **Step 3.5 ✅ Verification Standard**: Marking ✅ requires evidence to meet blueprint item's specification standard (quantity/dimensions/scope)

---

## V3.0.5 (2026-04-20)

### Added
- **Change Cascade Mechanism**: Global cascade rule (6 iteration types × cascade paths × incremental actions) — forces downstream deliverable updates when upstream changes
- **Red/Blue Team Feedback Triage**: Fatal gaps auto-supplemented (no user confirmation) / non-fatal gaps user-decided / conclusion+scoring fixed on spot / Round 2 re-run
- **Track E Search Standards**: ≥3 keyword groups × ≥10 pages = ≥300 raw posts, full-dataset quantitative + ≥15 selected qualitative
- **Track E API Degradation Chain**: 5-step degradation (retry → wait → retry → search engine → inform user), prohibits giving up after single failure

### Improved
- Change cascade promoted from Stage 7A to global Core Behavioral Rule, applicable at all Stages
- Classification anti-escape rules + S5 incremental evaluation 5-step flow + cascade escalation clause + cascade execution checklist
- judgment_rules.md Red/Blue Team output format adds "Finding Type" column

---

## V3.0.4 (2026-04-17)

### Added
- **Tier 1 Methodology Full Loading**: Stage 2 loads MECE + Issue Tree, Stage 4 loads Triangulation, Stage 6 loads Pyramid Principle (fixes declared-but-never-loaded gap)
- **Stage 5 re-reads research_definition.md**: Restores sub-question → insight traceability chain
- **Stage 6 blind spot review check**: Tier 2+ reports validated for blind spot section
- **Dashboard Stage 1 assessment**: Quality overview now includes user brief completeness check

### Fixed
- **SMART regex**: stage5.py character class `[SMART]` → requires bold markers `**S**:`
- **Stage 6 gate**: Added "chapter sections present" condition matching actual validator check
- **html_write_guard**: Outputs transparent warning on JSON parse failure instead of silent allow
- **report_helper author**: save/load no longer loses author field
- **stage4.py**: Consolidated duplicate load_state calls into single shared load
- **stage6.py data_count**: Fixed overlapping regex double-counting

### Improved
- **interview.md self-containment**: Internal knowledge-base and notification tool references generalized to "shared docs/notifications" with environment dependency fallback
- **Anti-pattern example diversity**: 10 examples across NEV, coffee, insurance, e-commerce, F&B, overseas expansion
- **Time estimates**: Tier-based with 20-30% retry buffer
- **Color consistency**: report_standards aligned with template (#1A365D + #667EEA)
- **Methodology file formatting**: 8 files `---##` newline fix, interview.md numbering dedup, ach.md trigger alignment
- **Usage record removal**: Stage 7B feature removed + build.sh A2 rule cleanup
- **Subagent Tier 1 search language**: Explicitly Chinese-only for quick scans

---

## V3.0.3 (2026-04-15)

### Added
- **Research Process Persistence**: evidence_base.md adds Research Execution Summary (cross-track contradictions/confirmations/gaps), Research Execution Plan (hypothesis-to-search mapping), Analysis Notes (4 mandatory fields), and Stage 5/6 Layered Re-read Protocol
- **Build Change Detection**: build.sh adds content-checksum-based source file change detection, supplementing mtime-only checks

### Fixed
- **IQR Detection**: Stage 2/4/6 validators now read `_state.json` IQR records instead of searching keywords in deliverable files
- **data_sources.md Loading**: Stage 3 layered loading (routing table + per-issue combinations only), Track-specific details loaded on-demand in Stage 4

### Improved
- **Anti-pattern Example Diversity**: All 10 anti-pattern examples upgraded from single "open source model" theme to diverse business scenarios (NEV, coffee, insurance, e-commerce, F&B, overseas expansion)

---

## V3.0.2 (2026-04-14)

### Added
- **S6 IQR Anti-pattern Detection**: Stage 6 Independent Quality Review adds Dimension 6 (item-by-item check against 10 anti-pattern rules)

---

## V3.0.1 (2026-04-12)

> **Methodology Index Merge + Tier 3 Report Length Enhancement**

### Methodology System (V3-03)
- `methodology_mapping.md` merged into `methodology/_index.md`, eliminating dual-source overlap
- MECE checkpoint supplemented with framework dimension coverage + explicit N/A dimension annotation
- `frameworks/_index.md` added N/A dimension criteria (weak relevance + low impact dual conditions)
- SKILL.md Tier 2 loading point fix: Stage 3 ACH + Stage 5 First Principles/Pre-mortem/ACH continuation

### Report Structure (V3-04)
- Tier 3 length increased from 15-30 pages to 20-35 pages, core chapters 4-5 chapters x 3-5 pages
- Report structure upgraded from six-section to seven-section format (added Blind Spot Review as independent chapter)
- Tier 3 sub-structure expansion enhanced: each chapter >= 1 ECharts, each dimension >= 2 paragraphs, each So What layer as independent paragraph
- Added Tier 3 page budget reference table (arithmetic validation min=20 / max=35)

---

## V3.0.0 (2026-04-10)

> **Quality Assurance System Overhaul -- From scattered checks to a risk-driven unified framework**

### Quality Assurance System
- Added unified quality framework: 7 reviewer role toolbox + risk-driven quality config table per Stage + failure handling + conflict resolution principles
- Added Stage 3 hypothesis self-check (4 criteria: falsifiable / sharp / comprehensive / verifiable)
- Gate Conditions completed: IQR BLOCK blocking (Stage 2/4/6) + interview decision logging (Stage 3)
- Red/Blue Team execution flow clarified: context passing path + hard requirements (no substantive challenge = cannot write to insights.md)
- Degradation paths for all quality tools: IQR / Dashboard / AskUserQuestion fallback when tools unavailable
- Stage 5 streamlined: redundant rule lists and depth gate sections removed (fully defined in judgment_rules.md)

---

## V2.0.12 (2026-04-05)

> **Interview State Chain Fix + Validator/Dashboard Precision Improvement**

### Interview State Recording Chain Fix
- SKILL.md Stage 3: added `state_manager.py log --type interview_activated/declined` call after interview decision
- SKILL.md Stage 4: added `state_manager.py log --type interview_checkpoint_done` call after interview follow-up checkpoint
- Root cause: state_manager handler was ready, stage4 validator was reading, Stage 6 interaction guide depended on it, but SKILL.md never instructed the model to write -> `interview_activated` was always false

### Validator Precision Fix
- `stage5.py`: insight count regex `[0-9#]` -> `[I#]?\s*\d`, covering `Insight I1` format
- `dashboard.py`: strip Markdown bold markers (`**`) before score extraction, fixing `= **19 points**` format match failure

---

## V2.0.11 (2026-04-05)

> **XHS Endpoint Fallback Fix** -- Xiaohongshu (RedNote) search restored.

### XHS Script Endpoint Fix
- `search_notes.js`: added `app/search_notes` endpoint to fallback list, fixing search returning empty results
- All 4 XHS scripts: removed time-sensitive "blocked" comments, endpoint availability changes constantly, maintaining complete fallback list for automatic adaptation
- Root cause: previous fix incorrectly judged "app endpoint blocked by anti-scraping" and removed app endpoint, when actually the web endpoint failed while app endpoint was available

---

## V2.0.10 (2026-04-04)

> **Stage 1 Clarification Question Optimization** -- Prohibited asking about research dimensions during Briefing; research dimensions are auto-generated by Stage 2 framework-driven process.

### Stage 1 Interactive Clarification Constraints
- Clarified question directions: decision purpose, target audience, specific companies/products of interest, geographic/time constraints, existing knowledge or hypotheses
- Prohibited asking "which dimensions/aspects to focus on" -- avoids overstepping Stage 2 MECE decomposition, avoids constraining user thinking
- Users can adjust dimensions when confirming research definition in Stage 2

---

## V2.0.9 (2026-04-04)

> **Hook Path Fix** -- Fixed blocking issue preventing all user Hooks from executing.

### Hook Path Fix (Blocking Bug)
- Frontmatter hooks: `${CLAUDE_SKILL_DIR}` -> `${CLAUDE_PLUGIN_ROOT}`
- Reason: `${CLAUDE_SKILL_DIR}` only performs string substitution in SKILL.md body text; frontmatter hook commands do not expand it (known Claude Code limitation + Claude Code CLI same behavior)
- `${CLAUDE_PLUGIN_ROOT}` performs both string substitution and environment variable setting in hook commands, pointing to the hook's parent skill directory
- Impact: all 4 hooks fixed (html_write_guard, context_budget_hook, stage_gate_hook, progress_logger)
- Inline `!` commands in body text retain `${CLAUDE_SKILL_DIR}` (expands correctly in that context)

---

## V2.0.8 (2026-04-04)

> **Protocol Compliance & State Machine Fix** -- 6th round of 10 quality checks, fixing Hook protocol, state machine Stage 3.5, version numbers, documentation sync.

### Hook Protocol Compliance
- `context_budget_hook.py`, `stage_gate_hook.py`: added `"decision": "allow"` field to output, complying with Claude Code Hook specification

### State Machine Stage 3.5 Support
- `state_manager.py`: STAGE_NAMES added `3.5: "Interview"`, `advance --stage` parsing changed from `int()` to `float()`, supporting complete Stage 3->3.5->4 path

### Version Number & Documentation Sync
- SKILL.md version number corrected from V2.0.6 to V2.0.8
- README_zh.md directory tree rewritten, adding V2 Harness subsystem (harness/, report_helper, validators/, hooks/)
- B-level evidence confidence label unified to medium confidence (aligned with triangulation.md authoritative definition)

### git-publish Trimming Rules First Full Execution (8 rules)
- A1-A4: API Key removal, usage record deletion, knowledge base reference cleanup, Claude Code CLI installation section removal
- B5-B8: Knowledge base MCP generalization, knowledge base search removal, knowledge base -> shared docs / notifications -> notifications, knowledge base -> knowledge base

---

## V2.0.7 (2026-04-04)

> **Ultimate Audit** -- 6 rounds, 41 checks, deep-diving into regex logic, state machine boundaries, report pipeline integration, public repository information security.

### Validator Regex Logic Fix
- stage4/stage5: cross-line matching `.*` -> `[\s\S]*?`, fixing framework conclusion detection and So What depth detection failures
- stage5: Red/Blue Team `8a`/`8b` markers added `\b` word boundary, preventing chapter number false matches

### State Machine Boundary Completion
- `resume_check.py`: DELIVERABLES added `3.5: interview_guides.md`, fixing interview stage breakpoint resume
- `compress_stage.py`: `_state.json` reading added try/except, following fail-open principle

### Report Pipeline Enhancement
- `ReportBuilder`: added `author` parameter (default "Alpha Insights Research"), replacing hardcoded value

### GitHub Trimming Rules Expansion (2 -> 8 rules)
- Added: CHANGELOG knowledge base references / README Claude Code CLI installation section / interview.md knowledge base and notifications / data_sources knowledge base / SKILL.md knowledge base search

---

## V2.0.6 (2026-04-04)

> **Six-Layer Verification Audit** -- Upgraded from scan-style review to verification-style review, 8 batches fixing 35 issues (12 HIGH / 14 MEDIUM / 9 LOW), zero regression.

### Tier Rule Unification
- All Tiers execute all 8 analysis rules + Red/Blue Team review + IQR review, analysis depth not reduced by Tier level
- ECharts chart requirements differentiated by Tier (Tier 2 >= 3 / Tier 3 >= 6)

### Gate <-> Validator 100% Alignment
- SKILL.md Gate Conditions and validator FAIL/WARN levels fully consistent
- evidence_base line count differentiated by Tier (10/20/40 lines)
- Cover/TOC/footer page missing upgraded from WARN to FAIL
- B-level evidence, interview decision, Red/Blue Team review all at FAIL-level validation

### State Machine Hardening
- `state_manager.py`: forward check (no backward jumps) + interview rejection path + IQR result tracking + Stage 3.5 Deliverable registration

### Path System Unification
- All references `workspace/{project}` -> `{ws}` (absolute paths), eliminating mixed usage ambiguity
- Python templates `{project}` -> `{project_slug}` unified
- ReportBuilder code templates use `os.path.join(ws, ...)` eliminating placeholder confusion

### Template and Definition Completion
- Stage 3/3.5/4 added output format templates (research plan, interview guide, Evidence Base structure)
- Layer 1/2/3 added operation definitions (who executes, what to do, what output)
- Vague metrics quantified: "reasonable data source combination" -> "covers >= 80% Sub-questions"

### Execution Mechanism Enhancement
- IQR Subagent invocation specification (invocation method, result handling, state recording, degradation path)
- Red Team fatal challenge added user decision authority (can accept correction or explicitly retain with annotation "user overrides Red Team fatal challenge")
- Multi-track failure decision rules (Track A failure -> block, others >= 2 failures -> pause and ask)
- Tier upgrade path detailed (1->2, 1->3, 2->3 what supplements needed)
- User partial insight acceptance handling rules
- Stage 7 Validator changed to all WARN (aligned with "no gated exit")
- Stage 2 loading checklist supplemented with `user_brief.md` context recovery
- Context budget threshold documented (70% warn / 90% block)

---

## V2.0 (2026-04-01)

> **Core Upgrade Philosophy**: Harness Engineering -- Don't over-invest in prompts, invest in the execution environment. Through script validation + state machine + Hook automation + context compression, constrain execution quality externally, turning "AI should do" into "system guarantees doing."

### New: Harness Execution Engine (`scripts/harness/`)

**State Management**
- `state_manager.py` -- Workspace initialization + `_state.json` state machine, tracking research stage, Tier, framework loading, interview status, and full-process metadata

**Six-Stage Validators** (`validators/stage1-6.py`)
- Automatic Deliverable validation per Stage, PASS/FAIL/WARN three-level determination
- Tier-aware: Tier 2+ enforces stricter FAIL-level validation for Red/Blue Team review, ECharts chart count, etc.
- Stage 5 Validator most comprehensive: score detection + Red/Blue Team review + substantive challenge + So What chain depth + Pre-mortem + SMART + user confirmation + key variables + action recommendations (13 checks total)

**Context Management (historical mechanism, deprecated in current V4)**
- `context_budget.py` -- Historical automatic budget estimator, removed from current V4
- `compress_stage.py` -- Historical automatic compression tool, removed from current V4

**Quality Dashboard**
- `dashboard.py` -- Before Stage 5->6 Stage Transition, aggregates S2-S5 four-stage quality metrics in a single view

**Session Recovery**
- `resume_check.py` -- On SKILL load, automatically scans in-progress research workspaces, prompting user to continue rather than restart

### New: Hook Automation System

SKILL.md frontmatter declares 4 Hooks, executed automatically by the platform:

| Hook | Trigger | Function |
|------|---------|----------|
| `html_write_guard.py` | PreToolUse:Write | Blocks Write tool from directly outputting HTML (must use Bash+Python) |
| `context_budget_hook.py` | PreToolUse:Read/Bash/Grep/Glob/Edit | Historical context budget alert hook, removed from current V4 |
| `stage_gate_hook.py` | PostToolUse:Write | Auto-runs gate validation after Deliverable write |
| `progress_logger.py` | PostToolUse:* | Async tool call logging (`_hook_log.jsonl`) |

Shared module: `_workspace_finder.py` -- Intelligently locates workspace directory from cwd, supporting multiple fallback strategies.

### New: Independent Quality Review (IQR)

- `resources/quality_review.md` -- Stage 2/4/6 three-stage IQR templates
- Independent Subagent review, handled as PASS/REVISE/BLOCK
- Auto-triggered for Tier 2+

### New: ReportBuilder Step-by-Step Generator

- `scripts/report_helper.py` -- `ReportBuilder` class, builds HTML reports step by step
- Auto-generates cover, table of contents, chapter headers, footer page, ECharts initialization code
- `values->data` auto-mapping, bypassing model output layer's filtering of `data` keyword
- Solves timeout/truncation issues with one-shot large HTML generation

### Improved: SKILL.md V2.0 Restructuring

**Stage Transition Protocol**
- Each Stage start enforces: Workspace path recovery + Context recovery + position broadcast
- Each Stage end outputs standardized Stage Transition block
- Full-stage Gate Conditions table (FAIL block + WARN alert)

**Stage 1**
- Added background pre-research (2-3 quick searches) + one-sentence conclusion broadcast (raw search results display prohibited)
- Three-Tier output system (Tier 1/2/3) formally incorporated into workflow, affecting all subsequent Stages

**Stage 3**
- Q->H mapping rules: each hypothesis annotated with corresponding Sub-question, Sub-questions without hypotheses noted with reasons
- Interview decision incorporated into confirmation flow (cannot be skipped)

**Stage 4**
- Framework analysis conclusions produced independently (new check item)
- Interview follow-up checkpoint (auto-triggered when Stage 3.5 activated)
- Track skip must inform user of reason

**Stage 5**
- Depth gate: So What chain >= 3 layers + Red-Team must produce >= 1 Substantive-level challenge
- Per-rule broadcast (black-box merged execution prohibited)
- User confirmation moved before Rule 7, before Red/Blue Team

**Stage 6**
- HTML must be generated via Bash+Python (hard rule, Hook auto-blocks Write .html)
- ReportBuilder step-by-step generation (1-2 chapters per step, avoiding timeout)
- Tier 2+ requires >= 3 ECharts interactive charts (FAIL-level validation)

**Stage 7B Wrap-up**
- Streamlined Wrap-up template: issue + Tier + report path + Key Findings + Star/Issue link


### Improved: Data Sources & Search

- `resources/research_engine.md` -- Track labels unified (A->G), execution order clarified
- XHS script endpoint migration (`check_topics.js`, `search_notes.js`, `get_note.js`)
- Knowledge base Track D search integration

### Improved: Insight Quality

- `resources/judgment_rules.md` -- insights.md output template standardized, score format unified to `= XX points`
- Red/Blue Team Subagent templates refined, challenge grading (Fatal/Substantive/Weak/Addressable)

### Architecture Principles

- **Graceful Degradation**: When Bash is unavailable (e.g., Openclaw environment), all Harness features fall back to V1 pure-instruction behavior, not blocking workflow
- **Fail Open**: All Hooks and validation scripts silently pass on exceptions
- **Self-contained**: External SKILL invocation prohibited, Alpha Insights must work independently

### File Manifest

```
scripts/harness/
├── state_manager.py          # State machine
├── stage_gate.py             # Validator unified entry
├── context_budget.py         # Historical: context budget analysis (removed from current V4)
├── compress_stage.py         # Historical: artifact compression (removed from current V4)
├── dashboard.py              # Quality dashboard
├── resume_check.py           # Session recovery
├── validators/
│   ├── __init__.py
│   ├── common.py             # Shared utilities + ValidationResult
│   ├── stage1.py ~ stage6.py # Six-stage Validators
└── hooks/
    ├── __init__.py
    ├── _workspace_finder.py  # Shared workspace locator
    ├── html_write_guard.py   # HTML write guard
    ├── context_budget_hook.py# Historical: context budget alert (removed from current V4)
    ├── stage_gate_hook.py    # Auto gate check
    └── progress_logger.py    # Progress logger

scripts/report_helper.py      # ReportBuilder + build_report()

resources/quality_review.md   # IQR templates (new)
```

---

## V1.0 (2026-03-26)

Initial release. Seven-stage workflow + 19 Frameworks + 9 Methodologies + 8 Judgment Rules + three Tiers + HTML report. See [GitHub Release](https://github.com/Ericyoung-183/alpha-insights).
