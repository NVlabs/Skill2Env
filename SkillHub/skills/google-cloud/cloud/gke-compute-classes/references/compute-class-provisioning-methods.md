# ComputeClass: Provisioning Methods & Binding

## node pool auto-creation vs. Manual Node Pools

| Method          | Description                      | Pinning via `nodepools` |
| --------------- | -------------------------------- | ----------------------- |
| **node pool     | Autoscaler creates/deletes pools | ❌ (Ephemeral names)     |
: auto-creation** : dynamically at the ComputeClass  :                         :
:                 : level. **Does NOT require        :                         :
:                 : cluster-level Node Auto          :                         :
:                 : Provisioning.**                  :                         :
| **Manual**      | Pre-provisioned by admin. Faster | ✅ (Stable names)        |
:                 : scheduling.                      :                         :

1.  Node pool is a GKE API resource, not a Kubernetes CRD.
2.  On regional clusters, auto-created node pools are regional by default
3.  No way to set a prefix or custom name for auto-created node pools

### Custom Node Initialization

ComputeClass node pool auto-creation dynamically manages nodes and **does not
natively support custom UserData or startup scripts** via the `nodePoolConfig`.
To initialize nodes:

1.  **Privileged DaemonSets (Recommended):** Deploy a DaemonSet with an
    `initContainer` to perform host-level setup or install proprietary
    monitoring agents.
2.  **Custom OS Images:** GKE supports custom OS images via the
    [gke-custom-image-builder](https://github.com/GoogleCloudPlatform/gke-custom-image-builder-cos)
    (Private preview; contact account team), though DaemonSets are the primary
    K8s-native workaround.

### Hybrid Strategy

Put manual pools at the top for zero-latency scheduling; use node pool
auto-creation fallbacks below for infinite scale.

## Stateful Workloads & Storage

For Zonal PVs, use `volumeBindingMode: WaitForFirstConsumer` in the
`StorageClass` to avoid cross-zone deadlocks between disks and autoscaled nodes.

**Recommended (GKE 1.35.3-gke.1290000+): the built-in `dynamic-rwo`
StorageClass** (`type: dynamic`, `pd-type: pd-balanced`, `hyperdisk-type:
hyperdisk-balanced`, `use-allowed-disk-topology: "true"`).
`use-allowed-disk-topology` makes the **Cluster Autoscaler disk-topology-aware**
— it reads the workload's disk requirements and scales up **only disk-compatible
node options** ("machine serenity"), skipping incompatible-generation priorities
instead of provisioning a node that then fails PV attach. This is what lets a
stateful ComputeClass keep a broad `priorities[]` fallback list across machine
families/generations safely (see
[Gen Isolation exception](./compute-class-prioritization.md)). Built-in on
supported clusters (reference by name; no need to create); asset
`dynamic-rwo-storageclass.yaml` documents its contents. NOTE: this is the
**data-PV StorageClass**, distinct from `priorities[].storage.bootDiskType` (the
node boot disk).

## Intent-based vs. Strict Configuration

-   **Intent-based (Preferred):** `machineFamily: n4`, `minCores: 16`. Allows
    GKE to find best-fit shape or substitute families.
-   **Strict:** `machineType: n4-standard-16`. Pins to exact SKU.

## Binding Manual Pools to ComputeClass

Manual pools must be labeled/tainted to be eligible for a ComputeClass (unless
it's the cluster default).

```bash
gcloud container node-pools update <POOL> \
    --node-labels="cloud.google.com/compute-class=<CLASS-NAME>" \
    --node-taints="cloud.google.com/compute-class=<CLASS-NAME>:NoSchedule"
```

When using node pool auto-creation, ComputeClasses auto-tolerate these taints;
workloads do **not** need matching tolerations.

## Default Class Selection

-   **Cluster Default:** Create ComputeClass named `default` + enable feature on
    cluster.
-   **Namespace Default:** Label NS
    `cloud.google.com/default-compute-class=<name>`.
-   **Workload Selection:** `nodeSelector: cloud.google.com/compute-class:
    <name>`.

## Integration with Kueue (Batch/Job Queuing)

For AI/ML batch workloads, use **Kueue** to manage quotas and job admission,
while relying on **ComputeClasses** to handle hardware provisioning (fallback
routing between Spot, DWS, and On-Demand).

To map a Kueue `ResourceFlavor` to a ComputeClass, use the node label in the
flavor definition:

```yaml
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: "ccc-flavor"
spec:
  nodeLabels:
    cloud.google.com/compute-class: "your-compute-class-name"
```

When Kueue admits the job, it automatically injects this `nodeSelector` into the
Pod. The GKE Autoscaler will then provision hardware according to the
ComputeClass's prioritized fallback list.
