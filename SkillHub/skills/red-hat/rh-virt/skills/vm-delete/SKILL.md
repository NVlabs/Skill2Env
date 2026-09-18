---
name: vm-delete
description: |
  Permanently delete virtual machines and their associated resources from OpenShift Virtualization.

  Use when:
  - "Delete VM [name]"
  - "Remove virtual machine [name]"
  - "Destroy VM [name]"
  - "Clean up VM [name]"

  This skill handles permanent VM deletion with strict safety confirmations and typed verification.

  NOT for power management (use vm-lifecycle-manager to stop VMs).

license: Apache-2.0
model: inherit
color: red
allowed-tools: resources_get resources_delete resources_list resources_create_or_update vm_lifecycle pods_list_in_namespace
---

# /vm-delete Skill

Permanently delete virtual machines and their associated resources (storage, DataVolumes) from OpenShift Virtualization clusters. This skill enforces strict safety protocols including typed confirmation and pre-deletion validation.

## Prerequisites

**Required MCP Server**: `openshift-virtualization` ([OpenShift MCP Server](https://github.com/openshift/openshift-mcp-server))

**Required MCP Tools**:
- `resources_get` (from openshift-virtualization) - Verify VM exists and get details
- `resources_delete` (from openshift-virtualization) - Delete Kubernetes resources
- `resources_list` (from openshift-virtualization) - List dependent resources (PVCs, DataVolumes)
- `resources_create_or_update` (from openshift-virtualization) - Update resources (e.g., remove finalizers)
- `vm_lifecycle` (from openshift-virtualization) - Stop running VMs before deletion
- `pods_list_in_namespace` (from openshift-virtualization) - List pods for diagnostics

**Required Environment Variables**:
- `KUBECONFIG` - Path to Kubernetes configuration file with cluster access

**Required Cluster Setup**:
- OpenShift cluster (>= 4.19)
- OpenShift Virtualization operator installed
- ServiceAccount with RBAC permissions to delete VirtualMachine and PVC resources

### Prerequisite Verification

**Before executing:**
1. Check `openshift-virtualization` exists in `mcps.json` → If missing, report setup
2. Verify `KUBECONFIG` is set (presence only, never expose value) → If missing, report
3. Check RBAC permissions (optional) → Verify delete permissions for VirtualMachine and PVC

**Human Notification Protocol:** `❌ Cannot execute vm-delete: MCP server not available. Setup: Add to mcps.json, set KUBECONFIG, restart Claude Code. Docs: https://github.com/openshift/openshift-mcp-server`

⚠️ **SECURITY**: Never display KUBECONFIG path or credential values.

## When to Use This Skill

**Trigger when:**
- User explicitly invokes `/vm-delete` command
- User requests permanent VM deletion
- User wants to clean up test/development VMs
- User needs to free cluster resources
- User wants to decommission VMs

**User phrases:**
- "Delete VM test-vm in namespace dev"
- "Remove virtual machine web-server"
- "Destroy VM old-database"
- "/vm-delete"

**Do NOT use when:**
- Stop VM temporarily → `/vm-lifecycle-manager`
- Create VM → `/vm-create`
- View VMs → `/vm-inventory`

## Workflow

### Step 1: Gather and Validate

**CRITICAL**: Complete ALL validation BEFORE user confirmation.

**Required from user:** VM Name, Namespace

**1.1: Verify VM Exists**

**MCP Tool**: `resources_get` (apiVersion="kubevirt.io/v1", kind="VirtualMachine", namespace=`<ns>`, name=`<vm>`)

**Errors:**
- Not found → Report error, suggest vm-inventory
- Permission denied → Report RBAC error

**1.2: Check Protection Label**

Check `metadata.labels` for `protected: "true"`.

**If protected:** Report: `❌ Cannot Delete Protected VM. VM has protected label. Remove: oc label vm <vm> -n <ns> protected-. Operation cancelled.` **STOP workflow.**

**1.3: Check Running State**

Check `status.printableStatus` (Running/Starting/Migrating = running, Stopped/Halted = stopped).

**If running:** Report: `⚠️ VM Running. Must stop before deletion. Options: stop-and-delete / cancel` **Wait for response.**

**1.4: Stop VM (if applicable)**

**ONLY if user chose "stop-and-delete".**

**MCP Tool**: `vm_lifecycle` (namespace=`<ns>`, name=`<vm>`, action="stop")

Report: `⏸️ Stopping VM... Wait 10-30s.` **Wait 10s**, verify stopped.

**1.5: Discover Storage**

**MCP Tool**: `resources_list`

**DataVolumes**: apiVersion="cdi.kubevirt.io/v1beta1", kind="DataVolume", namespace=`<ns>`, labelSelector="vm.kubevirt.io/name=`<vm>`"

**PVCs** (if no DVs): apiVersion="v1", kind="PersistentVolumeClaim", namespace=`<ns>`, labelSelector="vm.kubevirt.io/name=`<vm>`"

Parse: Extract names, calculate total storage size.

### Step 2: Present Scope and Get Options

Display deletion scope in this format:

```markdown
## ⚠️ VM Deletion - Review Scope

**VM**: `<vm>` | **Namespace**: `<ns>` | **Status**: <Stopped/Running>

**Resources**: VM `<vm>` (Age: <age>, vCPU: <cpu>, Memory: <mem>)
**Storage**: DataVolume `<dv>` (30Gi), PVC `<pvc>` (30Gi) - Total: 30Gi
OR **Storage**: None (ephemeral)

### Deletion Options
**1: VM Only** - Preserves storage for reuse
**2: VM + Storage** ← Recommended (test/dev) - Frees storage
**3: Cancel**

Select (1, 2, or 3):
```

**Wait for selection.** Handle: 3→Cancel, 1→delete_storage=false, 2→delete_storage=true

### Step 3: Typed Confirmation (MANDATORY)

**CRITICAL**: User MUST type exact VM name.

Display typed confirmation prompt (adjust based on delete_storage flag):

```markdown
## 🔴 PERMANENT DELETION - Typed Confirmation Required

**CANNOT BE UNDONE**

**Will delete**:
✗ VirtualMachine: `<vm>` (namespace: `<ns>`)
[If delete_storage=true, show:]
✗ DataVolume: `<dv>` | ✗ PVC: `<pvc>` | ✗ All data lost
[If delete_storage=false, show:]
✓ Storage PRESERVED

Type `<vm>` to confirm: _____
```

**Validation:**
- Match → Continue to Step 4 (Execute Deletion)
- Mismatch → Report: `❌ Confirmation Failed. You typed: <input>. Expected: <vm>. Cancelled.` **STOP.**

### Step 4: Execute Deletion

**ONLY AFTER**: ✓ Validation ✓ Option selected ✓ Typed name confirmed

**4.1: Delete VM**

**MCP Tool**: `resources_delete` (apiVersion="kubevirt.io/v1", kind="VirtualMachine", namespace=`<ns>`, name=`<vm>`)

**Errors:** Fails → Report, don't delete storage; Not found → Continue

Report: `🗑️ Deleting VM... ✓ Deleted`

**4.2: Delete Storage (if delete_storage=true)**

**For each DataVolume:**
**MCP Tool**: `resources_delete` (apiVersion="cdi.kubevirt.io/v1beta1", kind="DataVolume", namespace=`<ns>`, name=`<dv>`)

**For each PVC:**
**MCP Tool**: `resources_delete` (apiVersion="v1", kind="PersistentVolumeClaim", namespace=`<ns>`, name=`<pvc>`)

**Errors:** Report which failed, continue with others

Report: `🗑️ Deleting storage... ✓ DV deleted (storage freed) ✓ PVC deleted`

### Step 5: Report Results

**Success (with storage):**

```markdown
## ✓ VM Deleted (Complete Cleanup)
**Deleted**: VM + DataVolume + PVC | **Freed**: <size>
**Impact**: Permanent removal. Cannot recover.
**Verify**: "List VMs in namespace <ns>" - VM should not appear
```

**Success (storage preserved):**

```markdown
## ✓ VM Deleted (Storage Preserved)
**Deleted**: VM | **Preserved**: DataVolume + PVC (<size>)
**Reuse**: Create new VM with existing DV/PVC
**Delete later**: `oc delete datavolume <dv> -n <ns>`
```

**Partial failure (storage failed):**

**OPTIONAL**: Read [storage-errors.md](docs/troubleshooting/storage-errors.md) for PVC cleanup. Output: "Consulted storage-errors.md for failure."

```markdown
## ⚠️ Partial Deletion
**Deleted**: VM | **Failed**: DV/PVC (error: <error>)
**Action**: Manual cleanup: `oc delete datavolume <dv> -n <ns>`
```

**Complete failure:**

**OPTIONAL**: Read [lifecycle-errors.md](docs/troubleshooting/lifecycle-errors.md) for deletion failures. Output: "Consulted lifecycle-errors.md for failure causes."

```markdown
## ❌ VM Deletion Failed
**Error**: <error>
**Troubleshooting**: Check permissions, verify VM exists, check finalizers (see lifecycle-errors.md)
```

## Common Issues

### Issue 1: VM Not Found
**Error**: "VirtualMachine not found"
**Solution**: Verify name/namespace with vm-inventory. Check spelling.

### Issue 2: RBAC Permissions
**Error**: "Forbidden: Cannot delete VirtualMachines"
**Solution**: Verify delete permissions for VirtualMachine and PVC. Contact admin. Check: `oc auth can-i delete virtualmachines -n <ns>`

### Issue 3: VM Has Finalizers
**Error**: "VM deletion blocked by finalizers"
**Solution**: Consult [lifecycle-errors.md](docs/troubleshooting/lifecycle-errors.md) "VM Stuck in Terminating" for MCP-first approach using `resources_get` to check finalizers, `resources_create_or_update` to remove if needed.

### Issue 4: Storage Deletion Failure
**Error**: "PVC deletion failed: resource in use"
**Solution**: Verify VM deleted first. Consult [storage-errors.md](docs/troubleshooting/storage-errors.md) for MCP-first diagnostics using `pods_list_in_namespace` to check mounts, `resources_get` for PVC status.

### Issue 5: Confirmation Mismatch
**Error**: "Names do not match"
**Solution**: Type exact VM name (case-sensitive). Copy-paste from deletion scope. Retry.

### Issue 6: Protected VM
**Error**: "VM has protected label"
**Solution**: Remove: `oc label vm <vm> -n <ns> protected-`. Retry deletion.

## Dependencies

### Required MCP Servers
- `openshift-virtualization` - OpenShift MCP with KubeVirt toolset (https://github.com/openshift/openshift-mcp-server)

### Required MCP Tools
- `resources_get` - Get VM (apiVersion, kind, namespace, name)
- `resources_delete` - Delete resources (apiVersion, kind, namespace, name)
- `resources_list` - List resources (apiVersion, kind, namespace, labelSelector)
- `resources_create_or_update` - Update resources (resource JSON) - for finalizer removal
- `vm_lifecycle` - VM lifecycle (namespace, name, action: stop)
- `pods_list_in_namespace` - List pods (namespace) - for PVC mount diagnostics

### Related Skills
- `vm-lifecycle-manager` - Stop VMs | `vm-inventory` - List VMs | `vm-create` - Create VMs | `vm-clone` - Clone VMs

### Reference Documentation
- [lifecycle-errors.md](docs/troubleshooting/lifecycle-errors.md) - Deletion failures, finalizers, stuck Terminating (consulted on deletion failure)
- [storage-errors.md](docs/troubleshooting/storage-errors.md) - Storage deletion, PVC cleanup (consulted on storage failure)
- [Troubleshooting INDEX](docs/troubleshooting/INDEX.md) - Full error index
- [OpenShift Virt Docs](https://docs.redhat.com/en/documentation/openshift_container_platform/4.21/html-single/virtualization/index)
- [KubeVirt API](https://kubevirt.io/api-reference/)
- [K8s Finalizers](https://kubernetes.io/docs/concepts/overview/working-with-objects/finalizers/)

## Critical: Human-in-the-Loop Requirements

**CRITICAL: IRREVERSIBLE operations.** You MUST:

1. **Pre-Deletion Validation** (Execute FIRST)
   - Verify VM exists (`resources_get`)
   - Check VM running state
   - Discover dependent resources
   - Check protection labels (`protected: "true"`)

2. **Safety Checks**
   - **REFUSE deletion** if protected label exists
   - **REQUIRE VM stopped** if running
   - **List all resources** to be deleted

3. **Typed Confirmation (MANDATORY)**
   - Display complete deletion scope
   - **Require exact VM name** to confirm
   - Accept only exact match (case-sensitive)
   - Mismatch → Cancel, don't proceed
   - Match → Proceed directly to deletion

4. **Deletion Options**
   - Ask: VM only / VM+Storage / Cancel
   - **NEVER assume** which option

5. **Never Auto-Execute**
   - NEVER delete without typed confirmation
   - NEVER proceed if typed name mismatches
   - NEVER skip typed verification

**Why**: Permanent data loss, service impact, accidental deletion prevention

## Security Considerations

- **RBAC**: Requires delete VirtualMachine, PVC, DataVolume
- **Typed Verification**: Prevents accidental deletion
- **Protection Labels**: `protected: "true"` blocks deletion
- **Audit**: Kubernetes audit logs
- **Graceful Shutdown**: Stops VMs before deletion
- **KUBECONFIG**: Never exposed
- **Namespace Isolation**: RBAC-enforced
- **No Force Delete**: Never uses `--force` or `--grace-period=0`

## Example Usage

### Example 1: Complete Deletion (VM + Storage)

```
User: "Delete test-vm in dev"
Agent: [Validates ✓, discovers 30Gi storage]
       [Shows deletion scope - see Step 2 format]
User: "2" [VM+Storage]
Agent: [Shows typed confirmation - see Step 3 format]
User: "test-vm"
Agent: [Executes: VM ✓, DV ✓, PVC ✓]
       [Shows success report - see Step 5 format]
## ✓ VM Deleted (Complete Cleanup) | Freed: 30Gi
```

### Example 2: VM Only (Preserve Storage)

```
User: "Remove web-server but keep storage"
Agent: [Validates, shows scope]
User: "1" [VM only]
Agent: [Typed confirmation]
User: "web-server"
Agent: [Executes deletion]
## ✓ VM Deleted (Storage Preserved) | Preserved: 50Gi
```

### Example 3: Protected VM (Blocked)

```
User: "Delete production-db"
Agent: [Validates: protected label found]
❌ Cannot Delete Protected VM. Remove label: oc label vm production-db protected-
```

### Example 4: Running VM (Stop First)

```
User: "Delete api-server"
Agent: [Validates: VM running]
⚠️ VM Running. Options: stop-and-delete / cancel
User: "stop-and-delete"
Agent: [Stops VM, waits, continues with deletion]
```

### Example 5: User Cancels

```
User: "Delete test-vm"
Agent: [Shows typed confirmation]
Type `test-vm` to confirm:
User: "wait, cancel"
❌ Confirmation Failed. You typed: wait, cancel. Expected: test-vm. Cancelled.
```

### Example 6: Dry-Run Preview

```
User: "What would be deleted if I delete test-vm?"
Agent: [Execute Step 1-2 only, stop before confirmation]
## 🔍 Deletion Preview
**Would delete (Option 2)**: VM + DV + PVC (30Gi freed)
This is preview only. No resources deleted.
```

## Advanced Features

### Batch Deletion
Delete multiple VMs: `"Delete VMs test-01, test-02, test-03 in dev"` → Process each VM individually through the full workflow (Steps 1-5), requiring typed confirmation of each VM name separately. Never use a generic batch confirmation — each VM must be confirmed by its exact name.

### Dry-Run Mode
Show deletion scope without executing: Execute Step 1-2, skip Steps 3-4. User request: "Show what would be deleted if I delete VM xyz"

### Protected VM Label
Automatic enforcement: If VM has `protected: "true"` label, refuse deletion in Step 1.2. Example YAML: `metadata.labels.protected: "true"`
