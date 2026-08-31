---
name: obd-administration
description: Install, update, and administer the tested OBD controller workflows, including mirrors and repositories, offline artifacts, exact dynamic-tool provisioning for retained workflows, trace evidence, OBD_HOME discovery, and scoped automatic-confirm handling. Use for controller-scoped OBD work; use the specialized cluster, tenant, testing, or obdiag skill for those domains.
metadata:
  author: oceanbase
  version: "3.0"
---

# OBD Administration

Operate the OBD control plane without silently changing a managed deployment. Controller installation, repository state, tool inventory, trace evidence, and tested OBD environment values have independent lifecycles and authorization boundaries.

Before the first package lookup or acquisition for controller installation, maintenance, offline preparation, or dynamic-tool provisioning, read the shared [deployment package closure](../references/deployment-package-sets.md). Before treating an unlisted controller operation as executable, read the shared [current Skill-version unsupported capabilities](../references/current-version-unsupported.md).

## Online Package Source Priority

Before any package network request, apply the [fixed mirror-source and acquisition-fallback workflow](references/mirror-and-repositories.md#fixed-online-package-source-order). Try the installed OBD/repository path on the selected controller first. If it fails, use controller-local `curl`, `wget`, the operating-system package manager, or another applicable downloader for the exact artifact; verify it, import an OBD-consumed RPM with `obd mirror clone <path>` or use the artifact's proved local registration/install path, and retry through local resolution. If no controller-local method works, use another reachable host only as a checksummed artifact relay from the same ordered sources while keeping OBD and its metadata on the selected controller. Never use `obd mirror` as a network downloader.

## Required Shared Gates

Read the shared references that apply to every task:

- [Product and capability resolution](../references/product-and-capability-resolution.md) before selecting a command, package, plugin, or repository.
- [Operation contract](../references/operation-contract.md) before any live controller/host/deployment query, SSH/SQL/network access, download, installation, persistent setting, external action, or other mutation.
- [Completion criteria](../references/completion-criteria.md) before declaring the controller or requested capability ready.
- [Failure recovery and evidence](../references/failure-recovery-and-evidence.md) after a failure, timeout, interruption, or mixed state and before retrying or cleaning.
- [Cleanup and ownership boundaries](../references/cleanup-boundaries.md) before any cleanup, removal, reset, prune, or deletion.

## Route the Task

Read only the references relevant to the request:

| Request | Reference |
|---|---|
| Install OBD on a controller | [installation.md](references/installation.md) |
| Update, replace, pin, downgrade, or roll back OBD | [controller-maintenance.md](references/controller-maintenance.md) |
| Inspect or manage mirrors, repositories, package candidates, or remote repository registration | [mirror-and-repositories.md](references/mirror-and-repositories.md) |
| Prepare or validate an air-gapped component repository | [offline-repository.md](references/offline-repository.md) |
| Inventory or install the exact dynamic tool required by a retained workflow | [tool-lifecycle.md](references/tool-lifecycle.md) |
| Retrieve or interpret an OBD trace ID with `obd display-trace` | [trace-evidence.md](references/trace-evidence.md) |
| Resolve `OBD_HOME` or temporarily handle automatic confirmation | [runtime-environment.md](references/runtime-environment.md) |

For `obd obdiag`, diagnostic collection, checks, analysis, scenes, or RCA, use [obdiag-diagnostics](../obdiag-diagnostics/SKILL.md). Do not invoke a dynamic alias merely to find out whether its tool is installed.

## Controller Boundary

Before acting, identify the controller host, current user, exact executable, installation owner and method, `OBD_HOME`, registered deployments, active OBD tasks, repository state, and tool inventory. For a cluster deployment, inspect all supplied cluster hosts before selecting the controller: reuse the target host that owns the intended registration or another unambiguous existing target-host controller; only after every target is reachable and confirmed to have no OBD executable, package record, or metadata, install OBD on the first supplied target without asking. Never default to the automation runner or an unrelated host. Re-resolve the controller identity after an SSH hop, user change, executable change, or environment change.

When the workflow manages remote hosts, use the remote host selected by the shared controller-discovery rule and keep OBD execution and metadata there. If the user omitted both SSH user and password, try passwordless `root` access before asking for credentials. Do not turn the automation runner or an artifact-relay host into the controller, ask the user whether the cluster is deployed instead of inspecting it, or switch controller identity after an acquisition failure. Follow the shared operation contract for target-host discovery, controller-local acquisition fallbacks, and the bounded artifact-relay boundary.

Do not:

- install or replace OBD on a target host unless that host is explicitly the controller;
- update OBD as an implicit workaround for a failed cluster operation;
- treat repository availability as package compatibility or selection;
- use automatic confirmation, force, environment clearing, repository cleaning, or hidden-metadata edits as generic automation or recovery;
- infer permission to operate a deployment from permission to administer its controller.

Report controller acceptance separately from the health of every registered deployment.
