# Cluster Lifecycle

Use this workflow for display, start, stop, restart, destroy, redeploy, prune, `demo`, and `perf`. Refresh deployment and real runtime state immediately before every mutation.

## Resolve the Target

Record the controller, deployment, product form, component/plugin and artifact identities, registered servers, paths, ports, current OBD status, actual processes/listeners, SQL/API health, active tasks, tenants, backups, and external dependants.

Read the exact selected subcommand help. If server, component, or service selectors are available, resolve them to an explicit target list and show selected and unselected objects. Short options are command-scoped; prefer long names and never reuse `-S` from a deployment example in another command.

## List and Display

Preserve the ordinary logical-inventory path before choosing a lifecycle mutation:

```bash
obd cluster list
obd cluster display <deploy_name>
```

Confirm these forms with the installed help. They can still initialize or reconcile controller-local `OBD_HOME` state and write a trace, so apply the OBD CLI startup-side-effect gate in the shared operation contract; they are not strict zero-write probes. Treat their output as controller registration and reported status, not proof that every process, listener, dependency, or data plane is healthy. For a status-only request, stop after the requested inventory unless the user separately asks for diagnosis or a state change.

## Start, Stop, and Restart

Before start, establish whether the deployment is fully installed or partially initialized, whether ports and paths remain owned by it, and whether dependencies are ready. Before stop/restart, identify application routing, active workload, replication/management relationships, and the acceptable outage.

Apply the shared telemetry gate immediately before start or stop; OBD V4.6.0 documents both as telemetry triggers. Inspect the installed implementation for restart rather than assuming it has identical behavior. A telemetry-setting change is a separate controller-wide mutation, not part of lifecycle authorization.

Inspect the version-matched stop and restart workflows for a pre-stop compaction stage. In the inspected `ob-deploy` tree, the OceanBase 4.2.1.4 workflows add `connect` and `compaction` before stop or restart unless an internal `skip_compaction` input is set. The matched compaction plugin issues minor freezes for `sys`, `all_user`, and `all_meta`; a connection failure or an individual SQL failure is warned and the workflow can continue. Disclose the freeze and possible I/O/compaction impact before execution, preserve each warning, and verify the freeze/compaction outcome independently instead of inferring it from the later stop or restart exit.

Do not invent, expose, or recommend the internal `skip_compaction` input as a user option. Use it only if the installed public command help explicitly exposes a supported equivalent and its consistency and recovery impact has been reviewed.

Run only the reviewed command form:

```bash
obd cluster start <deploy_name> [version-supported selectors]
obd cluster stop <deploy_name> [version-supported selectors]
obd cluster restart <deploy_name> [version-supported selectors]
```

Do not widen a scoped request to the whole deployment. Afterward, verify every selected target reached the intended state, every unselected target remained unchanged, dependency order is healthy, and the applicable SQL/API/data-plane check passes. Report mixed states explicitly.

Before a scoped `restart`, require the deployment to be fully running and healthy and inspect the selected build's status branch. Inspected OBD implementations can accept a stopped deployment and call a whole-deployment start before applying restart component/server selectors when state is stopped or unhealthy. Therefore, never issue a scoped restart against a stopped, partially running, or unhealthy deployment unless that implicit full start and every affected component have been separately displayed and authorized. If the request must remain scoped, stop and use a version-proved alternative.

Treat `reload` according to its own installed help rather than borrowing restart selectors. Current inspected OBD HEAD exposes no component/server selector for reload and applies the workflow across the deployment; on a stopped or unhealthy deployment it can first start the whole deployment. Present and authorize reload as a whole-deployment configuration/availability operation, or stop when the requested scope is narrower.

## Automatic Startup and systemd

Treat a plugin field such as `enable_auto_start` as a persistent privileged host mutation, not an ordinary runtime parameter. Before enabling or disabling it, inspect the exact installed plugin script and record the service account, unit name/content, executable and PID paths, start/stop/restart policy, sudo path, files copied, permission changes, marker files, `systemctl` operations, and behavior during reload and destroy.

Verified current OceanBase plugin code can copy an `auto_start.sh` helper, create an `obd_oceanbase_<appname>.service` unit, run `daemon-reload` and `enable`, configure `Restart=on-failure`, and recursively make the deployment `tmp` directory world-readable/writable/executable. It can also feed an SSH password to `sudo -S`. Treat these as version-specific implementation evidence. If the broad permission or credential exposure violates policy, stop; do not enable auto-start and do not “fix” the shipped workflow by silently editing it.

Show the exact per-host diff and collision/privilege/security impact, then obtain persistent-host authorization. Verify the installed unit's checksum/content, owner/mode, enabled/active state, PID ownership, marker/helper paths, effective directory permissions, and agreement with OBD and SQL health. Do not reboot merely to test it unless reboot is separately authorized.

Disabling the setting, reloading configuration, and destroying a deployment can remove different subsets of the marker, enabled state, helper, and unit. Inspect the selected version's cleanup path first. Disabling automatic startup alone must not stop a currently running database process; stop it only when a separately reviewed stop or destroy scope has been authorized. Afterward verify `systemctl` state, unit-file absence/presence as intended, daemon state, processes, and retained permission changes. Never remove a similarly named unit or recursively rewrite permissions as generic cleanup.

## Destroy and Prune

Read [cleanup and ownership boundaries](../../references/cleanup-boundaries.md) before defining either removal set. Destroying runtime/data state and pruning controller metadata are separate operations.

`destroy` can stop services and delete deployment-owned data. Before requesting confirmation, show:

- exact deployment/component/server identity;
- all canonical home, data, log, shared-storage, and external paths and their ownership;
- tenants, backup state, replication/OCP/monitoring/client dependencies;
- what the installed destroy workflow removes and retains;
- recovery boundary and separately owned data that must remain.

Obtain destructive authorization immediately before the exact command. Do not add an ignore, force, or standby-bypass option automatically.

After that authorization, preserve the installed public command shape:

```bash
obd cluster destroy <deploy_name>
```

Use `prune-config` only after proving the deployment is in a version-supported metadata-only state and inspecting what the installed command removes. Inspected implementations allow `destroyed` or `configured`; do not use it for a deployed or running state. Permission to destroy does not authorize metadata pruning. Verify absence of the exact authorized objects and preservation of unrelated deployments and paths.

```bash
obd cluster prune-config <deploy_name>
```

## Redeploy

Redeploy is a destructive rebuild, not a repair, reload, component-add, or monitoring-install shortcut. Require the normal destroy evidence plus the exact replacement artifacts/configuration, backups and recovery plan, outage, tenant outcome, and post-rebuild identity expectations.

If OCP is present, read [ocp.md](ocp.md) and classify its MetaDB and takeover relationship before authorization. If shared storage or external data paths are present, read [shared-storage.md](shared-storage.md) and prove what redeploy will and will not erase.

After the complete destructive-rebuild plan is authorized, use only the installed public form:

```bash
obd cluster redeploy <deploy_name>
```

After redeploy, verify the replacement artifact/configuration, process/listener state, authenticated data plane, tenant/data outcome, and every management/monitoring relationship. A newly healthy process does not prove data or control-plane continuity.

## Quick-Deploy Shortcuts

`obd demo` and `obd perf` are integrated mutating convenience workflows, not configuration generators. Their deployment names are fixed to `demo` and `perf`. Use either only when the user explicitly chooses that exact shortcut and accepts its installed behavior.

Before execution, read installed help/workflow; inspect the matching registered name, target paths, ports, processes, and component set; and explain every object that can be overwritten or removed. In the inspected current source, `demo` internally enables force, clean, force-delete, and force-kill, while `perf` enables force, clean, force-delete, and maximum-resource generation. These are implicit implementation behaviors even when the user does not type those flags. Reconfirm them for the installed build and bind authorization to the complete collision and deletion set. Prefer a uniquely named config deployment whenever ownership is unclear.

`perf` is the official maximum-specification local quick-deploy command, not an alias for `autodeploy`. It defaults to a build-defined component set and a fixed `perf` namespace. Do not silently substitute `autodeploy`, use it as a general production or commercial deployment path, or assume “maximum” consumes every byte safely. Reserve OS and operational headroom and review the generated topology and resources before execution.

For the previously supported database-only demo scope, prefer the explicit long form when installed help confirms it:

```bash
obd demo --components=oceanbase-ce
```

After execution, verify the registered `demo` component list, real processes/listeners, exact paths, and authenticated SQL/HTTP data planes that apply. Report cleanup or overwritten state separately from the new demo result.

For `perf`, perform the same checks against the registered `perf` deployment and verify the actual resource allocation and component set rather than inferring them from the command name.

## Failure Handling

Preserve trace IDs and inspect registered state, real processes, listeners, paths, and component health before retrying. A timeout may leave a running remote task; a non-zero exit may follow a partial stop or start. Never use redeploy, destroy, broad restart, or path deletion as generic cleanup.

## Sources

- Official OBD V4.6.0 Command Guide sections 1.1–1.2 and the cluster lifecycle command group.
- Official OBD V4.6.0 Quick Start section 2.
- `ob-deploy` snapshot `4ef23088...`: `_cmd.py` `DemoCommand` and `PrefCommand`; version-matched lifecycle workflows under `workflows/`.
