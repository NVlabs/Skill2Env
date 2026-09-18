# ComputeClass: Migrating from Karpenter

## Concept Mapping

| Karpenter             | GKE ComputeClass            | Note                   |
| --------------------- | --------------------------- | ---------------------- |
| `NodePool`            | `ComputeClass`              | Collapse multiple      |
:                       :                             : NodePools into         :
:                       :                             : `priorities[]`.        :
| `spec.weight`         | **Order in `priorities[]`** | Top wins. Strictly     |
:                       :                             : ordered traversal.     :
| `instance-family In   | `machineFamily: n4`         | GCP equivalents: `m6i` |
: [m6i]`                :                             : -> `n4`, `c6i` ->      :
:                       :                             : `c4`.                  :
| `capacity-type: spot` | `spot: true`                | Declare per priority.  |
| `consolidateAfter:    | `consolidationDelayMinutes: | Floor is 1 minute.     |
: 30s`                  : 1`                          :                        :
| `drift`               | `activeMigration: {         | Honors PDBs.           |
:                       : optimizeRulePriority\: true :                        :
:                       : }`                          :                        :
| `disruption.budgets`  | **PodDisruptionBudget       | Standard K8s resource. |
:                       : (PDB)**                     :                        :

## Family Translation (AWS -> GCP)

-   **General Purpose:** `m5/m6i` -> `n2 / n4`.
-   **Compute Optimized:** `c5/c6i` -> `c2 / c4`.
-   **AMD:** `m5a/m6a` -> `n2d / n4d`.
-   **ARM:** `c7g/m7g` -> `c4a / n4a`.
-   **Memory Optimized:** `r5/r6i` -> `n2-highmem / n4-highmem`.

## Key Behavioral Differences

-   **Fast-fail Traversal:** ComputeClass falls through to next priority
    immediately on failure. No probabilistic selection.
-   **Spec Changes:** Updating ComputeClass doesn't drift nodes automatically
    unless `activeMigration` is enabled.
-   **Drift Throttling:** GKE does not have a global drift delay (like
    'consolidateAfter'). You must use PDBs on your deployments to throttle
    activeMigration (drift) rates.
-   **Spot vs OD:** On GCP, Spot/OD often share capacity for CPU. Always include
    an OD floor.
-   **No Topology in ComputeClass:** Set `topologySpreadConstraints` on the Pod,
    not the ComputeClass.
-   **`whenUnsatisfiable`:** Karpenter's "any VM" doesn't match GKE's
    `ScaleUpAnyway` (which picks E2). Use `DoNotScaleUp` and accept `Pending`.

## Sharp Edge: translate Pod selectors to GKE-native labels

The #1 post-migration trap. Karpenter/EKS Pod `nodeSelector`/affinity uses
AWS-style or generic keys that GKE's autoscaler does **not** recognize — the Pod
stays `Pending` with `noScaleUp` (no priority matches).

-   **Machine family:** generic `machine-family: c4` → GKE
    `cloud.google.com/machine-family: c4`.
-   **Machine shape/type:** AWS `node.kubernetes.io/instance-type: m6i.4xlarge`
    → GKE shape `node.kubernetes.io/instance-type: n4-standard-16` (both keys
    are real: `cloud.google.com/machine-family` = family,
    `node.kubernetes.io/instance-type` = shape).
-   **Better:** drop the node-label selector entirely and select the
    ComputeClass — `nodeSelector: { cloud.google.com/compute-class: <NAME> }` —
    letting `priorities[]` choose the family/shape.
-   **GPU Pods:** also add the GPU toleration (`nvidia.com/gpu: Exists`) — GKE
    auto-taints GPU nodes; missing it is another common `noScaleUp` cause (see
    SKILL CRITICAL GPU-TAINT RULE).
