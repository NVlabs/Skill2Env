---
name: cleanup-cycles
description: "Detect and untangle circular dependencies. Runs madge/skott (TS), pycycle (Py), or compiler-only checks (Go/Rust). Auto-fixes leaf-extractable cycles; reports core cycles for human review. Use when the user asks to find circular imports, fix dependency cycles, or untangle module graph. Example queries — \"find circular imports\", \"fix dependency cycles\", \"untangle our module graph\", \"why is madge complaining\"."
argument-hint: "[scope (optional path or glob)]"
user-invocable: true
---

Detect circular import dependencies and break them where it's mechanically safe. Cycles between leaf utilities can be fixed by extraction; cycles between core modules need architectural decisions and are reported, not auto-fixed.

## Preflight

1. **Language detect**: `package.json` (TS/JS), `pyproject.toml` (Py), `go.mod` (Go), `Cargo.toml` (Rust). Note: Go and Rust prevent cycles at compile time, so this skill is mostly TS/Py work.
2. **Git state**: refuse auto-apply on dirty tree.
3. **Report dir**: ensure `.claude/cleanup-reports/` exists.
4. **Existing scripts**: check `package.json` for a `cycle:check` (or similar) script — if the repo already wires up madge with custom config, prefer that over defaults.

## Detect

### TypeScript / JavaScript
```bash
# Madge is the standard. Skott is faster for large repos.
bunx madge --circular --extensions ts,tsx,js,jsx --json src/ apps/ packages/ > /tmp/madge.json 2>/dev/null \
  || npx madge --circular --extensions ts,tsx --json . > /tmp/madge.json
```
Each entry is an array describing one cycle: `["a.ts", "b.ts", "a.ts"]`.

### Python
```bash
pipx run pycycle --here --verbose > /tmp/pycycle.txt 2>&1 || true
# Fallback: import-linter with auto-config
pipx run import-linter > /tmp/import-linter.txt 2>&1 || true
```

### Go
```bash
# Go enforces acyclic at compile; this just confirms build is clean.
go build ./... 2>&1
# Optional: visualize with goda for ergonomics
go install github.com/loov/goda@latest 2>/dev/null
goda graph ./... > /tmp/goda.dot 2>/dev/null || true
```
If `go build` fails with `import cycle`, that's the report.

### Rust
```bash
cargo build 2>&1   # rustc rejects cycles
# For visibility into module graph: cargo-modules
cargo install cargo-modules 2>/dev/null
cargo modules generate tree 2>/dev/null || true
```

## Assess

Write `.claude/cleanup-reports/cleanup-cycles-{YYYY-MM-DD}.md`:

```markdown
# Circular Dependencies Assessment — YYYY-MM-DD

## Summary
- Total cycles: N
- HIGH confidence (auto-fixable by leaf extraction): X
- MEDIUM confidence (refactor needed): Y
- LOW (architectural redesign): Z

## Cycles

### Cycle 1 — HIGH
- Path: `a/util.ts → b/helper.ts → a/util.ts`
- Shared piece: `formatCurrency` defined in `b/helper.ts`, called by `a/util.ts`. `b/helper.ts` imports a single constant `LOCALE` from `a/util.ts`.
- Plan: Extract `LOCALE` to new `a/constants.ts`. `b/helper.ts` imports from there. Cycle broken.

### Cycle 2 — MEDIUM
- Path: `domains/user/index.ts → domains/account/index.ts → domains/user/index.ts`
- Both modules export and consume each other's primary types. No leaf to extract.
- Recommendation: introduce a `domains/shared/types.ts` for cross-domain types, OR invert one direction with dependency injection.

## Critical Assessment
[2-3 paragraphs: what does the cycle pattern reveal about the architecture? Are cycles concentrated in one area? Is there a missing layer?]
```

## Apply

**Auto-fix HIGH-confidence leaf-extraction cycles only.**

### Confidence rubric

**HIGH (auto-apply):**
- Cycle has exactly 2 modules.
- One direction of the cycle is a single small thing: a constant, a type, a pure utility function ≤20 lines, with no further dependencies inside the cycle.
- Extracting that thing to a new module will provably break the cycle.

**MEDIUM (report only):**
- Cycle has 3+ modules.
- Both directions consume non-trivial APIs of the other.
- Extracting would require moving classes/functions with their own dependency tails.

**LOW (note for human):**
- Cycle is structural (e.g., bidirectional ORM relations, parent/child component refs) — may be intentional.
- Cycle disappears under conditional imports — leave alone, document.

### Execution (HIGH only)

1. Identify the leaf piece (constant/type/util).
2. Create new file at the appropriate location: `src/<area>/<name>.ts`. Prefer placing inside the consumer that has fewer outside imports.
3. Move the leaf there.
4. Update both old modules' imports.
5. Re-run madge/pycycle to confirm the cycle is gone.
6. Commit: `chore(cleanup): cleanup-cycles — N cycles broken via leaf extraction`.

## Verify

```bash
# Re-run cycle detection — should report 0 for HIGH-applied cycles
bunx madge --circular . 2>&1
pycycle --here 2>&1
go build ./... 2>&1
cargo build 2>&1

# Then standard typecheck/test/lint (see cleanup-unused for full list)
bun run check 2>&1 || npx tsc --noEmit && npx eslint .
pytest 2>&1
```

If verify fails or new cycles appear: `git revert HEAD`, mark fixes as MEDIUM, escalate.

## Output

- "Broke N circular dependencies. M cycles deferred for architectural review."
- Path to report.
- Verify status.

## NEVER

- Auto-apply on cycles with 3+ modules — these always need human judgment.
- Use barrel files (`index.ts` re-exports) as the cycle-breaking solution — they often hide cycles instead of fixing them.
- Touch framework-imposed cycles (e.g., React component file importing its own types from a sibling) — those are conventions, not bugs.
- Move types into a `types.ts` god-file — prefer co-location with the smallest scope that breaks the cycle.
- Suppress cycle warnings via tooling config — fix or report, never silence.
