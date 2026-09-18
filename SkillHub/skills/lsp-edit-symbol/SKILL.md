---
name: lsp-edit-symbol
description: "Edit a named symbol without knowing its file or position. Use when you want to change a function, type, or variable by name and don't have exact coordinates. Resolves the symbol to its definition, retrieves its full range, and applies the edit."
argument-hint: "[symbol-name] [new-body-or-signature]"
user-invocable: true
allowed-tools:
  - mcp__lsp__find_symbol
  - mcp__lsp__list_symbols
  - mcp__lsp__apply_edit
  - mcp__lsp__replace_symbol_body
license: MIT
compatibility: Requires the agent-lsp MCP server (github.com/blackwell-systems/agent-lsp)
metadata:
  required-capabilities: workspaceSymbolProvider
---

# lsp-edit-symbol

Edit a named symbol (function, type, variable) without needing its exact file path
or line/column. Primary path uses `replace_symbol_body` for direct symbol replacement.
Falls back to `find_symbol` + `list_symbols` + `apply_edit` when
the server does not support document symbols well.

## Workflow

### Step 1 — Locate the file

```json
{ "tool": "find_symbol", "query": "MyFunc" }
```

Returns a list of matching symbols with file URI and position. Pick the definition
(not a test file, not a stub). If multiple matches, use the container name or file
path to disambiguate.

### Step 2 — Replace the symbol body (primary path)

Use `replace_symbol_body` to replace the entire function/method/type body by name:

```json
{
  "tool": "replace_symbol_body",
  "file_path": "/path/to/file.go",
  "symbol_path": "MyFunc",
  "new_body": "func MyFunc() error {\n\treturn nil\n}"
}
```

For methods, use dot notation: `"MyStruct.Method"`.

This resolves the symbol by name within the file, finds its full range, and replaces
it atomically. No position math required.

**If `replace_symbol_body` fails** (e.g., the server cannot resolve document symbols
for this file), fall back to the manual path below.

### Fallback — Manual resolution via document symbols

**Step 2b — Get the full range:**

```json
{
  "tool": "list_symbols",
  "file_path": "/path/to/file.go",
  "language_id": "go"
}
```

Find `MyFunc` in the returned tree. The `range` field covers the entire symbol
including its body; `selectionRange` covers only the name.

**Step 3b — Apply the edit:**

Option A (text-match, recommended when you have the old text):
```json
{
  "tool": "apply_edit",
  "file_path": "/path/to/file.go",
  "old_text": "func MyFunc() {",
  "new_text": "func MyFunc() error {"
}
```

Option B (positional, when you have the exact range):
```json
{
  "tool": "apply_edit",
  "workspace_edit": {
    "changes": {
      "file:///path/to/file.go": [{
        "range": { "start": {"line": 12, "character": 0}, "end": {"line": 18, "character": 1} },
        "newText": "func MyFunc() error {\n\treturn nil\n}"
      }]
    }
  }
}
```

## Decision guide

| Situation | Approach |
|-----------|----------|
| Replacing full body | `replace_symbol_body` (primary path) |
| Changing signature only | Step 1 + apply_edit with one-line old_text |
| Symbol name ambiguous | Use `find_symbol` query + container name filter |
| Server lacks document symbols | Fallback path (Step 2b + 3b) |
| After edit | Run `get_diagnostics` to verify no errors introduced |

## Notes

- `replace_symbol_body` is the preferred path for full-body replacements. It handles
  symbol resolution and range calculation internally.
- `find_symbol` returns declaration sites, not all references. The
  first non-test result is usually the definition.
- Positions in `list_symbols` are **1-based** (shifted from LSP convention).
  `apply_edit` `workspace_edit` expects **0-based**; subtract 1 when using positional
  mode (Option B). Text-match mode (Option A) requires no position math.
- For renames (not edits), use `/lsp-rename` instead; it updates all call sites.
