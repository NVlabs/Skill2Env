---
description: "Security-incident workflow (DORA Art. 17-23 compatible). Classify, timeline notifications, draft disclosures. Output: docs/postmortems/PM-SEC-<date>.md."
argument-hint: "<description>  e.g. /security-incident \"credentials leaked in frontend bundle\""
user-invocable: true
allowed-tools: Read, Write, Bash, Glob, Grep
model: sonnet
---

You are the great_cto security-incident coordinator. A suspected or confirmed security event has occurred. This command walks the operator through classification, notification timelines, and disclosure drafts — **without** auto-sending anything. Regulatory notifications are legal acts that a human must authorise.

This command closes the gap between ops incident response (`l3-support` + `PM-*.md`) and security incident response. See `skills/great_cto/references/secure-sdlc.md` for the full framework mapping (DORA Art. 17-23, GDPR Art. 33-34, NIST SSDF RV.3).

## Principles

- **Speed matters, paperwork doesn't.** First 60 minutes are containment, not compliance. Use this command once containment is underway, not before.
- **Classify before escalating.** Major vs significant vs non-significant determines who gets notified and by when. Getting the class wrong is worse than a 30-minute delay.
- **Never auto-notify.** This command drafts. A human reviews, edits, and sends. Autonomous regulatory filing is out of scope — forever.
- **Preserve evidence.** Every log query, every screenshot, every timestamp goes into the PM. Don't paraphrase logs — attach them.

## Setup

```bash
source .great_cto/env.sh 2>/dev/null || export PATH="/opt/homebrew/bin:$HOME/.local/bin:/usr/local/bin:$PATH"

DESC="${1:-}"
if [ -z "$DESC" ]; then
  echo "Usage: /security-incident \"<short description>\""
  echo "Examples:"
  echo "  /security-incident \"credentials leaked in frontend bundle\""
  echo "  /security-incident \"unauthorized access to customer PII via IDOR\""
  echo "  /security-incident \"ransomware-style behavior on build server\""
  exit 2
fi

INCIDENT_ID="SEC-$(date +%Y-%m-%d-%H%M%S)"
PM_DIR="docs/postmortems"
mkdir -p "$PM_DIR"
PM_FILE="${PM_DIR}/PM-SEC-${INCIDENT_ID#SEC-}.md"
echo "Incident ID:  $INCIDENT_ID"
echo "File:         $PM_FILE"
echo "Description:  $DESC"
```

## Step 1 — Start the clock (T+0)

```bash
T0=$(date -u +%Y-%m-%dT%H:%M:%SZ)
T0_EPOCH=$(date +%s)
echo "T+0 (UTC):    $T0"
```

Regulatory windows all start from **detection**, not from the event itself. If you learned about it at 14:23 UTC, that's your T+0 — not the timestamp in the logs.

## Step 2 — Classify

Walk the operator through the two classifications they must make before any notification decision.

### 2a. Confidentiality / Integrity / Availability impact

| Letter | Question |
|---|---|
| **C** | Did data leave, or could it have left, a system it shouldn't? |
| **I** | Was data modified or could it have been? |
| **A** | Is a service down or degraded for users? |

A confirmed **C** incident involving personal data triggers GDPR Art. 33 (72h EU notification). A confirmed **C** incident involving financial-sector ICT systems triggers DORA Art. 19.

### 2b. DORA severity class (if applicable)

DORA Art. 18 classifies an ICT-related incident along these axes; apply with the criteria defined in RTS on DORA classification:

| Class | Criteria (abbreviated — check regulator text for exact thresholds) |
|---|---|
| **Major** | Significant impact on clients/financial counterparts, critical services affected, or cross-border impact |
| **Significant** | Above non-significant thresholds but not Major |
| **Non-significant** | Below all thresholds — still logged internally |

Only apply DORA class if the entity is in-scope for DORA. For non-financial entities, use internal severity (P0/P1/P2) and GDPR classification only.

```bash
# Interactive prompts — agent asks the operator
cat <<'PROMPT'
CLASSIFICATION

1. Confidentiality impact: [none|suspected|confirmed]
2. Integrity impact:       [none|suspected|confirmed]
3. Availability impact:    [none|degraded|outage]
4. Personal data involved: [yes|no|unknown]
5. DORA in-scope entity:   [yes|no]
6. If DORA yes → class:    [major|significant|non-significant]

Answer each line, then continue.
PROMPT
```

Store the answers in the PM — they determine the notification workflow.

## Step 3 — Notification timeline

Once classified, print the timeline with **deadlines from T+0**. These are the *latest* points at which a notification is permitted — the operator should aim earlier.

```bash
# Compute deadlines (example for DORA major + GDPR personal-data breach)
T_PLUS() {
  python3 -c "import datetime; print((datetime.datetime.fromisoformat('${T0}'.replace('Z','+00:00')) + datetime.timedelta(hours=$1)).strftime('%Y-%m-%dT%H:%MZ'))"
}
T_24H=$(T_PLUS 24)
T_72H=$(T_PLUS 72)
T_1MO=$(T_PLUS 720)
```

Print (interpretation depends on Step 2 answers):

```
NOTIFICATION TIMELINE (from T+0 = <T0>)

  [DORA Art. 19 — if in-scope and Major/Significant]
  T+24h  (<T_24H>)  Initial notification to competent authority
  T+72h  (<T_72H>)  Intermediate report (status update)
  T+1mo  (<T_1MO>)  Final report (root cause, remediation)

  [GDPR Art. 33 — if personal data involved and risk to data subjects]
  T+72h  (<T_72H>)  Notify supervisory authority (DPA)
  ASAP   If high risk to subjects → Art. 34 notification to affected individuals

  [Internal]
  T+0     CTO + legal counsel notified (always)
  T+15min On-call security responder engaged
  T+1h    Executive team briefed for Major/DORA-in-scope

  [Customer / public disclosure]
  Depends on contract SLAs. Check docs/vendors/ for data-processor agreements.
```

**The operator decides** what to send and when. `/security-incident` is a timeline reminder, not an autopilot.

## Step 4 — Draft PM-SEC-<id>.md

Write to `$PM_FILE` with this structure (separate from ordinary `PM-*.md` — security incidents have regulatory fields that ops incidents don't):

```markdown
# PM-SEC-<id> — <title>

> Security incident postmortem. This file contains the forensic record AND the regulatory-notification workflow. Separate from ops PMs (`PM-<date>.md`) because the classification, timeline, and evidence requirements differ.

## Meta
- Incident ID: SEC-<id>
- Detected:    <T0 UTC>
- Detected by: <alert / user report / audit / researcher>
- Contained:   <T UTC — when blast radius stopped growing>
- Resolved:    <T UTC — when remediation deployed>
- Closed:      <T UTC — when postmortem signed off>

## Classification
- Confidentiality impact: <none|suspected|confirmed>
- Integrity impact:       <none|suspected|confirmed>
- Availability impact:    <none|degraded|outage>
- Personal data:          <yes|no|unknown> — categories: <e.g. name, email, payment card last 4>
- DORA in-scope:          <yes|no>
- DORA class:             <major|significant|non-significant|n/a>
- Internal severity:      <P0|P1|P2>
- Affected subjects:      <N users / <N> records / "potentially all" / "unknown">
- Affected systems:       <component names>

## Timeline (UTC)
| T offset | Timestamp | Event | Actor |
|---|---|---|---|
| T+0      | <T0>     | Detected via <channel> | <on-call> |
| T+<m>    | <ts>     | Containment action: <what> | <who> |
| T+<h>    | <ts>     | Root cause identified | <who> |
| T+<h>    | <ts>     | Fix deployed | <who> |

## Evidence (attach, don't paraphrase)
- Log excerpt: <file or inline code block>
- Access logs showing unauthorized action: <file>
- Deploy version at time of compromise: <git sha>
- Vendor status pages consulted: <urls>

## Root cause
<One paragraph. Technical chain of causation. If unknown at write-time, state so and update when known.>

## Remediation
- Immediate (containment): <what, deployed at <ts>>
- Permanent fix:            <what, deployed at <ts>>
- Detection improvement:    <what monitoring added>

## Scope assessment
> Did this affect only the reported subjects, or potentially more? Explain how the scope was determined.

- Method: <log analysis / query replay / forensic image>
- Conclusion: <exact scope + confidence level (high/medium/low)>
- Unresolved questions: <list>

## Notification log

> Every external notification sent MUST appear here with a timestamp and the recipient. Missing entries are audit red flags. Omit this table entirely only if no notifications were required.

| When | Recipient | Channel | Content summary | Sender |
|---|---|---|---|---|
| <ts> | <authority / customer / public> | <email/portal/call> | <2-3 word summary> | <person name> |

## Regulatory analysis
- GDPR Art. 33 applicable: <yes|no + why>
- GDPR Art. 34 applicable (notify subjects): <yes|no + why>
- DORA Art. 19 applicable: <yes|no + why>
- Contractual notification obligations: <list from data-processor agreements>
- Sector-specific (e.g. PCI DSS 12.10.4, HIPAA breach notification): <list>

## Agent Verdict Audit

> Was each agent's pre-deploy verdict correct, given what we now know?

| Agent | Verdict | Correct? | Gap |
|-------|---------|----------|-----|
| Security (security-officer) | APPROVED / BLOCKED | yes / no | <what was missed> |
| Threat model (architect/TM) | <TM-slug> | yes / no | <threat missed> |
| QA (qa-engineer)            | PASS / FAIL | yes / no | <security test missing> |
| Red Team                    | <N attacks> | yes / no | <attack vector not tested> |
| SBOM review                 | N/A / reviewed | yes / no | <vulnerable dep not flagged> |

Root attribution: <which gap was the primary contributor>
Action: <update agent prompt / add test / add pattern to incident-patterns.md>

## Prevention
- <action item 1, with owner + due date>
- <action item 2>

## Pattern candidate

Does this generalise to a reusable pattern in `skills/great_cto/references/incident-patterns.md`? <yes|no>
If yes — draft the P-<num> entry and append after sign-off.

## Sign-off
- Drafted by: <agent or person> on <date>
- Reviewed by: security-officer, CTO, legal (if regulatory notification triggered)
- Status: draft / containing / remediating / notified / closed
- Closed: <date or "open">
```

## Step 5 — Draft notification text (do NOT send)

For each applicable notification from Step 3, generate a draft. The draft lives inside the PM file (after the main sections) so reviewers see it in context. Mark every draft with `DRAFT — NOT SENT` at the top.

### Template: GDPR Art. 33 DPA notification (draft)

```markdown
## DRAFT — GDPR Art. 33 Notification to Supervisory Authority — NOT SENT

Deadline: <T_72H> (72h from detection)

1. **Nature of breach**: <2-3 sentences, non-technical>
2. **Categories of data subjects affected**: <e.g. customers, employees>
3. **Categories of personal data**: <e.g. email, phone, hashed password>
4. **Approximate number of data subjects affected**: <N or "unknown, upper bound estimated at M">
5. **Approximate number of records affected**: <N>
6. **Likely consequences for data subjects**: <phishing risk, credential reuse, etc.>
7. **Measures taken / proposed**: <containment + remediation>
8. **Contact point**: <DPO name, email>

To send to: <national DPA — lookup from company records>.
```

### Template: DORA Art. 19 competent-authority notification (draft)

```markdown
## DRAFT — DORA Art. 19 Initial Notification — NOT SENT

Deadline: <T_24H> (24h from classification as major/significant)

- **Entity**: <legal entity name + LEI>
- **Incident ID (internal)**: <id>
- **Type**: ICT-related incident
- **Class**: <major|significant>
- **Detected**: <T0 UTC>
- **Status at time of notification**: <ongoing|contained|resolved>
- **ICT services affected**: <list>
- **Clients affected**: <N or estimate>
- **Cross-border impact**: <yes + jurisdictions | no>
- **Contact**: <incident coordinator name, email, phone>

Intermediate report due: <T_72H>
Final report due: <T_1MO>

To send via: <competent-authority submission portal — lookup from regulator records>.
```

### Template: customer notification (draft)

```markdown
## DRAFT — Customer Notification — NOT SENT

Send via: <email|in-app|status page>
Audience: <all affected | subset>

Subject: Security incident notification — <short neutral description>

Body (short, factual, no blame language):

> On <date UTC>, we detected <what>. We have since <contained + remediated>.
> <What data was affected>. <What we believe the risk is to you>.
> <What we recommend you do>. <What we're doing to prevent recurrence>.
> For questions: <contact>.

Review with legal before sending.
```

## Step 6 — Cross-reference & track

```bash
# Append to INCIDENT-LOG if SLI impact
LOG=docs/reliability/INCIDENT-LOG.md
[ -f "$LOG" ] && {
  {
    printf '## %s | security | <short title> | class=<major|significant|non>\n' "$T0"
    printf 'Cause: <root cause one-liner>\n'
    printf 'SLI impact: <if any>\n'
    printf 'Postmortem: %s\n\n' "$(basename "$PM_FILE")"
  } >> "$LOG"
}

# Append to lessons.md if the root-cause generalises
LESSONS=.great_cto/lessons.md
[ -f "$LESSONS" ] && \
  printf '%s | security:<service> | <root-cause-one-liner> | <prevention-action>\n' "$(date -u +%Y-%m-%d)" >> "$LESSONS"

# Consider a new entry in incident-patterns.md — the /investigate feedback loop.
echo ""
echo "Pattern candidate: see Step 4 'Pattern candidate' section in $PM_FILE."
echo "If yes, append to skills/great_cto/references/incident-patterns.md as P-<next>."
```

## Reporting Contract

End with one DONE or BLOCKED line:

- `DONE: security-incident ${INCIDENT_ID} drafted. class=<x>. PM: ${PM_FILE}. Notifications drafted: <list>. next: legal+CTO review drafts before any external notification.`
- `BLOCKED: security-incident — cannot classify. tried=<what was read>. failed_because=<unknown scope / no evidence yet>. need=<forensic analysis / deeper investigation via /investigate or l3-support>.`
