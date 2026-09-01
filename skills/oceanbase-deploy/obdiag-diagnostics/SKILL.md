---
name: obdiag-diagnostics
description: Collect and analyze OceanBase diagnostic evidence through `obd obdiag`, including bounded gathers, checks, analysis, scenes, ASH, and RCA when supported by the installed tool. Use for incident diagnosis and obdiag requests; do not use for ordinary lifecycle status checks.
metadata:
  author: oceanbase
  version: "2.0.1"
---

# Diagnostics with obd obdiag

## Highest-Priority Gate: OBD Requires root or sudo

Before any live discovery or operation in this Skill, resolve and log in to every machine the workflow must access, then verify that the same login-session user is root with `id -u == 0` or can run `sudo -n true`. Only the minimum host/login identity and authentication checks may precede this gate. If any required machine fails it, do not invoke OBD and do not resolve, download, install, or run obdiag. Report `UNSUPPORTED — the current Skill version does not support using OBD with a login user that lacks root or usable non-interactive sudo privileges` and ask the user to switch the login user or configure usable sudo. Do not edit sudoers or use a user-local/all-in-one/source/manual-extraction workaround. After the gate passes, retain that login-session user and use sudo only for privileged commands. Apply the shared [highest-priority OBD privilege gate](../references/operation-contract.md#highest-priority-obd-privilege-gate).

Choose the smallest evidence scope that can answer the question. Tool availability, tool installation, collection, analysis, a tool finding, and independently confirmed root cause are separate results.

Before resolving or acquiring obdiag, read the shared [deployment package closure](../references/deployment-package-sets.md) and identify the exact dynamic diagnostic-tool artifact and installation path required by the retained workflow.

Before any package network request, select the effective artifact source before the acquisition mechanism and apply the shared [fixed package-source workflow](../obd-administration/references/mirror-and-repositories.md#fixed-online-package-source-order). A `.repo` file is configuration rather than a package source; prove the effective package URL, and keep operating-system dependency repositories separate. Remain on the current required source while trying applicable controller-local OBD/tool, `curl`, `wget`, or package-manager paths; verify and import/register the exact artifact locally before retrying. Keep OBD and obdiag execution on the selected controller, and never use `obd mirror` as a network downloader.

## Required Shared Gates

Read:

- [Product and capability resolution](../references/product-and-capability-resolution.md) before selecting an obdiag package, command, or target.
- [Operation contract](../references/operation-contract.md) before any live controller/host/deployment query, SSH/SQL/API/network access, installation, collection, scene update, artifact transfer, or another external action.
- [Completion criteria](../references/completion-criteria.md) before reporting collection, diagnosis, or root cause complete.
- [Failure recovery and evidence](../references/failure-recovery-and-evidence.md) before retrying a failed or interrupted diagnostic task or cleaning partial output.
- [Cleanup and ownership boundaries](../references/cleanup-boundaries.md) before removing diagnostic tools, generated files, collected evidence, or other artifacts.

Then read [workflows.md](references/workflows.md) for tool discovery, scope selection, execution, and interpretation rules.

## Tool Discovery

Identify the active OBD build and obdiag installation through core OBD tool inventory, already installed executable paths, and non-alias version evidence. Do not invoke `obd obdiag` or `obd obdiag --help` as an inventory probe because alias resolution can install or replace a dynamic tool.

If the tool is absent, install it through the supported [dynamic tool lifecycle](../obd-administration/references/tool-lifecycle.md) and verify the resulting executable, package version, and hash. Only after that exact installed identity is proved may alias-specific help be used to discover the available diagnostic command syntax. If alias invocation then attempts an unreviewed install or replacement, stop and reconcile tool state instead of accepting the side effect. Tool setup does not by itself authorize production collection; establish the diagnostic target and impact separately afterward.

## Diagnostic Boundary

Resolve the deployment, nodes, components, tenant when applicable, time window, evidence modules, output path, retention, expected size, data sensitivity, and runtime overhead before execution. Broad log collection, stack capture, performance sampling, or an all-module gather requires an impact review immediately before collection.

Do not present a rule, log pattern, check failure, or RCA suggestion as confirmed root cause until independent runtime, SQL/API, or system evidence corroborates it. Do not upload, delete, or broadly share diagnostic artifacts unless that action is separately in scope.
