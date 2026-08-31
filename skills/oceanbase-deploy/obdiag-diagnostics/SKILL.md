---
name: obdiag-diagnostics
description: Collect and analyze OceanBase diagnostic evidence through `obd obdiag`, including bounded gathers, checks, analysis, scenes, ASH, and RCA when supported by the installed tool. Use for incident diagnosis and obdiag requests; do not use for ordinary lifecycle status checks.
metadata:
  author: oceanbase
  version: "2.0.1"
---

# Diagnostics with obd obdiag

Choose the smallest evidence scope that can answer the question. Tool availability, tool installation, collection, analysis, a tool finding, and independently confirmed root cause are separate results.

Before resolving or acquiring obdiag, read the shared [deployment package closure](../references/deployment-package-sets.md) and identify the exact dynamic diagnostic-tool artifact and installation path required by the retained workflow.

Before any package network request, apply the shared [fixed mirror-source and acquisition-fallback workflow](../obd-administration/references/mirror-and-repositories.md#fixed-online-package-source-order). Try normal OBD/tool acquisition on the selected controller first; if it fails, use controller-local `curl`, `wget`, the operating-system package manager, or another applicable downloader, verify and import/register the exact artifact locally, then retry. If no controller-local method works, use another reachable host only as a checksummed artifact relay from the same ordered sources. Keep OBD and obdiag execution on the selected controller, and never use `obd mirror` as a network downloader.

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
