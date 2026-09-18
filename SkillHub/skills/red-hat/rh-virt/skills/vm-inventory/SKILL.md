---
name: vm-inventory
description: |
  List and view virtual machines across namespaces with status, resource usage, and health information.

  Use when:
  - "List all VMs"
  - "Show VMs in namespace [name]"
  - "What VMs are running?"
  - "Get details of VM [name]"

  This skill provides comprehensive VM inventory and status reporting.

  NOT for creating or modifying VMs (use vm-create or vm-lifecycle-manager instead).

license: Apache-2.0
model: inherit
color: cyan
allowed-tools: resources_list resources_get
---

# /vm-inventory Skill

List and inspect virtual machines in OpenShift Virtualization clusters. This skill provides read-only access to VM information without making any modifications.

## Prerequisites

**Required MCP Server**: `openshift-virtualization` ([OpenShift MCP Server](https://github.com/openshift/openshift-mcp-server))

**Required MCP Tools**:
- `resources_list` (from openshift-virtualization) - List Kubernetes resources including VirtualMachines
- `resources_get` (from openshift-virtualization) - Get specific Kubernetes resource details

**Required Environment Variables**:
- `KUBECONFIG` - Path to Kubernetes configuration file with cluster access

**Required Cluster Setup**:
- OpenShift cluster (>= 4.19)
- OpenShift Virtualization operator installed
- ServiceAccount with RBAC permissions to list and get VirtualMachine resources

### Prerequisite Verification

**Before executing:**
1. Check `openshift-virtualization` exists in `mcps.json` → If missing, report setup
2. Verify `KUBECONFIG` is set (presence only, never expose value) → If missing, report
3. (Optional) Test basic connectivity to cluster → If fails, report connection error

**Human Notification Protocol:** `❌ Cannot execute vm-inventory: MCP server not available. Setup: Add to mcps.json, set KUBECONFIG, restart Claude Code. Docs: https://github.com/openshift/openshift-mcp-server`

⚠️ **SECURITY**: Never display KUBECONFIG path or credential values. Never fall back to CLI commands (`oc`, `kubectl`) — all operations must go through MCP tools exclusively.

## When to Use This Skill

**Trigger when:**
- User explicitly invokes `/vm-inventory` command
- User wants to see all VMs or VMs in a specific namespace
- User asks about VM status or health
- User needs to find a VM by name
- User wants details about a specific VM configuration

**User phrases:**
- "List all VMs"
- "Show VMs in production namespace"
- "What VMs are running?"
- "Get details of VM web-server"
- "Show me the status of database-vm"
- "/vm-inventory" (explicit command)

**Do NOT use when:**
- User wants to create a VM → Use `/vm-create` skill instead
- User wants to start/stop VMs → Use `/vm-lifecycle-manager` skill instead
- User wants to modify VM configuration → Different operation (not inventory)

## Workflow

**CRITICAL EXECUTION PATTERN**:
1. **Use MCP server tools exclusively** - `resources_list` or `resources_get`
2. **If MCP tools fail** - Report the error and guide the user to fix MCP setup
3. **Never use CLI commands** - No `oc` or `kubectl` execution under any circumstances

### Workflow A: List All VMs (Across All Namespaces)

**Step 1: Query VirtualMachine Resources Using MCP Tool**

**MCP Tool**: `resources_list` (apiVersion="kubevirt.io/v1", kind="VirtualMachine", allNamespaces=true)

**Errors:** Tool not found/connection error → Report error, guide user to fix MCP setup

**Step 2: Get Resource Details for Running VMs**

**Large cluster safeguard**: If Step 1 returned more than 20 VMs, skip VMI queries entirely. Display a summary table using only VM resource data (Name, Namespace, Status) and suggest the user narrow down by namespace: `⚠️ Found <N> VMs across all namespaces. Showing summary view. Use "List VMs in namespace <ns>" for full details.`

To display complete VM information (when 20 or fewer VMs), query VirtualMachineInstance (VMI) resources:

**MCP Tool**: `resources_list` (apiVersion="kubevirt.io/v1", kind="VirtualMachineInstance")

**For each VMI, extract**:
- `.spec.domain.cpu.sockets` and `.spec.domain.memory.guest` - Resources column ("X vCPU, YGi")
- `.status.volumeStatus[].persistentVolumeClaimInfo.capacity.storage` - Storage column (sum all PVC volumes, exclude container disks/cloudinit)
- `.status.guestOSInfo.prettyName` or `.status.guestOSInfo.name` + version - Guest OS column
- `.status.interfaces[0].ipAddress` - IP column (primary interface)
- `.status.nodeName` - Node column
- `.status.conditions[]` - Conditions column (Ready, AgentConnected, LiveMigratable)

**Stopped VMs**: Use VirtualMachine spec for Resources only; Storage/Guest OS/IP/Conditions show "-"

**Step 3: Format and Display Results**

**ALWAYS display in table format** ordered by namespace and status:

```markdown
## 📋 Virtual Machines (All Namespaces)

| Namespace | VM Name | Status | Age | Resources | Storage | Guest OS | Node | IP | Conditions |
|-----------|---------|--------|-----|-----------|---------|----------|------|----|------------|
| development | debug-vm | ⚠ Pending | 2d | 2 vCPU, 4Gi | 30Gi | - | - | - | ⚠ Not Ready |
| development | test-vm | ✓ Running | 5d | 2 vCPU, 4Gi | 30Gi | Ubuntu 24.04 | worker-03 | 10.131.0.20 | ✓ Ready, ✓ Live Migration |
| production | database-vm | ✗ Stopped | 30d | 8 vCPU, 16Gi | - | - | - | - | - |
| production | web-server-01 | ✓ Running | 15d | 4 vCPU, 8Gi | 100Gi | RHEL 9.7 | worker-01 | 10.131.0.15 | ✓ Ready, ✓ Agent, ✗ Live Migration |
| production | web-server-02 | ✓ Running | 15d | 4 vCPU, 8Gi | 100Gi | RHEL 9.7 | worker-02 | 10.131.0.16 | ✓ Ready, ✓ Agent, ✗ Live Migration |

**Summary:**
- **Total VMs**: 5
- **Running**: 3
- **Stopped**: 1
- **Pending**: 1
```

**Table Ordering Rules:**
1. **Primary sort**: Namespace (alphabetical)
2. **Secondary sort**: Status (Running → Pending → Stopped → Failed/Error)
3. **Tertiary sort**: VM Name (alphabetical within same namespace and status)

**Status Indicators:**
- ✓ Running/Ready
- ✗ Stopped/Halted
- ⚠ Pending/Starting/Terminating
- ❌ Failed/Error

**Resources Column Format**: MUST show "X vCPU, YGi" (query VMI `.spec.domain.cpu.sockets` and `.spec.domain.memory.guest`), NOT instance type names (e.g., NOT "u1.medium")

### Workflow B: List VMs in Specific Namespace

**Step 1: Gather Namespace**

Ask user for namespace if not provided.

**Step 2: Query VMs in Namespace Using MCP Tool**

**MCP Tool**: `resources_list` (apiVersion="kubevirt.io/v1", kind="VirtualMachine", namespace=`<namespace>`)

**Errors:** Tool fails → Report error, guide user to fix MCP setup

**Step 3: Get Resource Details and Display**

Follow same format rules as Workflow A Step 2-3. Use namespace-specific header:

```markdown
## 📋 Virtual Machines in '<namespace>'

| Name | Status | vCPU | Memory | Age | Node |
|------|--------|------|--------|-----|------|
| web-server-01 | Running | 4 | 8Gi | 15d | worker-01 |
| web-server-02 | Running | 4 | 8Gi | 15d | worker-02 |
| database-vm | Stopped | 8 | 16Gi | 30d | - |

**Summary**: 3 VMs (2 running, 1 stopped)
```

### Workflow C: Get Details of Specific VM

**Step 1: Gather VM Information**

Required: VM name, Namespace (ask if not provided)

**Step 2: Retrieve VM Resource Details Using MCP Tool**

**MCP Tool**: `resources_get` (apiVersion="kubevirt.io/v1", kind="VirtualMachine", namespace=`<namespace>`, name=`<vm-name>`)

**Errors:** Tool fails → Report error, guide user to fix MCP setup

**Step 3: Interpret Status and Conditions**

Report the VM status as-is from the API response. Do NOT read external documentation files to interpret status — use the status indicators defined in the Output Formatting Guidelines section below. If the user needs troubleshooting guidance, suggest they use a dedicated troubleshooting skill instead.

**Step 4: Display Detailed Information**

```markdown
## 🖥️ Virtual Machine Details

### Basic Information
- **Name**: `web-server-01`
- **Namespace**: `production`
- **Status**: Running
- **Created**: 15 days ago

### Configuration
- **Instance Type**: u1.medium
- **Workload**: Fedora
- **Run Strategy**: Always (auto-restart on crash)

### Resources
- **vCPU**: 4 cores
- **Memory**: 8Gi
- **Storage**: 50Gi
- **Storage Class**: ocs-storagecluster-ceph-rbd

### Network
- **Primary**: default (pod network)
- **Secondary**: vlan100 (multus - 192.168.100.5)

### Volumes
- **rootdisk**: 50Gi (DataVolume/PVC)

### Current State
- **Phase**: Running
- **Ready**: True
- **Node**: worker-01
- **Pod IP**: 10.129.2.45
- **Guest OS Uptime**: 12 days

### Conditions
- ✓ Ready
- ✓ LiveMigratable
- ✓ AgentConnected

### Labels
- app: web
- env: production
- tier: frontend
```

### Workflow D: Filter VMs by Criteria

**Step 1: Query VMs with Filters Using MCP Tool**

**MCP Tool**: `resources_list` (apiVersion="kubevirt.io/v1", kind="VirtualMachine", allNamespaces=true, labelSelector=`<selector>`)

**Filtering options**:
- By Labels (via labelSelector): `"app=web"`, `"app=web,env=production"`, `"tier in (frontend,backend)"`
- By Status (post-processing): Filter results by `status.printableStatus` field
- By Resource Size (post-processing): Parse instance type or VMI resource specs

**Errors:** Tool fails → Report error, guide user to fix MCP setup

**Step 2: Display Filtered Results**

Display with explanation: `## 📋 VMs with label 'app=web'` + list/table using Workflow A format

## Common Issues

### Issue 1: No VMs Found
**Error**: Empty list | **Causes**: No VMs exist, wrong namespace, insufficient RBAC | **Response**: Report no VMs found, suggest create VM (vm-create), list namespaces, check permissions

### Issue 2: Permission Denied
**Error**: "Forbidden: User cannot list VirtualMachines" | **Solution**: Verify KUBECONFIG has list/get permissions, contact admin

### Issue 3: Cluster Connection Error
**Error**: "Unable to connect to cluster" | **Solution**: Verify KUBECONFIG valid, check `oc cluster-info`, verify network, check credentials expiry

## Output Formatting Guidelines

**Use consistent status indicators:**
- ✓ Running/Healthy/Ready
- ✗ Stopped/Halted
- ⚠ Warning/Pending/Migrating
- ❌ Critical/Failed/Error

**Include key information always:**
- VM name and namespace
- Current status
- Resource allocation (vCPU, memory)
- Age/creation time
- Node placement (for running VMs)

**Organize by namespace** when showing multiple VMs for logical grouping and clear separation.

**Provide actionable next steps:** How to start stopped VMs, get more details, when to use other skills

## Integration with Other Skills

**Before creating a VM** (vm-create): Use vm-inventory to check if VM name exists, verify namespace has capacity
**Before lifecycle operations** (vm-lifecycle-manager): Check current VM status, verify VM exists
**For troubleshooting**: Get VM overview with vm-inventory first, then use vm-troubleshooter for deep diagnostics

## Dependencies

### Required MCP Servers
- `openshift-virtualization` - OpenShift MCP server (https://github.com/openshift/openshift-mcp-server)

### Required MCP Tools (PRIMARY - Always try first)
- `resources_list` - List resources (apiVersion, kind, namespace optional, allNamespaces optional, labelSelector optional)
- `resources_get` - Get resource details (apiVersion, kind, namespace, name)

**Important**: All operations must use MCP tools exclusively. CLI commands (`oc`, `kubectl`) are prohibited to prevent command injection risks.

### Related Skills
- `vm-create` - Create VMs after checking inventory
- `vm-lifecycle-manager` - Manage VMs discovered in inventory
- `vm-troubleshooter` (planned) - Diagnose problematic VMs from inventory

### Reference Documentation
- [OpenShift Virtualization Documentation](https://docs.redhat.com/en/documentation/openshift_container_platform/4.21/html-single/virtualization/index#virt/about_virt/about-virt.html)
- [KubeVirt VirtualMachine API](https://kubevirt.io/api-reference/)
- [Accessing VMs](https://docs.redhat.com/en/documentation/openshift_container_platform/4.21/html-single/virtualization/index#virt/virtual_machines/virt-accessing-vm-consoles.html)
- [VM Status Conditions](https://kubevirt.io/user-guide/virtual_machines/vm_status_conditions/)

## Human-in-the-Loop Requirements

This skill is **read-only** — no user confirmation is required. It does not change VM state, modify configuration, delete resources, or consume cluster capacity.

## Security Considerations

- Read-only operations - no modifications to VMs
- Respects Kubernetes RBAC permissions
- Only shows VMs in namespaces user has access to
- KUBECONFIG credentials never exposed in output
- No sensitive VM configuration details displayed by default
- All queries audited in Kubernetes API logs

## Example Usage

### Example 1: List all VMs (table format)

```
User: "List all VMs"
Agent: [MCP: resources_list(apiVersion="kubevirt.io/v1", kind="VirtualMachine", allNamespaces=true)]
       [Queries VMI resources for CPU/memory]
       [Displays table format from Workflow A Step 3]
```

### Example 2: MCP unavailable

```
User: "List all VMs"
Agent: [MCP tool fails]
       ❌ Cannot execute vm-inventory: MCP server not available.
       Setup: Add openshift-virtualization to mcps.json, set KUBECONFIG, restart Claude Code.
       Docs: https://github.com/openshift/openshift-mcp-server
```

### Example 3: Get specific VM details

```
User: "Show me details of web-server-01 in production"
Agent: [MCP: resources_get(kind="VirtualMachine", namespace="production", name="web-server-01")]
       [Displays VM Details format from Workflow C Step 4]
```

### Example 4: Filter running VMs

```
User: "Show me all running VMs"
Agent: [Lists all VMs, filters by status.printableStatus == "Running"]
       ## ✓ Running Virtual Machines
       ### production: web-server-01 (4 vCPU, 8Gi, worker-01) | web-server-02 (4 vCPU, 8Gi, worker-02)
       ### development: test-vm (2 vCPU, 4Gi, worker-03)
       **Total**: 3 running VMs
```
