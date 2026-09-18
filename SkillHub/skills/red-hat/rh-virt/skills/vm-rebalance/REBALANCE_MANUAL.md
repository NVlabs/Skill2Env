# Manual Rebalancing Strategy

**Status**: ✅ FULLY IMPLEMENTED

**Purpose**: Execute VM migrations where the user specifies which VM(s) to move and the target node(s).

## When to Use Manual Mode

Use this mode when the user specifies:
- Exact VM name(s) to migrate
- Target node(s) for placement
- Migration type (live or cold)

**User Request Patterns:**
- "Move VM database-01 to worker-03"
- "Live migrate web-server from worker-01 to worker-05"
- "Cold migrate app-vm to worker-02"
- "Migrate VMs web-01, web-02, web-03 to worker-05"

## Manual Rebalancing Workflow

### Step 1: Gather Migration Parameters

**Collect the following information from the user:**

**Required Parameters:**
1. **VM Name(s)** - Name of virtual machine(s) to migrate
   - Example: "database-01" or ["web-01", "web-02", "web-03"]

2. **Source Namespace** - Namespace where VM(s) exist
   - Example: "production", "vms", "dev-environment"

3. **Target Node** (optional for live migration, required for cold migration)
   - Example: "worker-03", "worker-node-1.example.com"
   - For live migration: Can be omitted (scheduler chooses)
   - For cold migration: Required (set via nodeAffinity)

4. **Migration Type** - Choose migration strategy
   - `live` - Zero downtime, VM stays running (requires RWX storage)
   - `cold` - Brief downtime, stop → move → start (always works)

**If user doesn't specify migration type, determine automatically:**
- Check VM's PVC access mode using `resources_get`
- If PVC has ReadWriteMany (RWX) → Suggest live migration
- If PVC has ReadWriteOnce (RWO) → Require cold migration
- If uncertain → Ask user to choose

### Step 2: Validate Migration Feasibility

**CRITICAL**: Before proceeding with migration execution, perform the **Common Validation Logic** defined in SKILL.md.

**Reference**: See [SKILL.md - Common Validation Logic](./SKILL.md#common-validation-logic) for complete validation steps.

**The common validation performs these checks** (defined in SKILL.md):
1. **Validation 1**: Verify VM Exists
2. **Validation 2**: Check Current VM Location
3. **Validation 3**: Validate Storage Compatibility (RWX vs RWO)
4. **Validation 4**: Verify Target Node Exists

**Only proceed to Step 3 after all validations pass.**

### Step 3: Present Rebalance Plan for Confirmation

**After validation, present the rebalance plan to the user:**

**For Live Migration:**

```markdown
## VM Rebalance Plan

**Please review and confirm the migration:**

| Parameter | Value | Details |
|-----------|-------|---------|
| VM Name | `<vm-name>` | [from user input] |
| Namespace | `<namespace>` | [from user input] |
| Current Node | `<current-node>` | [detected from VMI status] |
| Target Node | `<target-node>` | [from user input or "Scheduler decides"] |
| Migration Type | `live` | Zero downtime, VM stays running |
| Storage Type | `RWX (ReadWriteMany)` | Live migration supported |
| Current Status | `Running` | [from VMI phase] |

**Migration Strategy: Live Migration**

**What will happen:**
1. Create VirtualMachineInstanceMigration resource
2. KubeVirt will:
   - Create new virt-launcher pod on target node
   - Transfer VM memory and state (live)
   - Switch network traffic to new pod
   - Terminate old virt-launcher pod
3. VM continues running throughout (brief network pause <1s)

**Impact:**
- ✓ Zero downtime (VM stays running)
- ✓ Applications remain accessible
- ⚠️ Brief network pause during cutover (<1 second)
- ⚠️ Requires network bandwidth for memory transfer
- ⚠️ Migration duration depends on VM memory size

**Estimated Duration:** ~30-60 seconds for typical VM (depends on memory size)

**Reference**: See [references/live-migration-best-practices.md](./references/live-migration-best-practices.md) for configuration parameters, storage requirements, and network optimization

**Rollback:** If migration fails, VM continues running on current node

Confirm this migration or tell me what to change:
- yes - Proceed with migration
- no - Cancel migration
- modify - Change parameters
```

**For Cold Migration:**

```markdown
## VM Rebalance Plan

| Parameter | Value | Details |
|-----------|-------|---------|
| VM Name | `<vm-name>` | [from user input] |
| Namespace | `<namespace>` | [from user input] |
| Current Node | `<current-node>` | [detected] |
| Target Node | `<target-node>` | [from user input] |
| Migration Type | `cold` | VM will stop and restart |
| Storage Type | `RWO (ReadWriteOnce)` | Live migration not supported |
| Current Status | `Running` | Will be stopped then restarted |

**Migration Strategy: Cold Migration**

**What will happen:**
1. Update VM spec with **required nodeAffinity** (forces placement on target node)
2. Stop VM using vm_lifecycle
3. VM pod terminates on current node
4. Start VM using vm_lifecycle
5. Kubernetes scheduler places VM on target node (due to nodeAffinity)
6. **After migration:** You'll choose whether to remove the affinity for long-term flexibility

**Impact:**
- ⚠️ **Downtime**: ~30-60 seconds while VM restarts
- ⚠️ Applications will be interrupted
- ⚠️ Network connections will be dropped
- ✓ Works with any storage type (RWO or RWX)
- ✓ Less resource-intensive than live migration
- ℹ️ **Long-term**: After migration, you can remove node affinity to allow flexible rescheduling if target node fails

**Estimated Downtime:** ~30-60 seconds

**Rollback:** Can start VM again if migration fails

**Note on Node Affinity:**
We use nodeAffinity (not nodeSelector) for better long-term resilience. After migration, you'll have the option to remove it, allowing the VM to reschedule to other nodes if <target-node> fails in the future.

**Reference**: See [references/production-considerations.md](./references/production-considerations.md) for workload categorization and downtime planning strategies

Confirm this migration or tell me what to change:
- yes - Proceed with cold migration
- no - Cancel
- modify - Change parameters
```

**WAIT for user confirmation before proceeding to Step 4.** Do NOT continue until user explicitly confirms with "yes".

### Step 4a: Execute Live Migration (if migration type = live)

**ONLY PROCEED AFTER USER CONFIRMATION IN STEP 3.**

**Create a VirtualMachineInstanceMigration resource to trigger live migration:**

**MCP Tool**: `resources_create_or_update` (from openshift-virtualization)

**Parameters**:
- `resource`: (JSON object as string) - REQUIRED
  - Complete VirtualMachineInstanceMigration resource definition as a JSON-formatted string
  - Must follow KubeVirt API specification

**Resource Structure** (for live migration):

```json
{
  "apiVersion": "kubevirt.io/v1",
  "kind": "VirtualMachineInstanceMigration",
  "metadata": {
    "name": "migration-<vm-name>-<timestamp>",
    "namespace": "<namespace>"
  },
  "spec": {
    "vmiName": "<vm-name>"
  }
}
```

**Example tool invocation:**
```json
{
  "resource": "{\"apiVersion\":\"kubevirt.io/v1\",\"kind\":\"VirtualMachineInstanceMigration\",\"metadata\":{\"name\":\"migration-database-01-20260223\",\"namespace\":\"production\"},\"spec\":{\"vmiName\":\"database-01\"}}"
}
```

**Note**: The `resource` parameter accepts the resource definition as a JSON-formatted string. The MCP tool will parse and apply this resource to the cluster.

**Note on Target Node Selection:**
- KubeVirt scheduler automatically selects target node
- To influence target node, update VM's nodeAffinity BEFORE creating migration
- For manual target node selection, combine with nodeAffinity update first

**Expected Output**: VirtualMachineInstanceMigration resource created successfully

**Error Handling:**
- If creation fails → Check RBAC permissions, report error to user
- If VMI not found → Verify VM is running, report error
- If VMI not migratable → Check storage access mode, suggest cold migration

#### Monitor Migration Progress

**After creating migration, monitor progress:**

**MCP Tool**: `resources_get` (from openshift-virtualization)

**Parameters** (to monitor migration status):
- `apiVersion`: "kubevirt.io/v1" - REQUIRED
- `kind`: "VirtualMachineInstanceMigration" - REQUIRED
- `name`: "migration-<vm-name>-<timestamp>" - REQUIRED
- `namespace`: "<namespace>" - REQUIRED

**Poll every 5-10 seconds until migration completes or fails.**

**Timeout**: Stop polling after 10 minutes (600 seconds) and report timeout error to user. Most migrations complete within 1-5 minutes depending on VM memory size.

**Reference**: See [references/performance-tuning.md](./references/performance-tuning.md) for timeout configuration and migration optimization strategies

**Expected Output**: VMIM resource with status field

**Extract Information:**
- `status.phase` - Migration phase:
  - `Scheduling` - Finding target node
  - `PreparingTarget` - Setting up target pod
  - `TargetReady` - Target pod ready
  - `Running` - Transferring memory
  - `Succeeded` - Migration completed
  - `Failed` - Migration failed
- `status.migrationState.completed` - Boolean, true when done
- `status.migrationState.targetNode` - Destination node
- `status.migrationState.sourceNode` - Origin node
- `status.migrationState.startTimestamp` - When migration began
- `status.migrationState.endTimestamp` - When migration completed

**When status.phase = "Succeeded":**
- Migration completed successfully
- Proceed to Step 5 (Report Results)

**When status.phase = "Failed":**
- Extract failure reason from status
- Consult troubleshooting documentation (see Step 5 failure handling)
- Report detailed error to user

### Step 4b: Execute Cold Migration (if migration type = cold)

**ONLY PROCEED AFTER USER CONFIRMATION IN STEP 3.**

**Cold migration workflow: Stop VM → Re-read VM → Update node placement → Start VM**

#### Sub-step 4b.1: Stop the VM

**MCP Tool**: `vm_lifecycle` (from openshift-virtualization)

**Parameters**:
- `namespace`: "<namespace>" - REQUIRED
- `name`: "<vm-name>" - REQUIRED
- `action`: "stop" - REQUIRED

**Expected Output**: VM stopped successfully, VMI terminates

**Wait for VM to fully stop:**
1. Wait 10 seconds
2. Check VM status using `resources_get` (VirtualMachine)
3. If `status.printableStatus` is not "Stopped", wait another 10 seconds and check again
4. Repeat until VM is fully stopped

**Error Handling:**
- If stop fails → Report error, check if VM is already stopped
- If VM stuck in Terminating after 60 seconds → Report to user

#### Sub-step 4b.2: Re-read VM for Fresh ResourceVersion

**MCP Tool**: `resources_get` (from openshift-virtualization)

**Parameters**:
- `apiVersion`: "kubevirt.io/v1" - REQUIRED
- `kind`: "VirtualMachine" - REQUIRED
- `name`: "<vm-name>" - REQUIRED
- `namespace`: "<namespace>" - REQUIRED

**Why**: `vm_lifecycle` modified the VM. Re-reading gets fresh resourceVersion to prevent conflicts when updating nodeAffinity.

**Use this fresh VM spec for nodeAffinity update in next step.**

#### Sub-step 4b.3: Update VM nodeAffinity

**MCP Tool**: `resources_create_or_update` (from openshift-virtualization)

**Parameters**:
- `resource`: (JSON object as string) - REQUIRED
  - Complete VirtualMachine resource from Sub-step 4b.2 with updated nodeAffinity

**Resource Modification** (add required nodeAffinity to VM spec):

Preserve all existing VM fields and only modify the affinity section.

**Critical Affinity Structure:**
```json
{
  "spec": {
    "template": {
      "spec": {
        "affinity": {
          "nodeAffinity": {
            "requiredDuringSchedulingIgnoredDuringExecution": {
              "nodeSelectorTerms": [
                {
                  "matchExpressions": [
                    {
                      "key": "kubernetes.io/hostname",
                      "operator": "In",
                      "values": ["<target-node>"]
                    }
                  ]
                }
              ]
            }
          }
        }
      }
    }
  }
}
```

**Why nodeAffinity instead of nodeSelector?**
- Provides flexibility for long-term resilience
- If target node fails later, user can remove affinity to allow rescheduling
- More powerful than nodeSelector (supports multiple nodes, preferences)

**Expected Output**: VirtualMachine resource updated successfully

**Error Handling:**
- If update fails → Check RBAC permissions, explain to user with exact error
- If VM not found → Report error with VM name and namespace
- If conflicts with existing affinity → Ask user: "VM already has node affinity rules. Should I replace them with new affinity to <target-node>?"

#### Sub-step 4b.4: Start the VM

**MCP Tool**: `vm_lifecycle` (from openshift-virtualization)

**Parameters**:
- `namespace`: "<namespace>" - REQUIRED
- `name`: "<vm-name>" - REQUIRED
- `action`: "start" - REQUIRED
  - Example: `"start"` (power on the VM)

**Expected Output**: VM starts successfully

**After starting, verify VM scheduled on target node:**

**MCP Tool**: `resources_get` (from openshift-virtualization)

**Parameters** (get VMI to verify node placement):
- `apiVersion`: "kubevirt.io/v1" - REQUIRED
- `kind`: "VirtualMachineInstance" - REQUIRED
- `name`: "<vm-name>" - REQUIRED
- `namespace`: "<namespace>" - REQUIRED

**Expected Output**: VMI resource with node placement

**Extract Information:**
- `status.nodeName` - Should match target node
- `status.phase` - Should be "Running"

**Verification:**
- If `status.nodeName` matches target node → Success, proceed to Step 4b.5
- If `status.nodeName` does NOT match target node → Migration failed, report error with explanation

**Error Handling with Clear Explanations:**
- If VM fails to start → Explain: "VM failed to start on <target-node>. This usually means the node doesn't have enough resources (CPU/memory) or has scheduling constraints preventing this VM."
  - Consult [scheduling-errors.md](../../docs/troubleshooting/scheduling-errors.md)
  - Suggest: Check node capacity, verify node is Ready, check for taints
- If VM scheduled on wrong node → Explain: "VM started but Kubernetes placed it on <actual-node> instead of <target-node>. This means <target-node> couldn't accommodate the VM due to resource constraints, taints, or other scheduling rules."
  - Report actual vs expected node
  - Ask user if they want to retry with different target node
- If VM stuck in Scheduling phase → Explain: "VM cannot be scheduled. The target node likely lacks sufficient CPU/memory resources, or has taints that prevent scheduling."
  - Show node constraints
  - Suggest checking node details using `resources_get` with kind="Node"

#### Sub-step 4b.5: Post-Migration Cleanup (Optional - Long-term Resilience)

**After successful cold migration, ask user about removing node affinity for long-term flexibility.**

**Present cleanup option to user:**

```markdown
## ✓ Cold Migration Successful - VM Running on Target Node

**VM Details:**
- **Name**: `<vm-name>`
- **Namespace**: `<namespace>`
- **Current Node**: `<target-node>` ✓

**Important: Long-term Resilience**

The VM now has a **required node affinity** to `<target-node>`. This means:
- ✓ VM will stay on `<target-node>` (as you requested)
- ⚠️ If `<target-node>` fails or needs maintenance later, the VM **cannot reschedule** to other nodes

**Recommendation:** Remove the node affinity to allow flexible rescheduling in the future.

Would you like to remove the node affinity now?
- **yes** - Remove affinity (VM can reschedule to any healthy node if <target-node> fails)
- **no** - Keep affinity (VM stays pinned to <target-node> permanently)
- **later** - Keep for now, I'll remove it manually when needed
```

**WAIT for user decision.**

**If user says "yes" (remove affinity):**

**MCP Tool**: `resources_get` (from openshift-virtualization)

**Parameters** (get current VM spec):
- `apiVersion`: "kubevirt.io/v1" - REQUIRED
- `kind`: "VirtualMachine" - REQUIRED
- `name`: "<vm-name>" - REQUIRED
- `namespace`: "<namespace>" - REQUIRED

**Expected Output**: Full VirtualMachine resource with current affinity

**Modify the VM spec to remove nodeAffinity:**

Extract the full VM resource, then remove `spec.template.spec.affinity.nodeAffinity` (or set to null/empty).

**MCP Tool**: `resources_create_or_update` (from openshift-virtualization)

**Parameters**:
- `resource`: (JSON object as string) - REQUIRED
  - Complete VirtualMachine resource with affinity removed as a JSON-formatted string

**Important**:
- Preserve all other VM spec fields
- Only remove the affinity section
- VM continues running on current node (doesn't trigger immediate reschedule)
- Future restarts will allow flexible scheduling

**Expected Output**: VirtualMachine resource updated successfully

**Error Handling:**
- If update fails → Explain: "Failed to remove node affinity. RBAC permissions issue or API error. VM will remain pinned to <target-node>. You can remove manually using `resources_create_or_update` with the VM spec after removing the affinity field."

**If user says "no" or "later" (keep affinity):**
- Report: "Node affinity kept. VM will remain on <target-node>. To remove manually later, use `resources_create_or_update` with the VM spec after removing the affinity field."
- Proceed to Step 5

### Step 5: Report Migration Results

**On Success (Live Migration):**

```markdown
## ✓ Live Migration Successful

**VM Details:**
- **Name**: `<vm-name>`
- **Namespace**: `<namespace>`
- **Migration Type**: Live (zero downtime)

**Migration Summary:**
- **Source Node**: `<source-node>`
- **Target Node**: `<target-node>`
- **Duration**: <duration> seconds
- **Status**: Succeeded

**Impact:**
- ✓ VM remained running throughout migration
- ✓ Applications stayed accessible
- ✓ Brief network pause during cutover (<1 second)

**Current VM Status:**
- **Running on**: `<target-node>`
- **Phase**: Running
- **Ready**: True

### Next Steps

**Verify application health:**
Use `/vm-inventory` to check VM status

**View migration details:**
Use `resources_get` with kind="VirtualMachineInstanceMigration" and name="migration-<vm-name>-<timestamp>"

**Cleanup:**
The VirtualMachineInstanceMigration resource can be deleted if no longer needed.
```

**On Success (Cold Migration) - If affinity was REMOVED:**

```markdown
## ✓ Cold Migration Successful

**VM Details:**
- **Name**: `<vm-name>`
- **Namespace**: `<namespace>`
- **Migration Type**: Cold (with downtime)

**Migration Summary:**
- **Source Node**: `<source-node>`
- **Target Node**: `<target-node>`
- **Downtime**: ~<duration> seconds
- **Status**: Succeeded

**Steps Completed:**
1. ✓ Updated VM with required nodeAffinity to `<target-node>`
2. ✓ Stopped VM on `<source-node>`
3. ✓ Started VM on `<target-node>`
4. ✓ Verified VM running on target node
5. ✓ Removed node affinity for flexible rescheduling

**Current VM Status:**
- **Running on**: `<target-node>`
- **Phase**: Running
- **Ready**: True
- **Node Affinity**: None (can reschedule to any node if needed)

**Long-term Resilience:**
✓ VM can now reschedule to other nodes if `<target-node>` fails or needs maintenance.

### Next Steps

**Verify application health:**
Use `/vm-inventory` to check VM status

**Test application connectivity:**
VM has restarted, verify services are healthy.
```

**On Success (Cold Migration) - If affinity was KEPT:**

```markdown
## ✓ Cold Migration Successful

**VM Details:**
- **Name**: `<vm-name>`
- **Namespace**: `<namespace>`
- **Migration Type**: Cold (with downtime)

**Migration Summary:**
- **Source Node**: `<source-node>`
- **Target Node**: `<target-node>`
- **Downtime**: ~<duration> seconds
- **Status**: Succeeded

**Steps Completed:**
1. ✓ Updated VM with required nodeAffinity to `<target-node>`
2. ✓ Stopped VM on `<source-node>`
3. ✓ Started VM on `<target-node>`
4. ✓ Verified VM running on target node
5. ℹ️ Kept node affinity (as requested)

**Current VM Status:**
- **Running on**: `<target-node>`
- **Phase**: Running
- **Ready**: True
- **Node Affinity**: Required on `<target-node>` (VM will stay on this node)

**Important:**
⚠️ VM is pinned to `<target-node>`. If this node fails, the VM cannot reschedule to other nodes.

**To remove affinity later:**
Use `resources_create_or_update` with the VM spec after removing the `spec.template.spec.affinity` field

### Next Steps

**Verify application health:**
Use `/vm-inventory` to check VM status

**Test application connectivity:**
VM has restarted, verify services are healthy.
```

**On Failure (with Troubleshooting):**

**OPTIONAL**: If migration fails, consult documentation for common failure scenarios.

**Document Consultation** (OPTIONAL - when migration fails):
1. **Action**: Read relevant troubleshooting guides to understand VM migration failure scenarios:
   - [scheduling-errors.md](../../docs/troubleshooting/scheduling-errors.md) - For ErrorUnschedulable, node taints, resource constraints
   - [lifecycle-errors.md](../../docs/troubleshooting/lifecycle-errors.md) - For VM start/stop failures during cold migration
   - [storage-errors.md](../../docs/troubleshooting/storage-errors.md) - For PVC access mode issues affecting live migration
2. **Output to user**: "I consulted [scheduling-errors.md](../../docs/troubleshooting/scheduling-errors.md) to understand potential causes for the migration failure."

**When to consult**:
- Live migration fails (check storage, network, resource constraints)
- Cold migration fails during start (likely scheduling or resource issues)
- VM stuck in ErrorUnschedulable state
- Unexpected error messages from migration tools

**When NOT to consult**:
- RBAC permission errors (clear cause)
- VM not found errors (clear cause)
- PVC access mode incompatibility (already validated in Step 2)

```markdown
## ❌ Migration Failed

**Error**: <error-message-from-tool>

**VM Details:**
- **Name**: `<vm-name>`
- **Namespace**: `<namespace>`
- **Migration Type**: <live|cold>
- **Source Node**: `<source-node>`
- **Target Node**: `<target-node>`

**Common Causes:**

**For Live Migration Failures:**
- **Insufficient resources** - Target node lacks CPU/memory for VM
- **Network bandwidth** - Slow network prevents migration convergence
- **PVC access mode** - Storage is not ReadWriteMany (RWX)
- **Timeout exceeded** - Migration took longer than allowed (default 150s/GiB)
- **High memory write rate** - VM writes to memory faster than transfer rate

**For Cold Migration Failures:**
- **Node not schedulable** - Target node is cordoned, has taints, or lacks resources
- **NodeSelector conflict** - VM has other scheduling constraints preventing placement
- **VM failed to start** - Check scheduling errors on target node
- **Storage issues** - PVC not accessible from target node

**Troubleshooting Steps:**

1. **Check node availability:**
   Use `resources_list` with kind="Node" to verify target node is Ready and schedulable

2. **Check VM events:**
   Use `resources_get` with kind="VirtualMachine" to see VM status and conditions

3. **Check migration status** (for live migration):
   Use `resources_list` with kind="VirtualMachineInstanceMigration" to see migration resource status

4. **Verify storage access:**
   Use `resources_get` with kind="PersistentVolumeClaim" to check PVC access modes

5. **Check resource capacity:**
   Use `nodes_top` or `resources_get` with kind="Node" to verify available CPU/memory

**Recommended Actions:**

- **If timeout**: Retry with slower workload or enable auto-converge
- **If resources**: Choose different target node with more capacity
- **If storage**: Use cold migration instead (works with RWO)
- **If node unavailable**: Verify node is Ready and untainted

**Rollback (if migration succeeded but VM has issues on target node):**

To move VM back to original node, perform reverse migration:
- **For live migration**: Create new migration from current node → original node
- **For cold migration**: Update nodeAffinity to original node, restart VM
- Use same migration type as original migration

Example: "Migrate <vm-name> from <target-node> back to <source-node>"

Would you like help troubleshooting this error?
```

## Batch VM Migration

**For migrating multiple VMs in a single operation:**

**User Request:** "Migrate VMs web-01, web-02, web-03 to worker-05"

**Safety Limits:**
- ⚠️ **Batches >5 VMs**: Warn user about potential network saturation and suggest staged execution
- ⚠️ **Batches >10 VMs**: Strongly recommend splitting into multiple batches (e.g., 5 VMs at a time)
- ⚠️ **Multiple cold migrations**: Warn about cumulative downtime impact

**Reference**: See [references/anti-patterns.md](./references/anti-patterns.md) for common mistakes when performing batch migrations and network saturation issues

**Workflow:**
1. Validate all VMs exist and are migratable
2. Determine migration type for each (based on storage)
3. **Check batch size** - If >5 VMs, warn user and offer to stage migrations
4. Present batch rebalance plan:
   ```markdown
   ## Batch Rebalance Plan

   Migrating 3 VMs to worker-05:

   | VM Name | Current Node | Migration Type | Impact |
   |---------|--------------|----------------|--------|
   | web-01 | worker-01 | live | <1s pause |
   | web-02 | worker-02 | live | <1s pause |
   | web-03 | worker-03 | cold | ~40s downtime |

   Total: 2 live migrations + 1 cold migration

   Proceed with batch migration?
   ```
4. Execute migrations sequentially (avoid saturating network)
5. Report results for each VM

## Example Usage

### Example 1: Successful Live Migration

```
User: "Live migrate VM database-01 from production namespace to worker-03"

Agent: [Validates VM exists, checks storage is RWX, verifies target node]

## VM Rebalance Plan

Please review and confirm the migration:

| Parameter | Value | Details |
|-----------|-------|---------|
| VM Name | `database-01` | from user input |
| Namespace | `production` | from user input |
| Current Node | `worker-01` | detected from VMI status |
| Target Node | `worker-03` | from user input |
| Migration Type | `live` | Zero downtime, VM stays running |
| Storage Type | `RWX (ReadWriteMany)` | Live migration supported |

**What will happen:**
1. Create VirtualMachineInstanceMigration resource
2. VM memory and state transferred live to worker-03
3. Brief network pause during cutover (<1 second)

**Impact:** Zero downtime, brief network pause

Confirm this migration?

User: "yes"

Agent: [Creates VirtualMachineInstanceMigration resource]
       [Monitors migration status]

## ✓ Live Migration Successful

**VM Details:**
- Name: `database-01`
- Namespace: `production`
- Migration Type: Live (zero downtime)

**Migration Summary:**
- Source Node: `worker-01`
- Target Node: `worker-03`
- Duration: 45 seconds
- Status: Succeeded

VM is now running on `worker-03`.
```

### Example 2: Successful Cold Migration

```
User: "Move VM web-server to worker-05 using cold migration"

Agent: [Validates VM exists, checks current node, verifies target node]

## VM Rebalance Plan

| Parameter | Value | Details |
|-----------|-------|---------|
| VM Name | `web-server` | from user input |
| Namespace | `vms` | detected/default |
| Current Node | `worker-02` | detected |
| Target Node | `worker-05` | from user input |
| Migration Type | `cold` | VM will stop and restart |
| Storage Type | `RWO (ReadWriteOnce)` | Live migration not supported |

**What will happen:**
1. Update VM nodeAffinity to target worker-05
2. Stop VM (applications will be interrupted)
3. Start VM (Kubernetes places on worker-05)

**Impact:** Downtime ~30-60 seconds

Confirm this migration?

User: "yes"

Agent: [Updates VM nodeAffinity]
       [Calls vm_lifecycle stop]
       [Calls vm_lifecycle start]
       [Verifies VM on target node]

## ✓ Cold Migration Successful

**VM Details:**
- Name: `web-server`
- Namespace: `vms`
- Migration Type: Cold (with downtime)

**Migration Summary:**
- Source Node: `worker-02`
- Target Node: `worker-05`
- Downtime: ~40 seconds
- Status: Succeeded

VM is now running on `worker-05`. Verify application health.
```

### Example 3: Migration Failure - Storage Incompatible

```
User: "Live migrate app-vm to worker-03"

Agent: [Validates VM]
       [Checks PVC access mode - discovers RWO]

## ❌ Live Migration Not Supported

**VM Details:**
- Name: `app-vm`
- Namespace: `default`
- Storage Type: `RWO (ReadWriteOnce)`

**Issue:** Live migration requires ReadWriteMany (RWX) storage. This VM uses ReadWriteOnce (RWO), which only allows attachment to one node at a time.

**Recommended Solution:** Use cold migration instead.

Would you like to proceed with cold migration? (Brief downtime ~30-60 seconds)

User: "yes, do cold migration"

Agent: [Switches to cold migration workflow]
       [Continues with cold migration process...]
```

---

**Reference Documentation:**

**Internal Skill Documentation**:
- [references/live-migration-best-practices.md](./references/live-migration-best-practices.md) - Configuration, requirements, dedicated networks
- [references/performance-tuning.md](./references/performance-tuning.md) - Right-sizing, overcommit, bandwidth tuning
- [references/anti-patterns.md](./references/anti-patterns.md) - Common mistakes to avoid
- [references/production-considerations.md](./references/production-considerations.md) - HA strategies, capacity planning

**Official KubeVirt Documentation**:
- [Live Migration - KubeVirt User Guide](https://kubevirt.io/user-guide/compute/live_migration/)
- [Node Assignment - KubeVirt User Guide](https://kubevirt.io/user-guide/compute/node_assignment/)
- [VirtualMachineInstanceMigration API](https://kubevirt.io/api-reference/main/definitions.html#_v1_virtualmachineinstancemigration)
