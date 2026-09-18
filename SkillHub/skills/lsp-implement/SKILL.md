---
name: lsp-implement
description: Find all concrete implementations of an interface or abstract type. Use when you need to know what types satisfy an interface, or what subtypes exist before changing a base type.
argument-hint: "[interface-or-type-name]"
user-invocable: true
allowed-tools: mcp__lsp__start_lsp mcp__lsp__get_server_capabilities mcp__lsp__go_to_symbol mcp__lsp__go_to_implementation mcp__lsp__type_hierarchy mcp__lsp__open_document
license: MIT
compatibility: Requires the agent-lsp MCP server (github.com/blackwell-systems/agent-lsp)
metadata:
  required-capabilities: implementationProvider
  optional-capabilities: typeHierarchyProvider workspaceSymbolProvider
---

> Requires the agent-lsp MCP server.

# lsp-implement

Find every concrete type that implements an interface, or every subtype of an
abstract type. Read-only — does not modify any files.

Use this skill **before** changing an interface signature, adding a method to
an interface, or removing a base-type method. It tells you every type that
must be updated.

**Invocation:** User provides `type_name` (e.g. `"Handler"`, `"io.Reader"`).
Optionally provide `workspace_root`.

---

## Prerequisites

Check server capabilities — `go_to_implementation` and `type_hierarchy` are
optional features not implemented by all language servers:

```
mcp__lsp__get_server_capabilities()
```

Note which of `go_to_implementation` and `type_hierarchy` appear in
`supported_tools`. The steps below depend on this result.

If neither is supported, report `"Server does not support implementation
lookup"` and stop.

---

## Step 1 — Locate the interface or type

```
mcp__lsp__go_to_symbol({
  "symbol_path": "<TypeName>",
  "workspace_root": "/abs/path"   // optional
})
→ returns: file, line, column (1-indexed)
```

Open the file so the language server tracks it:

```
mcp__lsp__open_document({
  "file_path": "<file from go_to_symbol>"
})
```

Record `file`, `line`, `column` for subsequent steps.

---

## Step 2 — Find all implementations

Only if `go_to_implementation` appears in `supported_tools`.

```
mcp__lsp__go_to_implementation({
  "file_path": "<file>",
  "line": <line>,
  "column": <column>
})
```

Returns a list of locations — each is a concrete type that satisfies the
interface. Group by file. Record type names and locations.

If `go_to_implementation` is **not** supported: skip; note in report.

---

## Step 3 — Type hierarchy (subtypes and supertypes)

Only if `type_hierarchy` appears in `supported_tools`.

```
mcp__lsp__type_hierarchy({
  "file_path": "<file>",
  "line": <line>,
  "column": <column>,
  "direction": "subtypes"   // use "both" to also see what this type extends
})
```

`subtypes` returns concrete types that extend or embed this type.
`supertypes` returns what this type itself implements.

Cross-reference with Step 2 results — the union gives the complete
implementation surface.

If `type_hierarchy` is **not** supported: skip; note in report.

---

## Step 4 — Report

```
## Implementation Report: <TypeName>

### Definition
- File: <file>:<line>
- Kind: interface / abstract type / base struct

### Concrete Implementations (<N> found)
- TypeA — <file>:<line>
- TypeB — <file>:<line>
...

### Type Hierarchy
Supertypes: [list or "none"]
Subtypes: [list or "same as implementations above" or "not supported"]

### Risk Assessment
| N implementations | Recommendation |
|---|---|
| 0 | Interface unused or no external implementors found. May be internal-only. |
| 1–3 | Low risk. All implementors can be updated together. |
| 4–10 | Medium risk. Plan updates package by package. |
| > 10 | High risk. Changing the interface is a breaking API change. |
```

---

## Common use cases

**Before adding a method to an interface:**
Run lsp-implement to find all types that will need the new method. Each
implementation site must be updated — this is your required change list.

**Before removing a method:**
Find all types that implement it. Check whether any external (outside this
repo) packages may be affected.

**Understanding polymorphism in an unfamiliar codebase:**
Run lsp-implement on the primary interface to see the full type hierarchy
before making any changes.

---

## Language notes

| Language | `go_to_implementation` finds... |
|---|---|
| Go | All types with matching method sets |
| TypeScript | All classes implementing the interface |
| Java/C# | All classes/structs implementing the interface |
| Rust | All structs with `impl Trait for ...` |

For Go: `go_to_implementation` on an interface finds all types that satisfy
it, even without an explicit `implements` declaration.
