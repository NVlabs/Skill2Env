# Shared LSP Skill Patterns

## @@ Position Marker

When calling position-based tools (inspect_symbol, go_to_definition,
find_references), prefer the position_pattern parameter over line/column:

    "position_pattern": "func (c *LSPClient) Initiali@@ze"

The @@ marker indicates cursor position (character immediately after @@).
More reliable than coordinate math. line/column still work as fallback.

## LineScope: Restricting position_pattern to a Line Range

When the same token appears multiple times in a file, `position_pattern` may
match the wrong occurrence. Use `line_scope_start` and `line_scope_end` to
restrict the search to a specific range:

    "position_pattern": "@@myVar",
    "line_scope_start": 40,
    "line_scope_end": 60

The match is restricted to lines 40–60 (inclusive, 1-indexed). The cursor
position returned is file-absolute — no adjustment needed.

**When to use:** any time the same token (variable name, method name, keyword)
appears in multiple places and you know the approximate line the symbol is on.
Use `list_symbols` or `go_to_symbol` first to get the line, then pass
`line_scope_start: line - 5, line_scope_end: line + 5` as a safe window.

**Omitting the args** (or passing 0 for both) falls back to full-file search —
all existing callers are unaffected.

## start_lsp Guard Pattern

Every skill that calls LSP tools SHOULD include a guard:
"If LSP is not yet initialized, call start_lsp with the workspace root first."

Auto-init note: agent-lsp supports workspace auto-inference from file paths.
Explicit start_lsp only needed when switching workspace roots.

## Diagnostic Diff Output Format

    ## Diagnostic Summary
    - Errors introduced:   N  (each as: file:line - message)
    - Errors resolved:     N  (each as: file:line - message)
    - Net change:         +N / -N / 0
    - Warnings introduced: N (only if N > 0)
    - Warnings resolved:   N (only if N > 0)

Rules: only show sections where N > 0. Net change of 0 = safe to proceed.
