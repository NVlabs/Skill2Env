---
name: lsp-understand
description: Deep-dive exploration of unfamiliar code — given a symbol or file, builds a complete Code Map showing type info, implementations, call hierarchy (2-level depth limit), all references, and source. Broader than lsp-explore: accepts files, synthesizes multi-symbol relationships, and produces a navigable dependency map.
argument-hint: "[symbol-name | file-path]"
user-invocable: true
allowed-tools: mcp__lsp__inspect_symbol mcp__lsp__go_to_implementation mcp__lsp__find_callers mcp__lsp__find_references mcp__lsp__get_symbol_source mcp__lsp__list_symbols mcp__lsp__open_document mcp__lsp__go_to_symbol mcp__lsp__get_server_capabilities
license: MIT
compatibility: Requires the agent-lsp MCP server (github.com/blackwell-systems/agent-lsp)
metadata:
  required-capabilities: hoverProvider
  optional-capabilities: implementationProvider callHierarchyProvider referencesProvider documentSymbolProvider workspaceSymbolProvider
---

> Requires the agent-lsp MCP server.

# lsp-understand

Deep-dive exploration of unfamiliar code — given a symbol or file, synthesizes
hover info, implementations, call hierarchy (bounded to 2 levels), all
references, and source into a structured Code Map.

Read-only — does not modify any files.

---

## Differentiation from lsp-explore

`/lsp-explore` is a single-symbol pass: given one symbol name, it runs hover +
implementations + call hierarchy + references and produces a per-symbol report.
Use lsp-explore for quick "what is this one thing" questions.

`/lsp-understand` is broader in three ways:

1. **Accepts a file path as input** — explores all exported symbols in that file
   as a group (Mode B), rather than requiring a single symbol name.
2. **Synthesizes cross-symbol relationships** — produces a dependency map showing
   how entry points call each other, share callers, or implement the same
   interface, rather than isolated per-symbol reports.
3. **Enforces a 2-level call hierarchy depth limit** — prevents infinite recursion
   in deeply connected code.

Use lsp-understand for "how does this module work as a whole."

---

## Input — Two Modes

**Mode A (symbol):** User provides a symbol name in dot notation
(e.g., `"codec.Encode"`, `"Handler.ServeHTTP"`).

**Mode B (file):** User provides an absolute file path. All exported symbols in
the file become the entry points.

---

## Prerequisites

Call `mcp__lsp__get_server_capabilities` before Step 2 to determine which
capabilities are available. Skip steps that require missing capabilities:

- `go_to_implementation`: skip Step 2b if `implementationProvider: false`
- `find_callers`: skip Steps 2c and 2d if `callHierarchyProvider: false`; note
  in the Code Map output that call hierarchy was unavailable

---

## Step 1 — Entry Point Resolution

### Mode A: Single Symbol

Call `mcp__lsp__go_to_symbol` to locate the symbol definition:

```
mcp__lsp__go_to_symbol({
  "symbol_path": "<dot-notation name>",   // e.g. "codec.Encode"
  "workspace_root": "<root>"              // optional
})
→ returns: file_path, line, column (1-indexed)
```

Record `file_path`, `line`, and `column`. If `go_to_symbol` returns nothing,
report:

> Symbol not found: `<name>`
> Check the dot-notation path (e.g. "Package.Symbol") and ensure the workspace
> root covers the file.

Stop immediately — do not proceed to Step 2.

The single symbol becomes the sole entry point.

### Mode B: File Path

Call `mcp__lsp__open_document` then `mcp__lsp__list_symbols`:

```
mcp__lsp__open_document({ "file_path": "<absolute path>" })

mcp__lsp__list_symbols({ "file_path": "<absolute path>" })
→ returns: list of symbols with kind, line, column
```

Filter to exported symbols:
- **Go:** uppercase first letter
- **TypeScript/JavaScript:** `export` keyword
- **Rust:** `pub` visibility

Cap at **10 exported symbols maximum**. If more than 10 are found, prioritize
top-level functions and types; skip constants and variables.

Each filtered symbol becomes an entry point with its `file_path`, `line`, and
`column`.

---

## Step 2 — Per-Symbol Analysis

For each entry point, run the following sub-steps. Where possible, parallelize
calls within each step.

### 2a — Type Info and Docs

Call `mcp__lsp__inspect_symbol` using `position_pattern` with the `@@`
marker (see references/patterns.md):

```
mcp__lsp__inspect_symbol({
  "file_path": "<file>",
  "position_pattern": "<symbol@@name>",
  "line_scope_start": <line - 5>,
  "line_scope_end": <line + 5>
})
→ returns: hover text with type signature and doc comment
```

Store result as `hover_text`. If the call fails or returns nothing, set
`hover_text` to an empty string. Do not stop.

### 2b — Implementations (capability-gated)

If `implementationProvider` is available in server capabilities:

```
mcp__lsp__go_to_implementation({
  "file_path": "<file>",
  "line": <line>,
  "column": <column>
})
→ returns: list of concrete implementation locations
```

Skip if capability is absent. Record `"not supported by this server"` rather
than stopping.

### 2c — Incoming Call Hierarchy (bounded to 2 levels)

If `callHierarchyProvider` is available:

**Level 1 — Direct callers:**

```
mcp__lsp__find_callers({
  "file_path": "<file>",
  "line": <line>,
  "column": <column>,
  "direction": "incoming"
})
→ returns: list of direct caller functions with file and line
```

**Level 2 — Callers of callers:**

For each Level 1 caller, call `mcp__lsp__find_callers` once more:

```
mcp__lsp__find_callers({
  "file_path": "<caller file>",
  "line": <caller line>,
  "column": <caller column>,
  "direction": "incoming"
})
→ returns: Level 2 callers
```

**STOP at Level 2 — do not recurse further under any circumstances.**

If Level 2 callers > 10: summarize by count and file, do not list individually.

### 2d — Outgoing Calls (Level 1 only)

If `callHierarchyProvider` is available:

```
mcp__lsp__find_callers({
  "file_path": "<file>",
  "line": <line>,
  "column": <column>,
  "direction": "outgoing"
})
→ returns: list of functions this symbol calls
```

**Level 1 only — no recursion.**

### 2e — All References

```
mcp__lsp__find_references({
  "file_path": "<file>",
  "line": <line>,
  "column": <column>,
  "include_declaration": false
})
→ returns: every usage site across the workspace
```

Group by file and count distinct files.

### 2f — Source

```
mcp__lsp__get_symbol_source({
  "file_path": "<file>",
  "line": <line>,
  "column": <column>
})
→ returns: implementation body
```

---

## Step 3 — Synthesize Relationships

After analyzing all entry points, identify cross-symbol relationships:

- **Internal calls:** Which entry points call each other? (from outgoing calls
  in Step 2d)
- **Shared callers:** Which entry points are called by the same Level 1 callers?
- **Shared interface:** Which entry points implement the same interface? (from
  Step 2b)

This synthesis step is what distinguishes `/lsp-understand` from running
multiple `/lsp-explore` calls. The output is a dependency map, not isolated
per-symbol reports.

---

## Step 4 — Output: Code Map

Produce a structured Code Map with these sections:

```
## Code Map: <target>

### Summary
<2-3 sentence description of what this code does, synthesized from
hover docs and source reading>

### Symbols (<N> analyzed)

#### <SymbolName>
- **Type:** <type signature from hover>
- **Source:** <file:line>
- **Incoming callers (L1):** <list; count only if > 5>
- **Incoming callers (L2):** <summarized; e.g., "called by 3 HTTP handlers">
- **Outgoing calls:** <what this symbol calls>
- **Implements:** <interface name, if applicable>
- **References:** N sites across M files

### Dependency Relationships
<symbols that call each other, as a simple text diagram or list>
e.g.:
  HandlerA → Parse → Validate
  HandlerB → Parse

### Entry Points to This Code
<top-level callers that are NOT in this file — where does outside code
call in?>

### Depth-limit Note
Call hierarchy stopped at 2 levels. <N> additional callers exist beyond
Level 2 — use /lsp-explore on specific symbols to drill deeper.
```

---

## Depth Control Rules

These limits are hard constraints — never exceed them:

- Incoming call hierarchy recursion **stops at Level 2**
- Outgoing calls: **Level 1 only**, no recursion
- If Level 2 callers > 10: **summarize by count and file**, do not list individually
- Do NOT follow call chains beyond these limits under any circumstances

---

## Example

```
Goal: understand how the file pkg/codec/encoder.go works as a whole

Step 1 — Mode B (file path)
  open_document: pkg/codec/encoder.go
  list_symbols: pkg/codec/encoder.go
  → exported symbols: Encoder (type), Encode (func), Reset (func), NewEncoder (func)
  → 4 exported symbols (under 10 cap)

get_server_capabilities
  → go_to_implementation: supported
  → find_callers: supported

Step 2 — Per-symbol analysis (run in parallel across symbols)

  Symbol: NewEncoder (pkg/codec/encoder.go:12)
    inspect_symbol → "func NewEncoder(w io.Writer) *Encoder"
    go_to_implementation → 0 (concrete function)
    find_callers incoming L1 → 5 callers
    find_callers incoming L2 → 3 callers of those callers
    find_callers outgoing → calls: bufio.NewWriter
    find_references → 5 sites in 3 files
    get_symbol_source → implementation body

  Symbol: Encode (pkg/codec/encoder.go:28)
    inspect_symbol → "func (e *Encoder) Encode(v any) error"
    go_to_implementation → implements codec.Encoder interface
    find_callers incoming L1 → 8 callers (listed)
    find_callers incoming L2 → > 10: "12 additional callers across 5 files"
    find_callers outgoing → calls: NewEncoder, e.w.Flush
    find_references → 8 sites in 5 files
    get_symbol_source → implementation body

  (similar for Encoder type and Reset func...)

Step 3 — Synthesize relationships
  - Encode calls NewEncoder (internal dependency)
  - NewEncoder and Encode share callers in cmd/main.go
  - Encode implements codec.Encoder interface

## Code Map: pkg/codec/encoder.go

### Summary
This file implements a streaming JSON encoder backed by a buffered writer.
NewEncoder constructs an Encoder wrapping any io.Writer; Encode serializes
values and flushes. Reset allows reuse without allocation.

### Symbols (4 analyzed)

#### NewEncoder
- **Type:** func NewEncoder(w io.Writer) *Encoder
- **Source:** pkg/codec/encoder.go:12
- **Incoming callers (L1):** cmd.main, app.Start, loader.Load, test.Setup, bench.Run
- **Incoming callers (L2):** 3 callers across 2 files
- **Outgoing calls:** bufio.NewWriter
- **Implements:** n/a
- **References:** 5 sites across 3 files

#### Encode
- **Type:** func (e *Encoder) Encode(v any) error
- **Source:** pkg/codec/encoder.go:28
- **Incoming callers (L1):** 8 callers (cmd/main.go, internal/app.go, ...)
- **Incoming callers (L2):** 12 additional callers across 5 files (depth limit reached)
- **Outgoing calls:** NewEncoder, e.w.Flush
- **Implements:** codec.Encoder
- **References:** 8 sites across 5 files

...

### Dependency Relationships
  cmd.main → NewEncoder → bufio.NewWriter
  cmd.main → Encode → NewEncoder
  Encode → Reset

### Entry Points to This Code
- cmd.main (cmd/main.go:14)
- app.Start (internal/app.go:31)
- loader.Load (internal/loader.go:55)

### Depth-limit Note
Call hierarchy stopped at 2 levels. 12 additional callers exist beyond
Level 2 for Encode — use /lsp-explore on specific symbols to drill deeper.
```
