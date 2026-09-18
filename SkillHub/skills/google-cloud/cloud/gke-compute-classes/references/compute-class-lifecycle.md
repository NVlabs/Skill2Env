# ComputeClass: Lifecycle, Drift & Updates

## Consolidation (Scale-down)

Controlled via `spec.autoscalingPolicy`.

-   `consolidationDelayMinutes`: Floor is **1 minute**.
-   `consolidationThreshold`: CPU utilization % (0 = always candidate).
-   `gpuConsolidationThreshold`: Accelerator utilization %.
-   *Note:* Maintenance windows do **not** block consolidation. Use PDBs to
    suppress disruption.
-   *Blockers:* Local storage, 'safe-to-evict: false', and bare pods block
    scale-down. **DaemonSets do NOT block scale-down by default.** If empty
    nodes aren't scaling down, look for other blocking system pods.
-   **System Pod Segregation**: Since non-DaemonSet system pods (e.g., in
    `kube-system` namespace) often have tight PDBs or single replicas that block
    scale-down, **always recommend segregating system pods into a dedicated
    system ComputeClass/node pool** (using `system-pool-compute-class.yaml`).
    This isolates the system pods and keeps them from blocking the consolidation
    of Spot/workload nodes.

## ActiveMigration (Drift)

Reconciles pods back to higher-priority rules (similar to Karpenter drift).

-   `optimizeRulePriority: true`: Enables the drift controller.
-   **Disruption:** Honors PDBs (Voluntary disruption). Without a PDB, eviction
    is uncontrolled.
-   **Warning:** `maxUnavailable: 0` PDBs permanently block Active Migration.
-   **Trigger:** Higher-priority capacity becomes available.

> **CRITICAL K8S DISTINCTION:** PDBs and `safe-to-evict: false` ONLY protect
> against *voluntary* disruptions (ActiveMigration, scale-down, upgrades). They
> **DO NOT** prevent *involuntary* Spot VM preemptions. Spot nodes can be
> reclaimed at any time, regardless of PDBs.

## Updating a ComputeClass

-   **No Retroactive Change:** Updating a ComputeClass does **not** change
    existing nodes.
-   **New Nodes Only:** Only nodes created after the update use the new spec.
-   **Drift Behavior:**
    -   *Without ActiveMigration:* Old-spec nodes persist until rescheduled
        (rollout, drain, preemption).
    -   *With ActiveMigration:* Controller drifts pods toward nodes matching the
        updated (higher-priority) spec.
-   **Disruption-Sensitive:** For training/stateful roles, schedule updates for
    maintenance windows or drain manually.
