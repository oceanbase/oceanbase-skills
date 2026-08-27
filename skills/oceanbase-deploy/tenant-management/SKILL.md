---
name: tenant-management
description: Manage OceanBase tenant lifecycle, workload optimization, backup and restore, and physical primary/standby relationships through obd. Use for tenant creation, deletion, inspection, optimization, backup, restore, switchover, failover, or related disaster-recovery requests. Do not use for SeekDB HA or cluster deployment lifecycle.
metadata:
  author: oceanbase
  version: "3.0"
---

<!-- Compatibility anchors retained for published 2.x deep links. -->
<a id="oceanbase-tenant-management-obd"></a>
<a id="when-to-use-this-skill"></a>
<a id="tenant-commands"></a>
<a id="create-tenant"></a>
<a id="drop-tenant"></a>
<a id="show-tenants"></a>
<a id="optimize-tenant"></a>
<a id="backup-restore"></a>
<a id="backup--restore"></a>
<a id="set-backup-config"></a>
<a id="run-backup"></a>
<a id="restore-from-backup"></a>
<a id="usage-examples"></a>
<a id="create-a-tenant"></a>
<a id="configure-and-run-backup"></a>
<a id="related-skills"></a>

# OceanBase Tenant Management

Resolve the installed OBD build, product form, deployment, and tenant before selecting a command. This skill supports community and commercial OceanBase forms when the installed command and component plugins prove the requested operation is available.

## Shared Gates

Read the shared references required by the current stage:

- Before selecting syntax, product form, or packages, read [product and capability resolution](../references/product-and-capability-resolution.md).
- Before any live controller/host/deployment query, SSH/SQL/API/network access, external action, or mutation, read the [operation contract](../references/operation-contract.md).
- Before declaring success, read the [completion criteria](../references/completion-criteria.md).
- After a failure, timeout, interruption, or mixed result, read [failure recovery and evidence](../references/failure-recovery-and-evidence.md) before retrying or cleaning anything.
- Before dropping or removing a tenant, database resource object, backup/archive object, or generated artifact, read [cleanup and ownership boundaries](../references/cleanup-boundaries.md).

## Route by Intent

| Request | Required reference |
|---|---|
| Create or inspect a tenant; plan resources, topology, credentials, or network allowlists | [tenant-creation.md](references/tenant-creation.md) |
| Drop a tenant | [tenant-deletion.md](references/tenant-deletion.md) |
| Optimize an existing tenant for a workload | [workload-optimization.md](references/workload-optimization.md) |
| Configure archive/backup storage, run, inspect, or cancel a backup, or restore, inspect, or cancel a tenant restore | [backup-restore.md](references/backup-restore.md) |
| Create or operate a physical primary/standby tenant, including switchover, failover, decouple, recovery target, log source, or protection mode | [physical-standby.md](references/physical-standby.md) |

## Hard Boundaries

- Treat tenant drop, tenant restore, backup-task cancellation, restore-task cancellation, failover, and decouple as separate high-impact operations. Authorization for inspection, ordinary tenant creation, backup, restore, or switchover does not authorize cancellation. The V4.6.0/current reviewed restore path creates a new target tenant and refuses an existing target; do not invent overwrite semantics or turn restore authorization into permission to drop an existing tenant.
- Do not place tenant, `standbyro`, storage, decryption, KMS, or other credentials in reusable commands or reports.
- A tenant row or successful OBD exit is not completion. Apply the domain checks in the selected reference and verify an authenticated data-plane outcome when applicable.
- Do not translate physical standby requests into SeekDB HA commands or infer a tenant relationship from deployment names alone.

For cluster deployment, component lifecycle, or upgrades, use [cluster-management](../cluster-management/SKILL.md). For benchmarks and functional tests, use [testing-and-benchmark](../testing-and-benchmark/SKILL.md).
