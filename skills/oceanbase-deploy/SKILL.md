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

## Default Controller, SSH, and Existing-State Discovery

For every OBD-based cluster deployment mode, including configuration-file, interactive, autodeploy, demo, and perf paths, keep the controller on a cluster deployment host unless the user explicitly selected a separate controller. Probe the user-supplied target hosts in their original order before choosing or installing OBD. Reuse the target host that owns the intended registered deployment, or an otherwise unambiguous existing target-host controller. Only after every target host is reachable and confirmed to have no OBD executable, package ownership, or controller metadata, install OBD on the first target host without asking the user to choose. Never default to installing or running OBD on the automation runner.

When the user supplied neither an SSH user nor an SSH password, first try non-interactive passwordless SSH as `root` using the existing key or agent. Do not ask for credentials before that attempt. If it fails, preserve the host-specific error and then ask the user for the required access information; do not guess another account, password, key, or tunnel.

Do not ask the user whether a cluster is already deployed. Determine that through read-only inspection of candidate-controller registrations and, on every target host, relevant package/service state, processes, listeners, deployment paths, and database identity when reachable. A missing registration or stopped process alone does not prove absence. Ask only when access failed or the completed inspection leaves a genuine identity or ownership ambiguity. Follow the detailed [controller, SSH, and cluster discovery contract](references/operation-contract.md#default-controller-ssh-and-cluster-discovery).

## Default New-Cluster Sizing

For a new OceanBase cluster deployment, when the user does not specify resource values, a resource cap, or a non-maximum sizing profile, default to the [maximum-utilization workflow](cluster-management/references/maximum-utilization.md) without asking the user to choose a size. Explicit user values or caps take precedence. This default maximizes only the resolved target hosts; it does not add hosts, components, tenants, or topology that the user did not request.

For a new distributed deployment with multiple user-supplied Observer hosts and no explicit zone mapping, assign each distinct host to a distinct new zone in deterministic host order. Do not ask the user to choose the default placement. Preserve an explicit zone mapping, do not infer extra hosts or replicas, and do not claim that logical zones sharing one physical failure domain provide high availability.

## Deployment Package Closure

Before the first package lookup or acquisition for any deployment, component addition, upgrade, or reinstall, read the shared [deployment package closure](references/deployment-package-sets.md). Build the complete package set from the final requested component graph, including selected `*-libs`, JRE, client-library, image, and conditional utility dependencies; do not stop after downloading the obvious primary component RPM. In online mode prove every closure entry is resolvable; in local-package/offline mode place and verify the complete closure on the selected remote controller, plus every required node-local image, before package selection.

## Online Package Source Priority

For every package acquired online from OceanBase public repositories, first let the selected controller-side OBD or repository workflow try the exact artifact in this fixed mirror-source order: `https://mirrors.oceanbase.com`, then the direct package directories under `https://mirrors.aliyun.com/oceanbase`. Do not put a generic Internet-connectivity test ahead of the first source attempt. Across the required attempts on one source, do not repeat only the same failed fetch path: after the normal OBD/repository acquisition fails, try the exact file on the same controller with `curl`, `wget`, the operating-system package manager, or another applicable downloader. Verify the artifact, import an OBD-consumed local RPM with `obd mirror clone <path>` or use the artifact's version-proved local registration/install path, and retry through local resolution. If no controller-local method can acquire it, use another reachable host only as a checksummed artifact relay from the same ordered sources; keep OBD and execution on the selected controller. Ask only after the approved sources, compatible suffixes, controller-local methods, and relay have failed, or before introducing an unlisted source or a different controller. Never use `obd mirror` as a network downloader. Read the detailed [fixed package-source workflow](obd-administration/references/mirror-and-repositories.md#fixed-online-package-source-order) before the first package network request.

## Default Database Bootstrap Password

For a new OceanBase cluster deployment, do not ask the user to choose the initial database `root`/`sys` password unless the user has already specified one. When no override was supplied, leave the bootstrap-password field absent and use the installed OBD workflow's proved random-password generation path; do not generate the value in the agent or substitute an empty value. Keep the generated value protected and verify authentication without printing it. Read the cluster workflow's [database bootstrap-password default](cluster-management/references/config-deployment.md#database-bootstrap-password-default) before rendering deployment YAML.

## Route the Request

| Skill | Use when |
|---|---|
| [cluster-management](cluster-management/SKILL.md) | Deploy or operate OceanBase clusters and OBD-managed components; manage configuration, upgrades, component changes, monitoring, OCP, Config Server, Binlog/CDC services, OMS, networking, or shared-storage deployments. |
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
