---
name: alterlab-skill-name
description: <Verb-led statement of what the skill does, naming the real tools/libraries/databases/methods>. Use when <concrete trigger conditions and keywords a user's request would contain>. Part of the AlterLab Academic Skills suite.
license: MIT
allowed-tools: Read Write Edit Bash(python:*)
metadata:
  skill-author: AlterLab
  version: "1.0.0"
---

# Skill Title

One-paragraph overview: what this skill does and the value it adds. Keep the whole
SKILL.md body under ~500 lines — move long detail into `references/` (loaded on demand).

## When to Use This Skill

Use this skill when the user wants to:
- <concrete task 1>
- <concrete task 2>

### Does NOT Trigger

| Scenario | Use Instead |
|----------|-------------|
| <adjacent task> | `alterlab-other-skill` |

## Core Capabilities

### 1. <Capability>

Concrete, correct guidance with real APIs/commands. Cite real sources; never fabricate
citations, benchmarks, or DOIs.

## Resources

- `references/<topic>.md` — detailed reference loaded on demand
- `scripts/<tool>.py` — runnable helper (invoke as `python scripts/<tool>.py`)

<!--
AUTHORING CHECKLIST (see CONTRIBUTING.md → Skill Quality Standards):
- name == this directory's name, lowercase-hyphen, no 'claude'/'anthropic'
- description: third person, leads with what + "Use when", suite label LAST, <=1024 chars
- body <500 lines; reference files exist; tools scoped in allowed-tools
- add evals/evals.json on the docs/evals.schema.json shape
  (>=3 should_trigger + >=1 should_not_trigger assertion — see docs/evals.md)
- validate: python scripts/audit_skills.py  &&  uv run pytest tests/
-->
