---
name: cleanup-dedupe
description: "Detect duplicated code blocks and refactor to DRY where it reduces complexity. Runs jscpd (multi-language), filters by signal-to-noise, and auto-extracts only token-identical blocks ≥30 LOC. Use when the user asks to deduplicate, DRY up, find copy-paste, or consolidate repeated logic. Example queries — \"DRY this up\", \"find copy-paste in the codebase\", \"consolidate repeated logic\", \"where are the duplicated blocks\"."
argument-hint: "[scope (optional path or glob)]"
user-invocable: true
---

Find duplicated code and consolidate where it reduces complexity. Auto-extract only token-identical, sizeable blocks. Smaller or divergent duplicates often shouldn't be DRY'd — premature abstraction is worse than 3 similar lines.

## Preflight

1. **Language detect** — jscpd handles 150+ languages, so we run it on whatever is present.
2. **Git state**: refuse auto-apply on dirty tree.
3. **Report dir**: ensure `.claude/cleanup-reports/` exists.
4. **Read existing util conventions**: where does the project keep shared utilities? Look for `lib/`, `utils/`, `shared/`, `common/`, package directories. Extracted code goes there.

## Detect

```bash
# jscpd - the standard for cross-language clone detection
bunx jscpd --min-tokens 70 --min-lines 30 --threshold 0 --reporters json --output /tmp/jscpd-out . 2>/dev/null \
  || npx jscpd --min-tokens 70 --min-lines 30 --reporters json --output /tmp/jscpd-out .
```

Parse `/tmp/jscpd-out/jscpd-report.json`. Each duplication entry has `firstFile`, `secondFile`, `lines`, `tokens`, and the actual fragment.

**Filter the noise** before further analysis:
- Drop matches in `node_modules/`, `dist/`, `build/`, `.next/`, `__generated__/`, `*.generated.*`.
- Drop matches inside test files mirroring each other (test setup duplication is often intentional).
- Drop matches that are just type/interface definitions — those go to `cleanup-types`.
- Drop matches in migration files.

## Assess

Write `.claude/cleanup-reports/cleanup-dedupe-{YYYY-MM-DD}.md`:

```markdown
# Duplication Assessment — YYYY-MM-DD

## Summary
- Total clones found: N (after filtering noise)
- HIGH confidence (auto-extractable): X
- MEDIUM (similar but divergent): Y
- LOW (structural similarity, intentional): Z
- Estimated LOC saved (HIGH only): ~N

## Clones

### Clone 1 — HIGH (extract to `packages/utils/src/format.ts`)
- Files: `apps/app/features/holdings/format.ts:15-67`, `apps/admin/features/users/format.ts:22-74`
- 52 lines, 380 tokens, identical
- Both implement `formatCompactNumber(n: number): string`
- Extract to: `packages/utils/src/formatCompactNumber.ts`, both sites import.

### Clone 2 — MEDIUM
- Files: A and B
- Similar structure but divergent in 3 spots — the formatting differs by locale, the rounding by precision.
- Recommendation: don't extract yet — the abstraction needs a parameterization design that the human should decide.

## Critical Assessment
[2-3 paragraphs: are duplicates concentrated in one area? Is there a missing shared package? Are the duplicates a sign that an early abstraction would have been wrong, OR that a missing abstraction is hurting?]
```

## Apply

**Auto-extract HIGH-confidence only.**

### Confidence rubric

**HIGH (auto-apply):**
- ≥30 LOC AND ≥70 tokens (jscpd defaults).
- Token-identical (jscpd's strict mode, after stripping comments and whitespace).
- Same function signature OR reducible to one with no parameter changes.
- Across 2+ files in the same workspace/package boundary OR a clear shared package exists.
- Not in test files, fixtures, or generated code.

**MEDIUM (report only):**
- Similar but with 1-3 spot divergences — needs parameterization design.
- Cross-package duplication where extraction requires creating a new shared package.
- 15-29 LOC — borderline; sometimes 3 similar functions are clearer than 1 over-parameterized one.

**LOW (note, no action):**
- Structural similarity (e.g., 5 React components with the same prop-spreading pattern) — usually intentional.
- Test setup boilerplate.

### Execution (HIGH only)

1. Determine the destination:
   - Same package: existing `lib/` or `utils/` directory.
   - Different packages: shared package if one exists (e.g., `packages/utils/`), else escalate to MEDIUM (don't auto-create new packages).
2. Create the new util file with the extracted function. Use the canonical name from one of the source files; prefer the more descriptive name.
3. Replace both source occurrences with imports of the new util.
4. Delete the originals.
5. Single commit: `chore(cleanup): cleanup-dedupe — extracted N shared utilities`.

## Verify

```bash
bun run check 2>&1 || npx tsc --noEmit && npx eslint .
bun test 2>&1 || pytest 2>&1
# Re-run jscpd to confirm reduction
bunx jscpd --min-tokens 70 --min-lines 30 . 2>&1
```

If verify fails: revert and downgrade all to MEDIUM.

## Output

- "Extracted N shared utilities, saved ~M LOC. K duplicates deferred — see report."
- Report path.
- Verify status.

## NEVER

- Extract code from generated/`.d.ts`/migration files.
- Create a new shared package automatically — escalate that decision.
- Extract React/Vue components on prop-pattern similarity alone — composition vs. abstraction is design judgment.
- Force an abstraction that requires changing function signatures of either source — that's a behavior change, not a refactor.
- DRY two similar test cases — tests benefit from explicitness; let them duplicate.
- Extract code that has different error handling or different side effects in each location — not actually duplicate behavior.
