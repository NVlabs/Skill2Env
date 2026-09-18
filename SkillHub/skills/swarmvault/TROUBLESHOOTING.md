# Troubleshooting

## `swarmvault` command not found

The ClawHub skill does not bundle the CLI binary by itself. Install the published package and verify it:

```bash
npm install -g @swarmvaultai/cli
swarmvault --version
```

If the binary still is not found, check that npm's global bin directory is on `PATH`.

## Node version too old

SwarmVault requires Node `>=24`.

```bash
node --version
```

Upgrade Node before troubleshooting provider or compile behavior.

## The vault compiles, but quality is weak

Check whether the vault is still using the built-in `heuristic` provider. That is a valid local/offline default, but its synthesis is intentionally lighter. Add a model provider in `swarmvault.config.json` when you want richer synthesis quality or optional capabilities such as embeddings, vision, or image generation.

For local semantic graph query, `embeddingProvider` must point at an embedding-capable backend such as `ollama` or another OpenAI-compatible embeddings service. The built-in `heuristic` provider does not generate embeddings.

## Audio or video files ingest, but no transcript appears

Audio and video ingest need `tasks.audioProvider` to point at a provider with `audio` capability. Without that, SwarmVault still ingests the source and records an extraction warning instead of failing the whole run.

The quickest fully-local fix is `swarmvault provider setup --local-whisper --apply`, which installs a `local-whisper` provider (whisper.cpp shell-out), downloads the default ggml model into `~/.swarmvault/models/`, and wires `tasks.audioProvider` at it. If the command reports the binary missing, install whisper.cpp first (`brew install whisper-cpp` on macOS, `sudo apt install whisper.cpp` on Debian/Ubuntu) and re-run. Override binary or model paths with `localWhisper.binaryPath` / `localWhisper.modelPath` in `swarmvault.config.json` or `SWARMVAULT_WHISPER_BINARY` in the environment.

Local video extraction also needs `ffmpeg` on PATH or `SWARMVAULT_FFMPEG_BINARY`. Public video URL ingest with `swarmvault ingest --video <url>` or `swarmvault add --video <url>` needs `yt-dlp` on PATH or `SWARMVAULT_YTDLP_BINARY`.

YouTube transcript ingest does not need a model provider, but it can still fail when the video has no accessible captions or the upstream transcript fetch path is unavailable.

## Source reviews or dashboards did not appear

If you expected a source-scoped guide or review page, use one of these flows:

```bash
swarmvault ingest <input> --guide
swarmvault source add <input> --guide
swarmvault source session <source-id-or-session-id>
```

Then verify:

- `wiki/outputs/source-briefs/`
- `wiki/outputs/source-sessions/`
- `wiki/outputs/source-guides/`
- `wiki/dashboards/index.md`
- `wiki/dashboards/timeline.md`
- `wiki/dashboards/source-sessions.md`
- `wiki/dashboards/source-guides.md`
- `state/approvals/`

## `wiki/graph/report.md`, share kit, or search artifacts are missing

Run:

```bash
swarmvault next
swarmvault compile
swarmvault doctor
```

Then verify:

- `wiki/graph/report.md`
- `wiki/graph/share-card.md`
- `wiki/graph/share-card.svg`
- `wiki/graph/share-kit/`
- `state/graph.json`
- `state/retrieval/`

If the vault lives inside git and you want a quick graph-level delta, run `swarmvault diff`.

## Artifacts appear in the wrong directory

Check whether `SWARMVAULT_OUT` is set:

```bash
echo "$SWARMVAULT_OUT"
```

When it is set, generated `raw/`, `wiki/`, `state/`, `agent/`, and `inbox/` directories resolve under that output root. `swarmvault.config.json` and `swarmvault.schema.md` remain in the project root.

## Graph status reports stale

Run:

```bash
swarmvault graph status .
swarmvault check-update .
```

If it recommends `swarmvault graph update`, the detected changes are code-only and can use the faster graph refresh path; `swarmvault update` is the top-level alias for the same refresh. If it recommends `swarmvault compile`, graph/report artifacts are missing, a non-code tracked source changed, or a pending semantic refresh already exists.

When you know exactly which files changed, `swarmvault graph update --file <path>` (repeatable) refreshes just those files instead of walking every tracked root. Concurrent per-file refreshes coalesce through a lock plus queue under `state/watch/`, so rapid edit bursts do not stack compiles. Installed Claude Code hooks run this automatically in the background after Edit/Write tools.

`swarmvault graph update` and `swarmvault update` abort when the refreshed graph drops more than 25% of nodes or edges. Re-run with `swarmvault graph update . --force`, `swarmvault update . --force`, or `SWARMVAULT_FORCE_UPDATE=1` only when the shrink is expected, such as after deliberately deleting a large source tree.

Before exporting, merging, pushing, or publishing graph artifacts, run `swarmvault graph validate --strict` to catch dangling references, duplicate ids, or invalid confidence values.

## Compile fails on a larger note set

If an older CLI fails with heap exhaustion, `Map maximum size exceeded`, or a bare `Unexpected end of JSON input`, upgrade SwarmVault and rerun compile:

```bash
npm install -g @swarmvaultai/cli@latest
swarmvault compile
```

Current releases bound source-analysis concurrency and graph projection during compile. If the error says `Failed to parse JSON file ...`, remove or restore the named derived state file and compile again; JSON state writes are atomic in current releases to reduce partial-file failures.

## Agent rule files differ

That can be expected. SwarmVault owns only the managed block between `swarmvault:managed:start` and `swarmvault:managed:end`. The managed SwarmVault block should match across compatible agent rule files, but user-owned text before or after that block is preserved and may differ per tool.

New vaults do not receive agent rule files during `init`, `quickstart`, `scan`, or `clone` unless you pass `--install-agent-rules` with configured `agents`. For one-off setup, run `swarmvault install --agent <agent>` instead.

## Vault doctor reports warnings

`swarmvault doctor` is the broad health summary. It checks graph artifacts, retrieval, review queues, watch state, migrations, managed sources, and task ledgers, then prints concrete follow-up commands. The `swarmvault graph serve` workbench shows the same full check list with details and copyable suggested commands.

If you only need orientation and do not want any prompts, notices, repairs, or writes, run `swarmvault next` first. It returns `status`, key `paths`, `checks`, and prioritized `recommendations` in human or JSON output.

Safe derived retrieval repairs can be applied with:

```bash
swarmvault doctor --repair
```

If the graph or wiki pages are missing, run `swarmvault compile`; if review or candidate counts are high, inspect `swarmvault review list` and `swarmvault candidate list`.

## Context pack is empty or missing expected evidence

Context packs are built from compiled graph and search artifacts. Run `swarmvault compile` first when the vault is new, then build a narrower pack:

```bash
swarmvault context build "Prepare the next agent" --target ./src --budget 8000
```

Then verify:

- `wiki/context/`
- `state/context-packs/`

If many items are listed as omitted, increase `--budget` or narrow `--target`.

## MCP client reports `[object Undefined]` or `no such column`

First verify the installed CLI version used by the MCP client:

```bash
swarmvault --version
```

SwarmVault 3.14.1 and newer normalize optional MCP response fields and retry hyphenated retrieval targets with conservative SQLite FTS tokenization. Upgrade and restart the MCP client subprocess if you see `unacceptable kind of an object to dump [object Undefined]` from `query_vault`, `build_context_pack`, `start_task`, or `start_memory_task`, or if a hyphenated target such as `concept:distributionally-robust-receive-combining` reports `no such column`.

```bash
npm install -g @swarmvaultai/cli@latest
```

## Task is missing or does not show in the graph

Tasks are durable local artifacts. Start or inspect them with:

```bash
swarmvault task list
swarmvault task start "Prepare the next agent" --target ./src
swarmvault task resume <task-id>
```

Then verify:

- `wiki/memory/index.md`
- `wiki/memory/tasks/`
- `state/memory/tasks/`

Run `swarmvault compile` after creating or updating tasks when you want task and decision nodes to appear in `state/graph.json` and the graph viewer. Existing `memory` commands remain compatibility aliases.

## Agent searches are being denied

Search denial only happens after an explicit opt-in: installing with `swarmvault install --agent <agent> --hook --graph-first`, or setting `hooks.graphFirst: "deny"` in `swarmvault.config.json`. With that opt-in, the first broad Grep/Glob/Bash search per session is intercepted with a deny plus a redirect message pointing at the plain `swarmvault graph query|explain|path` commands (the message warns against `--json`, which produces much larger output). `swarmvault graph query "<seed>"` prints the top matches with page paths plus an inline excerpt of the best-matching wiki page, so one command usually answers where-is/what-calls questions without follow-up file reads. For who-calls and impact-of-change questions, the redirect message also recommends `swarmvault graph callers <symbol>`, which lists every caller from graph call edges with exact file:line call-site evidence instead of a repo-wide grep. This is a one-time guided redirect, not a block: repeating the same search is then allowed, so work is never stuck. Searches scoped to vault artifact directories (`wiki/`, `raw/`, `state/`), single files, or search tools filtering piped output are never intercepted.

Without the opt-in, hooks stay advisory (`context` mode): a one-time guidance note, no denial. To change or disable the behavior:

```bash
SWARMVAULT_GRAPH_FIRST=context   # session guidance only, no search interception
SWARMVAULT_GRAPH_FIRST=off       # disable graph-first behavior entirely
```

Or set `hooks.graphFirst` to `deny`, `context`, or `off` in `swarmvault.config.json`. The default without any opt-in is `context`.

## `swarmvault install` edited `.gitignore` or `tsconfig.json`

That is intentional host-project hygiene. `swarmvault install --agent <agent>` appends the vault artifact directories (`raw/`, `wiki/`, `state/`, `agent/`, `inbox/`) to `.gitignore` in git repos, adds them to a strict-JSON `tsconfig.json` `"exclude"` list so stored source copies under `raw/` do not break the host typecheck, and warns when linter configs still cover the artifact directories. Commented (JSONC) tsconfig files are never rewritten — a warning explains the manual edit instead.

To opt out, set `SWARMVAULT_OUT` so generated artifacts live outside the repo; the hygiene edits are skipped entirely.

## Hook is not firing

Reinstall the hook in the project root and verify the settings entries:

```bash
swarmvault install --agent claude --hook
```

Then check that `.claude/settings.json` contains the SwarmVault hook entries (session start, search interception, and post-edit refresh matchers) and that `.claude/hooks/swarmvault-graph-first.js` exists. Reinstalling migrates older installed hook entries to the current matcher layout while preserving user-owned hook entries. For user-scope installs under `~/.claude` (`install --agent claude --hook --scope user`), remember the hook intentionally no-ops in repos without a compiled `wiki/graph/report.md`, so run `swarmvault compile` first if the session shows no graph-first behavior.

## Agent install or hooks seem stale

Re-run the relevant install command in the project root:

```bash
swarmvault install status --agent codex --hook
swarmvault install --agent claude --hook
swarmvault install --agent gemini --hook
swarmvault install --agent opencode --hook
swarmvault install --agent copilot --hook
swarmvault install --agent kilo --hook
```

For Aider:

```bash
swarmvault install --agent aider
```

## Update paths

Update the skill:

```bash
clawhub update swarmvault
```

Update the CLI:

```bash
npm install -g @swarmvaultai/cli@latest
```

## More Help

- Docs: https://www.swarmvault.ai/docs
- Providers: https://www.swarmvault.ai/docs/providers
- Web troubleshooting: https://www.swarmvault.ai/docs/getting-started/troubleshooting
- GitHub issues: https://github.com/swarmclawai/swarmvault/issues
