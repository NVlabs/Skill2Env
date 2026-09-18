# Alpha Insights Installation Contract for AI Agents

This repository root is the Alpha Insights skill package. Do not create a sibling
directory next to `alpha-insights`; install or copy this package itself.

## Goal

Install Alpha Insights for the user's current agent platform, then prove the
runtime is wired correctly with the matching verifier.

## Platform Decision

1. If the user asks for Codex Desktop, or `CODEX_HOME` / `~/.codex` is present,
   use the Codex path:
   ```bash
   python3 scripts/install_codex.py --verify
   ```
2. If the user asks for Claude Code or a Cloud Code compatible runtime, keep the
   root `SKILL.md` frontmatter hooks intact and install this folder as that
   platform's skill package. Then run:
   ```bash
   python3 scripts/verify_cloudcode.py
   ```
3. If the platform is unclear, ask the user which agent they use. Do not guess.

## Codex Desktop Contract

The installer must:

- Copy the package to `$CODEX_HOME/skills/alpha-insights/`, or
  `~/.codex/skills/alpha-insights/` when `CODEX_HOME` is unset.
- Replace any existing `alpha-insights` install directly. Do not create sibling
  backup directories under `$CODEX_HOME/skills/` or `~/.codex/skills/`.
- Remove Cloud Code-only frontmatter hooks from the installed `SKILL.md`.
- Rewrite inline resume checks to use the installed absolute Codex skill path.
- Register Codex hook wrappers in `~/.codex/hooks.json`:
  - PreToolUse -> `scripts/codex_hooks/alpha_insights_pre_tool.py`
  - PostToolUse -> `scripts/codex_hooks/alpha_insights_post_tool.py`
- Preserve unrelated hooks already present in `hooks.json`.
- Run `scripts/verify_codex.py` unless the user explicitly skips verification.

## Claude Code / Cloud Code Compatible Contract

The installed package must keep the root `SKILL.md` frontmatter hooks. Those
hooks call the shared harness through `${CLAUDE_PLUGIN_ROOT}` and the inline
resume check through `${CLAUDE_SKILL_DIR}`.

Correct package boundary:

```text
~/.claude/skills/alpha-insights/SKILL.md
~/.claude/skills/alpha-insights/frameworks/
~/.claude/skills/alpha-insights/scripts/
```

Wrong package boundaries:

```text
~/.claude/skills/BusinessAnalystSkill/V4/alpha-insights/
~/.claude/skills/alpha-insights/alpha-insights/SKILL.md
~/.claude/skills/alpha-insights/SKILL.md  # with frontmatter hooks stripped
```

Run `scripts/verify_cloudcode.py` after installation or before publishing.

## Proof Required

After installation, report:

- Installed skill path
- Hook registration status
- Python compile status
- HTML write guard smoke result
- Stage 1 gate smoke result
- Stage 3.5 interview gate smoke result
