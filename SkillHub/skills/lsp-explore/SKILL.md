---
name: lsp-explore
description: "Tell me about this symbol": hover + implementations + call hierarchy + references in one pass — for navigating unfamiliar code.
argument-hint: "[symbol-name]"
user-invocable: true
allowed-tools: mcp__lsp__start_lsp mcp__lsp__go_to_symbol mcp__lsp__inspect_symbol mcp__lsp__go_to_implementation mcp__lsp__find_callers mcp__lsp__find_references mcp__lsp__open_document mcp__lsp__get_server_capabilities
license: MIT
compatibility: Requires the agent-lsp MCP server (github.com/blackwell-systems/agent-lsp)
metadata:
  required-capabilities: hoverProvider
  optional-capabilities: implementationProvider callHierarchyProvider referencesProvider
---

> Requires the agent-lsp MCP server.

# lsp-explore

"Tell me about this symbol" — hover, implementations, call hierarchy, and
references in a single pass. Use when navigating unfamiliar code: you get
type info, doc comments, who calls it, what implements it, and every
reference site without issuing four separate commands.

Read-only — does not modify any files.

**Invocation:** User provides a symbol name in dot notation (e.g.
`"codec.Encode"`, `"Buffer.Reset"`). Optionally provide `workspace_root`
to scope the search.

---

## Prerequisites

If LSP is not yet initialized, call `mcp__lsp__start_lsp` with the workspace
root first. Auto-inference applies when file paths are provided.

---

## Phase 1 — Locate the symbol

Call `mcp__lsp__go_to_symbol` with `symbol_path` set to the user-provided name:

```
mcp__lsp__go_to_symbol({
  "symbol_path": "Package.SymbolName",   // dot notation; e.g. "codec.Encode"
  "workspace_root": "<root>"             // optional
})
→ returns: file, line, column (1-indexed)
```

Record the returned `file`, `line`, and `column`. If `go_to_symbol` returns
nothing, report:

> Symbol not found: `<name>`
> Check the dot-notation path (e.g. "Package.Symbol") and ensure the workspace
> root covers the file.

Stop immediately — do not proceed to Phase 2.

Then open the file so the language server has it in view:

```
mcp__lsp__open_document({
  "file_path": "<file from go_to_symbol>"
})
```

---

## Phase 2 — Hover (always available)

Call `mcp__lsp__inspect_symbol` at the definition location:

```
mcp__lsp__inspect_symbol({
  "file_path": "<file from Phase 1>",
  "line": <line from Phase 1>,
  "column": <column from Phase 1>
})
```

Store the result as `hover_text`. If the call fails or returns nothing, set
`hover_text` to an empty string. Do not stop.

---

## Phase 3 — Implementations (capability-gated)

Call `mcp__lsp__get_server_capabilities` to see what the server supports:

```
mcp__lsp__get_server_capabilities()
→ returns: supported_tools list
```

If `go_to_implementation` appears in `supported_tools`, call it:

```
mcp__lsp__go_to_implementation({
  "file_path": "<file from Phase 1>",
  "line": <line from Phase 1>,
  "column": <column from Phase 1>
})
→ returns: list of implementation locations (file, line)
```

Record locations as `implementations`. If `go_to_implementation` is **not**
in `supported_tools`, record `"not supported by this server"` — do not stop.

---

## Phase 4 — Call hierarchy and references (run in parallel)

Issue both calls in the same message — they are independent:

### 4a — Incoming callers

Only if `find_callers` appears in `supported_tools`:

```
mcp__lsp__find_callers({
  "file_path": "<file from Phase 1>",
  "line": <line from Phase 1>,
  "column": <column from Phase 1>,
  "direction": "incoming"
})
→ returns: list of caller functions with file and line
```

If `find_callers` is **not** in `supported_tools`, note
`"not supported by this server"` — do not stop.

### 4b — All reference sites

```
mcp__lsp__find_references({
  "file_path": "<file from Phase 1>",
  "line": <line from Phase 1>,
  "column": <column from Phase 1>,
  "include_declaration": false
})
→ returns: list of reference locations (file, line)
```

Collect all reference locations. Group by file and count distinct files.

---

## Output format — Explore Report

Produce the report in this format:

```
## Explore Report: <SymbolName>

### Definition
- File: <file>:<line>
- Hover: <hover_text or "unavailable">

### Implementations (<N> found, or "not supported")
[list of file:line entries, or "none found", or "not supported by this server"]

### Callers (incoming call hierarchy)
[list of caller function names with file:line, or "none", or "not supported"]

### References (<N> total across <M> files)
[list of file:line entries grouped by file, or "none found"]

### Summary
- Symbol kind:      <inferred from hover or "unknown">
- Reference count:  <N>
- Files with refs:  <M distinct files>
- Callers:          <K>
- Implementations:  <P or "not supported">
```

Keep the report concise. The goal is "understand this symbol in one pass."

---

## Example

```
Goal: understand the exported function `ParseConfig` in pkg/config

Phase 1 — go_to_symbol: symbol_path="config.ParseConfig"
  → pkg/config/parser.go:42:6

open_document: pkg/config/parser.go

Phase 2 — inspect_symbol: line=42, column=6
  → hover_text: "func ParseConfig(path string) (*Config, error) — reads and
    validates a config file from path"

Phase 3 — get_server_capabilities
  → go_to_implementation: in supported_tools
  go_to_implementation: line=42, column=6
  → 0 implementations (ParseConfig is a concrete function, not an interface method)

Phase 4 (parallel):
  find_callers direction=incoming
  → 3 callers: cmd.main (cmd/main.go:14), app.Start (internal/app.go:31),
               loader.Load (internal/loader.go:55)

  find_references include_declaration=false
  → 7 references in 4 files

## Explore Report: ParseConfig

### Definition
- File: pkg/config/parser.go:42
- Hover: func ParseConfig(path string) (*Config, error) — reads and validates a
  config file from path

### Implementations (0 found)
none found

### Callers (incoming call hierarchy)
- cmd.main — cmd/main.go:14
- app.Start — internal/app.go:31
- loader.Load — internal/loader.go:55

### References (7 total across 4 files)
cmd/main.go: line 14
internal/app.go: lines 31, 87
internal/loader.go: line 55
pkg/config/parser_test.go: lines 12, 34, 56, 78

### Summary
- Symbol kind:      function
- Reference count:  7
- Files with refs:  4
- Callers:          3
- Implementations:  0
```
