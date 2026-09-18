# Version 1.0.5: Documentation Reorganization

This release reorganizes the project structure to better align guidance documents with research references, making it easier for users to locate comprehensive methodology resources.

## What's New

### Documentation Structure Reorganization

**Moved guidance files to `references/` directory**
- `research-log-guidance.md` - Moved from `assets/templates/` to `references/`
- `research-plan-guidance.md` - Moved from `assets/templates/` to `references/`

**Updated SKILL.md references**
- Corrected references to relocated guidance documents
- Improved navigation between templates and guidance

**Benefits of this reorganization:**
- Guidance documents grouped with other reference materials
- Clearer distinction between templates (in `assets/templates/`) and references (in `references/`)
- Better information architecture for users seeking detailed methodology
- Easier maintenance and documentation updates

## Structure After Reorganization

```
genealogy-research-skill/
├── assets/templates/          # Simplified, practical templates
│   ├── research-plan-template.md
│   ├── research-log-template.md
│   ├── citation-template.md
│   └── evidence-analysis-template.md
│
├── references/                # Comprehensive reference documentation
│   ├── research-plan-guidance.md
│   ├── research-log-guidance.md
│   ├── citation-templates.md
│   ├── evidence-evaluation.md
│   ├── gps-guidelines.md
│   └── research-strategies.md
│
├── SKILL.md                   # Main skill definition
├── README.md                  # Installation and overview
└── CHANGELOG.md               # Version history
```

## Why This Matters

### Improved Information Architecture

Users now have a clearer structure:
- **Templates** (`assets/templates/`) - Quick, practical tools for daily work
- **References** (`references/`) - Comprehensive methodology and detailed guidance

### Better User Experience

When users need:
- **Quick guidance**: Start with simplified templates
- **Detailed methodology**: Consult reference documents in the same `references/` directory

This mirrors the successful separation of simplified templates from detailed guidance introduced in v1.0.3 and v1.0.4.

## Professional Standards

All documentation continues to support:
- **Genealogical Proof Standard (GPS)** - Reasonably exhaustive research documented
- **Evidence Explained** - Complete and accurate citations
- **Board for Certification of Genealogists (BCG)** - Professional methodology

## Installation

### Quick Start

1. Download the latest release: `family-history-planning-v1.0.5.zip`
2. Extract the ZIP file
3. **Claude.ai users**: Enable Skills in Settings > Capabilities, then upload the skill folder
4. **Claude Code users**: Move the `family-history-planning` folder to `~/.claude/skills/`
5. Start using: Just ask Claude about family history research!

### Full Instructions

See the [README.md](https://github.com/emaynard/claude-family-history-research-skill/blob/main/README.md#installation) for complete installation instructions.

## What This Skill Does

The Family History Research Planning Skill provides Claude with specialized knowledge for:
- **Research Planning** - Create structured research plans following GPS standards
- **Citation Creation** - Generate properly formatted genealogical citations for 14+ source types
- **Evidence Analysis** - Systematically analyze and resolve conflicting genealogical evidence
- **Research Documentation** - Create professional research logs and documentation

## Changelog

### Version 1.0.5 Changes
- Reorganized guidance documents to `references/` directory
- Updated SKILL.md references to reflect new documentation locations
- Improved project structure for better information architecture
- Updated GitHub Actions release workflow

### Related Changes from Previous Releases
See the [full changelog](https://github.com/emaynard/claude-family-history-research-skill/blob/main/CHANGELOG.md) for complete version history.

## Support

- **Issues**: Report bugs or request features in [GitHub Issues](https://github.com/emaynard/claude-family-history-research-skill/issues)
- **Documentation**: See [README.md](https://github.com/emaynard/claude-family-history-research-skill/blob/main/README.md)
- **Professional Standards**: Refer to GPS, Evidence Explained, and BCG resources
- **Responsible AI**: Learn more at [CRAIGEN.org](https://craigen.org)

---

**Full Changelog**: https://github.com/emaynard/claude-family-history-research-skill/compare/v1.0.4...v1.0.5
