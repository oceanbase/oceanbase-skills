# Scaling and Component Changes

Use this workflow for Observer/OBProxy scale changes and OBD component add/delete. A registered node or component is not accepted until the product data plane recognizes it.

## Capability and Dependency Gate

1. Record the installed OBD build and selected subcommand help, deployment/product form, component plugins, repositories, status, topology, and real runtime state.
2. Derive the dependency graph and supported scale/component transitions from the registered configuration and installed workflows. Do not transfer a dependency order from a different product form or release.
3. Build an explicit incremental manifest: selected component/nodes, versions/releases/hashes, zones/failure domains, paths, ports, resources, network identity, and dependencies.
4. Check package compatibility and exact artifact availability. New nodes must not silently resolve a different release from existing nodes unless the reviewed workflow explicitly permits that transition.
5. Check target host identity, SSH, OS/runtime, canonical paths, ports, capacity, time/network, and overlap using the deployment preflight.
6. Identify application, tenant, OCP, monitoring, Config Server, log-service, and shared-storage dependencies and the availability impact.

Do not add a component simply because it appears in an example, bundle, or repository. Do not convert an incremental request into a replacement full configuration or redeploy.

## Scale Out

Render only the new server/component entries required by the installed `scale_out` workflow and validate them against the selected plugin schema.

```bash
obd cluster scale_out <deploy_name> --config=<incremental_config.yaml>
```

Use this syntax only when confirmed by installed help. Preserve the trace and config checksum. Verify OBD registration, actual binary identity, process/listener ownership, OceanBase/OBProxy product-side membership, zone placement, replication/balance progress, and existing-node health. Do not accept the operation while a node is merely registered but not serving its intended role.

## Scale In

Scale-in support, command form, evacuation behavior, and safety guards vary. Use it only when the installed OBD build and component workflow expose the exact transition. Before authorization, show the nodes/data/roles removed, quorum and failure-domain impact, active workload, evacuation or rebalance plan, retained paths, and rollback limit.

Never simulate scale-in by deleting YAML, stopping a process, deleting a component, or destroying its directory. Afterward verify product-side membership, data safety, topology, client routing, resource release, and absence of stale configuration.

## Add a Component

Build a schema-validated incremental config containing only the requested component and required fields. Use the installed syntax, commonly:

```bash
obd cluster component add <deploy_name> --config=<incremental_config.yaml>
```

For monitoring read [monitoring.md](monitoring.md); for OCP, Config Server, `oceanbase.ai`, `oblogservice`, and shared storage read their dedicated references. Verify the component exactly once in registered state, actual process/listener/path ownership, dependency integration, its own health/API, and a representative consumer path.

Inspect the exact semantics of any `--confirm`-like option before using it. In inspected OBD code, `component add --confirm` skips the prompt and immediately invokes restart. Adding Config Server when OBProxy already exists builds a selector containing OBProxy plus the existing OceanBase database component; adding it without OBProxy leaves the selector empty and can expand to a whole-deployment restart. Other component additions can reach the same empty-selector full-restart branch. Never use this flag merely to make automation non-interactive. Display and authorize the exact restart set first, or omit the flag and stop if the prompt cannot be handled safely.

If no safe incremental-add path exists, stop and present the limitation. Do not substitute redeploy or manual `.obd` metadata edits.

## Delete a Component

Before deletion, derive all dependants and consumers and identify retained data/configuration. Show the exact component/servers, availability effect, residual paths, and recovery boundary, then obtain configuration/destructive authorization as applicable.

Use only the installed command form. Remove dependants or migrate consumers in the derived order; do not assume one fixed monitoring deletion order across versions. After deletion, prove registered configuration, processes, listeners, dependency references, client/management paths, and separately owned data match the approved result.

The established command surface commonly uses:

```bash
obd cluster component del <deploy_name> <component_name> [version-supported selectors]
```

Do not turn the placeholder into an executable command until the exact component, dependants, retained paths/data, and installed selector syntax have passed the gate above.

## Partial Failure

On failure, freeze retries and record the trace, incremental config, registered before/after state, artifact installs, real processes/listeners, product topology, and dependency health. Do not drop a partially joined node, delete its directories, rerun with force, or redeploy until the observed stage proves the recovery action safe.
