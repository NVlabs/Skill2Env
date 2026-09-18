# Automatic Rebalancing Strategy

**Status**: ✅ PRODUCTION READY

**Purpose**: AI-driven rebalancing where user explains high-level goals (CPU balance, memory optimization, drain node, etc.) and AI generates optimal rebalance plan. User can modify or approve plan before execution.

---

## When to Use Automatic Mode

Use this mode when the user wants:
- AI to analyze cluster and propose optimal rebalancing
- High-level goal specification (balance CPU, optimize memory, drain node)
- Expert recommendations with ability to customize
- Multi-objective optimization (CPU AND memory simultaneously)
- Intelligent rebalance planning without manual VM-by-node decisions

**User Request Patterns:**
- "Rebalance VMs based on CPU load"
- "Optimize cluster for CPU and memory"
- "Drain worker-02 for maintenance"
- "Automatically balance the cluster"
- "Help me redistribute VMs to improve performance"
- "Optimize VM placement"

**Do NOT use Automatic mode when:**
- User specifies exact VM→node mappings → Use Manual mode
- User only wants to see available VMs → Use `/vm-inventory` skill

---

## Workflow

### Step 1: Gather Cluster State and Determine Optimization Goal

**1.1 Collect Cluster Information**

**List all VMs across namespaces:**

**MCP Tool**: `resources_list` (from openshift-virtualization)

**Parameters**:
```json
{
  "apiVersion": "kubevirt.io/v1",
  "kind": "VirtualMachine"
}
```

Extract for each VM:
- Name, namespace
- Current node placement (from VirtualMachineInstance if running)
- Resource requests (CPU, memory)
- Storage type (RWX vs RWO) - determines live vs cold migration capability

**List all nodes:**

**MCP Tool**: `resources_list` (from openshift-virtualization)

**Parameters**:
```json
{
  "apiVersion": "v1",
  "kind": "Node"
}
```

Extract for each node:
- Name, status (Ready/NotReady)
- Capacity and allocatable resources
- Current utilization
- Taints and labels
- Schedulable status (not cordoned)

**Gather resource usage metrics:**

**MCP Tool**: `nodes_top` (from openshift-virtualization)

**Parameters**: None (lists all nodes)

Extract current CPU and memory utilization for each node.

**MCP Tool**: `pods_top` (from openshift-virtualization)

**Parameters**:
```json
{
  "all_namespaces": true,
  "label_selector": "kubevirt.io=virt-launcher"
}
```

Extract current CPU and memory usage for each VM.

---

**1.2 Determine Optimization Goal from User Request**

**Analyze user's language to infer goal:**

| User Phrase | Optimization Goal | Metrics to Optimize |
|-------------|-------------------|---------------------|
| "balance CPU", "CPU load" | Balance CPU utilization | Minimize CPU variance across nodes |
| "optimize memory", "memory pressure" | Balance memory utilization | Minimize memory variance across nodes |
| "balance cluster", "rebalance", "optimize" | Multi-objective (CPU + memory) | Minimize both CPU and memory variance |
| "drain worker-02", "evacuate node-X" | Drain specific node | Migrate all VMs off target node |
| "optimize performance" | Performance optimization | Balance resources + avoid hotspots |
| "distribute VMs evenly" | VM count distribution | Equal number of VMs per node |

**If goal is ambiguous**, ask user to clarify:

```
I can optimize the cluster for several goals:
1. **CPU load balancing** - Distribute CPU usage evenly across nodes
2. **Memory load balancing** - Distribute memory usage evenly across nodes
3. **Both CPU and memory** - Multi-objective optimization
4. **Drain specific node** - Move all VMs off a node for maintenance
5. **VM count distribution** - Equal number of VMs per node

Which optimization goal would you like me to pursue?
```

**WAIT for user response** before proceeding.

---

**1.3 Support Multi-Objective Optimization**

When user requests multiple goals (e.g., "balance CPU and memory"):

**Approach:**
1. **Calculate scoring function** combining all objectives
2. **Weight objectives** (can ask user for priorities or use defaults)
3. **Find rebalance plan** that optimizes combined score

**Example Scoring:**
```
Score = (0.5 × CPU_variance_reduction) + (0.5 × Memory_variance_reduction)
```

**User can adjust weights** if AI proposes alternative approach:

```
I can optimize for:
- Equal priority: CPU 50%, Memory 50%
- CPU-focused: CPU 70%, Memory 30%
- Memory-focused: CPU 30%, Memory 70%

Would you like to adjust priorities, or proceed with equal weighting?
```

---

### Step 2: Analyze and Generate Optimal Migration Plan

**2.1 Identify Migration Candidates**

For each optimization goal:

**CPU Balancing:**
- Identify overloaded nodes (>80% CPU)
- Identify underloaded nodes (<50% CPU)
- Select VMs to migrate from overloaded to underloaded nodes

**Memory Balancing:**
- Identify nodes with high memory pressure (>85%)
- Identify nodes with low memory usage (<50%)
- Select VMs to migrate for better distribution

**Node Drain:**
- Select ALL VMs currently on target node
- Find suitable destination nodes with capacity

**Performance Optimization:**
- Identify VMs with high resource variance (bursty workloads)
- Distribute high-performance VMs across different nodes
- Avoid co-locating resource-intensive VMs

**2.2 Apply Constraints and Validation**

For each candidate migration, check:

**Storage Compatibility** (see SKILL.md - Common Validation Logic):
- RWX storage → Live migration possible
- RWO storage → Cold migration required
- Stopped VM → Cold migration required

**Target Node Capacity:**
- Verify target has sufficient CPU and memory
- Account for VM resource requests
- Ensure node is Ready and schedulable

**Taints and Tolerations:**
- Check target node for taints
- Verify VM has matching tolerations
- If mismatch, skip that target or propose adding tolerations

**Concurrency Limits** (see [references/performance-tuning.md](./references/performance-tuning.md)):
- Cluster limit: 5 concurrent migrations (default)
- Per-node limit: 2 outbound migrations (default)
- Plan migration batches respecting limits

**Network Bandwidth:**
- Avoid saturating network with too many concurrent large VM migrations
- Consider VM memory size when scheduling concurrent migrations

**2.3 Optimize Migration Plan**

**Migration Ordering Strategy:**

1. **Smallest VMs first** - Faster migrations, higher success rate
2. **Live migrations before cold** - Minimize total downtime
3. **Group by source node** - Efficient for node draining
4. **Respect dependencies** - Avoid migrating related VMs simultaneously (e.g., database + app tier)

**Expected Improvement Calculation:**

**Before migration:**
```
CPU variance = StdDev([worker-01: 85%, worker-02: 78%, worker-03: 42%, worker-04: 38%])
            = 22.1%
```

**After migration:**
```
CPU variance = StdDev([worker-01: 65%, worker-02: 58%, worker-03: 62%, worker-04: 55%])
            = 4.2%
```

**Improvement:**
```
Variance reduction: 22.1% → 4.2% = 81% improvement
```

---

### Step 3: Present Plan to User with Modification Options

**CRITICAL**: Use the **Common Plan Visualization** format defined in SKILL.md.

**Reference**: [SKILL.md - Common Plan Visualization](./SKILL.md#common-plan-visualization)

**Present the plan with:**
1. **Optimization Goal** statement
2. **VM Rebalance Plan** table (from SKILL.md common format)
3. **Node State: Before → After** table (from SKILL.md common format)
4. **Key Improvement** summary line
5. **Migration Summary** (for batch operations)
6. **Risks & Considerations** (optional)
7. **User options** (approve / modify / explain / cancel)

**Additional context for automatic mode:**
- State the optimization goal clearly (CPU balance, memory balance, multi-objective, node drain, etc.)
- Include expected improvements with metrics (variance reduction, capacity headroom, etc.)
- Offer modification options (skip, change target, reorder)
- Allow user to explain reasoning for specific migrations

**CRITICAL: WAIT for user response before executing.**

---

**3.1 Handle User Modifications**

If user selects **"modify"**, enter interactive modification mode:

**Example Interaction:**

```
User: "modify"

Agent: "Which migrations would you like to modify?"

Options:
- "skip <#>" - Remove migration from plan (e.g., "skip 5")
- "change target <#> to <node>" - Change destination (e.g., "change target 1 to worker-04")
- "reorder" - Change execution order
- "done" - Finish modifications and execute

User: "skip 5"

Agent: "Migration #5 (app-vm-05) removed from plan. Updated plan:"

## Updated Rebalancing Plan

**Proposed Migrations:** (Now 4 migrations)

| # | VM | Current Node | Target Node | Type | Impact |
|---|----|--------------|-------------|------|--------|
| 1 | database-01 | worker-01 | worker-03 | live | <1s |
| 2 | web-server-02 | worker-01 | worker-04 | live | <1s |
| 3 | cache-vm | worker-02 | worker-04 | live | <1s |
| 4 | api-gateway | worker-02 | worker-03 | live | <1s |

**Updated Expected Improvements:**
- CPU variance: 22.1% → 5.8% (74% improvement)
- Memory variance: 11.8% → 8.1% (31% improvement)

**Ready to execute?** (approve / modify more / cancel)

User: "approve"

Agent: [Proceeds to Step 4 - Execution]
```

---

**3.2 AI Proposes Better Approach (If Detected)**

If AI detects a potentially better strategy, propose alternative:

```
💡 **Alternative Approach Detected**

I notice that migrating app-vm-05 via cold migration will cause 40s downtime. However, I found:
- app-vm-05 is currently stopped (not running)
- Moving it now via cold migration has **zero additional downtime** since it's already offline

**Alternative proposal:**
Include app-vm-05 in the plan (no additional impact vs current state)

Would you like to:
- **accept alternative** - Include app-vm-05 in plan
- **keep original** - Proceed with current plan
- **explain more** - Tell me more about this alternative
```

**User has final word** - If user prefers original plan, execute original plan.

---

### Step 4: Validate All VMs Before Execution

**BEFORE executing any migration**, validate ALL VMs in the plan:

**For each VM**, perform **Common Validation Logic from SKILL.md**:

1. **Verify VM exists** (see SKILL.md - Validation 1)
2. **Check current location** (see SKILL.md - Validation 2)
3. **Validate storage compatibility** (see SKILL.md - Validation 3)
4. **Verify target node exists** (see SKILL.md - Validation 4)

**If any VM fails validation:**
- Remove from rebalance plan
- Warn user: "Migration #X (vm-name) failed validation: [reason]. Proceeding with remaining migrations."
- Continue with other migrations

**Reference**: [SKILL.md - Common Validation Logic](./SKILL.md#common-validation-logic)

---

### Step 5: Execute Migrations with Progress Reporting

**5.1 Group Migrations by Type**

**Live Migrations** (execute first):
- Can run concurrently (up to cluster limits)
- Lower risk, zero downtime
- Follow live migration workflow from REBALANCE_MANUAL.md

**Cold Migrations** (execute after live migrations):
- Run sequentially (to prevent cascading failures)
- Higher risk, has downtime
- Follow cold migration workflow from REBALANCE_MANUAL.md

**5.2 Respect Concurrency Limits**

**Cluster-wide limit**: 5 concurrent migrations (default)
**Per-node limit**: 2 outbound migrations per source node (default)

**Monitor current migrations:**

**MCP Tool**: `resources_list` (from openshift-virtualization)

**Parameters**:
```json
{
  "apiVersion": "kubevirt.io/v1",
  "kind": "VirtualMachineInstanceMigration"
}
```

Count migrations where `.status.phase` is NOT "Succeeded" or "Failed".

**Wait if at limit** before starting new migrations.

**Reference**: [references/performance-tuning.md](./references/performance-tuning.md#concurrency-limits-tuning)

---

**5.3 Execute Each Migration**

**For Live Migrations:**

**Create VirtualMachineInstanceMigration:**

**MCP Tool**: `resources_create_or_update` (from openshift-virtualization)

**Parameters**:
```json
{
  "resource": "apiVersion: kubevirt.io/v1\nkind: VirtualMachineInstanceMigration\nmetadata:\n  name: migrate-<vm-name>-<timestamp>\n  namespace: <namespace>\nspec:\n  vmiName: <vm-name>"
}
```

**Monitor migration progress:**

Poll using `resources_get` for VirtualMachineInstanceMigration, checking `.status.phase`:
- Pending → Scheduling → PreparingTarget → Running → Succeeded

**For Cold Migrations:**

Follow cold migration workflow from REBALANCE_MANUAL.md:
1. Stop VM using `vm_lifecycle` (action: stop) and wait for completion
2. Re-read VM using `resources_get` for fresh resourceVersion
3. Update VM nodeAffinity to target node
4. Start VM using `vm_lifecycle` (action: start)
5. Verify VM reached target node

**Reference**: [REBALANCE_MANUAL.md - Cold Migration Workflow](./REBALANCE_MANUAL.md)

---

**5.4 Report Progress Incrementally**

After each migration completes:

```markdown
## Automatic Rebalancing in Progress

**Status:** 2/4 migrations complete

✓ **database-01**: Migrated to worker-03 (live, 42s)
✓ **web-server-02**: Migrated to worker-04 (live, 38s)
⏳ **cache-vm**: Migrating to worker-04 (live, in progress - 15s elapsed)
⏸️ **api-gateway**: Pending (waiting for cache-vm to complete)

**Estimated time remaining:** 2-3 minutes
```

Update after each completion/start.

---

**5.5 Error Handling During Execution**

**On first failure:**

1. **Stop remaining migrations** (do not continue blindly)
2. **Report detailed status**:

```markdown
## ⚠️ Rebalancing Paused - Migration Failed

**Status:** 2/4 successful, 1 failed, 1 not attempted

**Successful:**
- ✓ database-01: Migrated to worker-03 (live, 42s)
- ✓ web-server-02: Migrated to worker-04 (live, 38s)

**Failed:**
- ❌ cache-vm: Migration timeout (VM memory write rate too high)

**Not Attempted:**
- ⏸️ api-gateway: Skipped due to previous failure

**Troubleshooting:**

Migration timeout typically occurs when:
- VM has high memory write rate (database, caching workload)
- Network bandwidth insufficient for transfer speed
- VM memory size very large (>32GB)

**Recommendations:**
1. Reduce workload on cache-vm and retry
2. Use cold migration for cache-vm (will have ~30-60s downtime)
3. Check network bandwidth availability

**How would you like to proceed?**
- **retry** - Retry failed migration with same settings
- **retry cold** - Retry using cold migration instead
- **skip** - Skip cache-vm and continue with api-gateway
- **abort** - Stop rebalancing, leave cluster in current state
```

3. **Wait for user decision** before proceeding

**Reference**: [SKILL.md - Common Error Handling](./SKILL.md#common-error-handling)

---

### Step 6: Report Final Results

**On Complete Success:**

```markdown
## ✓ Automatic Rebalancing Complete

**All migrations successful!**

**Executed Migrations:**

| VM | From | To | Type | Duration | Status |
|----|------|----|----|----------|--------|
| database-01 | worker-01 | worker-03 | live | 42s | ✓ Success |
| web-server-02 | worker-01 | worker-04 | live | 38s | ✓ Success |
| cache-vm | worker-02 | worker-04 | live | 35s | ✓ Success |
| api-gateway | worker-02 | worker-03 | live | 41s | ✓ Success |

**Cluster State: Before → After**

| Node | CPU Before | CPU After | Change | Memory Before | Memory After | Change |
|------|------------|-----------|--------|---------------|--------------|--------|
| worker-01 | 85% | 68% | -17% ✓ | 72% | 59% | -13% ✓ |
| worker-02 | 78% | 58% | -20% ✓ | 65% | 52% | -13% ✓ |
| worker-03 | 42% | 62% | +20% | 48% | 61% | +13% |
| worker-04 | 38% | 55% | +17% | 51% | 63% | +12% |

**Improvements Achieved:**
- ✓ **CPU load balanced**: All nodes within 10% variance (was 22.1%)
- ✓ **Memory balanced**: All nodes within 8% variance (was 11.8%)
- ✓ **No node exceeding 70% utilization** (was 85% max)
- ✓ **Cluster capacity headroom**: 41% average (was 28%)
- ✓ **Total execution time**: 2 minutes 36 seconds

**Next Steps:**
- Monitor cluster for 24-48 hours to ensure sustained improvement
- Consider removing nodeAffinity constraints (if added) for long-term flexibility
- Use `/vm-inventory` to verify all VMs are healthy

Cluster is now optimally balanced. No further action needed.
```

**On Partial Success:**

Display similar format but include:
- Which migrations succeeded
- Which failed (with error details and troubleshooting)
- Which were not attempted (and why)
- Current cluster state vs target
- Recommendations for completing rebalancing

---

## Advanced Features

### Intelligent Workload Analysis

**Categorize VMs by workload type** (see [references/production-considerations.md](./references/production-considerations.md)):

- **Database** (high dirty page rate) → Schedule during low-activity window, consider cold migration
- **Web servers** (low dirty page rate) → Safe for concurrent live migration
- **Caching** (very high dirty page rate) → Migrate during idle or use cold migration
- **Batch processing** → Migrate during job idle periods

**Use workload characteristics** to optimize migration scheduling.

### Network Bandwidth Awareness

**Monitor network saturation:**

**MCP Tool**: `nodes_stats_summary` (from openshift-virtualization)

**Parameters**:
```json
{
  "name": "<node-name>"
}
```

Review `.network.interfaces[].rxBytes` and `.network.interfaces[].txBytes`.

**If saturation detected** (>80% utilization):
- Reduce concurrent migrations
- Set bandwidth limits per migration
- Suggest dedicated migration network

**Reference**: [references/live-migration-best-practices.md#dedicated-migration-network](./references/live-migration-best-practices.md#dedicated-migration-network-production-best-practice)

### Multi-Constraint Optimization

**Consider additional constraints:**
- **Anti-affinity rules**: Don't co-locate VMs with same label
- **Topology spread**: Distribute VMs across zones/racks
- **Resource quotas**: Respect namespace limits
- **Custom scheduling**: Honor existing nodeSelector/tolerations

**If conflicts detected**, explain to user and suggest resolution.

---

## Human-in-the-Loop Requirements

**CRITICAL: This mode requires user approval at multiple points.**

### 1. Goal Clarification (if ambiguous)
- Present optimization options
- Wait for user to select goal
- Do NOT proceed with assumptions

### 2. Plan Approval (MANDATORY)
- Display complete rebalance plan
- Show expected impact and improvements
- Offer modification options
- **REQUIRE explicit approval** ("approve", "yes", "execute")
- **NEVER execute without approval**

### 3. Plan Modification (if requested)
- Allow user to skip migrations
- Allow changing target nodes
- Allow reordering
- Recalculate expected improvements
- Present updated plan for approval

### 4. Error Handling (on failure)
- Stop execution immediately
- Report failure details
- Ask user how to proceed
- **Do NOT continue without user decision**

### 5. Alternative Proposals (if AI detects better approach)
- Present alternative with rationale
- Show comparison vs original plan
- **User chooses** - execute user's preference

**Rationale**: User maintains control over cluster changes while benefiting from AI's analytical capabilities.

---

## Safety Considerations

**Automatic mode involves batch operations with higher complexity:**

**Risks:**
- ⚠️ Multiple concurrent migrations can saturate network
- ⚠️ Batch failures can compound
- ⚠️ Wrong optimization goal can worsen cluster state
- ⚠️ User must understand multi-VM impact

**Mitigations:**
- ✓ Require explicit plan approval before execution
- ✓ Allow plan modification before execution
- ✓ Stop on first failure (no blind continuation)
- ✓ Respect cluster concurrency limits
- ✓ Validate all VMs before starting any migration
- ✓ Detailed progress reporting with errors
- ✓ Clear troubleshooting guidance

**Best Practices:**
- Start with dev/test clusters to learn behavior
- Use during maintenance windows for production
- Monitor network bandwidth during migrations
- Have rollback plan for critical workloads
- Consider snapshots before risky migrations (use `/vm-snapshot-create`)

**Reference**: [references/anti-patterns.md](./references/anti-patterns.md)

---

## Example Usage

### Example 1: Multi-Objective Optimization

```
User: "Rebalance VMs to optimize both CPU and memory"

Agent: [Loads REBALANCE_AUTOMATIC.md]
       [Gathers cluster state: VMs, nodes, metrics]
       [Determines goal: Multi-objective (CPU + memory)]
       [Analyzes and generates plan]

## Automatic Rebalancing Plan

**Optimization Goal:** Balance CPU and memory load across cluster

[Displays plan with 5 migrations]
[Shows current state, proposed migrations, expected improvements]

**How would you like to proceed?**
Options: approve | modify | explain <#> | cancel

User: "approve"

Agent: [Validates all VMs]
       [Executes migrations with progress reporting]

## ✓ Automatic Rebalancing Complete

All 5 migrations successful.
- CPU variance: 22.1% → 4.2% (81% improvement)
- Memory variance: 11.8% → 7.3% (38% improvement)

Cluster is now balanced.
```

### Example 2: With User Modification

```
User: "Balance cluster CPU load"

Agent: [Generates plan with 4 migrations]

## Automatic Rebalancing Plan

[Shows plan including cold migration of app-vm-05]

User: "modify - skip 4"

Agent: "Migration #4 (app-vm-05) removed from plan."

[Shows updated plan with 3 migrations]
[Recalculates expected improvements]

**Ready to execute?** (approve / modify more / cancel)

User: "approve"

Agent: [Executes 3 migrations]

## ✓ Rebalancing Complete

3/3 migrations successful.
CPU variance: 22.1% → 6.8% (69% improvement)
```

### Example 3: AI Proposes Alternative

```
User: "Drain worker-02 for maintenance"

Agent: [Generates plan to migrate all 5 VMs from worker-02]

💡 **Alternative Approach Detected**

I notice 2 VMs on worker-02 use RWO storage (cold migration required).
Current plan has ~80s total downtime (2 VMs × 40s each).

**Alternative:**
Migrate VMs sequentially instead of concurrently to reduce risk:
- Same total time
- Lower network impact
- Easier to abort if issues

Would you like to: accept alternative | keep original | explain more

User: "accept alternative"

Agent: [Updates plan to sequential execution]
       [Presents updated plan for approval]
```

---

**Sources:**
- [Live Migration - KubeVirt User Guide](https://kubevirt.io/user-guide/compute/live_migration/)
- [Node Assignment - KubeVirt User Guide](https://kubevirt.io/user-guide/compute/node_assignment/)
- [Kubernetes Descheduler](https://github.com/kubernetes-sigs/descheduler)
- [Best Practices for Virtual Machine Deployments](https://learn.microsoft.com/en-us/azure/openshift/best-practices-openshift-virtualization)

**Last Updated**: 2026-02-24
**Status**: Production Ready
