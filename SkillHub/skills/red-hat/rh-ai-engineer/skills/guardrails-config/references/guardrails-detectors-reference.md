# Guardrails Detectors Reference

Authoritative source for GuardrailsOrchestrator CRD fields, detector model recommendations, and orchestrator configuration structure.

## GuardrailsOrchestrator CRD

```yaml
apiVersion: trustyai.opendatahub.io/v1alpha1
kind: GuardrailsOrchestrator
metadata:
  name: guardrails-<target-isvc-name>
  namespace: <namespace>
spec:
  replicas: 1
  orchestratorConfig: <configmap-name>       # ConfigMap with detector routing config
  enableBuiltInDetectors: true               # Enable regex/validation detectors
  enableGuardrailsGateway: true              # Sidecar gateway for endpoint proxying
  otelExporter:                              # Optional: OpenTelemetry export
    endpoint: <collector-endpoint>
```

## Cluster Requirements

- **RHOAI version**: 2.14+ required for GuardrailsOrchestrator support
- **CRD name**: `guardrailsorchestrators.trustyai.opendatahub.io`
- **DSC enablement**: same as TrustyAI — `spec.components.trustyai.managementState: Managed`

## Recommended Detector Models

| Model | Use Case | GPU | Memory | Accuracy |
|-------|----------|-----|--------|----------|
| `ibm-granite/granite-guardian-3.1-2b` | Content safety, general harm | 1 GPU | ~8Gi | Good |
| `ibm-granite/granite-guardian-3.1-8b` | Content safety, nuanced detection | 1 GPU | ~24Gi | Higher |

These models are deployed as separate InferenceServices and serve as HuggingFace-type detectors.

## Detector Types

### HuggingFace Detector (model-based)
- Deployed as a KServe InferenceService
- Endpoint contract: `/api/v1/text/contents`
- Supports: content safety classification, toxicity, prompt injection
- Requires GPU or large CPU allocation

### LLM Judge Detector
- Uses an existing vLLM-served LLM as a judge
- Endpoint contract: OpenAI-compatible (`/v1/chat/completions`)
- Supports: custom natural-language evaluation criteria
- No additional deployment needed if LLM is already served

### Built-in Detector (regex/validation)
- Lightweight, no model deployment needed
- Supports: regex pattern matching, JSON/XML/YAML format validation
- Enabled via `enableBuiltInDetectors: true` in the CR

## Orchestrator ConfigMap Structure

The ConfigMap referenced by `spec.orchestratorConfig` uses this structure:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: guardrails-config-<isvc-name>
  labels:
    app.kubernetes.io/part-of: trustyai-guardrails
    trustyai.opendatahub.io/target-model: <isvc-name>
data:
  config.yaml: |
    orchestrator:
      target_model:
        name: <isvc-name>
        endpoint: <model-endpoint-url>
      detectors:
        input:
          - name: <detector-name>
            type: model|regex|llm-judge
            endpoint: <detector-endpoint>    # for model/llm-judge types
            pattern: <regex>                 # for regex type
            action: block|warn|passthrough
        output:
          - name: <detector-name>
            type: model|regex|llm-judge
            endpoint: <detector-endpoint>
            action: block|warn|passthrough
      policy:
        default_action: block|warn|passthrough
```

## Pod Selectors

- Orchestrator pods: label includes the CR name (e.g., `app.kubernetes.io/name=guardrails-<isvc-name>`)
- Guarded endpoint: exposed via the orchestrator's Service/Route, proxies to the target model

