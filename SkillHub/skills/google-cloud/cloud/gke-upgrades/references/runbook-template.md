# Runbook Command Templates

Standard command sequences for GKE upgrades. Replace placeholders: `CLUSTER_NAME`, `ZONE`, `TARGET_VERSION`, `NODE_POOL_NAME`.

## Table of Contents
- [Pre-flight](#pre-flight) (Line 12-31)
- [Control plane upgrade](#control-plane-upgrade) (Line 32-47)
- [Node pool upgrade (Standard only)](#node-pool-upgrade-standard-only) (Line 48-71)
- [Maintenance window configuration](#maintenance-window-configuration) (Line 72-109)
- [Rollback/Downgrade guidance](#rollbackdowngrade-guidance) (Line 110-145)

## Pre-flight

```bash
# Current versions
gcloud container clusters describe CLUSTER_NAME \
  --zone ZONE \
  --format="table(name, currentMasterVersion, nodePools[].version)"

# Available versions for channel
gcloud container get-server-config --zone ZONE \
  --format="yaml(channels)"

# Deprecated API usage
kubectl get --raw /metrics | grep apiserver_request_total | grep deprecated

# Cluster health
kubectl get nodes
kubectl get pods -A | grep -v Running | grep -v Completed
```

## Control plane upgrade

```bash
gcloud container clusters upgrade CLUSTER_NAME \
  --zone ZONE \
  --master \
  --cluster-version TARGET_VERSION

# Verify (wait ~10-15 min)
gcloud container clusters describe CLUSTER_NAME \
  --zone ZONE \
  --format="value(currentMasterVersion)"

kubectl get pods -n kube-system
```

## Node pool upgrade (Standard only)

```bash
# Configure surge settings
gcloud container node-pools update NODE_POOL_NAME \
  --cluster CLUSTER_NAME \
  --zone ZONE \
  --max-surge-upgrade MAX_SURGE \
  --max-unavailable-upgrade MAX_UNAVAILABLE

# Upgrade
gcloud container node-pools upgrade NODE_POOL_NAME \
  --cluster CLUSTER_NAME \
  --zone ZONE \
  --cluster-version TARGET_VERSION

# Monitor progress
watch 'kubectl get nodes -o wide -L cloud.google.com/gke-nodepool'

# Verify
gcloud container node-pools list --cluster CLUSTER_NAME --zone ZONE
kubectl get pods -A | grep -v Running | grep -v Completed
```

## Maintenance window configuration

```bash
# Set recurring maintenance window
gcloud container clusters update CLUSTER_NAME \
  --zone ZONE \
  --maintenance-window-start YYYY-MM-DDTHH:MM:SSZ \
  --maintenance-window-end YYYY-MM-DDTHH:MM:SSZ \
  --maintenance-window-recurrence "FREQ=WEEKLY;BYDAY=SA"

# Add maintenance exclusion (up to 90 days)
gcloud container clusters update CLUSTER_NAME \
  --zone ZONE \
  --add-maintenance-exclusion-name="EXCLUSION_NAME" \
  --add-maintenance-exclusion-start=START_TIME \
  --add-maintenance-exclusion-end=END_TIME

# Add persistent maintenance exclusion (until End of Support)
gcloud container clusters update CLUSTER_NAME \
  --zone ZONE \
  --add-maintenance-exclusion-name="EXCLUSION_NAME" \
  --add-maintenance-exclusion-start=START_TIME \
  --add-maintenance-exclusion-until-end-of-support \
  --add-maintenance-exclusion-scope=no_upgrades

# Add node pool level exclusion (during creation)
gcloud container node-pools create NODE_POOL_NAME \
  --cluster CLUSTER_NAME \
  --zone ZONE \
  --add-maintenance-exclusion-until-end-of-support

# Add node pool level exclusion (existing pool)
gcloud container node-pools update NODE_POOL_NAME \
  --cluster CLUSTER_NAME \
  --zone ZONE \
  --add-maintenance-exclusion-until-end-of-support
```

## Rollback/Downgrade guidance

- **Control Plane Patches**: Can be downgraded by running the upgrade command with the target older patch version.
- **Control Plane Minors**: Rollback is only available during the first step of the 2-step upgrade process.
- **Node Pools (Minor & Patch)**: Can be downgraded directly by running the node pool upgrade command targeting the older version, OR by creating a new pool at the old version and migrating workloads (safer).

### Downgrade Control Plane (Patch or Step-1 Minor)
```bash
gcloud container clusters upgrade CLUSTER_NAME \
  --master \
  --zone ZONE \
  --cluster-version TARGET_PREVIOUS_VERSION
```

### Downgrade Node Pool (Direct)
```bash
gcloud container node-pools upgrade NODE_POOL_NAME \
  --cluster CLUSTER_NAME \
  --zone ZONE \
  --cluster-version TARGET_PREVIOUS_VERSION
```

### Downgrade Node Pool (Safe migration - recommended)
```bash
# Create replacement node pool at previous version
gcloud container node-pools create NODE_POOL_NAME-rollback \
  --cluster CLUSTER_NAME \
  --zone ZONE \
  --cluster-version PREVIOUS_VERSION \
  --num-nodes NUM_NODES \
  --machine-type MACHINE_TYPE

# Cordon old pool and migrate workloads
kubectl cordon -l cloud.google.com/gke-nodepool=NODE_POOL_NAME
```
