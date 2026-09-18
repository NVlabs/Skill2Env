---
name: lsp-concurrency-audit
description: Concurrency safety audit for a type or file. Maps all fields, traces which are accessed from concurrent contexts (goroutines, threads, async tasks), and flags fields that lack synchronization. Produces a field-level safety report. Language-agnostic across 4 concurrency families.
argument-hint: "<file-path> [--type <TypeName>]"
user-invocable: true
allowed-tools: mcp__lsp__start_lsp mcp__lsp__open_document mcp__lsp__blast_radius mcp__lsp__find_callers mcp__lsp__list_symbols mcp__lsp__get_symbol_source mcp__lsp__find_references
license: MIT
compatibility: Requires the agent-lsp MCP server (github.com/blackwell-systems/agent-lsp)
metadata:
  required-capabilities: documentSymbolProvider referencesProvider
  optional-capabilities: callHierarchyProvider
---

> Requires the agent-lsp MCP server.

# lsp-concurrency-audit

Given a type or file, map all fields, identify which are accessed from multiple
concurrent contexts, and flag fields that lack synchronization. Produces a
field-level concurrency safety report.

## When to Use

- Before refactoring a type that is accessed from goroutines/threads
- Auditing a codebase for data race candidates
- Reviewing a PR that adds concurrent access to an existing type
- Understanding which fields in a type need mutex protection

## Input

```
/lsp-concurrency-audit <file-path> [--type <TypeName>]
```

If `--type` is provided, audit only that type. Otherwise, audit all types in
the file that have concurrent callers.

## Step 1: Discover types and fields

Call `list_symbols` on the target file to enumerate all types (structs, classes):

```
mcp__lsp__list_symbols({ "file_path": "<target>" })
```

For each type (kind=23 struct, kind=5 class), collect:
- Type name
- All fields (children with kind=8 field or kind=7 variable)
- Whether any field's name or detail contains sync primitives
  ("Mutex", "RWMutex", "Lock", "Semaphore", "atomic", "Atomic", "sync.",
  "pthread_mutex", "std::mutex")

If `--type` was specified, filter to that type only.

## Step 2: Blast radius and sync-guarded status

Call `blast_radius` on the file:

```
mcp__lsp__blast_radius({
  "changed_files": ["<target>"],
  "scope": "all"
})
```

From the result, for each method on each target type:
- Record `sync_guarded: true/false` from the response
- Record `non_test_callers` count (blast radius)
- Record `test_callers` count

## Step 3: Trace concurrent boundaries

For each method on each target type, call `find_callers` with
`cross_concurrent: true`:

```
mcp__lsp__find_callers({
  "file_path": "<target>",
  "line": <method_line>,
  "column": <method_column>,
  "direction": "incoming",
  "cross_concurrent": true
})
```

Record for each method:
- `concurrent_callers`: list of callers that cross concurrent boundaries
- `pattern`: the concurrent entry pattern detected (e.g., "go func(", "Thread.start(")

## Step 4: Classify fields

For each field in each type, determine its safety status:

**SAFE:** The type is sync-guarded (has a mutex/lock field) AND all methods
that access this field acquire the lock before access. Confidence: verified
if the type has a sync primitive; suspected if relying on external locking.

**UNSAFE (data race candidate):** The field is accessed by methods that have
`concurrent_callers` AND the type has no sync primitive. This is a potential
data race.

**WRITE-CONCURRENT:** The field is written by a method that has concurrent
callers. Higher severity than read-only concurrent access.

**READ-ONLY:** The field is only read (not written) from concurrent contexts.
Lower severity; often safe but worth flagging for review.

Severity assignment:
- `error`: UNSAFE + WRITE-CONCURRENT (probable data race)
- `warning`: UNSAFE + READ-ONLY (potential race under high concurrency)
- `info`: SAFE (sync-guarded, for documentation)

## Step 5: Output

```markdown
## Concurrency Audit: <TypeName>

**File:** <file_path>
**Fields:** N total, M sync-guarded
**Concurrent methods:** K (methods called from goroutines/threads/tasks)

### Field Safety Report

| Field | Type | Sync | Concurrent Writers | Concurrent Readers | Status |
|-------|------|------|-------------------|-------------------|--------|
| mu | sync.RWMutex | (is sync) | - | - | SYNC PRIMITIVE |
| sender | NotificationSender | guarded | 2 (SetSender, Send) | 3 | SAFE |
| subscribers | []Subscriber | none | 1 (Subscribe) | 2 | UNSAFE (write-concurrent) |

### Concurrent Call Sites

For each UNSAFE field, list the concurrent callers:

- `subscribers` written by `Subscribe` called from:
  - `setupNotificationHub` via `go func()` at notifications.go:45
  - `handleNewSession` via `go func()` at server.go:312

### Recommendations

- Add `sync.RWMutex` to protect `subscribers` field
- Or: use channel-based access pattern instead of direct field mutation
```

## Caveats

1. **Heuristic detection.** Concurrent boundary detection relies on source
   pattern matching, not runtime analysis. False negatives are possible when
   concurrent entry is indirect (e.g., passed as a callback to a framework).

2. **Lock discipline not verified.** The audit checks whether a sync primitive
   exists on the type, not whether every method actually acquires it before
   field access. A type with a mutex but inconsistent locking will show as
   SAFE when it may not be.

3. **External synchronization invisible.** If synchronization is provided by
   an external lock (e.g., the caller holds a lock before calling the method),
   the audit will flag the field as UNSAFE. Add a comment or annotation to
   suppress.

4. **Read vs write detection is heuristic.** Determining whether a method
   reads or writes a field requires source code analysis. The skill reads the
   method body and looks for assignment patterns (`field =`, `field.Store()`,
   `append(field,`). False positives are possible for complex access patterns.
