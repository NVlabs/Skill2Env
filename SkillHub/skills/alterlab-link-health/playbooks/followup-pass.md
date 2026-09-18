# Playbook — Follow-up pass (3-agent targeted residual)

Use when: the initial APPLY phase reduced errors significantly (e.g. 1208 → 67) but some residuals remain. Typical residuals cluster into three independent classes, each suited to its own subagent.

## Shape

```
fetch latest CI run  →  classify residuals  →  3 parallel subagents  →  single fix-up commit  →  redispatch  →  verify
```

## Fetch and classify

Pull the latest failing run's log:

```bash
gh run view <id> --log-failed > audit/after1.log
grep -E '\[ERROR\]|\[40[0-9]\]|\[5[0-9][0-9]\]|\[TIMEOUT\]' audit/after1.log \
  | sort -u > audit/residuals.txt
```

Classify each residual into one of three buckets:

| Class | Examples | Typical cause |
|-------|----------|----------------|
| **Substitution regressions** | `/v3/docsdocs`, `/api/swagger-ui/index.htmlswagger-ui/...`, over-greedy prefix rewrites | Tier 3 sed bugs — concatenation, double-append, chain-substitution overreach. |
| **Genuinely dead / flaky infra** | Upstream docs sites that 404'd a page, hosts with consistent CI-side failures, SSL/OCSP issues | Need either a better substitute (verify!) or an exclusion with rationale. |
| **Config-fixable** | GraphQL endpoints returning 400, hosts that need a specific status in `accept` | Add the status to `.lychee.toml`'s `accept` array with a comment. |

## Parallel agent dispatch (3 subagents)

| Agent | Name | Responsibility |
|-------|------|----------------|
| **agent-R** | `regression-repair` | For each substitution-regression URL: grep the repo to find the broken pattern, write a targeted corrective sed (narrow scope — don't re-use the broad Tier 3 rules). Verify each repair with curl. Produce the fix-up commit content for these files. |
| **agent-D** | `dead-infra-triage` | For each dead/flaky URL: probe from this box (curl with reasonable timeout) to confirm the host state. Choose exclude-with-rationale vs. find-a-real-substitute. Verify substitutes before proposing them. Output `.lycheeignore` additions + any URL rewrites. |
| **agent-C** | `config-tuning` | Identify config-fixable residuals. Propose `accept = [...]` additions or `max_retries` bumps. Keep additions narrow — never blanket-accept 5xx. |

All three write their output to `audit/followup-<name>.md` and do not commit.

## Synthesize into one commit

Single commit with message describing all three classes:

```
fix(links): repair Tier 3 regressions + broaden exclude list

<paragraph describing the regression bugs>
<paragraph describing the dead-infra exclusions>
<paragraph describing the config tuning>
```

Why one commit: reviewers can see the full cleanup logic in one place, and the guardrail diff (baseline-vs-post-this-commit) shows one net effect.

## Re-dispatch + verify

After pushing the fix-up:

1. `gh workflow run check-links.yml --ref <branch>`.
2. Wait for completion via a polling monitor.
3. Run the Tier 3 guardrail diff once more. Any residual that's a regression goes back through agent-R. Any new dead-infra gets agent-D.

## Stopping criteria

Stop when one of:

- Errors = 0 (ideal).
- Errors = N (small, single-digit) and every residual has a rationale comment in `.lycheeignore` / `KNOWN_LINK_DEBT.md`.
- Consecutive dispatches show different residuals each time — that's CI flake, and the config should be tuned (bump retries) rather than pursuing individual URLs.
