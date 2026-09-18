---
name: lsp-inspect
description: Full code quality audit for a file, package, or directory. Supports batch mode (directory walk with --top ranking), comparison mode (--diff for branch-only issues), severity calibration by blast radius, fix suggestions, and confidence tiers. Applies a check taxonomy (dead symbols, silent failures, error wrapping, coverage gaps, test coverage, doc drift, unrecovered panics, context propagation, concurrency safety) using LSP-first strategies. Concurrency checks cover 25 languages across 4 families (goroutine, thread, async, actor). Produces a severity-tiered findings report. Language-agnostic.
argument-hint: "<file-or-directory> [--checks <type1>,<type2>] [--json] [--top N] [--diff]"
user-invocable: true
allowed-tools: mcp__lsp__start_lsp mcp__lsp__open_document mcp__lsp__blast_radius mcp__lsp__find_references mcp__lsp__list_symbols mcp__lsp__inspect_symbol mcp__lsp__get_diagnostics mcp__lsp__find_callers mcp__lsp__go_to_definition mcp__lsp__get_server_capabilities mcp__lsp__get_cross_repo_references Bash
license: MIT
compatibility: Requires the agent-lsp MCP server (github.com/blackwell-systems/agent-lsp)
metadata:
  required-capabilities: documentSymbolProvider referencesProvider
  optional-capabilities: callHierarchyProvider
---

> Requires the agent-lsp MCP server.

# lsp-inspect

Full code quality audit for a file, package, or directory. Combines LSP batch
analysis (`blast_radius`) with targeted per-symbol checks and LLM-driven
heuristic analysis. Produces a severity-tiered findings report with confidence
tiers and fix suggestions.

## When to Use

- Auditing a package before a release or major refactor
- Finding dead code, untested exports, and error handling gaps in unfamiliar code
- Reviewing code quality of an external codebase for contribution opportunities
- Pre-merge quality gate on a set of changed files
- Batch inspection of an entire directory with ranked output
- Comparing branch changes against main to find newly introduced issues

## Input

```
/lsp-inspect <target> [--checks <type1>,<type2>] [--json] [--top N] [--diff]
```

**Target** can be:
- A file path: `/lsp-inspect src/handlers/auth.go`
- A directory/package: `/lsp-inspect internal/runnables/`
- Multiple targets: `/lsp-inspect pkg/a.go pkg/b.go`

**Directory detection:** When target is a directory, walk all `.go`, `.ts`, `.py`
files in it recursively. Produce a ranked report: "Top N findings sorted by
severity then blast radius."

**Flags:**
- `--checks <type1>,<type2>`: only run listed check types (default: all applicable)
- `--json`: emit structured JSON instead of markdown
- `--top N`: Maximum findings to report (default 20). Only applies to directory/batch mode.
- `--diff`: Only inspect files changed vs main branch. Filter findings to lines within the diff ranges. Output header: "New issues introduced by this branch."

## Check Taxonomy

| Check | What it finds | LSP strategy |
|-------|--------------|--------------|
| `dead_symbol` | Exported symbol with zero references | Tier 1A: `blast_radius` batch; Tier 1B: `find_references` per-symbol |
| `test_coverage` | Exported symbol with no test callers | Tier 1A: `blast_radius` test_callers field |
| `silent_failure` | Error/exception suppressed without re-raise or logging | Read code, identify bare `except:`, empty `if err != nil {}`, swallowed returns |
| `error_wrapping` | Error returned/raised without context | Read code, identify `return err` without `fmt.Errorf` wrapping or `raise` without `from` |
| `coverage_gap` | Unhandled input, error path, or code branch | Read code, identify switch/match without default, unchecked type assertions |
| `doc_drift` | Docstring/comment that doesn't match the actual signature | Compare `inspect_symbol` hover text against source |
| `panic_not_recovered` | Unhandled crash in a goroutine or async context | Read code, identify `go func()` without recover, unguarded `.unwrap()` |
| `context_propagation` | Function receives context but creates a fresh root for callees | Read code, identify `context.Background()` in functions with `ctx` parameter |
| `unrecovered_concurrent_entry` | Concurrent entry point without recovery | Read code, identify goroutines/threads/tasks without try-catch or recover |
| `unchecked_shared_state` | Type assertion or cast on concurrent data structure without safety check | Read code, identify bare `.(*Type)` on sync.Map, unchecked casts on ConcurrentHashMap |
| `channel_never_closed` | Channel or queue created but never closed in the same package | Read code + grep, find creation sites without matching close/shutdown |
| `shared_field_without_sync` | Field accessed from concurrent contexts without synchronization | `blast_radius` (sync_guarded) + `find_callers` (cross_concurrent) |

## Execution

### Step 0: Initialize and verify workspace

```
mcp__lsp__start_lsp(root_dir="<repo_root>")
```

Open one file per package being audited:

```
mcp__lsp__open_document(file_path="<target_file>", language_id="<lang>")
```

**Warm-up check (mandatory):** Pick one symbol you know is actively used.
Call `find_references` on it. If it returns `[]`, wait 3-5 seconds and retry.
Do not proceed until a known-active symbol returns >= 1 reference.

### Step 0.5: Diff mode file selection

When `--diff` is set:
1. Run `git diff --name-only main` to get changed files
2. Run `git diff main` to get line-level change ranges
3. Use only changed files as inspection targets
4. After Step 3, filter findings: keep only those whose File:Line falls within
   a changed line range from the diff
5. Prepend output with: '## New issues introduced by this branch'

### Step 1: Batch analysis (Tier 1A)

Call `blast_radius` once per file in the target:

```
mcp__lsp__blast_radius(changed_files=["/abs/path/file.go"], include_transitive=false)
```

This returns all exported symbols with:
- `non_test_callers`: count of production code references
- `test_callers`: count of test file references

Classify immediately:
- `non_test_callers == 0 AND test_callers == 0` -> dead symbol candidate (confidence: verified)
- `non_test_callers == 0 AND test_callers > 0` -> test-only (may be dead, confidence: suspected)
- `non_test_callers > 0 AND test_callers == 0` -> untested export (confidence: verified)

If `blast_radius` fails or is unavailable, fall back to Tier 1B
(`find_references` per-symbol) for `dead_symbol` checks.

### Step 2: Heuristic checks (LLM-driven)

Read the source code of each file (use offset/limit for files over 500 lines).
Apply the following checks by reading and reasoning about the code:

**silent_failure:** Look for:
- Go: `if err != nil { return }` (no error returned), bare `_ = fn()`
- Python: bare `except:` or `except Exception: pass`
- TypeScript: empty `.catch(() => {})`, `try {} catch(e) {}`
- Rust: `.unwrap_or_default()` on fallible ops that should propagate

**error_wrapping:** Look for:
- Go: `return err` without `fmt.Errorf("context: %w", err)`
- Python: `raise ValueError(str(e))` without `from e`
- TypeScript: `throw e` without wrapping in a contextual error

**coverage_gap:** Look for:
- Switch/match without exhaustive cases or default branch
- Unchecked type assertions (`v := x.(Type)` vs `v, ok := x.(Type)`)
- Missing nil/null checks before dereference after fallible calls

**doc_drift:** For exported functions, compare:
- Parameter names in docstring vs actual signature
- Return type described in doc vs actual return
- Use `inspect_symbol` hover text to cross-reference

**panic_not_recovered:** Look for:
- Go: `go func() { ... }()` without `defer recover()`
- Rust: `.unwrap()` or `.expect()` in non-test, non-main code
- Python: bare thread creation without exception handling

**context_propagation:** Look for:
- Functions that accept `ctx context.Context` but call `context.Background()` or `context.TODO()` internally

**unrecovered_concurrent_entry:** Detect concurrent entry points without recovery.
Language-specific patterns (check by language family):
- Go: `go func() { ... }()` where the function body has no `defer func() { if r := recover()` pattern. Weight: library transport code (error severity), application code with middleware protection (info).
- Java/Kotlin/Scala: `new Thread(...)` or `ExecutorService.submit(...)` without try-catch wrapping the Runnable body, and no `UncaughtExceptionHandler` set on the thread.
- C#: `Task.Run(...)` or `new Thread(...)` without try-catch in the delegate body.
- C/C++: `pthread_create` or `std::thread` without exception handling in the thread function.
- Rust: `std::thread::spawn` without `catch_unwind` in the closure. Also flag `.unwrap()` inside spawned threads (panics kill only that thread but lose the error).
- Swift: `DispatchQueue.async` or `Task { }` without do-catch.
- Python: `threading.Thread(target=...)` without try-except in the target function. `asyncio.create_task()` without error handling on the awaited result.
- TypeScript/JavaScript: `new Worker()` without `onerror` or `error` event handler. `Promise` constructor without `.catch()` on the chain.
- Zig: `try std.Thread.spawn` without error handling on the spawned function.
- Elixir/Erlang/Gleam: Skip (actor model with supervisors; unrecovered processes are by design).
- Lua/Bash/SQL: Skip (no concurrency primitives).

**unchecked_shared_state:** Detect unsafe type operations on concurrent data structures:
- Go: `sync.Map` `.Load()`, `.LoadOrStore()`, or `.LoadAndDelete()` followed by a bare type assertion `actual.(*Type)` without the `, ok` pattern. The safe pattern is `v, ok := actual.(*Type)`.
- Java: `ConcurrentHashMap.get()` with unchecked cast and no `instanceof` guard.
- C#: `ConcurrentDictionary` value retrieval with unchecked cast.
- Other languages: skip (dynamic typing or type system prevents this class of bug).

**channel_never_closed:** Detect channels or queues that are created but never closed:
- Go: `make(chan T)` or `make(chan T, N)` where `close(channelName)` does not appear in the same package. May indicate goroutine leaks (receivers block on `range` forever).
- Python: `queue.Queue()` creation without a sentinel value pattern (`queue.put(None)` + `if item is None: break`).
- Rust: `mpsc::channel()` where the sender is never dropped or explicitly closed.
- TypeScript: `new MessageChannel()` or `new BroadcastChannel()` without `.close()`.
- Java: `BlockingQueue` creation without a poison pill or shutdown pattern.
- Other languages: skip if no channel/queue primitives.

**shared_field_without_sync:** Detect struct/class fields accessed from multiple
concurrent contexts without synchronization. This check composes two tools:

1. Call `blast_radius` on the target file. For each symbol where
   `sync_guarded: false` (or absent), the symbol's type lacks sync primitives.
2. For each such symbol, call `find_callers` with `cross_concurrent: true`.
   If `concurrent_callers` is non-empty, the symbol is called from a concurrent
   context (goroutine, thread, async task) without synchronization.
3. Flag any symbol where: (a) it modifies state (writes to fields, not a pure
   read-only function), AND (b) it has concurrent callers, AND (c) its parent
   type is not sync-guarded.

Language-agnostic: `blast_radius` provides `sync_guarded`, `find_callers`
provides `concurrent_callers`. The check logic is identical regardless of
whether the concurrent boundary is a goroutine, thread, or async task.

Severity:
- error: field written from 2+ concurrent contexts with no sync (data race)
- warning: field written from 1 concurrent context (potential race under load)
- info: field read-only from concurrent contexts (likely safe, but flag for review)

### Step 3: Cross-check and classify

For each finding, assign:

**Severity (calibrated by blast radius):**
- `error`: Will cause runtime failure, data loss, or resource leak, OR any finding where `non_test_callers >= 10` (high blast radius amplifies severity)
- `warning`: May cause confusion, maintenance burden, or subtle bugs, OR findings where `non_test_callers` is 3-9
- `info`: Style issue or improvement opportunity, OR `non_test_callers <= 2`

Use the `non_test_callers` count from Step 1's `blast_radius` result as a
severity multiplier. A silent failure in a function with 50 callers is
error-severity; the same pattern with 2 callers is info.

**Cross-file impact scoring:** For every finding, look up the symbol's
`non_test_callers` count from Step 1's blast_radius result. Use this as a
severity multiplier: if non_test_callers >= 10, escalate severity by one tier
(info->warning, warning->error). Document the caller count in the finding.

**Confidence tiers:**
- `verified`: LSP-confirmed (Tier 1A/1B) or unambiguous code pattern (act immediately)
- `suspected`: Heuristic match with possible false positive (pattern match, investigate first)
- `advisory`: Grep-based or uncertain pattern match (style, optional)

### Step 4: Output

Produce the findings report:

```markdown
## Inspection Report: <target>

**Files analyzed:** N
**Checks applied:** [list]
**Findings:** E errors, W warnings, I info

### Errors

| # | Check | File:Line | Finding | Confidence | Fix |
|---|-------|-----------|---------|------------|-----|
| 1 | dead_symbol | pkg/foo.go:42 | `UnusedHelper` has 0 references (0 callers) | verified (LSP) | Remove lines 42-55 (function `UnusedHelper`) |

### Warnings

| # | Check | File:Line | Finding | Confidence | Fix |
|---|-------|-----------|---------|------------|-----|
| 1 | error_wrapping | pkg/bar.go:88 | `return err` without context wrapping (5 callers) | verified | Change `return err` to `return fmt.Errorf("funcName: %w", err)` |
| 2 | test_coverage | pkg/foo.go:15 | `ProcessInput` has 0 test callers (8 callers) | verified (LSP) | Add test for `ProcessInput` in foo_test.go |

### Info

| # | Check | File:Line | Finding | Confidence | Fix |
|---|-------|-----------|---------|------------|-----|
| 1 | doc_drift | pkg/foo.go:20 | Docstring mentions `timeout` param, signature has `deadline` (1 caller) | suspected | Update docstring parameter name from timeout to deadline |
```

**Fix suggestions per check type:**
- `dead_symbol`: "Remove lines N-M (function `FuncName`)"
- `error_wrapping`: "Change `return err` to `return fmt.Errorf(\"funcName: %w\", err)`"
- `silent_failure`: "Add `return fmt.Errorf(...)` after the if block"
- `test_coverage`: "Add test for `FuncName` in file_test.go"
- `coverage_gap`: "Add default case to switch statement at line N"
- `doc_drift`: "Update docstring parameter name from X to Y"
- `panic_not_recovered`: "Add `defer func() { if r := recover()... }()` at goroutine start"
- `context_propagation`: "Replace `context.Background()` with `ctx` parameter"

When `--json` is passed, emit structured JSON with the same fields.

### Step 4.5: Batch ranking

When multiple files are analyzed, sort all findings by: (1) severity tier
(error > warning > info), (2) blast radius (non_test_callers descending),
(3) file path alphabetically. Emit only the top N findings (default 20,
controlled by --top flag). Append a summary line: 'Showing N of M total findings.'

### Step 5: Persist results

After producing the findings report, write a JSON file to
`.agent-lsp/last-inspection.json` in the workspace root. The JSON schema:

```json
{
  "target": "<original target path>",
  "timestamp": "<ISO 8601>",
  "files_analyzed": N,
  "findings": [
    {
      "severity": "error|warning|info",
      "confidence": "verified|suspected|advisory",
      "check": "<check_type>",
      "file": "<path>",
      "line": N,
      "finding": "<description>",
      "fix": "<exact fix text>",
      "blast_radius": N
    }
  ],
  "summary": {"errors": N, "warnings": N, "info": N}
}
```

This file is served by the `inspect://last` MCP resource for programmatic access.

## Caveats

1. **Re-exports:** Symbols in `__init__.py` (Python), `index.ts` (TypeScript),
   or public API surface files may appear dead locally but are consumed externally.
   Check `__all__`, barrel exports, and package-level re-exports before classifying.

2. **Registration patterns:** Symbols passed as values to framework registrars
   (HTTP handlers, plugin hooks) show zero LSP references. Grep wiring files
   before confirming dead.

3. **Library public API:** If the target is a library consumed by external repos,
   zero internal references doesn't mean dead. Use `--consumer-repos` or note
   as "library export, verify externally."

4. **Heuristic checks are advisory.** Silent failure and error wrapping checks
   depend on LLM reasoning about intent. False positives are expected; always
   review before acting on findings.

5. **Large files:** For files over 500 lines, read targeted sections (use
   offset/limit). Do not read entire large files into context.
