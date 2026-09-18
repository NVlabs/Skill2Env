---
name: vm-rebalance
description: |
  Orchestrate VM migrations across cluster nodes for load balancing, maintenance, and resource optimization.

  Use when:
  - "Move VM database-01 to worker-03"
  - "Rebalance VMs to optimize CPU load"
  - "Drain worker-02 for maintenance"
  - "Automatically rebalance the cluster"

  Supports Manual (user-driven) and Automatic (AI-driven) modes.

  NOT for creating VMs (use vm-create) or lifecycle only (use vm-lifecycle-manager).

license: Apache-2.0
model: inherit
color: yellow
allowed-tools: resources_list resources_get resources_create_or_update vm_lifecycle nodes_top pods_top nodes_stats_summary
---

# /vm-rebalance Skill

Orchestrate VM migrations across OpenShift cluster nodes for load balancing, maintenance, and resource optimization. Supports manual and automatic rebalancing with live migration (zero downtime) and cold migration (brief downtime) strategies.

**Implementation**: Uses KubeVirt's VirtualMachineInstanceMigration API for live migrations and node affinity for cold migrations.

## Prerequisites

**Required MCP Server**: `openshift-virtualization` ([OpenShift MCP Server](https://github.com/openshift/openshift-mcp-server))

**Required MCP Tools**:
- `resources_list` - List VMs and nodes
- `resources_get` - Get VM and node details
- `resources_create_or_update` - Create migrations and update VM specs
- `vm_lifecycle` - Start/stop VMs for cold migration
- `nodes_top` - Monitor node resource usage
- `pods_top` - Monitor VM resource consumption

**Required Environment Variables**:
- `KUBECONFIG` - Path to Kubernetes configuration file

**Required Cluster Setup**:
- OpenShift cluster (>= 4.17)
- OpenShift Virtualization operator installed
- ServiceAccount with permissions: get/list/update for VMs, create for VirtualMachineInstanceMigration
- For live migration: RWX storage and sufficient network bandwidth

### Prerequisite Verification

**Before executing:**
1. Check `openshift-virtualization` exists in `mcps.json` → If missing, report setup
2. Verify `KUBECONFIG` is set (presence only, never expose value) → If missing, report
3. For live migration: Check PVC access mode is ReadWriteMany (RWX) via `resources_get`

**Human Notification Protocol:** `❌ Cannot execute vm-rebalance: MCP server not available. Setup: Add to mcps.json, set KUBECONFIG, restart Claude Code. Docs: https://github.com/openshift/openshift-mcp-server`

⚠️ **SECURITY**: Never display KUBECONFIG path or credential values.

## When to Use This Skill

**Trigger when:**
- User explicitly invokes `/vm-rebalance`
- User requests moving VM(s) to specific node(s)
- User wants to drain node for maintenance
- User requests load balancing or resource optimization

**User phrases:**
- "Move VM database-01 to worker-03"
- "Live migrate web-server to worker-05"
- "Drain worker-02 for maintenance"
- "Balance CPU load across nodes"
- "Automatically rebalance the cluster"

**Do NOT use when:**
- Creating VMs → `/vm-create`
- Start/stop only → `/vm-lifecycle-manager`
- Cloning VMs → `/vm-clone`
- Deleting VMs → `/vm-delete`

## Workflow

### Step 1: Determine Rebalancing Mode

**Manual Mode**: User specifies VM name(s) and target node(s). Example: "Move VM database-01 to worker-03"

**Automatic Mode**: User requests AI-driven rebalancing. Example: "Rebalance VMs based on CPU"

### Step 2: Load Strategy File and Execute

**For Manual Mode:**

**Document Consultation** (REQUIRED - Execute FIRST):
1. **Action**: Read [REBALANCE_MANUAL.md](./REBALANCE_MANUAL.md) using Read tool
2. **Output to user**: "I consulted [REBALANCE_MANUAL.md](./REBALANCE_MANUAL.md) to understand the manual migration workflow."
3. **Then execute**: Follow workflow in REBALANCE_MANUAL.md

---

**For Automatic Mode:**

**Document Consultation** (REQUIRED - Execute FIRST):
1. **Action**: Read [REBALANCE_AUTOMATIC.md](./REBALANCE_AUTOMATIC.md) using Read tool
2. **Output to user**: "I consulted [REBALANCE_AUTOMATIC.md](./REBALANCE_AUTOMATIC.md) to understand the automatic rebalancing workflow."
3. **Then execute**: Follow workflow in REBALANCE_AUTOMATIC.md

## Common Validation Logic

**Shared by ALL migration strategies. Execute before any VM migration:**

### Validation 1: Verify VM Exists

**MCP Tool**: `resources_get` (apiVersion="kubevirt.io/v1", kind="VirtualMachine", name=`<vm>`, namespace=`<ns>`)

**Extract**: `spec.template.spec.volumes[].persistentVolumeClaim.claimName`, `status.ready`

**Errors**: VM not found → Use vm-inventory | Namespace not found → Verify name | Permission denied → Check RBAC

### Validation 2: Check Current VM Location

**MCP Tool** (if VM running): `resources_get` (apiVersion="kubevirt.io/v1", kind="VirtualMachineInstance", name=`<vm>`, namespace=`<ns>`)

**Extract**: `status.nodeName`, `status.phase`

**Validation**: If already on target → "VM already on target node. No migration needed."

### Validation 3: Validate Storage Compatibility

**MCP Tool**: `resources_get` (apiVersion="v1", kind="PersistentVolumeClaim", name=`<pvc>`, namespace=`<ns>`)

**Extract**: `spec.accessModes`
- ReadWriteMany (RWX) → Live migration supported
- ReadWriteOnce (RWO) → Live migration NOT supported

**Error for live migration**: If RWO → "Cannot live migrate. Use cold migration (brief downtime ~30-60s)."

**Reference**: [references/live-migration-best-practices.md](./references/live-migration-best-practices.md)

### Validation 4: Verify Target Node Exists

**MCP Tool**: `resources_list` (apiVersion="v1", kind="Node")

**Validation**: Verify target exists, `status.conditions[]` shows Ready=True, not cordoned

**Errors**: Not found → "Node doesn't exist" | Not Ready → "Choose different target" | Cordoned → "Uncordon or choose different target"

**Reference**: [scheduling-errors.md](docs/troubleshooting/scheduling-errors.md)

## Node Selection for Automatic Rebalancing

**Applies to Automatic Mode only.**

**Use** `resources_list` **(apiVersion="v1", kind="Node")**

Filter where ALL true:
1. `metadata.labels["kubevirt.io/schedulable"] == "true"`
2. `status.capacity["devices.kubevirt.io/kvm"]` > "0"
3. No `node-role.kubernetes.io/control-plane` or `node-role.kubernetes.io/master` label

**If no nodes**: "No suitable nodes. Check OpenShift Virtualization operator and hardware virtualization support."

**Note**: Ignore custom taints. Use official KubeVirt labels.

## Common Migration Types

**Live Migration**: Zero downtime, <1s pause during cutover. Requires RWX storage. Memory transferred while VM runs.

**Cold Migration**: Brief downtime (~30-60s). Works with any storage. Stop VM → Update placement → Start on target.

**Reference**: [references/live-migration-best-practices.md](./references/live-migration-best-practices.md)

## Common Plan Visualization

**ALL strategies MUST use this standardized format for consistency.**

### Information Relevance Principle

Show only what matters:
- ✅ Include: Deviations from defaults, user-specified criteria, non-obvious context
- ❌ Exclude: Standard procedures, default settings, info already visible in tables

### Standard Plan Format

**Table 1: VM Rebalance Plan**

```markdown
## 📋 VM Rebalance Plan

| VM | Instance Type | Current Node | → | New Node | Type | Downtime | Notes |
|----|---------------|--------------|---|----------|------|----------|-------|
| vm-1 | u1.xlarge | worker-01 | → | worker-03 | Live | <1s pause | ContainerDisk |
| vm-2 | u1.2xmedium | worker-01 | → | worker-02 | Cold | ~40s | RWO storage |
| vm-3 | u1.medium | worker-02 | - | *stays* | - | - | Already balanced |
```

**Column Definitions**: VM name | Instance type | Current node | Movement indicator | Target node (or *stays*) | Migration type (Live/Cold/-) | Downtime (<1s/~30-60s/-) | Brief explanation

**Table 2: Node State Before → After**

```markdown
## 📊 Node State: Before → After

| Node | VMs Now | CPU Now | Memory Now | → | VMs After | CPU After | Memory After | Change |
|------|---------|---------|------------|---|-----------|-----------|--------------|--------|
| worker-01 | 5 | 85% | 72% | → | 3 | 68% | 59% | ✓ Reduced load |
| worker-02 | 2 | 42% | 48% | → | 3 | 58% | 61% | ← Receiving VMs |
| worker-03 | 3 | 38% | 51% | → | 4 | 55% | 63% | ← Receiving VMs |
```

**CRITICAL - Capacity Calculation Method:**

CPU/Memory percentages MUST be calculated based on **allocated capacity**, not actual runtime usage:

**CPU Percentage Calculation**:
1. Get node total CPU capacity from `resources_get` Node → `status.capacity.cpu` (e.g., "32" = 32 vCPUs)
2. For each VM on node, get allocated vCPUs from VMI → `spec.domain.cpu.sockets × spec.domain.cpu.cores × spec.domain.cpu.threads`
3. Sum all VM vCPUs on the node
4. Calculate: (Sum of VM vCPUs / Node CPU capacity) × 100

**Memory Percentage Calculation**:
1. Get node total memory capacity from `resources_get` Node → `status.capacity.memory` (e.g., "128Gi")
2. For each VM on node, get allocated memory from VMI → `spec.domain.memory.guest`
3. Sum all VM memory allocations on the node (convert to same units)
4. Calculate: (Sum of VM memory / Node memory capacity) × 100

**Example**: Node with 32 vCPUs hosting VMs with 2+4+8+4+2 = 20 vCPUs → CPU = 62.5% (20/32), NOT the actual runtime usage which might be 0% if VMs are idle.

**Rationale**: Shows **capacity planning** (how much is reserved) rather than runtime utilization, which is more useful for rebalancing decisions.

**Overcommit Detection and Warning**:

If any node's CPU or Memory percentage **exceeds 100%** after rebalancing:

```markdown
⚠️ **OVERCOMMIT WARNING**

**Node(s) will be overcommitted after this rebalance:**
- **worker-02**: CPU 125% (40 vCPUs allocated / 32 vCPUs capacity) - **25% overcommit**
- **worker-03**: Memory 110% (88Gi allocated / 80Gi capacity) - **10% overcommit**

**Impact:**
- **CPU overcommit**: VMs may experience CPU throttling and reduced performance when all VMs are active simultaneously
- **Memory overcommit**: Risk of VM eviction or OOM (Out of Memory) if total memory demand exceeds node capacity

**Recommendations:**
- Consider distributing VMs across more nodes to avoid overcommit
- Review VM instance types to ensure they match actual workload requirements
- Monitor node resource usage closely after rebalancing

**Proceed with overcommit?** (yes/cancel)
```

**When NOT to warn**: If percentages ≤ 100%, overcommit is not present. Omit this warning section.

**After tables, include:**

**Key Improvement**: `"Distribution from 1 node to 4 nodes hosting VMs"` or `"CPU variance reduced from 22% to 4% (81% improvement)"`

**Rebalance Summary** (batch operations):
```markdown
- Total VMs: 5 | Live: 4 | Cold: 1 | Staying: 2
- Total Downtime: ~40s | Duration: 1-2min (parallel)
```

**Execution Mode**: `**Parallel** (default) - all VMs rebalance simultaneously` OR `**Sequential** (user requested)`

**Terminology Standards**:
- ✅ "VM Rebalance Plan", "Rebalancing", "Live/Cold migration", "Current Node/New Node", "VMs Now/VMs After"
- ❌ "VM Migration Plan" (reserved for future migration skill)

## Common Error Handling

### Error 1: Live Migration Fails - Storage Not RWX
**Symptom**: "Cannot live migrate: PVC access mode is ReadWriteOnce"
**Solution**: Use cold migration OR convert PVC to RWX
**Reference**: [storage-errors.md](docs/troubleshooting/storage-errors.md)

### Error 2: VM Stuck ErrorUnschedulable After Cold Migration
**Symptom**: "VM cannot be scheduled: ErrorUnschedulable"
**Solution**: Check node capacity (`nodes_top`), verify no blocking taints (`resources_get` Node), add tolerations, choose different target, remove nodeSelector
**Reference**: [scheduling-errors.md](docs/troubleshooting/scheduling-errors.md)

### Error 3: Live Migration Times Out
**Symptom**: "Migration exceeded timeout: 150s per GiB"
**Solution**: Retry migration, reduce VM workload, use cold migration, increase timeout in HyperConverged CR
**Reference**: [references/performance-tuning.md](./references/performance-tuning.md)

### Error 4: Migration Rejected - Cluster Limit Reached
**Symptom**: "Migration rejected: cluster limit reached (5 concurrent)"
**Solution**: Wait for migrations to complete (`resources_list` VirtualMachineInstanceMigration), retry, migrate sequentially, increase limit
**Reference**: [references/performance-tuning.md](./references/performance-tuning.md)

### Error 5: RBAC Permission Denied
**Symptom**: "Forbidden: User cannot create VirtualMachineInstanceMigration"
**Solution**: Verify RBAC permissions (`create` on VirtualMachineInstanceMigration, `update` on VirtualMachine), contact admin

### Error 6: Network Saturation
**Symptom**: Multiple migrations slow/fail, high network utilization
**Solution**: Reduce concurrent migrations, set bandwidth limit, use dedicated migration network
**Reference**: [references/performance-tuning.md](./references/performance-tuning.md)

### Error 7: Resource Version Conflict During Cold Migration
**Symptom**: "Apply failed: conflict with 'kubernetes-mcp-server' using .spec.runStrategy"
**Solution**: After `vm_lifecycle` stop, re-read VM using `resources_get` before updating nodeAffinity (gets fresh resourceVersion)
**Workflow**: Stop → Wait → Re-read → Update nodeAffinity → Start
**Reference**: [REBALANCE_MANUAL.md - Sub-step 4b.2.5](./REBALANCE_MANUAL.md)

## Dependencies

### Required MCP Servers
- `openshift-virtualization` - OpenShift MCP server (https://github.com/openshift/openshift-mcp-server)

### Required MCP Tools
- `resources_list`, `resources_get`, `resources_create_or_update`, `vm_lifecycle`, `nodes_top`, `pods_top`, `nodes_stats_summary`

### Related Skills
- `vm-inventory` - List VMs and check placement
- `vm-lifecycle-manager` - Simple start/stop
- `vm-create` - Create VMs with placement
- `vm-snapshot-create` - Backup before risky migrations

### Reference Documentation

**Skill Strategy Files**:
- [REBALANCE_MANUAL.md](./REBALANCE_MANUAL.md) - User-driven migration
- [REBALANCE_AUTOMATIC.md](./REBALANCE_AUTOMATIC.md) - AI-driven rebalancing

**Performance and Best Practices**:
- [references/live-migration-best-practices.md](./references/live-migration-best-practices.md) - Configuration, requirements, networks
- [references/performance-tuning.md](./references/performance-tuning.md) - Right-sizing, overcommit, bandwidth
- [references/anti-patterns.md](./references/anti-patterns.md) - Common mistakes
- [references/production-considerations.md](./references/production-considerations.md) - HA, capacity, security

**Troubleshooting**:
- [Troubleshooting INDEX](docs/troubleshooting/INDEX.md) - Master index
- [scheduling-errors.md](docs/troubleshooting/scheduling-errors.md) - ErrorUnschedulable, taints
- [storage-errors.md](docs/troubleshooting/storage-errors.md) - PVC access modes
- [lifecycle-errors.md](docs/troubleshooting/lifecycle-errors.md) - VM start/stop

**Official Documentation**:
- [OpenShift Virt - Live Migration](https://docs.redhat.com/en/documentation/openshift_container_platform/4.21/html-single/virtualization/index#virt-live-migration)
- [OpenShift Virt - Node Placement](https://docs.redhat.com/en/documentation/openshift_container_platform/4.21/html-single/virtualization/index#virt-node-placement)
- [KubeVirt - Live Migration](https://kubevirt.io/user-guide/compute/live_migration/)
- [KubeVirt - Node Assignment](https://kubevirt.io/user-guide/compute/node_assignment/)
- [VirtualMachineInstanceMigration API](https://kubevirt.io/api-reference/main/definitions.html#_v1_virtualmachineinstancemigration)

## Critical: Human-in-the-Loop Requirements

**IMPORTANT**: This skill performs VM migrations affecting placement and availability. You MUST:

1. **Before Initiating Migration**
   - Present complete rebalance plan (VM, nodes, type, impact)
   - Explain downtime (live = <1s pause, cold = 30-60s)
   - Show current vs target placement
   - Ask: "Confirm this migration?"
   - Wait for explicit confirmation

2. **Never Auto-Execute**
   - **NEVER migrate without confirmation**
   - **NEVER assume live vs cold** - ask or infer from storage
   - **NEVER skip impact explanation**
   - **NEVER proceed if validation fails**

3. **For Batch Operations**
   - Present all VMs to migrate
   - Show total impact (e.g., "3 VMs, 2 live + 1 cold")
   - Confirm entire batch before starting
   - Report progress for each
   - Stop on first failure

**Why**: Live migration (brief pause, bandwidth, performance impact), Cold migration (downtime, dropped connections), Wrong node (performance degradation), Batch (network saturation)

**Rationale**: Prevents unintended disruption; maintains user control.

## Security Considerations

- **RBAC Enforcement**: Requires specific permissions (create/update/list)
- **Node Access**: Respects node taints and RBAC policies
- **Storage Security**: Data remains encrypted if using encrypted storage classes
- **Network Isolation**: Migrations respect NetworkPolicies
- **Audit Trail**: All operations logged in Kubernetes API audit logs
- **KUBECONFIG Security**: Credentials never exposed
- **Resource Quotas**: Respects namespace quotas
- **Tenant Isolation**: Cannot migrate across namespaces without RBAC

---

**Strategy Implementation**: ✅ REBALANCE_MANUAL.md | ✅ REBALANCE_AUTOMATIC.md

**Reference Documentation**: ✅ live-migration-best-practices.md | ✅ performance-tuning.md | ✅ anti-patterns.md | ✅ production-considerations.md

**Last Updated**: 2026-02-24 | **OpenShift Virtualization**: 4.17, 4.18, 4.19, 4.20
