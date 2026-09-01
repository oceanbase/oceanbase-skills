---
name: obd-administration
description: Install, update, and administer the tested OBD controller workflows, including mirrors and repositories, offline artifacts, exact dynamic-tool provisioning for retained workflows, trace evidence, OBD_HOME discovery, and scoped automatic-confirm handling. Use for controller-scoped OBD work; use the specialized cluster, tenant, testing, or obdiag skill for those domains.
metadata:
  author: oceanbase
  version: "2.0.1"
---

# OBD Administration

## Highest-Priority Gate: OBD Requires root or sudo

Before applying any other live rule in this Skill, resolve and log in to every machine the workflow must access, then verify that the same login-session user is root with `id -u == 0` or can run `sudo -n true`. Only the minimum host/login identity and authentication checks may precede this gate. If any required machine fails it, do not install or invoke OBD and do not begin package lookup, download, repository work, controller discovery, or another OBD operation. Report `UNSUPPORTED — the current Skill version does not support using OBD with a login user that lacks root or usable non-interactive sudo privileges` and ask the user to switch the login user or configure usable sudo. Do not edit sudoers or use a user-local/all-in-one/source/manual-extraction workaround. After the gate passes, keep the login-session user as the OBD owner and use sudo only for privileged commands. Apply the shared [highest-priority OBD privilege gate](../references/operation-contract.md#highest-priority-obd-privilege-gate).

Operate the OBD control plane without silently changing a managed deployment. Controller installation, repository state, tool inventory, trace evidence, and tested OBD environment values have independent lifecycles and authorization boundaries.

Before the first package lookup or acquisition for controller installation, maintenance, offline preparation, or dynamic-tool provisioning, read the shared [deployment package closure](../references/deployment-package-sets.md). Before treating an unlisted controller operation as executable, read the shared [current Skill-version unsupported capabilities](../references/current-version-unsupported.md).

## Mandatory Package Acquisition Order

Before any package lookup or network request, select the effective artifact source before the acquisition mechanism and apply the [fixed package-source workflow](references/mirror-and-repositories.md#fixed-online-package-source-order). This applies to every OceanBase public package handled here, not only OBD. Source 1 is the actual package directories under `https://mirrors.oceanbase.com`; source 2 is the actual package directories under `https://mirrors.aliyun.com/oceanbase`. A `.repo` file is only package-manager configuration, so its download host is not the package source; prove its effective package URL before using or counting it. Keep operating-system dependency repositories separate from OceanBase package acquisition.

For OBD itself, Community and Commercial deployments use the same `ob-deploy` package from the public `community` tree. On a clean controller with no verified local OBD RPM, begin under `https://mirrors.oceanbase.com/community/`, default to direct controller-local `curl` or `wget`, and install the exact local RPM with the operating-system package manager. An OBD-dependent deployment request authorizes this proved first installation and package-manager non-interactive acceptance such as `-y`; do not ask separately before executing the install. This does not authorize replacement, upgrade, downgrade, or an unproved candidate. Do not add a persistent OceanBase `.repo` merely as the default OBD bootstrap path. `obd mirror` starts only after an artifact is already local; never use it as a network downloader.

`ob-deploy` is the direct controller package-manager installation exception. For other OBD-consumed component RPMs, default online mode lets the installed OBD/repository workflow resolve, fetch, and deploy the proved remote winner. If direct controller-local download obtains an exact component RPM, verify it, import it with `obd mirror clone <path>`, complete and isolate the local package closure, then let the owning OBD workflow distribute or install it. Do not package-manager-install Observer, proxy, monitoring, or other OBD component RPMs on the controller or every target unless the installed component workflow explicitly proves that consumer path. Read [installation.md](references/installation.md) before using an all-repositories-disabled local install for `ob-deploy`.

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

Before acting, identify the controller host, current user, exact executable, installation owner and method, `OBD_HOME`, registered deployments, active OBD tasks, repository state, and tool inventory. For a cluster deployment, inspect all supplied cluster hosts before selecting the controller: reuse the target host that owns the intended registration or another unambiguous existing target-host controller; only after every target is reachable and confirmed to have no OBD executable, package record, or metadata, install OBD on the first supplied target with non-interactive package-manager acceptance and without asking. Never default to the automation runner or an unrelated host. Re-resolve the controller identity after an SSH hop, user change, executable change, or environment change.

When the workflow manages remote hosts, use the remote host selected by the shared controller-discovery rule and keep OBD execution and metadata there. Use the user's supplied SSH login user on every deployment machine; if no login user is specified, use `root`, and if no authentication material is supplied, use passwordless SSH. Once logged in, retain that login-session user for all controller work and controller-to-node SSH. Do not infer or switch to another OBD execution user. When controller-to-node authentication alone fails, automatically append that login user's controller public key to the same login user's `authorized_keys` through already-verified access, without another prompt. Preserve existing keys and SSH policy, and request access only when no approved path can modify the exact target or its identity is ambiguous. Do not turn the automation runner or an artifact-relay host into the controller, ask the user whether the cluster is deployed instead of inspecting it, or switch controller identity after an acquisition failure. Follow the shared operation contract for target-host discovery, controller-local acquisition fallbacks, and the bounded artifact-relay boundary.

Do not:

- install or replace OBD on a target host unless that host is explicitly the controller;
- update OBD as an implicit workaround for a failed cluster operation;
- treat repository availability as package compatibility or selection;
- use automatic confirmation, force, environment clearing, repository cleaning, or hidden-metadata edits as generic automation or recovery;
- infer permission to operate a deployment from permission to administer its controller.

Report controller acceptance separately from the health of every registered deployment.
