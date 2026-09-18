---
name: lsp-format-code
description: Format a file or selection using the language server's formatter. Use before committing to apply consistent style, or after generating code to clean up indentation and spacing. Supports full-file and range-based formatting.
argument-hint: "[file-path] [optional: start_line-end_line]"
user-invocable: true
allowed-tools: mcp__lsp__open_document mcp__lsp__format_document mcp__lsp__format_range mcp__lsp__apply_edit mcp__lsp__get_diagnostics mcp__lsp__get_server_capabilities
license: MIT
compatibility: Requires the agent-lsp MCP server (github.com/blackwell-systems/agent-lsp)
metadata:
  required-capabilities: documentFormattingProvider
  optional-capabilities: documentRangeFormattingProvider
---

> Requires the agent-lsp MCP server.

# lsp-format-code

Format a file or selection using the language server's formatter — the same
formatting engine your IDE uses. Applies language-specific rules (gofmt, prettier,
rustfmt, black) without requiring those tools to be on PATH separately.

## When to use

- Before committing: ensure consistent style across edited files
- After generating code: clean up AI-generated indentation and spacing
- After a refactor that shifted indentation levels
- When a linter flags style violations fixable by the formatter

Use `/lsp-safe-edit` instead when you are making a logic change and want
before/after diagnostic comparison alongside the edit.

---

## Workflow

### Step 1 — Check formatting is supported (optional)

If unsure whether the language server supports formatting for this file, check
capabilities first:

```
mcp__lsp__get_server_capabilities({ "file_path": "<file>" })
```

Look for `documentFormattingProvider` (full-file) and
`documentRangeFormattingProvider` (range). If neither is present, the server
does not support formatting — stop and report.

Skip this step if you know the language supports formatting (Go, TypeScript,
Rust, Python all do via their standard servers).

### Step 2 — Open the file

```
mcp__lsp__open_document({ "file_path": "/abs/path/to/file.go", "language_id": "go" })
```

### Step 3 — Request formatting edits

**Full file:**
```
mcp__lsp__format_document({ "file_path": "/abs/path/to/file.go" })
```

**Selection only:**
```
mcp__lsp__format_range({
  "file_path": "/abs/path/to/file.go",
  "start_line": <N>,
  "end_line": <M>
})
```

Both return `TextEdit[]` — a list of replacements to apply. They do **not**
write to disk. If the list is empty, the file is already correctly formatted.

### Step 4 — Apply the edits

Pass the `TextEdit[]` from Step 3 to `apply_edit`:

```
mcp__lsp__apply_edit({ "workspace_edit": <TextEdit[] from Step 3> })
```

This writes the formatting changes to disk.

### Step 5 — Verify (optional but recommended)

Call `get_diagnostics` to confirm formatting did not introduce any errors:

```
mcp__lsp__get_diagnostics({ "file_path": "/abs/path/to/file.go" })
```

Formatting should never introduce errors — if it does, report immediately
without committing.

---

## Output format

```
## Format result: <filename>

Changes applied: N edits
Lines affected: <range or "whole file">
Formatter: <gopls | typescript-language-server | rust-analyzer | ...>

Status: FORMATTED ✓
```

If no edits were returned:
```
Status: ALREADY FORMATTED — no changes needed
```

If formatting is not supported:
```
Status: NOT SUPPORTED — <server> does not expose documentFormattingProvider
Fallback: run the formatter directly (gofmt, prettier, rustfmt, etc.)
```

---

## Multi-file formatting

For formatting multiple files (e.g. all files changed in a PR):

1. Call `format_document` for each file — these can run in parallel.
2. Collect all `TextEdit[]` responses.
3. Apply each file's edits via `apply_edit` sequentially.
4. Report total edits across all files.

Do not apply edits from multiple files in a single `apply_edit` call —
apply per-file to keep changes scoped and reversible.

---

## Decision guide

| Situation | Action |
|-----------|--------|
| Formatting a whole file before commit | `format_document` → `apply_edit` |
| Formatting only generated code in a function | `format_range` with the function's line range |
| Empty `TextEdit[]` returned | File is already formatted — no action needed |
| Server doesn't support formatting | Report and suggest running CLI formatter directly |
| Formatting introduces diagnostics | Do not commit — report immediately |
| Formatting a Go file in a workspace repo | Ensure `GOWORK=off` is set if running via shell fallback |

---

## Language notes

| Language | Formatter | Server |
|----------|-----------|--------|
| Go | `gofmt` (via gopls) | `gopls` |
| TypeScript / JavaScript | `prettier` or built-in (via typescript-language-server) | `typescript-language-server` |
| Rust | `rustfmt` (via rust-analyzer) | `rust-analyzer` |
| Python | `black` or `autopep8` (via pyright/pylsp) | `pyright-langserver` or `pylsp` |
| C / C++ | `clang-format` (via clangd) | `clangd` |

The language server delegates to the language's standard formatter — results
match what your IDE would produce.
