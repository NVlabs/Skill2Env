---
name: alterlab-link-health
description: "Audits and repairs Markdown link health across a skills repo via a four-tier pipeline (config hardening, intra-repo file-ref fixes, external URL substitutions, residual exclusions) and enforces a Tier 3 substitution guardrail that prevents regressions of previously-passing links; designed for lychee-based GitHub Actions link checkers but generalizes to markdown-link-check and similar tools. Use when the request mentions link audit, dead links, link health, lychee, broken links, link checker, markdown link audit, link-health audit, 404 audit, check-links failing, CI link-check, or 連結健檢, 死鏈, 失效連結, 斷鏈檢查. Part of the AlterLab Academic Skills suite."
license: MIT
allowed-tools: Read Write Edit Bash WebFetch WebSearch
compatibility: Targets lychee-based GitHub Actions link checkers (generalizes to markdown-link-check); no external API key or account required
metadata:
  skill-author: AlterLab
  version: "1.0"
  last_updated: "2026-04-21"
  source_audit: "AlterLab-IEU/AlterLab-Academic-Skills PR #1 (merged 2026-04-21 as 93a72fe)"
---

# Link Health — Repo-wide Markdown Link Audit Methodology

A reusable methodology for bringing a broken docs-heavy repo's link checker to green. Codified from a real audit that took `AlterLab-IEU/AlterLab-Academic-Skills` from **1208 errors out of 1966 links** to **0 errors out of 1912 links** across 8 commits, with an auto-detected Tier 3 regression that validated the guardrail rule.

## Quick Start

**Full audit (fresh repo, failing link checker):**

```
Audit and repair the link health of <owner/repo>. Run the full four-tier pipeline.
```
→ Dispatch the 10-agent audit from `playbooks/full-audit.md`, then the tiered APPLY phase.

**Targeted residual pass (first dispatch reduced errors but some remain):**

```
The link checker is down from 1208 to 67 errors. Close the residuals.
```
→ Dispatch the 3-agent followup pass from `playbooks/followup-pass.md`.

**Post-merge cleanup (PR is green, need to finalize human-decision items):**

```
Finalize the post-merge cleanup: resolve pending human-decision items, file follow-up issues, document link debt.
```
→ Dispatch the 4-agent post-merge pass from `playbooks/post-merge.md`.

---

## Trigger Conditions

### Trigger Keywords

**English**: link audit, dead links, link health, lychee, broken links, link checker, markdown link audit, link-health audit, 404 audit, check-links failing, CI link-check

**繁體中文**: 連結健檢, 死鏈, 失效連結, 斷鏈檢查, 連結審計

### When This Skill Applies

- A weekly `Check Links` (or similar lychee / markdown-link-check) workflow has been failing.
- The user mentions a large error count (hundreds+) that they suspect is mostly config-driven false positives.
- The user wants to refactor broken intra-repo file references across many skills / docs.
- The user wants a reusable process for link debt maintenance going forward.

### Non-Trigger Scenarios

| Scenario | Skill / Tool to Use Instead |
|----------|-----------------------------|
| Fix a single broken link in a single file | Direct Edit — no pipeline needed |
| Add a new URL to skill docs | `alterlab-scientific-writing` or the relevant domain skill |
| Verify a bibliography actually exists (DOI/author resolution, fabricated/hallucinated citations) | `alterlab-citation-verifier` — it cross-checks Crossref/OpenAlex/Semantic Scholar/arXiv. Link-health only repairs broken hyperlinks in docs; it never validates that a cited work exists. |
| Audit repo structure beyond links (schema, metadata) | Separate `schema-drift` audit (out of scope) |

---

## Pipeline Overview (4 Tiers)

Each tier is a single reviewable commit. Run them in order — each unlocks the next by making the error signal cleaner.

| Tier | Scope | Typical Delta |
|------|-------|---------------|
| **1 — Config** | Introduce `.lychee.toml` with an additive accept set, a `.lycheeignore` for permanent noise hosts, and a hardened CI workflow. | Biggest single win — often -70% to -90% of errors. Fixes the "`--accept 403` replaces the default set" gotcha. |
| **2 — Intra-repo refs** | Repair `[ERROR] file://` entries: singular/plural directory typos, missing path prefixes, YAML frontmatter bugs. Wrap pedagogical placeholder paths as inline code. | Eliminates the bulk of real breakage — usually 200-400 entries collapse to zero. |
| **3 — URL substitutions** | Replace MOVED external URLs with verified-live substitutes; replace DEAD_INFRA URLs with replacement resources. **Never substitute without verification.** | Reduces residuals to the low dozens. |
| **4 — Exclusions** | Everything left that cannot be fixed: bot-hostile hosts, pedagogical placeholders, expired upstream infrastructure, chronically flaky academic sites. | Gets to 0 errors or stable single-digit residuals. |

See `references/tier1-config.md` through `references/tier4-exclusions.md` for the decision rules in each tier.

---

## The Tier 3 Guardrail

After any URL substitution pass, **re-run the link checker and diff against the baseline success set**. Any URL that returned 200 OK in baseline and is non-200 after substitution is a regression and MUST be reverted before commit.

**Self-check:**

```bash
diff <(grep "^\[200\]" baseline.log | sort -u) \
     <(grep "^\[200\]" post.log | sort -u)
```

Output should show no deletions, only additions. Deletions mean a substitution regressed a previously-working URL.

This rule exists because during the source audit, broad `sed` prefix substitutions silently concatenated onto more-specific paths (e.g. `/v3/` → `/v3/docs` turned an already-correct `/v3/docs` into `/v3/docsdocs`). The guardrail caught it on the second CI dispatch, not the commit itself. **Assume your Tier 3 pass will have regressions. Verify.**

Full detail: `references/tier3-substitution.md`.

---

## The Verification-First Rule

**DEFAULT to probe-verification before any URL substitution.** Unverified substitutions are how phantom URLs land in public skills. Before every `[old] → [new]` replacement:

1. For GitHub repos: `gh api repos/owner/name` — status must be 200 (repo exists, not archived).
2. For HTTP URLs: `curl -sSI -L --max-time 15 '<new>'` — final status must be 200 (after redirects).
3. For PyPI / npm / crates packages: check the registry API or landing page directly.

If verification fails, **exclude the dead target** via `.lycheeignore` with a commented reason rather than guessing a replacement. An excluded dead link is honest; a substituted wrong link is a time bomb.

Full detail: `references/tier3-substitution.md` § "Verification rules".

---

## Playbooks

Three ready-to-dispatch prompt bundles that call this skill's tiers in the right order.

| Playbook | When to Use | Agents |
|----------|-------------|--------|
| `playbooks/full-audit.md` | Fresh audit, failing CI, no prior work. | 10 parallel subagents + synthesis |
| `playbooks/followup-pass.md` | Errors significantly reduced but residuals remain. | 3 targeted subagents |
| `playbooks/post-merge.md` | PR green, time to resolve pending human-decision items. | 4 parallel subagents |

All three follow the same shape: **pre-flight → parallel dispatch → synthesize → commit/PR/merge → verify**.

---

## References

| File | Content |
|------|---------|
| `references/tier1-config.md` | `.lychee.toml` schema, workflow YAML, accept-code gotchas |
| `references/tier2-intra-repo.md` | Intra-repo path audit, singular/plural directory patterns, frontmatter fixes |
| `references/tier3-substitution.md` | URL substitution rules, the guardrail, sed-safety patterns |
| `references/tier4-exclusions.md` | When to exclude vs substitute, `.lycheeignore` category rubric |
| `references/known-debt-template.md` | The 5-category `KNOWN_LINK_DEBT.md` layout for maintainers |

---

## Examples

- `examples/pr-1-retrospective.md` — the source audit that generated this skill. 1208 → 0 errors, 8 commits, auto-detected Tier 3 regression in commit 5 (`9cbd801`), merged as `93a72fe`.

---

## Scope Discipline

This skill fixes *link health*. It does NOT:

- Standardize SKILL.md schemas across the repo. File schema drift as a separate issue.
- Refactor skill content, examples, or prose. Only touches link URLs and the CI config.
- Modify `.lychee.toml`'s accept list to mask real breakage. Flaky upstream 5xx / timeouts get excluded per-host with rationale, not blanket-accepted.

Scope discipline keeps the PR reviewable and the link-check signal honest.
