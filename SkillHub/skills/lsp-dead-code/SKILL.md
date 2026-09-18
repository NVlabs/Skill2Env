---
name: lsp-dead-code
description: Enumerate exported symbols in a file and surface those with zero references across the workspace. Use when auditing for dead code, cleaning up APIs, or checking which exports are safe to remove.
argument-hint: "[file-path]"
user-invocable: true
allowed-tools: mcp__lsp__list_symbols mcp__lsp__find_references mcp__lsp__open_document mcp__lsp__safe_delete_symbol
license: MIT
compatibility: Requires the agent-lsp MCP server (github.com/blackwell-systems/agent-lsp)
metadata:
  required-capabilities: documentSymbolProvider referencesProvider
---

> Requires the agent-lsp MCP server.

# lsp-dead-code

Audit an exported symbol list for zero-reference candidates. Calls
`list_symbols` to enumerate symbols, then checks each exported
symbol with `find_references` to find callers. Produces a classified report.

## When to Use

Use this skill when you want to identify dead code in a file — exported
symbols that are defined but never called anywhere in the workspace. Common
use cases:

- Cleaning up APIs before a release
- Identifying legacy exports that can be safely removed
- Auditing a package for unused public surface area

**Important:** This skill surfaces *candidates*. Always review results
manually before deleting anything. See the Caveats section below.

## What counts as "exported"

| Language   | Exported means...                                                      |
|------------|------------------------------------------------------------------------|
| Go         | Identifier starts with an uppercase letter (e.g. `MyFunc`, `MyType`)  |
| TypeScript | Has `export` keyword; or is a public class member (no `private`)       |
| Python     | Not prefixed with `_`; or explicitly listed in `__all__`               |
| Java/C#    | Has `public` or `protected` visibility modifier                        |
| Rust       | Has `pub` keyword                                                      |

## Prerequisites

If LSP is not yet initialized, call `mcp__lsp__start_lsp` with the
workspace root first:

```
mcp__lsp__start_lsp({ "root_dir": "/your/workspace" })
```

agent-lsp supports auto-inference from file paths, so explicit start is
only required when switching workspaces or on a cold session.

## Step 0 — Verify indexing is complete (mandatory)

**Do not skip this step.** An under-indexed workspace returns `[]` for
symbols that ARE referenced, producing false dead-code candidates.

Pick one symbol you know is actively used (e.g. the primary constructor,
a widely-called utility function). Call `find_references` on it:

```
mcp__lsp__find_references({
  "file_path": "/abs/path/to/file.go",
  "line": <known-active symbol line>,
  "column": <known-active symbol column>,
  "include_declaration": false
})
```

**If this returns `[]`:** the workspace is not indexed. Wait 3–5 seconds
and retry. Do not proceed until a known-active symbol returns ≥1 reference.
If it never returns results after 15 seconds, restart the LSP server with
`mcp__lsp__restart_lsp_server` and re-open the target file.

## Step 1 — Open the file and enumerate symbols

Open the file so the language server tracks it, then fetch all symbols:

```
mcp__lsp__open_document({ "file_path": "/abs/path/to/file.go" })

mcp__lsp__list_symbols({ "file_path": "/abs/path/to/file.go" })
```

Collect the full symbol list. Filter to **exported symbols only** using the
language-appropriate rule from the table above.

**Coordinate note:** `list_symbols` returns 1-based coordinates.
Pass `selectionRange.start.line` and `selectionRange.start.character`
directly to `find_references` — no conversion needed.

**"no identifier found" error:** This means the column points to whitespace
or a keyword rather than the identifier name. This happens with methods
whose receiver prefix shifts the name rightward (e.g. `func (c *Client) MethodName`
— the name starts at column 21, not column 1). Fix: grep the declaration
line for the symbol name to find its exact column:

```
grep -n "MethodName" file.go
# count characters to find the 1-based column of the name
```

Then retry `find_references` with the corrected column.

## Step 2 — Check references for each exported symbol

For each exported symbol, call `find_references` with
`include_declaration: false` so the definition site itself is excluded
from the count. A count of 0 means no callers, not no occurrences.

```
mcp__lsp__find_references({
  "file_path": "/abs/path/to/file.go",
  "line": <selectionRange.start.line>,
  "column": <selectionRange.start.character>,
  "include_declaration": false
})
```

Record the result for each symbol:
```
{ symbol_name, kind, line, reference_count, locations[] }
```

**Batching note:** For files with many exported symbols (>20), process in
batches of 5–10 to avoid overwhelming the LSP server.

**Zero-reference cross-check (required before classifying as dead):**
When `find_references` returns `[]` for a symbol that looks foundational
(a handler, a constructor, a type used as a field), do not trust LSP alone.
LSP can miss references made through value-passing, interface satisfaction,
or function registration patterns (e.g. `server.AddResource(HandleFoo)`).
Before classifying as dead, run a text search in the primary wiring files:

```
grep -r "SymbolName" main.go server.go cmd/ internal/
```

If grep finds the name in a registration or assignment context, the symbol
is active — LSP just couldn't resolve the indirect reference. Update your
classification accordingly.

## Step 3 — Classify and report

Classify each exported symbol by reference count:

- **Zero references (LSP + grep)** — confirmed dead candidate. Flag with WARNING.
- **Zero LSP, found by grep** — active via registration/value pattern. Mark as ACTIVE.
- **1–2 references** — review manually. May be test-only usage.
- **3+ references** — active symbol. Not dead code.

For test-only references: if all locations are in `_test.go` files (Go) or
files named `*.test.*` / `*.spec.*`, mark the symbol as "test-only" in
the report rather than "zero-reference".

Produce the Dead Code Report using the format in
[references/patterns.md](references/patterns.md).

## Caveats

The following cases produce zero LSP references even though the symbol IS
used at runtime. Do not delete any zero-reference candidate without
manual review:

1. **Incomplete indexing.** `find_references` only searches files open or
   indexed by the language server. If the workspace is partially indexed,
   results may be incomplete. The Step 0 warm-up check catches this.

2. **Registration patterns.** Symbols passed as values to registration
   functions (e.g. `server.AddTool(HandleFoo)`, `http.HandleFunc("/", handler)`)
   appear as zero LSP references from the *definition site* because gopls
   tracks the call to the registrar, not the handler name. Always grep
   wiring files for zero-reference handlers before classifying as dead.

3. **Reflection and dynamic dispatch.** Symbols used via reflection
   (`reflect.TypeOf` in Go, `Class.forName` in Java) or dynamic dispatch
   have no static call sites visible to the LSP.

4. **`//go:linkname` and assembly.** Go symbols linked via `//go:linkname`
   or referenced from assembly files will show zero LSP references.

5. **Library public API.** Exported symbols called from external packages
   not present in the workspace will show zero references even if
   consumers exist.

6. **Declaration excluded from count.** The definition site is not counted
   (`include_declaration: false`). A count of 0 means no callers found,
   not that the symbol never appears in the source tree.

7. **Always review before deleting.** Zero LSP references is a signal to
   investigate, not a guarantee the symbol is unused.

## Step 4 — Next steps

After generating the report:

- **For each zero-reference symbol (confirmed by grep):** Run `lsp-impact`
  on the symbol to confirm. If `lsp-impact` also finds zero references, it
  is safe to consider for removal. Still check the Caveats section above.

- **For symbols with only test-file references:** Mark as "test-only" in
  the report. These may be candidates for removal if the tests themselves
  are redundant, but should not be deleted without reviewing whether the
  tests serve a documentation or contract purpose.

- **For symbols with 1–2 references in production code:** These are likely
  active but lightly used. Do not remove without checking whether they are
  part of a committed public API.

## Step 5 — Optional cleanup with `safe_delete_symbol`

After reviewing the dead code report and confirming candidates with the user,
you may offer to remove confirmed zero-reference symbols using `safe_delete_symbol`:

```
mcp__lsp__safe_delete_symbol({
  "file_path": "/abs/path/to/file.go",
  "symbol_path": "DeadFunction"
})
```

This tool performs its own reference check before deleting. If any references
exist (even ones missed in the initial scan), the deletion is refused.

**Requirements before using this step:**

1. The user has explicitly confirmed they want the symbol removed.
2. The symbol was classified as a confirmed dead candidate (zero LSP + zero grep references).
3. You have reviewed the Caveats section above and communicated relevant risks.

Do NOT auto-delete symbols without user confirmation. Present the dead code
report first, let the user select which symbols to remove, then execute
`safe_delete_symbol` for each approved removal.
