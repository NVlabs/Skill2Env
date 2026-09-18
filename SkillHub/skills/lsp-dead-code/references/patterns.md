# lsp-dead-code: Reference Patterns

Supplementary reference detail for the `lsp-dead-code` skill.

---

## Dead Code Report Format

Use this format when producing the audit output in Step 3.

```
## Dead Code Audit: path/to/file.go

Exported symbols: N total
Zero-reference: M candidates
Test-only reference: K

### Zero-Reference Candidates (WARNING)
| Symbol     | Kind     | Line | References |
|------------|----------|------|------------|
| MyFunc     | function | 42   | 0          |
| MyType     | type     | 87   | 0          |

### Test-Only References
| Symbol      | Kind     | Line | References | Test files     |
|-------------|----------|------|------------|----------------|
| HelperFunc  | function | 15   | 1          | foo_test.go    |

### Active Symbols
| Symbol    | Kind     | Line | References |
|-----------|----------|------|------------|
| PublicAPI | function | 3    | 12         |
```

Fill in:
- **N** — total count of exported symbols found by `list_symbols` after
  filtering for the language's export rule.
- **M** — count of symbols where `find_references` returned `[]`.
- **K** — count of symbols where every reference location is a test file.

---

## Coordinate Conversion

`list_symbols` returns **0-based** coordinates (LSP native).
`find_references` requires **1-based** coordinates.

Always apply this conversion before calling `find_references`:

```
line_for_refs = symbol.selectionRange.start.line + 1
col_for_refs  = symbol.selectionRange.start.character + 1
```

Quick reference table:

| list_symbols output | find_references input |
|-----------------------------|----------------------|
| selectionRange.start.line   | line + 1             |
| selectionRange.start.character | column + 1        |

Example: a symbol at `selectionRange.start = { line: 41, character: 5 }`
requires `find_references(line: 42, column: 6)`.

---

## Exported Symbol Detection by Language

| Language   | Exported means...                                                      |
|------------|------------------------------------------------------------------------|
| Go         | Identifier starts with an uppercase letter (e.g. `MyFunc`, `MyType`)  |
| TypeScript | Has `export` keyword; or is a public class member (no `private`)       |
| Python     | Not prefixed with `_`; or explicitly listed in `__all__`               |
| Java/C#    | Has `public` or `protected` visibility modifier                        |
| Rust       | Has `pub` keyword                                                      |

When in doubt, treat the symbol as exported and check references anyway.
The cost is one extra tool call; the benefit is avoiding a false "not dead"
conclusion.

---

## False-Positive Categories

These are cases where `find_references` returns `[]` (or a low count) even
though the symbol IS used at runtime. Never delete a zero-reference
candidate without checking these:

1. **Reflection usage**
   - Go: `reflect.TypeOf(MyType{})`, `reflect.ValueOf`, struct tag scanning
   - Java: `Class.forName("com.example.MyClass")`
   - Python: `getattr(module, "my_func")`
   The LSP sees no static call site, so the reference count is 0.

2. **`//go:linkname` or assembly-linked symbols**
   Go symbols linked via `//go:linkname` in another package, or referenced
   directly from `.s` assembly files, are invisible to the LSP reference
   finder.

3. **Library public API (external consumers)**
   If the file being audited is part of a published library, callers in
   external modules not present in the workspace will never appear in
   `find_references` results. A zero count for a library export usually means
   "not called inside this repo", not "not called anywhere".

4. **Interface implementations verified at compile time**
   Go: `var _ io.Reader = (*MyReader)(nil)` — this line is a compile-time
   check, not a call. The symbol `MyReader` may appear in `find_references`
   output, but the intent is interface satisfaction, not usage.

5. **CGo exported functions**
   Functions annotated with `//export MyFunc` for CGo are callable from C
   code. The LSP has no visibility into C callers.

6. **Build tag variants**
   A symbol compiled only under a specific OS or architecture
   (`//go:build linux`) may appear unused when the workspace is indexed on
   a different platform.

---

## Batching Pattern

For large files with many exported symbols, process in batches to avoid
overwhelming the LSP server:

```
Batch 1: symbols[0..4]   → call find_references for each
Batch 2: symbols[5..9]   → call find_references for each
...
```

Between batches, sanity-check: if a symbol that is clearly used (e.g., a
well-known public function) returns `[]`, the workspace may still be
loading. Steps to recover:

1. Wait 2–3 seconds.
2. Retry `find_references` for that symbol.
3. If it still returns `[]`, note it as "possibly incomplete — workspace
   indexing may be incomplete" in the report instead of flagging it as
   zero-reference.

A reliable signal that indexing is complete: re-querying a symbol that
previously returned `[]` now returns a non-empty list without any code
change.
