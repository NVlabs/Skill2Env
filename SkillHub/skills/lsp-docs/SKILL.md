---
name: lsp-docs
description: Three-tier documentation lookup for any symbol — hover → offline toolchain doc → source definition. Use when hover text is absent, insufficient, or the symbol is in an unindexed dependency.
argument-hint: "[symbol-name]"
user-invocable: true
allowed-tools: mcp__lsp__inspect_symbol mcp__lsp__get_symbol_documentation mcp__lsp__go_to_definition mcp__lsp__get_symbol_source
license: MIT
compatibility: Requires the agent-lsp MCP server (github.com/blackwell-systems/agent-lsp)
metadata:
  required-capabilities: hoverProvider
  optional-capabilities: definitionProvider
---

> Requires the agent-lsp MCP server.

# lsp-docs

Three-tier documentation lookup for any symbol. Works when the language server
is unavailable, when hover returns empty results, or when the symbol lives in a
transitive dependency that gopls or pyright does not index.

Read-only — does not modify any files.

**Invocation:** User provides `symbol_name` in fully-qualified form (e.g.
`"fmt.Println"`, `"std::vec::Vec::new"`, `"os.path.join"`). Optionally provide
`file_path` for any file in the same module, which improves Go package resolution.

---

## Decision table

| Situation | Recommended tier |
|-----------|-----------------|
| Symbol in current workspace | Tier 1 (hover) |
| Symbol in direct dependency | Tier 2 (toolchain doc) |
| Symbol in transitive dep (not indexed by LSP) | Tier 2 |
| No LSP server available | Tier 2 → Tier 3 |
| No toolchain installed (e.g., Rust without cargo) | Tier 3 |

---

## Tier 1 — LSP hover (fast, live, position-based)

Call `inspect_symbol` with the file path and cursor position (1-based).

```
mcp__lsp__inspect_symbol({
  "file_path": "/abs/path/to/file.go",
  "line": 42,
  "column": 8
})
```

If the result contains a non-empty `contents` field with useful type and doc
information, **stop here and return it**. Hover is the fastest path and should
always be tried first.

If hover returns empty `contents`, or the language server is not initialized,
proceed to Tier 2.

---

## Tier 2 — Offline toolchain documentation (authoritative, name-based)

Call `get_symbol_documentation` with the fully-qualified symbol name and
`language_id`. This fetches documentation from the local toolchain (go doc,
pydoc, cargo doc) without requiring an LSP session. Works for transitive
dependencies that the language server does not index.

```
mcp__lsp__get_symbol_documentation({
  "symbol": "fmt.Println",
  "language_id": "go",
  "file_path": "/abs/path/to/any/file/in/the/module.go",  // optional, improves Go pkg resolution
  "format": "markdown"   // optional: wraps signature in code fence
})
```

**Interpreting the result:**

- If `source == "toolchain"`: return the `doc` and `signature` fields to the
  user. These are authoritative — sourced directly from the installed toolchain,
  ANSI-stripped, and ready for display.
- If `source == "error"`: note the `error` field (toolchain failure reason) and
  proceed to Tier 3.

---

## Tier 3 — Source definition (last resort)

Call `go_to_definition` to navigate to the symbol definition, then call
`get_symbol_source` to extract the source text. This always works when the
symbol exists in the workspace or module cache, even without a language server.

```
mcp__lsp__go_to_definition({
  "file_path": "/abs/path/to/caller.go",
  "line": 42,
  "column": 8
})
// → returns definition location

mcp__lsp__get_symbol_source({
  "file_path": "<definition file from above>",
  "line": <definition line from above>
})
// → returns full function/type source text
```

Present the source text to the user with a note that it is raw source, not
rendered documentation.

---

## lsp-impact integration note

Before running `lsp-impact` on an unfamiliar symbol, call
`get_symbol_documentation` to understand its signature and semantics. This
prevents misinterpreting the impact report due to incorrect assumptions about
what the symbol does.

---

## Example

```
Goal: look up documentation for http.ListenAndServe in a Go project

Tier 1 — inspect_symbol: cursor on "ListenAndServe" in main.go:14:6
  → contents: "" (empty — server not initialized)
  Proceed to Tier 2.

Tier 2 — get_symbol_documentation:
  symbol: "net/http.ListenAndServe"
  language_id: "go"
  file_path: "/Users/you/code/myapp/main.go"
  format: "markdown"

  Result:
  {
    "symbol": "net/http.ListenAndServe",
    "language": "go",
    "source": "toolchain",
    "doc": "func ListenAndServe(addr string, handler http.Handler) error\n\nListenAndServe listens on the TCP network address addr and then calls Serve...",
    "signature": "func ListenAndServe(addr string, handler http.Handler) error",
    "error": ""
  }

  source == "toolchain" → return doc and signature to user. Done.

Tier 3 — skipped (Tier 2 succeeded)
```
