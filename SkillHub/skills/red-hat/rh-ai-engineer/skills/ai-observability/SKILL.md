---
name: ai-observability
description: |
  Analyze AI model performance, GPU utilization, and cluster health on OpenShift AI.

  Use when:
  - "How is my model performing?"
  - "What GPUs are available in the cluster?"
  - "Show me inference latency for Llama"
  - "Check OpenShift cluster health metrics"
  - "Trace a slow inference request"
  - "Correlate errors across my inference stack"

  Query-driven, read-only analysis. Routes to the appropriate observability domain based on user intent.

  NOT for deploying models (use /model-deploy).
  NOT for debugging failed deployments (use /debug-inference).
model: inherit
color: cyan
license: Apache-2.0
allowed-tools: list_models list_vllm_namespaces get_gpu_info get_deployment_info analyze_vllm chat_vllm analyze_openshift list_openshift_metric_groups list_openshift_namespaces query_tempo_tool get_trace_details_tool search_metrics execute_promql korrel8r_get_correlated list_data_science_projects list_inference_services get_inference_service resources_get resources_list pods_list
---

# /ai-observability Skill

Analyze AI model inference performance, GPU utilization, OpenShift cluster health, and distributed traces on Red Hat OpenShift AI. This is a query-driven, read-only skill: the user asks a question, and the skill routes to the appropriate observability domain (vLLM metrics, OpenShift health, Tempo traces, or cross-domain correlation via Korrel8r).

## Prerequisites

**Required MCP Server**: `ai-observability` ([AI Observability MCP](https://github.com/rh-ai-quickstart/ai-observability-summarizer))

**Required MCP Tools**:
- `list_models` (from ai-observability) - Discover served models
- `list_vllm_namespaces` (from ai-observability) - List monitored namespaces
- `get_gpu_info` (from ai-observability) - GPU inventory and utilization
- `get_deployment_info` (from ai-observability) - Deployment health status
- `analyze_vllm` (from ai-observability) - Model performance analysis
- `chat_vllm` (from ai-observability) - Conversational follow-up on vLLM metrics
- `analyze_openshift` (from ai-observability) - Cluster/namespace health metrics
- `list_openshift_metric_groups` (from ai-observability) - Available metric categories
- `list_openshift_namespaces` (from ai-observability) - Namespaces in Prometheus
- `query_tempo_tool` (from ai-observability) - Distributed trace queries
- `get_trace_details_tool` (from ai-observability) - Trace span details
- `search_metrics` (from ai-observability) - Metric discovery by pattern
- `execute_promql` (from ai-observability) - Custom PromQL queries
- `korrel8r_get_correlated` (from ai-observability) - Cross-domain signal correlation

**Optional MCP Server**: `rhoai` ([RHOAI MCP Server](https://github.com/opendatahub-io/rhoai-mcp))

**Optional MCP Tools** (from rhoai):
- `list_data_science_projects` - Discover RHOAI projects for scope selection
- `list_inference_services` - List deployed models with structured status for context
- `get_inference_service` - Get InferenceService status for context

**If rhoai is unavailable or returns errors**: Use `openshift` tools as fallback — `resources_list` with `apiVersion: serving.kserve.io/v1beta1`, `kind: InferenceService` replaces `list_inference_services`; `resources_list` with `apiVersion: v1`, `kind: Namespace`, `labelSelector: opendatahub.io/dashboard=true` replaces `list_data_science_projects`.

**Optional MCP Server**: `openshift` ([OpenShift MCP Server](https://github.com/openshift/openshift-mcp-server))

**Optional MCP Tools** (from openshift):
- `resources_get` (from openshift) - Get raw resource details for context
- `resources_list` (from openshift) - List InferenceServices, Namespaces (fallback for rhoai tools)
- `pods_list` (from openshift) - List predictor pods for correlation context

**Common prerequisites** (KUBECONFIG, OpenShift+RHOAI cluster, verification protocol): See [skill-conventions.md](../references/skill-conventions.md).

**Additional environment variables**:
- `AI_OBSERVABILITY_MCP_URL` - URL for the AI Observability MCP server (e.g., `http://aiobs-mcp.apps.cluster.example.com`)

**Additional cluster requirements**:
- AI Observability MCP server deployed on-cluster (from `quay.io/ecosystem-appeng/aiobs-mcp-server`)
- Prometheus configured with vLLM and OpenShift metrics
- Tempo configured for distributed tracing (optional, for trace analysis)
- Korrel8r deployed (optional, for cross-domain correlation)

## When to Use This Skill

**Use this skill when you need to:**
- Check model inference performance (latency, throughput, error rates)
- View GPU inventory and utilization across the cluster
- Analyze OpenShift cluster health metrics by category
- Trace slow inference requests with distributed tracing (Tempo)
- Correlate signals across logs, metrics, traces, and alerts (Korrel8r)
- Run custom PromQL queries against cluster Prometheus

**Do NOT use this skill when:**
- You need to troubleshoot a failed deployment (use `/debug-inference`)
- You want to deploy or redeploy a model (use `/model-deploy`)
- You need to create or modify a ServingRuntime (use `/serving-runtime-config`)

## Workflow

### Step 1: Verify MCP and Triage Intent

**Verify ai-observability MCP server is reachable.** If any tool call fails with a connection error:

```
Cannot execute /ai-observability: ai-observability MCP server is not reachable.

Setup Instructions:
1. Deploy the server on your cluster from quay.io/ecosystem-appeng/aiobs-mcp-server
   See: https://github.com/rh-ai-quickstart/ai-observability-summarizer
2. Set AI_OBSERVABILITY_MCP_URL to the server route URL
3. Restart Claude Code to reload MCP servers

Options: setup (show deployment guide) / abort
```

**WAIT for user decision if MCP is unavailable.**

**Classify user query** into one of these domains:

| Domain | Trigger Phrases | Primary Tool(s) |
|--------|----------------|-----------------|
| Model Discovery | "what models", "list models", "what's deployed" | `list_models`, `list_vllm_namespaces` |
| GPU Inventory | "GPU", "GPU utilization", "what GPUs", "available hardware" | `get_gpu_info` |
| vLLM Performance | "latency", "throughput", "performance", "how is [model]", "slow" | `analyze_vllm` |
| OpenShift Health | "cluster health", "namespace metrics", "node health", "pods" | `analyze_openshift` |
| Tracing | "trace", "latency trace", "slow request", "spans" | `query_tempo_tool` |
| Correlation | "correlate", "root cause", "what's related to" | `korrel8r_get_correlated` |
| Custom PromQL | "PromQL", "custom query", "specific metric" | `execute_promql` |

If the intent is ambiguous, present the domain options and ask the user to choose.

If the user specifies a model name, use `list_models` first to verify it exists and get the correct identifier. If the user does not specify a namespace, use `list_vllm_namespaces` or `list_openshift_namespaces` to discover available namespaces and present them.

**Project context** (if `rhoai` MCP available): For "what's running" or "what's deployed" queries, use `list_data_science_projects` (from rhoai) to provide project-level overview. Use `list_inference_services` (from rhoai) per project to show deployed models with status.

**WAIT for user to confirm scope before proceeding to analysis.**

### Step 2: Execute Analysis

Branch based on the domain determined in Step 1.

#### Step 2a: Model Discovery

**MCP Tool**: `list_models` (from ai-observability)

**Parameters**: None

**MCP Tool**: `list_vllm_namespaces` (from ai-observability)

**Parameters**: None

Present results:

| Model Name | Namespace |
|------------|-----------|
| [model] | [namespace] |

**Offer**: "Would you like to analyze performance for a specific model, or check GPU inventory?"

**WAIT for user decision.**

#### Step 2b: GPU Inventory

**MCP Tool**: `get_gpu_info` (from ai-observability)

**Parameters**: None

Present results:

| Node | GPU Type | Count | Temperature | Power Usage |
|------|----------|-------|-------------|-------------|
| [node] | [type] | [count] | [temp] | [watts] |

If GPUs are near capacity, note: "Some GPUs are heavily utilized. Check model performance or consider scaling."

**Offer**: "Would you like to check which models are using these GPUs, or analyze a specific model's performance?"

**WAIT for user decision.**

#### Step 2c: vLLM Performance Analysis

Requires: model name (from user or discovered via `list_models` in Step 1).

**MCP Tool**: `get_deployment_info` (from ai-observability)

**Parameters**:
- `namespace`: model's namespace - REQUIRED
- `model`: model name - REQUIRED

Report deployment status (is_new_deployment, deployment_date).

**MCP Tool**: `analyze_vllm` (from ai-observability)

**Parameters**:
- `model_name`: vLLM model identifier - REQUIRED
- `summarize_model_id`: LLM for analysis (use server default if not specified) - REQUIRED
- `time_range`: natural language time range, e.g., `"15m"`, `"1h"`, `"24h"` - OPTIONAL (default: `"15m"`)
- `start_datetime`: ISO datetime string - OPTIONAL (alternative to time_range)
- `end_datetime`: ISO datetime string - OPTIONAL (alternative to time_range)

Present the LLM-generated analysis covering: latency (p50/p95/p99), throughput (requests/sec), token rates (input/output tokens/sec), error rate, queue depth.

**Offer**:
```
Would you like to:
1. Ask a follow-up question about these metrics
2. Trace a slow inference request
3. Correlate with other signals (logs, alerts)
4. Check a different time range
5. Exit analysis
```

**WAIT for user decision.**

If user asks a follow-up question:

**MCP Tool**: `chat_vllm` (from ai-observability)

**Parameters**:
- `model_name`: same model name - REQUIRED
- `prompt_summary`: the analysis output from `analyze_vllm` - REQUIRED
- `question`: the user's follow-up question - REQUIRED
- `summarize_model_id`: LLM for response - REQUIRED

#### Step 2d: OpenShift Health Analysis

**MCP Tool**: `list_openshift_metric_groups` (from ai-observability)

**Parameters**: None

Present available metric categories to user if they did not specify one.

**WAIT for user to select a category.**

**MCP Tool**: `analyze_openshift` (from ai-observability)

**Parameters**:
- `metric_category`: the selected category (e.g., `"Fleet Overview"`, `"GPU & Accelerators"`, `"Workloads & Pods"`, `"Storage & Networking"`) - REQUIRED
- `scope`: `"cluster_wide"` or `"namespace_scoped"` - OPTIONAL (default: `"cluster_wide"`)
- `namespace`: required when scope is `"namespace_scoped"` - CONDITIONAL
- `time_range`: natural language time range - OPTIONAL
- `start_datetime`: ISO datetime string - OPTIONAL
- `end_datetime`: ISO datetime string - OPTIONAL

Present the health assessment and key metrics.

**Offer**: "Would you like to check another metric category, drill into a specific namespace, or exit?"

**WAIT for user decision.**

#### Step 2e: Distributed Tracing

Requires: service name or operation name, and time range.

**MCP Tool**: `query_tempo_tool` (from ai-observability)

**Parameters**:
- `query`: TraceQL query string (e.g., `"{resource.service.name=\"[service]\"}"`) - REQUIRED
- `start_time`: ISO datetime string (e.g., `"2024-01-01T00:00:00Z"`) - REQUIRED
- `end_time`: ISO datetime string - REQUIRED
- `limit`: max traces to return - OPTIONAL (default: 10)

Present traces:

| Trace ID | Duration (ms) | Root Service | Span Count | Start Time |
|----------|--------------|--------------|------------|------------|
| [id] | [duration] | [service] | [spans] | [time] |

**Ask**: "Would you like to drill into a specific trace? Enter a Trace ID."

**WAIT for user decision.**

If user selects a trace:

**MCP Tool**: `get_trace_details_tool` (from ai-observability)

**Parameters**:
- `trace_id`: the trace ID string - REQUIRED

Present span waterfall:

| Span | Service | Operation | Duration (ms) | Status |
|------|---------|-----------|---------------|--------|
| [span-id] | [service] | [operation] | [duration] | [ok/error] |

**Offer**: "Would you like to view another trace, correlate this trace with logs/metrics, or exit?"

**WAIT for user decision.**

#### Step 2f: Cross-Domain Correlation (Korrel8r)

Requires: a starting point (pod name and namespace, or other Korrel8r domain query).

**MCP Tool**: `korrel8r_get_correlated` (from ai-observability)

**Parameters**:
- `query`: Korrel8r domain query string - REQUIRED
  - Example: `k8s:Pod:{"namespace":"llm-serving","name":"vllm-predictor-abc"}`
- `goals`: array of target domain class names - REQUIRED
  - Example: `["log:application", "metric:metric", "trace:span", "alert:alert"]`

Present correlated signals grouped by domain:

**Related Logs**: [count] log entries found
**Related Metrics**: [count] metric series
**Related Traces**: [count] trace spans
**Related Alerts**: [count] active alerts

**Offer**: "Would you like to drill into any of these correlated signals?"

**WAIT for user decision.**

#### Step 2g: Custom PromQL Query

For advanced users who want to run specific PromQL.

**MCP Tool**: `search_metrics` (from ai-observability)

**Parameters**:
- `pattern`: search string (e.g., `"vllm latency"`) - OPTIONAL (default: `""`)
- `limit`: max results, 1-1000 - OPTIONAL (default: 50)

Present matching metrics with their descriptions. Let user select or compose a query.

**MCP Tool**: `execute_promql` (from ai-observability)

**Parameters**:
- `query`: PromQL query string - REQUIRED
- `time_range`: relative time range (e.g., `"5m"`, `"1h"`) - OPTIONAL
- `start_datetime`: ISO datetime string - OPTIONAL
- `end_datetime`: ISO datetime string - OPTIONAL

Present query results.

**Offer**: "Would you like to run another query, or exit?"

**WAIT for user decision.**

### Step 3: Follow-Up and Drill-Down

After presenting initial results, offer domain-appropriate follow-up options:

- For vLLM analysis: use `chat_vllm` for conversational follow-up
- For traces: allow drilling into specific trace IDs via `get_trace_details_tool`
- For correlation: allow drilling into correlated signals
- For any domain: offer to switch to a different analysis domain

Present options and **WAIT for user decision**. Options always include an "Exit analysis" choice.

### Step 4: Summary and Next Steps

When the user chooses to exit:

Summarize key findings from the analysis session.

**If issues were found**, suggest:
- `/debug-inference` for deployment or pod-level problems
- `/model-deploy` to redeploy with different configuration
- Custom PromQL queries for ongoing monitoring

**If everything looks healthy**, confirm: "All monitored metrics are within normal ranges."

## Common Issues

### Issue 1: AI Observability MCP Server Not Deployed

**Error**: Connection refused or timeout when reaching `AI_OBSERVABILITY_MCP_URL`

**Cause**: The AI Observability MCP server is not deployed on the cluster, or the route/service is not accessible.

**Solution:**
1. Deploy the server from `quay.io/ecosystem-appeng/aiobs-mcp-server` -- see https://github.com/rh-ai-quickstart/ai-observability-summarizer
2. Verify the route is accessible: `oc get route -n [namespace] aiobs-mcp`
3. Set `AI_OBSERVABILITY_MCP_URL` to the route URL
4. Restart Claude Code to reload MCP servers

### Issue 2: No Models Found in Monitoring

**Error**: `list_models` returns empty results

**Cause**: vLLM metrics are not being scraped by Prometheus, or no InferenceServices are deployed.

**Solution:**
1. Verify InferenceServices exist: use `resources_list` from `openshift` MCP
2. Check that Prometheus ServiceMonitor is configured for vLLM metrics
3. Verify the vLLM serving container exposes `/metrics` endpoint

### Issue 3: Tempo Traces Not Available

**Error**: `query_tempo_tool` returns empty or connection error

**Cause**: Tempo is not deployed, or distributed tracing is not configured for the inference stack.

**Solution:**
1. Verify Tempo is deployed in the cluster
2. Check OpenTelemetry instrumentation on the inference endpoints
3. Verify Tempo datasource is configured in the MCP server

### Issue 4: Korrel8r Correlation Returns No Results

**Error**: `korrel8r_get_correlated` returns empty correlation

**Cause**: Korrel8r is not deployed, or the query format is incorrect.

**Solution:**
1. Verify Korrel8r is deployed and accessible
2. Check the query format matches Korrel8r domain syntax (e.g., `k8s:Pod:{"namespace":"[ns]","name":"[pod]"}`)
3. Ensure the target pod/namespace exists and has generated observability signals

## Dependencies

### MCP Tools
See [Prerequisites](#prerequisites) for the complete list of required and optional MCP tools.

### Related Skills
- `/debug-inference` - Troubleshoot deployment issues found during analysis
- `/model-deploy` - Redeploy models with different configuration based on findings
- `/serving-runtime-config` - Adjust runtime parameters if performance issues are runtime-related
- `/model-monitor` - TrustyAI bias/drift metrics (complements infrastructure observability)

### Reference Documentation
- [known-model-profiles.md](docs/references/known-model-profiles.md) - Expected performance baselines for common models
- [supported-runtimes.md](docs/references/supported-runtimes.md) - Runtime capabilities and known limitations

## Critical: Human-in-the-Loop Requirements

See [skill-conventions.md](../references/skill-conventions.md) for general HITL and security conventions.

**Skill-specific checkpoints:**
- After triage (Step 1): confirm analysis scope (model, namespace, time range) before running queries
- After initial analysis (Step 2): present follow-up options, wait for user choice
- After correlation (Step 2f): confirm before drilling into correlated signals
- **NEVER** expose raw Prometheus/Tempo credentials or internal cluster endpoints in output
- **NEVER** execute unbounded PromQL queries (no time limit, extremely wide label selectors) without confirming with the user
