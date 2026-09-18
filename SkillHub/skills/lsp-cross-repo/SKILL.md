---
name: lsp-cross-repo
description: Cross-repository analysis — find all callers of a library symbol in one or more consumer repos. Use when refactoring a shared library and need to understand how consumers use it.
argument-hint: "[symbol-name] in [library-file:line:col] used by [consumer-root ...]"
user-invocable: true
allowed-tools: mcp__lsp__start_lsp mcp__lsp__find_symbol mcp__lsp__get_cross_repo_references mcp__lsp__add_workspace_folder mcp__lsp__list_workspace_folders mcp__lsp__go_to_implementation mcp__lsp__find_callers mcp__lsp__inspect_symbol
license: MIT
compatibility: Requires the agent-lsp MCP server (github.com/blackwell-systems/agent-lsp)
metadata:
  required-capabilities: referencesProvider
  optional-capabilities: implementationProvider callHierarchyProvider workspaceSymbolProvider
---

> Requires the agent-lsp MCP server.

# lsp-cross-repo

Multi-root cross-repo caller analysis for library + consumer workflows. Finds all
usages of a library symbol across one or more consumer codebases in a single call.

Read-only — does not modify any files.

## When to use

- Before changing a library API: find all callers in every consumer
- Before deleting a symbol: verify it has no cross-repo dependents
- When a change in repo A might break repo B or C
- Auditing how internal packages are used across services

Use `/lsp-impact` instead for single-repo blast-radius analysis.

## Workflow

### Step 1 — Initialize the primary workspace

Start the language server on the library root if not already running:

```
mcp__lsp__start_lsp({ "root_dir": "/path/to/library" })
```

### Step 2 — Locate the library symbol

Find the symbol's definition to get `file_path`, `line`, and `column`:

```
mcp__lsp__find_symbol({ "query": "<symbol-name>" })
```

Pick the result in the library repo (not a test file).

### Step 3 — Find all cross-repo references (primary step)

Call `get_cross_repo_references` with the symbol location and all consumer repo
roots. This adds each consumer as a workspace folder, waits for indexing, runs
`find_references` across all roots, and returns results partitioned by repo:

```
mcp__lsp__get_cross_repo_references({
  "symbol_file": "/abs/path/to/library/file.go",
  "line": <line>,
  "column": <column>,
  "consumer_roots": [
    "/abs/path/to/consumer-a",
    "/abs/path/to/consumer-b"
  ]
})
```

Returns:
- `library_references` — usages within the library itself
- `consumer_references` — a map of `consumer-root → [file:line ...]`
- `warnings` — any roots that could not be indexed (check these manually)

**Decision after Step 3:**

| Result | Action |
|--------|--------|
| No consumer refs | Safe to change — verify `warnings` is empty first |
| Consumer refs found | Run `/lsp-impact` on each call site before editing |
| `warnings` non-empty | Re-add that root manually and retry Step 3 |

### Step 4 — Callers and implementations (optional)

For a deeper look at how consumers call the symbol:

```
mcp__lsp__find_callers({
  "file_path": "<library-file>",
  "line": <line>,
  "column": <column>,
  "direction": "incoming"
})
```

For interfaces — all consumer-side implementations:

```
mcp__lsp__go_to_implementation({
  "file_path": "<library-file>",
  "line": <line>,
  "column": <column>
})
```

## Output format

```
## Library-internal references
- file:line — brief context

## Consumer references

### /path/to/consumer-a
- file:line — brief context

### /path/to/consumer-b
- file:line — brief context
```

## Decision guide

| Situation | Action |
|-----------|--------|
| No consumer refs, warnings empty | Safe to change |
| Consumer refs found | Run `/lsp-impact` on each call site before editing |
| `warnings` lists a consumer root | That root failed indexing — check LSP logs |
| Consumer uses interface, not concrete type | Use `go_to_implementation` to find all implementors |

## Example

```
# Refactoring ParseConfig in a shared config library used by 3 services

start_lsp(root_dir="/repos/config-lib")
find_symbol(query="ParseConfig")        # find definition → file:42:6
get_cross_repo_references(
  symbol_file="/repos/config-lib/pkg/config/parser.go",
  line=42, column=6,
  consumer_roots=["/repos/api-service", "/repos/worker-service", "/repos/batch-job"]
)
# → library_references: 2
# → consumer_references: {api-service: [main.go:14, app.go:31], worker-service: [runner.go:8]}
# → warnings: []
```
