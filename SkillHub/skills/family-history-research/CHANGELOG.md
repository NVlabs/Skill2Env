# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.5] - 2025-10-21

### Changed
- **Documentation reorganization**: Moved `research-log-guidance.md` and `research-plan-guidance.md` from `assets/templates/` to `references/`
  - Clearer distinction between simplified templates and comprehensive references
  - Better information architecture for users seeking detailed methodology
  - Guidance documents now grouped with other reference materials
- Updated SKILL.md references to reflect new documentation locations
- Updated `.github/workflows/release.yml` for v1.0.5 release process

## [1.0.4] - 2025-10-21

### Added
- **Research Log Template Refactoring**
  - Simplified `research-log-template.md` for practical daily documentation
  - New `research-log-guidance.md` with comprehensive methodology

### Changed
- Template and reference structure mirrors successful v1.0.3 approach

## [1.0.3] - 2025-10-19

### Added
- **Privacy and Responsible AI Use guidance** following CRAIGEN principles
  - Prominent privacy warning section in README.md
  - Best practices for protecting private genealogical information
  - Clear DO/DO NOT guidelines for sharing data with AI systems
  - Reference to Coalition for Responsible AI in Genealogy
  - Privacy notice added to SKILL.md header

## [1.0.2] - 2025-10-19

### Added
- Comprehensive installation instructions in README.md
- Quick Start section for experienced users
- Detailed step-by-step installation guide for Claude.ai and Claude Code
- Prerequisites, verification steps, and troubleshooting section

### Changed
- Moved BMAD Method conversion details from README.md to CHANGELOG.md
- Improved wording in 'When Claude Uses This Skill' section
- Streamlined README for better user-facing information

## [1.0.1] - 2025-10-19

### Changed
- Renamed skill from "genealogy-research" to "family-history-planning"
- Updated all documentation to use "family history research" terminology
- Refined skill description to emphasize planning assistance
- Updated main titles in SKILL.md, README.md, and template files
- Added version tracking to SKILL.md frontmatter and header

## [1.0.0] - 2025-10-17

### Added
- Initial release of Family History Research Planning Skill for Claude
- Core skill file (SKILL.md) with procedural knowledge for family history and genealogy research
- Research planning workflow with GPS framework integration
- Citation creation system supporting 14+ source types
- Evidence analysis and conflict resolution framework
- Research logging templates and workflows
- Reference documentation:
  - Citation templates for census, vital records, land records, probate, military, immigration, newspapers, and more
  - Evidence evaluation frameworks for systematic conflict resolution
  - GPS (Genealogical Proof Standard) detailed guidelines
  - Advanced research strategies and methodologies
- Output templates:
  - Research plan template
  - Citation template
  - Evidence analysis template
  - Research log template
- Comprehensive README with usage instructions
- MIT License
- .gitignore for common development environments

### Documentation
- Professional genealogical standards compliance (GPS, Evidence Explained, BCG)
- Conversion notes from BMAD Method genealogy-assistant module
- Progressive disclosure architecture for efficient context usage

## Conversion from BMAD Method

This skill was converted from a BMAD Method genealogy assistant module that included:
- 3 specialized agents (Research Coordinator, Source Analyst, Evidence Evaluator)
- 4 workflows (research planning, citation generation, evidence analysis, research logging)
- Professional genealogical standards
- Template-based document generation

### Key Differences from BMAD

**BMAD Structure:**
- Multiple agent files with personas and menus
- Separate workflow files (YAML config + instructions + checklists)
- Template variable substitution
- Extensive step-by-step XML-tagged instructions

**Claude Skill Structure:**
- Single SKILL.md with procedural knowledge
- Reference files for detailed information
- Template files in assets
- Concise, focused guidance

### What Was Preserved
- All professional genealogical knowledge
- GPS framework and requirements
- Evidence Explained citation standards
- Conflict resolution methodologies
- Research strategies
- Template structures

### What Was Adapted
- Agent personas converted to procedural workflows
- Multi-file workflows consolidated
- XML-tagged instructions converted to markdown
- Variable placeholders preserved in templates
- Checklist validation integrated into workflows


[Unreleased]: https://github.com/emaynard/claude-family-history-research-skill/compare/v1.0.5...HEAD
[1.0.5]: https://github.com/emaynard/claude-family-history-research-skill/compare/v1.0.4...v1.0.5
[1.0.4]: https://github.com/emaynard/claude-family-history-research-skill/compare/v1.0.3...v1.0.4
[1.0.3]: https://github.com/emaynard/claude-family-history-research-skill/compare/v1.0.2...v1.0.3
[1.0.2]: https://github.com/emaynard/claude-family-history-research-skill/compare/v1.0.1...v1.0.2
[1.0.1]: https://github.com/emaynard/claude-family-history-research-skill/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/emaynard/claude-family-history-research-skill/releases/tag/v1.0.0
