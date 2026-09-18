---
name: vm-lifecycle-manager
description: |
  Manage virtual machine lifecycle operations including start, stop, and restart.

  Use when:
  - "Start VM [name]"
  - "Stop the virtual machine [name]"
  - "Restart VM [name]"
  - "Power on/off VM [name]"

  This skill handles VM state transitions safely with user confirmation for each action.

  NOT for creating VMs (use vm-create) or deleting VMs (use vm-delete).

license: Apache-2.0
model: inherit
color: blue
allowed-tools: vm_lifecycle resources_get
---

# /vm-lifecycle-manager Skill

Control virtual machine power state in OpenShift Virtualization using the `vm_lifecycle` tool.

## Prerequisites

**Required MCP Server**: `openshift-virtualization` ([OpenShift MCP Server](https://github.com/openshift/openshift-mcp-server))

**Required MCP Tools**:
- `vm_lifecycle` (from openshift-virtualization) - Manage VM power state

**Required Environment Variables**:
- `KUBECONFIG` - Path to Kubernetes configuration file with cluster access

**Required Cluster Setup**:
- OpenShift cluster (>= 4.19)
- OpenShift Virtualization operator installed
- ServiceAccount with RBAC permissions to update VirtualMachine resources

### Prerequisite Verification

**Before executing:**
1. Check `openshift-virtualization` exists in `mcps.json` → If missing, report setup
2. Verify `KUBECONFIG` is set (presence only, never expose value) → If missing, report

**Human Notification Protocol:** `❌ Cannot execute vm-lifecycle-manager: MCP server not available. Setup: Add to mcps.json, set KUBECONFIG, restart Claude Code. Docs: https://github.com/openshift/openshift-mcp-server`

⚠️ **SECURITY**: Never display KUBECONFIG path or credential values.

## When to Use This Skill

**Trigger when:**
- User explicitly invokes `/vm-lifecycle-manager` command
- User requests starting/stopping/restarting a VM
- User wants to change VM power state

**User phrases:**
- "Start VM web-server in namespace vms"
- "Stop the database VM"
- "Restart test-vm"
- "Power on the VM called api-server"
- "/vm-lifecycle-manager" (explicit command)

**Do NOT use when:**
- Create VM → `/vm-create`
- List VMs → `/vm-inventory`
- Delete VM → `/vm-delete`

## Workflow

### Step 1: Gather Parameters and Confirm

**Required from user:** VM Name, Namespace, Action (start|stop|restart)

**Present for confirmation:**

```markdown
## VM Lifecycle Operation

| Parameter | Value | Impact |
|-----------|-------|--------|
| VM Name | `<vm>` | from user |
| Namespace | `<ns>` | from user |
| Action | `<action>` | start: consumes resources / stop: graceful shutdown / restart: brief interruption (~1-2min) |

Confirm: yes/no
```

**WAIT** for explicit "yes" before proceeding to Step 2.

### Step 2: Execute Lifecycle Operation

**ONLY AFTER user confirmation in Step 1.**

**For start or stop actions:**

**MCP Tool**: `vm_lifecycle` (namespace=`<ns>`, name=`<vm>`, action=`<start|stop>`)

**For restart action (composite operation):**

**CRITICAL**: Implement restart as two separate operations to avoid resourceVersion conflicts:

1. **Stop VM**: `vm_lifecycle` (namespace=`<ns>`, name=`<vm>`, action="stop")
2. **Verify stopped**: `resources_get` (apiVersion="kubevirt.io/v1", kind="VirtualMachine", namespace=`<ns>`, name=`<vm>`) → Check `status.printableStatus` == "Stopped"
3. **Wait**: 5 seconds for VM to fully stop
4. **Start VM**: `vm_lifecycle` (namespace=`<ns>`, name=`<vm>`, action="start")
5. **Verify started**: `resources_get` → Check `status.printableStatus` == "Running"

**Errors:**
- VM not found → Report, suggest vm-inventory
- Permission denied → Report RBAC error
- Already in desired state → Inform user
- Stop fails during restart → Report, do not proceed to start
- Start fails during restart → Report, VM is stopped
- Transition fails → Report details

### Step 3: Report Operation Status

**On Success:**

```markdown
## ✓ VM <Action> Successful

**VM**: `<vm>` | **Namespace**: `<ns>` | **Action**: <action> | **RunStrategy**: <Always|Halted>

**Impact**:
- **start**: Running, consuming resources (CPU/memory). Access: virtctl console or SSH. RunStrategy: Always (auto-restart on crash)
- **stop**: Stopped, resources freed. State preserved. Start: "Start VM <vm>". RunStrategy: Halted (stays off)
- **restart**: Running after stop+start. Brief interruption (~1-2min). Monitor app logs. RunStrategy: Always

**Next**: "Show status of VM <vm>" or "List VMs in namespace <ns>"
```

**On Failure:**

**OPTIONAL**: Read [lifecycle-errors.md](docs/troubleshooting/lifecycle-errors.md) for start/stop failures or [scheduling-errors.md](docs/troubleshooting/scheduling-errors.md) for ErrorUnschedulable. Output: "Consulted lifecycle-errors.md for failure."

**When to consult**: Start/stop failures, stuck transitions, unexpected errors. **NOT**: Already in state, not found, RBAC errors.

```markdown
## ❌ Lifecycle Operation Failed

**Error**: <error>

**Causes**: VM not found | RBAC denied | Already in desired state | VM in transition (wait 30-60s) | Resource constraints (start)

**Troubleshoot**:
1. vm-inventory to verify VM exists
2. Check RBAC: `oc auth can-i update virtualmachines -n <ns>`
3. View VM status and events
4. Check node capacity (for start operations)
```

## Common Issues

### Issue 1: VM Not Found
**Error**: "VirtualMachine 'xyz' not found in namespace 'abc'"
**Solution**: Verify spelling, check namespace, use vm-inventory, VM may be deleted

### Issue 2: VM Already in Desired State
**Warning**: "VM is already running" (when attempting start)
**Solution**: Not an error - VM already in desired state. Use `restart` if intended to restart

### Issue 3: Permission Denied
**Error**: "Forbidden: User cannot update VirtualMachines"
**Solution**: Verify RBAC permissions (update VirtualMachine resources), contact admin

### Issue 4: VM Stuck in Transitioning State
**Error**: "VM stuck in 'Terminating' or 'Starting'"
**Solution**: Wait 30-60s, check events (`oc describe vm`), use vm-troubleshooter, check virt-launcher pod

### Issue 5: Insufficient Resources (Start)
**Error**: "Insufficient CPU/memory to start VM"
**Solution**: Check cluster availability, stop other VMs, scale nodes, resize VM to smaller instance type

### Issue 6: Restart Implementation
**Note**: Restart is implemented as two separate operations (stop → verify → start → verify)
**Reason**: Avoids Kubernetes resourceVersion conflicts when using single restart action
**Behavior**: If stop succeeds but start fails, VM remains stopped. Check VM status with vm-inventory

## Understanding RunStrategy

| Action | RunStrategy | Behavior |
|--------|------------|----------|
| start | Always | Runs, auto-restarts on crash |
| stop | Halted | Stops, stays off |
| restart | Always | Stops, starts, auto-restarts |

## Dependencies

### Required MCP Servers
- `openshift-virtualization` - OpenShift MCP server with KubeVirt toolset

### Required MCP Tools
- `vm_lifecycle` - Manage VM power state (start/stop/restart)

### Related Skills
- `vm-create` - Create VMs
- `vm-inventory` - Check VM status
- `vm-troubleshooter` (planned) - Diagnose startup/shutdown issues

### Reference Documentation
- [lifecycle-errors.md](docs/troubleshooting/lifecycle-errors.md) - Start/stop failures, stuck transitions (consulted on failures)
- [scheduling-errors.md](docs/troubleshooting/scheduling-errors.md) - ErrorUnschedulable, resource constraints (consulted when VM won't start)
- [Troubleshooting INDEX](docs/troubleshooting/INDEX.md) - Navigation hub for error categories
- [OpenShift Virt Docs](https://docs.redhat.com/en/documentation/openshift_container_platform/4.21/html-single/virtualization/index#virt/about_virt/about-virt.html)
- [KubeVirt Lifecycle](https://kubevirt.io/user-guide/virtual_machines/lifecycle/)
- [RunStrategy Docs](https://kubevirt.io/user-guide/virtual_machines/run_strategies/)
- [OpenShift MCP](https://github.com/openshift/openshift-mcp-server)

## Critical: Human-in-the-Loop Requirements

**IMPORTANT:** This skill requires explicit user confirmation before executing. You MUST:

1. **Wait for user confirmation** on specific action (start/stop/restart) before executing `vm_lifecycle`
2. **Do NOT proceed** until user explicitly approves
3. **Present action clearly** with VM name, namespace, intended state change
4. **Never auto-execute** - these operations impact running services
5. **Warn about consequences** - stopping interrupts services, starting consumes resources, restarting causes downtime

If user says "no" or wants to reconsider, do not proceed.

**Batch operations**: When the user requests actions on multiple VMs, process each VM individually through the full workflow (Step 1-3) with separate confirmation for each. Never use a single bulk confirmation for multiple VMs.

**Why**: start (consumes resources), stop (interrupts services), restart (brief downtime). User should verify correct VM and understand impact.

## Security Considerations

- Requires RBAC permissions (update VirtualMachine resources)
- Stop operations attempt graceful shutdown; guest OS/app data consistency depends on workload
- Start operations consume resources (quota limits apply)
- All operations audited in Kubernetes API logs
- KUBECONFIG credentials never exposed
- ServiceAccount permissions limit controllable VMs

## Example Usage

### Example 1: Start Stopped VM

```
User: "Start VM web-server in namespace vms"
Agent: [vm-lifecycle-manager skill]
## VM Lifecycle Operation
| VM Name | `web-server` | Namespace | `vms` | Action | `start` | consumes resources |
Confirm: yes/no
User: "yes"
Agent: [vm_lifecycle(namespace="vms", name="web-server", action="start")]
## ✓ VM Start Successful
VM: `web-server` | Namespace: `vms` | RunStrategy: Always
Impact: Running, consuming resources. Access: virtctl console or SSH
```

### Example 2: Stop with User Reconsidering

```
User: "Stop the database VM in production namespace"
Agent: [vm-lifecycle-manager skill]
| VM | `database` | Namespace | `production` | Action | `stop` | graceful shutdown |
Confirm: yes/no
User: "wait, no, don't stop it"
Agent: Operation cancelled. VM 'database' in namespace 'production' remains running.
```

### Example 3: Restart VM

```
User: "Restart test-vm in namespace dev"
Agent: [vm-lifecycle-manager skill]
| VM | `test-vm` | Namespace | `dev` | Action | `restart` | brief interruption ~1-2min |
User: "yes"
Agent: [Composite restart operation]
       1. vm_lifecycle(namespace="dev", name="test-vm", action="stop")
       2. Verify stopped: resources_get → status.printableStatus="Stopped"
       3. Wait 5s
       4. vm_lifecycle(namespace="dev", name="test-vm", action="start")
       5. Verify started: resources_get → status.printableStatus="Running"
## ✓ VM Restart Successful
VM: `test-vm` | Namespace: `dev` | RunStrategy: Always
Impact: Running after stop+start. Brief interruption. Monitor app logs.
```

### Example 4: VM Already in Desired State

```
User: "Start web-server in namespace vms"
Agent: [vm-lifecycle-manager skill]
       [Checks VM status via resources_get — already Running]
## ℹ️ VM Already Running
VM: `web-server` | Namespace: `vms` | Status: Running
Result: No action taken - VM already in desired state.
To restart: "Restart VM web-server in namespace vms"
```

### Example 5: Batch Operations

```
User: "Stop VMs web-01, web-02, web-03 in namespace production"
Agent: [vm-lifecycle-manager skill — processes each VM individually with full workflow]

## VM Lifecycle Operation
| VM Name | `web-01` | Namespace | `production` | Action | `stop` | graceful shutdown |
Confirm: yes/no
User: "yes"
Agent: [vm_lifecycle(namespace="production", name="web-01", action="stop")]
✓ web-01: Stopped

## VM Lifecycle Operation
| VM Name | `web-02` | Namespace | `production` | Action | `stop` | graceful shutdown |
Confirm: yes/no
User: "yes"
[...repeats for each VM with individual confirmation...]
```
