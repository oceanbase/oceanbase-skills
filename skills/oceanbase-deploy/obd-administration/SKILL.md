---
name: obd-administration
description: Install, update, and administer the OBD controller, including mirrors and repositories, offline artifacts, stored-credential encryption, dynamic tools, top-level host utilities, trace evidence, OBD Web/API, runtime environment, developer mode, and telemetry. Use for controller-scoped OBD work; use the specialized cluster, tenant, testing, or obdiag skill for those domains.
metadata:
  author: oceanbase
  version: "3.0"
---

# OBD Administration

Operate the OBD control plane without silently changing a managed deployment. Controller installation, repository state, tool inventory, stored credentials, Web listeners, host initialization, and OBD environment values have independent lifecycles and authorization boundaries.

## Required Shared Gates

Read the shared references that apply to every task:

- [Product and capability resolution](../references/product-and-capability-resolution.md) before selecting a command, package, plugin, or repository.
- [Operation contract](../references/operation-contract.md) before any live controller/host/deployment query, SSH/SQL/API/network access, download, installation, listener, persistent setting, credential change, external action, or other mutation.
- [Completion criteria](../references/completion-criteria.md) before declaring the controller or requested capability ready.
- [Failure recovery and evidence](../references/failure-recovery-and-evidence.md) after a failure, timeout, interruption, or mixed state and before retrying or cleaning.
- [Cleanup and ownership boundaries](../references/cleanup-boundaries.md) before any cleanup, removal, reset, prune, uninstall, or deletion.

## Route the Task

Read only the references relevant to the request:

| Request | Reference |
|---|---|
| Install OBD on a controller | [installation.md](references/installation.md) |
| Update, replace, pin, downgrade, or roll back OBD | [controller-maintenance.md](references/controller-maintenance.md) |
| Uninstall OBD or an owning OceanBase All-in-One installation | [controller-uninstall.md](references/controller-uninstall.md) |
| Inspect or manage mirrors, repositories, package candidates, or remote repository registration | [mirror-and-repositories.md](references/mirror-and-repositories.md) |
| Prepare or validate an air-gapped component repository | [offline-repository.md](references/offline-repository.md) |
| Enable/disable OBD credential encryption or manage its encryption passkey | [credential-storage.md](references/credential-storage.md) |
| List, install, update, or uninstall a dynamic OBD tool | [tool-lifecycle.md](references/tool-lifecycle.md) |
| Use `obd tool command`, `obd tool db_connect`, `obd tool dooba`, or another deployment-bound helper | [deployment-tools.md](references/deployment-tools.md) |
| Use top-level `obd host` precheck, initialization, or user operations | [host-tools.md](references/host-tools.md) |
| Retrieve or interpret an OBD trace ID with `obd display-trace` | [trace-evidence.md](references/trace-evidence.md) |
| Start OBD Web or invoke its version-specific API | [web-api.md](references/web-api.md) |
| Change `obd env`, developer mode, lock behavior, automatic confirmation, transfer behavior, or telemetry | [runtime-environment.md](references/runtime-environment.md) |

For `obd obdiag`, diagnostic collection, checks, analysis, scenes, or RCA, use [obdiag-diagnostics](../obdiag-diagnostics/SKILL.md). Do not invoke a dynamic alias merely to find out whether its tool is installed.

## Controller Boundary

Before acting, identify the controller host, current user, exact executable, installation owner and method, `OBD_HOME`, registered deployments, active CLI/Web/API tasks, repository state, and tool inventory. Re-resolve them after an SSH hop, user change, executable change, or environment change.

Do not:

- install or replace OBD on a target host unless that host is explicitly the controller;
- update OBD as an implicit workaround for a failed cluster operation;
- treat repository availability as package compatibility or selection;
- use automatic confirmation, force, environment clearing, repository cleaning, or hidden-metadata edits as generic automation or recovery;
- infer permission to operate a deployment from permission to administer its controller.

Report controller acceptance separately from the health of every registered deployment.
