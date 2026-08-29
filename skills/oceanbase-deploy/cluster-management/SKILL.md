---
name: cluster-management
description: Deploy and operate community or commercial OceanBase clusters with obd, including distributed and commercial standalone or centralized forms, multi-node maximum-utilization sizing, lifecycle changes, upgrades, monitoring, OCP, network access, Config Server, Binlog/CDC services, OMS, oceanbase.ai, oblogservice, and shared-storage topologies. Use for OceanBase cluster control-plane work; route tenant, benchmark, diagnostic, controller-administration, and unrelated product workflows elsewhere.
metadata:
  author: oceanbase
  version: "3.0"
---

<!-- Compatibility anchors retained for published 2.x deep links. -->
<a id="oceanbase-cluster-management-obd"></a>
<a id="when-to-use-this-skill"></a>
<a id="ocp-terminology-convention"></a>
<a id="critical-safety-rules"></a>
<a id="installation"></a>
<a id="quick-start"></a>
<a id="cluster-lifecycle-commands"></a>
<a id="os-environment-requirements"></a>
<a id="os--environment-requirements"></a>
<a id="monitoring"></a>
<a id="mirror-repository-management"></a>
<a id="mirror--repository-management"></a>
<a id="ocp-ce-takeover"></a>
<a id="usage-examples"></a>
<a id="quick-demo"></a>
<a id="deploy-with-config-file"></a>
<a id="interactive-deploy"></a>
<a id="explicitly-requesting-ocp-express"></a>
<a id="destroying-a-cluster-requires-confirmation"></a>
<a id="related-skills"></a>

# OceanBase Cluster Management with obd

This skill supports both community and commercial OceanBase. Never select a component key, package, YAML field, or lifecycle command from the product label alone.

When OBD or the version-matched plugin is unavailable, you may still prepare a clearly labeled, non-executable decision blueprint containing placeholders and unresolved evidence. Do not claim schema validation, artifact compatibility, precheck success, or runtime support until those inputs exist.

## Default Controller, SSH, and Cluster Discovery

Across every cluster deployment path, default the OBD controller to one of the user-supplied cluster hosts, never the automation runner. Inspect all target hosts in supplied order before selecting it. Reuse the host that owns the intended OBD registration or another unambiguous existing target-host controller; when all targets are reachable and every target is confirmed to have no OBD executable, package record, or metadata, install OBD on the first target host without asking. An explicit user-selected controller overrides this default.

If both SSH user and password are omitted, first try passwordless `root` SSH with the existing key or agent and ask for access details only after that host-specific attempt fails. Do not ask whether the cluster is already deployed: inspect OBD registrations plus target-host processes, listeners, services, deployment paths, and reachable database identity. Read and apply the shared [default controller, SSH, and cluster discovery contract](../references/operation-contract.md#default-controller-ssh-and-cluster-discovery) before choosing a controller or classifying a target as clean, deployed, stopped, or unmanaged.

## Default New-Cluster Sizing

When a new OceanBase deployment request does not specify resource values, a cap, or a non-maximum profile, select [maximum-utilization sizing](references/maximum-utilization.md) by default and do not ask the user to choose a deployment size. Preserve explicit user sizing. Apply maximum sizing only to the resolved target hosts and requested database component; do not infer extra nodes, optional components, or tenants.

## Default New-Cluster Zone Placement

For a new distributed deployment with multiple user-supplied Observer hosts and no explicit zone mapping, assign each distinct host to a distinct new zone in deterministic host order. Do not ask the user to choose this default. Preserve explicit placement, do not infer extra hosts or replicas, and do not claim high availability when logical zones share one physical failure domain. This default does not apply to standalone or centralized product forms.

## Deployment Package Closure

Before the first package lookup, download, import, or image load for a deployment, component addition, upgrade, or reinstall, read the shared [deployment package closure](../references/deployment-package-sets.md). Expand the final requested component graph into every primary and companion artifact before acquisition. A database RPM without its applicable `*-libs`, an OCP package without its plugin-selected JRE, or an OMS archive loaded on only some nodes is not a complete local/offline package plan.

## Online Package Source Priority

Before any package network request, apply the shared [fixed mirror-source and acquisition-fallback workflow](../obd-administration/references/mirror-and-repositories.md#fixed-online-package-source-order). Try normal OBD/repository acquisition on the selected controller first. If that path fails, try the exact artifact there with `curl`, `wget`, the operating-system package manager, or another applicable downloader; verify it, import an OBD-consumed RPM with `obd mirror clone <path>` or use the artifact's proved local registration/install path, and continue through local resolution. If every controller-local method fails, use another reachable host only as a checksummed artifact relay from the same ordered sources; do not move OBD or deployment execution. Never use `obd mirror` as a network downloader.

## Default Database Bootstrap Password

For a new OceanBase deployment, do not ask for an initial database `root`/`sys` password unless the user explicitly supplied one. By default, omit the password field and let the installed OBD workflow generate the random value; never replace that path with an agent-generated or empty password. Follow the detailed [database bootstrap-password default](references/config-deployment.md#database-bootstrap-password-default).

## Shared Gates

Read these references at the indicated point:

- Before selecting a product form, command, plugin, artifact, or YAML key, read [product and capability resolution](../references/product-and-capability-resolution.md).
- Before any live controller/host/deployment query, SSH/SQL/API/network access, download, external action, or mutation, read the [operation contract](../references/operation-contract.md).
- Define acceptance before execution with the [completion criteria](../references/completion-criteria.md).
- After a failure, timeout, interruption, or mixed result, read [failure recovery and evidence](../references/failure-recovery-and-evidence.md) before retrying or cleaning.
- Before cleanup, removal, destroy, redeploy, prune, or deletion, read [cleanup and ownership boundaries](../references/cleanup-boundaries.md).

Treat `oceanbase-ce`, `oceanbase`, `oceanbase-standalone`, and `oceanbase.ai` as version-dependent candidate component keys. Confirm the installed plugin and repository entry. Do not turn a community configuration into a commercial configuration by renaming one key.

## Route by Operation

Read only the references needed for the request.

| Request | Reference |
|---|---|
| Determine or validate every package needed by a deployment topology before acquisition | [deployment-package-sets.md](../references/deployment-package-sets.md) |
| Default sizing for a new cluster with no user-specified resources, or an explicitly requested dedicated-host/capped maximum-utilization deployment | [maximum-utilization.md](references/maximum-utilization.md) |
| Any new community, commercial distributed, or commercial standalone/centralized config-file, interactive, or autodeploy request | [config-deployment.md](references/config-deployment.md), which performs common preflight and then selects exactly one product blueprint |
| `edit-config`, `reload`, parameter classification, or `chst` | [configuration-changes.md](references/configuration-changes.md) |
| Start, stop, restart, display, destroy, redeploy, prune, `demo`, or `perf` | [lifecycle.md](references/lifecycle.md) |
| Add or delete a component | [component-changes.md](references/component-changes.md) |
| Component or cluster upgrade | [upgrade.md](references/upgrade.md) |
| Change a deployed component artifact with `cluster reinstall` | [component-reinstall.md](references/component-reinstall.md) |
| Persistent host initialization with `cluster init4env` | [environment-initialization.md](references/environment-initialization.md) |
| Supported standalone management-IP change | [change-ip.md](references/change-ip.md) |
| Adopt an already running cluster into OBD | [cluster-takeover.md](references/cluster-takeover.md) |
| OBAgent, Prometheus, Grafana, or Alertmanager | [monitoring.md](references/monitoring.md) |
| OCP CE, commercial OCP, OCP Express, takeover, or OCP-aware redeploy | [ocp.md](references/ocp.md) |
| SQL/RPC/obshell access, OBProxy, `local_ip`, `devname`, VIP, or external load balancer boundaries | [network-access.md](references/network-access.md) |
| OceanBase Config Server | [config-server.md](references/config-server.md) |
| The commercial `oceanbase.ai` component | [oceanbase-ai.md](references/oceanbase-ai.md) |
| The commercial `oblogservice` component | [oblogservice.md](references/oblogservice.md) |
| Deploy an `obbinlog-ce`/`obbinlog` service or manage tenant Binlog instances with `obd binlog` | [binlog.md](references/binlog.md) |
| Deploy or operate the legacy `oblogproxy` CDC/log-proxy component | [oblogproxy.md](references/oblogproxy.md) |
| Deploy, operate, or upgrade OMS through an installed OBD OMS workflow | [oms.md](references/oms.md) |
| Commercial shared-storage deployment topology | [shared-storage.md](references/shared-storage.md) |
| Load or inspect a license for an OBD-managed commercial standalone/centralized deployment | [commercial standalone license gate](references/deployment-templates/commercial-standalone.md#license-management) |

## Essential Boundaries

- Prefer a uniquely named, reviewed configuration-file deployment. `obd demo` and `obd perf` are mutating convenience workflows with fixed `demo` and `perf` namespaces; inspect their installed behavior and existing state before use.
- Add optional components only when the user requested them or accepted their explained purpose and impact. Monitoring, OCP, Config Server, OBProxy, `oceanbase.ai`, and `oblogservice` are never implicit.
- Never use `redeploy` as a default repair, configuration apply, or component-add mechanism. It destroys and rebuilds deployment-owned state.
- Destroy, redeploy, prune, component deletion, and forced operations require authorization bound to the exact observed target and impact. An explicit request to execute an ordinary non-destructive cluster workflow already authorizes its necessary in-scope persistent changes and expected rolling restarts; do not ask again only because those effects persist.
- Adding or removing Observer servers from an already registered deployment is unsupported. Report `UNSUPPORTED` before mutation; do not simulate the topology change through SQL, obshell, `edit-config`, component operations, process control, metadata edits, or path deletion.
- A successful command, registered deployment, or running process is not sufficient. Verify the applicable control-plane, runtime, and data-plane outcomes.

## Out of Scope

Route tenant CRUD, backup/restore, and tenant replication to [tenant-management](../tenant-management/SKILL.md), and benchmarks or mysqltest to [testing-and-benchmark](../testing-and-benchmark/SKILL.md). Return ambiguous requests to the [oceanbase-deploy overview](../SKILL.md).

SeekDB is a separate product skill. Other product-specific workflows outside the routing table are also out of scope; do not translate them into a similarly named Config Server, `oblogproxy`, `oblogservice`, `obbinlog`, OMS, or `oceanbase.ai` operation.
