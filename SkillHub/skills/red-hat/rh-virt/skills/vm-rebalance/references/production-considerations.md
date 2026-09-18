# Production Considerations for VM Rebalancing

**Purpose**: Production deployment guidance, workload planning, high availability strategies, and operational best practices for VM rebalancing in OpenShift Virtualization.

**When to consult this document**: Before deploying to production, when planning capacity, or when designing HA/DR strategies.

---

## Official Sources

This document is compiled from official Red Hat documentation:

- [Best Practices for Virtual Machine Deployments on OpenShift Virtualization](https://learn.microsoft.com/en-us/azure/openshift/best-practices-openshift-virtualization) - Microsoft Azure Red Hat OpenShift (2026-02-16)
- [Announcing Right-Sizing for OpenShift Virtualization](https://developers.redhat.com/articles/2025/04/28/announcing-right-sizing-openshift-virtualization) - Red Hat Developer (2025-04-28)
- [Best Practices to Deploy VMs in Red Hat OpenShift Virtualization](https://docs.netapp.com/us-en/netapp-solutions-virtualization/openshift/os-osv-bpg.html) - NetApp Solutions
- [OpenShift Virtualization Best Practices](https://trilio.io/openshift-virtualization/) - Trilio

---

## Workload Identification and Categorization

### Common Workload Types

Before provisioning VMs, categorize workloads to determine performance and resource requirements:

| Workload Type | Characteristics | Resource Profile | Migration Considerations |
|---------------|----------------|------------------|--------------------------|
| **General Purpose** | Web servers, app servers, CMS | Moderate CPU/memory | Easy to migrate, low dirty page rate |
| **Database** | RDBMS, NoSQL | High CPU, memory, consistent IOPS | High dirty page rate; schedule migrations carefully |
| **Real-time Analytics** | Operational dashboards | Low latency, high throughput | Sensitive to migration pause; use dedicated network |
| **AI/ML** | Training, inference | Very high CPU/GPU, memory | Large memory footprint; long migration times |
| **Data Streaming** | Event-driven architectures | High throughput, low latency | Network-intensive; avoid concurrent migrations |
| **Batch Processing** | Periodic jobs | Variable resources | Migrate during job idle periods |
| **HPC** | Scientific simulations | Very high CPU, memory | Extremely long migrations; consider cold migration |
| **Edge/IoT** | Sensor aggregation | Low resources | Easy to migrate, scale horizontally |
| **Media Processing** | Encoding, streaming | High CPU, network | High dirty page rate during processing |
| **Dev/Test** | Development environments | Variable | Higher overcommit acceptable |

### Workload Assessment Using MCP Tools

**Step 1: Inventory Current VMs**

**MCP Tool**: `resources_list` (from openshift-virtualization)

**Parameters**:
```json
{
  "apiVersion": "kubevirt.io/v1",
  "kind": "VirtualMachine"
}
```

**Step 2: Analyze Resource Usage**

**MCP Tool**: `pods_top` (from openshift-virtualization)

**Parameters**:
```json
{
  "all_namespaces": true,
  "label_selector": "kubevirt.io=virt-launcher"
}
```

**Step 3: Categorize by Usage Pattern**

Group VMs by observed characteristics:
- CPU-intensive: >70% CPU utilization
- Memory-intensive: >80% memory utilization
- I/O-intensive: High storage throughput
- Network-intensive: High network bandwidth

**Step 4: Plan Rebalancing Strategy**

Based on workload type:
- **CPU-intensive**: Balance CPU across nodes
- **Memory-intensive**: Balance memory across nodes
- **I/O-intensive**: Distribute across different storage backends
- **Network-intensive**: Stagger migrations to avoid saturation

---

## Right-Sizing Virtual Machines for Production

### Health Metrics Definition

Establish target ranges for healthy resource utilization:

**CPU Utilization:**
- **Target**: 60-70% average usage
- **Warning**: >80% sustained
- **Critical**: >90% sustained
- **Action**: Scale up VM or rebalance to less loaded node

**Memory Pressure:**
- **Target**: 70-80% utilization
- **Warning**: >85% with swap activity
- **Critical**: >95% or OOM events
- **Action**: Increase VM memory or reduce workload

**Disk I/O:**
- **Target**: <10ms latency, <70% queue depth
- **Warning**: >50ms latency
- **Critical**: >100ms latency or queue saturation
- **Action**: Move to faster storage tier or distribute workload

**Network Throughput:**
- **Target**: <70% interface capacity
- **Warning**: >80% sustained
- **Critical**: >90% or packet loss
- **Action**: Enable multiqueue, use faster NICs, rebalance

### Monitoring Setup Using MCP Tools

**VM-Level Metrics:**

**MCP Tool**: `pods_top` (from openshift-virtualization)

Provides current CPU and memory usage for VM launcher pods.

**Node-Level Metrics:**

**MCP Tool**: `nodes_top` (from openshift-virtualization)

Shows aggregate node resource consumption.

**Detailed Statistics:**

**MCP Tool**: `nodes_stats_summary` (from openshift-virtualization)

**Parameters**:
```json
{
  "name": "<node-name>"
}
```

Provides comprehensive metrics including:
- Per-pod resource usage
- Container-level metrics
- Filesystem usage
- Network interface statistics
- PSI (Pressure Stall Information) metrics on cgroup v2 systems

### Sizing Recommendations by Workload

**Database Workloads:**
- Start with: 4-8 vCPU, 16-32Gi memory
- Storage: Premium SSD or NVMe with RWX support
- Network: Enable multiqueue virtio-net
- Special: Consider dedicated CPU placement (`dedicatedCpuPlacement: true`)

**Web Servers:**
- Start with: 2-4 vCPU, 4-8Gi memory
- Storage: Standard SSD acceptable
- Network: Standard configuration sufficient
- Special: Scale horizontally rather than vertically

**AI/ML Workloads:**
- Start with: 8-16 vCPU, 32-64Gi memory
- Storage: High-performance SSD
- Network: High bandwidth (consider dedicated migration network)
- Special: GPU support currently not available (plan accordingly)

**Dev/Test Environments:**
- Start with: 1-2 vCPU, 2-4Gi memory
- Storage: Standard tier acceptable
- Network: Standard configuration
- Special: Higher overcommit ratios acceptable (1.5-1.8x CPU)

### Minimum Requirements

From Microsoft Azure Red Hat OpenShift documentation:
> "Minimum core requirement: OpenShift Virtualization requires a minimum of eight (8) core Azure VMs for OpenShift worker nodes."

**Implications for Rebalancing:**
- Worker nodes must have ≥8 cores
- Plan VM placement considering this minimum
- Avoid creating nodes smaller than this threshold

---

## High Availability Strategies

### VM-Level High Availability

**RunStrategy Configuration:**

```yaml
apiVersion: kubevirt.io/v1
kind: VirtualMachine
metadata:
  name: critical-app
spec:
  runStrategy: Always  # Ensures VM restarts after failures
```

**RunStrategy Options:**

| Strategy | Behavior | Use Case |
|----------|----------|----------|
| `Always` | VM runs continuously; restarts on failure | Production VMs requiring HA |
| `RerunOnFailure` | Restarts only if VM crashes | Batch workloads |
| `Manual` | User controls start/stop | Dev/test VMs |
| `Halted` | VM stays stopped | Maintenance, cold storage |

**Eviction Strategy:**

OpenShift Virtualization automatically sets `evictionStrategy` to `LiveMigrate` for VMs with RWX storage:

```yaml
spec:
  template:
    spec:
      evictionStrategy: LiveMigrate  # Automatically set for RWX VMs
```

**Note for Single Node OpenShift (SNO):**

From known issues:
> "In a Single Node OpenShift (SNO) cluster, a VMCannotBeEvicted alert occurs on virtual machines created from common templates that have the eviction strategy set to LiveMigrate."

**Workaround**: Use `evictionStrategy: None` for SNO clusters.

### Pod Anti-Affinity for VM Replicas

For critical applications, deploy multiple VM replicas with anti-affinity:

```yaml
apiVersion: kubevirt.io/v1
kind: VirtualMachine
metadata:
  name: web-server-replica-1
  labels:
    app: web-server
spec:
  template:
    metadata:
      labels:
        app: web-server
    spec:
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchExpressions:
              - key: app
                operator: In
                values:
                - web-server
            topologyKey: kubernetes.io/hostname  # Different nodes
```

**Benefits:**
- VMs distributed across different failure domains
- Node failure affects only one replica
- Improves overall availability

**Verify Distribution Using MCP Tools:**

**MCP Tool**: `resources_list` (from openshift-virtualization)

**Parameters**:
```json
{
  "apiVersion": "kubevirt.io/v1",
  "kind": "VirtualMachineInstance",
  "labelSelector": "app=web-server"
}
```

Check `.status.nodeName` for each instance to confirm distribution.

### Machine Health Checks

**Critical for Automatic Failover:**

From Red Hat documentation:
> "If a node fails and machine health checks are not deployed on your cluster, virtual machines (VMs) with RunStrategy: Always configured are not automatically relocated to healthy nodes."

**Deploy Machine Health Checks:**

Configure at cluster level to detect and remediate node failures. This enables automatic VM recovery without manual intervention.

**Monitor Node Health:**

**MCP Tool**: `resources_list` (from openshift-virtualization)

**Parameters**:
```json
{
  "apiVersion": "v1",
  "kind": "Node"
}
```

Filter for nodes where `.status.conditions[]` shows unhealthy states (`Ready=False`, `DiskPressure=True`, `MemoryPressure=True`).

### Topology Spread for Zone Resilience

For multi-zone clusters, use topology spread rules:

```yaml
spec:
  template:
    spec:
      topologySpreadConstraints:
      - maxSkew: 1
        topologyKey: topology.kubernetes.io/zone
        whenUnsatisfiable: DoNotSchedule
        labelSelector:
          matchLabels:
            app: critical-app
```

**Benefits:**
- VMs spread across availability zones
- Zone failure doesn't affect all replicas
- Improved disaster recovery

---

## Capacity Planning

### Cluster Sizing Approach

**Scale Out vs Scale Up:**

From Microsoft Azure Red Hat OpenShift guidance:
> "Scale out or up for demanding workloads: Add more nodes or upsize the nodes in your Azure Red Hat OpenShift cluster for high concurrency or resource-intensive applications."

**Scale Out (add more nodes):**
- **Pros**: Better fault tolerance, horizontal growth, more migration targets
- **Cons**: Higher complexity, more license costs, requires cluster expansion

**When to Scale Out:**
- Current nodes consistently >70-80% utilized
- Need more fault isolation
- Planning for growth
- HA requirements mandate distribution

**Scale Up (larger node sizes):**
- **Pros**: Simpler management, better resource consolidation, fewer migration hops
- **Cons**: Larger blast radius, limited by max instance size, single point of failure risk

**When to Scale Up:**
- VMs don't fit on existing nodes
- Few large VMs rather than many small VMs
- Simplicity valued over distribution

**Recommended Approach:**
1. Start with moderate node sizes (8-16 cores)
2. Scale out to 3-5 nodes minimum for HA
3. Scale up only when specific VMs require larger nodes
4. Maintain headroom (30-40% free capacity) for migrations and failures

### Node Pool Strategy

**Create workload-specific pools using labels and taints:**

**Pool Configuration Example:**

**General VM Pool:**
- Node size: 8-16 cores, 32-64GB RAM
- Labels: `workload-type=general`
- No taints (default scheduling)

**High-Performance Pool:**
- Node size: 16-32 cores, 64-128GB RAM
- Labels: `workload-type=high-performance`, `cpumanager=true`
- Taints: `performance=dedicated:NoSchedule`

**GPU Pool (future):**
- Node size: GPU-enabled instances
- Labels: `workload-type=gpu`
- Taints: `nvidia.com/gpu=present:NoSchedule`

**Configure Labels Using MCP Tools:**

**MCP Tool**: `resources_get` then `resources_create_or_update` (from openshift-virtualization)

**Step 1: Get Node**

**Parameters**:
```json
{
  "apiVersion": "v1",
  "kind": "Node",
  "name": "<node-name>"
}
```

**Step 2: Add Labels**

Modify `.metadata.labels`:
```json
{
  "workload-type": "high-performance",
  "cpumanager": "true"
}
```

**Step 3: Update Node**

Use `resources_create_or_update` with modified resource.

**Benefits of Node Pools:**
- Simplifies maintenance (drain entire pool)
- Limits blast radius (failures contained)
- Improves efficiency (right-sized for workload)
- Enables topology spread rules

### Capacity Headroom

**Reserve capacity for:**
- Node failures (n-1 redundancy minimum)
- VM migrations (target nodes need free resources)
- Burst workloads (temporary spikes)
- New VM deployments

**Recommended Headroom:**
- **Production**: 30-40% free capacity cluster-wide
- **Dev/Test**: 20-30% free capacity
- **Minimum**: 20% free capacity (below this, rebalancing becomes difficult)

**Monitor Capacity Using MCP Tools:**

**MCP Tool**: `nodes_top` (from openshift-virtualization)

Calculate cluster-wide utilization:
```
Total CPU Used / Total CPU Capacity = Cluster CPU Utilization
Total Memory Used / Total Memory Capacity = Cluster Memory Utilization
```

**Action Thresholds:**
- <70%: Healthy headroom
- 70-80%: Plan for expansion
- >80%: Add nodes urgently
- >90%: Emergency capacity issue

---

## Storage Planning for Production

### Storage Backend Selection

**OpenShift Data Foundation (ODF):**
- **Best for**: General purpose, production workloads
- **Performance**: High IOPS, low latency (<5ms)
- **RWX Support**: Yes
- **Considerations**: Requires dedicated storage nodes; use taints/tolerations to isolate ODF workload

**Azure NetApp Files (ANF):**
- **Best for**: High-performance databases, latency-sensitive apps
- **Performance**: Very high IOPS, very low latency (<1ms)
- **RWX Support**: Yes
- **Considerations**: Choose performance tier based on workload requirements

**NFS-CSI (SSD-backed):**
- **Best for**: Dev/test, general use
- **Performance**: Medium IOPS, medium latency (5-10ms)
- **RWX Support**: Yes
- **Considerations**: Cost-effective, sufficient for non-critical workloads

**AWS EBS gp3:**
- **Best for**: Cost-effective storage
- **Performance**: Medium IOPS, medium latency (10-20ms)
- **RWX Support**: No (RWO only)
- **Considerations**: Cannot use live migration; cold migration only

### Storage QoS and Limits

**NetApp ONTAP QoS:**

From NetApp documentation:
> "Apply QoS policies to SVMs to limit the number of IOPS consumable by the Trident provisioned volumes."

**Why QoS Matters:**
- Prevents one VM from starving others
- Protects non-Trident workloads from VM I/O impact
- Enforces fair resource distribution
- Predictable performance for all VMs

**SVM Isolation:**

From NetApp documentation:
> "Establish dedicated Storage Virtual Machines (SVMs) to provide isolation and administrative separation between tenants."

**Benefits:**
- Tenant isolation
- Privilege delegation
- Resource quota enforcement
- Security boundary

### Storage Validation Before Rebalancing

**For Live Migration, verify RWX storage:**

For each VM:

**Step 1: Get VM**

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

**Step 2: Extract PVC Names**

From `.spec.template.spec.volumes[].persistentVolumeClaim.claimName`.

**Step 3: Check PVC Access Mode**

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

**Required**: `.spec.accessModes` must include `"ReadWriteMany"`.

---

## Network Planning

### Dedicated Migration Network

**Production Requirement:**

For production clusters with large VMs or frequent migrations, a dedicated migration network is **highly recommended**.

**Benefits:**
- Isolates migration traffic from applications
- Enables 100Gbps bandwidth for large VM migrations
- Prevents network contention
- Improves security (separate VLAN)

**Implementation:**

See [live-migration-best-practices.md](./live-migration-best-practices.md) for complete configuration steps.

**Key Components:**
1. Secondary physical NIC or VLAN
2. NodeNetworkConfigurationPolicy (NNCP)
3. NetworkAttachmentDefinition (NAD)
4. HyperConverged CR configuration

### Network Performance Tuning

**MTU Configuration:**

Set to 9000 (jumbo frames) for migration networks:

```json
{
  "cniVersion": "0.3.1",
  "name": "migration-bridge",
  "type": "macvlan",
  "mtu": 9000,
  "ipam": {...}
}
```

**Multiqueue virtio-net:**

Enable for VMs with >4 vCPUs and high network throughput:

```yaml
spec:
  template:
    spec:
      domain:
        devices:
          interfaces:
          - name: default
            model: virtio
            networkInterfaceMultiqueue: true
```

### Network Isolation

**Namespace Separation:**

From best practices:
> "Use Namespaces to provide logical boundary for resources."

**Pod Security Policies:**

Disable privileged container capabilities for VM launcher pods to enhance security.

**Separate Export Policies:**

For NFS storage, implement separate export policies for infrastructure nodes vs application nodes.

---

## Operational Best Practices

### Phased Production Rollout

From best practices:
> "Begin with non-critical or dev/test workloads before moving production systems - this phased approach allows teams to gain hands-on experience while minimizing risk."

**Recommended Phases:**

**Phase 1: Development/Test (2-4 weeks)**
- Deploy 5-10 test VMs
- Validate performance vs expectations
- Test live and cold migration workflows
- Benchmark resource overhead
- Train operations team

**Phase 2: Non-Critical Production (4-8 weeks)**
- Migrate non-critical workloads (internal tools, QA environments)
- Monitor stability and performance
- Refine sizing and configurations
- Build runbooks and procedures
- Establish monitoring and alerting

**Phase 3: Critical Production (Ongoing)**
- Migrate critical workloads in prioritized order
- Ensure HA and DR fully configured
- 24/7 monitoring and on-call support
- Document rollback procedures
- Conduct regular DR tests

### Start Small, Scale Gradually

From best practices:
> "When starting with OpenShift Virtualization, it's essential to start small and scale up as needed to avoid over-provisioning and wasting resources."

**Growth Strategy:**

**Month 1-2: Pilot**
- 5-10 VMs
- Single workload type
- Limited users
- Focus on learning

**Month 3-6: Expansion**
- 20-50 VMs
- Multiple workload types
- Broader user base
- Refine processes

**Month 6-12: Production Scale**
- 50-200+ VMs
- All workload types
- Organization-wide
- Mature operations

**Benefits:**
- Avoids over-provisioning
- Iterative learning
- Cost-effective growth
- Risk mitigation

### Monitoring and Alerting

**Key Metrics to Monitor:**

**VM Health:**
- Status (Running, Stopped, Error)
- Resource utilization (CPU, memory, disk, network)
- Guest agent connectivity
- Migration status

**Node Health:**
- Resource utilization
- virt-handler pod status
- Network connectivity
- Storage backend health

**Cluster Health:**
- Current migration count vs limits
- HyperConverged CR status
- Storage capacity and performance
- Network saturation

**Migration Operations:**
- Success/failure rate
- Average migration duration
- Timeout occurrences
- Concurrent migration count

**Alert Thresholds:**

| Metric | Warning | Critical |
|--------|---------|----------|
| Node CPU | >80% | >90% |
| Node Memory | >85% | >95% |
| Migration Failures | >10% | >25% |
| virt-handler Pods Not Ready | Any | >1 |
| Cluster Migration Limit | >80% (4/5) | At limit (5/5) |

### Backup and Disaster Recovery

**VM Snapshots:**

Use vm-snapshot skills for point-in-time backups before risky operations:
- Before major migrations
- Before configuration changes
- Before OS upgrades in guest
- Regular backup schedule (daily/weekly)

**Disaster Recovery Planning:**

**Multi-Zone Deployment:**
- Distribute VMs across availability zones
- Use topology spread constraints
- Configure zone-resilient storage

**Backup Strategy:**
- Regular VM snapshots
- Export critical VM definitions
- Document restore procedures
- Test DR scenarios quarterly

**RTO/RPO Targets:**

Define recovery objectives:
- **RTO** (Recovery Time Objective): How quickly must VMs be recovered?
- **RPO** (Recovery Point Objective): How much data loss is acceptable?

**Example Targets:**

| Workload Tier | RTO | RPO | Strategy |
|---------------|-----|-----|----------|
| Critical | <15 min | <5 min | Multi-zone HA, frequent snapshots |
| Important | <1 hour | <1 hour | Daily snapshots, documented restore |
| Standard | <4 hours | <24 hours | Weekly snapshots, manual restore |

---

## Cost Optimization

### Resource Efficiency

**Avoid Overprovisioning:**

From Microsoft Azure Red Hat OpenShift guidance:
> "Avoid overprovisioning by aligning resources with actual usage patterns."

**Cost Factors:**
- Azure compute costs (worker node instances)
- OpenShift licensing
- VM operating system licensing
- Storage costs (capacity and performance tier)
- Network egress charges

**Optimization Strategies:**

**1. Right-size VMs based on actual usage**

Monitor with `pods_top` and resize VMs that are consistently under-utilized.

**2. Use appropriate storage tiers**

Don't use Premium storage for dev/test VMs; match tier to workload requirements.

**3. Implement auto-scaling**

For workloads with variable demand, use horizontal scaling rather than over-provisioning.

**4. Consolidate with overcommit**

In dev/test environments, use higher overcommit ratios (1.5-1.8x CPU) to maximize density.

**5. Schedule non-critical VMs**

Stop dev/test VMs during off-hours to reduce costs.

### Load Balancing for Efficiency

**Rebalancing Improves Efficiency:**
- Prevents hotspots (overloaded nodes)
- Enables better resource utilization
- Reduces need for emergency node additions
- Extends hardware lifespan (even wear)

**Regular Rebalancing Schedule:**
- **Weekly**: Review node utilization, plan migrations if imbalance detected
- **Monthly**: Comprehensive rebalancing to optimize distribution
- **Quarterly**: Capacity planning and infrastructure rightsizing

---

## Security Considerations

### Tenant Isolation

**Namespace Separation:**

Deploy VMs for different tenants/teams in separate namespaces.

**Network Policies:**

Implement NetworkPolicies to restrict inter-VM communication:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: tenant-isolation
  namespace: tenant-a
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          tenant: tenant-a
```

**RBAC:**

Grant users permissions only for their namespace's VMs, not cluster-wide access.

### VM Security Hardening

**Guest OS Security:**
- Regular patching and updates
- Disable unnecessary services
- Configure firewall rules
- Enable SELinux/AppArmor

**Secrets Management:**
- Use Kubernetes Secrets for credentials
- Inject secrets into VMs via cloud-init
- Rotate secrets regularly
- Never store secrets in VM images

**Access Control:**
- SSH key authentication only (disable password auth)
- Implement bastion/jump hosts
- Use VPN for remote access
- Audit access logs

---

## Related Documentation

- [Live Migration Best Practices](./live-migration-best-practices.md) - Configuration parameters and requirements
- [Performance Tuning](./performance-tuning.md) - Optimization strategies
- [Anti-Patterns](./anti-patterns.md) - Common mistakes to avoid

---

**Last Updated**: 2026-02-24
**OpenShift Virtualization Versions**: 4.17, 4.18, 4.19, 4.20
**Status**: Production-ready guidance from official Red Hat sources
