---
name: infra-pack
description: IaC patterns (Terraform/Pulumi/CDK decision), GitOps (ArgoCD/Flux), FinOps + Karpenter for K8s autoscaling, secrets management (Vault/Doppler), observability stack
when_to_use: Building IaC, Kubernetes platforms, platform engineering, DevOps tooling
applies_to:
  - infra
---

# Infra Pack

> Extends `infra` archetype with IaC tool decision tree, GitOps patterns, FinOps essentials, observability stack, and edge runtime constraints.
> Auto-loaded when `archetype: infra` is detected in PROJECT.md.
> Also loaded explicitly via `packs: [infra-pack]`.

## Decision tree — IaC tool

| If you... | Pick | Why |
|-----------|------|-----|
| Want HCL, declarative, mature ecosystem, multi-cloud | **Terraform / OpenTofu** | The standard. OpenTofu is the open-source fork after license change. Use OpenTofu for new projects. |
| Want general-purpose languages (TS/Python/Go), strong typing | **Pulumi** | IaC in the language you already know. Better refactoring, testing. |
| AWS-only, want to model with TypeScript/Python | **AWS CDK** | First-party from AWS. Synthesises to CloudFormation. |
| Kubernetes-native, control plane lives in cluster | **Crossplane** | Treat cloud resources as K8s objects. Best when you're already deep in K8s. |
| Don't want to manage state files | **Pulumi (managed backend)** or **Terraform Cloud** | State management is a real pain. Pay for it. |

**Anti-pattern**: mixing Terraform + Pulumi + CDK in same org without a clear boundary. Pick one per team. Cross-tool resources are nightmare to debug.

## State backend — non-negotiable

Never store state on a developer's laptop. Always remote, always locked.

| Tool | State backend |
|------|--------------|
| Terraform / OpenTofu | S3 + DynamoDB lock; Terraform Cloud; Spacelift |
| Pulumi | Pulumi Cloud (managed); S3 + DynamoDB self-hosted |
| AWS CDK | CloudFormation (managed by AWS) |

State backend MUST have:
- Encryption at rest
- Versioning (S3 versioning enabled)
- Access logs (CloudTrail or equivalent)
- IAM least-privilege (only CI + ops can read; only Atlantis/CI can write)

## CI for IaC

| Tool | Purpose |
|------|---------|
| **Atlantis** | Self-hosted; comments `terraform plan` on every PR; `atlantis apply` after approval |
| **Terraform Cloud** | Hosted equivalent; commercial |
| **Spacelift** | Multi-IaC (Terraform, Pulumi, CDK), policy-as-code via OPA |
| **Env0** | Similar to Spacelift; better Terragrunt support |

For new project without strong preference: **Atlantis on a small EC2/ECS instance** is enough until you hit ~20 PRs/day. Then graduate to Spacelift.

## Policy as code — required for compliance

Don't trust developers to remember 100 security rules. Encode them.

| Tool | Use |
|------|-----|
| **Open Policy Agent (OPA)** + Conftest | Generic policy engine, works for K8s, Terraform, Dockerfile, GitHub PRs |
| **Sentinel** | HashiCorp's policy engine — Terraform Cloud only |
| **Checkov** | Security-focused for Terraform/CloudFormation/K8s — pre-commit + CI gate |
| **tfsec** | Now part of Trivy — security-only Terraform scanner |
| **kube-score / Polaris** | K8s manifest best-practice checks |

Run all of these in CI. Block merge on critical findings.

Example OPA policy (no public S3 buckets):

```rego
package terraform.s3
deny[msg] {
    resource := input.resource_changes[_]
    resource.type == "aws_s3_bucket_public_access_block"
    not resource.change.after.block_public_acls
    msg := sprintf("S3 bucket %v must block public ACLs", [resource.address])
}
```

## GitOps for Kubernetes

| Tool | When |
|------|------|
| **ArgoCD** | Most popular. Web UI for visibility. Application sets for fleet management. |
| **Flux** | CNCF graduated. CLI-first. Integrates with Helm Operator and Kustomize natively. |
| **Argo Workflows** (different from ArgoCD) | For job orchestration, not GitOps |

Both are excellent. Pick based on team preference for UI-vs-CLI. **Don't run both.**

GitOps rules:
- Production state lives in git, not in `kubectl` commands
- Drift detection: ArgoCD/Flux alerts when cluster diverges from git
- Sync waves for ordered deploys (CRDs first, then operators, then apps)
- Sealed secrets or External Secrets Operator for credentials in git

## Cluster management decision

| Need | Pick |
|------|------|
| Production multi-team, AWS | **EKS** + managed node groups + Karpenter for autoscaling |
| Production multi-team, GCP | **GKE Autopilot** for managed nodes; **GKE Standard** for control |
| Production multi-team, Azure | **AKS** + virtual node pools |
| Cheap dev/staging on a VPS | **k3s** (Rancher) — full K8s in 100 MB |
| Edge / IoT clusters | **k3s** or **MicroK8s** |
| Bare metal production | **kubeadm** + custom lifecycle, OR **Rancher RKE2** for managed feel |

**Anti-pattern**: rolling your own etcd HA in a 3-engineer team. Use managed control plane.

## Service mesh — only when you need it

Service mesh adds operational cost. Justify with a concrete need:

- mTLS between services (compliance requirement)
- Traffic shifting / canary at L7 (without app code changes)
- Distributed tracing without instrumenting every service
- Multi-cluster service discovery

| Tool | When |
|------|------|
| **Linkerd** | Simpler, lower memory overhead, best for "we just want mTLS + observability" |
| **Istio** | Heavier, more features, best for "we need policy + traffic management" |
| **Cilium** | eBPF-based, replaces kube-proxy, can also do mesh; pick when network perf matters |

If you can't articulate the concrete benefit in one sentence → don't install a mesh. The default Kubernetes networking + Pod-to-Pod TLS via cert-manager is enough for most teams.

## Secrets management

| Tool | When |
|------|------|
| **External Secrets Operator** | K8s-native, syncs from AWS Secrets Manager / Vault / GCP Secret Manager into Secrets |
| **HashiCorp Vault** | Self-hosted, full feature set (PKI, dynamic secrets, transit encryption) |
| **Doppler** | SaaS, dev-friendly UX, syncs to most platforms |
| **AWS Secrets Manager / GCP Secret Manager / Azure Key Vault** | Cloud-native, integrates with IAM |
| **Sealed Secrets (Bitnami)** | GitOps-friendly: encrypted secrets in git, decrypted in cluster |
| **SOPS + age** | File-based encryption for IaC secrets, works with any tool |

**Default for new K8s project**: External Secrets Operator + AWS Secrets Manager (or GCP/Azure equivalent). Lowest overhead, cloud-native.

**Never**:
- Commit `.env` files with real secrets
- Pass secrets via CI environment variables that get logged
- Print secrets in error messages
- Use the same secret for dev/staging/prod

## Observability stack

For new projects, the LGTM stack (Grafana ecosystem) is a strong default:

| Layer | Tool |
|-------|------|
| Metrics | **Prometheus** (scrape) → **Mimir** (long-term storage at scale) or **Grafana Cloud** |
| Logs | **Loki** (log aggregation) |
| Traces | **Tempo** (distributed traces, OTLP-native) |
| Dashboards | **Grafana** |
| Profiling | **Pyroscope** (continuous profiling) |
| Alerting | **Alertmanager** (Prometheus) → PagerDuty / Opsgenie |

All of these are open source, all integrate via OpenTelemetry. If your `l3-support` agent is wired with `mcp-servers/grafana.md`, it queries this stack natively.

Alternatives by ecosystem:
- **AWS native**: CloudWatch Logs + Metrics + X-Ray
- **GCP native**: Cloud Logging + Monitoring + Trace
- **Commercial all-in-one**: Datadog (most features, most expensive), New Relic, Honeycomb (best for traces)

## Instrumentation — OpenTelemetry only

Standardise on OTel. Don't ship app code with vendor-specific SDKs.

```yaml
# Application emits OTel signals to a collector
APP_SDK → OTLP → otel-collector → backend (Tempo/Loki/Mimir or vendor)
```

The collector is the abstraction layer. Switch backends by reconfiguring the collector, not by re-instrumenting your apps.

OTel auto-instrumentation libraries cover Node, Python, Java, Go, Ruby, .NET. Manual instrumentation only for custom spans.

## FinOps essentials

Cloud costs grow silently. Set guardrails:

### Tagging

Every resource MUST have:
- `team` — who owns this
- `env` — prod / staging / dev
- `cost-center` — for chargeback
- `expires` — for ephemeral resources (auto-delete script picks these up)

Enforce via Terraform default tags + Checkov rules.

### Budget alerts

Per AWS account / GCP project / Azure subscription:
- Alert at 50% of monthly budget
- Alert at 75%
- Alert at 90% (page on-call)
- Hard cap (suspend creation of new expensive resources) at 100%

Use AWS Budgets / GCP Billing Budgets / Azure Cost Management.

### Karpenter (AWS)

Replaces cluster-autoscaler with smarter, faster, cheaper node provisioning. Picks Spot instances when possible, consolidates underutilised nodes.

```yaml
# Provisioner: 70% Spot, 30% On-Demand
spec:
  requirements:
    - key: karpenter.sh/capacity-type
      operator: In
      values: [spot, on-demand]
  limits:
    cpu: 1000
```

Typical savings: 40-60% vs cluster-autoscaler with all-On-Demand.

### Spot instances

Use for:
- Stateless workers
- Batch jobs (with checkpointing)
- Dev/staging environments
- Karpenter-managed K8s nodes

Don't use for:
- Stateful databases (well, except read replicas)
- Single-instance services with no fast restart
- Long-running jobs without checkpointing

### Reserved instances / Savings plans

- Compute Savings Plans (AWS): commit to $/hr for 1 or 3 years, get 20-50% discount, applies to EC2/Fargate/Lambda
- GCP Committed Use Discounts: 1 or 3 year, similar
- Azure Reserved Instances: similar

Run a quarterly review: are commits utilised > 90%? Adjust at renewal.

`/cost` command surfaces commit utilisation if `cost-history.log` is configured.

## Edge runtime

If your `infra` archetype includes `edge-app`, see `web-pack.md` § "Edge runtime considerations". Hard constraints (cold start, bundle size, memory) are real, not preferences.

## Disaster recovery (DR)

For each environment, define and test:

- **RPO** (Recovery Point Objective): max data loss tolerable (e.g. 1 hour)
- **RTO** (Recovery Time Objective): max downtime tolerable (e.g. 4 hours)

Then choose strategy:

| Strategy | Cost | RTO | RPO |
|----------|------|-----|-----|
| Backup & restore | $ | hours-days | hours |
| Pilot light | $$ | minutes-hours | minutes |
| Warm standby | $$$ | minutes | seconds |
| Multi-site active | $$$$ | seconds | near-zero |

DR drills run quarterly. Documented in `docs/runbooks/DR.md`. `l3-support` knows the runbook location and reads it during incidents.

## Compliance defaults for `infra` archetype

| Trigger | Add to compliance |
|---------|-------------------|
| Always | `cis-benchmarks` (CIS Benchmark for AWS/GCP/Azure/K8s) |
| K8s | `cis-k8s` |
| Public cloud | `aws-foundations` / `gcp-cis` / `azure-cis` |
| EU data | `gdpr` (data residency, BCRs) |
| US healthcare | `hipaa` (BAA with cloud providers) |
| US financial | `soc2`, `sox` |
| Critical infra (EU) | `nis2` |
| Financial (EU) | `dora` |

`security-officer` runs the matching checklist when these are set.

## Anti-patterns specific to `infra` archetype

| Pattern | Why it fails | Fix |
|---------|-------------|-----|
| `terraform apply` from a developer's laptop | Drift, race conditions, credentials in shell history | All applies via Atlantis/CI |
| Sharing AWS root credentials in Slack | Compromise = full account takeover | IAM roles + SSO + MFA |
| One huge Terraform state file | Slow plans, high blast radius | Split by lifecycle (network/data/compute) and team |
| `kubectl apply` from any machine | Drift from git, no audit trail | GitOps via Argo/Flux |
| No backups for "stateless" services | Some service was actually stateful (config, secrets, certificates) | Back up everything that took human work to create |
| All-On-Demand Kubernetes nodes | 40-60% cost overhead | Karpenter + Spot |
| Manual TLS cert rotation | Forgotten cert = outage at 3am | cert-manager + Let's Encrypt |
| Public S3 buckets | Data breach in production | Bucket Policy + Block Public Access |
| `:latest` Docker tags in production | Non-reproducible deploys, can't roll back | Pin to git SHA tag, use `Always` pull policy |

## QA extras provided by this pack

When `archetype: infra`, `qa-engineer` automatically runs:

- **`terraform plan`** on every PR (via Atlantis)
- **Checkov** scan (Terraform + K8s manifests)
- **tfsec / Trivy** scan
- **CIS Benchmark** for cloud + K8s
- **DR failover drill** verification (test ran < 90 days ago)
- **Cost delta** check (`> 20%` increase requires justification)
- **Drift check** (no `terraform plan` shows uncommitted changes)

## Recommended `PROJECT.md` for new infra project

```yaml
primary: infra-iac
archetype: infra
project_size: medium
stack: [terraform, kubernetes, helm, aws]
team-size: 2
compliance: [cis-benchmarks, gdpr]
deploy-method: terraform
qa-extras: [checkov, tfsec, drift-check]
packs: [infra-pack]
```
