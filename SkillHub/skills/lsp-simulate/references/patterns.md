# lsp-simulate Reference Patterns

## Session Lifecycle State Machine

Sessions follow a linear lifecycle. Transitions are one-way; you cannot
move backward (e.g. re-edit after evaluate requires a new session).

```
create_simulation_session
         |
         v
      [created]
         |
         | simulate_edit / simulate_chain
         v
      [mutated]
         |
         | evaluate_session
         v
     [evaluated]
        / \
       /   \
  commit  discard
      \     /
       \   /
        v v
  [committed / discarded]
         |
         | destroy_session
         v
     [destroyed]

Any state --(revert failure / version mismatch)--> [dirty]
[dirty] --> destroy_session (only valid operation)
```

Always call `destroy_session` as the final step. Skipping it leaks server
resources — sessions are held in memory until destroyed or the server restarts.

## evaluate_session Response Fields

| Field              | Type    | Meaning                                                              |
|--------------------|---------|----------------------------------------------------------------------|
| net_delta          | int     | +N = N errors introduced; -N = N resolved; 0 = safe                 |
| confidence         | string  | Quality of the diagnostic result (see Confidence Interpretation)     |
| errors_introduced  | array   | New errors from the simulated edit (each: line, col, message, severity) |
| errors_resolved    | array   | Errors fixed by the simulated edit (same shape as errors_introduced) |
| edit_risk_score    | float   | 0.0 (no risk) to 1.0 (high risk); higher when exported symbols are affected |
| timeout            | bool    | true if diagnostics did not settle within timeout_ms                 |
| affected_symbols   | array   | Symbol names whose type-error count changed                          |
| duration_ms        | int     | Time taken for diagnostic collection                                 |
| scope              | string  | Scope used for evaluation: "file" or "workspace"                     |
| session_id         | string  | The session that was evaluated                                       |

Error/warning objects in `errors_introduced` and `errors_resolved`:

| Field    | Type   | Meaning                                  |
|----------|--------|------------------------------------------|
| line     | int    | 1-indexed line number in the file        |
| col      | int    | 1-indexed column number                  |
| message  | string | Diagnostic message text                  |
| severity | string | "error" or "warning"                     |

## preview_edit vs Full Session

**Use `preview_edit` when:**
- You have a single what-if edit to check
- You do not need to inspect the patch before applying
- You want minimal ceremony (no session management)

```
mcp__lsp__preview_edit(
  workspace_root: "/your/workspace",
  language: "go",
  file_path: "/abs/path/to/file.go",
  start_line: 42, start_column: 1,
  end_line: 42, end_column: 20,
  new_text: "replacement"
)
-- Returns the same shape as evaluate_session.
-- net_delta: 0 means safe to apply. Apply with the Edit or Write tool.
```

`preview_edit` creates a session, applies the edit, evaluates, and
destroys — all in one call. No cleanup required.

**Use a full session when:**
- You are applying multiple edits that build on each other (later edits depend on earlier ones)
- You want to review the generated patch (`commit_session(apply: false)`) before writing to disk
- You need to use `simulate_chain` to find the safe-to-apply boundary

## Confidence Interpretation

Confidence reflects how thoroughly LSP has analysed the changes.

| Confidence | Meaning                                                                         | Recommended action                                             |
|------------|---------------------------------------------------------------------------------|----------------------------------------------------------------|
| high       | File-scoped diagnostics fully settled. Result is reliable.                      | Trust net_delta. Commit if 0.                                  |
| eventual   | Workspace-scoped evaluation. Diagnostics may not be fully settled yet.          | Likely reliable. Re-evaluate with `scope: "workspace"` again if risk matters. |
| partial    | Evaluation timed out before diagnostics settled. Results are incomplete.        | Discard. Retry with a smaller scope or higher timeout_ms.      |
| stale      | Session was mutated again after evaluation started. Result is out of date.      | Discard. Re-evaluate after the current edits stabilize.        |

When `timeout: true` appears alongside `confidence: "partial"`, increase
`timeout_ms` (default: 3000 for file, 8000 for workspace) or switch to
`scope: "file"` for a faster, more reliable result.

## Position Convention

All position parameters are **1-indexed** throughout the simulation API:

- `start_line`, `end_line`: line numbers matching `cat -n` output and editor line numbers
- `start_column`, `end_column`: column numbers, 1 = first character on the line

This matches the agent-lsp convention used by all position-based tools
(`find_references`, `inspect_symbol`, `find_callers`, etc.).

Example: to replace text on line 10, columns 5–15:

```
start_line: 10, start_column: 5,
end_line: 10, end_column: 15
```

The range is half-open: `end_column` points to the character after the last
character to replace (same as LSP range convention).
