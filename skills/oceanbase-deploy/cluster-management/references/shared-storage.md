# Commercial Shared-Storage Deployment

Use this workflow only for a commercial OceanBase deployment topology whose selected installed plugin and artifacts explicitly support shared storage. This is database runtime storage, not tenant backup/archive storage, a benchmark data directory, or permission to provision an external storage service.

## Capability and Ownership Gate

1. Resolve product/component/version, OBD/plugin/workflow, commercial artifacts, and authoritative compatibility evidence for the exact shared-storage mode.
2. Identify the storage backend, protocol/driver/client, endpoint, namespace/tenant, pool/volume/filesystem/object identifiers, mount or URI semantics, authentication/TLS, and external owner.
3. Record per-host device/mount identity, canonical paths, permissions/UID/GID, symlinks, mount options, multipath/fencing/lease behavior, capacity/inodes, latency/throughput, durability, and failure domains.
4. Separate shared database data from local home, logs, caches, temporary files, and any local redo/log areas as defined by the plugin. Do not assume every path is shared.
5. Establish exactly what OBD deploy, stop, destroy, redeploy, scale, and upgrade workflows create, format, retain, or delete. External storage ownership is not inferred from a path appearing in YAML.
6. Define storage provisioning, snapshot/backup, fencing, credential rotation, and recovery ownership outside OBD when the plugin does not manage them.

The same path text on multiple servers does not prove the same backing storage. Conversely, different mount points may refer to one volume. Verify stable backend identity.

## Schema-Gated Configuration

Derive every storage key from the selected commercial plugin. A non-executable decision blueprint is:

```yaml
<verified-commercial-component-key>:
  servers:
    - ip: <management_ip>
  global:
    <verified-storage-mode-key>: <supported_shared_mode>
    <verified-backend-or-endpoint-keys>: <approved_storage_identity>
    <verified-shared-data-path-or-uri-keys>: <approved_values>
    <verified-local-home-log-temp-keys>: <canonical_local_paths>
    <verified-storage-credential-key>: <protected_secret_reference>
```

Do not guess a backend type, parameter name, URI, mount layout, or credential format. A protected reference is valid only when the selected plugin preserves that protection; if it embeds a secret in ordinary YAML, a URI, a remote command, or trace output, stop unless the exact exposure and credential lifecycle are separately approved. If the commercial schema/artifact is unavailable, report the missing input and stop rather than falling back to local disks or a community template.

## Preflight and Deployment

On every target, verify driver/client version, route/TLS/authentication, backend identity, read/write permissions in a dedicated approved test object/path, capacity/inodes/performance headroom, clock/fencing prerequisites, and absence of another cluster's ownership marker. Remove only the dedicated test object created for preflight.

Show the storage namespace/volume, intended cluster identity, formatting/initialization effects, data-loss boundary, external rollback/snapshot, and exact paths before authorization. Then follow [config-deployment.md](config-deployment.md) using the reviewed schema and artifact lock.

## Acceptance

Verify all hosts see the intended backend identity and plugin-required consistency state; local/shared paths have correct ownership; actual processes/listeners and SQL topology are healthy; the product reports the intended storage mode; a controlled data operation persists as expected; and no unrelated namespace or volume changed.

Do not simulate a host/storage failure merely to prove resilience without separate disruptive-test authorization. Use existing product health and non-destructive storage evidence unless a controlled failover test is explicitly requested.

## Lifecycle and Recovery

Before scale, upgrade, redeploy, destroy, or storage replacement, map leases/fencing, active I/O, snapshots/backups, data ownership, and external consumers. Treat removal of OBD metadata, local paths, mounts, external volumes, snapshots, and stored data as separate operations with separate authorization.

On failure preserve trace, storage identities/mounts, plugin/configuration, process and product state, leases/fencing evidence, and backend errors. Do not remount with weaker options, reformat, clear locks, delete a namespace, or redeploy as generic recovery.
