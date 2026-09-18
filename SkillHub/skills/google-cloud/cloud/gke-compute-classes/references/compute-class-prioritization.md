# ComputeClass: Prioritization, Logic & Fallbacks

## Traversal & Tie-Breaking

-   **Sequential:** Tried top-to-bottom. Unobtainable shapes get a **5-minute
    cooldown**. Max **~10 entries** (prevents infinite loops).
-   **Tie-break (No Score):** Top entry wins. If multiple shapes match one rule,
    lowest unit cost wins.
-   **Tie-break (`priorityScore`):** Int 1–1000 (Higher = Preferred). If one
    rule has a score, **all** must. Max **3 rules per score**. Tied rules
    evaluated together; lowest cost wins. (GKE 1.35.2+).
-   **Equal-Score Zonal Balancing (Round-Robin)**: Since GKE reservations are
    zonal, to achieve balanced scale-up across multiple zones (e.g.,
    `us-central1-a`, `b`, and `c`), you can define separate priority rules for
    each zone and assign them the **exact same `priorityScore`**. GKE will
    evaluate these tied zonal rules together, performing a round-robin selection
    to achieve roughly equal zonal distribution of nodes. Note that this
    requires using specific reservation names per zone.

## Fallback Patterns

Pattern        | Priority Order           | Rationale                                                                                   | Asset
-------------- | ------------------------ | ------------------------------------------------------------------------------------------- | -----
Inference      | Res -> OD -> DWS -> Spot | Accelerator node startup is slow. Avoid Spot preemption risk for latency-sensitive serving. | `genai-inference-g4-compute-class.yaml`
Prod Training  | Res -> DWS -> OD -> Spot | DWS wait acceptable. Spot preemption disruptive.                                            | `tpu-v5e-training-compute-class.yaml`
Dev Training   | Spot -> OD               | Spot for cost; OD floor unblocks dev.                                                       |
Cost Batch     | Spot -> OD               | Use `priorityScore` to pick cheapest Spot family.                                           | `spot-cost-tiebreak-compute-class.yaml`
Latency Hybrid | Manual -> Auto-creation  | Skip auto-creation delay by hitting warm pools.                                             | `manual-pool-tiebreak-compute-class.yaml`

## Key Rules

-   **No repetition:** Doesn't improve obtainability.
-   **Vary dimensions:** Zone, Family, Capacity (Spot/OD), **machine size
    (cores)**.
-   **Size obtainability (large shapes are scarce):** Shapes **>32 vCPU** draw
    from thinner capacity pools and hit `out.of.resources` stockouts far more
    than ≤32-core shapes. A ComputeClass pinned to large machines **only** has
    no escape hatch → `Pending`. Add **smaller-core fallback priorities** *if
    the workload allows it*. **Gate on Pod requests:** node auto-creation sizes
    nodes to Pod *requests*, so a single pod requesting >32 vCPU **cannot** land
    on a smaller node — only horizontally-scalable workloads (many small pods
    that bin-pack) benefit. For a genuinely large single pod, vary
    **zone/family** instead, not cores.
-   **Always include a floor:** End with high-availability OD (e.g., N4/E2) to
    prevent `Pending`.
-   **Stateful Gen Isolation:** For PV workloads, do NOT mix hardware
    generations (e.g., all Gen 4 OR all Gen 2) in `priorities[]`. Mixing causes
    Hyperdisk vs PD attachment failures. **Exception (GKE
    1.35.3-gke.1290000+):** with the built-in `dynamic-rwo` StorageClass (`type:
    dynamic` + `use-allowed-disk-topology: "true"`) the autoscaler scales up
    only disk-compatible nodes, so it skips the incompatible-generation priority
    instead of attach-failing — mixing generations is then safe.
-   **Mixed Architectures:** Mix ARM (`n4a`) and x86 (`n4`) in `priorities[]`.
    Autoscaler skips incompatible shapes based on Pod constraints. **Must use
    multi-platform image builds.**
-   **Spot Availability:** For CPU, if OD is out, Spot usually is too. For
    Accelerators, Spot often has capacity when OD doesn't.
