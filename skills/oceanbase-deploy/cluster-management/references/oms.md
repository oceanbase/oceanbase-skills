# OBD-Managed OMS

Use this workflow for deploying, operating, configuring, upgrading, or troubleshooting OceanBase Migration Service (OMS) through OBD. OMS is not OCP, ODP, Binlog Service, an OceanBase tenant, or a data-migration project. This workflow proves the OMS control plane; source/target mapping, migration-project configuration, cutover, and migrated-data validation still require the version-matched OMS product documentation.

## Required Gates and Evidence Boundary

Before producing an executable command or configuration:

- Read [product and capability resolution](../../references/product-and-capability-resolution.md) and preserve the exact installed OMS component key, plugin, schema, workflows, image, edition, and license boundary.
- Read the shared [operation contract](../../references/operation-contract.md), including controller identity, credentials, telemetry, and mutation authorization.
- Use the shared [configuration deployment](config-deployment.md), [lifecycle](lifecycle.md), and [completion criteria](../../references/completion-criteria.md) unless this reference adds a stricter OMS rule.
- After failure, timeout, interruption, or a mixed result, read [failure recovery and evidence](../../references/failure-recovery-and-evidence.md). Before destroy, redeploy, cleanup, or removal, also read [cleanup and ownership boundaries](../../references/cleanup-boundaries.md).

The public OBD V4.6.0 baseline documents:

- deployment management for **OMS Community Edition 4.2.11 or later** with OBD 4.0.0 or later;
- CLI upgrade for an OBD-managed OMS Community Edition deployment with OBD 4.0.0 or later;
- graphical upgrade for OMS Community Edition with OBD 4.1.0 or later.

The guide's x86 CentOS 7.9 environment is a worked example, not a universal support matrix. Confirm the actual OS, architecture, Docker, OMS, and OBD compatibility before execution.

Current source recognizes both `oms` and `oms-ce`. Official V4.6.0 deployment examples commonly use `oms`, while the documented CE upgrade example uses `oms-ce`. Preserve the exact key registered in the selected deployment and confirmed by installed help; do not normalize one key into the other.

Commercial OMS remains supported by capability resolution, not by copying the CE baseline. Require approved commercial documentation, images, repositories, schema, plugins, workflows, and upgrade matrix. Never replace a commercial image or component with `oms-ce`, a `feature_*_ce` tag, or a public/community artifact merely because the open-source controller recognizes a similar name.

## Choose the Supported Path

| Requested outcome | Path |
|---|---|
| Reproducible deployment | Reviewed YAML, then separate `cluster deploy` and `cluster start` transitions |
| Guided CE deployment | `obd web`, only when the user explicitly requests the graphical workflow |
| Lifecycle or configuration change | Installed OMS lifecycle/reload workflow, with the migration-task impact shown first |
| OMS upgrade | OMS-specific online/offline upgrade workflow; never generic reinstall or redeploy |
| Scale out or component add/delete | Stop unless the installed OMS package exposes a dedicated OMS workflow and edition/version documentation authorizes it |

OBD V4.6.0 explicitly excludes OMS from generic component addition and scale-out. Inspected current OMS packages also lack dedicated generic scale/add/delete workflows. A generic command being accepted is not evidence that OMS containers or topology changed correctly.

The documented Web entry point, `obd web`, listens on `0.0.0.0` and defaults to port 8680. Starting it creates a network listener and controller task. Review interface exposure, authentication, firewall, reverse proxy/TLS, port ownership, and shutdown before authorization. Do not start Web merely to discover whether OMS support exists.

## Deployment Preflight

Resolve and record:

1. **Controller and artifacts:** exact OBD build and `OBD_HOME`, installed OMS plugin/workflows, approved image repository, tag, image ID/digest, provenance, and license boundary. Do not use an internal registry string copied from an example.
2. **Hosts and Docker:** every OMS node's machine identity, OS/architecture, Docker version/service, privilege model, and ability to inspect the exact image. For multi-node OMS, the approved image must be loaded on every node and every node must report the same image identity. The inspected image check does not pull a missing image.
3. **Topology:** choose single-node, single-region multi-node, or multi-region multi-node. Map each OMS server to exactly one region; require unique `cm_location` values, exactly one default region, no duplicate `cm_nodes`, and equality between the union of `cm_nodes` and the configured server set.
4. **MetaDB:** choose either an existing external MySQL/OceanBase MetaDB or an explicitly approved OceanBase dependency in the same YAML. Record database/tenant/schema identity, endpoint, account privilege, TLS/network, backup owner, recovery plan, and availability. The guide recommends a highly available MetaDB. Do not create, replace, or upgrade it implicitly.
5. **Monitoring:** OMS monitoring is optional. The V4.6.0 baseline documents InfluxDB 1.8. Treat its deployment, endpoint, credential, retention, and backup as separately owned scope.
6. **Paths and resources:** use dedicated empty canonical paths with known owner, mount, symlink, inode, and cleanup boundaries. The V4.6.0 guide requires at least 500 GB free for `mount_path`. Current source warnings at lower disk, CPU, or memory thresholds are not proof that a host satisfies OMS product sizing.
7. **Ports and routes:** check every real listener and firewall path for MetaDB, optional InfluxDB, OMS services, the UI/API endpoint, and inter-region traffic.
8. **Secrets:** determine how MetaDB, TSDB, SSH, registry, and UI credentials enter OBD and remote configuration. Treat the registered/generated YAML, OBD traces, container inspection, and mounted OMS configuration as sensitive evidence.

Importing an OMS image with `docker load` is a separate host/repository mutation. Before running it on every selected node, verify the archive checksum and expected image identity, obtain authorization, and confirm the resulting repository, tag, and image ID. Do not add `--force` or cleanup a path when an image or directory check fails.

## Version-Gated Configuration

The following is a decision scaffold for an external MetaDB, not executable YAML. Replace every placeholder only from the selected installed schema and a version-matched released example:

```yaml
<exact_oms_component_key>:
  type: docker
  image_name: <approved_image_repository_without_tag>
  tag: <approved_image_tag>
  servers:
    - name: <unique_server_name>
      ip: <oms_server_ip>
  global:
    oms_meta_host: <external_metadb_host>
    oms_meta_port: <external_metadb_port>
    oms_meta_user: <approved_metadb_user>
    oms_meta_password: <protected_secret_input>
    mount_path: <dedicated_empty_absolute_path>
    regions:
      - cm_location: 1
        cm_is_default: true
        cm_region: <region_identifier>
        cm_region_cn: <optional_display_name>
        cm_url: http://<cm_endpoint>:<cm_server_port>
        cm_nodes:
          - <oms_server_ip>
```

When OMS uses an OceanBase component in the same deployment as MetaDB, add the dependency only after reviewing that OceanBase deployment and tenant/resource outcome:

```yaml
<exact_oms_component_key>:
  depends:
    - <exact_reviewed_oceanbase_component_key>
```

Do not combine these fragments or omit explicit `oms_meta_*` values merely because a similarly named OceanBase component exists. Prove that the installed OMS plugin derives the intended sys-tenant endpoint and credential from that exact dependency. For an OceanBase MetaDB, the V4.6.0 UI requires a sys-tenant account but says not to append the tenant name; inspected current configuration generation also rejects `@sys` in `oms_meta_user`.

### Core Key Semantics

Confirm these classifications against the installed schema before editing a deployment:

| Keys | V4.6.0 baseline | Change boundary |
|---|---|---|
| `type`, `image_name`, `tag` | OMS uses `type: docker`; exact image and tag select the artifact | Immutable in the configuration table; use the supported OMS upgrade path |
| `servers` | OMS node IPs, not hostnames | Redeploy-class topology change |
| `oms_meta_host`, `oms_meta_port`, `oms_meta_user`, `oms_meta_password` | Required for an external MetaDB | Documented as restart-required |
| `drc_rm_db`, `drc_cm_db`, `drc_cm_heartbeat_db` | OMS MetaDB schema names | Immutable after deployment |
| `tsdb_service`, `tsdb_url`, `tsdb_username`, `tsdb_password` | Optional; documented service is `INFLUXDB` | Documented as restart-required |
| `ghana_server_port`, `nginx_server_port`, `cm_server_port`, `supervisor_server_port`, `sshd_server_port` | Defaults 8090, 8089, 8088, 9000, and 2023; each 1025-65535 | Documented as restart-required |
| `mount_path` | Dedicated absolute data path with at least 500 GB free | Immutable |
| `regions`, `cm_is_default`, `cm_url` | Required topology and service routing | Documented as restart-required |
| `cm_location`, `cm_region`, `cm_region_cn`, `cm_nodes` | Region identity and membership | Immutable in the V4.6.0 table |
| `settings` | Optional pass-through values | Use only keys formally supported by the selected OMS version |

The GUI documents default schema names `oms_rm`, `oms_cm`, and `oms_cm_heartbeat_<location>`, while the raw configuration table and examples are inconsistent about whether they must be explicit. Do not infer a universal default; inspect the installed generator/schema or supply reviewed, collision-free names explicitly.

Likewise, official V4.6.0 examples use `tsdb_url`, while an inspected source schema also mentions `tsdb_host` and `tsdb_port` even though runtime code consumes `tsdb_url`. Do not translate between these forms. Require the installed parser/precheck to accept the exact rendered configuration.

Without a VIP, `regions[].cm_url` must use `cm_server_port`, normally 8088. The browser/UI endpoint normally uses `nginx_server_port`, 8089. Do not confuse them. Write an `https://` URL in full when TLS is configured, and do not use `127.0.0.1` as a multi-host CM endpoint.

The official baseline uses one `mount_path`. Inspected current source can also expose split `logs_mount_path`, `run_mount_path`, and `store_mount_path`; if that installed schema is selected, provide all three and give each its own ownership, capacity, and cleanup review.

## Deploy and Start

Review the full configuration and image identity, apply the shared telemetry gate, and use the installed public syntax:

```bash
obd cluster deploy <deploy_name> --config=<reviewed_oms.yaml>
obd cluster start <deploy_name>
```

`deploy` registers and installs the deployment but does not prove OMS is running. Inspect its trace, registered configuration, repository/image identity, initialized paths, and partial state before separately authorizing `start`. Never add `--force`, `--clean`, or a redeploy shortcut to bypass a non-empty path: inspected OMS initialization can recursively clear the selected data path under force behavior.

In inspected current source, first start can create a privileged Docker container using host networking, host-mounted configuration/data paths, relaxed process limits, and the exact image. It can also submit OMS deployment telemetry independently of ordinary command reporting. Verify these behaviors in the installed build and include the container, mount, privilege, listener, and telemetry effects in authorization.

Accept deployment only when all applicable checks pass:

- OBD reaches a successful terminal state and preserves a trace ID;
- registered component key, image repository/tag/hash, servers, regions, ports, and paths match the reviewed plan;
- every node has the same approved image and the expected container, host-network, mounts, and runtime state;
- every node's `http://<node>:<nginx_port>/oms/health` returns a healthy result, or the installed version's equivalent authenticated health check passes;
- every expected region/UI/API endpoint is reachable through the approved route and OMS authentication succeeds;
- MetaDB identity, expected schemas, and connectivity are correct; optional InfluxDB is healthy when configured;
- a representative OMS migration control-plane operation is usable and unrelated deployments, images, paths, schemas, and listeners are unchanged.

`obd cluster display` reports registered state and region URLs; it is not a substitute for per-node health, authentication, image, MetaDB, or migration-control-plane checks.

## Lifecycle, Configuration, and HA

Use installed `display`, `start`, `stop`, `restart`, `reload`, and `destroy` workflows through the shared lifecycle gates. Before stop or restart, identify running migration tasks and accepted interruption. Inspected current OBD requires an OMS-specific restart confirmation because migration tasks can become unavailable.

For a configuration change, apply the V4.6.0 change classification above and the installed OMS parameter/workflow evidence. Do not describe a successful `edit-config` or `reload` as proof that restart-required or immutable keys took effect. Inspected reload regenerates and distributes OMS configuration, runs container initialization, and then performs a health check; treat it as a possible availability and MetaDB/TSDB interaction, not a text-only edit.

OMS CE starts with HA disabled in the documented baseline. Enabling or disabling `ha.config.enable` in the OMS console is a separate product mutation. Record the current value, migration tasks, expected availability effect, rollback, and validation; do not enable HA merely because deployment succeeded.

Destroy is destructive. Inspected workflows force-remove OMS containers and recursively clean `mount_path`, or the installed split data/config paths. Display every canonical deletion target and obtain exact authorization immediately before the command. Do not delete external MetaDB schemas, InfluxDB data, image repositories, controller backups, or OBD registration unless each separately owned object is explicitly included. Metadata pruning is separate from destroy.

## OMS-Specific Upgrade

Use the OMS upgrade path only for an edition and source/target version pair proved by installed and authoritative evidence. The public V4.6.0 procedure covers OMS Community Edition; do not transfer it to commercial OMS.

### Preflight

1. Require an OBD-managed, fully running, healthy deployment with no pending configuration change. Record the exact registered OMS component key, current image/tag/hash, migration tasks, regions, containers, MetaDB/TSDB, HA state, and recovery boundary.
2. Load the exact target image on every OMS node and verify identical repository, tag, image ID/digest, provenance, and compatibility.
3. Disable OMS HA before upgrade through the documented product control only after separate availability authorization. Verify `ha.config.enable=false`; do not rely only on an OBD prompt or precheck.
4. Review source/target compatibility, current and target package candidates, online/offline mode, expected outage, per-node scratch capacity, controller backup path, and rollback boundary.
5. Back up critical MetaDB schemas and independently verify every expected backup artifact before allowing the upgrade to cross an irreversible stage.

Use the installed public command shape. The V4.6.0 CE example uses `oms-ce`, but substitute the exact component key registered in the selected deployment:

```bash
obd cluster upgrade <deploy_name> \
  --component=<exact_registered_oms_component> \
  --tag=<approved_target_tag> \
  --image-name=<approved_target_image> \
  --oms-backup-path=<dedicated_controller_backup_path>
```

For OMS, V4.6.0 requires `--tag` and `--image-name`; `--version` is the non-OMS form. Review the displayed start and destination image hashes and abort on any mismatch. The current source can accept an explicit `offline` or `online` positional mode; use it only when the installed command help exposes that syntax. Otherwise use the documented controlled interactive choice.

Do not add `--skip-check`. Do not add `--disable-oms-backup` merely to proceed: skipping backup is a separate high-risk decision requiring explicit acceptance of MetaDB recovery loss.

### Backup Boundary

The documented backup path is local to the OBD controller; the CLI default is `~/oms/meta_backup_data`, while the graphical workflow requires an absolute path with at least 2 GiB free. Use a dedicated protected directory outside deployment-owned cleanup paths.

Inspected current source dumps `oms_cm`, `oms_rm`, and region heartbeat schemas from the first OMS container. It does **not** establish a backup of InfluxDB monitoring/history. It can also delete older `heatbeat_sequence` rows before dumping and place the MetaDB password in a `docker exec`/`mysqldump` argument. Treat backup as a credential-exposing MetaDB mutation, verify the installed implementation, and obtain authorization for that exact behavior.

Do not accept a successful backup task alone. Require every expected SQL file to exist, be non-empty and protected, map to the reviewed schema set, and pass an appropriate readability/restore-validation check without overwriting production data.

### Upgrade Modes

| Mode | Documented behavior | Required additional gate |
|---|---|---|
| Offline | Replaces the old container with a container from the target image; migration links are briefly interrupted | Approve the outage and prove how to recover if the old container is stopped but the new one never becomes healthy |
| Online | Replaces component files inside the existing container; the guide states migration links remain uninterrupted when prerequisites hold | Provide a new per-node export directory with more than 20 GiB free; treat the operation as availability-impacting because hot update or rollback can fail |

For online upgrade, preserve every node's export directory, container backup path, logs, and rollback result until acceptance. For offline upgrade, preserve both old and new container identities and do not restart or remove either after a partial failure until the active image, MetaDB state, and recovery path are known.

### Upgrade Acceptance

Require all deployment acceptance checks plus:

- every OMS machine is `Online` in the OMS console;
- `Help Center > About OMS` or a version-matched authenticated API reports the exact target version;
- every node uses the approved target image/package and no unexplained mixed or backup container remains;
- representative migration links/tasks are in the expected state and client routing is correct;
- MetaDB schemas are healthy and every required backup remains protected;
- online rollback is confirmed complete on every node when it was triggered;
- HA is re-enabled only after all validation passes and only when that separate product mutation is requested and authorized.

## Official Error Triage

| Error | Meaning | Narrow response |
|---|---|---|
| `OBD-4701 failed to connect meta db` | External MetaDB connection or configuration failed | Verify exact MetaDB identity, route, TLS, account, and installed key names; review a complete configuration before `edit-config` |
| `OBD-4702 failed to connect influxdb` | Configured InfluxDB endpoint or credential failed | Verify the optional TSDB identity and the installed `tsdb_*` schema; do not deploy or replace InfluxDB implicitly |
| `OBD-4703 ... not enough disk space` | Online-upgrade export path is too small | Select a new dedicated per-node path satisfying the documented capacity and ownership checks |
| `OBD-4704 HA is enabled` | Upgrade requires OMS HA to be disabled | Disable HA only through the reviewed OMS product workflow and verify the value before retrying |

An `edit-config` recommendation does not authorize reload, restart, redeploy, schema creation, or another upgrade attempt. Classify the observed state and apply the narrowest supported transition.

## Failure and Cleanup Boundary

On any failed deploy, start, reload, upgrade, or Web task, preserve:

- OBD/Web task and trace IDs, redacted inputs, plugin/workflow identities, and terminal stage;
- registered and generated configuration checksums;
- exact current/target images, old/new/backup containers, mounts, export paths, listeners, and per-node health;
- MetaDB schema state, backup artifacts, executed DML/DDL evidence, InfluxDB state, HA value, and migration-task state.

Do not use the Web “redeploy” recovery button, rerun deploy/upgrade, delete containers or volumes, restore a MetaDB backup, initialize schemas again, re-enable HA, or clean export paths until the completed stage and data-loss boundary are known. The graphical redeploy action cleans a failed OMS installation environment and is therefore a destructive operation requiring its own reviewed deletion set and authorization.

## Sources

- Official OBD V4.6.0 User Guide: sections 6, 10, 11.4, 16, and 35.
- Official OBD V4.6.0 Command Guide: `cluster upgrade` and OMS-specific options.
- Official OBD V4.6.0 error guide: `OBD-4701` through `OBD-4704`.
- [Official public OBD V4.6.0 source baseline](../../references/source-baselines.md#official-obd-v460-baseline): `const.py`, `_cmd.py`, `core.py`, `plugins/oms/1.0.0/`, `workflows/oms/1.0.0/`, and the OBD Web OMS handler.
