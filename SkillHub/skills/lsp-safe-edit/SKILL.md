---
name: lsp-safe-edit
description: Wrap any code edit with before/after diagnostic comparison. Speculatively previews the change first (preview_edit), then applies to disk only if the error delta is acceptable. If post-edit errors appear, surfaces code actions for quick fixes. Handles single and multi-file edits.
user-invocable: true
allowed-tools: mcp__lsp__start_lsp mcp__lsp__open_document mcp__lsp__get_diagnostics mcp__lsp__preview_edit mcp__lsp__simulate_chain mcp__lsp__suggest_fixes mcp__lsp__format_document mcp__lsp__apply_edit Edit Write Bash
license: MIT
compatibility: Requires the agent-lsp MCP server (github.com/blackwell-systems/agent-lsp)
metadata:
  optional-capabilities: codeActionProvider documentFormattingProvider
  tool_permissions:
    phases:
      setup:
        description: "Open files and capture baseline diagnostics"
        allowed:
          - "mcp__lsp__start_lsp"
          - "mcp__lsp__open_document"
          - "mcp__lsp__get_diagnostics"
        forbidden:
          - "mcp__lsp__apply_edit"
          - "Edit"
          - "Write"
      speculative_preview:
        description: "Simulate the edit in memory before touching disk"
        allowed:
          - "mcp__lsp__preview_edit"
          - "mcp__lsp__simulate_chain"
        forbidden:
          - "mcp__lsp__apply_edit"
          - "Edit"
          - "Write"
      apply:
        description: "Write the change to disk"
        allowed:
          - "Edit"
          - "Write"
          - "mcp__lsp__apply_edit"
        forbidden:
          - "mcp__lsp__simulate_*"
      verify_and_fix:
        description: "Collect post-edit diagnostics, surface code actions, format"
        allowed:
          - "mcp__lsp__get_diagnostics"
          - "mcp__lsp__suggest_fixes"
          - "mcp__lsp__apply_edit"        # for applying code action fixes
          - "mcp__lsp__format_document"
        forbidden:
          - "mcp__lsp__simulate_*"
          - "mcp__lsp__run_build"
          - "mcp__lsp__run_tests"
    global_forbidden:
      - "mcp__lsp__rename_symbol"          # safe-edit uses direct edits
      - "mcp__lsp__blast_radius"      # blast radius is lsp-impact's job
---

> Requires the agent-lsp MCP server.

# lsp-safe-edit

Wrap any code edit with a before/after diagnostic comparison. Speculatively
previews the change in-memory before touching disk, then diffs errors introduced
vs. resolved after applying. If errors appear, surfaces code actions to fix them.

## Prerequisites

LSP must be running for the target workspace. If not yet initialized, call
`mcp__lsp__start_lsp` with the workspace root before proceeding.

Auto-init note: agent-lsp supports workspace auto-inference from file paths.
Explicit `start_lsp` is only needed when switching workspace roots.

## Input

- **target file(s):** One or more files to be edited (absolute paths).
- **description of change:** What you intend to edit and why.

---

## Workflow

### Step 1 — Open target file(s)

Call `mcp__lsp__open_document` for each file that will be edited:

```
mcp__lsp__open_document(file_path: "/abs/path/to/file.go", language_id: "go")
```

### Step 2 — Capture baseline diagnostics (BEFORE)

Call `mcp__lsp__get_diagnostics` for each target file. Store as BEFORE.
For multi-file edits, collect diagnostics for all files involved.

```
BEFORE = mcp__lsp__get_diagnostics(file_path: "/abs/path/to/file.go")
```

If the server returns an empty list immediately after open, wait briefly and
retry — LSP analysis is async.

### Step 3 — Speculative preview (preview_edit)

Before touching disk, call `mcp__lsp__preview_edit` to preview the
error delta of the intended change:

```
mcp__lsp__preview_edit(
  file_path: "/abs/path/to/file.go",
  start_line: <N>,
  start_column: <col>,
  end_line: <N>,
  end_column: <col>,
  new_text: "<replacement text>"
)
```

Returns `net_delta` (new errors introduced minus errors resolved) without
writing to disk.

**Decision:**

| `net_delta` | Action |
|-------------|--------|
| ≤ 0 | Proceed — edit improves or does not worsen error state |
| > 0 | **Pause.** Report introduced errors to user and ask: "Proceed anyway? [y/n]" |

If `net_delta > 0` and user says "n", stop. Do not apply the edit.

**Multi-file edits:** `preview_edit` covers one file at a time. For
edits spanning multiple files, run it for each file independently and sum the
deltas. If any file shows `net_delta > 0`, pause before continuing.

**When to skip Step 3:** If the intended change is a new file (Write), there is
no existing file to simulate against. Skip to Step 4.

### Step 3b — Refactor preview with simulate_chain (renames and signature changes)

Use this step **instead of or after** Step 3 when the change is a rename,
signature change, or any edit with dependent follow-on edits (e.g., updating
all call sites after adding a parameter).

`simulate_chain` applies a sequence of speculative edits in-memory and reports
whether the cumulative change is safe — without touching disk:

```
mcp__lsp__simulate_chain({
  "workspace_root": "/abs/path/to/workspace",
  "language": "go",
  "edits": [
    {
      "file_path": "/abs/path/to/file.go",
      "start_line": <N>, "start_column": <col>,
      "end_line": <N>,   "end_column": <col>,
      "new_text": "<replacement>"
    },
    // additional dependent edits (e.g. call site updates) ...
  ]
})
```

Returns:
- `cumulative_delta` — net error change across all steps
- `safe_to_apply_through_step` — how many steps are safe to apply in sequence

**Decision:**

| `cumulative_delta` | `safe_to_apply_through_step` | Action |
|--------------------|------------------------------|--------|
| ≤ 0 | = total steps | All steps safe. Proceed to Step 4. |
| ≤ 0 | < total steps | Safe up to that step. Review remaining steps. |
| > 0 | any | Net regression. Report to user before proceeding. |

**When to use Step 3b:**
- Renaming an exported symbol and updating its call sites
- Adding/removing a parameter and updating all callers
- Any multi-file refactor where edits are order-dependent

**When to skip Step 3b:**
- Simple in-place edits with no dependent follow-on edits (Step 3 is sufficient)
- New file creation (no existing text to simulate against)

### Step 4 — Apply the edit to disk

Apply the change using the Edit or Write tool:

- Use `Edit` for targeted replacements in an existing file.
- Use `Write` only when creating a new file or doing a full rewrite.

```
Edit(file_path: "/abs/path/to/file.go", old_string: "...", new_string: "...")
```

For multi-file edits, apply each file's changes before collecting post-edit
diagnostics (Step 5). If any individual edit fails, stop and report before
applying remaining files.

### Step 5 — Capture post-edit diagnostics (AFTER)

Call `mcp__lsp__get_diagnostics` again for each edited file. Store as AFTER.

```
AFTER = mcp__lsp__get_diagnostics(file_path: "/abs/path/to/file.go")
```

For multi-file edits, collect diagnostics for all files and merge the results.

### Step 6 — Compute the diagnostic diff

Compare BEFORE and AFTER:

- **Introduced** = diagnostics in AFTER not in BEFORE (new problems).
- **Resolved** = diagnostics in BEFORE not in AFTER (fixed problems).

Match by `(file, line, message)` tuple to handle line-number shifts. Treat
`error` and `warning` severity separately.

### Step 7 — Surface code actions if errors were introduced

If any new `error`-severity diagnostics appear, call `mcp__lsp__suggest_fixes`
at each error location to surface quick fixes:

```
mcp__lsp__suggest_fixes(
  file_path: "<file>",
  start_line: <error line>,
  start_column: 1,
  end_line: <error line>,
  end_column: 999
)
```

Report available code actions to the user:

```
Errors introduced (2):
  file.go:34 — undefined: MyType
    → Code action: Import "mypackage" (quickfix)
  file.go:51 — cannot use int as string
    → No code actions available

Apply code actions? [y/n/select]
```

If the user accepts, apply the code action's `WorkspaceEdit` via
`mcp__lsp__apply_edit`, then re-collect diagnostics and re-diff.

### Step 8 — Format (optional)

If the diagnostic diff is clean (net change ≤ 0), offer to format the edited
file via the language server:

```
mcp__lsp__format_document({ "file_path": "/abs/path/to/file" })
```

Returns `TextEdit[]`. If non-empty, apply immediately:

```
mcp__lsp__apply_edit({ "workspace_edit": <TextEdit[]> })
```

Skip if the user did not ask for formatting, or if there are unresolved errors
(fix errors before formatting).

### Step 9 — Report using DiagnosticDiffFormat

Output the final summary:

```
## Edit Summary

Files changed: N
Errors introduced: A  →  Errors resolved: B  (net: A-B)
Warnings introduced: C  →  Warnings resolved: D

### Introduced errors
- file.go:34 — undefined: MyType

### Resolved errors
- file.go:12 — unused variable: x
```

---

## Decision Guide

| Net change | Action |
|------------|--------|
| 0 | Safe. No new errors. |
| Negative | Net improvement — errors resolved. Safe. |
| Positive (after code actions) | **Do NOT commit.** Offer to revert. |

When net change > 0 after code actions:

1. Show the full list of remaining introduced errors.
2. Offer to revert using the original `old_string` in a follow-up `Edit` call.
3. Wait for user decision before proceeding.

Do not commit or stage files when net change > 0.

---

## Multi-file workflow

For edits spanning multiple files (e.g., changing a function signature and all
its call sites):

1. **Open all files** in Step 1.
2. **Collect BEFORE diagnostics** for all files.
3. **Simulate each file** independently in Step 3 — sum `net_delta` values.
4. **Apply edits file by file** in Step 4 — stop on first failure.
5. **Collect AFTER diagnostics** for all files and merge.
6. **Check code actions** on any file showing new errors.

Report the combined diagnostic diff across all files in the final summary.
