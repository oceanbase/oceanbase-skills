---
name: cluster-management
description: Deploy and operate tested OceanBase Community Edition clusters with obd, including multi-node maximum-utilization sizing, lifecycle changes, configuration, upgrades, component changes, monitoring, network access, and Config Server. Use for OceanBase cluster control-plane work; route tenant, benchmark, diagnostic, and controller-administration workflows elsewhere.
metadata:
  author: oceanbase
  version: "2.0.1"
---

<!-- Compatibility anchors retained for published 2.x deep links. -->
<a id="oceanbase-cluster-management-obd"></a>
<a id="when-to-use-this-skill"></a>
<a id="critical-safety-rules"></a>
<a id="installation"></a>
<a id="cluster-lifecycle-commands"></a>
<a id="os-environment-requirements"></a>
<a id="os--environment-requirements"></a>
<a id="monitoring"></a>
<a id="mirror-repository-management"></a>
<a id="mirror--repository-management"></a>
<a id="usage-examples"></a>
<a id="deploy-with-config-file"></a>
<a id="destroying-a-cluster-requires-confirmation"></a>
<a id="related-skills"></a>

# OceanBase Cluster Management with obd

This skill covers the tested OceanBase Community Edition workflows. Confirm the installed component key, package, YAML field, and lifecycle command before execution.

When OBD or the version-matched plugin is unavailable, you may still prepare a clearly labeled, non-executable decision blueprint containing placeholders and unresolved evidence. Do not claim schema validation, artifact compatibility, precheck success, or runtime support until those inputs exist.

## Mandatory Package Acquisition Order

Before any package lookup or network request, select the effective artifact source before the download mechanism and apply the shared [fixed package-source workflow](../obd-administration/references/mirror-and-repositories.md#fixed-online-package-source-order) to every package in the complete deployment closure. Source 1 is the actual package directories under `https://mirrors.oceanbase.com`; source 2 is the actual package directories under `https://mirrors.aliyun.com/oceanbase`. A `.repo` file is only configuration: its download host does not identify the package source, so prove the effective package URL before using or counting it. Keep operating-system dependency repositories separate from OceanBase package acquisition.

When this workflow must bootstrap OBD, use the shared `ob-deploy` package for both Community and Commercial deployments and begin under `https://mirrors.oceanbase.com/community/`. With no verified controller-local RPM, default to direct controller-local `curl` or `wget` followed by installation of the exact local RPM. The deployment request authorizes the proved first installation and package-manager non-interactive acceptance such as `-y`; do not ask separately before running it. This does not authorize replacement, upgrade, downgrade, or an unproved candidate. Do not add an OceanBase `.repo` merely as the default bootstrap path. Never use `obd mirror` as a network downloader.

For other OBD-managed component RPMs, default online mode lets the installed OBD/repository workflow fetch the proved winners. A successful direct download changes the complete closure to local-package mode: verify and `obd mirror clone` the controller-local RPMs, isolate remote resolution, and let the owning OBD cluster workflow distribute or install them. Do not package-manager-install Observer or companion components independently on every target unless the installed component workflow explicitly requires it.

## New-Deployment Host Initialization

Before a configuration-file deployment or integrated maximum-utilization `autodeploy`, complete the public OBD [host-environment initialization](references/config-deployment.md#host-environment-initialization) for every target as the actual deployment user and verify persistent limits in a fresh login session. Do not use `autodeploy` as the first host-environment probe and then repair the state it leaves behind.

For Observer storage, reserve `<home_path>/store` as OBD's canonical data entry. Never place `data_dir` or `redo_dir` below that path. `data_dir` may equal the canonical entry when the installed plugin uses it as the direct data root; `redo_dir` may equal it only as the same plugin-supported single-root topology. When automatically deriving explicit custom values, use disjoint home, data, and redo siblings and keep a supported separately selected redo filesystem separate. Observer starting with `-d <home_path>/store` is not evidence that the installed plugin ignores `data_dir` or no longer supports `redo_dir`; OBD can realize the configured topology through canonical links. Apply the detailed [Observer storage-path invariant](references/config-deployment.md#observer-storage-path-invariant) before rendering YAML.

Once deployment initialization has created the storage topology, preserve the registered `home_path`, `data_dir`, and `redo_dir`; a failed start is not permission to remove those values or manually create Observer-internal `store`, `clog`, `slog`, or `sstable` paths. Follow the linked storage and recovery rules instead.

Before treating an unlisted cluster, product, or component operation as executable, read the shared [current Skill-version unsupported capabilities](../references/current-version-unsupported.md). Do not use a generic component, upgrade, reinstall, configuration, or lifecycle command to recreate a workflow that the current Skill version does not support.

## Default Controller, SSH, and Cluster Discovery

Across every cluster deployment path, default the OBD controller to one of the user-supplied cluster hosts, never the automation runner. Inspect all target hosts in supplied order before selecting it. Reuse the host that owns the intended OBD registration or another unambiguous existing target-host controller; when all targets are reachable and every target is confirmed to have no OBD executable, package record, or metadata, install OBD on the first target host with package-manager non-interactive acceptance and without asking. An explicit user-selected controller overrides this default.

Use the user's supplied SSH login user on every deployment machine; if no login user is specified, use `root`, and if no authentication material is supplied, use passwordless SSH. After login, use that login-session user for all host work, OBD installation and execution, controller files, and controller-to-node SSH. Do not infer or switch to another OBD user. If controller-to-node passwordless authentication fails, automatically append the controller login user's public key to the same login user's `authorized_keys` through already-verified access and retest without asking for separate permission. Preserve existing keys and SSH policy, and ask only when no approved access path can make that bounded change or host identity is ambiguous. Do not ask whether the cluster is already deployed: inspect OBD registrations plus target-host processes, listeners, services, deployment paths, and reachable database identity. Read and apply the shared [default controller, SSH, and cluster discovery contract](../references/operation-contract.md#default-controller-ssh-and-cluster-discovery) before choosing a controller or classifying a target as clean, deployed, stopped, or unmanaged.

## Default New-Deployment Directory

When a new deployment has no user-specified paths, select each target's [default deployment base directory](references/config-deployment.md#default-deployment-base-directory) under the established login-session user before sizing or rendering YAML. Choose the writable persistent filesystem with the greatest usable free capacity and create new deployment-specific paths there as the installed schema permits. For Observer, derive disjoint home/data/redo siblings rather than nesting custom storage below the reserved `<home_path>/store`; a separately selected eligible redo filesystem remains separate. Do not prefer the login user's home over a larger writable filesystem, assume `/data/1`, change ownership of an existing directory merely to make it eligible, or relocate registered paths.

## Default New-Cluster Sizing

When a new OceanBase deployment request does not specify resource values, a cap, or a non-maximum profile, select [maximum-utilization sizing](references/maximum-utilization.md) by default and do not ask the user to choose a deployment size. Preserve explicit user sizing. Apply maximum sizing only to the resolved target hosts and requested database component; do not infer extra nodes, optional components, or tenants.

## Default New-Cluster Zone Placement

For a new distributed deployment with multiple user-supplied Observer hosts and no explicit zone mapping, assign each distinct host to a distinct new zone in deterministic host order. Do not ask the user to choose this default. Preserve explicit placement, do not infer extra hosts or replicas, and do not claim high availability when logical zones share one physical failure domain.

## Deployment Package Closure

Before the first package lookup, download, or import for a deployment, component addition, upgrade, or reinstall, read the shared [deployment package closure](../references/deployment-package-sets.md). Expand the final requested component graph into every primary and companion artifact before acquisition. A database RPM without its applicable `*-libs`, or a test client without its required client library, is not a complete local/offline package plan.

## Default Database Bootstrap Password

For a new OceanBase deployment, do not ask for an initial database `root`/`sys` password unless the user explicitly supplied one. By default, omit the password field and let the installed OBD workflow generate the random value; never replace that path with an agent-generated or empty password. Follow the detailed [database bootstrap-password default](references/config-deployment.md#database-bootstrap-password-default).

## Shared Gates

Read these references at the indicated point:

- Before selecting a product form, command, plugin, artifact, or YAML key, read [product and capability resolution](../references/product-and-capability-resolution.md).
- Before any live controller/host/deployment query, SSH/SQL/API/network access, download, external action, or mutation, read the [operation contract](../references/operation-contract.md).
- Define acceptance before execution with the [completion criteria](../references/completion-criteria.md).
- After a failure, timeout, interruption, or mixed result, read [failure recovery and evidence](../references/failure-recovery-and-evidence.md) before retrying or cleaning.
- Before cleanup, removal, destroy, prune, or deletion, read [cleanup and ownership boundaries](../references/cleanup-boundaries.md).

Treat `oceanbase-ce` as a version-dependent candidate component key. Confirm the installed plugin and repository entry rather than relying on a remembered example.

## Route by Operation

Read only the references needed for the request.

| Request | Reference |
|---|---|
| Determine or validate every package needed by a deployment topology before acquisition | [deployment-package-sets.md](../references/deployment-package-sets.md) |
| Default sizing for a new cluster with no user-specified resources, or an explicitly requested dedicated-host/capped maximum-utilization deployment | [maximum-utilization.md](references/maximum-utilization.md) |
| A new Community Edition configuration-file deployment | [config-deployment.md](references/config-deployment.md) |
| `edit-config`, `reload`, parameter classification, or `chst` | [configuration-changes.md](references/configuration-changes.md) |
| Start, stop, restart, display, destroy, or prune | [lifecycle.md](references/lifecycle.md) |
| Add or delete retained `obproxy-ce`, `obagent`, `prometheus`, `grafana`, or `ob-configserver` components | [component-changes.md](references/component-changes.md) plus the owning OBProxy, monitoring, or Config Server reference |
| OceanBase Community Edition cluster rolling upgrade | [upgrade.md](references/upgrade.md) |
| Change a deployed `obproxy-ce` artifact with `cluster reinstall` | [component-reinstall.md](references/component-reinstall.md) |
| OBAgent, Prometheus, or Grafana | [monitoring.md](references/monitoring.md) |
| SQL/RPC/obshell access or OBProxy | [network-access.md](references/network-access.md) |
| OceanBase Config Server | [config-server.md](references/config-server.md) |

## Essential Boundaries

- Prefer a uniquely named, reviewed configuration-file deployment.
- Add optional components only when the user requested them or accepted their explained purpose and impact. Monitoring, Config Server, and OBProxy are never implicit.
- Destroy, prune, component deletion, and forced operations require authorization bound to the exact observed target and impact. An explicit request to execute an ordinary non-destructive cluster workflow already authorizes its necessary in-scope persistent changes and expected rolling restarts; do not ask again only because those effects persist.
- Adding or removing Observer servers from an already registered deployment is not supported by the current Skill version. Report `UNSUPPORTED — current Skill version` before mutation; do not simulate the topology change through SQL, obshell, `edit-config`, component operations, process control, metadata edits, or path deletion.
- A successful command, registered deployment, or running process is not sufficient. Verify the applicable control-plane, runtime, and data-plane outcomes.

## Out of Scope

Route tenant CRUD, backup/restore, and tenant replication to [tenant-management](../tenant-management/SKILL.md), and benchmarks or mysqltest to [testing-and-benchmark](../testing-and-benchmark/SKILL.md). Return ambiguous requests to the [oceanbase-deploy overview](../SKILL.md).
