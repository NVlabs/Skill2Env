---
name: vm-create
description: |
  Create new virtual machines in OpenShift Virtualization with automatic instance type resolution and OS selection.

  Use when:
  - "Create a new VM"
  - "Deploy a virtual machine with [OS]"
  - "Set up a VM in namespace [name]"
  - "Provision a [size] VM"

  This skill handles VM creation with intelligent defaults for OpenShift Virtualization.

  NOT for managing existing VMs (use vm-lifecycle-manager or vm-delete instead).

license: Apache-2.0
model: inherit
color: green
allowed-tools: vm_create resources_get resources_list namespaces_list events_list vm_lifecycle resources_create_or_update
---

# /vm-create Skill

Create virtual machines in OpenShift Virtualization using the `vm_create` tool from the openshift-virtualization MCP server.

## Prerequisites

**Required MCP Server**: `openshift-virtualization` ([OpenShift MCP Server](https://github.com/openshift/openshift-mcp-server))

**Required MCP Tools**:
- `vm_create` (from openshift-virtualization) - Create VirtualMachine resources
- `resources_get` (from openshift-virtualization) - Check VM existence and status
- `resources_list` (from openshift-virtualization) - List StorageClasses
- `namespaces_list` (from openshift-virtualization) - List available namespaces
- `events_list` (from openshift-virtualization) - Diagnostic event gathering
- `vm_lifecycle` (from openshift-virtualization) - VM restart for workarounds

**Required Environment Variables**:
- `KUBECONFIG` - Path to Kubernetes configuration file with cluster access

**Required Cluster Setup**:
- OpenShift cluster (>= 4.19)
- OpenShift Virtualization operator installed
- ServiceAccount with RBAC permissions to create VirtualMachine resources
- Namespace with appropriate permissions

### Prerequisite Verification

**Before executing:**
1. Check `openshift-virtualization` exists in `mcps.json` → If missing, report setup instructions
2. Verify `KUBECONFIG` is set (check presence only, never expose value) → If missing, report to user

**Human Notification Protocol:** `❌ Cannot execute vm-create: MCP server 'openshift-virtualization' not available. Setup: Add to mcps.json, set KUBECONFIG env var, restart Claude Code. Docs: https://github.com/openshift/openshift-mcp-server`

⚠️ **SECURITY**: Never display KUBECONFIG path or credential values.

## When to Use This Skill

**Trigger this skill when:**
- User explicitly invokes `/vm-create` command
- User requests creating a new virtual machine
- Deploying VMs with specific OS (Fedora, Ubuntu, RHEL, CentOS, Debian)
- Setting up VMs with custom sizing (small, medium, large)
- Provisioning VMs with specific storage requirements

**User phrases:**
- "Create a Fedora VM in namespace vms"
- "Deploy a medium Ubuntu VM with 100Gi disk"
- "Set up a RHEL VM called database-01"
- "/vm-create" (explicit command)

**Do NOT use when:**
- Start/stop existing VMs → Use `/vm-lifecycle-manager`
- List VMs → Use `/vm-inventory`
- Delete VMs → Use `/vm-delete`

## Workflow

### Step 1: Gather VM Requirements

**Determine missing parameters:**

**Required:** VM Name (validate: lowercase, alphanumeric+hyphens, start letter, max 63 chars, unique), Namespace
**Optional (use defaults):** OS (fedora), Size (medium), Storage (30Gi), Performance (u1), Autostart (false)

**Gather cluster info:**
- List namespaces: `namespaces_list` (from openshift-virtualization) — ask user to select if not provided
- List StorageClasses: `resources_list` with apiVersion="storage.k8s.io/v1", kind="StorageClass"
- Identify default SC: annotation `storageclass.kubernetes.io/is-default-class`="true"
- Analyze SC: `.volumeBindingMode` (Immediate/WaitForFirstConsumer), provisioner (rbd/cephfs=RWX hint)

**If parameters missing, use AskUserQuestion tool with questions for:** VM Name (custom input with validation), Namespace (current + list), OS (fedora/ubuntu/rhel/centos-stream/debian/opensuse), Performance (u1/c1/m1/o1), Size (small/medium/large/xlarge), Storage (30Gi/50Gi/100Gi/custom), StorageClass (dynamic list with hints), Autostart (yes/no). See Example Usage for complete JSON structure.

**Process responses - map labels to values:**
- OS: "Fedora"→`"fedora"`, "Ubuntu"→`"ubuntu"`, "RHEL"→`"rhel"`, "CentOS Stream"→`"centos-stream"`, "Debian"→`"debian"`, "OpenSUSE"→`"opensuse"`
- Performance: "General Purpose (u1)"→`"u1"`, "Compute (c1)"→`"c1"`, "Memory (m1)"→`"m1"`, "Overcommitted (o1)"→`"o1"`
- Size: "Small"→`"small"`, "Medium"→`"medium"`, "Large"→`"large"`, "XLarge"→`"xlarge"`
- Autostart: "No"→`false`, "Yes"→`true`

### Step 2: Check VM Existence

**MCP Tool**: `resources_get` (from openshift-virtualization)
**Parameters**: apiVersion="kubevirt.io/v1", kind="VirtualMachine", namespace=`<namespace>`, name=`<vm-name>`

**If VM exists:**
```
⚠️ VM `<name>` already exists in namespace `<namespace>`
Status: <status>
Options: 1) Different name, 2) Delete existing, 3) Cancel
```
**STOP** and wait for user decision.

**If not exists:** Proceed to Step 3.

### Step 3: Present Configuration for Confirmation

Display configuration table:
```markdown
## Virtual Machine Configuration

| Parameter | Value | Notes |
|-----------|-------|-------|
| VM Name | `<name>` | validated |
| Namespace | `<namespace>` | from user/context |
| OS | `<os>` | from selection |
| Performance | `<perf>` | default: u1 |
| Size | `<size>` | default: medium |
| Storage | `<storage>` | default: 30Gi |
| StorageClass | `<sc>` | default: cluster default |
| Autostart | `<yes/no>` | default: no |

This will create a VirtualMachine consuming cluster resources.
Confirm: yes/no/modify
```

**WAIT** for explicit user confirmation before proceeding.

### Step 4: Create Virtual Machine

**MCP Tool**: `vm_create` (from openshift-virtualization)

**Parameters**:
- `namespace`: `<namespace>` - REQUIRED
- `name`: `<vm-name>` - REQUIRED
- `workload`: `<os>` - OPTIONAL (default: fedora)
- `size`: `<size>` - OPTIONAL (small/medium/large/xlarge)
- `storage`: `<storage>` - OPTIONAL (default: 30Gi)
- `performance`: `<perf>` - OPTIONAL (u1/c1/m1/o1)
- `autostart`: `<bool>` - OPTIONAL (default: false)

**Example**: `vm_create({"namespace": "vms", "name": "web-server", "workload": "fedora", "size": "medium", "storage": "50Gi", "autostart": false})`

**Error Handling:**
- Namespace not found → Report, list available
- RBAC denied → Report permissions error
- Storage fails → Check StorageClass exists
- Scheduling fails → See Step 5

### Step 5: Verify Status and Diagnose Issues

**Wait 5-10 seconds, then check status:**

**MCP Tool**: `resources_get` (apiVersion="kubevirt.io/v1", kind="VirtualMachine", name=`<name>`, namespace=`<namespace>`)
**Extract**: `.status.printableStatus`

**Status interpretation:**
- Stopped/Halted → Success (VM created, not started)
- Running → Success (if autostart=true)
- Provisioning → Wait 5s, check again (max 3 retries, then report status as "still provisioning" and suggest the user check back later)
- ErrorUnschedulable → Execute diagnostic workflow (Step 5a)
- ErrorDataVolumeNotReady → Storage issue (see Common Issues)

#### 5a. Diagnostic Workflow (ErrorUnschedulable)

**CRITICAL: Document Consultation FIRST:**
1. Read [scheduling-errors.md](docs/troubleshooting/scheduling-errors.md) using Read tool
2. Output: "I detected ErrorUnschedulable. I consulted [scheduling-errors.md] to understand diagnosis strategies."

**Gather diagnostics:**
- List events: `events_list` (namespace=`<namespace>`) → Filter for VM/VMI
- Get VM: `resources_get` → Check `.status.conditions`
- List nodes: `resources_list` (apiVersion="v1", kind="Node") → Extract `.spec.taints`

**Parse root cause:**
- "taints" in events → Taints/tolerations issue
- "Insufficient cpu/memory" → Resource constraints
- "no nodes available" → No suitable nodes

**Present diagnosis:**
```markdown
## ⚠️ VM Scheduling Issue Detected

**Status**: ErrorUnschedulable | **Root Cause**: <identified-cause> | **Details**: <specifics>

### Recommended Solution
<workaround-description>
**Action**: Update VM via `resources_create_or_update`
**Impact**: <what-changes>
**Options**: 1) Apply workaround, 2) Manual, 3) Cancel, 4) Ignore
⚠️ MCP limitation: vm_create doesn't support tolerations
```

**Wait for user decision.**

**If user confirms:**
1. Apply patch: `resources_create_or_update` (fetch, add tolerations, update)
2. Verify: `resources_get` → Check `.spec.template.spec.tolerations`
3. **Restart VM**: `vm_lifecycle` (action="restart") to apply new spec
4. Wait 15-20s, check status → Stopped → Provisioning → Running

**Report**: `## ✓ Workaround Applied | **Action**: Added tolerations, restarted | **Status**: <current>`

### Step 6: Report Creation Status

**On success:**
```markdown
## ✓ Virtual Machine Created Successfully

**VM**: `<name>` (namespace: `<namespace>`)
**OS**: <os> | **Size**: <size> (<perf>) | **Storage**: <storage> | **Status**: <status>
**Provisioning**: ~2-5 min (Provisioning → Stopped)

### Next Steps
Start: "Start VM <name>" | View: "Show VM <name>"

### Accessing the VM
1. Serial: `virtctl console <name> -n <ns>`
2. VNC: OpenShift Console → Virtualization → VMs → <name> → Console
3. SSH: Get IP from VMI, `ssh <user>@<ip>`
4. Port Forward: `virtctl port-forward vmi/<name> -n <ns> 8080:80`

### Default Credentials
- Fedora: fedora | Ubuntu: ubuntu | RHEL: cloud-user | CentOS: centos | Debian: debian
- All require SSH key or console password set: `virtctl console <name>`, `sudo passwd <user>`
```

**On failure:**
```markdown
## ❌ Failed to Create Virtual Machine

**Error**: <error-message>

**Common Causes**:
- Namespace not exists → Create via `resources_create_or_update`
- RBAC denied → Check ServiceAccount permissions
- Resource constraints → Try smaller size
- Invalid parameters → Verify OS, size, storage format
- Operator not installed → Verify CSVs

Troubleshooting: See Common Issues
```

## Common Issues

### Issue 1: Namespace Not Found
**Error**: "Namespace 'xyz' not found"
**Solution**: List with `namespaces_list`, create with `resources_create_or_update`

### Issue 2: Insufficient Permissions
**Error**: "Forbidden: User cannot create VirtualMachines"
**Solution**: Verify KUBECONFIG RBAC, requires create VirtualMachine permissions, contact admin

### Issue 3: Resource Constraints (ErrorUnschedulable)
**Error**: "0/N nodes: Insufficient cpu/memory"
**Solution**: Check `nodes_top`, try smaller size (medium→small, o1 overcommitted), scale cluster

### Issue 4: Node Taints (ErrorUnschedulable)
**Error**: "0/N nodes: taints pod didn't tolerate"
**Solution**: Apply tolerations workaround (Step 5a), restart VM

### Issue 5: Storage Provisioning (ErrorDataVolumeNotReady)
**Error**: "PVC pending" or "StorageClass not found"
**Solution**: Verify SC (`resources_list`), check default annotation, verify provisioner, check quotas

### Issue 6: DataVolume Import Failure
**Error**: "DataVolume import failed" or "image pull error"
**Solution**: Verify internet access, check DV status, ensure valid OS, verify registry auth

### Issue 7: Operator Not Installed
**Error**: "VirtualMachine CRD not found"
**Solution**: Verify operator: `resources_list` (apiVersion="operators.coreos.com/v1alpha1", kind="CSV", namespace="openshift-cnv")

## Dependencies

### Required MCP Servers
- `openshift-virtualization` - OpenShift MCP server with KubeVirt toolset (https://github.com/openshift/openshift-mcp-server)

### Required MCP Tools
- `vm_create` - Create VMs (namespace, name, workload, size, storage, performance, autostart)
- `resources_get` - Get resources (apiVersion, kind, namespace, name)
- `resources_list` - List resources (apiVersion, kind, namespace optional)
- `namespaces_list` - List namespaces
- `events_list` - List events (namespace)
- `vm_lifecycle` - VM lifecycle (namespace, name, action: start/stop/restart)
- `resources_create_or_update` - Update resources (JSON)

### Related Skills
- `vm-lifecycle-manager` - Start VMs | `vm-inventory` - List VMs | `vm-delete` - Delete VMs | `vm-clone` - Clone VMs | `vm-snapshot-create` - Snapshot VMs

### Reference Documentation
- [scheduling-errors.md](docs/troubleshooting/scheduling-errors.md) - ErrorUnschedulable (consulted Step 5a)
- [storage-errors.md](docs/troubleshooting/storage-errors.md) - ErrorDataVolumeNotReady
- [network-errors.md](docs/troubleshooting/network-errors.md) - Network failures
- [runtime-errors.md](docs/troubleshooting/runtime-errors.md) - CrashLoopBackOff
- [Troubleshooting INDEX](docs/troubleshooting/INDEX.md) - Full error index
- [OpenShift Virt Docs](https://docs.redhat.com/en/documentation/openshift_container_platform/4.21/html-single/virtualization/index)
- [KubeVirt API](https://kubevirt.io/api-reference/)
- [OpenShift MCP](https://github.com/openshift/openshift-mcp-server)

## Critical: Human-in-the-Loop Requirements

**IMPORTANT:** This skill creates cluster resources consuming CPU, memory, storage. You MUST:

1. **Before Creating**
   - Display complete configuration in table format
   - Show resource impact
   - Ask: "Confirm: yes/no/modify"
   - Wait for explicit confirmation

2. **Never Auto-Execute**
   - NEVER create VMs without displaying configuration
   - NEVER assume approval
   - NEVER create multiple VMs without individual confirmations

**Why**: Resource consumption, cost impact, namespace quotas

**Rationale**: Prevents unintended resource consumption; maintains user control.

## Security Considerations

- **RBAC**: Requires create VirtualMachines (kubevirt.io/v1) in namespace
- **Namespace Isolation**: VMs in specified namespace only
- **Storage Quotas**: Respects ResourceQuotas
- **Image Security**: Default OS options (fedora, ubuntu, rhel, centos-stream, debian, opensuse) use upstream container disk images. Custom images via the `workload` parameter are not validated — warn the user when a custom image URL is provided and confirm the source is trusted before proceeding
- **KUBECONFIG**: Never exposed (presence only)
- **Audit**: All ops logged via K8s audit

## Example Usage

### Example 1: Complete Interactive Workflow

```
User: "Create a VM"
Agent: [No params, detects namespace: production, queries SCs]
       [AskUserQuestion with all 8 questions - see JSON below]
[User selects: my-app-server, production, fedora, u1, medium, 30Gi, default SC, no]
Agent: [Validates ✓, checks existence ✓, shows configuration table]
User: "yes"
Agent: [vm_create(...)]
## ✓ Virtual Machine Created Successfully
[Details, next steps, access instructions]
```

**AskUserQuestion JSON (8 questions: VM Name, Namespace, OS, Performance, Size, Storage, StorageClass, Autostart):**
```json
{"questions": [
  {"question": "VM name?", "header": "VM Name", "multiSelect": false, "options": [{"label": "Enter custom name", "description": "Lowercase, alphanumeric+hyphens, start letter, max 63"}]},
  {"question": "Namespace?", "header": "Namespace", "multiSelect": false, "options": [{"label": "<current> (Current)", "description": "From kubeconfig"}, {"label": "Other", "description": "<list>"}]},
  {"question": "OS?", "header": "OS", "multiSelect": false, "options": [{"label": "Fedora (Recommended)", "description": "General purpose"}, {"label": "Ubuntu", "description": "Web services"}, {"label": "RHEL", "description": "Enterprise"}, {"label": "CentOS Stream", "description": "Upstream RHEL"}, {"label": "Debian", "description": "Stable minimal"}, {"label": "OpenSUSE", "description": "Community"}]},
  {"question": "Performance?", "header": "Performance", "multiSelect": false, "options": [{"label": "General (u1) (Recommended)", "description": "Balanced - most workloads"}, {"label": "Compute (c1)", "description": "CPU-intensive"}, {"label": "Memory (m1)", "description": "Memory-intensive"}, {"label": "Overcommitted (o1)", "description": "Dev/test"}]},
  {"question": "Size?", "header": "Size", "multiSelect": false, "options": [{"label": "Small", "description": "1 vCPU, 2Gi"}, {"label": "Medium (Recommended)", "description": "2-4 vCPU, 4-8Gi"}, {"label": "Large", "description": "4-8 vCPU, 8-16Gi"}, {"label": "XLarge", "description": "8+ vCPU, 16+ Gi"}]},
  {"question": "Storage?", "header": "Storage", "multiSelect": false, "options": [{"label": "30Gi (Recommended)", "description": "Most workloads"}, {"label": "50Gi", "description": "Moderate needs"}, {"label": "100Gi", "description": "Large requirements"}, {"label": "Custom", "description": "Specify (e.g., 75Gi)"}]},
  {"question": "StorageClass?", "header": "SC", "multiSelect": false, "options": [{"label": "<default> (Default)", "description": "<perf-hint>, <migration-hint>"}, {"label": "<sc-1>", "description": "<hints>"}]},
  {"question": "Autostart?", "header": "Autostart", "multiSelect": false, "options": [{"label": "No (Recommended)", "description": "Start manually"}, {"label": "Yes", "description": "Auto-start"}]}
]}
```

### Example 2: Partial Parameters

```
User: "Create Ubuntu VM web-01 in apps"
Agent: [Detects: web-01, apps, ubuntu; Asks: Performance, Size, Storage, SC, Autostart]
[User: u1, large, 100Gi, local-storage, yes]
Agent: [Validates, shows config]
User: "yes"
Agent: [Creates with autostart=true]
## ✓ Virtual Machine Created and Starting
```

### Example 3: User Modifies Config

```
User: "Deploy memory-optimized RHEL VM db-server in production"
Agent: [Detects: db-server, production, rhel, m1; Asks: Size, Storage, SC, Autostart]
[User: large, 100Gi, ceph-rbd, no]
Agent: [Shows config]
User: "Actually, compute-optimized and autostart"
Agent: [Updates: c1, yes; Shows updated]
User: "yes"
Agent: [Creates]
```

## Advanced Features

**Custom Images**: `vm_create({"workload": "quay.io/containerdisks/fedora:latest", ...})` — ⚠️ When a custom image URL is provided, warn the user that image provenance is not verified and confirm the source is trusted before creating the VM
**Secondary Networks**: `vm_create({"networks": ["vlan-network"], ...})` or `{"networks": [{"name": "eth1", "networkName": "vlan"}], ...}`
**Explicit Instance Type**: `vm_create({"instancetype": "u1.large", ...})`
