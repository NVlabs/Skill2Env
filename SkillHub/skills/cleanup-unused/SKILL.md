---
name: cleanup-unused
description: "Detect and delete unused code, exports, files, and dependencies. Runs knip/vulture/staticcheck/cargo-machete appropriate to the language, writes a critical assessment, and auto-applies HIGH-confidence deletions. Use when the user asks to remove dead code, find unused exports, clean up dependencies, or run dead-code analysis. Example queries — \"find dead code\", \"what's unused in this repo\", \"are there unused npm deps\", \"kill the cruft\"."
argument-hint: "[scope (optional path or glob)]"
user-invocable: true
---

Detect unused code, exports, files, and dependencies. Auto-delete only what's verifiably dead. Write a critical assessment with confidence ratings; defer ambiguous items to the human.

## Preflight

1. **Detect language(s)** by checking for: `package.json` (TS/JS), `pyproject.toml`/`requirements.txt` (Py), `go.mod` (Go), `Cargo.toml` (Rust). Skip languages not present.
2. **Check git state.** If working tree is dirty, refuse to auto-apply — ask user to stash or commit first. The verify step needs a clean baseline to revert to.
3. **Create report dir**: `mkdir -p .claude/cleanup-reports/`. Add `.claude/cleanup-reports/` to `.gitignore` if not already present.
4. **Scan for dynamic-import patterns** that defeat static analysis. Save the list — findings in these areas drop to MEDIUM confidence.
   - JS/TS: `import(`, `require(`, `eval(`, `Function(`, `__webpack_require__`, dynamic route file conventions (`pages/`, `app/`)
   - Python: `__import__`, `importlib`, `getattr`, plugin entry-points in `setup.py`/`pyproject.toml`
   - Go: `reflect.`, plugin loader, build tags
   - Rust: `cfg(feature = ...)` gates, proc-macros, `extern crate`

## Detect

Run the right tool per language. Install on demand only after asking.

### TypeScript / JavaScript
```bash
# Knip is the gold standard. Most TS/JS repos already have it wired up.
bunx knip --reporter json > /tmp/knip.json 2>/dev/null || npx knip --reporter json > /tmp/knip.json
```
Parse `files`, `exports`, `types`, `dependencies`, `devDependencies`, `unlisted`, `binaries` arrays.

### Python
```bash
uvx vulture . --min-confidence 80 --json > /tmp/vulture.json 2>/dev/null || pipx run vulture . --min-confidence 80
```
Vulture confidence ≥80 maps roughly to our HIGH; 60-79 = MEDIUM.

### Go
```bash
go install honnef.co/go/tools/cmd/staticcheck@latest 2>/dev/null
staticcheck -checks=U1000 ./... > /tmp/staticcheck.txt
```
U1000 = unused code.

### Rust
```bash
cargo install cargo-machete 2>/dev/null
cargo machete --with-metadata > /tmp/machete.txt    # unused deps
cargo +nightly udeps 2>/dev/null || true            # optional, nightly-only
```
Use `RUSTFLAGS="-W dead_code"` and re-build for in-crate dead code if needed.

## Assess

Write `.claude/cleanup-reports/cleanup-unused-{YYYY-MM-DD}.md` with:

```markdown
# Unused Code Assessment — YYYY-MM-DD

## Scope
- Languages detected: [TS, Py, …]
- Tools run: [knip, vulture, …]
- Dynamic-import risk areas: [list paths]

## Summary
- Unused files: N (HIGH: x, MEDIUM: y)
- Unused exports: N (HIGH: x, MEDIUM: y)
- Unused dependencies: N (HIGH: x, MEDIUM: y)
- Total LOC removable (HIGH only): ~N

## Findings

| Conf | Type | Location | Tool said | Recommendation |
|------|------|----------|-----------|----------------|
| HIGH | export | src/utils/foo.ts:12 `parseDate` | knip: unused export | Delete export + function |
| MED  | file | src/legacy/old.ts | knip: unused file | Defer — referenced from dynamic import area |
| ...

## Critical Assessment

[2-4 paragraphs of human-readable analysis]
- What patterns emerged? (e.g., "8 of 12 unused exports are in `lib/legacy/` — consider deleting the whole directory")
- Why were items downgraded from HIGH to MEDIUM?
- Architectural observations.

## Out of scope
- [Items the tool flagged but skill won't touch — public API surfaces, framework conventions, etc.]
```

## Apply

**Auto-apply HIGH-confidence only.** Group all deletions into one commit.

### Confidence rubric

**HIGH (auto-apply):**
- Tool flagged the item AND it's not in a dynamic-import risk area
- Not on a public API surface (`index.ts`, `__init__.py`, `pub` items, package `main`/`exports`)
- Has zero references in the entire repo (verify with grep, not just the tool's word)
- For deps: not used in any script, config, or runtime require

**MEDIUM (report only, don't apply):**
- Tool flagged BUT one of: in dynamic-import area, on public API surface, has indirect references (re-exports), is a type-only export from a `.d.ts` consumed externally
- Vulture confidence 60-79
- Dependencies that appear in `peerDependencies` or are used by build tooling

**LOW (note in report, no action):**
- Heuristic guesses with no tool backing
- Things the user previously declined to delete (check git log for prior reverts)

### Execution

1. Delete files: `rm <path>` — but verify no `.gitignore`'d sibling files reference them first.
2. Remove exports: `Edit` to remove the export keyword + drop the symbol if internal usage is also zero.
3. Uninstall deps: `bun remove <pkg>` / `pip uninstall <pkg>` / `cargo remove <pkg>` — pick the manager from lockfile presence.
4. Single commit: `git add -A && git commit -m "chore(cleanup): cleanup-unused — N items removed"`.

## Verify

Run **all** that apply, in order. Halt and revert on first failure.

```bash
# Typecheck
bun run typecheck 2>&1 || npx tsc --noEmit
mypy . 2>&1 || true
go build ./... 2>&1
cargo check 2>&1

# Tests (if scripts exist)
bun test 2>&1 || npm test 2>&1
pytest 2>&1
go test ./... 2>&1
cargo test 2>&1

# Lint
bunx biome check . 2>&1 || npx eslint . 2>&1
ruff check . 2>&1
golangci-lint run 2>&1
cargo clippy 2>&1
```

If any fail: `git revert HEAD --no-edit`, downgrade all auto-applied items to MEDIUM in the report, append a "## Verify Failure" section with the error output.

## Output

End-of-turn message (≤4 lines):
- "Removed N unused items (X files, Y exports, Z deps). M deferred for review."
- Path to the report.
- Verify status (✓ all green, ✗ reverted).

## NEVER

- Delete anything in `node_modules/`, `.next/`, `dist/`, `build/`, or other generated dirs.
- Delete migration files (`drizzle/*.sql`, `alembic/`, `migrations/`) even if they look unused — they describe history.
- Delete test fixtures based on knip flags — they're often loaded by glob.
- Auto-apply on a dirty working tree — refuse and ask.
- Trust knip blindly for files in framework convention directories (Next.js `app/`, `pages/`, Remix `routes/`, etc.) — those have routing-based dynamic loads.
- Run `npm install --force` or any flag that bypasses lockfile integrity if a dep removal causes resolution issues.
