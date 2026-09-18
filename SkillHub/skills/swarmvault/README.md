# SwarmVault Skill

Use the SwarmVault skill when you want a local-first knowledge vault that compiles books, articles, notes, transcripts, chat exports, emails, calendars, datasets, spreadsheets, slide decks, screenshots, URLs, code, and research captures into durable markdown pages, a searchable graph, dashboards, resumable chat sessions, static AI export packs, context packs, a task memory ledger, and reviewable outputs on disk.

SwarmVault is built on the [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) pattern: keep a durable wiki between you and raw sources using a three-layer architecture (raw sources, wiki, schema). The LLM does the bookkeeping — cross-referencing, consistency, updating — while you curate sources and think about what they mean. SwarmVault turns that pattern into a local toolchain with graph navigation, search, review flows, automation, and optional provider-backed synthesis.

## Install

Install the skill from ClawHub:

```bash
clawhub install swarmvault
```

Install the CLI it depends on:

```bash
npm install -g @swarmvaultai/cli
swarmvault --version
swarmvault quickstart ./your-repo
swarmvault quickstart ./whitepaper.pdf --no-serve
swarmvault next
swarmvault demo --no-serve
swarmvault source add https://github.com/karpathy/micrograd
swarmvault ingest ./meeting.srt --guide
swarmvault ingest ./customer-call.mp3
swarmvault ingest https://www.youtube.com/watch?v=dQw4w9WgXcQ
swarmvault ingest --video https://example.com/product-demo.mp4
swarmvault source session transcript-or-session-id
swarmvault chat "What should the next agent know?"
swarmvault export ai --out ./exports/ai
```

Requirements:

- Node `>=24`
- A working `swarmvault` or `vault` binary on `PATH`

Update paths:

```bash
clawhub update swarmvault
npm install -g @swarmvaultai/cli@latest
```

## When To Use This Skill

- You want knowledge work to stay on disk instead of disappearing into chat history.
- The repo already contains `swarmvault.config.json` or `swarmvault.schema.md`.
- You want markdown wiki pages, graph artifacts, local search, approvals, candidates, and MCP exposure from the same workspace.
- You want resumable conversations over the compiled wiki and static handoff bundles for other tools.
- You want a save-first compile/query/review loop for source collections, codebases, or research material.
- You want one workflow for mixed non-code material such as EPUBs, CSV/TSV files, XLSX workbooks, PPTX decks, transcripts, Slack exports, mailbox files, and calendar exports.

## Quickstart

```bash
swarmvault quickstart ./your-repo
swarmvault quickstart ./whitepaper.pdf --no-serve
swarmvault quickstart ./your-repo --no-serve
swarmvault next
swarmvault demo --no-serve
swarmvault init --obsidian --profile personal-research
swarmvault source add ./exports/customer-call.srt --guide
swarmvault source session file-customer-call-srt-12345678
swarmvault source add https://github.com/karpathy/micrograd
swarmvault ingest ./src --repo-root .
swarmvault ingest ./customer-call.mp3
swarmvault ingest https://www.youtube.com/watch?v=dQw4w9WgXcQ
swarmvault ingest --video https://example.com/product-demo.mp4
swarmvault add https://arxiv.org/abs/2401.12345
swarmvault compile --max-tokens 120000
swarmvault diff
swarmvault graph share --post
swarmvault graph share --svg ./share-card.svg
swarmvault graph share --bundle ./share-kit
swarmvault query "What is the auth flow?"
swarmvault context build "Implement the auth refactor" --target ./src --budget 8000
swarmvault task start "Implement the auth refactor" --target ./src --agent codex
swarmvault doctor --repair
swarmvault graph blast ./src/index.ts
swarmvault graph status ./src
swarmvault check-update ./src
swarmvault graph stats
swarmvault graph validate --strict
swarmvault update ./src
swarmvault graph cluster
swarmvault cluster-only
swarmvault graph tree --output ./exports/tree.html
swarmvault tree --output ./exports/tree.html
swarmvault graph serve
swarmvault graph export --report ./exports/report.html
swarmvault graph export --callflow ./exports/callflow.html
swarmvault graph export --obsidian ./exports/graph-vault
swarmvault graph export --neo4j ./exports/graph.cypher
swarmvault merge-graphs ./exports/graph.json ./other-graph.json --out ./exports/merged-graph.json
swarmvault chat "What should the next agent know?"
swarmvault chat --resume <session-id> "What changed?"
swarmvault export ai --out ./exports/ai
swarmvault clone https://github.com/owner/repo --no-viz
swarmvault mcp
```

For the fastest scratch walkthrough of a local file, local repo, public GitHub repo, or docs tree, run `swarmvault quickstart ./path`, `swarmvault quickstart ./path --no-serve`, `swarmvault scan ./path --no-viz`, or `swarmvault clone https://github.com/owner/repo --branch main --no-viz`. `quickstart` is the beginner-friendly alias for `scan`: it initializes the current directory as a vault, ingests that input, compiles immediately, opens the graph viewer by default, and writes `wiki/graph/share-card.md`, `wiki/graph/share-card.svg`, and `wiki/graph/share-kit/`. Interactive file and directory runs show bounded stderr progress with the active file while JSON, MCP, watch, and CI-style flows stay quiet. Run `swarmvault next` when you want a read-only status check that recommends init, ingest, compile, query, review, or refresh commands. Use `quickstart --mcp`, `scan --mcp`, or `clone --mcp` when the next step should be an MCP stdio server.

If you want the same zero-config walkthrough without supplying your own inputs first, run `swarmvault demo --no-serve`. It creates a temporary demo vault with bundled sources and compiles it immediately.

For very large graphs, `swarmvault graph serve` and `swarmvault graph export --html` automatically start in overview mode. Add `--full` when you explicitly want the full canvas rendered. `swarmvault graph share --post` prints a compact copyable summary, `swarmvault graph share --svg [path]` writes a 1200x630 visual card, `swarmvault graph share --bundle [dir]` writes a portable share kit for posting, linking, or screenshotting, `swarmvault graph cycles` finds deterministic directed cycles, `swarmvault graph callers <symbol>` lists every caller of a symbol from graph call edges with exact file:line call-site evidence — it scans only the files the graph identifies as callers, so who-calls and impact-of-change questions skip repo-wide grep, `swarmvault graph status [path]` and `swarmvault check-update [path]` check graph/report freshness without writing watch artifacts, `swarmvault graph stats` prints lightweight graph counts and relation mix, `swarmvault graph validate [graph] --strict` checks duplicate ids, dangling references, confidence bounds, and conflicted-edge evidence before export/merge/push workflows, `swarmvault graph update [path]` and `swarmvault update [path]` block unexpected node/edge drops unless `--force` is explicit, `swarmvault graph update --file <path>` (repeatable) is the code-only fast path that refreshes just the named files instead of walking every tracked root — concurrent refreshes coalesce through a lock plus queue under `state/watch/`, `swarmvault watch [path] --once` targets one repo root without persisting watch config, `swarmvault graph query` accepts relation/context/evidence/node/language filters for focused traversal, `swarmvault graph tree [--output <html>]` / `swarmvault tree [--output <html>]` writes an interactive source/module/symbol tree with a node inspector, `swarmvault graph merge <graph...> --out <path>` / `swarmvault merge-graphs <graph...> --out <path>` combines SwarmVault or node-link graph JSON, `swarmvault graph cluster [--resolution <n>]` and `swarmvault cluster-only [vault]` recompute communities and graph report artifacts from the existing graph without re-ingest, and `graph export` also supports `--html-standalone`, `--json`, `--callflow`, `--obsidian`, `--canvas`, and `--neo4j` when you need richer sharing, Obsidian-native artifacts, or a Neo4j-ready Cypher import. `swarmvault diff` compares the current graph against the last committed graph so you can inspect graph-level changes after a compile.

`swarmvault context build "<goal>" --target <path-or-node> --budget <tokens>` creates an agent-ready evidence pack from the compiled vault. It saves JSON under `state/context-packs/`, writes a markdown companion under `wiki/context/`, reports omitted items when the token budget is too small, and can print `markdown`, `json`, or `llms` output for kickoff prompts and handoffs.

`swarmvault chat "question"` creates a persisted conversation over the compiled vault. Each turn writes structured state under `state/chat-sessions/` and a markdown transcript under `wiki/outputs/chat-sessions/`; use `swarmvault chat --resume <id> "follow-up"`, `chat --list`, and `chat --delete <id>` to manage saved sessions.

`swarmvault export ai --out <dir>` writes a static handoff pack for other agents and crawlers. The pack includes `llms.txt`, `llms-full.txt`, `graph.jsonld`, `manifest.json`, `ai-readme.md`, and per-page `.txt`/`.json` siblings so the compiled wiki can be consumed without starting the viewer or MCP server.

`swarmvault task start "<goal>" --target <path-or-node>` creates a durable task ledger and automatically links an initial context pack. Use `swarmvault task update <id> --note|--decision|--changed-path|--context-pack`, `swarmvault task finish <id> --outcome <text>`, and `swarmvault task resume <id> --format markdown|json|llms` to preserve decisions, evidence, touched files, outcomes, and follow-ups for the next agent. The older `memory` commands remain compatibility aliases.

`swarmvault doctor` is the quickest whole-vault health check before an agent handoff or viewer session. It reports graph, retrieval, review queue, watch status, migration, managed-source, and task state; `--repair` rebuilds safe derived retrieval artifacts. The same checks are available in the graph viewer workbench and through MCP as `doctor_vault`; the workbench also shows prioritized next actions, check details, copyable suggested commands, explicit capture modes, title/tag capture fields, editable context/task token budgets, and action receipts.

The default `heuristic` provider is a valid local/offline starting point. Add a model provider in `swarmvault.config.json` when you want richer synthesis quality or optional capabilities such as embeddings, vision, or image generation. The recommended fully-local setup is `ollama pull gemma4` wired up as the `compileProvider` and `queryProvider` (see the root README for the exact config block). Any supported provider works - OpenAI, Anthropic, Gemini, OpenRouter, Groq, Together, xAI, Cerebras, openai-compatible, or custom. Use `swarmvault provider add|list|show|remove` for config-preserving provider registry edits. Code files are always parsed locally via tree-sitter; only non-code text or image sources go to configured model providers.

`swarmvault init --profile` accepts `default`, `personal-research`, or a comma-separated preset list such as `reader,timeline`. For a custom vault style, edit the `profile` block in `swarmvault.config.json` directly; `swarmvault.schema.md` stays the human-written intent layer. The `personal-research` preset also enables `profile.guidedIngestDefault` and `profile.deepLintDefault`, so guided ingest/source and lint flows are on by default until you opt out with `--no-guide` or `--no-deep`.

For local semantic graph query without API keys, point `tasks.embeddingProvider` at an embedding-capable local backend such as Ollama, not `heuristic`.

With an embedding-capable provider available, SwarmVault can also merge semantic page matches into local search by default. `tasks.embeddingProvider` is the explicit way to choose that backend, but SwarmVault can also fall back to a `queryProvider` with embeddings support. Set `retrieval.rerank: true` when you want the configured `queryProvider` to rerank the merged top hits before answering.

Audio and video ingest use `tasks.audioProvider` when you configure a provider with `audio` capability. The fully-local option is `swarmvault provider setup --local-whisper --apply`, which installs a `local-whisper` provider, downloads a whisper.cpp ggml model into `~/.swarmvault/models/`, and assigns `tasks.audioProvider` so voice memos, meetings, interviews, and video audio transcribe with no API keys and no network calls. Local video needs `ffmpeg`; public video URL ingest with `--video` needs `yt-dlp`. YouTube transcript ingest works without a model provider. If you want to pin graph clustering instead of using the adaptive default and its oversized/low-cohesion community split pass, set `graph.communityResolution` in `swarmvault.config.json` or run `swarmvault graph cluster --resolution <n>` for one recompute.

Set `SWARMVAULT_OUT=<dir>` when generated `raw/`, `wiki/`, `state/`, `agent/`, and `inbox/` artifacts should be isolated from the source tree. Config and schema files remain in the project root, which keeps shared source worktrees clean while still giving agents the same vault contract.

`init`, `quickstart`, `scan`, and `clone` do not write project-local agent rule files by default. Run `swarmvault install --agent <agent> [--scope project|user]` for explicit installs, use `swarmvault install status --agent <agent>` for read-only status, or set `agents` in `swarmvault.config.json` and pass `--install-agent-rules` when you intentionally want configured targets installed together.

`swarmvault lint --deep --web` augments deep-lint findings with external evidence from a configured `webSearch` adapter. Web search is currently scoped to deep lint; compile, query, and explore stay on local vault state plus your configured LLM providers.

When the vault lives inside a git repo, `ingest`, `compile`, and `query` also accept `--commit` so generated `wiki/` and `state/` changes can be committed immediately. `compile --max-tokens <n>` trims lower-priority pages when you need bounded wiki output for a tighter context window.

Source-scoped artifacts are intentionally split by role:

| Artifact | Created by | Purpose |
|----------|-----------|---------|
| Source brief | `source add`, `ingest` (always) | Auto summary written to `wiki/outputs/source-briefs/` |
| Source review | `source review`, `source add --guide`, `ingest --review`, `ingest --guide` | Lighter staged assessment in `wiki/outputs/source-reviews/` |
| Source guide | `source guide`, `source add --guide`, `ingest --guide` | Guided walkthrough with approval-bundled updates in `wiki/outputs/source-guides/` |
| Source session | `source session`, `source add --guide`, `ingest --guide` | Resumable workflow state in `wiki/outputs/source-sessions/` and `state/source-sessions/` |

Supported non-code ingest includes `.pdf`, the full Word family (`.docx`, `.docm`, `.dotx`, `.dotm`), `.rtf`, `.odt`, `.odp`, `.ods`, `.epub`, `.csv`, `.tsv`, the full Excel family (`.xlsx`, `.xlsm`, `.xlsb`, `.xls`, `.xltx`, `.xltm`), the full PowerPoint family (`.pptx`, `.pptm`, `.potx`, `.potm`), `.ipynb` (Jupyter notebooks), `.bib` (BibTeX), `.org` (Org-mode), `.adoc`/`.asciidoc`, `.srt`, `.vtt`, Slack exports, `.eml`, `.mbox`, `.ics`, audio files (`.mp3`, `.wav`, `.m4a`, `.aac`, `.ogg`, `.webm`, and other `audio/*` inputs) through `tasks.audioProvider`, video files (`.mp4`, `.mov`, `.m4v`, `.mkv`, `.avi`, and other `video/*` inputs) through `ffmpeg` plus `tasks.audioProvider`, public video URLs with `--video` through `yt-dlp` plus `tasks.audioProvider`, direct YouTube transcript URLs, images (`.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`, `.bmp`, `.tif`, `.tiff`, `.svg`, `.ico`, `.heic`, `.heif`, `.avif`, `.jxl`), markdown/MDX/text notes, structured config/data (`.json`, `.jsonc`, `.json5`, `.yaml`, `.toml`, `.xml`, `.ini`, `.conf`, `.cfg`, `.env`, `.properties`) with schema hints, common developer manifests (`package.json`, `tsconfig.json`, `Cargo.toml`, `pyproject.toml`, `go.mod`, `go.sum`, `Dockerfile`, `Makefile`, `LICENSE`, `.gitignore`, `.editorconfig`, and similar) via content-sniffed text ingest so they are never silently dropped, browser clips, and research URLs captured through `swarmvault add`.

Supported code ingest covers `.js`, `.mjs`, `.cjs`, `.jsx`, `.ts`, `.mts`, `.cts`, `.tsx`, `.sh`, `.bash`, `.zsh`, `.py`, `.go`, `.rs`, `.java`, `.kt`, `.kts`, `.scala`, `.sc`, `.dart`, `.lua`, `.zig`, `.cs`, `.c`, `.cc`, `.cpp`, `.cxx`, `.h`, `.hh`, `.hpp`, `.hxx`, `.php`, `.rb`, `.ps1`, `.psm1`, `.psd1`, `.ex`, `.exs`, `.ml`, `.mli`, `.m`, `.mm`, `.res`, `.resi`, `.sol`, `.vue`, `.svelte`, `.jl`, `.v`, `.vh`, `.sv`, `.svh`, `.r`, `.R`, `.css`, `.html`, `.htm`, `.sql`, plus extensionless executable scripts with `#!/usr/bin/env node|python|ruby|bash|zsh` shebangs. Parser-backed local analysis extracts symbols, imports, local module references, dynamic JS/TS imports, Julia modules/types/functions, and Verilog/SystemVerilog modules/interfaces/packages/instantiations; SQL also emits table/view symbols plus read/write/join/reference graph edges. R emits an explicit parser diagnostic until a safe packaged grammar exists.

## What The Skill Package Includes

- `SKILL.md` - operational instructions for the model
- [`examples/quickstart.md`](examples/quickstart.md) - first-run setup flow
- [`examples/repo-workflow.md`](examples/repo-workflow.md) - repo ingest, compile, review, and graph workflow
- [`examples/graph-first-agent-workflow.md`](examples/graph-first-agent-workflow.md) - graph-first Claude Code onboarding, hook-enforced graph reads, and automatic refresh
- [`examples/research-workflow.md`](examples/research-workflow.md) - research capture and query workflow
- [`references/commands.md`](references/commands.md) - high-signal command cheat sheet
- [`references/artifacts.md`](references/artifacts.md) - what shows up under `raw/`, `wiki/`, and `state/`
- [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md) - common setup and runtime fixes
- [`validation/smoke-prompts.md`](validation/smoke-prompts.md) - release-validation prompts and expected outcomes

The published ClawHub package is intentionally text-only in this release.

## Core Workflow

1. Run `swarmvault next` when you need orientation before taking action.
2. Initialize the vault with `swarmvault init`.
3. Treat `swarmvault.schema.md` as the vault contract before serious compile or query work.
4. Use `swarmvault source add` when the input is a recurring local file, local directory, public GitHub repo root, or docs hub that should stay registered. Add `--branch`, `--ref`, or `--checkout-dir` for pinned public GitHub repo sources.
5. Add one-off material with `swarmvault ingest`, `swarmvault add`, or `swarmvault inbox import`.
6. Use `swarmvault ingest --guide`, `swarmvault source add --guide`, `swarmvault source reload --guide`, `swarmvault source guide <id>`, or `swarmvault source session <id>` when you want the stronger guided-session workflow. Set `profile.guidedIngestDefault: true` when guided mode should be the default for ingest/source commands, and use `--no-guide` to force the lighter path for a specific run. Profiles using `guidedSessionMode: "canonical_review"` stage approval-queued canonical page edits; `insights_only` profiles keep exploratory synthesis under `wiki/insights/`.
7. Compile with `swarmvault compile`, use `compile --max-tokens <n>` when the generated wiki must fit a bounded context window, or use `compile --approve` when the change should land in the approval queue first.
8. Inspect `wiki/`, `wiki/dashboards/`, and `state/` artifacts before broad re-search. When the vault lives inside git, `ingest|compile|query --commit` can commit those artifacts immediately after the run.
9. Use `swarmvault query`, `swarmvault chat`, `swarmvault context build`, `swarmvault export ai`, `swarmvault task`, `swarmvault memory`, `swarmvault explore`, `swarmvault review`, `swarmvault candidate`, and `swarmvault lint` to keep the vault current, portable, and reviewable. Set `profile.deepLintDefault: true` when `lint` should run the advisory deep pass by default, and use `--no-deep` to force a structural-only run.
10. Use `swarmvault doctor [--repair]` when the vault needs one health summary before deeper troubleshooting or handoff.
11. Use `swarmvault graph share --post` for a quick copyable summary, `swarmvault graph share --svg [path]` for a visual share card, `swarmvault graph share --bundle [dir]` for a portable share kit, `swarmvault graph blast` for reverse-import impact checks, `swarmvault graph cycles` for directed cycle checks, `swarmvault graph status [path]` or `swarmvault check-update [path]` for read-only graph freshness checks, `swarmvault graph stats` for lightweight counts and relation mix, `swarmvault graph validate [graph] --strict` before export/merge/push workflows, `swarmvault graph update [path] --force` or `swarmvault update [path] --force` only when a large graph shrink is expected, `swarmvault graph query "<seed>" --context calls --evidence extracted` for focused relation-aware traversal, `swarmvault graph tree` for an interactive source/module/symbol tree, `swarmvault graph merge <graph...> --out <path>` for combining SwarmVault or node-link JSON, `swarmvault graph cluster` or `swarmvault cluster-only` for graph community/report refresh without re-ingest, `swarmvault graph serve` for the live workspace, detailed health workbench, prioritized next actions, explicit capture modes, title/tag capture fields, budgeted agent handoffs, and bookmarklet clipper, `swarmvault graph export --report` for a self-contained HTML report, `swarmvault graph export --callflow <path>` for a directed relationship HTML view, `swarmvault graph export --neo4j <path>` for a Neo4j-ready Cypher import, other `swarmvault graph export` formats, `swarmvault graph push neo4j`, or `swarmvault mcp` when the vault needs to be explored or shared elsewhere.

## What SwarmVault Writes

- `SWARMVAULT_OUT` can relocate generated artifact directories while keeping config and schema at the project root
- `raw/sources/` and `raw/assets/` for canonical input storage
- `wiki/` for compiled source, concept, entity, code, graph, and output pages
- `wiki/outputs/source-briefs/` for recurring-source onboarding briefs
- `wiki/outputs/source-sessions/` for resumable guided session anchors
- `wiki/outputs/source-reviews/` for staged source-scoped review artifacts
- `wiki/outputs/source-guides/` for guided source integration artifacts
- `wiki/outputs/chat-sessions/` for persisted multi-turn chat transcripts
- `wiki/exports/ai/` for static AI handoff packs with `llms.txt`, full text, JSON-LD graph data, manifests, and per-page siblings
- `wiki/dashboards/` for recent sources, reading log, timeline, source sessions, source guides, research map, contradictions, and open questions
- `wiki/graph/share-card.md`, `wiki/graph/share-card.svg`, and `wiki/graph/share-kit/` for post-ready text, visual graph summaries, HTML preview, and JSON metadata generated on compile
- `wiki/context/` for markdown context-pack companions
- `wiki/memory/` for task ledger index and markdown task pages
- `wiki/candidates/` for staged concept/entity pages
- `state/graph.json` for the compiled graph
- `state/context-packs/` for saved JSON context packs with citations, token-budget accounting, included items, and omitted items
- `state/chat-sessions/` for structured resumable chat session state
- `state/memory/tasks/` for saved JSON task ledger records
- `state/retrieval/` for the local retrieval index and manifest
- `state/sources.json` plus `state/sources/<id>/` for managed-source registry state and working sync data
- `state/approvals/` for compile approval bundles
- `state/sessions/` and `state/jobs.ndjson` for saved run history

Generated guided artifacts and dashboards also carry Dataview-friendly fields such as `profile_presets`, `session_status`, `question_state`, `canonical_targets`, and `evidence_state` when you enable `profile.dataviewBlocks`.

## Agent And MCP Integration

Recommended per-repo onboarding for token-saving agent workflows:

```bash
cd <repo>
swarmvault init && swarmvault ingest .
swarmvault install --agent claude --hook --mcp --graph-first   # --graph-first opts in to search enforcement
swarmvault hook install        # git-hook refresh on commit/checkout (pass a repo path when the repo lives below the vault root)
```

For hook-capable agents, the installed hooks guide graph-first reads. The Claude Code hook injects graph-first instructions at session start — answer code-understanding questions with the plain `swarmvault graph query|explain|path` commands (avoid `--json`, which produces much larger output), `swarmvault query`, `swarmvault context build`, or `wiki/graph/report.md`, and read source files only when editing them — plus a graph staleness note. `swarmvault graph query "<seed>"` prints the top matches with page paths plus an inline excerpt of the best-matching wiki page, so one command usually answers where-is/what-calls questions without follow-up file reads. By default the hook is advisory: the first broad Grep/Glob/Bash search per session gets a one-time guidance note. Opt in to enforcement with `--graph-first` (persists `hooks.graphFirst: "deny"`), which denies that first search with the same guided redirect — repeating the search is then allowed, so work is never blocked. Either way the hook spawns a background `swarmvault graph update --file <path>` refresh after every Edit/Write. Searches scoped to vault artifact directories (`wiki/`, `raw/`, `state/`), single files, or search tools filtering piped output are never intercepted. `SWARMVAULT_GRAPH_FIRST=deny|context|off` overrides per session. The Codex, Gemini, Copilot, OpenCode, and Kilo hooks carry the same graph-first guidance with a session note plus a one-time search redirect appropriate to each tool's hook API.

`swarmvault install --agent claude --mcp` also registers the SwarmVault MCP server in the project's `.mcp.json` (`{"mcpServers":{"swarmvault":{"command":"swarmvault","args":["mcp"]}}}`). Claude installs additionally write a project skill bundle at `.claude/skills/swarmvault/SKILL.md`, and `--scope user` installs the skill, hook, and settings once under `~/.claude` for all repos — the hook no-ops in repos without a compiled graph report.

`swarmvault install --agent <agent>` also keeps the host project clean: in git repos the vault artifact directories are appended to `.gitignore`, strict-JSON `tsconfig.json` files get the artifact directories added to `"exclude"` so stored source copies under `raw/` do not break the host typecheck (commented JSONC tsconfigs are left untouched with a warning instead of a rewrite), and linter configs that still cover the artifact directories produce an advisory warning. Everything is skipped when `SWARMVAULT_OUT` keeps artifacts outside the repo.

Supported agent installs:

- `swarmvault install --agent codex --hook`
- `swarmvault install --agent claude --hook --mcp`
- `swarmvault install --agent cursor`
- `swarmvault install --agent gemini --hook`
- `swarmvault install --agent opencode --hook`
- `swarmvault install --agent aider`
- `swarmvault install --agent copilot --hook`
- `swarmvault install --agent trae`
- `swarmvault install --agent claw`
- `swarmvault install --agent droid`
- `swarmvault install --agent kiro`
- `swarmvault install --agent kilo --hook`
- `swarmvault install --agent hermes`
- `swarmvault install --agent antigravity`
- `swarmvault install --agent vscode`
- `swarmvault install --agent amp`
- `swarmvault install --agent augment`
- `swarmvault install --agent adal`
- `swarmvault install --agent bob`
- `swarmvault install --agent cline`
- `swarmvault install --agent codebuddy`
- `swarmvault install --agent command-code`
- `swarmvault install --agent continue`
- `swarmvault install --agent cortex`
- `swarmvault install --agent crush`
- `swarmvault install --agent deepagents`
- `swarmvault install --agent devin`
- `swarmvault install --agent firebender`
- `swarmvault install --agent iflow`
- `swarmvault install --agent junie`
- `swarmvault install --agent kilo-code`
- `swarmvault install --agent kimi`
- `swarmvault install --agent kode`
- `swarmvault install --agent mcpjam`
- `swarmvault install --agent mistral-vibe`
- `swarmvault install --agent mux`
- `swarmvault install --agent neovate`
- `swarmvault install --agent openclaw`
- `swarmvault install --agent openhands`
- `swarmvault install --agent pochi`
- `swarmvault install --agent qoder`
- `swarmvault install --agent qwen-code`
- `swarmvault install --agent replit`
- `swarmvault install --agent roo-code`
- `swarmvault install --agent trae-cn`
- `swarmvault install --agent warp`
- `swarmvault install --agent windsurf`
- `swarmvault install --agent zencoder`

Expose the vault over MCP with:

```bash
swarmvault mcp
```

The MCP surface includes graph stats, read-only graph freshness (`graph_status`), symbol caller lookup with file:line call-site evidence (`graph_callers`), code-only graph refresh (`update_graph`, with an optional files array for per-file refreshes), graph clustering refresh, community lookup, hyperedges, context-pack build/read/list, task start/update/finish/list/read/resume, compatibility memory task, `doctor_vault`, and retrieval status/rebuild/doctor tools so host agents can request bounded evidence, keep a durable task ledger, keep the graph current after edits, and inspect vault health without shelling out to the CLI.

## Links

- Docs: https://www.swarmvault.ai/docs
- Providers: https://www.swarmvault.ai/docs/providers
- Troubleshooting: https://www.swarmvault.ai/docs/getting-started/troubleshooting
- npm: https://www.npmjs.com/package/@swarmvaultai/cli
- GitHub: https://github.com/swarmclawai/swarmvault
