---
name: swarmvault
description: "Use SwarmVault when the user needs a local-first knowledge vault that writes durable markdown, graph, search, dashboard, review, chat-session, context-pack, task-ledger, static AI export, retrieval, and MCP artifacts to disk from books, notes, transcripts, exports, datasets, slide decks, files, URLs, code, and recurring source workflows."
version: "3.21.0"
metadata: '{"openclaw":{"requires":{"anyBins":["swarmvault","vault"]},"install":[{"id":"node","kind":"node","package":"@swarmvaultai/cli","bins":["swarmvault","vault"],"label":"Install SwarmVault CLI (npm)"}],"emoji":"🗃️","homepage":"https://www.swarmvault.ai/docs"}}'
---

# SwarmVault

Use this skill when the user wants a local-first knowledge vault built on the [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) pattern — three layers (raw sources, wiki, schema) where the LLM maintains a durable wiki between you and raw sources. Also use it when the project already contains `swarmvault.config.json` or `swarmvault.schema.md`.

For onboarding, examples, command references, or troubleshooting, read the bundled `README.md`, `examples/`, `references/`, and `TROUBLESHOOTING.md` before improvising workflow advice.

## Quick checks

- Work from the vault root.
- Use `swarmvault next` when you need a read-only orientation command before deciding whether to initialize, ingest, compile, query, review, or refresh.
- If the vault does not exist yet, run `swarmvault init`.
- Use `swarmvault demo --no-serve` when the user wants the fastest zero-config walkthrough before pointing SwarmVault at their own sources.
- Use `swarmvault quickstart <file-or-directory-or-github-url>` as the beginner-friendly first-run path when the user wants init + ingest + compile + graph viewer in one command.
- Use `swarmvault scan <file-or-directory-or-github-url> --no-serve`, `swarmvault scan <file-or-directory-or-github-url> --no-viz`, or `swarmvault clone <file-or-directory-or-github-url> --no-viz` when the user wants the fastest scratch pass over a local file, local repo, public GitHub repo, or docs tree without manually stepping through init + ingest + compile first; for GitHub URLs add `--branch`, `--ref`, or `--checkout-dir` when the user needs a pinned checkout. Use `scan --mcp` or `clone --mcp` when the next step should be an MCP stdio server. Use `swarmvault graph share --post` for copyable text, `swarmvault graph share --svg [path]` for a visual card, or `swarmvault graph share --bundle [dir]` for a portable folder with markdown, post text, SVG, HTML preview, and JSON metadata.
- Use `swarmvault context build "<goal>" --target <path-or-node> --budget <tokens>` when the next agent, review, or handoff needs a bounded evidence pack instead of a broad vault search.
- Use `swarmvault chat "question"` when a multi-turn conversation should survive handoff; resume with `swarmvault chat --resume <id> "follow-up"` and inspect saved transcripts under `wiki/outputs/chat-sessions/`.
- Use `swarmvault export ai --out <dir>` when another agent, crawler, or static workflow needs `llms.txt`, full text, JSON-LD graph data, a manifest, and per-page siblings without starting `graph serve`.
- Use `swarmvault task start "<goal>" --target <path-or-node>` when agent work should leave a durable task ledger with decisions, linked context packs, changed paths, outcomes, and follow-ups. The older `memory` command remains a compatibility alias.
- Use `swarmvault doctor` before broad troubleshooting or agent handoff; add `--repair` when the retrieval index can be safely rebuilt. In `swarmvault graph serve`, the workbench shows prioritized next actions, every doctor check with details, copyable suggested commands, and safe direct repair where available.
- Read `swarmvault.schema.md` before compile or query work. It is the vault's operating contract.
- If `wiki/graph/report.md` exists, use it before broad repo search.
- If `SWARMVAULT_OUT` is set, resolve generated artifacts from that output root: `raw/`, `wiki/`, `state/`, `agent/`, and `inbox/` live there while `swarmvault.config.json` and `swarmvault.schema.md` stay in the project root.

## Core loop

1. Run `swarmvault next` when the current vault state is unclear; it is read-only and returns paths, checks, and recommended commands.
2. Initialize a vault with `swarmvault init` when needed.
3. Update `swarmvault.schema.md` before a serious compile. Use it for naming rules, categories, grounding, freshness expectations, and exclusions.
4. Use `swarmvault source add <input>` when the input is a recurring local file, local directory, public GitHub repo root, or docs hub that should stay registered. For public GitHub repos, use `--branch`, `--ref`, or `--checkout-dir` when a branch, tag, commit, or reusable checkout matters.
5. Ingest one-off inputs with `swarmvault ingest <path-or-url>`, or ingest a whole repo tree with `swarmvault ingest <directory>`. Audio and video files use `tasks.audioProvider` when configured; local video needs `ffmpeg`, public video URLs use `swarmvault ingest --video <url>` / `swarmvault add --video <url>` with `yt-dlp`, and supported YouTube URLs go through direct transcript capture instead of generic URL ingest.
6. Use `swarmvault ingest --guide`, `swarmvault source add --guide`, `swarmvault source reload --guide`, `swarmvault source guide <id>`, or `swarmvault source session <id>` when the human should integrate one source at a time before canonical pages change. Set `profile.guidedIngestDefault: true` in `swarmvault.config.json` to make guided mode the default; use `--no-guide` to override. Profiles using `guidedSessionMode: "canonical_review"` stage approval-queued canonical edits; `insights_only` profiles keep exploratory synthesis in `wiki/insights/`. Use `--review` only for the lighter review-only path.
7. Use `swarmvault inbox import` for capture-style batches, then `swarmvault watch --lint --repo` when the workflow should stay automated. Add `--code-only` when the refresh should stay AST-only and defer non-code semantic re-analysis to a later `compile`. On tracked repos, code-only changes take that faster compile path automatically. Install `swarmvault hook install` when git checkouts and commits should trigger the same repo-aware code-only refresh automatically.
8. Compile with `swarmvault compile`, use `compile --max-tokens <n>` when the generated wiki must stay inside a bounded context budget, or use `compile --approve` when changes should go through the local review queue first.
9. Resolve staged work with `swarmvault review list|show|accept|reject` and `swarmvault candidate list|promote|archive`.
10. Ask questions with `swarmvault query "<question>"`. It saves durable answers into `wiki/outputs/` by default; add `--no-save` only for ephemeral checks. When an embedding provider is configured, query can merge semantic page matches into local search; `retrieval.rerank: true` lets the current `queryProvider` rerank the merged top hits before answering.
11. Use `swarmvault chat "question"` for a persisted multi-turn conversation over the compiled wiki, then resume or manage it with `swarmvault chat --resume <id>`, `chat --list`, and `chat --delete <id>`.
12. Build agent handoff bundles with `swarmvault context build "<goal>" --target <path-or-node> --budget <tokens>`. Use `--format markdown|json|llms` for the printed shape, and inspect `swarmvault context list|show|delete` for saved packs.
13. Start a task ledger with `swarmvault task start "<goal>" --target <path-or-node>`, update it with `swarmvault task update <id> --note|--decision|--changed-path|--context-pack`, finish it with `swarmvault task finish <id> --outcome <text>`, and use `swarmvault task resume <id> --format markdown|json|llms` for the next-agent handoff. `query`, `explore`, and `context build` can attach work with `--task <id>`; `--memory <id>` remains a compatibility alias.
14. Run `swarmvault export ai --out <dir>` when the compiled wiki should be handed to another agent or static crawler as `llms.txt`, full text, JSON-LD, manifest metadata, and per-page `.txt`/`.json` siblings.
15. Run `swarmvault doctor [--repair]` when the vault needs one health summary across graph, retrieval, review queues, watch state, migrations, managed sources, and task state before deeper troubleshooting.
16. Use `swarmvault explore "<question>" --steps <n>` for save-first multi-step research loops, or `--format report|slides|chart|image` when the artifact should be presentation-oriented.
17. Run `swarmvault lint` whenever the schema changed, artifacts look stale, or compile/query results drift. Set `profile.deepLintDefault: true` in `swarmvault.config.json` when the advisory deep-lint pass should be the default, and use `--no-deep` when you need a structural-only run. Add `--web` only when deep lint is enabled and a `webSearch.tasks.deepLintProvider` adapter is configured; web evidence is scoped to deep lint and does not change compile or query behavior.
18. Use `swarmvault mcp` when another agent or tool should browse, search, query, build context packs, manage tasks, and inspect vault or retrieval health from the vault through MCP.
19. Use `swarmvault graph share --post` when the user needs a quick copyable summary, `swarmvault graph share --svg [path]` when they need a 1200x630 visual card, `swarmvault graph share --bundle [dir]` when they need a portable share kit for posting, linking, or screenshotting, `swarmvault graph blast <target>` when they want reverse-import impact analysis, `swarmvault graph callers <symbol>` when they need every caller of a symbol from graph call edges with exact file:line call-site evidence, `swarmvault graph cycles` when they need directed cycle checks, `swarmvault graph status [path]` or `swarmvault check-update [path]` when they need a read-only stale check before deciding between `graph update` and `compile`, `swarmvault graph stats` when they need lightweight counts and relation mix, `swarmvault graph validate [graph] --strict` when a graph artifact should be checked before export, merge, push, or publish workflows, `swarmvault graph update [path] --force` or `swarmvault update [path] --force` only when a large node/edge shrink is expected, `swarmvault watch [path] --once --code-only` when one repo root should be refreshed without writing watch config, `swarmvault graph query "<seed>" --context calls --evidence extracted` when traversal should focus on relation groups, evidence classes, node types, or languages, `swarmvault graph tree [--output <html>]` or `swarmvault tree [--output <html>]` when they need an interactive source/module/symbol tree with a node inspector, `swarmvault graph merge <graph...> --out <path>` or `swarmvault merge-graphs <graph...> --out <path>` when they need to combine SwarmVault or node-link graph JSON, `swarmvault graph cluster [--resolution <n>]` or `swarmvault cluster-only [vault]` when they need communities and graph report artifacts recomputed without re-ingest, `swarmvault graph serve` when the live workspace, health workbench, Memory dashboard, or bookmarklet clipper will help, `swarmvault diff` when they need a graph-level change summary against the last committed baseline, or `swarmvault graph export --html <output>` / `graph export --report <output>` / `graph export --callflow <output>` when richer sharing will help. The live workbench exposes prioritized next actions, explicit capture modes, title/tag capture fields, context-pack/task token budgets, and action receipts; the bookmarklet sends page titles and selected text into the same capture path. `graph export` also supports `--html-standalone`, `--json`, `--obsidian`, `--canvas`, and `--neo4j` for lighter, Obsidian-native, or Neo4j-ready sharing.

## Graph-first code reads

When a compiled vault exists for a codebase (`wiki/graph/report.md` is present), answer code-understanding questions from the graph instead of reading or grepping source files — it returns condensed, evidence-backed answers in far fewer tokens:

- "Where is X / what calls Y / how is Z structured" → `swarmvault graph query "<seed>"`, `swarmvault graph explain "<node>"`, `swarmvault graph path "<a>" "<b>"`. Use the plain output: `graph query` prints the top matches with page paths plus an inline excerpt of the best-matching wiki page, so one command usually answers these questions without follow-up file reads. Avoid `--json` here — it produces much larger output.
- "Who calls X / impact of changing X" → `swarmvault graph callers <symbol>` lists every caller from graph call edges with exact file:line call-site evidence, scanning only the files the graph identifies as callers — use it instead of repo-wide grep for who-calls and impact-of-change questions. `swarmvault graph blast <target>` adds module-level reverse-import impact.
- Open questions over the whole codebase → `swarmvault query "<question>"`.
- Bounded handoff context → `swarmvault context build "<goal>" --target <path> --budget <tokens>`.
- Read source files directly only when editing them or when the graph lacks the needed detail.
- Check freshness with `swarmvault graph status`; refresh with `swarmvault graph update`, or `swarmvault graph update --file <path>` for just-edited files.
- Installed agent hooks default to advisory mode: a one-time guidance note on the first broad search, plus an automatic background single-file refresh after edits. Enforcement (the first broad Grep/Glob/Bash search per session is denied with a redirect to the graph; repeating the search is allowed) is opt-in — install with `--graph-first`, or set `hooks.graphFirst: "deny"` in `swarmvault.config.json`. `SWARMVAULT_GRAPH_FIRST=deny|context|off` overrides per session; search tools that filter piped output are never intercepted.

## Working rules

- Prefer changing the schema before re-running compile when organization or grounding is wrong.
- Treat `wiki/` and `state/` as first-class outputs. Inspect them instead of trusting a single chat answer.
- Use saved chat transcripts and static AI exports as durable handoff artifacts when the user asks for continuity across sessions or tools.
- Prefer `wiki/graph/report.md`, `state/graph.json`, and saved wiki pages over ad hoc broad search when they already exist.
- Use `swarmvault graph status [path]` or `swarmvault check-update [path]` before refreshing a tracked repo when you need to know whether a code-only `graph update`/`update` is enough or a full `compile` is required.
- Use `swarmvault graph validate [graph] --strict` before sharing, merging, pushing, or publishing graph artifacts when reference integrity matters.
- Use `source add` for recurring files, directories, public GitHub repo roots, and docs hubs. Use `ingest` and `add` for deliberate one-off inputs.
- When the vault lives in a git repo, `ingest|compile|query --commit` can commit `wiki/` and `state/` changes immediately after the run.
- The default heuristic provider is a valid local/offline starting point. Add a model provider only when the user wants richer synthesis quality or optional capabilities such as embeddings, vision, image generation, or audio transcription. The recommended fully-local setup is Ollama + Gemma: `ollama pull gemma4` then set `providers.llm` to `{ type: "ollama", model: "gemma4" }` and point `tasks.compileProvider`, `tasks.queryProvider`, and `tasks.lintProvider` at it. Use `swarmvault provider add|list|show|remove` when provider routing should be updated without hand-editing config.
- Audio and video ingest need `tasks.audioProvider` to resolve to a provider that exposes `audio` capability. For a fully local setup, run `swarmvault provider setup --local-whisper --apply` — installs the `local-whisper` provider, downloads a whisper.cpp ggml model into `~/.swarmvault/models/`, and points `tasks.audioProvider` at it. Local video also needs `ffmpeg`; public video URL ingest with `--video` needs `yt-dlp`. YouTube transcript ingest does not need a provider. Set `graph.communityResolution` when the user wants to pin community clustering instead of using the adaptive default and oversized/low-cohesion split pass, or run `swarmvault graph cluster --resolution <n>` for a one-off recompute.
- If an OpenAI-compatible backend cannot satisfy structured generation, reduce its declared capabilities instead of forcing every task through it.
- Keep raw sources immutable. Put corrections in schema, new sources, or saved outputs rather than manually rewriting generated provenance.

## Files and artifacts

- `swarmvault.schema.md`: vault-specific compile and query rules.
- `SWARMVAULT_OUT`: optional output root for generated artifact directories. When set, `raw/`, `wiki/`, `state/`, `agent/`, and `inbox/` are resolved under that directory.
- `raw/sources/` and `raw/assets/`: canonical source storage.
- `wiki/`: generated pages plus saved outputs.
- `wiki/outputs/source-briefs/`: saved onboarding briefs for managed sources.
- `wiki/outputs/source-sessions/`: resumable guided-session anchors plus question/answer history for one-source-at-a-time integration.
- `wiki/outputs/source-reviews/`: staged source-scoped review pages.
- `wiki/outputs/source-guides/`: staged source-integration guides for one-source-at-a-time workflows.
- `wiki/outputs/chat-sessions/`: persisted markdown transcripts for `swarmvault chat`.
- `wiki/dashboards/`: recent sources, reading log, timeline, source sessions, source guides, research map, contradiction, and open-question dashboards.
- `wiki/graph/share-card.md`, `wiki/graph/share-card.svg`, and `wiki/graph/share-kit/`: post-ready text, visual graph summaries, and a portable HTML-preview share bundle generated on compile.
- `wiki/exports/ai/`: default static AI handoff export with `llms.txt`, `llms-full.txt`, `graph.jsonld`, `manifest.json`, `ai-readme.md`, and optional per-page siblings.
- `wiki/context/`: markdown context-pack companions for agent kickoff, PR review, and handoff.
- `wiki/memory/`: task ledger index and markdown task pages.
- `wiki/code/`: module pages for ingested JavaScript, JSX, TypeScript (including `.mts`/`.cts`), TSX, Bash/shell script (with shebang-based detection for extensionless scripts), Python, Go, Rust, Java, Kotlin, Scala, Dart, Lua, Zig, C#, C, C++ (including `.c`/`.cc`/`.cpp`/`.cxx` and `.h`/`.hh`/`.hpp`/`.hxx`), PHP, Ruby, PowerShell (`.ps1`/`.psm1`/`.psd1`), Elixir (`.ex`/`.exs`), OCaml (`.ml`/`.mli`), Objective-C (`.m`/`.mm`), ReScript (`.res`/`.resi`), Solidity (`.sol`), Vue single-file components (`.vue`), Svelte single-file components (`.svelte`), HTML (`.html`/`.htm`), CSS, Julia (`.jl`), Verilog/SystemVerilog (`.v`/`.vh`/`.sv`/`.svh`), R (`.r`/`.R`), and SQL (`.sql`) sources. Julia and Verilog/SystemVerilog use packaged WASM grammars; JS/TS capture static and dynamic imports; SQL adds table/view symbols plus read/write/join/reference graph edges; R emits an explicit diagnostic until a safe packaged parser exists.
- `state/extracts/`: extracted markdown and JSON sidecars for PDF, the full Word family (`.docx`/`.docm`/`.dotx`/`.dotm`), RTF (`.rtf`), OpenDocument (ODT/ODP/ODS), EPUB, CSV/TSV, the full Excel family (`.xlsx`/`.xlsm`/`.xlsb`/`.xls`/`.xltx`/`.xltm`), the full PowerPoint family (`.pptx`/`.pptm`/`.potx`/`.potm`), Jupyter notebooks (`.ipynb`), BibTeX (`.bib`), Org-mode (`.org`), AsciiDoc (`.adoc`/`.asciidoc`), transcripts, Slack exports, email, calendar, audio transcripts, video transcripts, YouTube transcript captures, and image sources (`.png`/`.jpg`/`.jpeg`/`.gif`/`.webp`/`.bmp`/`.tif`/`.tiff`/`.svg`/`.ico`/`.heic`/`.heif`/`.avif`/`.jxl`), plus structured previews for config/data files (JSON/JSONC/JSON5/TOML/YAML/XML/INI/ENV/PROPERTIES/CFG/CONF) and content-sniffed text ingest for developer manifests (`package.json`, `Cargo.toml`, `go.mod`, `LICENSE`, `.gitignore`, `Dockerfile`, `Makefile`, and similar plaintext files).
- `state/code-index.json`: repo-aware code aliases and local import resolution data.
- `wiki/projects/`: project rollups over canonical pages.
- `wiki/candidates/`: staged concept and entity pages awaiting promotion.
- `state/graph.json`: compiled graph.
- `state/context-packs/`: saved JSON context-pack artifacts with citations, token-budget accounting, included items, and omitted items.
- `state/chat-sessions/`: saved structured chat state for resumable wiki conversations.
- `state/memory/tasks/`: saved JSON task ledger records with decisions, changed paths, outcomes, and follow-ups.
- `state/retrieval/`: local retrieval index, SQLite FTS shard, and manifest.
- `state/sources.json` and `state/sources/<id>/`: managed-source registry entries plus working sync state.
- `state/approvals/`: staged review bundles from `compile --approve`.
- `state/sessions/`: canonical session artifacts for compile, query, explore, lint, watch, review, and candidate actions.
- `state/jobs.ndjson`: watch-mode run log.

## Agent integration

- `swarmvault install --agent codex|claude|cursor|goose|pi|gemini|opencode|aider|copilot|trae|claw|droid|kiro|kilo|hermes|antigravity|vscode|amp|augment|adal|bob|cline|codebuddy|command-code|continue|cortex|crush|deepagents|devin|firebender|iflow|junie|kilo-code|kimi|kode|mcpjam|mistral-vibe|mux|neovate|openclaw|openhands|pochi|qoder|qwen-code|replit|roo-code|trae-cn|warp|windsurf|zencoder` installs agent-specific rules into the current project. Agents in the extended roster receive a project-level skill bundle at the tool's conventional skills directory.
- `swarmvault init`, `quickstart`, `scan`, and `clone` leave project-local agent rule files alone by default. Use `install --agent` explicitly, or set `agents` in `swarmvault.config.json` and pass `--install-agent-rules` to initialization or scan commands when configured installs are intentional.
- `swarmvault install --agent codex|claude|opencode|gemini|copilot|kilo --hook` installs graph-first hook or plugin support for the agents that expose project hook APIs. For Claude Code the hook surfaces staleness at session start, nudges the first broad search per session toward graph commands, and refreshes the graph in the background after edits; add `--graph-first` to opt in to search enforcement (persists `hooks.graphFirst: "deny"`). Use `swarmvault install status --agent <agent> [--hook] [--mcp]` to inspect expected files without writing.
- `swarmvault install --agent claude --mcp` also registers the SwarmVault MCP server in the project's `.mcp.json`; `swarmvault install --agent claude --hook --scope user` installs the skill, hook, and settings once under `~/.claude` for all repos (the hook no-ops in repos without a compiled graph report).
- `swarmvault install --agent <agent>` also keeps the host project clean: in git repos the vault artifact directories are appended to `.gitignore`, strict-JSON `tsconfig.json` files get the artifact directories added to `"exclude"` so stored source copies under `raw/` do not break the host typecheck (commented JSONC tsconfigs are left untouched with a warning), and linter configs that still cover the artifact directories produce an advisory warning. All hygiene edits are skipped when `SWARMVAULT_OUT` keeps artifacts outside the repo.
- `swarmvault install --agent aider` installs `CONVENTIONS.md` and wires `.aider.conf.yml` to read it when that config is valid YAML.
- `swarmvault install --agent antigravity` writes `.agents/rules/swarmvault.md` and `.agents/workflows/swarmvault.md`; reinstall removes older fully managed `.agent/` files.
- `swarmvault mcp` exposes tools and resources for page search, page reads, source listing, graph stats, graph status, symbol caller lookup with call-site evidence (`graph_callers`), code-only graph updates (optionally per-file), graph clustering refresh, community lookup, hyperedges, query, context-pack build/read/list, task start/update/finish/list/read/resume, compatibility memory tasks, vault doctor, retrieval status/rebuild/doctor, ingest, compile, and lint.

## Defaults to preserve

- Keep raw source material immutable under `raw/`.
- Save useful answers unless the user explicitly wants ephemeral output.
- Prefer reviewable flows such as `compile --approve`, `review`, and `candidate` when a change should not activate silently.
- Treat provider setup as part of serious vault operation. If only `heuristic` is configured, say so clearly.
- When a vault uses the `profile` block in `swarmvault.config.json`, respect it as the deterministic behavior layer. `swarmvault.schema.md` still defines the human intent layer.
