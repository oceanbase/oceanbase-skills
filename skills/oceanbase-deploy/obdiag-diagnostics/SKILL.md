---
name: obdiag-diagnostics
description: Collect and analyze OceanBase diagnostic evidence through `obd obdiag`, including bounded gathers, checks, analysis, scenes, ASH, and RCA when supported by the installed tool. Use for incident diagnosis and obdiag requests; do not use for ordinary lifecycle status checks.
metadata:
  author: oceanbase
  version: "3.0"
---

# Diagnostics with obd obdiag

Choose the smallest evidence scope that can answer the question. Tool availability, tool installation, collection, analysis, a tool finding, and independently confirmed root cause are separate results.

## Required Shared Gates

Read:

- [Product and capability resolution](../references/product-and-capability-resolution.md) before selecting an obdiag package, command, or target.
- [Operation contract](../references/operation-contract.md) before any live controller/host/deployment query, SSH/SQL/API/network access, installation, collection, scene update, artifact transfer, or another external action.
- [Completion criteria](../references/completion-criteria.md) before reporting collection, diagnosis, or root cause complete.
- [Failure recovery and evidence](../references/failure-recovery-and-evidence.md) before retrying a failed or interrupted diagnostic task or cleaning partial output.
- [Cleanup and ownership boundaries](../references/cleanup-boundaries.md) before removing diagnostic tools, generated files, collected evidence, or other artifacts.

Then read [workflows.md](references/workflows.md) for the inventory gate, scope selection, execution, and interpretation rules.

## Mandatory Tool Inventory Gate

Before any `obd obdiag` invocation, including `obd obdiag --help`, inspect the OBD tool inventory, local and remote repository candidates, installed tool paths, and automatic-confirm/network settings without invoking the alias. An installed tool does not make the alias read-only: determine whether this OBD build checks for or attempts an update before dispatching the requested obdiag command.

If the tool is absent, use the [dynamic tool lifecycle](../obd-administration/references/tool-lifecycle.md) and obtain explicit download/install authorization. If the tool is present but alias dispatch can update it and that behavior cannot be disabled or pinned safely, treat the first alias invocation as a potential download/tool-replacement mutation and obtain authorization for the resolved candidate—or do not invoke it. Authorization to install or update the tool is not authorization to inspect a deployment or collect production evidence; establish the diagnostic target and impact separately afterward.

## Diagnostic Boundary

Resolve the deployment, nodes, components, tenant when applicable, time window, evidence modules, output path, retention, expected size, data sensitivity, and runtime overhead before execution. Broad log collection, stack capture, performance sampling, or an all-module gather requires an impact review immediately before collection.

Do not present a rule, log pattern, check failure, or RCA suggestion as confirmed root cause until independent runtime, SQL/API, or system evidence corroborates it. Do not upload, delete, or broadly share diagnostic artifacts unless that action is separately in scope.
