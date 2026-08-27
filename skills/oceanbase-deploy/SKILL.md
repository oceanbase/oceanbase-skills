---
name: oceanbase-deploy
description: Route OceanBase deployment and operations through obd across community, commercial distributed, and commercial standalone or centralized product forms. Use for general or multi-domain OceanBase/obd requests, product-form discovery, or when the correct specialized skill is unclear. Route concrete work to cluster management, OBD administration, tenant management, testing, or diagnostics. Preserve the bundled SeekDB route for OBD-managed SeekDB lifecycle, HA, and monitoring work.
metadata:
  author: oceanbase
  version: "3.0"
---

<!-- Compatibility anchors retained for published 2.x deep links. -->
<a id="oceanbase-deploy-operations-obd"></a>
<a id="oceanbase-deploy--operations-obd"></a>
<a id="skill-index"></a>
<a id="quick-start"></a>
<a id="installation"></a>
<a id="ocp-terminology-convention"></a>
<a id="critical-safety-rules"></a>

# OceanBase Deployment and Operations with obd

Use this entry point to identify the product form, execution mode, and owning skill. Do not turn an explanation, configuration review, or diagnostic request into a deployment.

## Route the Request

| Skill | Use when |
|---|---|
| [cluster-management](cluster-management/SKILL.md) | Deploy or operate OceanBase clusters and OBD-managed components; manage configuration, upgrades, scaling, monitoring, OCP, Config Server, Binlog/CDC services, OMS, networking, or shared-storage deployments. |
| [obd-administration](obd-administration/SKILL.md) | Install or update the OBD controller; manage mirrors/repositories, stored credentials, dynamic tools, OBD Web/API, top-level host commands, trace evidence, runtime environment, or telemetry. |
| [tenant-management](tenant-management/SKILL.md) | Create, inspect, optimize, back up, restore, drop, or manage physical primary/standby tenants. |
| [testing-and-benchmark](testing-and-benchmark/SKILL.md) | Run Sysbench, TPC-H, TPC-C, or mysqltest through `obd test`. |
| [obdiag-diagnostics](obdiag-diagnostics/SKILL.md) | Install-gated diagnostic collection, analysis, checks, scenes, or RCA through `obd obdiag`. |
| [obd-seekdb](seekdb/SKILL.md) | Install/deploy, lifecycle, takeover, HA, or OBD-managed monitoring for a SeekDB deployment. |

SeekDB is a separate product family. Route an action to the bundled skill above only when the requested mechanism is `obd seekdb`, the action is OBD controller lifecycle/HA management of a registered SeekDB deployment, or OBD is managing that deployment's monitoring components. Route product installation that does not use OBD, builds, documentation, CLI/SQL, import, and query/export work to the top-level `seekdb` skill when installed—even when OBD originally deployed the target instance. Keep those routes distinct; do not translate `obd seekdb` into OceanBase cluster or tenant commands.

## Resolve Product and Capability First

Before proposing an executable command or configuration, read [product and capability resolution](references/product-and-capability-resolution.md). Support community and commercial deployments through the same operating model, but resolve the actual product form, component keys, plugins, repositories, and artifact set before selecting a template.

Do not:

- default to a community component or public mirror when the request or artifacts indicate a commercial deployment;
- treat a source-tree feature as proof that the installed OBD package exposes it;
- substitute OCP CE, enterprise OCP, OCP Express, or obshell Dashboard for one another;
- infer compatibility only because every requested package exists in a repository.

## Preserve the User's Execution Mode

- **Explain, plan, review, or audit:** stay read-only. Inspect only the supplied files and already available local evidence unless the user expands the scope.
- **Diagnose:** begin with the smallest relevant read-only evidence set. High-overhead collection or tool installation is a separate action.
- **Implement:** display the resolved targets, mutations, impact, and acceptance plan before execution. Obtain authorization at the point required by the risk class.

Read the shared [operation contract](references/operation-contract.md) before any live controller/host/deployment query, SSH/SQL/API/network access, download, write, or other externally visible action. A child skill can be selected directly, so every child in the routing table must also link this contract and retain its essential safety boundary.

## Define Completion and Failure Handling

Command exit, task acceptance, process state, control-plane state, and data-plane usability are different results.

- Read [completion criteria](references/completion-criteria.md) before declaring an operation complete.
- On failure, timeout, interruption, or a mixed state, read [failure recovery and evidence](references/failure-recovery-and-evidence.md) before retrying or cleaning anything.
- Before any cleanup, removal, reset, prune, drop, uninstall, or deletion, read [cleanup and ownership boundaries](references/cleanup-boundaries.md) and enumerate the exact removed and retained objects.

Never use `redeploy`, `destroy`, `--force`, metadata deletion, repository cleanup, tenant drop, or another broad mutation as a generic repair.

## Quick Start Boundary

Do not expose an unconditional `obd demo` or `obd perf` command as the default quick start. For a quick local deployment, route to the cluster skill and use its reviewed configuration workflow. If the user explicitly selects either shortcut, inspect its fixed deployment name, generated components, paths, ports, existing processes, implicit force/cleanup behavior, and recovery boundary first.

## Sensitive Values

Do not place passwords, passkeys, access keys, tokens, private keys, or credential-bearing URIs in reusable examples, chat output, process arguments when a protected input exists, or reports. Redact secrets without discarding the non-sensitive evidence needed to reproduce a failure.
