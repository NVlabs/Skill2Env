---
name: gke-basics
metadata:
  category: Containers
description: >-
  Core GKE cluster discovery and hub. Use to route to specialized GKE skills.
  Do not use for specialized tasks (networking, security, etc.) directly.
---

# GKE Basics

Managed Kubernetes platform on Google Cloud. Defaults to Autopilot mode.

## Quick Start

```bash
gcloud services enable container.googleapis.com --quiet
gcloud container clusters create-auto my-cluster --region=us-central1 --quiet
gcloud container clusters get-credentials my-cluster --region=us-central1 --quiet
```

## GKE Skill Routing Table

Load the single, most specific GKE sub-skill below matching your workload
requirements. **Do not load multiple GKE skills unless explicitly required.**

| Scenario             | Trigger Keywords             | Target Skill           |
| -------------------- | ---------------------------- | ---------------------- |
| Golden Path Defaults | production defaults, golden  | `gke-golden-path`      |
:                      : path                         :                        :
| Cluster Creation     | create cluster, provision    | `gke-cluster-creation` |
:                      : GKE                          :                        :
| Networking & Ingress | private cluster, VPC,        | `gke-networking`       |
:                      : Gateway API, Ingress, DNS    :                        :
| Security & IAM       | Workload Identity, Secret    | `gke-security`         |
:                      : Manager, RBAC, hardening     :                        :
| Autoscaling          | HPA, VPA, Cluster            | `gke-scaling`          |
:                      : Autoscaler, NAP              :                        :
| Compute Classes      | ComputeClass, Spot fallback, | `gke-compute-classes`  |
:                      : GPU/TPU nodes                :                        :
| Cost Optimization    | Spot VMs, rightsizing, cost  | `gke-cost`             |
:                      : allocation                   :                        :
| AI/ML Workloads      | LLM, GPU/TPU inference,      | `gke-inference`        |
:                      : serving, vLLM                :                        :
| Cluster Upgrades     | upgrade, maintenance window, | `gke-upgrades`         |
:                      : release channel              :                        :
| Observability        | monitoring, logging,         | `gke-observability`    |
:                      : Prometheus, dashboards       :                        :
| Multi-tenancy        | namespace isolation,         | `gke-multitenancy`     |
:                      : resource quota, LimitRange   :                        :
| Batch & HPC          | batch, HPC, Kueue, JobSet,   | `gke-batch-hpc`        |
:                      : parallel jobs                :                        :
| App Onboarding       | containerize, Dockerfile,    | `gke-app-onboarding`   |
:                      : deploy app, onboard          :                        :
| Backup & DR          | backup plan, restore,        | `gke-backup-dr`        |
:                      : disaster recovery, CMEK      :                        :
| Storage & PVC        | SSD, PV, PVC, StorageClass,  | `gke-storage`          |
:                      : GCS FUSE                     :                        :
| Reliability          | PDB, health probe, liveness, | `gke-reliability`      |
:                      : readiness                    :                        :

## Conceptual & Informational Queries (CRITICAL)

For purely conceptual, educational, or informational questions (e.g. "What is
GKE?", "Explain GKE architecture", or "Compare Standard vs Autopilot" in a
generic sense):

*   **Rule**: **Answer immediately using your pre-trained knowledge.**
*   **Constraint**: **Do not execute code searches, directory listings, or other
    tool calls** unless the user explicitly requests you to inspect the local
    workspace or run a command. Keep it fast, cheap, and direct.
