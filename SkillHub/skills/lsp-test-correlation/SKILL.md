---
name: lsp-test-correlation
description: Find and run the tests that cover a source file. Use after editing a file to discover exactly which test files and test functions need to run — without running the entire test suite.
argument-hint: "[file-path] [optional: run=true]"
user-invocable: true
allowed-tools: mcp__lsp__get_tests_for_file mcp__lsp__find_symbol mcp__lsp__open_document mcp__lsp__run_tests
license: MIT
compatibility: Requires the agent-lsp MCP server (github.com/blackwell-systems/agent-lsp)
metadata:
  optional-capabilities: workspaceSymbolProvider
---

> Requires the agent-lsp MCP server.

# lsp-test-correlation

Discover which tests cover a source file, then run only those tests. Faster
than running the full suite when you've changed one or two files and want
targeted feedback.

## When to use

- After editing a source file: "Which tests do I need to run for this change?"
- Before committing: run only the tests that cover what you touched
- Debugging a failure: find which test file corresponds to a broken source file
- Code review: understand what test coverage exists for a file before merging

Use `/lsp-verify` instead when you want to run the full suite and check all
three layers (diagnostics + build + tests). Use this skill when you want fast,
scoped test execution.

---

## Workflow

### Step 1 — Find correlated test files

Call `get_tests_for_file` for each edited source file:

```
mcp__lsp__get_tests_for_file({ "file_path": "/abs/path/to/source.go" })
```

Returns the test files that correspond to the source file. For multiple edited
files, call once per file.

**If no test files are returned:** the source file may have no dedicated test
file, or the mapping is not resolvable (e.g. integration tests in a separate
directory). See Step 2 for fallback.

### Step 2 — Enumerate test functions (fallback or enrichment)

If `get_tests_for_file` returns test files, use `find_symbol` to list
the test functions defined in those files:

```
mcp__lsp__find_symbol({ "query": "Test" })
```

Filter results to the correlated test files from Step 1. This gives you the
specific test function names to run rather than the whole test file.

**Fallback (no test files found):** query `find_symbol` for test
functions that contain the changed symbol's name:

```
mcp__lsp__find_symbol({ "query": "Test<ChangedFunctionName>" })
```

This catches cases where `get_tests_for_file` misses indirect coverage.

### Step 3 — Report the correlation map

Before running, report what was found:

```
## Test correlation for <file>

Source file: internal/tools/analysis.go
Test files:
  → internal/tools/analysis_test.go
     Tests: TestHandleGetCodeActions, TestHandleGetCompletions, TestHandleGetDocumentSymbols

No correlated test files found for: internal/lsp/normalize.go
  → Fallback: TestNormalizeCompletion, TestNormalizeDocumentSymbols (from workspace symbol search)
```

If the user provided `run=true` or asks to run, proceed to Step 4. Otherwise
stop here and let the user decide.

### Step 4 — Run correlated tests

Run only the correlated test files or functions. Scope as tightly as possible:

**Go — run specific package:**
```
mcp__lsp__run_tests({ "workspace_dir": "<root>", "test_filter": "TestHandleGetCodeActions|TestHandleGetCompletions" })
```

If `run_tests` does not support `test_filter`, pass the package path instead of
the workspace root to narrow scope. The test output will be smaller and faster
than running `./...`.

**Output handling:** If test output is large, do not read it in full. Search
for failures:
```
grep -E "^(FAIL|--- FAIL)" <output_file>
```

### Step 5 — Report results

```
## Test Results

Ran 3 tests in internal/tools/analysis_test.go

PASSED (2):
  TestHandleGetCodeActions
  TestHandleGetCompletions

FAILED (1):
  TestHandleGetDocumentSymbols — expected 3 symbols, got 2 (analysis_test.go:87)

Recommendation: Fix TestHandleGetDocumentSymbols before committing.
```

---

## Multi-file workflow

For changes spanning multiple source files:

1. Call `get_tests_for_file` for each changed file in parallel.
2. Deduplicate the resulting test files (the same test file may cover multiple
   source files).
3. Report the full correlation map before running.
4. Run the deduplicated test set once.

```
## Test correlation for 3 changed files

internal/tools/analysis.go      → internal/tools/analysis_test.go
internal/lsp/client.go          → internal/lsp/client_test.go, internal/lsp/client_completion_test.go
internal/resources/resources.go → (no dedicated test file)

Deduplicated test files to run: 3
```

---

## Decision guide

| Situation | Action |
|-----------|--------|
| `get_tests_for_file` returns test files | Use those; enumerate functions via `find_symbol` |
| No test files returned | Fallback to `find_symbol` with changed symbol names |
| Test files found but no matching test functions | Report gap — this source file may lack unit test coverage |
| More than 10 test files returned | Don't run all; use `/lsp-verify` for full suite instead |
| Test fails | Run `/lsp-verify` for full diagnostic picture |

---

## Example

```
# "I edited internal/tools/symbol_source.go — which tests should I run?"

get_tests_for_file(file_path="/repo/internal/tools/symbol_source.go")
  → internal/tools/symbol_source_test.go

find_symbol(query="TestGetSymbolSource")
  → TestGetSymbolSource_ContainsPosition (line 12)
  → TestGetSymbolSource_FindInnermost (line 34)
  → TestGetSymbolSource_PositionPattern (line 67)

# Report correlation, then run:
run_tests(workspace_dir="/repo", test_filter="TestGetSymbolSource")
  → 3 passed in 0.4s
```
