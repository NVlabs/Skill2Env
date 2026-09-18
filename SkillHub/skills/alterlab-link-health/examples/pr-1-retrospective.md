# Example — PR #1 Retrospective

The source audit that generated this skill. Real numbers, real commits, one real self-correction.

- **Repo**: `AlterLab-IEU/AlterLab-Academic-Skills`
- **PR**: [#1 fix(ci): harden link-check workflow and repair broken refs (link-health audit)](https://github.com/AlterLab-IEU/AlterLab-Academic-Skills/pull/1)
- **Audit + merge**: 2026-04-21, squash commit `93a72fe`
- **Branch**: `fix/link-health-audit` (deleted on merge)

## Before / after

Against the weekly `Check Links` workflow run 24662239329 (scheduled, 2026-04-20) for baseline, and `workflow_dispatch` run 24710712721 on the branch for final:

| Metric | Baseline (main) | After (fix/link-health-audit) | Δ |
|--------|----------------:|-------------------------------:|---:|
| Total links | 1966 | 1912 | -54 |
| ✅ Successful | 684 | **1497** | **+813** |
| 🔀 Redirected | 26 | 265 | +239 |
| 👻 Excluded | 42 | 148 | +106 |
| 🚫 **Errors** | **1208** | **0** | **-1208** |
| ⏳ Timeouts | 4 | 0 | -4 |
| ⛔ Unsupported | 2 | 2 | 0 |

Why the totals shifted by 54:
- Broken intra-repo `file://` refs that resolved in Tier 2 collapsed several near-duplicate entries (the same missing target was linked from multiple markdown files).
- The wider accept set + broader `.lycheeignore` reclassified many entries as Redirected or Excluded instead of probed-and-rejected.

## Commits on the branch (8 + 1 post-merge)

| # | SHA | Tier | Message |
|---|-----|------|---------|
| 1 | `96b5c27` | Tier 1 config | ci(links): add .lychee.toml, .lycheeignore, harden check-links workflow |
| 2 | `91079e9` | Tier 2 file refs | docs(refs): fix broken intra-repo Markdown links in skills tree |
| 3 | `0c8c272` | Tier 3 substitutions | docs(refs): replace moved / dead external URLs with current locations |
| 4 | `f025748` | Tier 4 exclusions | ci(links): extend .lycheeignore for unfixable / placeholder URLs |
| 5 | `9cbd801` | Fix-up | fix(links): repair post-dispatch regressions and broaden exclude list |
| 6 | `31fa0f5` | Fix-up | fix(links): close last 5 residual errors |
| 7 | `204e591` | Fix-up | fix(links): bump retries + exclude two chronically-flaky hosts |
| 8 | `426363c` | Post-merge cleanup | chore(links): finalize benchling substitution, document link debt |

Merged as `93a72fe` on `main`.

## Error trajectory

| Stage | Errors | Delta |
|-------|-------:|------:|
| Baseline (main) | 1208 | — |
| After Tier 1 (commit 1) + Tier 2 (commit 2) + Tier 3 (commit 3) + Tier 4 (commit 4) — first dispatch | 67 | **-1141** |
| After fix-up (commit 5) | 5 | -62 |
| After fix-up (commit 6) | 1 | -4 |
| After fix-up (commit 7) | 0 | -1 |

## The self-correction (why the Tier 3 guardrail exists)

Commit 3 (`0c8c272`) applied 57 URL substitutions across 46 files via a single batched `sed` pass. When the first dispatch landed at 67 errors (not the predicted 10-40), the triage surfaced three classes of regressions the Tier 3 commit had introduced:

1. **Double-append from prefix rules.** `s|/v3/|/v3/docs|g` also matched URLs already ending in `/v3/docs`, producing `/v3/docsdocs`. Affected: `api-v3.monarchinitiative.org`.
2. **Concatenation onto specific paths.** `s|pylabrobot.org/api/|pylabrobot.org/user_guide/index.html|g` merged onto trailing segments, producing `user_guide/index.htmlpylabrobot.liquid_handling.html`. Affected: 5 pylabrobot reference files.
3. **Chain-substitution overreach.** `s|clinvar/docs/|clinvar/docs/help/|g` rewrote specific sub-paths like `clinvar/docs/xsd_public/` into non-existent `clinvar/docs/help/xsd_public/`. Affected: 4 ClinVar reference files.

Plus one Tier 2 crossover bug: `s|reference/|references/|g` also matched inside an external URL `plotly.com/python-api-reference/`, turning it into `python-api-references/` (404).

Commit 5 (`9cbd801`) repaired all 11 regressions with narrower sed patterns. The Tier 3 guardrail rule (`references/tier3-substitution.md`) was derived from this experience: **rerun the link checker after each substitution pass and diff the baseline's 200-set against the post's 200-set**. Deletions from that diff are guaranteed regressions.

## Post-merge cleanup (commit 8 / PR `chore`)

The `benchling/benchling-sdk` GitHub URL was left in `.lycheeignore` during Tier 4 because the obvious substitute `benchling/benchling-api-client` returned 404 on the GitHub API (verified with `gh api repos/benchling/benchling-api-client` before choosing exclude over replace — an application of the Verification-First Rule). Later, `curl -sSI https://pypi.org/project/benchling-sdk/` returned 200, so the URL was substituted to PyPI in the post-merge cleanup, and the exclusion block was removed.

Filed as follow-up issues alongside commit 8:
- [#2 Pylabrobot docs refresh after MyST migration settles](https://github.com/AlterLab-IEU/AlterLab-Academic-Skills/issues/2) — tracks the `docs.pylabrobot.org/*` blanket exclusion.
- [#3 SKILL.md schema drift audit](https://github.com/AlterLab-IEU/AlterLab-Academic-Skills/issues/3) — schema observations surfaced during the audit, deliberately kept out of the link-health PR.

Created `.github/KNOWN_LINK_DEBT.md` documenting every current `.lycheeignore` entry with reason, date, and revisit trigger or tracking issue.

## Lessons that shaped this skill

1. **Config before content.** Tier 1 alone cut 900+ errors. Fixing intra-repo refs and replacing dead URLs on top of a broken `--accept` flag would have wasted cycles on work the config fix obviated.
2. **Verify every substitute.** One unverified `benchling-api-client` guess that actually 404s would have ridden to main and confused maintainers for months. `gh api repos/<owner>/<name>` is cheap; trust is expensive.
3. **Broad sed is a trap.** Applying 50+ prefix substitutions in one pass produced three classes of regressions not one of which was caught by reading the commit diff. The guardrail diff caught all of them on the first dispatch.
4. **Scope discipline compounds.** Every observation from the audit that *wasn't* link-health (SKILL.md schema, license-field normalization, category renames) got filed as a separate issue. The PR stayed one-topic and reviewable.
5. **The rationale is the PR body, not the commit.** Root-cause explanations survive longer in PR descriptions than in squashed commit messages. A future maintainer reads the PR first.

## Reproducing this audit on another repo

The 10-agent playbook in `playbooks/full-audit.md` is the dispatch prompt. Swap `AlterLab-IEU/AlterLab-Academic-Skills` for the target repo, point the scratch dir at a fresh location, and follow the tier-by-tier APPLY sequence. Expect 30-60 minutes from cold start to PR green on a repo of similar size (~2000 links).
