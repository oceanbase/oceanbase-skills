# Commercial `oblogservice`

Use this workflow for the OBD component commonly named `oblogservice`, the OceanBase log-service cluster. Do not route another log or CDC product request here merely because its name is similar.

## Capability and Dependency Gate

1. Record OBD build, exact `oblogservice` plugin/workflow, package version/release/architecture/hash/source, requested role, and commercial artifact boundary.
2. Resolve the supported upstream OceanBase product and version from the installed workflow. A locally inspected OBD source revision gates this integration to `oceanbase.ai` at or above a particular version; treat that as implementation evidence only and re-derive the exact component/version gate at runtime.
3. Resolve server-count/bootstrap rules, allowed co-location/multi-instance behavior, ports, canonical home/data/log paths, storage, CPU/memory/disk allocation, network/TLS/authentication, and dependency direction from the selected plugin.
4. Check combined host resources across all log-service instances and other components, not just each instance in isolation.
5. Verify bootstrap-server identity and reachability and map every upstream/downstream consumer.

If the product form, minimum version, bootstrap target, plugin, or commercial artifact cannot be proved, stop. Do not substitute another product or a generic log directory.

## Schema-Gated Deployment

Render configuration only from the installed `oblogservice` schema and reviewed manifest. Use the regular config deployment for a new topology or the safe incremental component workflow when it is explicitly supported. Never redeploy the upstream database merely to add log service.

Before execution, show selected servers/instances, bootstrap identity, resource allocation, paths/ports, dependency and availability impact, and artifact hashes. Validate all per-instance uniqueness constraints.

## Object-Storage Secret Boundary

An inspected `oblogservice` plugin treats an object-storage URL containing an access key as an ordinary string and can include it in rendered configuration and verbose trace. Prefer a plugin-supported secret reference. When the selected version requires a credential-bearing URL, use a dedicated least-privilege short-lived credential, protect the configuration and trace files, keep the value out of chat and reports, and rotate or revoke it after the scoped operation.

## Lifecycle and Upgrade Boundary

Read selected lifecycle subcommand help and plugin workflows for start, stop, restart, scale, reinstall, upgrade, and delete. At least one inspected OBD source revision explicitly rejects `oblogservice` upgrade; when the installed build does so, stop and present supported alternatives rather than forcing a generic cluster upgrade or reinstall.

Before stop/delete/scale-in, identify upstream availability impact, active consumers, retained log data, and recovery boundary. Permission to stop does not authorize deleting component metadata or persistent data.

## Acceptance and Failure

Verify component/artifact identity, every instance process/listener/path, bootstrap membership/leader state as defined by the plugin, upstream integration, resource state, and a representative supported log-service data-plane operation. A running process or open port is insufficient.

On failure preserve trace, configuration, plugin identity, bootstrap state, all instances, resources, paths/logs, and upstream health. Do not repeatedly change bootstrap servers, add instances, force an unsupported upgrade, delete data, or redeploy the database as generic recovery.
