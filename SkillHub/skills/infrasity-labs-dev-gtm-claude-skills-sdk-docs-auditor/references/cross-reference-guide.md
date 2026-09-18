# Cross-Reference Guide

When auditing any gap, always check if the content exists in another page before flagging it as "not covered anywhere". This reference describes the most common cross-reference patterns.

## Pages to always fetch and cross-check

1. **`/sdk/installation`** or `/getting-started`
2. **`/sdk/quick-start`** or `/quickstart`
3. **`/sdk/error-handling`** or `/errors`
4. **`/sdk/troubleshooting`**
5. **`/sdk/examples`**
6. **`/sdk/best-practices`**
7. **`/sdk/api-reference`** or `/sdk/reference` — CRITICAL for exception class names
8. **`/sdk/overview`** or `/sdk/control-plane-client-overview` — CRITICAL for constructor params
9. **Service pages**: agents, teams, jobs, workers, policies, environments, models, runtimes, skills, secrets, integrations, memory, semantic-search, context-graph

## Common cross-reference patterns by gap type

### Constructor / client setup gaps
- Env-var auto-detection → check: `api-reference`, `overview`, `control-plane-client-overview`
- Advanced params (timeout, max_retries, org_name) → check: `api-reference`
- Custom base_url → check: `api-reference`, `overview`

### Exception class gaps
- List all exception classes → check: `api-reference` exceptions section
- Service-specific exceptions (TeamError, JobError, etc.) → check: respective service page error handling section
- Import paths → check: `api-reference`

### Method signature discrepancies
- Execute call signature → check: `api-reference`, `control-plane-agents`
- Any method params → check: `api-reference` first, then the service-specific page

### Missing examples
- Memory examples → check: `context-graph-memory`
- Semantic search → check: `context-graph-semantic-search`
- Job scheduling → check: `control-plane-jobs`
- Policy management → check: `control-plane-policies`
- Worker management → check: `control-plane-workers`
- Agent lifecycle → check: `control-plane-agents`

### Missing best practices
- Worker best practices → check: `control-plane-workers` best practices section
- Job best practices → check: `control-plane-jobs` best practices section
- Policy best practices → check: `control-plane-policies` best practices section
- Agent best practices → check: `control-plane-agents` best practices section

### Missing troubleshooting
- Worker issues → check: `control-plane-workers` error handling section
- Job errors → check: `control-plane-jobs` error handling section
- Policy errors → check: `control-plane-policies` error handling section
- Dataset not found → check: `control-plane-client-overview` or dataset service page
- Health check URL → check: `api-reference` health service section, `examples`

## Gap classification rules

| Condition | Tag |
|-----------|-----|
| Content exists verbatim in another SDK page | `covered_in: [page-name]`, `nowhere: false` |
| Content is partially covered in another page | `covered_in: [page-name]`, `nowhere: false` with note |
| Content exists nowhere in the corpus | `covered_in: []`, `nowhere: true` |
| Factual error (wrong signature, wrong import) | Always `nowhere: true` regardless — the error needs fixing |

## Priority type classification

| Type | When to use |
|------|-------------|
| `error` | A factual mistake that will cause user code to fail (wrong method signature, wrong import path, wrong parameter name) |
| `missing` | A must-have that exists nowhere in the corpus |
| `xref` | Content exists on another page but needs to be linked/referenced from the audited page |
| `improvement` | A should-have gap — valuable but not causing user failures |

## Scoring deductions guide

### Installation (start at 100)
- Missing env-var auto-detection: -8
- Missing optional extras explanation: -6
- Missing version pinning guidance: -5
- Missing advanced constructor params: -7
- No verification snippet with expected output: -10
- No prerequisites section: -15
- No install command: -20

### Quick Start (start at 100)
- No minimal numbered step path: -15
- No expected output on any snippet: -10
- Worker/queue prerequisite unexplained: -12
- Model IDs not discoverable: -8
- Signature inconsistency with api-reference: -10
- No link to deeper docs: -5

### Error Handling (start at 100)
- Missing exception class from api-reference: -8 each
- No exception hierarchy diagram: -10
- Missing HTTP 401/403: -6
- No streaming error guidance: -7
- Wrong method signature in an example: -12
- Missing ControlPlaneError base usage: -5

### Troubleshooting (start at 100)
- No worker troubleshooting: -15
- No self-hosted/base_url guidance: -10
- Circular resolution for a common error: -8
- Missing service-specific section: -8 each
- No health check reference in "getting help": -5
- Rate limiting has no section: -8

### Examples (start at 100)
- Missing entire service category: -10 each
- No expected output on examples: -8
- Workflow example doesn't actually execute: -8
- No error handling in workflows: -7
- Missing multi-turn/session example: -6

### Best Practices (start at 100)
- Missing worker best practices: -8
- Missing job best practices: -7
- Missing policy best practices: -7
- Missing agent best practices: -7
- No concurrency/thread-safety: -10 (not covered anywhere penalty)
- No secret rotation guidance: -8
- Metrics example connects to nothing: -3