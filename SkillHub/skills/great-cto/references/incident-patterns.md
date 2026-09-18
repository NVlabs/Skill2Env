---
name: incident-patterns
description: Library of recurring production incidents: thundering herd, cache stampede, retry-storm, cascading failure, hot-partition, cold-start spike
when_to_use: Incident triage. Read by l3-support during P0/P1 response and pattern lookup at ARCH time
applies_to:
  - _default
---

# Incident pattern library

A curated library of recurring production failure patterns. `l3-support` appends to this file after every postmortem where the root cause generalises beyond the specific service. `/investigate` reads it to propose hypotheses for new alerts.

## Why this file exists

The AI-SRE pattern (Gouthamve, 2024) ships with one observation: an investigation agent is useless on day one and invaluable after five incidents — because pattern recognition compounds. The knowledge base, not the model, is the moat.

This file is that knowledge base for great_cto. It is **not** documentation of how things should work — it is a log of how things have actually broken, what the tell was, and what fixed it.

## Format

Each pattern is one H3 section:

```markdown
### P-<number> — <one-line pattern name>

**Tell**  — the symptom a human or agent would see first (log line, metric shape, user complaint).
**Hypothesis** — the mechanism, in one sentence.
**Confirm with** — the cheapest diagnostic that proves or disproves it (under 30 seconds).
**Fix** — what actually resolves it (link to PR / commit / runbook).
**Seen in** — PM-<date> (so the agent can cross-reference the full write-up).
**Applies to** — which stacks/archetypes this is relevant to (e.g. "any service behind an HPA"; "anything talking to S3 over IPv6"). Empty = universal.
```

Patterns are append-only. Never rewrite an entry — add a new one if the understanding evolves.

## Adding a pattern (for l3-support)

After writing a PM, ask yourself: **"If this happens again on a different service, would the PM help me?"** If yes — extract the pattern here. If no (it's a one-off bug in specific business logic) — skip.

Good candidates:
- Infrastructure-level failures (connection pools, DNS, certs, IPv6, proxy quirks)
- Framework-level footguns (ORM N+1 under specific loads, async-context loss)
- Deploy/rollout issues (HPA thrashing, config drift, cold-cache stampede)
- Third-party failure modes (S3 eventual consistency surprises, Stripe rate limits)

Bad candidates:
- "We had a bug in `calculateTotal`" — not a pattern, just a bug.
- "Database was down" — too generic to help next time.

## Patterns

<!--
The initial library is empty — l3-support populates it over time.
Seed entries (optional, keep if they match your stack):

### P-0001 — HPA thrashing during deploy exhausts source ports

**Tell** — connection-refused / EADDRNOTAVAIL errors 30-90s after a deploy; new pods come up but can't establish outbound connections.
**Hypothesis** — the old ReplicaSet is terminating while the new one is establishing outbound connections. Ephemeral ports aren't released fast enough; NAT/SNAT exhaustion on the node.
**Confirm with** — `kubectl get events --sort-by=.lastTimestamp | grep -i "FailedCreatePodSandBox\|network"`; check node-level conntrack table size.
**Fix** — raise `terminationGracePeriodSeconds`, lower `maxSurge` during rollout, or move to Topology-aware routing.
**Seen in** — PM-2024-XX-XX.
**Applies to** — any Kubernetes service with HPA and outbound HTTPS.
-->
