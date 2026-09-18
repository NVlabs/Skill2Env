# Troubleshooting GKE Upgrade Issues

## Diagnostic flowchart

## Table of Contents
- [Diagnostic flowchart](#diagnostic-flowchart) (Line 3-17)
- [1. PDB blocking drain (most common)](#1-pdb-blocking-drain-most-common) (Line 18-40)
- [2. Resource constraints (no room for pods)](#2-resource-constraints-no-room-for-pods) (Line 41-61)
- [3. Bare pods blocking drain](#3-bare-pods-blocking-drain) (Line 62-71)
- [4. Admission webhooks rejecting pod creation](#4-admission-webhooks-rejecting-pod-creation) (Line 72-88)
- [5. PVC attachment issues](#5-pvc-attachment-issues) (Line 89-98)
- [6. Long termination grace periods](#6-long-termination-grace-periods) (Line 99-108)
- [7. Upgrade operation stuck at GKE level](#7-upgrade-operation-stuck-at-gke-level) (Line 109-117)
- [8. Stockout during critical upgrades (e.g. cert expiration)](#8-stockout-during-critical-upgrades-eg-cert-expiration) (Line 118-148)
- [9. GPU node upgrade regressions (CrashLoopBackOff, driver issues)](#9-gpu-node-upgrade-regressions-crashloopbackoff-driver-issues) (Line 149-187)
- [Validation after applying a fix](#validation-after-applying-a-fix) (Line 188-200)

When an upgrade is stuck or failing, work through these checks in order. Each section has the diagnosis command, what to look for, and the fix.

## 1. PDB blocking drain (most common)

**Diagnose:**
```bash
kubectl get pdb -A -o wide
# Look for ALLOWED DISRUPTIONS = 0
kubectl describe pdb PDB_NAME -n NAMESPACE
```

**Fix — temporarily relax the PDB:**
```bash
# Option A: Allow all disruptions temporarily
kubectl patch pdb PDB_NAME -n NAMESPACE \
  -p '{"spec":{"minAvailable":null,"maxUnavailable":"100%"}}'

# Option B: Back up and edit
kubectl get pdb PDB_NAME -n NAMESPACE -o yaml > pdb-backup.yaml
# Edit minAvailable/maxUnavailable, then:
kubectl apply -f pdb-backup.yaml
```

Restore original PDB after upgrade completes.

## 2. Resource constraints (no room for pods)

**Diagnose:**
```bash
kubectl get pods -A | grep Pending
kubectl get events -A --field-selector reason=FailedScheduling
kubectl top nodes
kubectl describe nodes | grep -A 5 "Allocated resources"
```

**Fix — increase surge capacity:**
```bash
gcloud container node-pools update NODE_POOL_NAME \
  --cluster CLUSTER_NAME \
  --zone ZONE \
  --max-surge-upgrade 2 \
  --max-unavailable-upgrade 0
```

Or scale down non-critical workloads temporarily.

## 3. Bare pods blocking drain

**Diagnose:**
```bash
kubectl get pods -A -o json | \
  jq -r '.items[] | select(.metadata.ownerReferences | length == 0) | "\(.metadata.namespace)/\(.metadata.name)"'
```

**Fix:** Delete bare pods (they won't reschedule anyway) or wrap in Deployments.

## 4. Admission webhooks rejecting pod creation

**Diagnose:**
```bash
kubectl get validatingwebhookconfigurations
kubectl get mutatingwebhookconfigurations
# Check for webhooks matching broad API groups
kubectl describe validatingwebhookconfigurations WEBHOOK_NAME
```

**Fix — temporarily disable problematic webhook:**
```bash
# Add failure policy annotation or delete temporarily
kubectl delete validatingwebhookconfigurations WEBHOOK_NAME
# Re-create after upgrade
```

## 5. PVC attachment issues

**Diagnose:**
```bash
kubectl get pvc -A | grep -v Bound
kubectl get events -A --field-selector reason=FailedAttachVolume
```

**Fix:** Check if volumes are zone-locked. For regional clusters, PVs may need to be in the same zone as the new node. Consider migrating workloads to already-upgraded nodes.

## 6. Long termination grace periods

**Diagnose:**
```bash
kubectl get pods -A -o json | \
  jq '.items[] | select(.spec.terminationGracePeriodSeconds > 120) | {ns:.metadata.namespace, name:.metadata.name, grace:.spec.terminationGracePeriodSeconds}'
```

**Fix:** Reduce `terminationGracePeriodSeconds` in the workload spec if possible. GKE waits up to 1 hour for pod eviction during surge upgrades.

## 7. Upgrade operation stuck at GKE level

**Diagnose:**
```bash
gcloud container operations list --cluster CLUSTER_NAME --zone ZONE --filter="operationType=UPGRADE_NODES"
```

**Fix:** If the operation shows no progress for >2 hours after resolving pod-level issues, contact GKE support with cluster name, zone, and operation ID.

## 8. Stockout during critical upgrades (e.g. cert expiration)

**Diagnose:**
Upgrade is failing with `ZONE_RESOURCE_POOL_EXHAUSTED` or `QUOTA_EXCEEDED` errors, and the cluster has a critical pending deadline (e.g., control plane certificate expiring soon).

**Fix:**
1. **Change Upgrade Strategy**: Modify the node pool to use a rolling in-place upgrade (no surge) to bypass quota limits:
   ```bash
   gcloud container node-pools update NODE_POOL_NAME \
     --cluster CLUSTER_NAME \
     --zone ZONE \
     --max-surge-upgrade 0 \
     --max-unavailable-upgrade 1
   ```
2. **Open Support Case**: Immediately open a P1/P2 Google Cloud Support case, citing urgent certificate expiration and stockout.
3. **Retry in Different Zone/Region**: If the cluster is regional or multi-zonal, check if you can retry the upgrade in a different zone that might have capacity, or add a temporary node pool in a different zone/region to migrate workloads.
4. **Credential Rotation**: Perform a control plane credential rotation to renew certificates without upgrading the GKE version.
   ```bash
   gcloud container clusters update CLUSTER_NAME --start-credential-rotation --zone ZONE
   # Follow standard GKE documentation to complete the rotation.
   ```
5. **Enable DNS Endpoint**: If client connectivity is failing or at risk due to expired client certificates, enable the DNS-based control plane endpoint to allow IAM-based authentication.
   ```bash
   gcloud container clusters update CLUSTER_NAME --enable-dns-access --zone ZONE
   # Get credentials using DNS endpoint:
   gcloud container clusters get-credentials CLUSTER_NAME --dns-endpoint --zone ZONE
   ```

## 9. GPU node upgrade regressions (CrashLoopBackOff, driver issues)

**Diagnose:**
GPU nodes upgrade successfully, but ML pods are stuck in `CrashLoopBackOff` with `SIGSEGV` or driver initialization errors.

1. **Compare Node Metadata**: Check if the OS image, kernel version (`uname -r`), or NVIDIA driver version changed and differs between working (old) and non-working (new) nodes.
2. **Verify Driver Installer Logs**: Check logs of the `nvidia-driver-installer` container in the `nvidia-gpu-device-plugin` pod on the new node.
3. **Test GPU Access**: Deploy a simple test pod to verify if the GPU is accessible with the current driver:
   ```yaml
   apiVersion: v1
   kind: Pod
   metadata:
     name: gpu-test-vectoradd
   spec:
     containers:
     - name: vectoradd
       image: nvidia/samples:vectoradd-cuda11.6.0
       resources:
         limits:
           nvidia.com/gpu: 1
     restartPolicy: Never
   ```

**Fix:**
1. **Pin Driver Version**: If the default driver version changed, update your node pool configuration to pin to the previous working driver version (e.g., `R535`):
   ```bash
   gcloud container node-pools update NODE_POOL_NAME \
     --cluster CLUSTER_NAME \
     --zone ZONE \
     --accelerator type=GPU_TYPE,count=COUNT,gpu-driver-version=DRIVER_VERSION
   ```
2. **Update Workload Dependencies**: Rebuild container images with a CUDA version compatible with the new driver.
3. **Rollback Node Pool**: If production is blocked, roll back the node pool to the previous GKE version:
   ```bash
   gcloud container node-pools upgrade NODE_POOL_NAME \
     --cluster CLUSTER_NAME \
     --zone ZONE \
     --cluster-version PREVIOUS_VERSION
   ```

## Validation after applying a fix

```bash
# Monitor node upgrade progress
watch 'kubectl get nodes -o wide | grep -E "NAME|CURRENT_VERSION|TARGET_VERSION"'

# Check no pods stuck
kubectl get pods -A | grep -E "Terminating|Pending"

# Confirm upgrade resuming
gcloud container operations list --cluster CLUSTER_NAME --zone ZONE --limit=1
```
