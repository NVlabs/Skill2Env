# /vibe-replay:replay skill

This skill teaches AI agents how to generate session replays from [vibe-replay](https://github.com/tuo-lei/vibe-replay).

## How it works

- `SKILL.md` is the only file loaded into agent context when the skill is invoked
- This README is for humans only — it is never loaded by the agent

## What the agent learns

When the skill is loaded, the agent gains three capabilities:

### 1. Search and analyze local sessions (`sessions`)

Finds Claude Code, Cursor, and Codex sessions by query, project, provider, or retro signals.

```bash
npx vibe-replay sessions --query "auth bug" --limit 10 --json
npx vibe-replay sessions --query "PR review CI" --any --brief --dedupe --json
```

The agent uses the returned provider and file path to choose a session for replay, or to summarize a retro without manually browsing local transcript folders.

### 2. Generate GitHub PR artifacts (`--github`)

Produces markdown summary + animated GIF + SVG, ready to embed in PR descriptions.

```bash
npx vibe-replay --provider <provider> --session <path> --github
```

Output files (in `~/.vibe-replay/<slug>/`):
- `github-summary.md` — markdown with stats, tool breakdown, per-prompt details
- `session-preview.gif` — animated GIF (~30-60 KB)
- `session-preview.svg` — animated SVG with CSS keyframes

### 3. Generate interactive HTML replay (`--open`)

Produces a self-contained HTML file and opens it in the browser.

```bash
npx vibe-replay --provider <provider> --session <path> --open
```

## Use cases

### PR with text-only replay summary (default)

> "Create a PR with session replay"

The agent generates GitHub artifacts and embeds the **text summary** (stats, tool breakdown, per-prompt details) in the PR description. No binary files committed.

### PR with animated GIF

> "Create a PR with session replay, include the GIF"

The agent generates artifacts, copies the GIF into the repo (e.g., `.github/session-preview.gif`), and includes the image reference in the PR markdown. The GIF is typically 30-300 KB.

### Quick HTML replay

> `/vibe-replay:replay`

Generates a self-contained HTML file and opens it in the browser.

### Find a past session

> "Find the session where we debugged the Cursor auth bug"

The agent runs `vibe-replay sessions --json`, ranks matches, and reports the best candidates with provider, timestamp, project, and why each one matched.

### Session retro

> "Retro my last few vibe-replay sessions for prompt quality and tool usage"

The agent uses targeted `--scan` results to summarize prompt count, tool calls, duration, compactions, API errors, and process recommendations.

## Invocation modes

| Mode | Trigger | Example |
|------|---------|---------|
| Slash command | User types `/vibe-replay:replay` | `/vibe-replay:replay` |
| Model-invoked | User mentions replay when creating a PR | "Create a PR with session replay" |

## Install

### As a Claude Code plugin (recommended)

Open Claude Code, run `/plugin`, then search **vibe-replay** in the **Discover** tab and install.

Or via CLI:

```
/plugin marketplace add tuo-lei/vibe-replay
/plugin install vibe-replay@vibe-replay
```

### Manual (single file)

```bash
mkdir -p ~/.claude/skills/replay
curl -o ~/.claude/skills/replay/SKILL.md \
  https://raw.githubusercontent.com/tuo-lei/vibe-replay/main/skills/replay/SKILL.md
```

### For vibe-replay contributors

The project has a symlink at `.claude/skills/replay` → `skills/replay/`, so the skill is always loaded from source when working in this repo.

## CLI flags used by the skill

| Flag | Purpose |
|------|---------|
| `sessions` | Search local Claude Code, Cursor, and Codex sessions |
| `--session <path>` | Path to JSONL file (required for non-interactive mode) |
| `--provider <name>` | Provider returned by discovery/search, such as `claude-code`, `cursor`, or `codex` |
| `--open` | Generate HTML + open in browser + exit |
| `--github` | Generate markdown + GIF + SVG + exit |
| `--title "..."` | Override auto-detected title |

## Session discovery

For the current Claude Code session, the skill uses `${CLAUDE_SESSION_ID}` (substituted by Claude Code at load time) to grep for the current session's JSONL file in `~/.claude/projects/`.

For Cursor, Codex, and fuzzy/past Claude sessions, the skill uses `npx vibe-replay sessions --json` and then passes the returned `provider` and `filePath` to `vibe-replay --provider <provider> --session <path>`.
