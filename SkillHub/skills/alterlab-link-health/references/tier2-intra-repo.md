# Tier 2 — Intra-repo file references

Goal: eliminate every `[ERROR] file://` entry in the lychee log. These are broken relative-path references between Markdown files in the same repo — always real breakage, never a CI artefact.

## Extract the target list

After Tier 1 lands and the link checker reruns, grep the log for local-file errors:

```bash
grep '\[ERROR\] file:///' baseline.log \
  | sed 's|^.*file:///home/runner/work/<repo>/<repo>/||' \
  | sort -u
```

Strip the CI runner's checkout prefix so what remains is repo-relative. Dedupe — the same broken target often appears in multiple files.

## Classification

For each unique missing path, decide one of three categories:

| Category | Signal | Fix |
|----------|--------|-----|
| **PATH_TYPO** | Target would exist under a near-identical name (`reference/` vs `references/`, `mermaid_diagrams/` vs `diagrams/`, `X.md` vs `x.md`). | Mechanical `replace_all` on the referring file(s). |
| **WRONG_PATH** | Target file exists elsewhere in the repo; link is missing `../` or has an extra prefix. | Rewrite the link with the correct relative path. |
| **MISSING_FILE** | Target genuinely doesn't exist, and the link is inside a **template file** with illustrative prose. | Decide per Mermaid-placeholder policy (see below). |

## Common bug patterns

### Singular/plural directory name drift

When a skill is ported from an upstream project, the link URLs often preserve the upstream folder name (`reference/`) while the ported folder uses a different convention (`references/`). Grep + replace per-file:

```bash
grep -c '](reference/' skills/<skill>/SKILL.md
# N occurrences

# Safe if `reference/` is never a substring of `references/` (it isn't):
sed -i 's|](reference/|](references/|g' skills/<skill>/SKILL.md
```

**Check for collision**: before a bare `s/OLD/NEW/g`, grep for the candidate `NEW` text already in the file — if the substitution would corrupt existing occurrences, scope the match with a prefix (e.g. `](reference/` instead of `reference/`).

### Missing path prefix

Templates referencing style guides at `../X.md` when the guides actually live at `../references/X.md`. Same sed pattern, scoped to link syntax:

```bash
sed -i 's|](../markdown_style_guide\.md|](../references/markdown_style_guide.md|g' \
       skills/<skill>/templates/*.md
```

### YAML frontmatter indentation

If the repo's `validate-skills.yml` workflow parses YAML frontmatter, subtle indentation bugs under `metadata:` (e.g. a field indented 4 spaces under a `metadata:` block at column 0 with sibling fields at 2 spaces) will break the parser. These surface as Tier-2-adjacent issues worth catching while you're in the tree — but file anything beyond trivial indentation fixes as a separate schema PR.

## Mermaid-placeholder policy (pedagogical links)

Some template files deliberately include links to paths that **don't exist in the skill repo** — they illustrate the filename convention the skill's downstream consumer should adopt (`../adr/ADR-001-<slug>.md`, `../../docs/project/issues/issue-00000001-<slug>.md`, etc.).

Three options per placeholder:

| Option | Result | When |
|--------|--------|------|
| **A. Backtick-wrap** | ``[Label](../adr/foo.md)`` → ``Label — `../adr/foo.md` `` — inline code span. Lychee skips it; pedagogical value preserved. | **Default**. Preserves the filename example as visible code. |
| **B. Strip the link** | ``[Related ADR](../adr/foo.md)`` → `Related ADR` | When the path adds no teaching value. |
| **C. Create stub file** | Author a minimal `adr/ADR-001-<slug>.md` | When the referenced file is part of the skill's own promised content. |

**Default to A.** Option C should only be picked when the surrounding prose treats the file as skill-internal authoritative content, not an example for downstream consumers.

A precise sed for option A (note: POSIX ERE, `~` delimiter to avoid URL-slash collision):

```bash
sed -i -E 's~\[([^]]+)\]\((\.\./adr/[^)]*|\.\./workflow_guide\.md|\.\./operational_readiness\.md|\.\./\.\./docs/project/[^)]+)\)~\1 — `\2`~g' \
     skills/<skill>/templates/*.md
```

## Verify before committing

After the Tier 2 pass:

```bash
git diff --stat
# Line edits should be symmetric (N insertions, N deletions) — pure renames.

# Any asymmetric file-count line suggests unintended changes; inspect.
```

The PR's commit message should list the pattern types you applied, not every individual file — reviewers want to see the *rules*, not 300 lines of renames.
