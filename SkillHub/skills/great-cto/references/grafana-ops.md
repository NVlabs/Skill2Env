---
name: grafana-ops
description: Grafana ops knowledge base: dashboard layout conventions, common queries (Loki, Tempo, Prometheus), p95/p99 patterns, log correlation
when_to_use: Production support on Grafana stack. Read by l3-support + devops
applies_to:
  - _default
---

# Grafana Ops Reference

> Ops knowledge base for Grafana-integrated projects. Read by `l3-support` during log checks,
> quick diagnostics, and P0 response. Companion to `mcp-servers/grafana.md` (setup guide).

## Tool Map — MCP tool to workflow step

| Grafana MCP Tool | Workflow step | When used |
|---|---|---|
| `mcp__grafana__search_alerts` | Step 2 Priority 0 + Proactive Poll | First check: firing alerts before log scan |
| `mcp__grafana__query_loki` | Step 2 Priority 0 | Replace `tail`/`grep` on log files — LogQL patterns below |
| `mcp__grafana__get_panel` | Step 3 Quick diagnostics | Error rate + latency from dashboard panels |
| `mcp__grafana__list_dashboards` | P0 Angle 1 (Reproduction/Scope) | Find service dashboard to confirm scope |
| `mcp__grafana__query_tempo` | P0 Angle 4 (Proof/Observability) | Distributed trace for the failing request |

**gcx CLI** (supplement — runs in Bash, no MCP needed):

| Command | Step | Purpose |
|---------|------|---------|
| `gcx alerts list --state firing` | Step 3 | List all firing alerts with labels |
| `gcx alerts list --state pending` | Step 3 | Upcoming alerts before they fire |
| `gcx metrics query '<promql>'` | Step 3 | Ad-hoc PromQL (error rate, latency) |
| `gcx correlate --commit HEAD` | P0 Angle 3 | Correlate alert start with recent commits |
| `gcx correlate --commit <sha> --service <name>` | P0 Angle 3 | Pin to specific deploy |

---

## LogQL Patterns

Use as datasource: `$LOKI_DS` (default: `Loki`). Time range: last 30 min unless noted.

### Error rate spike
```logql
sum(rate({service=~"$SERVICE"} |= "error" [5m]))
  / sum(rate({service=~"$SERVICE"} [5m]))
```
**What to look for:** ratio > p0-threshold (default 5%). If spike correlates with a deploy → Angle 3 (Recent Changes).

### Latency outliers
```logql
{service=~"$SERVICE"} | json | duration > 500ms
  | line_format "{{.level}} {{.duration}} {{.path}} {{.msg}}"
```
**What to look for:** which paths are slow, whether ORM/DB calls appear in the trace fields.

### OOM / killed process
```logql
{service=~"$SERVICE"} |~ "OOM|out of memory|Killed process|memory limit exceeded"
```
**What to look for:** PID of killed process, timestamp vs deploy time, memory trend in last 30m.

### Service down / panic
```logql
{service=~"$SERVICE"} |~ "panic|fatal|SIGTERM|SIGKILL|exit status [1-9]"
  | line_format "{{.timestamp}} {{.level}} {{.msg}}"
```
**What to look for:** stack trace lines, goroutine dump (Go), segfault address. Filter last 100 lines: `| tail 100`.

### Auth failures (feeds security gate 3b)
```logql
{service=~"$SERVICE"} |~ "401|403|unauthorized|forbidden|invalid token|JWT expired"
  | json | line_format "{{.user_id}} {{.ip}} {{.path}} {{.msg}}"
```
**What to look for:** single IP → DDoS/brute force → security gate; many users → broken auth middleware → P0 ops.

### Dependency timeout
```logql
{service=~"$SERVICE"} |~ "timeout|context deadline exceeded|connection refused|dial tcp"
  | json | line_format "{{.target}} {{.duration}} {{.msg}}"
```
**What to look for:** `target` field shows which dependency (DB, cache, external API). Cross-reference with `gcx metrics query 'up{job="$DEPENDENCY"}'`.

---

## PromQL SLI Queries

Use `gcx metrics query '<promql>' --from now-30m` or `mcp__grafana__get_panel`.

### Availability (error rate)
```promql
sum(rate(http_requests_total{status=~"2.."}[5m]))
  / sum(rate(http_requests_total[5m]))
```
> Healthy: > 0.999. Below 0.995 → P0. Use `{service="$SERVICE"}` label if available.

### p95 latency
```promql
histogram_quantile(0.95,
  sum(rate(http_request_duration_seconds_bucket[5m])) by (le))
```
> Healthy: < 200ms. Above 500ms → P1. Above 2000ms → P0.

### Error budget burn rate (99.9% SLO, 30-day window)
```promql
1 - (
  sum(rate(http_requests_total{status=~"2.."}[1h]))
  / sum(rate(http_requests_total[1h]))
) / (1 - 0.999)
```
> Burn rate > 1 → consuming budget faster than it recovers. > 14.4 → P0 (30-day budget gone in 2h).

### Anomaly band (pairs with grafana/promql-anomaly-detection)
```promql
# Upper bound (3σ from historical mean)
avg_over_time(http_request_duration_seconds_bucket[7d:5m])
  + 3 * stddev_over_time(http_request_duration_seconds_bucket[7d:5m])
```
> If current metric exceeds this band → `grafana/promql-anomaly-detection` will fire an alert automatically.

---

## Alert Correlation Workflow

Maps to the **4-angle bug-hunt** in `l3-support` P0 response:

```
1. Firing alert (mcp__grafana__search_alerts)
   └─ Extract: service label, alert name, start time
        │
2. Loki log query (mcp__grafana__query_loki)
   └─ Use LogQL pattern matching alert type (error rate → Error spike pattern above)
   └─ Extract: traceID field from structured JSON logs
        │
3. Tempo trace (mcp__grafana__query_tempo)
   └─ datasource: $TEMPO_DS, traceId: <extracted above>
   └─ Output: span tree → identifies slowest service/DB call (Angle 2: Code Path)
        │
4. Commit correlation (gcx correlate --commit HEAD)
   └─ Shows which recent commit changed the failing service
   └─ If deploy timestamp matches alert start → regression candidate (Angle 3: Recent Changes)
        │
5. Root-cause statement (Angle 4: Proof)
   └─ Format: "<service> <error> caused by <commit/change> at <time>, affecting <N>% of requests"
   └─ Evidence: Loki line + Tempo span + git sha
```

**Quick correlation check** (run in Step 3 Quick diagnostics for all incidents, not just P0):
```bash
if [ "$GCX_OK" = "true" ]; then
  gcx correlate --commit HEAD 2>/dev/null | head -10
fi
```

---

## Proactive Alert Classification

When running the `## Proactive Alert Polling` check, classify `search_alerts` output:

| Alert condition | Triage | Action |
|----------------|--------|--------|
| `severity=critical` AND `state=firing` | P0 | Skip monitoring wait → jump to P0 Response immediately |
| `severity=warning` AND `state=firing` | P1 | Create Beads task, continue monitoring window |
| `severity=warning` AND `state=pending` | P2 | Log only — alert hasn't fired yet, watch |
| `severity=info` | P2 | Log only |
| Auth-related alert (see LogQL auth pattern) | → security gate | Stop ops triage, run `/sec incident` |

---

## gcx Command Reference

```bash
# List all firing alerts with labels
gcx alerts list --state firing

# List pending alerts (about to fire)
gcx alerts list --state pending

# Query a metric ad-hoc
gcx metrics query 'up{job="api"}' --from now-30m
gcx metrics query 'sum(rate(http_requests_total[5m])) by (service)'

# Correlate an alert window with commits
gcx correlate --commit HEAD
gcx correlate --commit <sha> --service <service-name>

# All gcx commands respect GRAFANA_URL + GRAFANA_API_KEY from environment
# Set these from env.sh or PROJECT.md grafana-api-key-env: field
```
