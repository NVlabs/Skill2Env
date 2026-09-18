---
name: lsp-fix-all
description: Apply available quick-fix code actions for all current diagnostics in a file, one at a time with re-collection between each fix. Use to bulk-resolve errors and warnings the language server can fix automatically.
argument-hint: "[file-path]"
user-invocable: true
allowed-tools: mcp__lsp__get_diagnostics mcp__lsp__suggest_fixes mcp__lsp__apply_edit mcp__lsp__open_document mcp__lsp__format_document
license: MIT
compatibility: Requires the agent-lsp MCP server (github.com/blackwell-systems/agent-lsp)
metadata:
  required-capabilities: codeActionProvider
  optional-capabilities: documentFormattingProvider
---

> Requires the agent-lsp MCP server.

# lsp-fix-all

Apply available quick-fix code actions for all current diagnostics in a file,
one at a time, re-collecting diagnostics between each fix because line numbers
shift after each application.

**Important distinction from `/lsp-safe-edit`:** This skill fixes **pre-existing**
diagnostics in a file — errors and warnings that already exist before any edit
session begins. `/lsp-safe-edit` has a code-action step (Step 7) for fixing errors
**introduced by a specific edit you just made**. Use this skill for systematic
bulk-fixing of existing issues, independent of any edit session.

## When to use / not use

**Use this skill when:**
- A file has accumulated errors or warnings you want to resolve automatically
- You want to clean up a file before starting new work
- You want to apply all available language-server quick-fixes in bulk

**Do NOT use this skill when:**
- You just made an edit and want to fix newly introduced errors — use `/lsp-safe-edit`
- You want to apply structural refactors — this skill applies quick-fixes only (see filtering below)
- The file has zero diagnostics (the skill will report clean and stop)

## Input

- **file_path:** Absolute path to the file to fix.

---

## Workflow

### Step 1 — Open and collect initial diagnostics

Call `mcp__lsp__open_document` with the target file path to ensure it is loaded
in the language server. Then call `mcp__lsp__get_diagnostics` to retrieve all
current diagnostics.

If zero diagnostics are returned: report "No diagnostics found — file is clean."
and stop. No further steps are needed.

Record the initial count of errors and warnings for the summary output.

### Step 2 — Classify and filter code actions

For EACH diagnostic (process one at a time, not in batch):

1. Call `mcp__lsp__suggest_fixes` at the diagnostic's position/range.
2. Filter the returned actions to quick-fix kind only.
3. Skip any diagnostic for which no applicable quick-fix exists — note it in the summary.

**Decision gate — which code actions to apply:**

| Action kind | Apply? |
|---|---|
| `quickfix` | YES |
| `quickfix.*` | YES |
| `refactor` | NO — structural change |
| `refactor.extract` | NO — structural change |
| `refactor.inline` | NO — structural change |
| `source.organizeImports` | YES — safe formatting |
| `source.*` (others) | NO — skip unless organizeImports |
| (no kind / empty) | NO — unknown, skip |

A code action qualifies if: `kind == "quickfix"`, OR `kind` starts with `"quickfix."`,
OR `kind == "source.organizeImports"`.

Reject actions whose kind is `"refactor"`, starts with `"refactor."`, or has no
kind field at all.

### Step 3 — Apply one fix and re-collect (the core loop)

This is the critical correctness constraint: **never apply more than one fix per
iteration.** After each `apply_edit` call, line numbers in the file shift. Always
re-call `get_diagnostics` before processing the next diagnostic.

**Loop:**

```
iteration = 0
max_iterations = 50

while iteration < max_iterations:
    diagnostics = mcp__lsp__get_diagnostics(file_path)
    if diagnostics is empty: break

    for each diagnostic in diagnostics:
        actions = mcp__lsp__suggest_fixes(diagnostic.range)
        applicable = filter to quickfix / source.organizeImports kinds (see Step 2)
        if applicable is not empty:
            apply the first applicable action via mcp__lsp__apply_edit
            record: (line, message, action title) in "Fixed" list
            iteration += 1
            break  # restart the outer loop — line numbers have shifted

    if no diagnostic in this pass had an applicable quick-fix:
        break  # no progress possible — exit loop
```

Exit the loop when:
- The diagnostics list is empty, OR
- No remaining diagnostic has an applicable quick-fix action, OR
- The iteration counter reaches 50 (safety guard against edge cases where a
  fix introduces a new fixable diagnostic, preventing infinite loops)

If `apply_edit` returns an error: stop the loop immediately and report the
failure in the summary. Do not attempt further fixes.

### Step 4 — Verify and format

After the loop exits:

1. Call `mcp__lsp__get_diagnostics` one final time to capture the post-fix state.
2. For any remaining diagnostics that had no applicable quick-fix, list them in
   the "Skipped" section with explanation.
3. Call `mcp__lsp__format_document` to clean up any indentation drift introduced
   by the applied edits.

### Output format

```
## lsp-fix-all Summary

File: /path/to/file.go
Initial diagnostics: N errors, M warnings
Fixes applied: K
Remaining (no auto-fix available): J

### Fixed
- line X: <message> → applied: <action title>

### Skipped (no quick-fix available)
- line Y: <message>
```

If `apply_edit` failed mid-loop, append:

```
### Loop stopped
- apply_edit returned error on line Z: <error message>
- Fixes applied before failure: K
```

---

## Safety rules

- Never apply more than one code action per loop iteration
- Always re-collect diagnostics after each `apply_edit` before the next fix
- Never apply refactor or structural code actions — quick-fix and source.organizeImports only
- If `apply_edit` returns an error, stop the loop and report the failure; do not continue
- Maximum iterations: 50 (safety guard against infinite loops in edge cases where a fix introduces a new fixable diagnostic)
- Do not use `execute_command` — `apply_edit` is sufficient for all quick-fixes

---

## Prerequisites

LSP must be running for the target workspace. If not yet initialized, call
`mcp__lsp__start_lsp` with the workspace root before proceeding.

Auto-init note: agent-lsp supports workspace auto-inference from file paths.
Explicit `start_lsp` is only needed when switching workspace roots.
