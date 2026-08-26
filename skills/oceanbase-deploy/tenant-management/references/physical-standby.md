# Physical Primary/Standby Tenants

Use this workflow for tenant-level physical standby creation, topology inspection, switchover, failover, decouple, recovery-target changes, log-source changes, or protection-mode changes. Do not confuse it with deployment topology or SeekDB HA.

## Prove Both Compatibility Layers

Resolve the exact primary deployment and tenant and the intended standby deployment and tenant. Record each cluster ID, product form, component key, OceanBase version/release, artifact hash, tenant role, SQL/RPC endpoint, zones, resources, and current health.

Verify separately:

1. **OceanBase kernel compatibility:** the exact product forms and versions support the requested replication relationship and protection mode.
2. **OBD orchestration compatibility:** the installed OBD core and both selected component plugins support the exact component pair in the requested direction.

Healthy clusters and kernel support do not prove that OBD can orchestrate a heterogeneous pair. If release-specific evidence for that pair and direction is unavailable, stop before `create-standby`. Do not rename registered components, inject an unrelated component, redeploy healthy clusters, or change network/resource fields as a workaround.

## Preflight the Relationship

Read the installed help for the selected tenant subcommand. Confirm the primary tenant is healthy and `PRIMARY`, its log stream is complete, and the standby cluster has sufficient per-zone CPU, memory, log disk, Unit, and resource-pool capacity.

For a service-based source, verify the version-required SQL/RPC reachability and credential path. For a location-based source, verify the data-backup and archive-log chain, recovery target, storage reachability, and decryption material. Determine the requested protection mode from its write-availability, latency, downgrade, and failure-domain consequences rather than accepting a default silently.

Keep tenant-root, `standbyro`, storage, and decryption credentials protected. If the selected command exposes a required secret only through argv, disclose that limitation and use an approved permission-controlled local procedure; never describe the argument path as protected.

For the reviewed OBD V4.6.0 path using the OceanBase `4.2.0.0` plugin, a supplied `--standbyro-password` must be non-empty and must not contain a single quote, double quote, backtick, semicolon, or ASCII space. Validate the actual value locally without printing it, and re-read the installed plugin before applying this release-specific rule elsewhere.

Do not let omission of that option make the account decision implicit. Before mutation, select and authorize exactly one path:

1. **Existing manually managed `standbyro`:** supply the matching approved local credential through `--standbyro-password`. If the account exists but the value is absent or does not authenticate, stop; do not replace the account or rotate its password implicitly.
2. **OBD-managed `standbyro`:** allow OBD to reuse its stored value or, when none exists, generate a password, create the account if needed, grant its required read access, and persist the password in deployment component metadata. Disclose those account/grant writes and metadata persistence before execution. Verify metadata path ownership and permissions, backup/export exposure, who can retrieve the secret, redaction, and the post-creation rotation and account-lifecycle plan.

## Create and Accept a Standby

In builds that expose it, positional arguments are commonly ordered as standby deployment, primary deployment, and primary tenant. Confirm that order from installed help:

```bash
obd cluster tenant create-standby \
  <standby_deploy_name> \
  <primary_deploy_name> \
  <primary_tenant_name> \
  --tenant-name=<standby_tenant_name> \
  --type=<SERVICE_or_LOCATION> \
  --sync-mode=<reviewed_mode> \
  [version-supported source, resource, and credential options supplied through the approved local procedure]
```

Do not copy ordinary tenant-create options without checking `create-standby --help`.

Accept creation only when OBD and SQL show the intended `PRIMARY`/`STANDBY` roles, the topology graph has exactly the intended edge, the log source and protection mode are correct, replay is advancing without errors, measured replication lag is acceptable, `standbyro` authentication works, the selected credential persistence and custody path is verified without exposing the value, and no partial Unit/pool/account remains. A controlled write/replay test is optional and requires a separately approved test fixture; do not write business data merely to validate creation.

## Role and Source Operations

Refresh the topology graph, roles, reachability, replay SCN/time, lag, errors, application routing, archive state, and protection mode immediately before every mutation.

Before authorizing a role mutation, derive and show the version-specific protection-mode transition for every involved tenant. The reviewed OBD V4.6.0 behavior is:

| Operation | Topology or condition | Automatic protection-mode result |
|---|---|---|
| Planned switchover | cascading topology, or the selected standby is itself the configured strong-sync standby (including one-primary/one-standby and one-primary/multiple-standby topologies) | modes remain unchanged |
| Planned switchover | one primary has mixed strong-sync and performance standbys, and the directly associated performance standby is switched | every involved tenant changes to `MAXIMIZE PERFORMANCE` |
| Emergency failover | a strong-sync standby is promoted | the promoted tenant changes to `MAXIMIZE PERFORMANCE` |
| Decouple | a strong-sync standby is decoupled | the former primary and standby change to `MAXIMIZE PERFORMANCE` |

Treat any reduction to `MAXIMIZE PERFORMANCE` as a change to the data-loss envelope, not an incidental role-switch effect. Show the affected tenant identities and before/after modes and obtain explicit authorization for the downgrade in addition to the role operation. If version-matched evidence does not prove the installed version's transition, stop before mutation rather than assuming this matrix applies.

### Planned switchover

Use the installed `switchover` form only when both sides are healthy and synchronized within the accepted threshold. Coordinate writes and client routing and obtain availability-impact authorization. Verify both new roles, reverse-direction replication, write endpoint, client routing, and the authorized protection-mode transition afterward.

### Emergency failover

Failover is emergency promotion, not a substitute for switchover. Prove the old primary cannot accept writes and is fenced from clients and peers. Report the last synchronized SCN/time, possible data-loss window, and any automatic protection-mode downgrade, then obtain explicit failover and downgrade authorization. Verify new-primary writeability, routing, and protection mode and keep the old primary fenced until a reviewed reintegration plan exists.

### Decouple

Decouple permanently removes the relationship and can leave two independently writable tenants. Obtain explicit authorization for that outcome and any automatic protection-mode downgrade, then verify relationship and log-source metadata are removed and record both independent identities, routes, and protection modes.

After any switchover, failover, or decouple, query the database-side tenant role, `PROTECTION_MODE`, and `SYNC_STANDBY_DEST` for every involved tenant and compare them with the authorized transition matrix and intended relationship graph. Command or task success alone does not prove this state. If any value is unavailable or mismatched, report `partial` or `unknown` and keep fencing and routing decisions conservative.

### Recovery target, log source, and protection mode

Use `recover`, `switch-log-source`, or `set-sync-mode` only when installed help exposes the operation. Validate mutually exclusive timestamp, SCN, and unlimited-replay choices; SERVICE versus LOCATION source requirements; and topology support for the selected mode. Verify database-side values and continuing replay after the change.

## Destruction, Upgrade, and Failure Boundaries

Before dropping either tenant or upgrading/destroying either deployment, inspect the complete relationship graph and the version-specific standby guards. Never add `--ignore-standby` automatically. Show every affected tenant, availability or orphaning consequence, required order, and recovery path.

On any partial result, preserve both deployment configurations, roles, graph, task/trace, replay state, resources, and accounts. Do not drop a partial standby, fail over, decouple, or redeploy either cluster merely to retry creation.
