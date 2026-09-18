---
name: lsp-local-symbols
description: Fast file-scoped symbol analysis — find all usages of a symbol within the current file, list all symbols defined in the file, and get type info at a position. Use when you need local-scope analysis without a workspace-wide search.
argument-hint: "[symbol-name] in [file-path]"
user-invocable: true
allowed-tools: mcp__lsp__open_document mcp__lsp__list_symbols mcp__lsp__inspect_symbol mcp__lsp__get_document_highlights
license: MIT
compatibility: Requires the agent-lsp MCP server (github.com/blackwell-systems/agent-lsp)
metadata:
  required-capabilities: documentSymbolProvider
  optional-capabilities: documentHighlightProvider hoverProvider
---

> Requires the agent-lsp MCP server.

# lsp-local-symbols

File-scoped symbol analysis using the language server index. Faster than
workspace-wide search for questions about a single file: what symbols are
defined here, where is this symbol used within the file, and what type does it
have.

Read-only — does not modify any files.

## When to use

- "Where is `x` used in this file?" — use `get_document_highlights`
- "What functions and types are defined in this file?" — use `list_symbols`
- "What type does this symbol have?" — use `inspect_symbol`
- Reviewing a file before editing — get the full symbol map first
- Local refactor scoping — confirm a symbol is only used in one place before inlining it

Use `/lsp-impact` instead when you need workspace-wide callers and cross-file
references. Use `/lsp-dead-code` when auditing exported symbols for zero callers.

## When NOT to use

`get_document_highlights` is file-scoped by design — it only finds usages within
the open file. If a symbol is used across multiple files, this skill will not
find those. Use `find_references` (via `/lsp-impact`) for cross-file analysis.

---

## Workflow

### Step 1 — Open the file

Open the file so the language server tracks it:

```
mcp__lsp__open_document
  file_path: "/abs/path/to/file.go"
  language_id: "go"              # go, typescript, python, rust, etc.
```

### Step 2 — List all symbols in the file

Get the full symbol tree for the file:

```
mcp__lsp__list_symbols
  file_path: "/abs/path/to/file.go"
```

This returns all functions, types, variables, constants, and methods defined in
the file — including nested symbols (methods on types, fields in structs).

Use this to:
- Understand the file's structure before editing
- Find the exact position of a named symbol
- See what a file exposes before reading it in full

**Reading the output:** Each symbol has a `range` (full body including braces)
and a `selectionRange` (just the name). Coordinates are 1-based. Use
`selectionRange.start.line` and `selectionRange.start.character` as inputs to
`get_document_highlights` and `inspect_symbol`.

### Step 3 — Find all usages within the file

Call `get_document_highlights` at the symbol's position:

```
mcp__lsp__get_document_highlights
  file_path: "/abs/path/to/file.go"
  line: <selectionRange.start.line from Step 2>
  column: <selectionRange.start.character from Step 2>
```

Returns every occurrence of the symbol within the file, classified as:
- `read` — the symbol is read here
- `write` — the symbol is assigned/mutated here
- `text` — a text match (fallback when semantic classification isn't available)

**Speed note:** `get_document_highlights` is significantly faster than
`find_references` for file-local queries — it does not scan the entire workspace
index. Use it first; escalate to `find_references` only if you need cross-file
results.

### Step 4 — Get type information (optional)

For any position of interest, get the type signature and docs:

```
mcp__lsp__inspect_symbol
  file_path: "/abs/path/to/file.go"
  line: <line>
  column: <column>
```

Returns the hover text: type signature, documentation, and inferred types.
Useful for confirming what a symbol is before deciding to rename or inline it.

---

## Output format

Report results in three sections (omit any section with no content):

```
## Symbols in <filename>

### Functions / Methods
- `FuncName` — line N–M
- `(Type) MethodName` — line N–M

### Types
- `TypeName` (struct/interface/alias) — line N

### Variables / Constants
- `ConstName` = value — line N

---

## Usages of `<symbol>` in <filename>

N occurrences across M lines:
- line 12 [write] — assignment
- line 34 [read]  — passed as argument
- line 67 [read]  — returned

---

## Type info

`<symbol>`: <type signature from inspect_symbol>
```

---

## Decision guide

| Question | Tool |
|----------|------|
| What's in this file? | `list_symbols` |
| Where is X used in this file? | `get_document_highlights` |
| What type is X? | `inspect_symbol` |
| Is X safe to inline (used once)? | `get_document_highlights` — count occurrences |
| Is X used outside this file? | Use `/lsp-impact` instead |
| Is X dead code (no callers anywhere)? | Use `/lsp-dead-code` instead |

---

## Example

```
# "Where is the `config` variable used in server.go?"

open_document(file_path="/repo/server.go", language_id="go")
list_symbols(file_path="/repo/server.go")
  → finds `config` at selectionRange line 42, col 2

get_document_highlights(file_path="/repo/server.go", line=42, column=2)
  → returns 7 occurrences: 1 write (line 42), 6 reads

inspect_symbol(file_path="/repo/server.go", line=42, column=2)
  → "config *Config — the parsed server configuration"
```
