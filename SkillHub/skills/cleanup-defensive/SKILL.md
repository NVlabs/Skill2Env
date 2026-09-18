---
name: cleanup-defensive
description: "Remove pointless try/catch blocks and defensive guards that hide errors or add no value. Preserves catches at true system boundaries (HTTP handlers, CLI entry, message consumers). Use when the user asks to remove try/catch, fix error hiding, clean up defensive code, or stop swallowing errors. Example queries — \"remove pointless try/catch\", \"we're swallowing errors\", \"stop hiding bugs in catch blocks\", \"clean up the defensive code\"."
argument-hint: "[scope (optional path or glob)]"
user-invocable: true
---

Remove try/catch and defensive null-checks that don't serve a real role. The goal is errors that propagate cleanly to the boundary that knows how to handle them, not silent fallbacks that hide bugs.

**Core principle**: catch only when you can do something more useful than the default propagation — and "log and rethrow" is rarely more useful than just letting it throw.

## Preflight

1. **Language detect**: TS/JS, Python, Go (`if err != nil` patterns), Rust (`unwrap_or`/`map_err` chains that smell defensive).
2. **Git state**: refuse on dirty tree.
3. **Report dir**: ensure exists.
4. **Identify boundary files** — preserve catches in:
   - HTTP request handlers (`app/api/`, `routes/`, Hono/Express/FastAPI handlers)
   - CLI entry points (files with `if __name__ == "__main__"`, `bin/*`, `cmd/*`)
   - Message/queue consumers (worker entry points, cron handlers)
   - Test files (test runners need failures localized)

## Detect

### TypeScript / JavaScript
```bash
# Find every try/catch
grep -rn --include="*.ts" --include="*.tsx" --include="*.js" -B1 -A5 "try {" \
  --exclude-dir=node_modules --exclude-dir=.next . > /tmp/try-catches.txt

# ESLint can flag the obvious useless ones
npx eslint --rule '{"no-useless-catch": "error"}' --no-eslintrc . 2>&1 | grep no-useless-catch > /tmp/useless-catch.txt
```

Categorize each catch block by content:
- **Rethrow only**: `catch (e) { throw e }` or `catch (e) { throw new Error(...) }` with no context added
- **Swallow + null/empty return**: `catch { return null }`, `catch { return [] }`, `catch { return {} }`
- **Swallow + log only**: `catch (e) { console.error(e) }` then continue silently
- **Log + rethrow**: `catch (e) { logger.error(e); throw e }` — usually pointless if a global handler logs
- **Substantive**: actually does cleanup, retries, returns a typed Result, transforms the error meaningfully

### Python
```bash
grep -rn --include="*.py" -B1 -A5 "try:" . > /tmp/py-try.txt
# Bare except is always defensive
grep -rn --include="*.py" -E "except\s*:|except\s+Exception\s*:" . > /tmp/py-bare-except.txt
```

### Go
```bash
# Find error-swallowing patterns: ignored errors, generic fallbacks
grep -rn --include="*.go" -E "_ = .*\.Err|_, _ =" . > /tmp/go-ignored.txt
```

### Rust
```bash
grep -rn --include="*.rs" -E "\.unwrap_or\(|\.unwrap_or_default\(|\.ok\(\)" . > /tmp/rust-defensive.txt
```

## Assess

Write `.claude/cleanup-reports/cleanup-defensive-{YYYY-MM-DD}.md`:

```markdown
# Defensive Code Assessment — YYYY-MM-DD

## Summary
- try/catch blocks scanned: N
- HIGH (remove): X — pure rethrow, swallow-and-return-null, useless wrappers
- MEDIUM (review): Y — log+rethrow, broad excepts with context
- LOW (preserve): Z — substantive handling, boundary code

## Findings

### HIGH — `lib/parse.ts:45`
```ts
try {
  return JSON.parse(s)
} catch (e) {
  return null
}
```
**Problem**: caller can't distinguish "valid JSON null" from "parse failed". Hides bugs.
**Fix**: remove try; let JSON.parse throw. If callers need optional, change return to `Result<T, ParseError>` or have caller wrap.

### HIGH — `services/user.ts:88`
```ts
try {
  return await fetchUser(id)
} catch (e) {
  throw e
}
```
**Problem**: literally a no-op wrapper.
**Fix**: remove try/catch entirely.

### MEDIUM — `services/payment.ts:120`
```ts
try {
  await charge(amount)
} catch (e) {
  logger.error('charge failed', { e, userId })
  throw e
}
```
**Problem**: log+rethrow. If global handler also logs, this is duplication.
**Recommendation**: check if there's a global error logger. If yes, remove. If the contextual data (`userId`) isn't otherwise captured, keep but add a note.

### LOW — `app/api/[...path]/route.ts:34` — preserve, this is the API boundary.

## Critical Assessment
[2-3 paragraphs on patterns: is this codebase prone to silent fallbacks? Are there layers wrapping errors unnecessarily?]
```

## Apply

**Auto-remove HIGH only.**

### Confidence rubric

**HIGH (auto-remove):**
- `try { x } catch { } ` (silent swallow, no return)
- `try { x } catch (e) { throw e }` (no-op)
- `try { x } catch (e) { throw new Error(e.message) }` (loses stack, adds nothing)
- `try { x } catch { return null/undefined/[]/{}/0 }` (silent fallback that hides errors) — only if file is NOT a boundary file
- Python `except: pass` blocks
- Go: `_ = someCall()` where the discarded value is `error`

**MEDIUM (report only):**
- Log + rethrow (might be intentional observability)
- Catch with retry logic
- Catch in middleware (might be intentional last-resort)
- `unwrap_or(default)` where default is a real value (might be intentional)

**LOW (preserve):**
- Inside boundary files (see preflight list)
- Inside `__init__.py` import-time error handlers (compatibility fallbacks)
- Catches that transform exception type meaningfully (e.g., `catch DBError { throw new ValidationError() }`)
- Cleanup catches with `finally` doing real work

### Execution

For each HIGH:
1. Remove the try wrapper, keep the body's expression.
2. If the function signature implied "may return null on error" because of the catch, that signature is now lying — flag for human review (do NOT change signatures automatically).
3. Single commit: `chore(cleanup): cleanup-defensive — removed N useless try/catch blocks`.

## Verify

```bash
bun run check 2>&1 || npx tsc --noEmit && npx eslint .
bun test 2>&1
pytest 2>&1
go test ./... 2>&1
cargo test 2>&1
```

Tests are critical here — removing a swallowed error often surfaces a real bug that was being hidden. If tests fail:
1. Read the failure carefully — is it a real bug being surfaced (good, don't revert; flag for human), or did we remove a catch that was load-bearing for tests (revert that one).
2. Default action: revert and downgrade to MEDIUM. The human can decide whether the surfaced failure is "actually a bug we should fix."

## Output

- "Removed N useless try/catch blocks. M deferred for review."
- Report path.
- Verify status. If tests surfaced previously-hidden errors: highlight clearly with "⚠️ Real errors surfaced — see report."

## NEVER

- Remove a catch in a request handler, route, message consumer, or CLI entrypoint.
- Remove a catch with `finally` that does cleanup (closing resources, releasing locks).
- Remove a catch that converts one error type to another semantically meaningful one.
- "Fix" Go's `if err != nil { return err }` patterns — that IS the proper Go way, not defensive code.
- Remove `unwrap()` from Rust without understanding the precondition; replacement should be `expect("reason")` minimum, or proper handling.
- Remove a Python `except` without checking if it's catching a specific expected exception.
- Modify error handling to "make tests pass" — the test failure may be the actual bug.
