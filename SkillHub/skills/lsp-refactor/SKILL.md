---
name: lsp-refactor
description: End-to-end safe refactor workflow — blast-radius analysis, speculative preview, apply to disk, verify build, run affected tests. Inlines lsp-impact + lsp-safe-edit + lsp-verify + lsp-test-correlation into one coordinated sequence.
argument-hint: "[symbol-or-file] [intent]"
user-invocable: true
allowed-tools: mcp__lsp__blast_radius mcp__lsp__preview_edit mcp__lsp__simulate_chain mcp__lsp__get_diagnostics mcp__lsp__run_build mcp__lsp__run_tests mcp__lsp__get_tests_for_file mcp__lsp__apply_edit mcp__lsp__replace_symbol_body mcp__lsp__open_document mcp__lsp__format_document Edit Write
license: MIT
compatibility: Requires the agent-lsp MCP server (github.com/blackwell-systems/agent-lsp)
metadata:
  required-capabilities: referencesProvider
  optional-capabilities: documentFormattingProvider
  tool_permissions:
    phases:
      blast_radius:
        description: "Phase 1: analyze impact before any edits"
        allowed:
          - "mcp__lsp__blast_radius"
          - "mcp__lsp__go_to_symbol"
          - "mcp__lsp__find_references"
        forbidden:
          - "mcp__lsp__apply_edit"
          - "mcp__lsp__simulate_*"
          - "Edit"
          - "Write"
      speculative_preview:
        description: "Phase 2: simulate edits in memory, compare diagnostics"
        allowed:
          - "mcp__lsp__open_document"
          - "mcp__lsp__get_diagnostics"
          - "mcp__lsp__preview_edit"
          - "mcp__lsp__simulate_chain"
        forbidden:
          - "mcp__lsp__apply_edit"
          - "Edit"
          - "Write"
      apply:
        description: "Phase 3: write changes to disk and format"
        allowed:
          - "mcp__lsp__apply_edit"
          - "mcp__lsp__format_document"
          - "Edit"
          - "Write"
        forbidden:
          - "mcp__lsp__simulate_*"
          - "mcp__lsp__rename_symbol"
      build_verification:
        description: "Phase 4: check diagnostics and run the build"
        allowed:
          - "mcp__lsp__get_diagnostics"
          - "mcp__lsp__run_build"
        forbidden:
          - "mcp__lsp__apply_edit"
          - "Edit"
          - "Write"
      test_execution:
        description: "Phase 5: find and run affected tests"
        allowed:
          - "mcp__lsp__get_tests_for_file"
          - "mcp__lsp__run_tests"
        forbidden:
          - "mcp__lsp__apply_edit"
          - "Edit"
          - "Write"
    global_forbidden:
      - "mcp__lsp__rename_symbol"        # refactor uses edit, not rename
---

> Requires the agent-lsp MCP server.

# lsp-refactor

End-to-end safe refactor workflow. Sequences blast-radius analysis, speculative
preview, disk apply, build verification, and targeted test execution in one
coordinated pass.

**This skill does NOT replace lsp-safe-edit or lsp-impact.**
- `lsp-safe-edit` wraps a single edit with before/after diagnostic comparison —
  use it when you need to make one targeted change with careful error diffing.
- `lsp-impact` is read-only blast-radius analysis — use it when you want to
  understand scope before deciding whether to proceed.
- `lsp-refactor` sequences ALL four workflows (lsp-impact → lsp-safe-edit →
  lsp-verify → lsp-test-correlation) in order. Use it when you know your target
  and intent up front and want the complete workflow without switching skills.

---

## Input

- **target**: symbol name in dot notation (e.g. `"codec.Encode"`, `"Buffer.Reset"`)
  OR file path (e.g. `"internal/lsp/client.go"`)
- **intent**: description of the change to make (e.g. "rename to ParseConfigV2",
  "add a second parameter `timeout time.Duration`")
- **workspace_root**: absolute path to the workspace root

---

## Phase 1 — Blast-Radius Analysis (inlined from lsp-impact)

**This phase is mandatory. Do not skip it, even for "small" refactors.**

Call `mcp__lsp__blast_radius` with `changed_files` set to the file
containing the target symbol. If the user provided a file path directly, use it.
If the user provided a symbol name, resolve the file first (e.g. via
`mcp__lsp__go_to_symbol`).

```
mcp__lsp__blast_radius({
  "changed_files": ["/abs/path/to/file"],
  "include_transitive": false
})
```

Returns:
- `affected_symbols` — exported symbols with reference counts
- `test_callers` — test files and enclosing test function names
- `non_test_callers` — production call sites

**Display:**
- Affected symbol count
- Test callers (each with enclosing test function name)
- Non-test callers (each with file:line)
- Total reference count

**High blast-radius gate:** If the total reference count exceeds 20, STOP and
ask the user to confirm before continuing:

```
High blast radius: N callers found. Proceed with refactor? [y/n]
```

If the user answers "n", abort. Do not proceed to Phase 2.

---

## Phase 2 — Speculative Preview (inlined from lsp-safe-edit)

Only reached if Phase 1 blast radius is acceptable (≤ 20 callers, or user confirmed).

### 2a — Open file and capture baseline diagnostics

```
mcp__lsp__open_document({ "file_path": "/abs/path/to/file", "language_id": "go" })
mcp__lsp__get_diagnostics({ "file_path": "/abs/path/to/file" })
```

Store baseline diagnostics as BEFORE.

### 2b — Speculative simulation

For a **single-file change**: use `preview_edit`:

```
mcp__lsp__preview_edit({
  "file_path": "/abs/path/to/file",
  "start_line": <N>,
  "start_column": <col>,
  "end_line": <N>,
  "end_column": <col>,
  "new_text": "<replacement text>"
})
```

For a **multi-file change** (e.g. rename + call site updates): use `simulate_chain`:

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
    }
    // additional dependent edits ...
  ]
})
```

### 2c — Evaluate simulation result

Display the speculative result using the Diagnostic Diff Output Format from
[references/patterns.md](references/patterns.md).

**Decision:**

| `net_delta` | Action |
|-------------|--------|
| ≤ 0 | Safe. Proceed to Phase 3. |
| > 0 | **Abort.** Report introduced errors. Do NOT apply to disk. |

If `net_delta > 0`, stop and show the full list of errors the simulation
introduced. Do not proceed to Phase 3.

---

## Phase 3 — Apply to Disk

Only reached if Phase 2 `net_delta <= 0`.

Apply the change using the Edit or Write tool. When the edit targets a complete
function or method body, `mcp__lsp__replace_symbol_body` is an alternative that
resolves the symbol by name and replaces its full range without position math:

```
mcp__lsp__replace_symbol_body({
  "file_path": "/abs/path/to/file",
  "symbol_path": "Package.Function",
  "new_body": "func Function() error {\n\treturn nil\n}"
})
```

For edits computed by simulation, `mcp__lsp__apply_edit` may be used directly if
the simulation returned an edit object:

```
Edit(file_path: "/abs/path/to/file", old_string: "...", new_string: "...")
```

For multi-file changes, apply each file's edits before moving to Phase 4.
If any individual apply fails, stop and report before applying remaining files.

After applying, format the changed file(s):

```
mcp__lsp__format_document({ "file_path": "/abs/path/to/file" })
```

Apply the returned `TextEdit[]` via `mcp__lsp__apply_edit` if non-empty.

---

## Phase 4 — Build Verification (inlined from lsp-verify)

Run in this order — LSP diagnostics first, then the compiler build:

```
mcp__lsp__get_diagnostics({ "file_path": "/abs/path/to/file" })
mcp__lsp__run_build({ "workspace_root": "/abs/path/to/workspace" })
```

**Decision:**

| Result | Action |
|--------|--------|
| Diagnostics clean, build passes | Proceed to Phase 5. |
| Diagnostics show new errors | Display errors and stop. Do not proceed to Phase 5. |
| Build fails | Display build output and stop. Do not proceed to Phase 5. |

If build fails, report the full build error output and stop. Test execution
is skipped until build passes.

---

## Phase 5 — Run Affected Tests (inlined from lsp-test-correlation)

For each file changed in Phase 3, find correlated test files:

```
mcp__lsp__get_tests_for_file({ "file_path": "/abs/path/to/changed/file" })
```

Deduplicate the resulting test files if multiple source files were changed.
Run only the correlated test files:

```
mcp__lsp__run_tests({ "workspace_root": "/abs/path/to/workspace", "test_files": [...] })
```

**If no correlated test files are found:** note "No test correlation found —
run full suite manually to confirm." Do not attempt to run `./...` automatically.

---

## Abort Conditions

The following conditions abort the workflow immediately. Each abort displays the
relevant output before stopping.

1. **Phase 1:** blast radius > 20 callers AND user does not confirm → abort
2. **Phase 2:** `net_delta > 0` (simulation introduced errors) → abort, show errors
3. **Phase 4:** build fails → abort, show build output
4. **Any phase:** LSP tool returns an unexpected error → abort, report tool output verbatim

---

## Output Format

After completing all phases, produce this structured report:

```
## lsp-refactor Complete

### Phase 1 — Blast Radius
Affected symbols: N
Test callers: M  (list each with enclosing test function)
Non-test callers: K

### Phase 2 — Speculative Preview
[Diagnostic Diff Output Format from patterns.md]
net_delta: 0 → safe to apply

### Phase 3 — Applied
Files changed: [list]

### Phase 4 — Build Verification
Diagnostics: N errors (0 new)
Build: PASS

### Phase 5 — Test Results
Test files run: [list]
Result: PASS / FAIL
```

If the workflow aborted at a phase, report only the phases completed and the
abort reason:

```
## lsp-refactor Aborted at Phase 2

### Phase 1 — Blast Radius
...

### Phase 2 — Speculative Preview
ABORTED: net_delta: +2 (errors introduced)
Errors:
- file.go:34 — undefined: NewType
- file.go:51 — cannot use int as string
```

---

## Example

```
Goal: rename exported function ParseConfig → ParseConfigV2 in pkg/config

Phase 1 — Blast Radius
  blast_radius(changed_files=["pkg/config/parser.go"])
  → affected_symbols: 1 (ParseConfig)
  → non_test_callers: 3 (cmd/main.go, internal/app.go, internal/loader.go)
  → test_callers: 1 (pkg/config/parser_test.go — TestParseConfig)
  → total references: 4 — within threshold, proceeding

Phase 2 — Speculative Preview
  open_document(file_path="pkg/config/parser.go")
  get_diagnostics → BEFORE: 0 errors
  simulate_chain(edits: [parser.go rename + 3 call-site updates])
  → cumulative_delta: 0 → safe to apply

Phase 3 — Applied
  Edit parser.go: func ParseConfig → func ParseConfigV2
  Edit cmd/main.go, internal/app.go, internal/loader.go: update call sites
  format_document(parser.go)

Phase 4 — Build Verification
  get_diagnostics → 0 errors
  run_build → success

Phase 5 — Test Results
  get_tests_for_file(parser.go) → pkg/config/parser_test.go
  run_tests(test_files=["pkg/config/parser_test.go"]) → PASS

## lsp-refactor Complete
...
```
