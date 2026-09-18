---
name: cleanup-weak-types
description: "Replace weak types (any, unknown, interface{}, untyped Python) with strong, inferable types. Researches actual usage to determine the correct type, runs typecheck after each change, reverts individual changes that fail. Use when the user asks to remove any/unknown, strengthen typing, fix weak types, or make code more type-safe. Example queries — \"remove all the `any` types\", \"strengthen our typing\", \"stop using unknown everywhere\", \"make this more type-safe\"."
argument-hint: "[scope (optional path or glob)]"
user-invocable: true
---

Replace weak escape-hatch types with strong types inferred from actual usage. Per-occurrence verification — each replacement is typechecked individually, reverted if it breaks. Conservative on public APIs.

## Preflight

1. **Language detect**: TS/JS (`any`, `unknown`, `as unknown as`, `Function`, `Object`), Python (`Any`, missing type hints), Go (`interface{}`, `any` since 1.18), Rust (`Box<dyn Any>` is rare; mostly look for `Box<dyn Trait>` where a concrete type would do).
2. **Git state**: refuse on dirty tree.
3. **Report dir**: ensure exists.
4. **Read project conventions**: check for a `check:weak-types` (or similar) script in package.json. Check `tsconfig.json` for `strict`/`noImplicitAny` flags. Check `mypy.ini` / `pyproject.toml [tool.mypy]` for strictness.
5. **Read allow-list**: many projects allow weak types in specific files (e.g., `*.test.ts`, generated code, third-party shim files). Find and respect them.

## Detect

### TypeScript / JavaScript
```bash
# Explicit `any`
grep -rn --include="*.ts" --include="*.tsx" -E "\b(: any\b|<any>|as any\b|as unknown as)" \
  --exclude-dir=node_modules --exclude-dir=dist --exclude-dir=.next . > /tmp/ts-weak.txt

# Compiler-derived implicit-any (more accurate than grep)
npx tsc --noImplicitAny --noEmit 2>&1 | grep "implicitly has an 'any' type" > /tmp/ts-implicit-any.txt
```

For each occurrence, capture the surrounding context (function signature, callers).

### Python
```bash
# Explicit Any imports + usage
grep -rn --include="*.py" -E "(from typing import.*Any|: Any\b|-> Any\b)" . > /tmp/py-any.txt

# Mypy strict mode finds untyped functions
mypy --disallow-untyped-defs --no-incremental . > /tmp/py-untyped.txt 2>&1 || true
```

### Go
```bash
grep -rn --include="*.go" -E "\binterface\{\}|\bany\b" . > /tmp/go-any.txt
```

### Rust
```bash
grep -rn --include="*.rs" -E "(Box<dyn |&dyn )" . > /tmp/rust-dyn.txt
```

## Assess

Write `.claude/cleanup-reports/cleanup-weak-types-{YYYY-MM-DD}.md`:

```markdown
# Weak Types Assessment — YYYY-MM-DD

## Summary
- Total weak-type sites: N
- HIGH (safe to auto-fix): X
- MEDIUM (public API or cross-package): Y
- LOW (justified — e.g., genuine unknown JSON, third-party): Z

## Findings

### HIGH — `apps/app/lib/parse.ts:45` `function process(data: any)`
- Inferable type: `data` is always called with `{ id: string; events: Event[] }` (3 callers checked).
- Replacement: `function process(data: { id: string; events: Event[] })`.
- Even better: lift to a named type `ProcessInput`.

### MEDIUM — `packages/sdk/src/client.ts:12` `function send(payload: any): Promise<any>`
- Public API of an SDK package — changing the type is a breaking change.
- Recommendation: introduce a generic `<T, R>` and have callers specify, OR use `unknown` and require validation.

### LOW — `lib/json.ts:8` `function parseJson(s: string): unknown`
- Genuinely unknown — JSON.parse output. Keep as `unknown`, ensure callers narrow.

## Critical Assessment
[2-3 paragraphs: where are weak types concentrated? Boundary code (HTTP handlers, JSON parsing) often justifies them. Internal logic almost never does.]
```

## Apply

**Auto-fix HIGH only, ONE AT A TIME with typecheck between each.** This is essential — bulk type changes can cascade in hard-to-predict ways.

### Confidence rubric

**HIGH (auto-apply, individually):**
- The weak type is in a private/internal function.
- All callers are in the same repo and pass the same type (or a small finite set easily expressed as a union).
- Replacement is mechanically derivable from usage.
- No re-export of the symbol from a package boundary.

**MEDIUM (report only):**
- Public API surface (exported from a package, used by a `.d.ts`, part of an SDK).
- Generic-amenable signatures (suggest the generic but don't apply).
- Discriminated union opportunities — the human picks the discriminator field.
- `as unknown as` casts — these usually indicate a deeper type design problem.

**LOW (note, no action):**
- Boundary code receiving genuine unknown input (HTTP body before validation, `JSON.parse`, dynamic config).
- Third-party shim files where the actual library is untyped.
- Test files (allowed in most weak-type allow-lists).

### Execution (HIGH, individually)

For EACH HIGH finding:
1. Capture the exact `git diff` of the proposed change.
2. Apply the change (Edit).
3. Run scoped typecheck: `bun run typecheck` or `tsc --noEmit`. For Python: `mypy <file>`.
4. If typecheck fails OR introduces new errors elsewhere: `git checkout -- <file>`, downgrade this finding to MEDIUM in the report, continue.
5. If typecheck passes, move on.

After all HIGH findings processed, single commit: `chore(cleanup): cleanup-weak-types — strengthened N type signatures`.

## Verify

```bash
# Full typecheck across the repo (not just changed files)
bun run typecheck 2>&1
mypy --strict . 2>&1 || mypy . 2>&1
go build ./... 2>&1
cargo check 2>&1

# Tests — important here, since type changes can affect runtime via narrowing
bun test 2>&1
pytest 2>&1
go test ./... 2>&1
cargo test 2>&1

# Project-specific weak-types gate
bun run check:weak-types 2>/dev/null || true  # project-specific script, if defined
```

If anything fails after the per-file pass somehow (rare but possible across-file inference): revert all and downgrade. Should rarely happen because we typecheck after each.

## Output

- "Strengthened N weak types. M deferred for review."
- Report path with breakdown of HIGH/MEDIUM/LOW.
- Verify status.

## NEVER

- Bulk replace `any` with `unknown` — that's a different defect, not a fix. Both are weak; `unknown` just forces narrowing.
- Replace `any` with an over-narrow type that breaks one of N callers — verify ALL callers fit.
- Touch generated types (Drizzle `$inferSelect`, OpenAPI codegen, Prisma) — fix the codegen config instead.
- Add `// @ts-ignore` or `# type: ignore` to make the change pass — that's hiding the problem.
- Modify ambient `.d.ts` declarations for third-party libraries.
- Remove an `as unknown as` cast without understanding why it was added — it's often masking a type incompatibility worth investigating, not silently fixing.
- Auto-add generics to public APIs — that's a contract change requiring human design.
