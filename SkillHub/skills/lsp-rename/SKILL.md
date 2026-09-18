---
name: lsp-rename
description: Two-phase safe rename across the entire workspace. Use when renaming any symbol, function, method, variable, type, or identifier — shows all affected sites before executing atomically via LSP. Never renames without confirmation.
argument-hint: "[old-name] [new-name]"
user-invocable: true
allowed-tools: mcp__lsp__go_to_symbol mcp__lsp__prepare_rename mcp__lsp__find_references mcp__lsp__rename_symbol mcp__lsp__apply_edit mcp__lsp__get_diagnostics
license: MIT
compatibility: Requires the agent-lsp MCP server (github.com/blackwell-systems/agent-lsp)
metadata:
  required-capabilities: referencesProvider renameProvider workspaceSymbolProvider
  tool_permissions:
    phases:
      prerequisites:
        description: Initialize LSP if needed
        allowed: ["mcp__lsp__start_lsp"]
        forbidden: []
      preview:
        description: "Locate symbol, validate rename, enumerate references, dry-run"
        allowed:
          - "mcp__lsp__go_to_symbol"
          - "mcp__lsp__prepare_rename"
          - "mcp__lsp__find_references"
          - "mcp__lsp__rename_symbol"    # dry_run=true only
        forbidden:
          - "mcp__lsp__apply_edit"
          - "Edit"
          - "Write"
      execute:
        description: "Capture pre-rename diagnostics, execute rename, apply, verify"
        allowed:
          - "mcp__lsp__get_diagnostics"
          - "mcp__lsp__rename_symbol"    # dry_run=false
          - "mcp__lsp__apply_edit"
        forbidden:
          - "mcp__lsp__simulate_*"
          - "mcp__lsp__run_build"
    global_forbidden:
      - "mcp__lsp__format_document"      # rename does not format
      - "mcp__lsp__run_tests"            # rename does not run tests
---

> Requires the agent-lsp MCP server.

# lsp-rename: Safe Symbol Rename

Renames a symbol across the workspace in two phases: preview first, then execute
only after explicit confirmation. Never renames without showing impact.

**Invocation:** User provides `old_name` (the symbol to rename) and `new_name`
(the replacement). Optionally provide `workspace_root` to scope the search.

---

## Prerequisites

If LSP is not yet initialized, call `mcp__lsp__start_lsp` with the workspace
root first. Auto-inference applies when file paths are provided, but an explicit
start is required when switching workspaces.

---

## Phase 1: Preview

Find the symbol, enumerate all references, and produce a dry-run preview.
**Do not apply any edits in this phase.**

### Step 1 — Locate the symbol

Call `mcp__lsp__go_to_symbol` with `symbol_path` set to `old_name`:

```
mcp__lsp__go_to_symbol
  symbol_path: "old_name"        # or "Package.OldName" for qualified paths
  workspace_root: "<root>"       # optional; omit to search entire workspace
```

This returns the definition location (file, line, column). If not found, report
the error and stop.

### Step 2 — Validate rename is possible

Call `mcp__lsp__prepare_rename` at the definition location from Step 1:

```
mcp__lsp__prepare_rename
  file_path: "<file from Step 1>"
  line: <line from Step 1>
  column: <column from Step 1>
```

`prepare_rename` asks the language server whether a rename is valid at this
position. If it returns an error (e.g. the symbol is a keyword, a built-in, or
in a location the server cannot rename), **stop immediately** and report:

> Cannot rename `OldName`: <server error message>
> Common causes: built-in or keyword, imported external package, or position is
> not on the symbol name. Try locating the declaration site directly.

Only proceed to Step 3 if `prepare_rename` succeeds.

### Step 3 — Enumerate references

Call `mcp__lsp__find_references` at the definition location from Step 1:

```
mcp__lsp__find_references
  file_path: "<file from Step 1>"
  position_pattern: "<symbol>@@"   # @@ immediately after the symbol name
  # fallback: use line/column from Step 1 if position_pattern is unavailable
```

Collect all returned locations. Note the total count and the distinct files.

### Step 4 — Dry-run preview

Call `mcp__lsp__rename_symbol` with `dry_run=true`. **Do not call `apply_edit`.**

```
mcp__lsp__rename_symbol
  file_path: "<file from Step 1>"
  line: <line from Step 1>
  column: <column from Step 1>
  new_name: "<new_name>"
  dry_run: true
```

The response includes a `workspace_edit` with all proposed changes and a
`preview.note` describing the scope.

### Step 5 — Report impact and hard stop

Display the preview summary to the user:

```
Rename preview: OldName -> NewName
  Locations to update: N (from find_references count)
  Files affected:      M (distinct files in workspace_edit)
  Language server:     <gopls | typescript-language-server | rust-analyzer | ...>

Changes:
  path/to/file1.go  lines 12, 45, 78
  path/to/file2.go  line 3
  ...
```

**REQUIRED hard stop — do not proceed without explicit user confirmation:**

> Proceed with rename? [y/n]

Wait for user input. Do not apply any edit until the user answers "y" or "yes".

---

## Edge Case: 0 References

If `find_references` returns an empty list (the symbol exists but has no external
usages), warn the user before stopping:

> Warning: no references found for `OldName`. The symbol may be unexported,
> dead code, or the LSP index may be stale. Renaming will update only the
> declaration site.
> Proceed anyway? [y/n]

If user answers "n", stop. If "y", continue to Phase 2.

---

## Phase 2: Execute

Only enter this phase after the user answers "y" or "yes" to the confirmation
prompt in Phase 1.

### Step 1 — Capture pre-rename diagnostics

Before applying changes, capture the current diagnostic state:

```
mcp__lsp__get_diagnostics
  file_path: "<one or more files in the workspace_edit>"
```

Store the result as `before_diagnostics`.

### Step 2 — Execute rename

Call `mcp__lsp__rename_symbol` without `dry_run` (or with `dry_run=false`):

```
mcp__lsp__rename_symbol
  file_path: "<file from Phase 1 Step 1>"
  line: <line from Phase 1 Step 1>
  column: <column from Phase 1 Step 1>
  new_name: "<new_name>"
```

This returns a `workspace_edit` with the full set of changes.

### Step 3 — Apply the edit

Call `mcp__lsp__apply_edit` with the `workspace_edit` from Step 2:

```
mcp__lsp__apply_edit
  workspace_edit: <workspace_edit from rename_symbol>
```

### Step 4 — Check diagnostics

Call `mcp__lsp__get_diagnostics` on the affected files and compare against
`before_diagnostics`:

```
mcp__lsp__get_diagnostics
  file_path: "<affected files>"
```

Compute introduced vs. resolved errors and display the Diagnostic Summary (see
[references/patterns.md](references/patterns.md)).

---

## Output Format

After Phase 2 completes, display:

```
## Rename Summary
- Old name: OldName
- New name: NewName
- Files changed: M
- Locations updated: N
- Post-rename errors: 0
```

Follow with the Diagnostic Summary if any errors changed (format in
[references/patterns.md](references/patterns.md)).

Only show Diagnostic Summary sections where N > 0. A net change of 0 means the
rename is safe.

---

## Language Support

Tested with `gopls`, `typescript-language-server`, and `rust-analyzer`. Most
LSP-compliant servers support `textDocument/rename` — agent-lsp works with
any of the 30+ supported language servers that advertise rename capability.
Check your server's capability list via `mcp__lsp__get_server_capabilities` if
you are unsure.
