# Live Migration Best Practices

**Purpose**: Configuration parameters, requirements, and best practices for VM live migration in OpenShift Virtualization.

**When to consult this document**: Before executing live migrations, when configuring cluster-wide migration settings, or when troubleshooting migration performance issues.

---

## Official Sources

This document is compiled from official Red Hat documentation:

- [Live Migrating VMs with OpenShift Virtualization](https://developers.redhat.com/articles/2025/07/14/live-migrating-vms-openshift-virtualization) - Red Hat Developer (2025-07-14)
- [How OpenShift Virtualization Supports VM Live Migration](https://developers.redhat.com/articles/2025/06/05/how-openshift-virtualization-supports-vm-live-migration) - Red Hat Developer (2025-06-05)
- [Chapter 12. Live Migration - OpenShift Container Platform 4.18](https://docs.redhat.com/en/documentation/openshift_container_platform/4.18/html/virtualization/live-migration) - Red Hat Documentation
- [Best Practices for Virtual Machine Deployments on OpenShift Virtualization](https://learn.microsoft.com/en-us/azure/openshift/best-practices-openshift-virtualization) - Microsoft Azure Red Hat OpenShift (2026-02-16)
- [Best Practices to Deploy VMs in Red Hat OpenShift Virtualization](https://docs.netapp.com/us-en/netapp-solutions-virtualization/openshift/os-osv-bpg.html) - NetApp Solutions

---

## Configuration Parameters

### HyperConverged CR Live Migration Settings

All live migration settings are configured in the `HyperConverged` custom resource located in the `openshift-cnv` namespace.

**Default Configuration:**
```yaml
apiVersion: hco.kubevirt.io/v1beta1
kind: HyperConverged
metadata:
  name: kubevirt-hyperconverged
  namespace: openshift-cnv
spec:
  liveMigrationConfig:
    completionTimeoutPerGiB: 800        # Seconds per GiB for migration completion
    parallelMigrationsPerCluster: 5     # Max concurrent migrations cluster-wide
    parallelOutboundMigrationsPerNode: 2 # Max concurrent migrations per source node
    progressTimeout: 150                 # Max seconds without progress before cancellation
    bandwidthPerMigration: 64Mi         # (Optional) Bandwidth limit per migration
    network: ""                          # (Optional) Dedicated secondary network for migration
```

**Parameter Explanations:**

| Parameter | Default | Description | Tuning Guidance |
|-----------|---------|-------------|-----------------|
| `completionTimeoutPerGiB` | 800s | Migration completion duration per gigabyte of VM memory | Increase for high memory write rate (dirty page) workloads |
| `progressTimeout` | 150s | Maximum seconds without migration progress before cancellation | Increase for large VMs (>100GB) or slow networks |
| `parallelMigrationsPerCluster` | 5 | Cluster-wide concurrent migration limit | Increase if network bandwidth allows; decrease if saturation occurs |
| `parallelOutboundMigrationsPerNode` | 2 | Per-node concurrent outbound migration limit | Keep at 2 to prevent single-node overload |
| `bandwidthPerMigration` | 64Mi | (Optional) Bandwidth limit per migration | Set to prevent network saturation; omit for unlimited |
| `network` | "" | (Optional) NetworkAttachmentDefinition for dedicated migration network | Highly recommended for production; see Dedicated Networks section |

**How to Update Configuration Using MCP Tools:**

**Step 1: Get current HyperConverged resource**

**MCP Tool**: `resources_get` (from openshift-virtualization)

**Parameters**:
```json
{
  "apiVersion": "hco.kubevirt.io/v1beta1",
  "kind": "HyperConverged",
  "namespace": "openshift-cnv",
  "name": "kubevirt-hyperconverged"
}
```

**Step 2: Modify the returned JSON to update liveMigrationConfig**

Add or update the `.spec.liveMigrationConfig` section:
```json
{
  "spec": {
    "liveMigrationConfig": {
      "completionTimeoutPerGiB": 1200,
      "parallelMigrationsPerCluster": 10,
      "progressTimeout": 300,
      "bandwidthPerMigration": "32Mi"
    }
  }
}
```

**Step 3: Apply the updated configuration**

**MCP Tool**: `resources_create_or_update` (from openshift-virtualization)

**Parameters**:
```json
{
  "resource": "<full-modified-hyperconverged-yaml-or-json>"
}
```

Pass the complete modified HyperConverged resource as YAML or JSON string.

---

## Prerequisites and Requirements

### Storage Requirements

**CRITICAL**: Live migration requires **ReadWriteMany (RWX)** access mode storage.

**Supported Storage Types for Live Migration:**

| Storage Type | Access Mode | Live Migration Support | Notes |
|--------------|-------------|------------------------|-------|
| NFS (ontap-nas driver) | RWX | ✅ Supported | Recommended for general use |
| SMB/CIFS (ontap-nas driver) | RWX | ✅ Supported | Windows-compatible |
| iSCSI/FC (ontap-san driver) | RWX (raw block mode only) | ✅ Supported | High performance; requires raw block volumes |
| Local storage / AWS EBS (gp3) | RWO | ❌ NOT Supported | Use cold migration instead |

**Validation Using MCP Tools:**

**MCP Tool**: `resources_get` (from openshift-virtualization)

**Parameters**:
```json
{
  "apiVersion": "v1",
  "kind": "PersistentVolumeClaim",
  "namespace": "<namespace>",
  "name": "<pvc-name>"
}
```

**Expected Output**: Check `.spec.accessModes` in the returned PVC resource.

For live migration, access modes must include `"ReadWriteMany"`.

**What Happens with RWO Storage:**

When attempting live migration with ReadWriteOnce (RWO) storage:
```
Error: cannot migrate VMI: PVC <pvc-name> is not shared, live migration requires
that all PVCs must be shared (using ReadWriteMany access mode)
```

**Solution**: Use cold migration workflow for VMs with RWO storage (see REBALANCE_MANUAL.md).

---

### Hardware and Network Requirements

**Minimum Requirements:**

- **Nodes**: Red Hat Enterprise Linux CoreOS (RHCOS) compute nodes (RHEL nodes are incompatible)
- **Network**: All nodes must be on the same L2 network or have routable connectivity
- **CPU**: Sufficient CPU headroom on target node for incoming VM workload
- **Memory**: Sufficient free memory on target node (>= VM memory allocation)

**Recommended for Production:**

- **Network Cards**: 100Gbps NICs for large VM migrations (>500GB memory)
- **Dedicated Migration Network**: Secondary physical network or VLAN for isolation
- **Storage Backend**: SSD-backed shared storage (NFS-CSI, OpenShift Data Foundation, Azure NetApp Files)
- **MTU Configuration**: Set to 9000 for migration networks to improve efficiency

---

## Dedicated Migration Network (Production Best Practice)

### Why Use a Dedicated Network?

**Benefits:**
- Isolates migration traffic from application workloads
- Prevents network contention and performance degradation
- Enables higher bandwidth allocation (e.g., 100Gbps dedicated)
- Improves security and manageability
- Reduces migration time for large VMs

**When to Use:**
- Production environments with large VMs (>100GB memory)
- Clusters with high application network traffic
- Environments requiring strict network isolation
- High-availability requirements with frequent migrations

### Configuration Example

**Step 1: Create NodeNetworkConfigurationPolicy (NNCP)**

**MCP Tool**: `resources_create_or_update` (from openshift-virtualization)

**Parameters**:
```json
{
  "resource": "apiVersion: nmstate.io/v1\nkind: NodeNetworkConfigurationPolicy\nmetadata:\n  name: migration-network-policy\nspec:\n  desiredState:\n    interfaces:\n      - name: br-lm\n        description: OVS bridge for live migration\n        type: ovs-bridge\n        state: up\n        bridge:\n          allow-extra-patch-ports: true\n          port:\n            - name: enp4s0\n              vlan:\n                mode: access\n                tag: 3030\n          options:\n            stp: false"
}
```

**Step 2: Create NetworkAttachmentDefinition (NAD)**

**MCP Tool**: `resources_create_or_update` (from openshift-virtualization)

**Parameters**:
```json
{
  "resource": "apiVersion: k8s.cni.cncf.io/v1\nkind: NetworkAttachmentDefinition\nmetadata:\n  name: migration-network\n  namespace: openshift-cnv\nspec:\n  config: '{\n    \"cniVersion\": \"0.3.1\",\n    \"name\": \"migration-bridge\",\n    \"type\": \"macvlan\",\n    \"master\": \"eth1\",\n    \"mode\": \"bridge\",\n    \"ipam\": {\n      \"type\": \"whereabouts\",\n      \"range\": \"10.200.5.0/24\",\n      \"excludeSubnets\": \"10.200.5.0/30\"\n    }\n  }'"
}
```

**Step 3: Configure HyperConverged CR to Use Network**

**MCP Tool**: Get current HyperConverged, modify, and update using `resources_create_or_update`

Add to `.spec.liveMigrationConfig`:
```json
{
  "network": "migration-network"
}
```

**Step 4: Verify virt-handler Pods Restarted**

**MCP Tool**: `pods_list` (from openshift-virtualization)

**Parameters**:
```json
{
  "labelSelector": "kubevirt.io=virt-handler"
}
```

**Expected**: All pods show READY status and recent start time (AGE).

Filter results where `status.containerStatuses[0].ready == true` and `status.containerStatuses[0].restartCount` is recent.

**Verification After Migration:**

**MCP Tool**: `resources_get` (from openshift-virtualization)

**Parameters**:
```json
{
  "apiVersion": "kubevirt.io/v1",
  "kind": "VirtualMachineInstanceMigration",
  "namespace": "<namespace>",
  "name": "<migration-name>"
}
```

Check `.status.migrationState.targetNodeAddress` - should be an IP from the dedicated subnet (e.g., 10.200.5.15).

---

## Migration Process and Technologies

### Pre-copy Migration

Live migration uses **pre-copy** strategy:

1. **Initial Copy**: VM continues running on source node while memory is copied to target
2. **Iterative Copy**: Pages modified during copy (dirty pages) are re-copied
3. **Cutover**: Brief pause (<1 second) to copy final dirty pages and switch execution
4. **Cleanup**: Source VM instance is terminated

**Multi-fd Technology** (for high-load scenarios):

- Sends data over multiple network streams in parallel
- Maximizes bandwidth utilization during migration
- Handles high dirty page rates (e.g., SAP HANA, databases with high write rates)
- Automatically enabled by KubeVirt when beneficial

**Migration Phases:**

```
Pending → Scheduling → PreparingTarget → Running → Succeeded
```

**Monitor with MCP Tools:**

**MCP Tool**: `resources_list` (from openshift-virtualization)

**Parameters**:
```json
{
  "apiVersion": "kubevirt.io/v1",
  "kind": "VirtualMachineInstanceMigration"
}
```

Filter results by `.status.phase` to see current migration status.

---

## Best Practices

### 1. VM Resource Optimization

**Enable Dedicated Resources:**

Configure VMs with dedicated CPU and memory isolation for performance-sensitive workloads:

```yaml
spec:
  template:
    spec:
      domain:
        cpu:
          dedicatedCpuPlacement: true
        resources:
          requests:
            memory: 16Gi
```

**Benefits:**
- Improves VM performance and latency predictability
- Reduces migration time (less CPU contention)
- Better accuracy for latency predictions

**When to Use:**
- Database workloads (PostgreSQL, MySQL, SAP HANA)
- Real-time analytics applications
- Low-latency requirements

### 2. Hugepage Configuration

For large VMs (>100GB memory), configure hugepages to reduce memory page overhead:

**Node Configuration Using MCP Tools:**

**MCP Tool**: `resources_get` then `resources_create_or_update` (from openshift-virtualization)

**Step 1: Get Node resource**

**Parameters**:
```json
{
  "apiVersion": "v1",
  "kind": "Node",
  "name": "<node-name>"
}
```

**Step 2: Add label to node**

Modify returned JSON to add `.metadata.labels.cpumanager = "true"`, then update with `resources_create_or_update`.

**VM Configuration:**
```yaml
spec:
  template:
    spec:
      domain:
        memory:
          hugepages:
            pageSize: 1Gi
```

**Benefits:**
- Reduces page-dirtying overhead during migration
- Improves memory access performance
- Faster migration completion for very large VMs (tested with 1TB VMs)

### 3. Network Optimization

**Set Network MTU to 9000** (jumbo frames):

Configure in the NetworkAttachmentDefinition used for migration:

```yaml
spec:
  liveMigrationConfig:
    network: migration-network  # NetworkAttachmentDefinition with MTU 9000
```

**Benefits:**
- Significantly improves network efficiency
- Reduces packet overhead
- Faster data transfer for large VM migrations

**Validate MTU Setting Using MCP Tools:**

**MCP Tool**: `resources_get` (from openshift-virtualization)

**Parameters**:
```json
{
  "apiVersion": "k8s.cni.cncf.io/v1",
  "kind": "NetworkAttachmentDefinition",
  "namespace": "openshift-cnv",
  "name": "migration-network"
}
```

Check `.spec.config` for MTU setting in the JSON configuration.

### 4. Storage Configuration

**For Testing/Development:**
- NFS-CSI with SSD backend storage
- Shared storage accessible from all nodes

**For Production:**
- OpenShift Data Foundation (ODF) with SSD-backed storage
- Azure NetApp Files with appropriate performance tier
- NetApp ONTAP with dedicated SVM for virtualization workloads

**Storage Validation Before Migration Using MCP Tools:**

For each VM in rebalance plan:

**Step 1: Get VM resource**

**MCP Tool**: `resources_get` (from openshift-virtualization)

**Parameters**:
```json
{
  "apiVersion": "kubevirt.io/v1",
  "kind": "VirtualMachine",
  "namespace": "<namespace>",
  "name": "<vm-name>"
}
```

**Step 2: Extract PVC names from `.spec.template.spec.volumes[].persistentVolumeClaim.claimName`**

**Step 3: For each PVC, verify access mode**

**MCP Tool**: `resources_get` (from openshift-virtualization)

**Parameters**:
```json
{
  "apiVersion": "v1",
  "kind": "PersistentVolumeClaim",
  "namespace": "<namespace>",
  "name": "<pvc-name>"
}
```

**Expected**: `.spec.accessModes` must include `"ReadWriteMany"`.

### 5. Concurrency Management

**Default Limits:**
- **Cluster-wide**: 5 concurrent migrations
- **Per-node outbound**: 2 concurrent migrations

**When to Increase:**
- Cluster has sufficient network bandwidth (100Gbps+ NICs)
- Dedicated migration network is configured
- Routine maintenance window with many VMs to migrate

**When to Decrease:**
- Network saturation detected (monitor with Prometheus)
- Migration failures due to timeouts
- Shared application network (no dedicated migration network)

**Monitoring Network Saturation Using MCP Tools:**

**MCP Tool**: `nodes_stats_summary` (from openshift-virtualization)

**Parameters**:
```json
{
  "name": "<node-name>"
}
```

Review `.network.interfaces[].rxBytes` and `.network.interfaces[].txBytes` for throughput metrics.

Alternatively, use `nodes_top` for current resource usage:

**MCP Tool**: `nodes_top` (from openshift-virtualization)

**Parameters**:
```json
{
  "name": "<node-name>"
}
```

### 6. Pre-Migration Validation Checklist

Before initiating migration:

1. ✅ **Storage**: Verify all PVCs use ReadWriteMany (RWX) access mode
2. ✅ **Network**: Confirm all nodes are network-accessible
3. ✅ **Capacity**: Verify target node has sufficient CPU and memory
4. ✅ **Health**: Check `virt-handler` pods are Running (1/1) on all nodes
5. ✅ **Workload**: Consider VM workload intensity (reduce load if possible)
6. ✅ **Limits**: Check current cluster migration count < `parallelMigrationsPerCluster`

**Validation Using MCP Tools:**

**1. Check PVC Access Modes:**

For each VM, use `resources_get` to get VirtualMachine, extract PVC names, then `resources_get` for each PVC and verify `.spec.accessModes` includes `"ReadWriteMany"`.

**2. Check virt-handler Health:**

**MCP Tool**: `pods_list` (from openshift-virtualization)

**Parameters**:
```json
{
  "labelSelector": "kubevirt.io=virt-handler"
}
```

Filter results where `status.containerStatuses[0].ready == true`. All pods must show ready status.

**3. Check Current Migration Count:**

**MCP Tool**: `resources_list` (from openshift-virtualization)

**Parameters**:
```json
{
  "apiVersion": "kubevirt.io/v1",
  "kind": "VirtualMachineInstanceMigration"
}
```

Count results where `.status.phase` is NOT "Succeeded" or "Failed". Compare to `parallelMigrationsPerCluster` limit from HyperConverged CR.

**4. Check Target Node Capacity:**

**MCP Tool**: `resources_get` (from openshift-virtualization)

**Parameters**:
```json
{
  "apiVersion": "v1",
  "kind": "Node",
  "name": "<target-node-name>"
}
```

Review `.status.allocatable` and `.status.capacity` for available CPU and memory.

Alternatively use `nodes_top`:

**MCP Tool**: `nodes_top` (from openshift-virtualization)

**Parameters**:
```json
{
  "name": "<target-node-name>"
}
```

---

## Test Results and Validation

### SAP HANA 1TB VM Live Migration (Red Hat Developer Article 2025-07-14)

**Test Environment:**
- **Hardware**: 8-socket Intel Xeon Platinum, 12TB memory, 100Gbps NICs
- **OpenShift**: 4.17.15
- **VM Size**: 1TB memory (SAP HANA 2.00.081.00.1733303410)
- **Storage**: NFS-CSI with SSD backend
- **Network**: Dedicated 100Gbps secondary network, MTU 9000

**Results:**
- ✅ **Idle/Cooled-off**: Live migration completed successfully with **zero data loss or corruption**
- ✅ **High-load**: Migrations progressed as expected even with large volumes of dirty pages
- ✅ **Integrity**: Full VM and data integrity maintained; failed migrations safely canceled
- ⏱️ **Duration**: ~30-60 seconds for typical VMs; longer for 1TB VM under load

**Key Findings:**
- Multi-fd technology enabled migrations to continue transferring data quickly while dirty pages were being generated
- Dedicated 100Gbps network critical for large VM migrations
- 1GB hugepages reduced page-dirtying overhead

---

## Limitations and Constraints

### Migration Requirements

**MUST HAVE for Live Migration:**
- ReadWriteMany (RWX) storage on all VM volumes
- VM currently running (VirtualMachineInstance exists)
- Target node has sufficient capacity (CPU, memory)
- All nodes have RHCOS (not RHEL)

**CANNOT Live Migrate When:**
- VM uses ReadWriteOnce (RWO) storage → Use cold migration
- VM is stopped (no VirtualMachineInstance) → Use cold migration or start VM first
- Target node is cordoned or NotReady → Choose different target
- Cluster at `parallelMigrationsPerCluster` limit → Wait for completion

### Known Issues

**Single Node OpenShift (SNO):**
- VMs created from common templates with `evictionStrategy: LiveMigrate` trigger `VMCannotBeEvicted` alert
- **Workaround**: Use `evictionStrategy: None` for SNO clusters

**OVN-Kubernetes CNI:**
- Cannot attach Linux bridge or bonding device to host's default interface
- **Workaround**: Use secondary network interface or switch to OpenShift SDN CNI

**MTU Differences:**
- OVS bridge default MTU: 1400
- Linux bridge default MTU: 1500
- **Impact**: May cause fragmentation; configure MTU explicitly

---

## Troubleshooting Common Issues

### Issue 1: Migration Timeout

**Symptom:**
```
Migration exceeded timeout: 150 seconds per GiB
```

**Causes:**
- High memory write rate (dirty page rate exceeds transfer rate)
- Insufficient network bandwidth
- Large VM memory size

**Solutions:**

**1. Increase timeout (temporary):**

Use `resources_get` to fetch HyperConverged CR, modify `.spec.liveMigrationConfig`, then update with `resources_create_or_update`:

```json
{
  "spec": {
    "liveMigrationConfig": {
      "completionTimeoutPerGiB": 1200,
      "progressTimeout": 300
    }
  }
}
```

**2. Reduce VM workload** during migration:
- Stop write-intensive processes temporarily
- Schedule migration during low-activity window

**3. Use cold migration** instead (guaranteed completion - see REBALANCE_MANUAL.md)

**4. Configure auto-converge** (cluster-level KubeVirt setting):
- Throttles vCPU to reduce dirty page rate
- Enables migration convergence for high write-rate VMs

### Issue 2: Network Saturation

**Symptom:**
- Multiple concurrent migrations slow or fail
- High network utilization on migration network

**Solutions:**

**1. Reduce concurrent migrations:**

Use `resources_get` to fetch HyperConverged CR, modify `.spec.liveMigrationConfig.parallelMigrationsPerCluster`, then update with `resources_create_or_update`:

```json
{
  "spec": {
    "liveMigrationConfig": {
      "parallelMigrationsPerCluster": 3
    }
  }
}
```

**2. Set bandwidth limit per migration:**

Modify `.spec.liveMigrationConfig.bandwidthPerMigration`:

```json
{
  "spec": {
    "liveMigrationConfig": {
      "bandwidthPerMigration": "32Mi"
    }
  }
}
```

**3. Use dedicated migration network** (see Dedicated Migration Network section)

### Issue 3: virt-handler Pods Not Ready

**Symptom:**

Using `pods_list` with `labelSelector: "kubevirt.io=virt-handler"`, some pods show `status.containerStatuses[0].ready == false`.

**Causes:**
- Recent HyperConverged configuration change
- Network configuration error
- Node connectivity issue

**Solutions:**

**1. Wait for pod restart** (after config change):

Pods restart automatically after HyperConverged update. Monitor using `pods_list` until all show ready status.

**2. Check pod logs:**

**MCP Tool**: `pods_log` (from openshift-virtualization)

**Parameters**:
```json
{
  "name": "<virt-handler-pod-name>",
  "namespace": "openshift-cnv",
  "tail": 100
}
```

**3. Verify node network configuration** (if using dedicated network):

Use `resources_list` to check NodeNetworkConfigurationPolicy:

**Parameters**:
```json
{
  "apiVersion": "nmstate.io/v1",
  "kind": "NodeNetworkConfigurationPolicy"
}
```

And NetworkAttachmentDefinition:

**Parameters**:
```json
{
  "apiVersion": "k8s.cni.cncf.io/v1",
  "kind": "NetworkAttachmentDefinition",
  "namespace": "openshift-cnv"
}
```

### Issue 4: Migration Rejected - Cluster Limit Reached

**Symptom:**
```
Migration rejected: cluster migration limit reached (5 concurrent)
```

**Solutions:**

**1. Wait for ongoing migrations** to complete:

Monitor using `resources_list`:

**MCP Tool**: `resources_list` (from openshift-virtualization)

**Parameters**:
```json
{
  "apiVersion": "kubevirt.io/v1",
  "kind": "VirtualMachineInstanceMigration"
}
```

Filter for migrations where `.status.phase` is NOT "Succeeded" or "Failed".

**2. Increase cluster limit** (if network allows):

Use `resources_get` to fetch HyperConverged CR, modify `.spec.liveMigrationConfig.parallelMigrationsPerCluster`, then update with `resources_create_or_update`:

```json
{
  "spec": {
    "liveMigrationConfig": {
      "parallelMigrationsPerCluster": 10
    }
  }
}
```

**3. Migrate VMs sequentially** instead of batch operation

---

## Related Documentation

- [Performance Tuning Guide](./performance-tuning.md) - Advanced tuning for migration performance
- [Anti-Patterns](./anti-patterns.md) - Common mistakes to avoid
- [Production Considerations](./production-considerations.md) - Right-sizing, workload planning, HA strategies
- [Troubleshooting: Scheduling Errors](../../../docs/troubleshooting/scheduling-errors.md) - ErrorUnschedulable after cold migration

---

**Last Updated**: 2026-02-24
**OpenShift Virtualization Versions**: 4.17, 4.18, 4.19, 4.20
**Status**: Production-ready guidance from official Red Hat sources
