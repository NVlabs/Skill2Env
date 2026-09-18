---
name: system-context
description: |
  **CRITICAL**: This skill must be used for system inventory and context gathering. DO NOT use raw MCP tools like get_cve_systems or get_host_details directly.

  Gather system inventory and deployment context for CVE-affected systems, including RHEL version detection, environment classification, and deployment analysis.

  Use when:
  - "What systems are affected by CVE-X?"
  - "Gather system context for remediation planning"
  - "Analyze deployment architecture for CVE"
  - "Detect RHEL versions across affected systems"

  This skill orchestrates MCP tools (get_cve_systems, get_host_details) for system analysis.

  **IMPORTANT**: ALWAYS use this skill instead of calling get_cve_systems or get_host_details directly for system context gathering.
model: inherit
color: blue
license: Apache-2.0
allowed-tools: vulnerability__get_cve_systems inventory__get_host_details
---

# System Context Gathering Skill

This skill gathers comprehensive system inventory and deployment context for CVE-affected systems, enabling informed remediation strategy decisions.

**Integration with Remediation Skill**: The `/remediation` skill orchestrates this skill as part of its Step 3 (Gather Context) workflow. For standalone system analysis, you can invoke this skill directly.

## When to Use This Skill

**Use this skill directly when you need**:
- Understand which systems are affected by a CVE
- Analyze deployment architecture (Kubernetes, bare metal, VMs)
- Detect RHEL versions across infrastructure
- Classify systems by environment (dev/staging/prod)
- Gather context before remediation planning

**Use the `/remediation` skill when you need**:
- End-to-end CVE remediation workflow
- Integrated analysis → context → playbook → execution
- Automated remediation strategy determination

**How they work together**: The `/remediation` skill uses this skill's output to determine remediation strategy (batch vs individual, Kubernetes pod eviction requirements, maintenance window needs, etc.).

## Workflow

### 1. Identify Affected Systems

**MCP Tool**: `get_cve_systems` or `vulnerability__get_cve_systems` (from lightspeed-mcp)

**Parameters**:
- `cve_id`: Exact CVE identifier (format: `"CVE-YYYY-NNNNN"`)
  - Example: `"CVE-2024-1234"`
- `limit`: Optional number of systems to return (default: all)
  - Example: `100`
  - Use for large deployments to paginate results
- `offset`: Optional pagination offset (default: 0)
  - Example: `0`
  - Use with limit for pagination

**Expected Output**: List of system UUIDs and basic metadata

**Example Response**:
```json
{
  "systems": [
    {
      "id": "uuid-1",
      "hostname": "web-server-01",
      "display_name": "web-server-01.prod.example.com"
    },
    {
      "id": "uuid-2",
      "hostname": "web-server-02",
      "display_name": "web-server-02.prod.example.com"
    }
  ],
  "total": 2
}
```

### 2. Gather Detailed System Information

**MCP Tool**: `get_host_details` or `inventory__get_host_details` (from lightspeed-mcp)

**Parameters**:
- `system_id`: UUID of the system to retrieve (from get_cve_systems result)
  - Example: `"uuid-1"`
  - Format: UUID string
- `include_system_profile`: `true` (retrieve complete system profile including packages, services)
  - Example: `true`
  - Recommended: Always true for context gathering
- `include_tags`: Optional boolean to include system tags (default: true)
  - Example: `true`
  - Tags provide environment, role, criticality classification

**Expected Output**: Detailed system profile

**Key Information to Extract**:
- RHEL version (rhel_version, os_release)
- System type (infrastructure_type: bare_metal, virtualized, container)
- IP addresses (network_interfaces)
- Tags (environment, role, criticality)
- System profile (CPU, memory, disk)
- Installed packages (installed_packages)
- Running services (enabled_services, running_processes)
- Last check-in time (updated)

**System Profile Structure**:
```json
{
  "id": "uuid-1",
  "hostname": "web-server-01",
  "display_name": "web-server-01.prod.example.com",
  "rhel_version": "8.9",
  "os_release": "Red Hat Enterprise Linux 8.9 (Ootpa)",
  "system_profile": {
    "os_release": "8.9",
    "arch": "x86_64",
    "kernel_version": "4.18.0-513.el8.x86_64",
    "number_of_cpus": 4,
    "number_of_sockets": 1,
    "cores_per_socket": 4,
    "system_memory_bytes": 17179869184,
    "infrastructure_type": "virtualized",
    "infrastructure_vendor": "kvm",
    "network_interfaces": [
      {
        "name": "eth0",
        "ipv4_addresses": ["10.0.1.10"]
      }
    ],
    "installed_packages": [...],
    "enabled_services": ["httpd", "sshd", ...],
    "running_processes": [...]
  },
  "tags": [
    {"namespace": "environment", "key": "env", "value": "production"},
    {"namespace": "role", "key": "role", "value": "web-server"},
    {"namespace": "criticality", "key": "level", "value": "high"}
  ]
}
```

### 3. Analyze Deployment Context

Synthesize gathered information to understand deployment architecture:

**A. RHEL Version Distribution**:
```
Affected Systems by RHEL Version:
- RHEL 7: 3 systems (15%)
- RHEL 8: 15 systems (75%)
- RHEL 9: 2 systems (10%)

Remediation Consideration:
→ Playbook must support multiple RHEL versions (use conditional yum/dnf)
```

**B. Environment Classification**:
```
Affected Systems by Environment:
- Production: 12 systems (60%) - HIGH PRIORITY
- Staging: 5 systems (25%) - MEDIUM PRIORITY
- Development: 3 systems (15%) - LOW PRIORITY

Remediation Strategy:
→ Remediate staging first for validation
→ Schedule maintenance window for production
→ Development can be patched anytime
```

**C. System Type Distribution**:
```
Affected Systems by Type:
- Bare metal: 12 systems (60%) - STANDARD REMEDIATION
- VMs (VMware): 8 systems (40%) - STANDARD REMEDIATION

Deployment Type:
→ Standard remediation workflow
→ Consider reboot requirements
→ Schedule maintenance windows for critical systems
```

**D. System Criticality**:
```
Affected Systems by Criticality:
- Critical (payment, auth): 5 systems - NEEDS MAINTENANCE WINDOW
- High (web, api): 10 systems - NEEDS TESTING
- Medium (internal tools): 3 systems - STANDARD DEPLOYMENT
- Low (dev, test): 2 systems - IMMEDIATE DEPLOYMENT OK

Remediation Approach:
→ Test on low-criticality systems first
→ Schedule maintenance for critical systems
→ Use rolling updates for high-availability services
```

### 5. Determine Remediation Strategy

Based on gathered context, recommend remediation strategy:

**Decision Matrix**:

| Context | Remediation Strategy |
|---------|---------------------|
| Single system, non-K8s | Standard playbook, immediate execution possible |
| Multiple systems, same RHEL version | Batch playbook, parallel execution |
| Multiple systems, mixed RHEL versions | Batch playbook with version conditionals |
| Kubernetes nodes | Rolling update with pod eviction |
| Critical production systems | Maintenance window required, staged rollout |
| Mixed environments | Remediate staging → validate → production |

**Strategy Output**:
```yaml
remediation_strategy:
  approach: "rolling_update"  # or "batch", "individual", "staged"

  requires_maintenance_window: true
  suggested_window: "Weekend, off-peak hours"

  requires_pod_eviction: true
  pod_eviction_strategy: "one_node_at_a_time"

  batch_size: 5
  parallel_execution: true

  test_first_on:
    - "staging-web-01"
    - "staging-web-02"

  rollout_order:
    - phase: "validation"
      systems: ["staging-web-01", "staging-web-02"]
      wait_for_verification: true

    - phase: "production_batch_1"
      systems: ["prod-web-01", "prod-web-02", "prod-web-03"]
      requires_approval: true

    - phase: "production_batch_2"
      systems: ["prod-web-04", "prod-web-05"]
      requires_approval: false

  estimated_duration_minutes: 60
  estimated_downtime_per_system: 5
```

### 6. Return Context Summary

Return comprehensive context for remediation planning:

```json
{
  "cve_id": "CVE-YYYY-NNNNN",

  "affected_systems": {
    "total": 20,
    "by_rhel_version": {
      "rhel7": 3,
      "rhel8": 15,
      "rhel9": 2
    },
    "by_environment": {
      "production": 12,
      "staging": 5,
      "development": 3
    },
    "by_type": {
      "kubernetes": 8,
      "bare_metal": 7,
      "vm": 5
    },
    "by_criticality": {
      "critical": 5,
      "high": 10,
      "medium": 3,
      "low": 2
    }
  },

  "kubernetes_context": {
    "has_k8s_nodes": true,
    "total_k8s_nodes": 8,
    "clusters": ["prod-cluster-01", "staging-cluster-01"],
    "total_pods_affected": 150,
    "has_pdbs": true,
    "daemonsets_present": true
  },

  "remediation_strategy": {
    "approach": "rolling_update",
    "requires_maintenance_window": true,
    "requires_pod_eviction": true,
    "batch_size": 5,
    "estimated_duration_minutes": 60
  },

  "recommendations": [
    "Test in staging environment first (5 systems available)",
    "Schedule maintenance window for production (12 critical systems)",
    "Use rolling updates with pod eviction for Kubernetes nodes",
    "Playbook must support RHEL 7, 8, and 9",
    "Consider batch size of 5 systems for parallel execution"
  ]
}
```

## Output Template

When completing context gathering, provide output in this format:

```markdown
# System Context Analysis

## CVE: CVE-YYYY-NNNNN

## Affected Systems Summary
**Total Systems**: 20

### By RHEL Version
- RHEL 7: 3 systems (15%)
- RHEL 8: 15 systems (75%)
- RHEL 9: 2 systems (10%)

### By Environment
- Production: 12 systems (60%) - HIGH PRIORITY
- Staging: 5 systems (25%) - TEST FIRST
- Development: 3 systems (15%)

### By System Type
- Kubernetes nodes: 8 systems (40%) - REQUIRES POD EVICTION
- Bare metal: 7 systems (35%)
- VMs: 5 systems (25%)

### By Criticality
- Critical: 5 systems (payment, auth services)
- High: 10 systems (web, API services)
- Medium: 3 systems (internal tools)
- Low: 2 systems (dev/test)

## Kubernetes Deployment
**Kubernetes Nodes**: 8 systems
**Clusters**: prod-cluster-01 (5 nodes), staging-cluster-01 (3 nodes)
**Total Pods Affected**: ~150 pods
**PodDisruptionBudgets**: Present (payment service, auth service)
**DaemonSets**: node-exporter, fluent-bit

## Recommended Remediation Strategy

**Approach**: Rolling Update with Pod Eviction

**Execution Plan**:
1. **Phase 1 - Validation** (Staging):
   - Systems: staging-web-01, staging-web-02 (5 systems)
   - Test playbook execution
   - Verify no issues before production

2. **Phase 2 - Production Batch 1**:
   - Systems: prod-web-01 to prod-web-05 (5 systems)
   - Requires approval after staging validation
   - Rolling update with pod eviction

3. **Phase 3 - Production Batch 2**:
   - Systems: prod-web-06 to prod-web-10 (5 systems)
   - Continue if Batch 1 successful

**Requirements**:
- Maintenance window: Weekend off-peak hours
- Pod eviction strategy: One node at a time
- Batch size: 5 systems (parallel execution)
- Estimated duration: 60 minutes total
- Estimated downtime per system: ~5 minutes

**Safety Measures**:
- Test in staging first
- Rolling updates maintain service availability
- PodDisruptionBudgets respected
- Rollback capability via snapshots (RHEL 8/9)

## Next Steps
1. Review remediation strategy
2. Schedule maintenance window for production
3. Generate remediation playbook (use playbook-generator skill)
4. Execute in staging for validation
5. Proceed with production deployment
```

## Examples

### Example 1: Simple Environment

**User Request**: "Gather context for CVE-2024-1234"

**Skill Response**:
1. Call `get_cve_systems` → 5 systems affected
2. Call `get_host_details` for each → All RHEL 8, production web servers
3. Analyze context → All same version, same environment, bare metal
4. Return simple remediation strategy: "Batch remediation, 5 systems, standard playbook"

### Example 2: Complex Multi-Version Deployment

**User Request**: "Gather context for kernel CVE affecting production environment"

**Skill Response**:
1. Call `get_cve_systems` → 10 systems affected
2. Call `get_host_details` → Mixed RHEL 8/9, production environment
3. Analyze system types → Mix of bare metal and VMs, high criticality tags
4. Check reboot requirements → Kernel update requires maintenance window
5. Return complex strategy: "Rolling update by RHEL version, separate playbooks for RHEL 8 and 9, coordinate maintenance window for critical systems"

### Example 3: Multi-Environment Deployment

**User Request**: "Gather context for CVE affecting dev, staging, and prod"

**Skill Response**:
1. Call `get_cve_systems` → 20 systems across 3 environments
2. Call `get_host_details` → Extract environment tags
3. Classify by environment → 3 dev, 5 staging, 12 prod
4. Determine criticality → Production has critical services
5. Return staged strategy: "Test on dev (3 systems) → Validate on staging (5 systems) → Deploy to production with approval (12 systems)"

## Error Handling

**No systems affected**:
```
CVE-YYYY-NNNNN Analysis Complete

Good news! No systems in your infrastructure are currently affected by this CVE.

Possible reasons:
- Systems are already patched
- Vulnerable packages are not installed
- Systems are running different versions

No remediation required.
```

**Lightspeed inventory access error**:
```
Unable to retrieve system details from Red Hat Lightspeed inventory.

Possible causes:
- Systems not registered to Red Hat Lightspeed
- Lightspeed inventory sync pending
- API authentication issue

Suggestions:
- Verify systems are registered: subscription-manager status
- Check Lightspeed connection: insights-client --status
- Re-run inventory sync: insights-client --register
```

**System tagging incomplete**:
```
Unable to fully classify systems due to incomplete tagging.

Proceeding with Red Hat Lightspeed data only.
Note: Environment and criticality tags missing from some systems.

To improve system classification:
1. Add environment tags to systems in Red Hat Lightspeed
2. Add criticality/role tags for better prioritization
3. Ensure all systems are registered and reporting
```

## Dependencies

### Required MCP Servers
- `lightspeed-mcp` - Red Hat Lightspeed platform access

### Required MCP Tools
- `get_cve_systems` or `vulnerability__get_cve_systems` (from lightspeed-mcp) - List systems affected by CVE
  - Parameters: cve_id (string, format CVE-YYYY-NNNNN), limit (number, optional), offset (number, optional)
  - Returns: List of system UUIDs and basic metadata (hostname, display_name)
- `get_host_details` or `inventory__get_host_details` (from lightspeed-mcp) - Get detailed system information
  - Parameters: system_id (UUID string), include_system_profile (boolean), include_tags (boolean, optional)
  - Returns: Complete system profile including RHEL version, infrastructure type, tags, packages, services

### Related Skills
- `cve-impact` - Provides CVE severity to inform criticality assessment
- `playbook-generator` - Consumes context to generate appropriate remediation playbook
- `remediation-verifier` - Uses system context to verify remediation on correct systems
- `cve-validation` - Validates CVE before gathering affected systems

### Reference Documentation
- None required (system context is gathered from MCP tool queries)

## Best Practices

1. **Always gather full context** - Don't skip system details even if deployment seems simple
2. **Classify by environment** - Always test in staging before production deployment
3. **Check system criticality** - Remediation strategy depends on system importance (critical vs low)
4. **Respect criticality tags** - High-criticality systems need maintenance windows and extra care
5. **Detect RHEL version mix** - Playbooks must handle multiple versions (conditional dnf/yum logic)
6. **Consider batch size** - Balance speed vs risk (5-10 systems per batch recommended)
7. **Plan for rollback** - Always have a backup strategy (snapshots, maintenance windows)
8. **Use pagination for large fleets** - If get_cve_systems returns 100+ systems, use limit/offset parameters
