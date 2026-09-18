# Anti-Patterns: What NOT to Do

**Purpose**: Common mistakes, anti-patterns, and pitfalls to avoid when rebalancing VMs in OpenShift Virtualization.

**When to consult this document**: Before planning rebalancing operations, when troubleshooting failures, or when designing cluster architecture.

---

## Official Sources

This document is compiled from official Red Hat documentation and community best practices:

- [Best Practices for Virtual Machine Deployments on OpenShift Virtualization](https://learn.microsoft.com/en-us/azure/openshift/best-practices-openshift-virtualization) - Microsoft Azure Red Hat OpenShift (2026-02-16)
- [Best Practices to Deploy VMs in Red Hat OpenShift Virtualization](https://docs.netapp.com/us-en/netapp-solutions-virtualization/openshift/os-osv-bpg.html) - NetApp Solutions
- [OpenShift Virtualization Best Practices](https://www.tigera.io/learn/guides/kubernetes-networking/openshift-virtualization/) - Tigera
- [Troubleshooting OpenShift Virtualization](https://access.redhat.com/articles/6256861) - Red Hat Customer Portal

---

## Storage Anti-Patterns

### ❌ Anti-Pattern 1: Using RWO Storage for Live Migration

**What NOT to Do:**
```yaml
# BAD: VM using ReadWriteOnce storage
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: vm-disk
spec:
  accessModes:
  - ReadWriteOnce  # Cannot live migrate!
  storageClassName: gp3
```

**Why It Fails:**

From Red Hat documentation:
> "Live migration requires the use of a shared storage solution that provides ReadWriteMany (RWX) access mode. The VM disks should be backed by storage option that provides RWX access mode."

**Error Message:**
```
cannot migrate VMI: PVC vm-disk is not shared, live migration requires
that all PVCs must be shared (using ReadWriteMany access mode)
```

**Correct Approach:**

**Before Planning Live Migration**, verify storage using MCP tools:

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

Check `.spec.accessModes` includes `"ReadWriteMany"`.

**If RWO storage**, use **cold migration** instead (see REBALANCE_MANUAL.md).

**Storage Types Supporting RWX:**
- ✅ NFS (ontap-nas driver)
- ✅ SMB/CIFS (ontap-nas driver)
- ✅ iSCSI/FC (ontap-san driver, **raw block mode only**)
- ❌ AWS EBS gp3 (RWO only)
- ❌ Local storage (RWO only)

---

### ❌ Anti-Pattern 2: Not Setting SVM Volume Limits

**What NOT to Do:**

Deploy Trident without configuring SVM (Storage Virtual Machine) volume limits, allowing unchecked resource consumption.

**Why It's Dangerous:**

From NetApp documentation:
> "Set volume limits to prevent Trident from consuming all storage"

**Impact:**
- Trident creates unlimited volumes
- Storage backend exhausted
- Other workloads starved of storage
- Production outages

**Correct Approach:**

Configure limits at multiple levels:

**1. SVM-level volume limit:**
```bash
vserver modify -vserver <svm_name> -max-volumes <num_of_volumes>
```

**2. Storage limits on SVM:**
```bash
vserver create -vserver vserver_name -aggregate aggregate_name -storage-limit value
```

**3. Trident backend parameters:**
- `limitVolumeSize`: Maximum volume size created by Trident (e.g., "100Gi")
- `limitVolumePoolSize`: Maximum FlexVol size for economy drivers (e.g., "500Gi")

---

### ❌ Anti-Pattern 3: Enabling showmount Without Justification

**What NOT to Do:**

Leave `showmount` enabled on NFS SVMs, exposing volume information to unauthorized clients.

**Why It's a Security Risk:**

From NetApp documentation:
> "Disable showmount to prevent unauthorized volume discovery"

**Correct Approach:**

Disable showmount unless specifically required:

```bash
vserver nfs modify -vserver <svm_name> -showmount disabled
```

Implement separate export policies for infrastructure vs application nodes for granular access control.

---

## Scheduling and Node Placement Anti-Patterns

### ❌ Anti-Pattern 4: Excessive Affinity Rules

**What NOT to Do:**

Apply too many complex affinity, anti-affinity, node selector, and toleration rules to VMs.

**Why It's Problematic:**

From community best practices:
> "Too many rules make scheduling slow and hard to reason about."

From Red Hat documentation:
> "Affinity rules only apply during scheduling. OpenShift Container Platform does not reschedule running workloads if the constraints are no longer met."

**Impact:**
- Slow VM scheduling (scheduler overhead)
- Impossible-to-satisfy constraints (VM stuck in Pending)
- Difficult troubleshooting (complex rule interactions)
- No automatic rebalancing when constraints violated

**Correct Approach:**

**Keep rules simple and minimal:**

```yaml
# GOOD: Simple, clear node selector
spec:
  template:
    spec:
      nodeSelector:
        workload-type: virtualization
```

```yaml
# BAD: Too many overlapping constraints
spec:
  template:
    spec:
      nodeSelector:
        node-role.kubernetes.io/worker: ""
        workload-type: virtualization
        zone: us-east-1a
        instance-type: m5.4xlarge
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchExpressions:
              - key: app
                operator: In
                values: [web, database, cache]
            topologyKey: kubernetes.io/hostname
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: tier
                  operator: In
                  values: [frontend]
              topologyKey: failure-domain.beta.kubernetes.io/zone
      tolerations:
      - key: dedicated
        operator: Equal
        value: virtualization
        effect: NoSchedule
      - key: high-performance
        operator: Exists
        effect: NoSchedule
```

**Recommendation:**
- Use **one** primary constraint (nodeSelector OR affinity)
- Add tolerations only when nodes have taints
- Avoid mixing required and preferred affinity rules
- Document the intent of each rule

---

### ❌ Anti-Pattern 5: Not Planning for Node Failures

**What NOT to Do:**

Rely on automatic VM failover without configuring machine health checks.

**Why It Fails:**

From Red Hat documentation:
> "If a node fails and machine health checks are not deployed on your cluster, virtual machines (VMs) with RunStrategy: Always configured are not automatically relocated to healthy nodes. To trigger VM failover, you must manually delete the Node object."

**Impact:**
- VMs remain assigned to failed node
- Manual intervention required for recovery
- Extended downtime during node failures

**Correct Approach:**

**1. Deploy Machine Health Checks:**

Configure cluster-level machine health checks to detect and remediate node failures automatically.

**2. Use RunStrategy: Always for HA VMs:**

```yaml
spec:
  runStrategy: Always  # Ensures VM restarts after node recovery
```

**3. Implement VM Replication:**

For critical VMs, create replicas with anti-affinity rules to ensure distribution across different nodes/zones.

**4. Monitor Node Health:**

**MCP Tool**: `resources_list` (from openshift-virtualization)

**Parameters**:
```json
{
  "apiVersion": "v1",
  "kind": "Node"
}
```

Filter for nodes where `.status.conditions[]` shows `Ready=False` or other unhealthy states.

---

## Resource Management Anti-Patterns

### ❌ Anti-Pattern 6: Exceeding CPU Overcommit Limits

**What NOT to Do:**

Configure CPU overcommit ratio >1.8x physical cores.

**Why It's Dangerous:**

From Red Hat documentation:
> "CPU over-commitment ratio must not exceed 1.8x of the number of physical cores while memory usage may not exceed 0.9x of the physical memory available in a cluster. CPU over-commitment leads to throttling, causing slowness of all workloads on the impacted node."

**Impact:**
- CPU throttling across ALL VMs on node
- Unpredictable performance degradation
- Cascading slowness affecting entire cluster
- User-facing application latency

**Correct Approach:**

**Check Current Overcommit:**

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

Review `.spec.resourceRequirements.vmiCPUAllocationRatio`.

**Safe Limits:**
- **Production**: 1.0-1.2x (no/minimal overcommit)
- **Dev/Test**: 1.2-1.5x (moderate overcommit)
- **Absolute Maximum**: 1.8x (with careful monitoring)

**Never Exceed**: 1.8x CPU or 0.9x memory limits.

---

### ❌ Anti-Pattern 7: Applying Strict Resource Limits to VMs

**What NOT to Do:**

Set both resource requests **and** limits on VMs without specific governance requirements.

**Why It's Problematic:**

From Microsoft Azure Red Hat OpenShift guidance:
> "Avoid strict resource limits: Set only guest memory for VMs; avoid strict resource limits unless required for governance."

**Impact:**
- CPU throttling even when node has spare capacity
- Reduced VM performance
- Wasted cluster resources
- Difficult troubleshooting (invisible throttling)

**Correct Approach:**

**Set requests only:**

```yaml
# GOOD: Requests only (allows bursting)
spec:
  template:
    spec:
      domain:
        resources:
          requests:
            memory: 16Gi
            cpu: 4
```

```yaml
# BAD: Requests + limits (strict throttling)
spec:
  template:
    spec:
      domain:
        resources:
          requests:
            memory: 16Gi
            cpu: 4
          limits:  # Avoid unless required
            memory: 16Gi
            cpu: 4
```

**Only set limits when:**
- Governance policies mandate strict resource boundaries
- Multi-tenant environments require isolation
- Preventing one VM from starving others

---

### ❌ Anti-Pattern 8: Relying on On-Premises Sizing References

**What NOT to Do:**

Size VMs in OpenShift Virtualization based on on-premises VM sizes without testing.

**Why It Fails:**

From Microsoft Azure Red Hat OpenShift guidance:
> "Avoid relying solely on on-premises sizing references; benchmark your own workloads to inform right sizing."

**Impact:**
- Overprovisioned VMs (wasted resources)
- Underprovisioned VMs (performance issues)
- Unexpected architectural overhead (VMs != native pods)
- Incorrect migration time estimates

**Correct Approach:**

**1. Benchmark workloads in OpenShift Virtualization:**
- Deploy test VMs with various sizes
- Run representative workload tests
- Measure actual performance vs requirements

**2. Account for architectural overhead:**

Expect 4-56% performance overhead vs bare metal (see performance-tuning.md for details).

**3. Monitor and adjust:**

**MCP Tool**: `pods_top` (from openshift-virtualization)

**Parameters**:
```json
{
  "all_namespaces": true,
  "label_selector": "kubevirt.io=virt-launcher"
}
```

Track actual resource usage and resize VMs accordingly.

---

## Network Anti-Patterns

### ❌ Anti-Pattern 9: Using OVN-Kubernetes with Linux Bridge on Default Interface

**What NOT to Do:**

Attempt to attach a Linux bridge or bonding device to the host's default interface when using OVN-Kubernetes CNI.

**Why It Fails:**

From Red Hat documentation:
> "If your OpenShift Container Platform cluster uses OVN-Kubernetes as the default CNI provider, you cannot attach a Linux bridge or bonding device to a host's default interface."

**Impact:**
- Network configuration failures
- VM networking broken
- Migration network setup fails

**Correct Approach:**

**Option 1: Use secondary network interface**

Attach Linux bridge to a different physical interface (not the default).

**Option 2: Switch to OpenShift SDN CNI**

If Linux bridge on default interface is required, reconfigure cluster to use OpenShift SDN instead of OVN-Kubernetes.

**Option 3: Use OVS bridge instead**

For migration networks, use Open vSwitch bridge (compatible with OVN-Kubernetes).

---

### ❌ Anti-Pattern 10: Ignoring MTU Mismatches

**What NOT to Do:**

Mix network types with different default MTUs without explicit configuration.

**Why It's Problematic:**

From Red Hat documentation:
> "When a virtual machine interface is connected to an OVS bridge, the default MTU is 1400, but when connected to a Linux bridge, the default MTU is 1500."

**Impact:**
- Packet fragmentation
- Reduced network performance
- Subtle communication failures
- Migration slowdowns

**Correct Approach:**

**Explicitly set MTU in NetworkAttachmentDefinition:**

```json
{
  "cniVersion": "0.3.1",
  "name": "migration-bridge",
  "type": "macvlan",
  "master": "eth1",
  "mode": "bridge",
  "mtu": 9000,  # Explicit MTU setting
  "ipam": {...}
}
```

**Validate MTU consistency across all interfaces involved in migration.**

---

## Architecture and Platform Anti-Patterns

### ❌ Anti-Pattern 11: Using RHEL Compute Nodes

**What NOT to Do:**

Deploy OpenShift Virtualization on Red Hat Enterprise Linux (RHEL) compute nodes.

**Why It Fails:**

From Red Hat documentation:
> "OpenShift Virtualization requires Red Hat Enterprise Linux CoreOS (RHCOS) compute nodes. Even though it is possible to deploy Red Hat Enterprise Linux (RHEL) compute nodes, they are incompatible with OpenShift Virtualization."

**Impact:**
- VM scheduling failures
- Unsupported configuration
- Migration failures
- No Red Hat support

**Correct Approach:**

**Verify all nodes are RHCOS:**

**MCP Tool**: `resources_list` (from openshift-virtualization)

**Parameters**:
```json
{
  "apiVersion": "v1",
  "kind": "Node"
}
```

For each node, check `.status.nodeInfo.osImage` contains "CoreOS".

**If RHEL nodes detected:**
- Replace with RHCOS nodes
- Do NOT schedule VMs on RHEL nodes
- Remove RHEL nodes from cluster before deploying virtualization workloads

---

### ❌ Anti-Pattern 12: Placing Master Nodes on Same VMware Host

**What NOT to Do:**

In VMware-based deployments, place multiple OpenShift master nodes on the same VMware ESXi host.

**Why It's Dangerous:**

From VMware best practices:
> "Critical best practices include: distributing the 3 virtual master nodes across different VMware hosts, placing each master node on a separate datastore, and avoiding hosting master nodes on datastores with high I/O workloads."

**Impact:**
- Single point of failure (host failure kills multiple masters)
- etcd performance degradation (etcd is latency-sensitive)
- Cluster control plane outage
- Violates high-availability principles

**Correct Approach:**

**1. Distribute master nodes across different VMware hosts**

Use VM anti-affinity rules to enforce separation.

**2. Use separate datastores for each master node**

Prevents storage failure from affecting multiple masters.

**3. Avoid high I/O datastores for master nodes**

etcd is sensitive to disk latency; use low-latency storage.

---

### ❌ Anti-Pattern 13: Ignoring etcd Latency Sensitivity

**What NOT to Do:**

Place etcd (control plane) on high-latency storage or overloaded nodes.

**Why It's Critical:**

From best practices:
> "The etcd component hosted on control-plane nodes is usually the component most sensitive to latency issues."

**Impact:**
- Cluster control plane slowness
- API server timeouts
- Failed VM operations
- Cluster instability

**Correct Approach:**

**1. Use low-latency storage for control plane nodes:**
- SSD-backed storage (not HDD)
- Local NVMe if available
- Avoid shared storage with high I/O contention

**2. Monitor etcd latency:**

Prometheus metrics: `etcd_disk_wal_fsync_duration_seconds`

**Target**: <10ms for WAL fsync

**3. Isolate control plane from VM workloads:**

Use taints on master nodes to prevent VM scheduling.

---

## Migration Operation Anti-Patterns

### ❌ Anti-Pattern 14: Not Reducing VM Workload During Migration

**What NOT to Do:**

Attempt live migration of write-intensive VMs (databases, caches) under full load.

**Why It's Problematic:**

High memory write rate (dirty page rate) can exceed network transfer rate, preventing migration convergence.

**Impact:**
- Migration timeouts
- Failed migrations
- Extended migration duration
- Network saturation

**Correct Approach:**

**Before migrating write-intensive VMs:**

1. **Schedule migration during low-activity window** (off-hours, maintenance window)

2. **Temporarily reduce workload:**
   - Stop non-critical background processes
   - Scale down application traffic
   - Pause batch jobs

3. **Consider cold migration instead** for extremely write-heavy workloads (guaranteed completion)

4. **Increase timeouts if load cannot be reduced:**

Modify `.spec.liveMigrationConfig.completionTimeoutPerGiB` in HyperConverged CR (see performance-tuning.md).

---

### ❌ Anti-Pattern 15: Parallel Migrations Without Dedicated Network

**What NOT to Do:**

Run many concurrent migrations on shared application network without bandwidth limits.

**Why It's Dangerous:**

- Saturates network bandwidth
- Degrades application performance
- Migration failures due to slow transfers
- Cascading performance impact

**Impact Observed:**

From search results:
> "Network saturation risk with concurrent migrations"

**Correct Approach:**

**Option 1: Use dedicated migration network** (see live-migration-best-practices.md)

**Option 2: Limit concurrent migrations:**

Modify `.spec.liveMigrationConfig.parallelMigrationsPerCluster` in HyperConverged CR:

```yaml
spec:
  liveMigrationConfig:
    parallelMigrationsPerCluster: 3  # Conservative limit
    bandwidthPerMigration: 64Mi      # Bandwidth cap per migration
```

**Option 3: Migrate sequentially**

Migrate VMs one at a time instead of batch operations.

---

### ❌ Anti-Pattern 16: Not Validating Migration Prerequisites

**What NOT to Do:**

Attempt migration without verifying storage, network, and capacity prerequisites.

**Why It Fails:**

Common failures:
- RWO storage → "PVC is not shared" error
- VM not running → "cannot migrate stopped VM"
- Node at capacity → ErrorUnschedulable
- Network issues → Migration timeout

**Correct Approach:**

**Always run pre-migration validation** (see live-migration-best-practices.md for complete checklist):

1. ✅ Verify PVC access modes (RWX required)
2. ✅ Check VM is running (VMI exists)
3. ✅ Validate target node capacity
4. ✅ Confirm virt-handler pods healthy
5. ✅ Check cluster migration limits

**Use Common Validation Logic from SKILL.md before every migration.**

---

## Production Deployment Anti-Patterns

### ❌ Anti-Pattern 17: Deploying to Production Without Testing

**What NOT to Do:**

Deploy VMs directly to production without dev/test validation.

**Why It's Risky:**

From best practices:
> "Begin with non-critical or dev/test workloads before moving production systems - this phased approach allows teams to gain hands-on experience while minimizing risk."

**Impact:**
- Unexpected performance issues
- Migration failures affecting production
- Learning curve impacts critical systems
- Difficult rollback

**Correct Approach:**

**Phased Rollout:**

**Phase 1: Development/Test**
- Deploy test VMs
- Validate performance and functionality
- Test migration workflows
- Gain operational experience

**Phase 2: Non-Critical Production**
- Migrate non-critical workloads
- Monitor performance and stability
- Refine sizing and configurations
- Build confidence

**Phase 3: Critical Production**
- Migrate critical workloads
- Ensure HA and DR configured
- 24/7 monitoring in place
- Rollback plan ready

---

### ❌ Anti-Pattern 18: Starting Big Instead of Small

**What NOT to Do:**

Provision large VM fleet from day one without iterative growth.

**Why It's Problematic:**

From best practices:
> "When starting with OpenShift Virtualization, it's essential to start small and scale up as needed to avoid over-provisioning and wasting resources."

**Impact:**
- Overprovisioned cluster (wasted costs)
- Underutilized resources
- Difficult rightsizing later
- Commitment to suboptimal architecture

**Correct Approach:**

**Start small:**
1. Deploy 5-10 VMs initially
2. Monitor resource usage patterns
3. Adjust sizing based on actual metrics
4. Gradually add VMs as needs grow

**Validate assumptions:**
- Test architectural overhead
- Measure actual performance
- Refine resource allocation
- Iterate on configuration

---

### ❌ Anti-Pattern 19: Not Monitoring After Rebalancing

**What NOT to Do:**

Execute rebalancing operations and assume everything is optimal without validation.

**Why It's Risky:**

- May not achieve intended load distribution
- Hidden performance degradation
- VMs scheduled suboptimally
- Resource contention not detected

**Correct Approach:**

**Post-Rebalancing Validation:**

**1. Verify VM placement:**

**MCP Tool**: `resources_get` (from openshift-virtualization)

For each migrated VM, confirm `.status.nodeName` matches expected target node.

**2. Monitor node resource usage:**

**MCP Tool**: `nodes_top` (from openshift-virtualization)

**Before vs After Comparison:**

| Node | CPU Before | CPU After | Improvement |
|------|------------|-----------|-------------|
| worker-01 | 85% | 65% | -20% ✓ |
| worker-02 | 78% | 64% | -14% ✓ |
| worker-03 | 42% | 58% | +16% |
| worker-04 | 38% | 53% | +15% |

**3. Validate application performance:**

Check application-specific metrics (response time, throughput, error rates).

**4. Monitor for 24-48 hours:**

Ensure sustained improvement without unexpected side effects.

---

## Summary: Anti-Pattern Checklist

Before rebalancing VMs, avoid these critical mistakes:

**Storage:**
- ❌ Using RWO storage for live migration
- ❌ Not setting SVM volume limits
- ❌ Leaving showmount enabled

**Scheduling:**
- ❌ Too many complex affinity rules
- ❌ Not configuring machine health checks

**Resources:**
- ❌ CPU overcommit >1.8x
- ❌ Strict resource limits without justification
- ❌ Using on-premises sizing without testing

**Network:**
- ❌ Linux bridge on default interface with OVN-Kubernetes
- ❌ Ignoring MTU mismatches
- ❌ Parallel migrations without dedicated network

**Platform:**
- ❌ Using RHEL compute nodes
- ❌ Master nodes on same VMware host
- ❌ Ignoring etcd latency sensitivity

**Operations:**
- ❌ Not reducing VM workload during migration
- ❌ Skipping pre-migration validation
- ❌ No post-rebalancing monitoring

**Production:**
- ❌ Deploying to production without testing
- ❌ Starting big instead of small

---

## Related Documentation

- [Live Migration Best Practices](./live-migration-best-practices.md) - What TO do for successful migrations
- [Performance Tuning](./performance-tuning.md) - Optimization strategies
- [Production Considerations](./production-considerations.md) - Right-sizing, workload planning, HA strategies

---

**Last Updated**: 2026-02-24
**OpenShift Virtualization Versions**: 4.17, 4.18, 4.19, 4.20
**Status**: Curated from official Red Hat sources and production experience
