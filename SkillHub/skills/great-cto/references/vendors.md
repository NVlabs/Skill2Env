---
name: vendors
description: Third-party vendor register: Stripe, Auth0, OpenAI, AWS regions, Datadog — fallback plans when vendor X has outage
when_to_use: Vendor introduction time + ARCH review. Read by architect
applies_to:
  - _default
---

# Vendor register — Reference

> Systematic tracking of **third-party services** (not libraries). Stripe, Auth0, OpenAI, Twilio, AWS regions, Datadog. When vendor X has an outage, the fallback plan is found in 30 seconds — not improvised in a panic.

## Scope

| In scope | Out of scope |
|----------|--------------|
| Paid SaaS services (APIs, hosted platforms) | npm/pip packages — those are deprecations.md |
| Cloud regions with distinct SLAs | OS-level libraries |
| Critical free-tier services (e.g. GitHub Actions) | Internal services |

**Criticality gate** — only create VENDOR-*.md for vendors with `criticality: critical` or `high`. Skip low-tier utilities to avoid register fatigue.

## File

`docs/vendors/VENDOR-<slug>.md` — one file per vendor. Slug is the vendor name lowercased.

## Schema

```markdown
# VENDOR-<slug>

## Role
<What this vendor does for us — 1-2 sentences.>

## Criticality
<critical | high | medium | low>

- **critical**: outage halts core product (payments, auth)
- **high**: outage degrades major feature (AI, notifications)
- **medium**: outage causes user friction (analytics, search)
- **low**: outage invisible to users (logging, monitoring)

## DORA classification (EU Digital Operational Resilience Act)

> Required for financial-sector entities subject to DORA (Reg. 2022/2554, Art. 28). Optional otherwise — if you're not in-scope for DORA, write "n/a" in the fields below but keep the section so a future audit can find it.

- **ICT-3P register entry**: <yes / no / n/a>
- **Supports critical or important function**: <yes / no / n/a>
  (DORA Art. 28 requires exit strategy + enhanced monitoring if yes)
- **Data shared**: <categories — e.g. "customer PII, payment card, transaction logs" / "none">
- **Data location**: <region(s) — e.g. "eu-west-1, eu-central-1">
- **Sub-processors**: <list names + URL of subprocessor page, or "none declared">
- **Concentration risk**: <low / medium / high — are multiple critical functions dependent on this one vendor?>

## Exit strategy

> Concrete plan for migrating away from this vendor. For `critical` vendors (and DORA "critical or important function" vendors) this must not be blank.

- **Trigger** (what would force a migration): <acquisition / security incident / SLA breach / pricing change>
- **Migration path**: <step-by-step, at least first 3 steps>
- **Alternative vendor(s)**: <name + rough switch cost>
- **Estimated migration time**: <days / weeks / months>
- **Data portability**: <what format can we export? is it fully structured?>
- **Tested**: <yes — last tested <YYYY-MM-DD> / no — theoretical only>

## SLA
- Commitment: <X.XX%> uptime per vendor public SLA
- Our dependency tier: <tier-reason>
- Status page: <URL>

## Incident history (last 12 months)
- <YYYY-MM-DD>: <description> — impact on us: <Nmin / Nh / none>
- ...
Source: <vendor status page URL>

## Fallback plan
- <Primary fallback>: <concrete action, who executes, how long>
- <Secondary fallback>: <last resort>
- Manual override: <emergency action, if any>

## Compliance certs (if applicable)
- <cert name>: valid until <YYYY-MM>
- ...

## Contract
- Renewal: <annual | monthly | usage-based; auto-renew date>
- Pricing tier: <tier and unit cost>
- Volume commitment: <none | $X/month>
- Key contract clauses: <data residency, termination, etc.>

## Risks (linked to register)
- R-NNN: <linked risk title>

## Last reviewed: <YYYY-MM-DD> (<who — usually security-officer>)
```

## Review cadence

- **Quarterly** (by security-officer): check incident history, cert expirations, renewal dates, risk linkage, DORA classification accuracy, exit strategy freshness (must be re-verified if not tested in > 12 months)
- **On-demand** when vendor has a public incident → append to incident history
- **At ARCH time** (by architect): when a new vendor is introduced → VENDOR doc created before ARCH merges

## Triggers — when to add a vendor

| Trigger | Who | Timing |
|---------|-----|--------|
| New external SDK/API adopted in ARCH | architect | before ARCH finalized |
| `/audit` detects vendor SDK in deps with no VENDOR-*.md | auto-suggest | advisory |
| Vendor cert approaching expiry (< 90d) | security-officer | via `/digest` |
| Vendor incident > 30min impacting us | l3-support | append to incident history |
| Cost/scale threshold crossed (e.g. > $1k/month) | architect or CTO | promote to `critical` if not already |

## Integration

- **architect (ARCH-time)**: for every external service referenced in ARCH, check `docs/vendors/VENDOR-<slug>.md` exists. If not → prompt CTO "New vendor <name>. Criticality? Create VENDOR doc?" Skip for `low` criticality.
- **security-officer (quarterly, via `/digest`)**: iterate all `VENDOR-*.md` at `critical` or `high`, verify cert validity, check renewal dates within 90 days, cross-reference incident history with risk register.
- **`/audit`**: scan `package.json` / `requirements.txt` / env vars for known vendor SDKs (stripe, auth0, openai, twilio, sendgrid, aws-sdk, etc.) → list any without matching VENDOR doc as advisory findings.

## Risk-register coupling

Any `critical` vendor gets at least one risk-register entry by default — the implicit "vendor outage" risk. If the fallback plan is solid, the risk can be `accepted`. If no fallback exists for a critical vendor, the risk must be `mitigating` or `planned`, not `accepted`.

## Consumers

- `architect` — checks at ARCH; adds vendor at decision time
- `security-officer` — quarterly review, cert monitoring
- `/audit` — detects vendors in deps without VENDOR docs
- `/digest` — renewal / cert expiry reminders
- l3-support — reads fallback plan during vendor-caused incidents
- Risk register — sink for vendor-related risks

## Not in scope (deliberately)

- Vendor price negotiation — that's procurement, not engineering record
- Vendor feature requests — belongs in backlog
- Complete cost accounting — see cost attribution (v1.0.74)
