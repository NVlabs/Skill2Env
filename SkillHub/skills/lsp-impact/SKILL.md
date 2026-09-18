---
name: lsp-impact
description: Blast-radius analysis for a symbol or file — shows all callers, type supertypes/subtypes, and reference count before you change it. Use when refactoring, deleting, or changing the signature of any function, type, or method. Also accepts a file path to surface all exported-symbol impact in one shot.
argument-hint: "[symbol-name | file-path]"
user-invocable: true
allowed-tools: mcp__lsp__go_to_symbol mcp__lsp__find_callers mcp__lsp__type_hierarchy mcp__lsp__find_references mcp__lsp__get_server_capabilities mcp__lsp__blast_radius
license: MIT
compatibility: Requires the agent-lsp MCP server (github.com/blackwell-systems/agent-lsp)
metadata:
  required-capabilities: referencesProvider
  optional-capabilities: callHierarchyProvider typeHierarchyProvider workspaceSymbolProvider
---

> Requires the agent-lsp MCP server.

# lsp-impact

Blast-radius analysis for any symbol or file. Discovers all direct references,
callers (via call hierarchy), and type relationships before you touch anything.
Read-only — does not modify any files.

Run this skill **before** lsp-edit-export: impact tells you what exists and how
widespread the change is; lsp-edit-export tells you how to execute the change safely.

**Invocation:**
- **File path** (e.g. `"internal/lsp/client.go"`) → use the File-level entry (Step 0) to surface all exported-symbol impact at once.
- **Symbol name** in dot notation (e.g. `"codec.Encode"`, `"Buffer.Reset"`) → skip Step 0; start at Prerequisites, then Step 1.

---

## Step 0 — File-level entry (when user provides a file path)

Use this shortcut when the user is changing or auditing an entire file rather
than a single symbol. `blast_radius` enumerates all exported symbols in
the file, resolves their references, and returns test callers (with enclosing
test function names) and non-test callers in a single call.

```
mcp__lsp__blast_radius({
  "changed_files": ["/abs/path/to/file.go"],
  "include_transitive": false   // set true to surface second-order callers
})
```

Returns:
- `affected_symbols` — each exported symbol with its reference count
- `test_callers` — test files + enclosing test function names
- `non_test_callers` — production call sites

**Decision after Step 0:**

| Result | Action |
|--------|--------|
| 0 non-test callers | Low blast radius. Proceed with change. |
| Few callers, known files | Medium risk. Update each call site. |
| Many callers across packages | High risk. Consider staged rollout. |
| Want symbol-level detail | Continue to Steps 1–5 for any specific symbol. |

Skip Steps 1–5 if the file-level summary is sufficient.

---

## Prerequisites (for symbol-level Steps 1–5)

If LSP is not yet initialized, call `mcp__lsp__start_lsp` with the workspace
root first.

Check what the server supports before proceeding — `find_callers` and
`type_hierarchy` are optional LSP features not implemented by all servers:

```
mcp__lsp__get_server_capabilities()
```

Note which tools appear in `supported_tools`. Steps 3 and 4 below depend on
this result.

---

## Step 1 — Locate the symbol

Use `go_to_symbol` with the symbol name provided by the user:

```
mcp__lsp__go_to_symbol({
  "symbol_path": "Package.SymbolName",
  "workspace_root": "/abs/path"   // optional, narrows scope
})
→ returns: file, line, column (1-indexed)
```

`symbol_path` uses dot notation. For a top-level function `Encode` in package
`codec`, use `"codec.Encode"`. For a method `Reset` on type `Buffer`, use
`"Buffer.Reset"`.

Record the returned `file`, `line`, and `column` — you will pass them to
every subsequent step.

---

## Step 2 — Enumerate all direct references (always available)

Call `find_references` with `include_declaration: false` to find every usage
site across the workspace:

```
mcp__lsp__find_references({
  "file_path": "<file from Step 1>",
  "position_pattern": "func @@SymbolName(",   // adjust prefix for symbol kind
  "include_declaration": false
})
```

Collect all reference locations. Group results by file. Record the total count
and list of files — these feed the Impact Report.

See [references/patterns.md](references/patterns.md) for `position_pattern`
examples by language and symbol kind.

---

## Step 3 — Call hierarchy (callers and callees)

Only if `find_callers` appears in `supported_tools` from Step 0.

```
mcp__lsp__find_callers({
  "file_path": "<file from Step 1>",
  "line": <line from Step 1>,
  "column": <column from Step 1>,
  "direction": "incoming"   // use "both" if callees are also needed
})
```

If `find_callers` is **not** in `supported_tools`, skip this step entirely.
Note `"call hierarchy not supported by this server"` in the Impact Report.

---

## Step 4 — Type hierarchy (supertypes and subtypes)

Only applicable when the symbol is a **type, interface, or class** (not a
plain function or method). Only if `type_hierarchy` appears in `supported_tools`.

```
mcp__lsp__type_hierarchy({
  "file_path": "<file from Step 1>",
  "line": <line from Step 1>,
  "column": <column from Step 1>,
  "direction": "both"
})
```

If the symbol is a **function or method**: skip this step; note
`"not applicable (function)"` in the report.

If `type_hierarchy` is **not** in `supported_tools`: skip this step; note
`"not supported by this server"` in the report.

---

## Step 5 — Report impact surface

Produce the Impact Report using the format defined in
[references/patterns.md](references/patterns.md).

Include:

- Symbol name, kind, and definition location
- Reference count and list of files containing references
- Callers from `find_callers` incoming (or skip note)
- Supertypes and subtypes from `type_hierarchy` (or skip note)
- Blast radius: count of distinct files affected

Then apply the decision guide:

| Blast radius | Recommendation |
|---|---|
| 0 references | Likely dead code. Confirm with lsp-dead-code before deleting. |
| 1–5 files | Low risk. Proceed. Update all callers. |
| 6–20 files | Medium risk. Plan changes carefully. Stage in waves. |
| > 20 files | High risk. Consider a deprecation path or feature flag. |

---

## Example

```
Goal: assess blast radius of exported function `ParseConfig` in pkg/config

Prerequisites — get_server_capabilities:
  → supported_tools: [go_to_symbol, find_references, find_callers, ...]
  → type_hierarchy: not in supported_tools

Step 1 — go_to_symbol: symbol_path="config.ParseConfig"
  → pkg/config/parser.go:42:6

Step 2 — find_references: position_pattern="func @@ParseConfig("
  → 7 references in 4 files
  → cmd/main.go, internal/app.go, internal/loader.go, pkg/config/parser_test.go

Step 3 — find_callers: direction="incoming"
  → callers: cmd.main (cmd/main.go:14), app.Start (internal/app.go:31), ...

Step 4 — type_hierarchy: skipped (function), also not supported by server

Step 5 — Impact Report:
  ## Impact Report: ParseConfig
  - Kind:         function
  - Definition:   pkg/config/parser.go:42:6
  - References:   7 across 4 files
  ...
  - Risk level:   low
```

## Note on position_pattern

`position_pattern` with `@@` is a agent-lsp extension. If your MCP client
does not support it, fall back to explicit `line` and `column` parameters from
the location returned by `go_to_symbol` in Step 1.
