---
name: vm-clone
description: |
  Clone existing virtual machines for testing, scaling, or creating templates.

  Use when:
  - "Clone VM [source] to [target]"
  - "Create a copy of VM [name]"
  - "Duplicate VM [name] for testing"
  - "Create 3 copies of template-vm"

  This skill clones VM configuration and optionally creates new storage or references existing storage.

  NOT for snapshots (use vm-snapshot for point-in-time backups).

license: Apache-2.0
model: inherit
color: blue
allowed-tools: resources_get resources_create_or_update resources_list
---

# /vm-clone Skill

Clone existing virtual machines in OpenShift Virtualization, creating new VMs with copied configuration and optional storage cloning. This skill is ideal for creating test environments, scaling workloads, or duplicating VM templates.

## Prerequisites

**Required MCP Server**: `openshift-virtualization` ([OpenShift MCP Server](https://github.com/openshift/openshift-mcp-server))

**Required MCP Tools**:
- `resources_get` (from openshift-virtualization) - Get source VM configuration
- `resources_create_or_update` (from openshift-virtualization) - Create cloned VM
- `resources_list` (from openshift-virtualization) - List DataVolumes, PVCs, VMs

**Required Environment Variables**:
- `KUBECONFIG` - Path to Kubernetes configuration file with cluster access

**Required Cluster Setup**:
- OpenShift cluster (>= 4.19)
- OpenShift Virtualization operator installed
- ServiceAccount with RBAC permissions to create VirtualMachine and PVC resources
- Source VM must exist

### Prerequisite Verification

**Before executing:**
1. Verify `openshift-virtualization` in `mcps.json`, `KUBECONFIG` set (never expose value)
2. Optional: Verify RBAC permissions for VirtualMachine, PVC/DataVolume creation

**Human Notification Protocol:** `❌ Cannot execute vm-clone: MCP server 'openshift-virtualization' is not available. Setup: Add to mcps.json, set KUBECONFIG, restart Claude Code. Docs: https://github.com/openshift/openshift-mcp-server`

⚠️ **SECURITY**: Never display KUBECONFIG path or credential values.

## When to Use This Skill

**Trigger this skill when:**
- User explicitly invokes `/vm-clone` command
- User wants to duplicate an existing VM
- User needs to create test/dev copies of production VMs
- User wants to scale horizontally by creating VM copies
- User wants to create VMs from a template VM

**User phrases that trigger this skill:**
- "Clone VM web-server to web-server-test"
- "Create a copy of database-vm"
- "Duplicate production-vm for staging"
- "Make 3 copies of template-vm"
- "/vm-clone" (explicit command)

**Do NOT use this skill when:**
- User wants to create a new VM from scratch → Use `/vm-create` skill instead
- User wants a point-in-time backup → Use snapshots instead
- User wants to move/migrate a VM → Use migration tools instead
- User wants to resize a VM → Modify existing VM instead

## Workflow

### Step 1: Gather Source VM Information

**Required Information from User:**
1. **Source VM Name** - Name of the VM to clone
2. **Source Namespace** - Namespace where source VM exists
3. **Target VM Name** - Name for the cloned VM
4. **Target Namespace** - Namespace for the cloned VM (can be same or different)

If user doesn't provide all information, ask for missing details.

**1.1: Verify Source VM Exists**

**MCP Tool**: `resources_get` (from openshift-virtualization)

**Parameters**:
```json
{
  "apiVersion": "kubevirt.io/v1",
  "kind": "VirtualMachine",
  "namespace": "<source-namespace>",
  "name": "<source-vm-name>"
}
```

**Expected Output**: Complete VirtualMachine resource specification

**Error Handling**:
- If VM not found → Report error, suggest using vm-inventory to find VMs
- If permission denied → Report RBAC error

**1.2: Check Target VM Name Availability**

**MCP Tool**: `resources_get` (from openshift-virtualization)

**Parameters**:
```json
{
  "apiVersion": "kubevirt.io/v1",
  "kind": "VirtualMachine",
  "namespace": "<target-namespace>",
  "name": "<target-vm-name>"
}
```

**If VM exists**: Offer options (choose different name, delete existing VM, cancel), wait for decision

**1.3: Discover Source VM Storage**

Use `resources_list` for DataVolumes (labelSelector: vm.kubevirt.io/name) or PVCs if not found
Parse: Extract storage names, calculate size, determine DataSources vs container disks

### Step 2: Ask User for Cloning Strategy

**Present storage cloning options:**

```markdown
## VM Cloning - Storage Strategy

**Source VM**: `<source-vm-name>` (namespace: `<source-namespace>`)
**Source Storage**: <source-disk> (<size>)

**Select cloning strategy:**

1. **Clone Storage** - Full copy, independent storage (~5-10 min, <size> new allocation)
2. **Reference Existing** - ⚠️ Shared disk (dangerous, both VMs access same storage)
3. **New Empty Storage** - Fresh disk, no data copied (<size> new allocation)
4. **Cancel** - Abort operation

**Select option (1-4):**
```

**Wait for user selection (1-4).**

**Handle response**: "4"/cancel → stop; "1" → clone_storage=true; "2" → warn + share_storage=true; "3" → new_storage=true

**Option 2 warning**: `⚠️ Shared Storage Dangerous - Both VMs share disk, data corruption risk. Only safe if source stopped. Use Option 1 instead. Proceed anyway? (yes/cancel)` Wait for explicit "yes".

### Step 3: Check Namespace Quota and Present Clone Configuration

**3.0: Check ResourceQuota** (before presenting confirmation)

Use `resources_list` (apiVersion="v1", kind="ResourceQuota", namespace=`<target-namespace>`) to check if quotas exist. If a quota is found, compare current usage against limits for CPU, memory, and storage. If the clone would push usage above 80% of any limit, include a warning in the confirmation summary.

**Present configuration summary:**

```markdown
## VM Clone Configuration - Review

**Source**: `<source-vm-name>` (<source-namespace>) - <instance-type>, <cpu> vCPU, <memory>
**Target**: `<target-vm-name>` (<target-namespace>) - Same config, starts Stopped
**Storage**: <strategy-description> - <size> <allocation-details>

**Resource Impact**: <cpu> vCPU, <memory> RAM, <storage> disk

**What changes**: IP addresses, hostname, MAC addresses, firmware UUID
**What's preserved**: Instance type, vCPU/memory, network config, cloud-init

**Proceed with VM cloning? (yes/no)**
```

**Wait for user confirmation.**

**Handle response:**
- If "yes" → Proceed to Step 4 (execute cloning)
- If "no", "cancel", "wait", or anything else → Cancel operation

**On cancellation:**
```markdown
VM cloning cancelled by user. No resources were created.
```

**STOP workflow**.

### Step 4: Execute VM Cloning

**ONLY PROCEED AFTER**: Source VM validated, target name available, user selected storage strategy, user confirmed configuration

**4.1: Prepare Cloned VM Specification**

Modify source VM spec:
1. Change metadata: `name` → target-vm-name, `namespace` → target-namespace; remove `uid`, `resourceVersion`, `creationTimestamp`, `status`
2. Update storage: clone_storage → new DataVolume with source PVC; share_storage → keep PVC refs; new_storage → empty DataVolume
3. Set `runStrategy: Halted` (starts stopped)
4. Generate new firmware UUIDs (`domain.firmware.uuid`, `domain.firmware.serial`)
5. Preserve: instance type, tolerations, network config, cloud-init

**4.2: Create Storage Resources**

**Clone storage** - Use `resources_create_or_update` with DataVolume (source.pvc from source, storage from source class/size)
**New empty storage** - Use `resources_create_or_update` with DataVolume (source.blank, storage from source class/size)

**4.3: Create Cloned VirtualMachine**

Use `resources_create_or_update` with prepared spec from 4.1
**Error handling**: Creation fails → report error, rollback storage; permission denied → RBAC error; namespace missing → namespace error

**4.4: Monitor Storage Cloning Progress**

Use `resources_get` on DataVolume, check `status.phase` (Pending/Succeeded/Failed), report every 30s, wait up to 15 min

### Step 5: Report Cloning Results

**On successful clone:**

```markdown
## ✓ VM Cloned Successfully

**Source**: `<source-vm-name>` (<source-namespace>)
**Target**: `<target-vm-name>` (<target-namespace>) - Status: Stopped (ready to start)
**Config**: <instance-type>, <cpu> vCPU, <memory>, <storage-size>

<if clone_storage=true>
**Storage**: ✓ Cloned in <time> - Independent storage, changes won't affect source
</if>
<if new_storage=true>
**Storage**: ✓ New empty storage created - OS installation may be required
</if>
<if share_storage=true>
**Storage**: ⚠️ Shared PVC `<source-pvc>` - Keep source VM stopped to avoid data corruption
</if>

**Next**: Start with `"Start VM <target-vm-name> in namespace <target-namespace>"`
```

**On cloning failure:**

**Document Consultation** (OPTIONAL - when cloning fails):
- **When to consult**: Storage cloning fails, VM creation fails, PVC clone not supported, storage class issues
- **When NOT to consult**: VM already exists, RBAC errors, namespace not found (clear causes)
- **Action**: Read [storage-errors.md](docs/troubleshooting/storage-errors.md) for VM cloning failures, storage provisioning, DataVolume errors
- **Output to user**: "I consulted [storage-errors.md](docs/troubleshooting/storage-errors.md) to understand potential causes."

```markdown
## ❌ VM Cloning Failed

**Error**: <error-message>
**Source**: `<source-vm-name>` (<source-namespace>) → **Target**: `<target-vm-name>` (<target-namespace>)

**Common Causes**:
- Insufficient storage quota - Namespace lacks storage capacity
- Insufficient RBAC permissions - ServiceAccount lacks create permissions
- Storage class not available - Target namespace cannot access storage class
- PVC clone not supported - Storage class doesn't support cloning
- Source VM still running - Some storage backends require source VM stopped

**Troubleshooting** (see [storage-errors.md](docs/troubleshooting/storage-errors.md)):
1. Check storage quota: `resources_list` for ResourceQuota in target namespace
2. Check permissions: `resources_list` to verify RBAC (note: `oc auth can-i` has no MCP equivalent)
3. Check storage class: `resources_get` for StorageClass config, `resources_list` for available classes
4. Check source VM status: vm-inventory skill `"Show status of VM <source-vm-name>"`
5. Check DataVolume status: `resources_get` for DataVolume phase and status

**Partial Resources** (may need cleanup):
- VirtualMachine: `<target-vm-name>`
- DataVolume: `<target-vm-name>-rootdisk`

**Cleanup**: `"Delete VM <target-vm-name> in namespace <target-namespace>"`

Would you like help troubleshooting this error?
```

## Advanced Features

### Batch Cloning
**User request:** "Create 3 copies of template-vm named web-01, web-02, web-03"
**Limit**: Maximum 5 clones per batch request. If user requests more, refuse and explain the limit exists to prevent resource exhaustion.
**Workflow**: Validate source once, generate/check target names, ask storage strategy once, then process each clone individually through Steps 3-5 with separate confirmation per VM. Stop on first failure.

### Cross-Namespace Cloning
**User request:** "Clone production-vm from production to staging namespace"
**Note**: Storage cloned across namespaces, network policies/quotas may differ, RBAC required in both namespaces

### Clone with Modifications (Future)
Allow modifications during clone: instance type/size, storage size, network config, cloud-init customization

## Common Issues

**Issue 1: Target VM Name Already Exists** - Choose different name, delete existing VM (if safe), use vm-inventory to check

**Issue 2: Insufficient Storage Quota** - Check quotas, request increase, use shared storage (if appropriate), delete unused PVCs

**Issue 3: Storage Class Not Accessible** - Verify storage class exists in target namespace, check cross-namespace cloning support, use different storage class, contact admin

**Issue 4: PVC Clone Not Supported** - Storage class doesn't support CSI volume cloning; use "new empty storage" option, snapshot and restore, or check storage class capabilities

**Issue 5: Source VM Running During Clone** - Stop source VM first, use snapshot-based cloning, check storage backend requirements

## Dependencies

### Required MCP Servers
- `openshift-virtualization` - OpenShift MCP server with core and kubevirt toolsets

### Required MCP Tools
- `resources_get` (from openshift-virtualization) - Get source VM and storage details
  - Parameters: apiVersion, kind, namespace, name
  - Source: https://github.com/openshift/openshift-mcp-server/blob/main/pkg/toolsets/core/resources.go

- `resources_create_or_update` (from openshift-virtualization) - Create cloned VM and storage
  - Parameters: resource (YAML/JSON)
  - Source: https://github.com/openshift/openshift-mcp-server/blob/main/pkg/toolsets/core/resources.go

- `resources_list` (from openshift-virtualization) - List DataVolumes, PVCs, VMs
  - Parameters: apiVersion, kind, namespace, labelSelector
  - Source: https://github.com/openshift/openshift-mcp-server/blob/main/pkg/toolsets/core/resources.go

### Related Skills
- `vm-create` - Create new VMs from scratch (alternative to cloning)
- `vm-inventory` - List and verify source/target VMs
- `vm-lifecycle-manager` - Start cloned VMs after creation
- `vm-delete` - Clean up failed clones or unwanted copies

### Reference Documentation
- [storage-errors.md](docs/troubleshooting/storage-errors.md) - VM cloning failure scenarios, storage provisioning issues, and DataVolume cloning errors (optionally consulted when cloning operations fail)
- [Troubleshooting INDEX](docs/troubleshooting/INDEX.md) - Navigation hub for discovering additional error categories when encountering unexpected issues outside the categories above
- [OpenShift Virtualization Cloning](https://docs.redhat.com/en/documentation/openshift_container_platform/4.21/html-single/virtualization/index#virt/virtual_machines/cloning_vms/virt-cloning-vm.html)
- [DataVolume Cloning](https://github.com/kubevirt/containerized-data-importer/blob/main/doc/datavolumes.md#cloning)
- [KubeVirt VirtualMachine API](https://kubevirt.io/api-reference/)
- [CSI Volume Cloning](https://kubernetes.io/docs/concepts/storage/volume-pvc-datasource/)

## Critical: Human-in-the-Loop Requirements

**IMPORTANT:** This skill creates new resources that consume cluster capacity. You MUST:

1. **Before Cloning**
   - Verify source VM exists and get full configuration
   - Ask user for clone configuration (name, namespace, storage strategy)
   - Present clone preview with resource impact
   - Wait for explicit user confirmation

2. **Configuration Confirmation**
   - Display source VM details
   - Show target VM configuration
   - Indicate storage cloning strategy
   - Estimate resource consumption (CPU, memory, storage)
   - Ask: "Proceed with VM cloning? (yes/no)"
   - Wait for explicit "yes"

3. **Never Auto-Execute**
   - **NEVER clone without user confirmation**
   - **NEVER assume storage strategy** - always ask user
   - **NEVER proceed if user says "no", "wait", "cancel"**

**Why This Matters:**
- **Resource Consumption**: Clones consume cluster resources (CPU, memory, storage)
- **Storage Costs**: Storage cloning can consume significant disk space
- **Naming Conflicts**: Duplicate names cause errors
- **Network Configuration**: May need adjustment for clones

## Security Considerations

- **RBAC Enforcement**: Requires create permissions in target namespace
- **Namespace Isolation**: Cannot clone across namespaces without proper permissions
- **Storage Quotas**: Respects namespace storage quotas
- **MAC Address Generation**: Automatic generation prevents MAC conflicts
- **UUID Generation**: New firmware UUIDs prevent conflicts
- **No Credential Exposure**: KUBECONFIG never exposed in output
- **Audit Trail**: All cloning operations logged in Kubernetes API audit logs

## Example Usage

### Example 1: Simple Clone with Storage

```
User: "Clone web-server to web-server-test in namespace dev"

Agent: [Validates source VM web-server (production), checks target name availability]
       [Discovers 50Gi storage, presents storage options]
       "Select storage strategy (1-4):"

User: "1"

Agent: [Shows: Source web-server (u1.medium, 2 vCPU, 4Gi) → Target web-server-test (dev, 50Gi clone)]
       "Proceed with VM cloning? (yes/no)"

User: "yes"

Agent: "📦 Creating storage... ⏳ Cloning (5-10 min)..."
       "✓ VirtualMachine web-server-test created in dev"
       "⏳ Storage cloning... Succeeded"
       "✓ VM Cloned Successfully - Source: web-server (production), Target: web-server-test (dev)"
       "Storage: ✓ Cloned in 7m23s - Independent storage"
       "Next: Start VM web-server-test in namespace dev"
```

### Example 2: Clone with New Empty Storage

```
User: "Clone template-vm to app-01 with empty storage"

Agent: [Validation complete, presents options]
       "Select storage strategy (1-4):"

User: "3"

Agent: "Proceed with VM cloning? (yes/no)"

User: "yes"

Agent: "✓ VM Cloned Successfully"
       "Storage: ✓ New empty storage created - OS installation may be required"
```

### Example 3: Batch Cloning

```
User: "Create 3 copies of template-vm named web-01, web-02, web-03 in production"

Agent: [Validates source, checks all names, asks storage strategy once]
       "Storage strategy for all clones: Clone Storage (1)"

       ## Clone 1 of 3: web-01
       "Source: template-vm → Target: web-01 (production), 30Gi clone"
       "Proceed with VM cloning? (yes/no)"
User: "yes"
Agent: "✓ web-01 cloned"

       ## Clone 2 of 3: web-02
       "Source: template-vm → Target: web-02 (production), 30Gi clone"
       "Proceed with VM cloning? (yes/no)"
User: "yes"
Agent: "✓ web-02 cloned"

       [... repeats for each VM with individual confirmation ...]
```

### Example 4: Shared Storage Warning

```
User: "Clone db-vm to db-test"

Agent: "Select storage strategy (1-4):"

User: "2"

Agent: "⚠️ WARNING: Shared Storage is Dangerous"
       "Risks: Data corruption if both VMs run simultaneously"
       "Proceed with shared storage anyway? (yes/cancel)"

User: "cancel"

Agent: "VM cloning cancelled. No resources created."
```
