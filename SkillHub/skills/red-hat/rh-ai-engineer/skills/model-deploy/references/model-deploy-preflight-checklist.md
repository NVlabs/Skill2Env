# Model Deploy Pre-flight Checklist

Run these checks BEFORE deploying to avoid repeated deployment failures. Each check uses MCP tools to validate the target environment.

## 0. Validate Namespace is an RHOAI Data Science Project

**MCP Tool**: `list_data_science_projects` (from rhoai)

Verify the target namespace appears in the project list. If not found, warn: "Namespace `[namespace]` is not a Data Science Project. Model serving may not be configured. Create one via the OpenShift AI dashboard or proceed at your own risk."

## 0b. Check Model Storage Access (S3 Sources)

**MCP Tool**: `list_data_connections` (from rhoai)
- `namespace`: target namespace

If model source is S3-based, verify a matching data connection exists. If not found, inform user: "No S3 data connection found in namespace. Create one via the OpenShift AI dashboard or provide model source as PVC or HuggingFace URI."

## 1. Check Deployment Mode Support

**MCP Tool**: `resources_list` (from openshift)
- `apiVersion`: `"serving.knative.dev/v1"`, `kind`: `"Service"`, `namespace`: target namespace

If Knative Services are not available (CRD not found or error) -> auto-select **RawDeployment** mode and inform the user: "Knative Services are not available on this cluster. Switching to RawDeployment mode."

## 2. Check Namespace Resource Constraints

**MCP Tool**: `resources_list` (from openshift)
- `apiVersion`: `"v1"`, `kind`: `"LimitRange"`, `namespace`: target namespace

If a LimitRange exists:
- **Action**: `resources_get` for each LimitRange to extract min/max/default values
- Validate that planned resource requests fit within max limits
- **Warning**: If LimitRange minimum CPU > 10m or minimum memory > 15Mi, KServe-injected sidecar containers (with hardcoded 10m CPU / 15Mi memory requests) will fail to schedule. Warn the user: "LimitRange minimums conflict with KServe sidecar containers. The LimitRange must be adjusted or removed before deployment can succeed."
- Adjust planned resource requests/limits to fit within constraints
- Present adjusted values to user

## 3. Discover GPU Node Taints

**MCP Tool**: `resources_list` (from openshift)
- `apiVersion`: `"v1"`, `kind`: `"Node"`, `labelSelector`: `"nvidia.com/gpu.present=true"`

For each GPU node, extract taints. If custom taints exist (beyond standard Kubernetes taints like `node-role.kubernetes.io/*`):
- Auto-generate matching tolerations for the InferenceService
- Present discovered taints and proposed tolerations to user for confirmation
- Common example: `ai-app=true:NoSchedule` requires toleration `{key: "ai-app", operator: "Equal", value: "true", effect: "NoSchedule"}`

## 4. Check Existing Deployments in Namespace

**MCP Tool**: `list_inference_services` (from rhoai)
- `namespace`: target namespace
- `verbosity`: `"standard"`

If similar InferenceServices exist, inspect their `storageUri`, runtime, and tolerations as a reference for proven-working configuration in this environment.

## 5. Validate Model Source Accessibility

If using `oci://` source:
- Check namespace service account `imagePullSecrets` can access the registry
- For `registry.redhat.io/rhelai1/*` images: these require RHEL AI subscription entitlements -- verify pull secret has access or recommend switching to `hf://` (HuggingFace) source
- **Default preference**: For public open-source models, prefer `hf://` sources (e.g., `hf://ibm-granite/granite-3.1-2b-instruct`) as they require no authentication

## Summary

Present pre-flight results in a summary table and note any adjustments made. **WAIT for user confirmation if significant changes were needed** (e.g., deployment mode switch, resource adjustments, tolerations added).
