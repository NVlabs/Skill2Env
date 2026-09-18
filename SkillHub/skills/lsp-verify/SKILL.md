---
name: lsp-verify
description: Full three-layer verification after any change — LSP diagnostics + compiler build + test suite, ranked by severity. Use after completing any edit, refactor, or feature to confirm nothing is broken before committing.
user-invocable: true
allowed-tools: mcp__lsp__get_diagnostics mcp__lsp__run_build mcp__lsp__run_tests mcp__lsp__get_tests_for_file mcp__lsp__suggest_fixes mcp__lsp__format_document mcp__lsp__apply_edit
license: MIT
compatibility: Requires the agent-lsp MCP server (github.com/blackwell-systems/agent-lsp)
metadata:
  optional-capabilities: codeActionProvider documentFormattingProvider
  tool_permissions:
    phases:
      test_correlation:
        description: "Pre-step: map changed source files to their test files"
        allowed:
          - "mcp__lsp__get_tests_for_file"
        forbidden:
          - "mcp__lsp__apply_edit"
          - "Edit"
          - "Write"
      diagnostics:
        description: "Layer 1: collect LSP diagnostics for changed files"
        allowed:
          - "mcp__lsp__start_lsp"
          - "mcp__lsp__get_diagnostics"
        forbidden:
          - "mcp__lsp__apply_edit"
          - "Edit"
          - "Write"
      build:
        description: "Layer 2: run compiler build"
        allowed:
          - "mcp__lsp__run_build"
        forbidden:
          - "mcp__lsp__apply_edit"
          - "Edit"
          - "Write"
      tests:
        description: "Layer 3: run test suite"
        allowed:
          - "mcp__lsp__run_tests"
          - "Bash"                         # scoped test commands for large repos
        forbidden:
          - "mcp__lsp__apply_edit"
          - "Edit"
          - "Write"
      fix_and_format:
        description: "Post-verification: apply code action fixes and format"
        allowed:
          - "mcp__lsp__suggest_fixes"
          - "mcp__lsp__apply_edit"
          - "mcp__lsp__format_document"
          - "mcp__lsp__get_diagnostics"    # re-check after fixes
        forbidden:
          - "mcp__lsp__simulate_*"
          - "mcp__lsp__run_build"          # re-run full verify instead
          - "mcp__lsp__run_tests"          # re-run full verify instead
    global_forbidden:
      - "mcp__lsp__simulate_*"             # verify is post-edit, not speculative
      - "mcp__lsp__rename_symbol"          # verify does not make semantic changes
---

> Requires the agent-lsp MCP server.

# lsp-verify: Three-Layer Verification

## When to Use

Run this skill after any significant change to verify correctness at every level:

- After editing source files (logic changes, refactors, new functions)
- After merging or rebasing branches
- After dependency updates or configuration changes
- Before committing or pushing code

## Input

- `workspace_dir` (required): absolute path to the workspace root (e.g. `/Users/you/code/myproject`)
- `changed_files` (optional): list of files you edited — used for targeted diagnostics

## Execution

### Pre-step: Test correlation (when `changed_files` is provided)

Before running the three layers, call `get_tests_for_file` for each changed
source file to build a source → test file map:

```
mcp__lsp__get_tests_for_file({ "file_path": "<changed/source/file>" })
```

Returns the test files that correspond to each source file. Store this map —
it is used in Layer 3 to focus failure analysis. If `changed_files` is unknown,
skip this step.

**Run all three layers in parallel** — they are independent and do not need to
be sequenced. Issue all three calls in the same message to minimize wall time.

### Layer 1: LSP Diagnostics

Call `mcp__lsp__get_diagnostics` with `file_path` set to each changed file.
`get_diagnostics` takes a file path, not a workspace directory.

Note: requires LSP to be initialized. If not yet running, call `start_lsp`
with the workspace root first.

```
mcp__lsp__get_diagnostics({ "file_path": "<path/to/changed/file>" })
```

Call once per changed file. If you don't know which files changed, call it on
the primary files touched in this session. Rank results by severity: errors
first, then warnings.

### Layer 2: Build

```
mcp__lsp__run_build({ "workspace_dir": "<workspace_dir>" })
```

Returns `{ "success": bool, "errors": [...] }`. A failed build means the code
does not compile. Build errors are blocking — must be resolved before shipping.

### Layer 3: Tests

```
mcp__lsp__run_tests({ "workspace_dir": "<workspace_dir>" })
```

Does NOT require `start_lsp`. Returns `{ "passed": bool, "failures": [...] }`.

**Large output warning:** `run_tests` on large repos can return hundreds of
thousands of characters and exceed the context window. If the result is saved
to a file rather than returned inline, do NOT attempt to read the whole file.
Instead, search it for failures:

```bash
grep -E "^(FAIL|--- FAIL)" <output_file>
```

Or scope tests to the correlated test files from the pre-step to avoid the
size issue entirely:

```bash
GOWORK=off go test -count=1 -short ./internal/mypackage/... 2>&1 | grep -E "FAIL|ok"
```

**Using test correlation:** If the pre-step produced a source → test file map,
cross-reference failing test names against that map. For each failure, note
whether it is in a correlated test file (directly covers the changed code) or
an unrelated test file (collateral failure from a shared dependency). This
distinction guides where to investigate first.

Test failures are blocking — they indicate regressions or unmet contracts.

## Output Format

After running all three layers, produce a structured report:

```
## Verification Report

### Layer 1: LSP Diagnostics
[CLEAN / N errors, M warnings]

<details if N > 0 or M > 0>
Errors:
- file:line - message

Warnings:
- file:line - message
</details>

### Layer 2: Build
[PASSED / FAILED - N errors]

<details if FAILED>
- error message (file:line)
</details>

### Layer 3: Tests
[PASSED / FAILED - N failures]

<details if FAILED>
- test name: message (file:line) [correlated / unrelated]
</details>

<if test correlation map exists>
Test files covering changed source:
  changed/source/file.go → test/source_file_test.go
</if>

### Summary
Overall: CLEAN / NEEDS ATTENTION
Blocking issues: [errors that must be fixed before shipping]
```

- **CLEAN**: no errors in any layer (warnings are advisory only)
- **NEEDS ATTENTION**: one or more blocking issues found

## Blocking vs Advisory

| Layer | Errors | Warnings |
|-------|--------|----------|
| LSP Diagnostics | Blocking | Advisory |
| Build | All blocking | N/A |
| Tests | All blocking | N/A |

Build errors and test failures block shipping. LSP warnings and style
suggestions are advisory — document them but do not treat as blockers unless
they indicate logical errors.

## When Verification Passes: Optional Format

If all three layers are CLEAN and `changed_files` is known, offer to format
the changed files before committing:

```
mcp__lsp__format_document({ "file_path": "<changed-file>" })
```

Apply the returned `TextEdit[]` via `apply_edit` if non-empty. Run once per
changed file. Skip if the user did not request formatting.

---

## When Errors Are Found: Applying Code Actions

If Layer 1 returns errors, the LSP may offer quick fixes. For each error
location, call `suggest_fixes` to surface available fixes:

```
mcp__lsp__suggest_fixes({
  "file_path": "<file>",
  "line": <error line>,
  "column": <error column>
})
```

Returns a list of available actions (e.g. "Add missing import", "Implement
interface methods", "Remove unused variable"). Pick the most appropriate one
and apply it:

```
mcp__lsp__apply_edit({
  "file_path": "<file>",
  "old_text": "<text to replace>",
  "new_text": "<replacement>"
})
```

Or if the code action returns a `workspace_edit`, pass it directly to
`apply_edit` via the `workspace_edit` parameter.

After applying, **re-run Layer 1** on the affected file to confirm the error
is resolved before moving on. Do not apply multiple code actions in bulk
without verifying each one — they may interact.

**When to use:** Compile errors from missing imports, unimplemented interface
methods, or type mismatches often have one-click fixes available. Manual
reasoning is still required for logic errors.
