---
name: replay
description: Find, analyze, and share AI coding sessions with vibe-replay. Use when the user asks for a replay, wants to find a past session, run a session retro, share Cursor/Claude/Codex session context, or attach session context to a PR.
allowed-tools: Bash(npx *) Bash(grep *) Bash(ls *) Bash(cat *) Bash(cp *) Bash(gh *)
argument-hint: [session-path-or-search-query]
---

# Session Replay and Search

This skill helps agents find local AI coding sessions, generate shareable replay artifacts, and paste polished session context into PRs. It uses [vibe-replay](https://github.com/tuo-lei/vibe-replay) for the raw session discovery, parsing, redaction, analytics, and export work, then uses agent judgment for review, cleanup, and sharing decisions.

## What this skill is for

Use this skill when the user asks to:

- Generate a replay or GitHub-ready summary of an AI coding session.
- Attach Claude Code, Cursor, or Codex session context to a PR.
- Find a previous session, transcript, replay, branch discussion, bug investigation, PR, or design thread.
- Remember what happened in a past agent conversation.
- Run a retro on prompt quality, tool usage, errors, compactions, cost, or agent efficiency.
- Compare sessions or choose which session should be replayed/shared.

Plain text summaries of an AI session - stats, tool breakdown, per-prompt details - are hard for an agent to write from scratch. Delegate that to `vibe-replay`, then use agent reasoning to handle the things a CLI cannot decide well:

- **Ranking session search results** - choosing the likely match from metadata and brief scan signals.
- **Reviewing flagged credentials** - deciding whether a regex hit is a real secret or a false positive.
- **Translating** session prompts that are not in the audience's language.
- **Softening tone** in prompts written when the user was frustrated.
- **Appending to PRs safely** - preserving existing PR descriptions instead of overwriting them.

Each cleanup step is opt-in. Ask the user before rewriting their content.

## Step 1 - Choose the session

Prefer structured discovery over manually browsing local history.

### If the user provides a session path

Use the provided path. Infer the provider when possible:

- Cursor transcripts usually live under `~/.cursor/projects/.../agent-transcripts/...`.
- Claude Code transcripts usually live under `~/.claude/projects/.../*.jsonl`.
- Codex sessions are discoverable through `vibe-replay sessions`; if the path is not obviously Claude or Cursor, pass the provider returned by search or ask the user.

### If this is the current Claude Code session

Find the current session file with `${CLAUDE_SESSION_ID}`:

```bash
grep -l '"sessionId":"${CLAUDE_SESSION_ID}"' ~/.claude/projects/*/*.jsonl 2>/dev/null
```

If multiple files match (normal after `/resume`), pick the oldest. `vibe-replay` auto-discovers related files by slug/project.

### If the user describes a past or fuzzy session

Use `vibe-replay sessions` first. Prefer `--json` so results can be ranked without scraping terminal text:

```bash
npx vibe-replay sessions --query "<terms>" --limit 10 --json
```

Useful filters:

```bash
npx vibe-replay sessions --project "vibe-replay" --json
npx vibe-replay sessions --provider cursor --query "auth bug" --json
npx vibe-replay sessions --query "codex parser" --scan --json
npx vibe-replay sessions --query "PR review CI" --any --brief --dedupe --json
```

Search workflow:

1. Start shallow with `--query` or `--project`, `--limit 10`, and `--json`.
2. Rank matches by timestamp, project, title/first prompt match quality, provider, and user intent.
3. If a remembered query has several loose terms and returns nothing, retry with `--any`.
4. Add `--brief` when the user asks a fuzzy retrospective question; it adds `matchQuality`, matched/unmatched terms, `whyMatched`, `brief`, `signals`, and `suggestedNextAction`.
5. Add `--dedupe` when repeated long-prompt sessions from multiple workspaces clutter results.
6. Only add plain `--scan` for a narrowed candidate set when the user asks about retro, efficiency, prompt quality, cost, tool usage, compactions, API errors, files modified, or session quality.

Avoid broad `--scan` over many sessions. It is intentionally available, but expensive compared with metadata search.

If `--json` returns an empty array, verify `vibe-replay` is installed and accessible:

```bash
npx vibe-replay --version
```

Then broaden or drop the query, retry with `--any`, filter by project/provider, or ask the user for a session path directly.

For search results, return a short ranked list with provider, timestamp, project, title or first prompt preview, slug/session id, why it matched, and whether deeper scan/replay is recommended. Do not dump full raw prompts unless the user asks.

After choosing a session, branch by intent:

- **PR sharing or replay export** - continue with Steps 2-5, then Step 7.
- **Session retro or efficiency analysis** - skip PR artifact cleanup and use Step 6.

## Step 2 - PR sharing path: generate the artifacts

Once you have a session path and provider, run `vibe-replay` with the provider when known:

```bash
npx vibe-replay --provider <provider> --session <PATH> --github
```

For Claude Code, `--provider claude-code` may be omitted because it is the default, but include the provider when it came from `vibe-replay sessions`. For Cursor, use `--provider cursor`. For Codex, use `--provider codex`.

This writes to `~/.vibe-replay/<slug>/`:

- `github-summary.md` - the markdown summary to paste into the PR.
- `redactions.json` - credential audit report.
- `session-preview.gif` / `.svg` - preview animations; skip unless the user explicitly asks.

If the user asks for an interactive local replay instead of PR artifacts, run:

```bash
npx vibe-replay --provider <provider> --session <PATH> --open
```

## Step 3 - Review credential redactions

Read `redactions.json`. It has two fields:

- `alreadyRedactedCount` - how many secrets `vibe-replay` already replaced with `[REDACTED]` automatically. Just report this number to the user.
- `leftoverFindings` - regex hits in the final markdown that `vibe-replay` was not confident enough to auto-redact.

If `leftoverFindings` is empty, say so and move on.

If `leftoverFindings` is non-empty, present the findings to the user. For each one:

- Show: rule (e.g. "GitHub Token"), context snippet (one line of surrounding text), and your judgment of whether it looks real
- Note that some matches are false positives - commit hashes, UUIDs, version strings, package names can look like tokens. Use the surrounding context to judge.
- Offer choices: "Redact all", "Review one-by-one", "Keep as-is" (if you believe they're false positives), or "Cancel"

If the user chooses to redact any finding, first copy the original to a working file. Do not overwrite `github-summary.md`:

```bash
cp ~/.vibe-replay/<slug>/github-summary.md ~/.vibe-replay/<slug>/github-summary.clean.md
```

Then apply replacements to `github-summary.clean.md`. The original stays intact so the user can recover the unedited version. All later steps (translation, tone) also operate on the `.clean.md` copy. Create it on the first edit, then keep using it.

## Step 4 - Offer translation

Read the working file (`github-summary.clean.md` if it exists from step 3, otherwise `github-summary.md`):

```bash
cat ~/.vibe-replay/<slug>/github-summary.clean.md 2>/dev/null || cat ~/.vibe-replay/<slug>/github-summary.md
```

Detect the language of the user-prompt sections. If the dominant language is not English (or does not match the repo's primary language - check `README.md` if unsure), ask:

> "The prompts are in {detected language}. Translate to {target language} before sharing? [Yes / No]"

If yes, apply this prompt to the user-prompt sections of the markdown (always write the result to `github-summary.clean.md`, creating it from a copy of the original if it doesn't exist yet):

```
You are a translation assistant for AI coding sessions.
Translate the following user prompts from {source} to {target}.

Rules:
- Only translate natural language text
- Preserve code blocks, file paths, variable names, CLI commands verbatim
- Preserve markdown formatting
- Keep technical jargon in English (API, endpoint, middleware, etc.)
- Maintain the original intent and tone
- If a prompt is already in {target}, return it unchanged
```

Only rewrite the prompt text. Do not touch tool-call output, file diffs, or stats.

## Step 5 - Offer tone softening

Scan the user-prompt sections for harsh language, profanity, frustration, or passive-aggressive tone toward the AI. If you find any, ask:

> "Some prompts contain {brief example, e.g. 'frustrated language'}. Soften the tone before sharing? [Professional / Neutral / Friendly / Skip]"

If the user picks a style, apply this prompt to the affected user prompts (write the result to `github-summary.clean.md`, same rule as step 3):

```
You are a tone adjustment assistant for AI coding sessions.
Rewrite the following user prompts to be more {style}.

Rules:
- Preserve the EXACT technical meaning and intent
- Remove frustration, harsh language, profanity, or passive-aggressive tone
- Keep code references, file paths, and technical terms unchanged
- If a prompt is already appropriate, return it unchanged
- Do NOT add excessive politeness or corporate-speak - keep it natural

Style guide:
- Professional: direct but respectful, suitable for work sharing
- Neutral: factual and unemotional, like documentation
- Friendly: warm and collaborative, like messaging a teammate
```

## Step 6 - Alternative path: session retro guidance

If the user asked for a session retro instead of PR sharing, do not generate or clean `github-summary.md`. Narrow the candidate set first, then use scan-backed results:

```bash
npx vibe-replay sessions --project "<project>" --limit 5 --scan --json
```

If the user gave search terms instead of a project, use a narrowed query:

```bash
npx vibe-replay sessions --query "<terms>" --limit 5 --scan --json
```

Separate observations from recommendations.

For efficiency analysis, look at:

- Prompt count and whether the user had to repeat intent.
- Tool calls per prompt and edit count per prompt.
- Long duration, API errors, compactions, and subagent count.
- First prompt clarity: goal, constraints, files, expected verification, and merge/review instructions.

Prefer actionable advice such as "the first prompt had a clear goal but missed verification criteria" or "the session became expensive because it searched broadly before narrowing to one file."

## Step 7 - Preview and paste

Show the user the final markdown (or a diff against the original if changes were made). Ask:

> "Paste into a PR now? [Append to current PR's body / Replace current PR's body / Open new PR / Just save the file / Cancel]"

Important: `gh pr edit --body-file <file>` replaces the entire PR body. If the user already has a hand-written summary, checklist, or screenshots in the PR body, replacing wipes them silently. Default to appending under a `## Session Replay` heading instead.

To append (recommended default):

```bash
# Read existing body, then write existing + separator + cleaned summary
gh pr view --json body --jq .body > /tmp/pr-body.md
SUMMARY=$(ls ~/.vibe-replay/<slug>/github-summary.clean.md 2>/dev/null || echo ~/.vibe-replay/<slug>/github-summary.md)
echo "" >> /tmp/pr-body.md
echo "---" >> /tmp/pr-body.md
echo "" >> /tmp/pr-body.md
echo "## Session Replay" >> /tmp/pr-body.md
echo "" >> /tmp/pr-body.md
cat "$SUMMARY" >> /tmp/pr-body.md
gh pr edit --body-file /tmp/pr-body.md
```

To replace, only if the user explicitly chooses this, confirm out loud what is about to be lost first:

```bash
gh pr edit --body-file ~/.vibe-replay/<slug>/github-summary.clean.md
```

If saving locally only, the cleaned version is already at `~/.vibe-replay/<slug>/github-summary.clean.md` from earlier steps. Just report the path. If no cleanup steps ran, copy the original first so the user has a `.clean.md` to share without touching the source.

## Notes

- The skip-the-image rule still applies: by default, do NOT include the GIF reference (first line of the original markdown) when pasting into a PR. Committing a binary GIF bloats git history. Only include it if the user explicitly asks for the GIF.
- `github-summary.clean.md` is the only shareable markdown file the skill edits. The original `github-summary.md` is treated as read-only so the user can always recover the raw output.
- The literal `${CLAUDE_SESSION_ID}` is interpolated by the Claude Code harness when this skill runs. If it is empty or no file matches, ask the user which session to use or search with `vibe-replay sessions`.
- Session data may contain private code, credentials, internal links, or frustrated wording. Quote only the minimum needed.
- Treat `vibe-replay sessions` as metadata/subsequence search, not semantic search. If results are weak, broaden terms, filter by project/provider, or inspect a small number of returned transcripts.
