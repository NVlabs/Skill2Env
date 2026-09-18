# Performance Tuning for VM Rebalancing

**Purpose**: Advanced performance tuning parameters, optimization strategies, and monitoring guidance for VM live migration and rebalancing operations.

**When to consult this document**: When migrations are slow, when planning large-scale rebalancing, or when optimizing cluster performance for frequent migrations.

---

## Official Sources

This document is compiled from official Red Hat documentation:

- [Live Migrating VMs with OpenShift Virtualization](https://developers.redhat.com/articles/2025/07/14/live-migrating-vms-openshift-virtualization) - Red Hat Developer (2025-07-14)
- [Best Practices for Virtual Machine Deployments on OpenShift Virtualization](https://learn.microsoft.com/en-us/azure/openshift/best-practices-openshift-virtualization) - Microsoft Azure Red Hat OpenShift (2026-02-16)
- [Announcing Right-Sizing for OpenShift Virtualization](https://developers.redhat.com/articles/2025/04/28/announcing-right-sizing-openshift-virtualization) - Red Hat Developer (2025-04-28)
- [Best Practices to Deploy VMs in Red Hat OpenShift Virtualization](https://docs.netapp.com/us-en/netapp-solutions-virtualization/openshift/os-osv-bpg.html) - NetApp Solutions

---

## Right-Sizing Virtual Machines

### Why Right-Sizing Matters for Rebalancing

Properly sized VMs:
- Migrate faster (smaller memory footprint)
- Reduce network bandwidth requirements
- Improve cluster resource utilization
- Enable more efficient load balancing
- Prevent resource contention during migrations

### Right-Sizing Methodology

**Step 1: Define Health Metrics**

Target healthy resource utilization ranges:

| Resource | Target Range | Warning Threshold | Critical Threshold |
|----------|--------------|-------------------|-------------------|
| CPU Utilization | 60-70% average | >80% | >90% |
| Memory Pressure | <80% | >85% | >95% |
| Disk I/O Latency | <10ms | >50ms | >100ms |
| Network Throughput | <70% capacity | >80% | >90% |

**Step 2: Monitor VM Resource Usage**

**Using MCP Tools:**

**MCP Tool**: `pods_top` (from openshift-virtualization)

**Parameters**:
```json
{
  "all_namespaces": true,
  "label_selector": "kubevirt.io=virt-launcher"
}
```

This returns CPU and memory usage for all VM launcher pods. Filter by specific namespace or VM name as needed.

**For detailed metrics:**

**MCP Tool**: `nodes_stats_summary` (from openshift-virtualization)

**Parameters**:
```json
{
  "name": "<node-name>"
}
```

Review `.pods[].containers[]` metrics for specific VM resource consumption including:
- `cpu.usageNanoCores` - Current CPU usage
- `memory.workingSetBytes` - Active memory usage
- `rootfs.usedBytes` - Disk usage

**Step 3: Analyze Historical Data**

Collect metrics over time (minimum 7 days for meaningful patterns):

- Peak usage periods
- Resource saturation events
- Correlation between workload and resource consumption
- Trending (growing vs stable resource needs)

**Step 4: Adjust VM Specifications**

Based on observed metrics, resize VMs using `resources_get` and `resources_create_or_update`:

**Example: Resize VM Memory**

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

Modify `.spec.template.spec.domain.resources.requests.memory` based on usage analysis, then update with `resources_create_or_update`.

**Avoid Overprovisioning:**
- Don't rely on on-premises sizing references
- Benchmark your actual workloads
- Consider OpenShift Virtualization architectural overhead (see Architectural Overhead section)

---

## Architectural Overhead

### OpenShift Virtualization Performance Characteristics

Running VMs in OpenShift Virtualization introduces architectural overhead compared to bare metal or native pods:

**Observed Performance (Azure Red Hat OpenShift with Standard_D96ds_v5 nodes, OpenShift 4.20, Virtualization 4.20):**

| Workload Type | VM Performance | Pod Performance | Overhead |
|---------------|----------------|-----------------|----------|
| **Compute** (events/sec) | 525,022 | 546,997 | ~4% slower |
| **Compute** (latency ms) | 0.70 | 0.65 | ~8% higher latency |
| **Storage** (1 thread TPM) | 4,332 | 6,303 | ~31% slower |
| **Storage** (32 threads TPM) | 64,294 | 103,359 | ~38% slower |
| **Network** (64B, 1 thread Gbps) | 0.4 | 0.9 | ~56% slower |
| **Network** (1024B, 8 threads Gbps) | 24.7 | 28.9 | ~15% slower |

**Key Takeaways:**
- Compute overhead is minimal (~4-8%)
- Storage and network have higher overhead (15-56% depending on workload)
- Multi-threaded workloads show better relative performance

**Implications for Rebalancing:**
- VMs require more time to migrate than equivalent containerized workloads
- Plan capacity with overhead in mind (don't fill nodes to 100%)
- Network-intensive VMs benefit most from dedicated migration networks
- Consider workload characteristics when planning concurrent migrations

---

## Tuned Configuration for High-Performance VMs

### SAP HANA Tuning Example

For database and high-performance workloads, apply tuned profiles to guest OS:

**Tuned Profile (RHEL Guest):**

```ini
[main]
summary=Optimize for SAP HANA and high-performance VMs

[cpu]
force_latency=cstate.id:3|70
governor=performance
energy_perf_bias=performance
min_perf_pct=100

[vm]
transparent_hugepages=never

[sysctl]
# Semaphore limits
kernel.sem = 32000 1024000000 500 32000

# Disable NUMA balancing for predictable performance
kernel.numa_balancing = 0

# Scheduler tuning for low latency
kernel.sched_min_granularity_ns = 3000000
kernel.sched_wakeup_granularity_ns = 4000000

# Memory management
vm.dirty_ratio = 40
vm.dirty_background_ratio = 10
vm.swappiness = 10
```

**When to Apply:**
- Database VMs (PostgreSQL, MySQL, Oracle, SAP HANA)
- Real-time analytics workloads
- Low-latency trading platforms
- High-performance computing (HPC) VMs

**Impact on Migration:**
- Reduces dirty page rate (faster convergence)
- More predictable migration times
- Better performance during and after migration

---

## CPU and Memory Overcommit

### Understanding Overcommit Ratios

OpenShift Virtualization allows overcommit of CPU and memory resources, enabling higher VM density per node.

**Default Overcommit Ratios:**
- CPU: No overcommit (1:1 mapping)
- Memory: No overcommit (1:1 mapping)

**Recommended Production Limits (Red Hat Guidance):**
- **CPU Overcommit**: Maximum 1.8x physical cores
- **Memory Overcommit**: Maximum 0.9x physical memory

**Consequences of Exceeding Limits:**
- **CPU**: Throttling causes slowness across all workloads on affected node
- **Memory**: OOM (Out of Memory) kills, VM crashes, data loss

### Configuring Overcommit

**Update HyperConverged CR using MCP Tools:**

**Step 1: Get HyperConverged resource**

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

**Step 2: Modify overcommit configuration**

Add to `.spec.resourceRequirements`:

```yaml
spec:
  resourceRequirements:
    vmiCPUAllocationRatio: 1.5    # Allow 1.5x CPU overcommit
    vmiMemoryOvercommitPercent: 20 # Allow 20% memory overcommit
```

**Step 3: Update using `resources_create_or_update`**

**Best Practices:**
- Use conservative overcommit for production (1.2x CPU max, 10% memory max)
- Use higher overcommit for dev/test (1.8x CPU, 20% memory acceptable)
- Monitor node resource usage closely after enabling overcommit
- Adjust based on actual VM behavior patterns

**Impact on Rebalancing:**
- Higher overcommit = more VMs per node = longer migration times
- Rebalancing may be needed more frequently with overcommit
- Target node capacity calculations must account for overcommit ratios

---

## Network Performance Tuning

### MTU Configuration

**Why MTU Matters:**
- Default MTU (1500 bytes) causes fragmentation for large data transfers
- Jumbo frames (MTU 9000) significantly improve network efficiency
- Critical for large VM migrations (>100GB memory)

**Set MTU in NetworkAttachmentDefinition:**

When creating dedicated migration network, include MTU setting:

**MCP Tool**: `resources_create_or_update` (from openshift-virtualization)

**Parameters** (excerpt):
```json
{
  "resource": "apiVersion: k8s.cni.cncf.io/v1\nkind: NetworkAttachmentDefinition\nmetadata:\n  name: migration-network\n  namespace: openshift-cnv\nspec:\n  config: '{\n    \"cniVersion\": \"0.3.1\",\n    \"name\": \"migration-bridge\",\n    \"type\": \"macvlan\",\n    \"master\": \"eth1\",\n    \"mode\": \"bridge\",\n    \"mtu\": 9000,\n    \"ipam\": {...}\n  }'"
}
```

**Validate MTU:**

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

Check `.spec.config` for `"mtu": 9000`.

### NAPI and Multiqueue Tuning

For network-intensive workloads, enable multiqueue virtio-net:

**VM Configuration:**
```yaml
spec:
  template:
    spec:
      domain:
        devices:
          interfaces:
          - name: default
            model: virtio
            masquerade: {}
            ports:
            - port: 80
            networkInterfaceMultiqueue: true  # Enable multiqueue
```

**Benefits:**
- Parallelizes network processing across multiple vCPUs
- Improves throughput for high-bandwidth workloads
- Reduces latency for network-intensive applications

**When to Use:**
- VMs with >4 vCPUs
- High network throughput requirements (>10Gbps)
- Web servers, load balancers, network appliances

---

## Storage Performance Optimization

### Storage Class Selection

Different storage backends have different performance characteristics:

| Storage Backend | IOPS | Latency | Throughput | Best For |
|-----------------|------|---------|------------|----------|
| OpenShift Data Foundation (ODF) | High | Low (<5ms) | Very High | General purpose, production |
| Azure NetApp Files (ANF) Premium | Very High | Very Low (<1ms) | Very High | Database, high-performance |
| NFS-CSI (SSD-backed) | Medium | Medium (5-10ms) | High | Dev/test, general use |
| AWS EBS gp3 | Medium | Medium (10-20ms) | Medium | Cost-effective, RWO only |

**Check Storage Class Performance:**

**MCP Tool**: `resources_get` (from openshift-virtualization)

**Parameters**:
```json
{
  "apiVersion": "storage.k8s.io/v1",
  "kind": "StorageClass",
  "name": "<storage-class-name>"
}
```

Review `.parameters` for performance tier, provisioning type, and backend configuration.

### Storage Limits (NetApp ONTAP)

When using NetApp storage backends, configure limits to prevent resource exhaustion:

**SVM Volume Limits:**

Set maximum volumes per SVM to prevent Trident from consuming all storage capacity.

**Storage Quotas:**

Implement storage limits on SVMs to enforce resource boundaries.

**Trident Backend Parameters:**

Configure in Trident backend definition:
- `limitVolumeSize`: Maximum individual volume size (e.g., "100Gi")
- `limitVolumePoolSize`: Maximum FlexVol size for economy drivers (e.g., "500Gi")

**Impact on Rebalancing:**
- Storage limits prevent VMs from growing unbounded
- Predictable storage capacity aids in target node selection
- Quota enforcement ensures fair resource distribution

---

## Migration Bandwidth Management

### Bandwidth Per Migration

**Purpose**: Limit bandwidth consumption per migration to prevent network saturation.

**Default**: Unlimited (no bandwidth limit)

**When to Set:**
- Shared application network (no dedicated migration network)
- Multiple concurrent migrations planned
- Network capacity constraints

**Configuration Using MCP Tools:**

**Step 1: Get HyperConverged resource**

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

**Step 2: Set bandwidth limit**

Modify `.spec.liveMigrationConfig.bandwidthPerMigration`:

```yaml
spec:
  liveMigrationConfig:
    bandwidthPerMigration: 64Mi   # 64 MiB/s per migration
```

Common values:
- `32Mi` - Conservative (256 Mbps)
- `64Mi` - Default (512 Mbps)
- `128Mi` - High bandwidth (1 Gbps)
- Omit field for unlimited

**Step 3: Update using `resources_create_or_update`**

**Monitoring Bandwidth Usage:**

**MCP Tool**: `nodes_stats_summary` (from openshift-virtualization)

**Parameters**:
```json
{
  "name": "<node-name>"
}
```

Review `.network.interfaces[].rxBytes` and `.network.interfaces[].txBytes` for current throughput.

**Tuning Guidance:**
- Start conservative (32-64Mi) and increase if migrations are slow
- Monitor network utilization during migrations
- Unlimited bandwidth is acceptable with dedicated migration network

---

## Concurrency Limits Tuning

### Parallel Migrations Per Cluster

**Default**: 5 concurrent migrations cluster-wide

**When to Increase:**
- Dedicated migration network with high bandwidth (100Gbps)
- Routine maintenance windows requiring many migrations
- Cluster has >20 nodes

**When to Decrease:**
- Network saturation observed
- Migration failures due to timeouts
- Shared application network

**Configuration:**

Modify `.spec.liveMigrationConfig.parallelMigrationsPerCluster` in HyperConverged CR:

```yaml
spec:
  liveMigrationConfig:
    parallelMigrationsPerCluster: 10  # Increase from default 5
```

**Conservative**: 3-5 migrations
**Moderate**: 5-10 migrations
**Aggressive**: 10-20 migrations (requires dedicated network)

### Parallel Outbound Migrations Per Node

**Default**: 2 concurrent outbound migrations per source node

**Recommendation**: Keep at 2 to prevent single-node overload.

**Why 2 is Optimal:**
- Prevents source node CPU/memory saturation
- Limits network bandwidth consumption per node
- Avoids cascading performance degradation
- Tested and validated by Red Hat

**Only increase to 3-4 if:**
- Node has very high CPU/memory headroom (>50% free)
- Dedicated high-bandwidth migration network
- Extensive testing validates stability

---

## Timeout Configuration

### Completion Timeout Per GiB

**Default**: 800 seconds per GiB of VM memory

**Calculation**: For a 16GB VM, timeout = 16 * 800 = 12,800 seconds (~3.5 hours)

**When to Increase:**
- High dirty page rate workloads (databases, caching systems)
- VMs with >100GB memory
- Network bandwidth constraints

**When to Decrease:**
- Fast dedicated migration network (100Gbps)
- Low dirty page rate (mostly idle VMs)
- Want faster failure detection

**Configuration:**

Modify `.spec.liveMigrationConfig.completionTimeoutPerGiB` in HyperConverged CR:

```yaml
spec:
  liveMigrationConfig:
    completionTimeoutPerGiB: 1200  # Increase for large/busy VMs
```

**Tuning by Workload Type:**

| Workload Type | Recommended Timeout | Rationale |
|---------------|---------------------|-----------|
| Database (write-heavy) | 1200-1600s | High dirty page rate |
| Web server (mostly read) | 600-800s | Low dirty page rate |
| Caching (Redis/Memcached) | 1600-2000s | Very high dirty page rate |
| General purpose | 800s (default) | Balanced |

### Progress Timeout

**Default**: 150 seconds without progress before cancellation

**Purpose**: Detects stuck migrations and fails fast rather than hanging indefinitely.

**When to Increase:**
- Very large VMs (>500GB memory)
- Slow networks (<1Gbps)
- Initial memory copy takes >2 minutes

**When to Decrease:**
- Want faster failure detection
- Prefer to retry quickly rather than wait

**Configuration:**

Modify `.spec.liveMigrationConfig.progressTimeout` in HyperConverged CR:

```yaml
spec:
  liveMigrationConfig:
    progressTimeout: 300  # 5 minutes without progress
```

**Recommended Values:**
- Small VMs (<50GB): 150s (default)
- Medium VMs (50-200GB): 200-300s
- Large VMs (>200GB): 300-600s

---

## Monitoring and Observability

### Key Metrics to Monitor

**During Rebalancing Operations:**

1. **Migration Progress**

**MCP Tool**: `resources_list` (from openshift-virtualization)

**Parameters**:
```json
{
  "apiVersion": "kubevirt.io/v1",
  "kind": "VirtualMachineInstanceMigration"
}
```

Monitor `.status.phase` for each migration (Pending → Scheduling → PreparingTarget → Running → Succeeded).

2. **Node Resource Usage**

**MCP Tool**: `nodes_top` (from openshift-virtualization)

**Parameters**:
```json
{
  "name": "<node-name>"
}
```

Track CPU and memory utilization before, during, and after migrations.

3. **Network Throughput**

**MCP Tool**: `nodes_stats_summary` (from openshift-virtualization)

**Parameters**:
```json
{
  "name": "<node-name>"
}
```

Review `.network.interfaces[]` metrics for bandwidth usage.

4. **VM Health**

**MCP Tool**: `resources_get` (from openshift-virtualization)

**Parameters**:
```json
{
  "apiVersion": "kubevirt.io/v1",
  "kind": "VirtualMachineInstance",
  "namespace": "<namespace>",
  "name": "<vm-name>"
}
```

Check `.status.conditions[]` for VM health status.

### Performance Benchmarking

**Before Rebalancing:**
- Establish baseline performance metrics
- Document current resource utilization
- Identify performance-sensitive VMs

**During Rebalancing:**
- Monitor migration duration
- Track network bandwidth consumption
- Watch for resource contention

**After Rebalancing:**
- Validate improved load distribution
- Confirm no performance degradation
- Document improvements achieved

**Tools for Benchmarking:**
- Apache JMeter (web application load testing)
- stress-ng (CPU/memory stress testing)
- fio (storage I/O benchmarking)
- iperf3 (network throughput testing)

---

## Scaling Strategies

### Scale Out vs Scale Up

**Scale Out** (add more nodes):
- **Pros**: Better fault tolerance, more migration targets, horizontal capacity growth
- **Cons**: Higher complexity, more licensing costs, requires cluster expansion

**Scale Up** (larger node sizes):
- **Pros**: Simpler management, fewer migration hops, better resource consolidation
- **Cons**: Larger blast radius, limited by maximum instance size, single point of failure risk

**For Demanding Workloads:**

From Microsoft Azure Red Hat OpenShift guidance:
> "Scale out or up for demanding workloads: Add more nodes or upsize the nodes in your Azure Red Hat OpenShift cluster for high concurrency or resource-intensive applications."

**Recommendation:**
- Start with scale-up to minimum 8-core Azure VMs (per OpenShift Virtualization requirements)
- Scale-out when individual nodes exceed 70-80% sustained utilization
- Balance between node size and cluster size for optimal resilience

### Node Pool Strategy

**Workload-Specific Node Pools:**

Create dedicated node pools for different VM workload types using labels, taints, and tolerations:

**Example Node Pool Configuration:**

**Pool 1: General VMs**
- Node labels: `workload-type=general`
- Node taints: None
- VM tolerations: Not required

**Pool 2: High-Performance VMs**
- Node labels: `workload-type=high-performance`
- Node taints: `performance=dedicated:NoSchedule`
- VM tolerations: Match taint

**Pool 3: GPU Workloads**
- Node labels: `workload-type=gpu`
- Node taints: `nvidia.com/gpu=present:NoSchedule`
- VM tolerations: Match taint

**Apply Labels to Nodes Using MCP Tools:**

**MCP Tool**: `resources_get` then `resources_create_or_update` (from openshift-virtualization)

Get node, modify `.metadata.labels`, then update.

**Benefits:**
- Simplifies maintenance (drain entire pool)
- Limits blast radius (failures contained to pool)
- Improves resource efficiency (right-sized pools)
- Enables topology spread rules (VMs across zones/pools)

---

## Related Documentation

- [Live Migration Best Practices](./live-migration-best-practices.md) - Configuration parameters and requirements
- [Anti-Patterns](./anti-patterns.md) - Common mistakes to avoid
- [Production Considerations](./production-considerations.md) - Right-sizing, workload planning, HA strategies

---

**Last Updated**: 2026-02-24
**OpenShift Virtualization Versions**: 4.17, 4.18, 4.19, 4.20
**Status**: Production-ready guidance from official Red Hat sources
