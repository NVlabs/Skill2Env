# Playbook — Full audit (10-agent dispatch)

Use when: a repo's `Check Links` workflow is failing with a large error count (hundreds+), no prior link-health work has been done, and you want a complete audit + fix cycle.

## Shape

```
pre-flight  →  10 parallel subagents  →  master report  →  4-tier APPLY  →  CI dispatch  →  post-dispatch cleanup if residuals
```

## Pre-flight (sequential, fail fast)

1. Verify tools: `gh auth status`, `git --version`, `node --version`, `lychee --version` (install if needed — falls back to `markdown-link-check` via `npx` if lychee not installable).
2. Verify network egress to `github.com` and `raw.githubusercontent.com`.
3. Create scratch dir: `~/work/<repo>-audit-$(date +%Y%m%d-%H%M)`.
4. Clone: `gh repo clone <owner/repo>` (full clone, not shallow — need the full markdown tree).
5. Log current default branch, latest commit SHA, last CI run status via `gh run list --limit 5`.
6. Grab the latest failing `Check Links` run log: `gh run view <id> --log-failed > audit/baseline.log`. Parse the summary block for total / successful / errors counts.

## Parallel agent dispatch (10 subagents, single message)

Each agent gets a self-contained prompt with the repo path, the baseline log path, and the specific deliverable filename under `audit/`.

| Agent | Name | Responsibility |
|-------|------|----------------|
| agent-1 | `lychee-config` | Draft corrected `.lychee.toml` + rationale. Confirm no existing config. |
| agent-2 | `broken-file-refs` | Classify every `[ERROR] file://` entry as PATH_TYPO / WRONG_PATH / MISSING_FILE. Per-file fix table. |
| agent-3 | `<worst-skill>-deep-dive` | Deep dive on the worst-affected skill (usually one concentrates the bulk of intra-repo breakage). Directory restructure plan. |
| agent-4 | `genuine-404s` | For every unique 404 URL, WebFetch to categorize DEAD_PERMANENT / MOVED / TRANSIENT / PLACEHOLDER. Replacement URL table. |
| agent-5 | `network-ssl-issues` | For every `[ERROR] network` / `[TIMEOUT]`, probe from this box with curl. Categorize DEAD_INFRA / SSL_EXPIRED / TRANSIENT_CI / RATE_LIMITED. |
| agent-6 | `doi-redirects` | Confirm publisher 403 redirects (BMJ, Oxford, Sage, OECD, Ensembl) are fixable via config alone. No URL changes. |
| agent-7 | `skill-md-structural` | Spot-check 20 random `SKILL.md` files against the canonical frontmatter schema. Drive-by integrity pass. |
| agent-8 | `ci-pipeline` | Inspect `.github/workflows/`. Draft hardened `check-links.yml`. Web-check current `actions/checkout` and `lychee-action` majors. |
| agent-9 | `badges-and-shields` | Confirm badge / shield URLs are false positives. Draft `.lycheeignore` badge block. |
| agent-10 | `prioritization-and-pr-plan` | **Sequential; depends on 1-9.** Synthesize 4-tier plan + PR title/body + consolidated human-decision list. |

**Dispatch 1-9 in parallel** (single message with 9 Agent tool calls). Then dispatch agent-10 after 1-9 complete.

Each agent's prompt must include:
- Absolute repo path.
- Absolute baseline log path.
- Output file path (`audit/agent-N.md`).
- "No commits, no pushes. Write only to `audit/`."
- Concrete budgets for web-probing agents (e.g. "up to 60 URLs max").

## Synthesize

After all 10 reports land:
- Write `audit/MASTER_REPORT.md` — executive summary pointing to agent-10.
- Write `audit/diff-preview.txt` — concrete file changes per tier.
- **Pause for human review** before APPLY. Present the consolidated human-decision list.

## APPLY (4 tiered commits on `fix/link-health-audit`)

Per `references/tier1-config.md` through `references/tier4-exclusions.md`. Each tier = one commit. See `examples/pr-1-retrospective.md` for real commit boundaries.

After all four commits: push, `gh pr create`, trigger `workflow_dispatch` on the branch, link the run in a PR comment.

## Post-dispatch

Run the guardrail diff (`references/tier3-substitution.md`). If residuals:
- **Regressions** (previously-200 URLs now failing) — revert the matching substitutions via a fix-up commit.
- **New residuals** (URLs that were also broken in baseline, still broken now) — cleanup-pass via `playbooks/followup-pass.md`, or additional `.lycheeignore` entries.

When errors hit 0 (or the agreed residual target), the PR is ready to merge.

## Expected timeline

- Pre-flight: ~2 min
- 9 parallel agents: 3-6 min total (slowest one gates)
- Agent-10 synthesis: ~2-3 min
- User review: human-paced
- APPLY 4 commits: 5-10 min
- First dispatch + analysis: ~3 min
- Post-dispatch cleanup: 1-3 additional fix-up commits, 5-10 min per dispatch cycle

Total assistant time: 30-60 minutes from cold start to PR green.
