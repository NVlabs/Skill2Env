---
name: security-tiers
description: Security tier matrix (T1 critical → T4 public): which controls per tier, which compliance keys map to tiers, override criteria
when_to_use: All archetypes. Read by security-officer for gate selection
applies_to:
  - _default
---

# Security Tiers — reference

Single source of truth for great_cto's security gate model. Read by `security-officer`
when picking the right depth of review, by `senior-dev` when emitting security signals
during implementation, and by `/sec status` when reporting the current posture.

Replaces the previous binary `mandatory | conditional | none` model (v1.0.101 and
earlier). The binary model had three systemic holes:

1. **`library → none` was a supply-chain default** — in 2026 npm/PyPI supply chain
   attacks are the #1 vector; zero gate is never the right answer.
2. **"conditional" read as "off by default"** on archetypes that actually own the
   blast radius (web-service with auth, infra with IAM).
3. **Archetype is a proxy for risk, not risk itself** — a `web-service` handling auth
   for 10M users is more security-critical than a `commerce` demo, but the old model
   said the opposite.

The tier model fixes all three.

---

## The three tiers

| Tier | Runs | Time | Never skipped |
|---|---|---|---|
| **`baseline`** | CVE scan (deps) + secret scan (commits + env) + dependency-freshness check | ~2 min | ✓ always, every pipeline |
| **`standard`** | `baseline` + STRIDE threat model + OWASP checklist + compliance map (from PROJECT.md) + data-flow sketch | ~15–25 min | ✓ unless explicit waiver with owner + expiry |
| **`deep`** | `standard` + penetration-style review (injection, IDOR, SSRF, XSS, auth bypass) + external dependency deep-audit + formal data-flow diagram + kill-chain analysis | ~45–90 min | ✓ never skipped on deep-tier archetypes |

`baseline` is the floor. **There is no "off".** A library with zero dependencies and
no network surface still gets CVE + secret scan — it's 2 minutes and closes the
supply-chain default.

---

## Archetype → default tier

Default tier if no signals fire and no override in PROJECT.md:

| Archetype | Default | Why |
|---|---|---|
| `web3` | **deep** | on-chain immutable; funds at stake |
| `iot-embedded` | **deep** | no post-ship patches; physical safety |
| `regulated` | **deep** | compliance by definition (GxP, financial services, ISO 27001) |
| `ai-system` | **standard** → `deep` on MCP/tool-use/external data ingestion | prompt injection, data leakage, but toy-RAG doesn't need full pen-test |
| `commerce` | **standard** → `deep` on PCI-relevant dep | payments/SaaS; PCI only if actually processing PAN |
| `infra` | **standard** | owns IAM + network perimeter + secrets |
| `data-platform` | **baseline** → `standard` on PII/PHI signals | varies enormously |
| `web-service` | **baseline** → `standard` on auth/crypto signals | varies enormously |
| `mobile-app` | **baseline** → `standard` on payment/biometric signals | |
| `library` | **baseline** | CVE + secret scan is always worth 2 min |

**Override in PROJECT.md** (use sparingly, always with reason):

```
## Security

default-tier: standard           # override default from archetype
tier-override-reason: "internal service but handles auth tokens for 10M users"
```

---

## Signal-driven upgrades

These fire automatically during `senior-dev` implementation. Each signal emits a
`SECURITY_SIGNAL: <name> <path>` line to the session log; `security-officer`
parses these and upgrades the tier for this pipeline run.

| Signal | Detection | Upgrade to |
|---|---|---|
| `pci-dep-introduced` | `package.json` / `requirements.txt` / `Cargo.toml` diff adds `stripe`, `plaid`, `square`, `braintree`, `adyen`, `checkout-com` | `standard` (with PCI-DSS compliance pack) |
| `crypto-dep-introduced` | diff adds `jose`, `jsonwebtoken`, `bcrypt`, `argon2`, `scrypt`, `tweetnacl`, `libsodium`, `openssl` bindings | `standard` |
| `auth-path-changed` | git diff path matches `auth/**`, `middleware/auth*`, `iam/**`, `oauth/**`, `saml/**`, `passport/**` | `standard` |
| `pii-field-added` | SQL/ORM migration adds a column matching `ssn`, `sin`, `dob`, `date_of_birth`, `passport`, `phone_number`, `email`, `medical_*`, `health_*` | `standard` (+ privacy-by-design review) |
| `iac-perimeter-changed` | Terraform/Pulumi/CDK diff touches `aws_security_group`, `aws_iam_*`, `google_iam_*`, `azurerm_role*`, public S3/GCS buckets | `standard` |
| `secret-in-diff` | pre-commit secret scan hits a new file | **block** (tier irrelevant — block the commit) |
| `high-cve-in-dep` | `npm audit` / `pip-audit` / `cargo audit` reports ≥ High CVE on a direct dep | `standard` (+ block until CVE addressed) |
| `external-ingest-added` | new HTTP client pointed at a non-allowlisted domain | `standard` |

**Order of precedence:** explicit `tier-override` in PROJECT.md > archetype default > signals. Signals can only **upgrade** the tier, never downgrade it. A `web3` project stays at `deep` even if no signals fire this run.

### Allowlists

`.great_cto/security-allowlist.yml` — optional, project-level. Lets teams suppress
a signal when the reason is documented:

```yaml
allowed-deps:
  - name: jsonwebtoken
    reason: used only for internal session tokens, not user auth
    approved-by: "@alice"
    expires: 2026-10-01

allowed-iac-paths:
  - terraform/staging/**   # staging perimeter changes don't need deep review
```

Waivers follow the same rules as threat-model waivers: named owner + expiry ≤ 90 days.

---

## What each tier actually produces

**`baseline`** writes:
- One line in the pipeline output: `SEC baseline: 0 CVEs, 0 secrets, 3 deps outdated — OK`
- Appends to `.great_cto/security-baseline.log`
- No artefact file — too cheap to generate one

**`standard`** writes:
- `docs/security/CSO-<slug>.md` — compliance officer report with threat-model summary, OWASP checklist results, compliance framework mapping
- `docs/threat-models/TM-<slug>.md` — STRIDE threat model with mitigations
- If PCI-DSS / HIPAA / etc. compliance fires: separate checklist appendix

**`deep`** writes everything `standard` produces, plus:
- Formal dataflow diagram (Mermaid) with trust boundaries
- Kill-chain analysis: for each high-impact threat, the concrete steps an attacker would take
- External dep deep-audit: supply-chain provenance (git history, maintainer count, last-release recency)
- Pen-test checklist (injection, IDOR, SSRF, XSS, auth bypass, race, time-of-check/use)

---

## Reading the current tier

`/sec status` reports:

```
Security posture — pipeline-<slug>

  Archetype default: web-service → baseline
  Signals fired:
    ✓ pci-dep-introduced  package.json  (stripe@14.12.0 added)
    ✓ auth-path-changed   src/middleware/auth.ts
  Effective tier: standard  (upgraded from baseline by 2 signals)

  Next run of security-officer will use tier=standard.
```

When no signals fire, the tier equals the archetype default. When signals fire,
the effective tier is the max of default and all signal upgrades.

---

## Anti-patterns to refuse

- **"Skip security this time, it's just a hotfix."** Hotfixes **introduce** CVEs more often than features — the fix touches the hot path under time pressure. Baseline still runs; it's 2 min.
- **"We already have SAST in CI, turn great_cto off."** SAST catches static bugs; `standard` tier also runs threat-model and compliance mapping. Different layer. Run both.
- **"Override tier from archetype down."** The model only allows upgrades from signals. Downgrades require a written `tier-override-reason` in PROJECT.md — this is deliberately annoying.
- **"Allowlist everything so CI stays green."** Allowlist entries with no expiry or no owner fail the next `/audit` lint pass (anti-pattern A3, owner+expiry required).
- **"My library has no network — skip baseline."** CVE scan is still valid; transitive deps may have shipping bugs. 2 minutes.

---

## Source artefacts

- This file — tier definitions
- `skills/great_cto/references/secure-sdlc.md` — how security-officer integrates with the rest of the pipeline
- `skills/great_cto/references/sec-metrics.md` — CVE MTTR, dep freshness SLOs
- `agents/security-officer.md` — implementation of tier-aware review
- `agents/senior-dev.md` — emits SECURITY_SIGNAL lines during implementation
- `.great_cto/security-baseline.log` — append-only baseline run log (never fails pipeline)
- `.great_cto/security-allowlist.yml` — optional project-level waivers

---

## Migration from v1.0.101 and earlier

If your PROJECT.md has an older `security-gate: mandatory|conditional|none` field,
it's now ignored. The tier is derived from archetype + signals. To preserve the
old behaviour exactly:

| Old | New equivalent |
|---|---|
| `security-gate: mandatory` | archetype default → `standard` or `deep`; no change needed |
| `security-gate: conditional` | archetype default → `baseline` + signals upgrade as warranted |
| `security-gate: none` | **not supported** — minimum is `baseline`; if the old "none" was intentional, add `default-tier: baseline` explicitly |

Most projects need zero config change — the new defaults are strictly more secure
than the old, without adding review burden where it wasn't needed.
