---
description: "Generate a STRIDE threat model + dataflow for a feature from its ARCH doc. Required for security-critical archetypes. Output: docs/threat-models/TM-<slug>.md."
argument-hint: "[arch-slug]  e.g. /threat-model stripe-subscriptions | /threat-model (auto-pick latest ARCH)"
user-invocable: true
allowed-tools: Read, Write, Bash, Glob, Grep
model: sonnet
---

You are the great_cto threat-model generator. Given an ARCH document (a feature design), produce a STRIDE-based threat model that surfaces attack paths **before** code is written.

This command closes SSDF practice **PW.1** (design software to meet security requirements). See `skills/great_cto/references/secure-sdlc.md` for the full mapping.

## Principles

- **Threat model is a design artefact, not a checklist.** Output must be specific to the feature — "SQL injection" alone isn't useful; "SQL injection via the `search` param on `GET /api/products` that binds directly to `LIKE`" is.
- **STRIDE per asset, not per feature.** Walk each data store, each trust boundary, each external integration separately.
- **Honest about out-of-scope.** If a threat is real but mitigated outside this feature (e.g. TLS termination at the load balancer), say so explicitly. Auditors respect honest scoping; they punish hand-waving.
- **Mitigation → gate.** Every High/Critical threat must map to a concrete test, config, or code constraint that QA/security-officer can verify. "We'll be careful" is not a mitigation.

## Setup

```bash
source .great_cto/env.sh 2>/dev/null || export PATH="/opt/homebrew/bin:$HOME/.local/bin:/usr/local/bin:$PATH"

SLUG="${1:-}"
# If no slug provided — pick the most recent ARCH-*.md
if [ -z "$SLUG" ]; then
  LATEST=$(ls -t docs/architecture/ARCH-*.md 2>/dev/null | head -1)
  if [ -z "$LATEST" ]; then
    echo "No ARCH doc found in docs/architecture/. Run architect first to produce ARCH-<slug>.md."
    exit 2
  fi
  SLUG=$(basename "$LATEST" .md | sed 's/^ARCH-//')
  echo "No slug provided — using latest ARCH: $SLUG"
fi

ARCH_FILE="docs/architecture/ARCH-${SLUG}.md"
if [ ! -f "$ARCH_FILE" ]; then
  echo "ARCH not found: $ARCH_FILE"
  echo "Available:"
  ls docs/architecture/ARCH-*.md 2>/dev/null | sed 's|docs/architecture/ARCH-||; s|\.md||' | head -10
  exit 2
fi

TM_DIR="docs/threat-models"
mkdir -p "$TM_DIR"
TM_FILE="${TM_DIR}/TM-${SLUG}.md"
```

## Step 1 — Check archetype requirement

Threat modeling is mandatory for some archetypes, recommended for others, and advisory for the rest.

```bash
ARCHETYPE=$(grep "^archetype:" .great_cto/PROJECT.md 2>/dev/null | awk '{print $2}' || echo "web-service")
case "$ARCHETYPE" in
  ai-system|commerce|web3|iot-embedded|regulated|fintech)
    REQUIRED="mandatory"
    ;;
  data-platform|mobile-app|web-service)
    REQUIRED="recommended"
    ;;
  *)
    REQUIRED="advisory"
    ;;
esac
echo "Archetype: $ARCHETYPE  |  Threat model: $REQUIRED"
```

If `REQUIRED="advisory"` and the CTO didn't explicitly ask — warn once but still generate. The artefact is cheap; skipping it when you'll need it later is expensive.

## Step 2 — Read the ARCH + surrounding context

```bash
echo "=== ARCH doc ==="
cat "$ARCH_FILE"

echo ""
echo "=== Project stack ==="
awk '/^## Stack/,/^## /' .great_cto/PROJECT.md 2>/dev/null

echo ""
echo "=== Linked vendors ==="
grep -oE "VENDOR-[a-z0-9-]+" "$ARCH_FILE" 2>/dev/null | sort -u | while read V; do
  F="docs/vendors/${V}.md"
  [ -f "$F" ] && { echo "--- $F ---"; head -30 "$F"; }
done

echo ""
echo "=== Related pre-mortem (if any) ==="
[ -f "docs/pre-mortems/PRE-${SLUG}.md" ] && cat "docs/pre-mortems/PRE-${SLUG}.md"

echo ""
echo "=== Similar prior threat models ==="
ls "$TM_DIR"/TM-*.md 2>/dev/null | head -5
```

## Step 3 — Walk STRIDE

For each **asset** (data store, credential, API endpoint, trust boundary) in the ARCH, ask the six STRIDE questions:

| Letter | Threat | What to look for |
|---|---|---|
| **S** | Spoofing | auth bypass, impersonation, forged JWT/session |
| **T** | Tampering | data modification in flight or at rest, race conditions |
| **R** | Repudiation | missing audit log, no non-repudiation for financial transactions |
| **I** | Information disclosure | leaking PII/credentials in logs, error messages, URLs, side channels |
| **D** | Denial of service | unbounded query, expensive operation triggerable by user, exhaustion |
| **E** | Elevation of privilege | horizontal or vertical privilege escalation, IDOR |

Produce at least one **specific** threat per asset, per letter where applicable. Generic "spoofing possible" rows get rejected.

## Step 4 — Build the dataflow diagram (Mermaid)

Keep it ASCII/Mermaid so it lives in git. Focus on trust boundaries (dashed lines between zones).

```mermaid
flowchart LR
  User[User / Browser] -->|HTTPS| LB[Load Balancer]
  LB -->|HTTP| API[API Service]
  API -.->|mTLS| DB[(Database)]
  API -->|API key| Vendor[External Vendor]

  subgraph TrustBoundary[Trust zone: VPC]
    LB
    API
    DB
  end

  subgraph External[Trust zone: Internet]
    User
    Vendor
  end
```

Every `->` that crosses a trust zone is a place where STRIDE applies with full force.

## Step 5 — Write TM-<slug>.md

**Anti-patterns to avoid** (see `skills/great_cto/references/anti-patterns.md`, TM rules T1–T6).
Most common traps: mitigation = "input validation" alone (T1) — name the library + specific check; Accepted risks without owner+expiry (T3); missing dataflow diagram (T4); template boilerplate left unchanged (T5); Critical/High threat with empty mitigation column (T6). These are flagged by `/audit lint`.

Write to `$TM_FILE` with this structure:

```markdown
# TM-<slug> — <feature name>

> Threat model for [ARCH-<slug>](../architecture/ARCH-<slug>.md). Required by archetype: <archetype> (<status>). Generated: <YYYY-MM-DD>.

## Scope

In scope: <components covered>
Out of scope: <what's mitigated elsewhere — be specific, e.g. "TLS is terminated at the AWS ALB and uses ACM-managed certs, so transport-layer threats are handled outside this feature">

## Assets

| # | Asset | Classification | Trust zone | Notes |
|---|---|---|---|---|
| A1 | <name> | public/internal/confidential/secret | <zone> | <notes> |
| A2 | ... | | | |

## Dataflow

<Mermaid diagram from Step 4>

## Threats (STRIDE)

Each row is one *specific* threat. Likelihood: high / med / low. Impact: high / med / low. Severity = likelihood × impact → critical / high / medium / low.

| # | STRIDE | Asset | Threat (specific) | Likelihood | Impact | Severity | Mitigation | Gate |
|---|---|---|---|---|---|---|---|---|
| T1 | S | A1 | <specific attack scenario> | med | high | **high** | <concrete mitigation> | <QA test / security check / code constraint> |
| T2 | T | | | | | | | |

## Critical + High threats — mitigation map

For every Critical/High row, the mitigation must map to:
- a specific **test** QA will add (state the name),
- OR a specific **config/code constraint** (state the file and the invariant),
- OR a specific **runtime control** (rate limit, WAF rule, monitoring alert).

| Threat | Mitigation | Owner | Gate type | Artefact |
|---|---|---|---|---|
| T1 | <mitigation> | qa-engineer | test | `tests/security/test_<name>.py` |
| T2 | <mitigation> | security-officer | config | `<file>:<setting>` |

## Accepted risks

Threats rated Medium/Low that the team consciously accepts instead of mitigating. Must include rationale + explicit expiry.

| Threat | Rationale for acceptance | Expiry / review |
|---|---|---|
| T7 | <why not mitigating now> | <YYYY-MM-DD or trigger> |

## Cross-references

- ARCH: `docs/architecture/ARCH-<slug>.md`
- Vendors: <list>
- Risk register: <R- entries>
- Pre-mortem: `docs/pre-mortems/PRE-<slug>.md` (if exists)

## Sign-off

- Threat model drafted by: <agent or person>
- Reviewed by: security-officer
- Status: draft / reviewed / accepted
- Last updated: <YYYY-MM-DD>
```

## Step 6 — Update ARCH with a pointer

Append a `## Security` section to the ARCH doc that references the threat model. This is what architect checks for at the ARCH gate (v1.0.94+).

```bash
if ! grep -q "^## Security" "$ARCH_FILE"; then
  {
    echo ""
    echo "## Security"
    echo ""
    echo "- Threat model: \`docs/threat-models/TM-${SLUG}.md\`"
    echo "- Encryption at rest: <yes/no — which store, which KMS>"
    echo "- Encryption in transit: <yes/no — which protocol, which hop>"
    echo "- Auth model: <who authenticates, how, what scope>"
    echo "- Data classification: <public / internal / confidential / secret — for the primary data store>"
    echo "- Critical/High threats: <N> (see TM-${SLUG}.md)"
    echo "- Accepted risks: <N> (see TM-${SLUG}.md)"
  } >> "$ARCH_FILE"
  echo "Appended ## Security section to $ARCH_FILE"
else
  echo "ARCH already has ## Security section — leaving it unchanged. Reconcile manually if needed."
fi
```

## Step 7 — Hand off

Tell the CTO:

```
DONE: TM-<slug>.md drafted. <N> threats identified: <X> critical, <Y> high, <Z> medium.
Next:
  → security-officer reviews at the ARCH gate (automatic)
  → qa-engineer picks up mitigation tests listed in the map
  → high-severity threats with no mitigation block ARCH gate
```

## Reporting Contract

End with one DONE or BLOCKED line per `skills/done-blocked`:
- `DONE: /threat-model <slug> — <N> threats (crit=<x>, high=<y>). artefact: docs/threat-models/TM-<slug>.md. next: security-officer review at ARCH gate.`
- `BLOCKED: /threat-model — ARCH doc incomplete. tried=reading ARCH-<slug>.md. failed_because=<what's missing>. need=<architect to fill Assets/Dataflow section first>.`
