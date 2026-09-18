# Graph-First Agent Workflow Example

Use this when the user wants Claude Code (or another hook-capable agent) to answer code questions from the graph instead of broad search, with the graph kept fresh automatically as files change.

## Commands

```bash
cd <repo>
swarmvault init && swarmvault ingest .
swarmvault install --agent claude --hook --mcp --graph-first
swarmvault hook install
swarmvault graph status .
swarmvault graph query "auth flow"
swarmvault graph explain "src/auth.ts"
swarmvault graph path "LoginForm" "SessionStore"
swarmvault graph callers "chargeCustomer"
swarmvault query "How does the auth flow work?"
swarmvault context build "Refactor the auth flow" --target ./src --budget 8000
swarmvault graph update --file ./src/auth.ts
swarmvault install status --agent claude --hook --mcp
```

## What To Check

- `.claude/settings.json` contains the SwarmVault hook entries and `.claude/hooks/swarmvault-graph-first.js` exists after `install --agent claude --hook`
- `.mcp.json` registers the `swarmvault` MCP server (`{"mcpServers":{"swarmvault":{"command":"swarmvault","args":["mcp"]}}}`) after `--mcp`
- `.claude/skills/swarmvault/SKILL.md` exists as the project skill bundle
- A new Claude Code session starts with injected graph-first instructions plus a staleness note when `wiki/graph/report.md` exists
- With `--graph-first` installed, the first broad Grep/Glob/Bash search in a session is denied once with a redirect to the plain `graph query|explain|path` commands (the deny message warns against `--json`, which produces much larger output); repeating the same search is then allowed. Without the opt-in the hook stays advisory and only adds a one-time guidance note
- Searches scoped to `wiki/`, `raw/`, `state/`, a single file, or search tools filtering piped output pass through without interception
- `swarmvault graph callers "chargeCustomer"` lists every caller of the symbol from graph call edges with exact file:line call-site evidence (it scans only the files the graph identifies as callers), and the deny/redirect message recommends it for who-calls/impact-of-change questions
- After the agent edits a file, a background `swarmvault graph update --file <path>` refresh runs and `swarmvault graph status .` reports the graph fresh again
- Concurrent edit bursts coalesce through the refresh lock plus queue under `state/watch/` instead of stacking compiles
- `graph_status` and `update_graph` are available over MCP for read-only freshness checks and code-only (optionally per-file) refreshes
- `swarmvault hook install` adds the git `post-commit`/`post-checkout` refresh so branch switches stay current too

## Guidance

- Answer "where is X / what calls Y / how is Z structured" questions with the plain `graph query`, `graph explain`, and `graph path` commands before reading source files; `graph query "<seed>"` prints the top matches with page paths plus an inline excerpt of the best-matching wiki page, so one command usually answers the question without follow-up file reads. Read sources directly only when editing them, and avoid `--json` for these reads — it produces much larger output.
- If a search is denied, run the suggested graph command first; retrying the same search is always allowed when the graph genuinely lacks the detail.
- Enforcement is opt-in: install with `--graph-first` (persists `hooks.graphFirst: "deny"`), or set `hooks.graphFirst` in `swarmvault.config.json` later. The default without opt-in is `context` — session guidance without denying searches. `SWARMVAULT_GRAPH_FIRST=deny|context|off` overrides per session.
- Use `swarmvault install --agent claude --hook --scope user` to set up `~/.claude` once for all repos; the hook no-ops in repos without a compiled graph report.
- Codex, Gemini, Copilot, OpenCode, and Kilo installs carry the same graph-first guidance adapted to each tool's hook API.
