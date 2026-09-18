# Quickstart Example

Use this when the user needs the shortest path from install to a working vault.

## Commands

```bash
npm install -g @swarmvaultai/cli
swarmvault quickstart ./repo
swarmvault quickstart ./notes.pdf --no-serve
swarmvault next
swarmvault quickstart ./repo --no-serve
swarmvault demo --no-serve
swarmvault init --obsidian
swarmvault scan ./repo --no-serve
swarmvault scan ./repo --no-viz
swarmvault clone https://github.com/owner/repo --branch main --no-viz
swarmvault source add https://github.com/karpathy/micrograd
swarmvault source add https://github.com/owner/repo --branch main --checkout-dir .swarmvault-checkouts/repo
swarmvault diff
swarmvault graph share --post
swarmvault graph share --svg ./share-card.svg
swarmvault graph share --bundle ./share-kit
swarmvault graph blast ./src/index.ts
swarmvault graph status ./src
swarmvault check-update ./src
swarmvault graph stats
swarmvault graph validate --strict
swarmvault update ./src
swarmvault graph cluster
swarmvault cluster-only
swarmvault graph tree --output ./tree.html
swarmvault tree --output ./tree.html
swarmvault graph query "auth calls" --context calls --evidence extracted --language typescript
swarmvault query "What are the key concepts?"
swarmvault context build "Explain the key concepts to the next agent" --target ./repo --budget 8000
swarmvault task start "Explain the key concepts to the next agent" --target ./repo --agent codex
swarmvault retrieval status
swarmvault doctor
swarmvault graph serve
swarmvault graph export --report ./graph-report.html
swarmvault graph export --neo4j ./graph.cypher
swarmvault merge-graphs ./graph.json ./other-graph.json --out ./merged-graph.json
swarmvault chat "What should the next agent know?"
swarmvault chat --resume <session-id> "What changed?"
swarmvault export ai --out ./exports/ai
```

## What To Check

- `swarmvault.schema.md` exists and reflects the vault contract
- `swarmvault next` reports `uninitialized`, `initialized`, or `compiled` and recommends the next safe command without changing files
- `demo --no-serve` leaves a temporary compiled vault behind even on a clean machine
- `quickstart`, `quickstart --no-serve`, `scan --no-serve`, `scan --no-viz`, and `clone --no-viz` accept local files as well as directories and leave a compiled vault behind even when the viewer is not launched
- `quickstart`, `scan`, and `clone` do not create project-local agent rule files unless `--install-agent-rules` is passed with configured agents
- `state/sources.json` contains the managed source registry entry
- `wiki/graph/report.md` exists after compile
- `graph status` and `check-update` report whether tracked repo changes need `graph update`/`update` or a full `compile` without writing watch state
- `watch [path] --once --code-only` can refresh one repo root without persisting watch config
- `graph stats` prints lightweight graph counts and relation mix without opening the viewer
- `graph validate --strict` checks graph artifact integrity before export, merge, push, or publish workflows
- `graph cluster` and `cluster-only` refresh graph communities and report artifacts from the existing graph without another ingest
- `graph query` can focus traversal with relation/context/evidence/node/language filters
- `graph tree` and `tree` write an interactive source/module/symbol HTML tree with a node inspector when the user wants file-oriented browsing
- `graph merge` and `merge-graphs` combine SwarmVault or node-link graph JSON artifacts
- `wiki/graph/share-card.md`, `wiki/graph/share-card.svg`, and `wiki/graph/share-kit/` exist after compile; `graph share --post` prints copyable text, `graph share --svg [path]` writes the visual card, and `graph share --bundle [dir]` writes the portable share kit
- `graph export --report` writes a shareable HTML report when the user wants a lighter artifact than the full workspace; `graph export --neo4j` writes a Cypher import file for Neo4j workflows
- `wiki/outputs/source-briefs/` contains a source brief
- `wiki/outputs/` contains the saved query answer
- `wiki/outputs/chat-sessions/` and `state/chat-sessions/` contain the chat transcript and structured session state when `chat` is used
- `wiki/context/` and `state/context-packs/` contain the saved context pack when `context build` is used
- `wiki/exports/ai/` or the configured export directory contains `llms.txt`, `llms-full.txt`, `graph.jsonld`, `manifest.json`, `ai-readme.md`, and optional page siblings when `export ai` is used
- `wiki/memory/` and `state/memory/tasks/` contain task ledger artifacts when `task start` is used
- `state/graph.json` and `state/retrieval/` exist
- `swarmvault doctor` reports `ok` or gives concrete next commands such as `swarmvault compile` or `swarmvault retrieval rebuild`; `graph serve` shows those checks and commands in the workbench

## Guidance

- If the answer quality is weak, check whether the vault is still on the `heuristic` provider.
- If the user is unsure what changed, point them at `wiki/` and `state/` before suggesting another compile.
- When the vault lives in git, `swarmvault diff` is the quickest graph-level summary of what the last compile changed.
