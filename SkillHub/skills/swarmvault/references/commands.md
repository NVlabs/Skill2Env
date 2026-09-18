# Command Reference

## Setup

```bash
swarmvault demo --no-serve
swarmvault quickstart ./apps/api
swarmvault quickstart ./docs/manual.pdf --no-serve
swarmvault next
swarmvault quickstart ./apps/api --no-serve
swarmvault init
swarmvault init --obsidian --profile personal-research
swarmvault init --obsidian --profile reader,timeline
swarmvault scan ./apps/api --no-serve
swarmvault scan ./apps/api --no-viz
swarmvault clone https://github.com/owner/repo --branch main --no-viz
swarmvault clone https://github.com/owner/repo --mcp
swarmvault --version
```

## Ingest and Capture

```bash
swarmvault source add https://github.com/karpathy/micrograd
swarmvault source add ./exports/customer-call.srt --guide
swarmvault source session <source-id-or-session-id>
swarmvault source list
swarmvault source reload --all
swarmvault source review <source-id>
swarmvault source guide <source-id>
swarmvault source delete <source-id>
swarmvault ingest <path-or-url>
swarmvault ingest ./customer-call.mp3
swarmvault ingest https://www.youtube.com/watch?v=dQw4w9WgXcQ
swarmvault ingest --video https://example.com/product-demo.mp4
swarmvault ingest <path-or-url> --commit
swarmvault ingest <path-or-url> --guide
swarmvault ingest <directory> --repo-root .
swarmvault add <url-or-doi-or-arxiv-id>
swarmvault inbox import <path>
```

## Compile, Query, Review

```bash
swarmvault compile
swarmvault compile --max-tokens 120000
swarmvault compile --approve
swarmvault diff
swarmvault query "<question>"
swarmvault query "<question>" --commit
swarmvault chat "What should the next agent know?"
swarmvault chat --resume <session-id> "What changed?"
swarmvault chat --list
swarmvault chat --delete <session-id>
swarmvault context build "<goal>" --target ./src --budget 8000
swarmvault context build "<goal>" --target concept:auth --format llms
swarmvault context list
swarmvault context show <context-pack-id>
swarmvault task start "<goal>" --target ./src --agent codex
swarmvault task update <task-id> --decision "Keep the change local-first"
swarmvault task update <task-id> --changed-path packages/engine/src/memory.ts
swarmvault task finish <task-id> --outcome "Task completed" --follow-up "Run release smoke"
swarmvault task resume <task-id> --format llms
swarmvault retrieval status
swarmvault retrieval doctor --repair
swarmvault doctor
swarmvault doctor --repair
swarmvault explore "<question>" --steps 3
swarmvault lint
swarmvault lint --conflicts
swarmvault review list
swarmvault review show <approval-id> --diff
swarmvault review accept <approval-id>
swarmvault candidate list
```

## Graph and Sharing

```bash
swarmvault graph serve
swarmvault graph serve --full
swarmvault graph share --post
swarmvault graph share --svg ./share-card.svg
swarmvault graph share --bundle ./share-kit
swarmvault graph blast ./src/index.ts
swarmvault graph callers "chargeCustomer"
swarmvault graph status ./src
swarmvault check-update ./src
swarmvault graph stats
swarmvault graph cycles
swarmvault graph validate --strict
swarmvault graph cluster
swarmvault cluster-only
swarmvault graph update ./src
swarmvault update ./src
swarmvault graph update --file ./src/auth.ts --file ./src/db.ts
swarmvault graph update ./src --force
swarmvault graph refresh
swarmvault graph query "auth calls" --context calls --evidence extracted --language typescript
swarmvault graph tree --output ./tree.html
swarmvault tree --output ./tree.html
swarmvault graph merge ./graph.json ./other-graph.json --out ./merged-graph.json
swarmvault merge-graphs ./graph.json ./other-graph.json --out ./merged-graph.json
swarmvault graph export --html ./graph.html
swarmvault graph export --report ./graph-report.html
swarmvault graph export --html ./graph.html --full
swarmvault graph export --html-standalone ./graph-standalone.html
swarmvault graph export --callflow ./callflow.html
swarmvault graph export --json ./graph.json --canvas ./graph.canvas
swarmvault graph export --obsidian ./graph-vault
swarmvault graph export --neo4j ./graph.cypher
swarmvault export ai --out ./exports/ai
swarmvault export ai --out ./exports/ai --no-page-siblings
swarmvault graph push neo4j --dry-run
swarmvault mcp
```

## Providers

```bash
swarmvault provider add router --type openrouter --model openrouter/auto --api-key-env OPENROUTER_API_KEY --capability chat --capability structured --task queryProvider
swarmvault provider list
swarmvault provider show router
swarmvault provider remove router --fallback local
swarmvault provider setup --local-whisper --apply
```

## Automation

```bash
swarmvault watch --lint --repo
swarmvault watch --repo --code-only --once
swarmvault graph status .
swarmvault check-update .
swarmvault watch ./src --once --code-only
swarmvault graph validate --strict
swarmvault graph update .
swarmvault update .
swarmvault graph update --file packages/engine/src/index.ts
swarmvault graph update . --force
swarmvault watch status
swarmvault hook install
swarmvault hook install packages/app   # repo below the vault root
swarmvault schedule list
swarmvault schedule run <job-id>
```

## Agent Installs

```bash
swarmvault install --agent codex --hook
swarmvault install --agent claude --hook
swarmvault install --agent claude --hook --mcp
swarmvault install --agent claude --hook --mcp --graph-first
swarmvault install --agent claude --hook --scope user
swarmvault install --agent gemini --hook
swarmvault install --agent opencode --hook
swarmvault install --agent aider
swarmvault install --agent copilot --hook
swarmvault install --agent trae
swarmvault install --agent claw
swarmvault install --agent droid
swarmvault install --agent kilo --hook
swarmvault install --agent devin
swarmvault install status --agent kilo --hook
swarmvault install status --agent claude --hook --mcp
```

The Claude Code hook guides graph-first reads: session-start graph instructions plus a staleness note, a one-time advisory note on the first broad Grep/Glob/Bash search per session, and a background `swarmvault graph update --file <path>` refresh after Edit/Write. Add `--graph-first` to opt in to enforcement (the first broad search is denied once with a guided redirect; repeating the search is allowed) — it persists `hooks.graphFirst: "deny"` in `swarmvault.config.json`, and `SWARMVAULT_GRAPH_FIRST=deny|context|off` overrides per session. `--mcp` registers the MCP server in the project `.mcp.json`; `--scope user` installs the Claude skill, hook, and settings under `~/.claude`.
