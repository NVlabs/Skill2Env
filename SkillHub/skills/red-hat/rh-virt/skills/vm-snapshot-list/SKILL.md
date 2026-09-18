---
name: vm-snapshot-list
description: |
  List virtual machine snapshots across namespaces with status, age, and recovery information.

  Use when:
  - "List snapshots for VM [name]"
  - "Show snapshots in namespace [name]"
  - "What snapshots exist for [vm]?"

  Read-only operation - no user confirmation required.

  NOT for creating/deleting snapshots (use vm-snapshot-create/delete instead).

license: Apache-2.0
model: inherit
color: cyan
allowed-tools: resources_list resources_get
---

# /vm-snapshot-list Skill

List virtual machine snapshots in OpenShift Virtualization. This read-only skill displays snapshot information including status, age, size, and recovery options.

## Prerequisites

**Required MCP Server**: `openshift-virtualization` ([OpenShift MCP Server](https://github.com/openshift/openshift-mcp-server))

**Required MCP Tools**:
- `resources_list` (from openshift-virtualization) - List VirtualMachineSnapshot resources
- `resources_get` (from openshift-virtualization) - Get snapshot details

**Required Environment Variables**:
- `KUBECONFIG` - Path to Kubernetes configuration file with cluster access

**Required Cluster Setup**:
- OpenShift cluster (>= 4.19)
- OpenShift Virtualization operator installed
- ServiceAccount with RBAC permissions to list VirtualMachineSnapshot resources

### Prerequisite Verification

**Before executing, verify MCP server availability:**

1. **Check MCP Server Configuration**
   - Verify `openshift-virtualization` exists in `mcps.json`
   - If missing → Report to user with setup instructions

2. **Check Environment Variables**
   - Verify `KUBECONFIG` is set (check presence only, never expose value)
   - If missing → Report to user

**Human Notification Protocol:**

When prerequisites fail:

```
❌ Cannot execute vm-snapshot-list: MCP server 'openshift-virtualization' is not available

📋 Setup Instructions:
1. Add openshift-virtualization to mcps.json
2. Set KUBECONFIG environment variable
3. Restart Claude Code to reload MCP servers

🔗 Documentation: https://github.com/openshift/openshift-mcp-server
```

## When to Use This Skill

**Trigger this skill when:**
- User wants to list available snapshots for recovery
- User wants to see snapshot status and age
- User wants to verify snapshot existence before restore
- User wants to identify old snapshots for deletion

**User phrases that trigger this skill:**
- "List all snapshots for web-server VM"
- "Show snapshots in namespace production"
- "What snapshots exist?"
- "Display VM snapshots"

**Do NOT use this skill when:**
- User wants to create a snapshot → Use `vm-snapshot-create` skill
- User wants to restore from snapshot → Use `vm-snapshot-restore` skill
- User wants to delete snapshots → Use `vm-snapshot-delete` skill

## Workflow

### Step 1: Gather Information

**Required Information from User:**
1. **Namespace** - Namespace to list snapshots from
2. **VM Name** (Optional) - Filter snapshots by specific VM

If user doesn't provide namespace, ask for it.

### Step 2: List Snapshots

**MCP Tool**: `resources_list` (from openshift-virtualization)

**Parameters** (with VM filter using label selector):
```json
{
  "apiVersion": "snapshot.kubevirt.io/v1beta1",
  "kind": "VirtualMachineSnapshot",
  "namespace": "<namespace>",
  "labelSelector": "vm.kubevirt.io/name=<vm-name>"
}
```

**Parameters** (all snapshots in namespace):
```json
{
  "apiVersion": "snapshot.kubevirt.io/v1beta1",
  "kind": "VirtualMachineSnapshot",
  "namespace": "<namespace>"
}
```

**Note**: The label selector `vm.kubevirt.io/name=<vm-name>` may not always exist. If no results are returned, fall back to listing all snapshots and filtering by checking `spec.source.name` field in the results.

**Expected Output**: List of VirtualMachineSnapshot resources

**Parse each snapshot to extract**:
- `metadata.name` - Snapshot name
- `metadata.namespace` - Namespace
- `metadata.creationTimestamp` - Creation time
- `spec.source.name` - VM name
- `status.phase` - Status (InProgress, Succeeded, Failed)
- `status.readyToUse` - Ready for restore (true/false)

**Error Handling**:
- If namespace not found → Report error
- If permission denied → Report RBAC error
- If no snapshots found → Report "No snapshots found"

### Step 3: Report Snapshot List

**If snapshots found:**

```markdown
## VM Snapshots

**Namespace**: `<namespace>`
<if vm_name provided>
**VM**: `<vm-name>`
</if>

### Available Snapshots

| Snapshot Name | VM Name | Status | Created | Age | ReadyToUse |
|---------------|---------|--------|---------|-----|------------|
| `pre-upgrade-snapshot` | `database-01` | Succeeded ✓ | 2024-01-15 10:30 | 2 days | true |
| `backup-snapshot` | `database-01` | Succeeded ✓ | 2024-01-10 08:00 | 7 days | true |
| `test-snapshot` | `web-server` | Succeeded ✓ | 2024-01-14 14:20 | 3 days | true |

**Total Snapshots**: 3

---

### Snapshot Details

**Snapshot: `pre-upgrade-snapshot`**
- **VM**: `database-01`
- **Status**: Succeeded ✓
- **Created**: 2024-01-15 10:30:00 UTC
- **Age**: 2 days
- **Ready to Use**: true

**Snapshot: `backup-snapshot`**
- **VM**: `database-01`
- **Status**: Succeeded ✓
- **Created**: 2024-01-10 08:00:00 UTC
- **Age**: 7 days
- **Ready to Use**: true

**Snapshot: `test-snapshot`**
- **VM**: `web-server`
- **Status**: Succeeded ✓
- **Created**: 2024-01-14 14:20:00 UTC
- **Age**: 3 days
- **Ready to Use**: true

---

### Actions

**To restore from a snapshot:**
```
"Restore VM <vm-name> from snapshot <snapshot-name>"
```

**To delete a snapshot:**
```
"Delete snapshot <snapshot-name>"
```

**To create a new snapshot:**
```
"Create snapshot of VM <vm-name>"
```
```

**If no snapshots found:**

```markdown
## VM Snapshots

**Namespace**: `<namespace>`
<if vm_name provided>
**VM**: `<vm-name>`
</if>

**No snapshots found.**

<if vm_name provided>
No snapshots exist for VM `<vm-name>` in namespace `<namespace>`.
</if>
<else>
No snapshots exist in namespace `<namespace>`.
</else>

**To create a snapshot:**
```
"Create snapshot of VM <vm-name>"
```
```

## Common Issues

### Issue 1: Permission Denied

**Error**: "Forbidden: User lacks permissions to list virtualmachinesnapshots"

**Cause**: Missing RBAC permissions for listing snapshots.

**Solution:**
1. Check permissions: `oc auth can-i list virtualmachinesnapshots -n <namespace>`
2. Contact cluster admin to grant list/get permissions for virtualmachinesnapshots
3. Try listing in a different namespace where you have permissions

### Issue 2: No Snapshots Found

**Error**: "No snapshots exist in namespace `<namespace>`"

**Cause**: Namespace has no snapshots, or wrong namespace.

**Solution:**
1. Verify correct namespace name
2. List snapshots without VM filter to see all snapshots
3. Check other namespaces: Use `namespaces_list` to see available namespaces
4. Check if snapshots were recently deleted: Use `events_list` in namespace

### Issue 3: Snapshot Shows Failed Status

**Error**: Snapshot listed but `status.phase: Failed` or `readyToUse: false`

**Cause**: Snapshot creation failed due to storage issues, hot-plugged volumes, or missing VolumeSnapshotClass.

**Solution:**
1. Get snapshot details: Use `resources_get` to check `status.conditions` for error messages
2. Check cluster events: Use `events_list` for snapshot-related errors
3. Common fixes:
   - VolumeSnapshotClass missing: Contact cluster admin
   - Hot-plugged volumes: Stop VM, persist volumes, recreate snapshot
   - Failed permanently: Delete and recreate snapshot

## Dependencies

### Required MCP Servers
- `openshift-virtualization` - OpenShift MCP server with kubevirt toolset

### Required MCP Tools
- `resources_list` (from openshift-virtualization) - List Kubernetes resources by type
  - Used for: Listing VirtualMachineSnapshot resources
  - Parameters: apiVersion, kind, namespace, labelSelector (optional)
  - Source: https://github.com/openshift/openshift-mcp-server

### Related Skills
- `vm-snapshot-create` - Create VM snapshots
- `vm-snapshot-restore` - Restore VMs from snapshots
- `vm-snapshot-delete` - Delete VM snapshots
- `vm-inventory` - List VMs before creating snapshots

### Reference Documentation
- [OpenShift Virtualization Snapshots](https://docs.redhat.com/en/documentation/openshift_container_platform/4.21/html-single/virtualization/index#virt-managing-vm-snapshots)
- [KubeVirt VM Snapshots](https://kubevirt.io/user-guide/operations/snapshot_restore_api/)

## Security Considerations

- **RBAC Enforcement**: Requires list permissions for VirtualMachineSnapshot resources
- **Namespace Isolation**: Only lists snapshots within specified namespace
- **Read-Only Operation**: No modifications or destructive actions
- **KUBECONFIG Security**: Credentials never exposed in output

## Example Usage

### Example 1: List Snapshots for Specific VM

```
User: "List all snapshots for database-01"

Agent: "Which namespace is database-01 in?"

User: "production"

Agent: [Invokes vm-snapshot-list skill]
       [Lists snapshots with VM filter]

## VM Snapshots

**Namespace**: `production`
**VM**: `database-01`

### Available Snapshots

| Snapshot Name | VM Name | Status | Created | Age | ReadyToUse |
|---------------|---------|--------|---------|-----|------------|
| `database-01-pre-upgrade` | `database-01` | Succeeded ✓ | 2024-01-15 10:30 | 2 hours | true |
| `database-01-daily-backup` | `database-01` | Succeeded ✓ | 2024-01-14 02:00 | 1 day | true |

**Total Snapshots**: 2

---

### Snapshot Details

**Snapshot: `database-01-pre-upgrade`**
- **VM**: `database-01`
- **Status**: Succeeded ✓
- **Created**: 2024-01-15 10:30:00 UTC
- **Age**: 2 hours
- **Ready to Use**: true

**Snapshot: `database-01-daily-backup`**
- **VM**: `database-01`
- **Status**: Succeeded ✓
- **Created**: 2024-01-14 02:00:00 UTC
- **Age**: 1 day
- **Ready to Use**: true

---

### Actions

**To restore from a snapshot:**
"Restore VM database-01 from snapshot <snapshot-name>"

**To delete a snapshot:**
"Delete snapshot <snapshot-name>"

**To create a new snapshot:**
"Create snapshot of VM database-01"
```

### Example 2: List All Snapshots in Namespace

```
User: "Show me all snapshots in namespace production"

Agent: [Invokes vm-snapshot-list skill]
       [Lists all snapshots without VM filter]

## VM Snapshots

**Namespace**: `production`

### Available Snapshots

| Snapshot Name | VM Name | Status | Created | Age | ReadyToUse |
|---------------|---------|--------|---------|-----|------------|
| `database-01-pre-upgrade` | `database-01` | Succeeded ✓ | 2024-01-15 10:30 | 2 hours | true |
| `database-01-daily-backup` | `database-01` | Succeeded ✓ | 2024-01-14 02:00 | 1 day | true |
| `web-server-backup` | `web-server` | Succeeded ✓ | 2024-01-13 03:00 | 2 days | true |

**Total Snapshots**: 3

VMs with snapshots: `database-01` (2), `web-server` (1)
```

### Example 3: No Snapshots Found

```
User: "List snapshots for test-vm"

Agent: "Which namespace is test-vm in?"

User: "dev"

Agent: [Invokes vm-snapshot-list skill]
       [Lists snapshots - none found]

## VM Snapshots

**Namespace**: `dev`
**VM**: `test-vm`

**No snapshots found.**

No snapshots exist for VM `test-vm` in namespace `dev`.

**To create a snapshot:**
"Create snapshot of VM test-vm"
```
