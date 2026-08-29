# Cluster Lifecycle

Use this workflow for display, start, stop, restart, destroy, and prune. Refresh deployment and real runtime state immediately before every mutation.

## Resolve the Target

Record the controller, deployment, product form, component/plugin and artifact identities, registered servers, paths, ports, current OBD status, actual processes/listeners, SQL/API health, active tasks, tenants, backups, and external dependants.

Read the exact selected subcommand help. If server, component, or service selectors are available, resolve them to an explicit target list and show selected and unselected objects. Short options are command-scoped; prefer long names and never reuse `-S` from a deployment example in another command.

## List and Display

Preserve the ordinary logical-inventory path before choosing a lifecycle mutation:

```bash
obd cluster list
obd cluster display <deploy_name>
```

Confirm these forms with the installed help. They can initialize or reconcile controller-local `OBD_HOME` state and write a trace; treat that as ordinary CLI bookkeeping unless the user explicitly requires strict zero-write inspection. Their output describes controller registration and reported status, not proof that every process, listener, dependency, or data plane is healthy. For a status-only request, stop after the requested inventory unless the user separately asks for diagnosis or a state change.

## Start, Stop, and Restart

Before start, establish whether the deployment is fully installed or partially initialized, whether ports and paths remain owned by it, and whether dependencies are ready. Before stop/restart, identify application routing, active workload, replication/management relationships, and the acceptable outage.

For unattended execution or measured availability, read [non-interactive automation execution](../../references/automation-execution.md). Record command events separately from the last successful authenticated probe, listener loss, expected PID transition, listener recovery, and first successful authenticated probe; command duration is not database downtime.

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

## Destroy and Prune

Read [cleanup and ownership boundaries](../../references/cleanup-boundaries.md) before defining either removal set. Destroying runtime/data state and pruning controller metadata are separate operations.

`destroy` can stop services and delete deployment-owned data. Before requesting confirmation, show:

- exact deployment/component/server identity;
- all canonical home, data, log, and external paths and their ownership;
- tenants, backup state, replication, monitoring, and client dependencies;
- what the installed destroy workflow removes and retains;
- recovery boundary and separately owned data that must remain.

Obtain destructive authorization immediately before the exact command. Do not add an ignore, force, or standby-bypass option automatically.

Before launching `destroy`, establish whether the caller has a controllable TTY. In a non-interactive runner, use only a public command-local confirmation form whose installed help and observed semantics prove that it acknowledges this exact prompt without widening deletion, forcing process termination, or changing standby behavior. Otherwise require a real PTY; an ordinary input pipe is not an interactive-session substitute. Do not enable controller-wide automatic confirmation, pipe generic `yes`, or substitute a force option. If neither safe form exists, stop before launch.

If an earlier invocation is already waiting for confirmation, identify its caller-owned PID and children and determine whether destruction began. Interrupt only that waiting invocation through its caller/session boundary, then reconcile registration, tasks, processes, listeners, and paths before another attempt; do not leave it running or assume that terminating the client rolled back server-side work.

After that authorization, preserve the installed public command shape:

```bash
obd cluster destroy <deploy_name>
```

After destroy, report independently whether deployment-owned processes/listeners/data paths were removed; empty deployment parent directories remain; OBD registration/configuration and traces remain; local mirror/package repositories remain; and any unexpected process, listener, data, unit, task, or reference remains. Expected controller evidence or an empty parent directory is not a failed data-destruction result, and destroy does not authorize `prune-config` or repository cleanup.

Use `prune-config` only after proving the deployment is in a version-supported metadata-only state and inspecting what the installed command removes. Inspected implementations allow `destroyed` or `configured`; do not use it for a deployed or running state. Permission to destroy does not authorize metadata pruning. Verify absence of the exact authorized objects and preservation of unrelated deployments and paths.

```bash
obd cluster prune-config <deploy_name>
```

Ordinary test cleanup does not prune controller metadata by default. If the user explicitly requests complete removal of this run's unique named deployment and the displayed removal set includes both runtime/data destruction and controller registration, that exact authorization may cover the staged `destroy` followed by `prune-config`; do not treat the default separation as a prohibition. After destroy, re-prove an eligible metadata-only state, confirm the exact deployment name through the PTY/confirmation rules above, prune only that registration, and verify all unrelated deployments remain. “Complete removal” of a deployment does not implicitly include mirror packages, repository definitions, the OBD installation, external storage, or unrelated traces unless those objects were separately enumerated and authorized.

## Failure Handling

Preserve trace IDs and inspect registered state, real processes, listeners, paths, and component health before retrying. A caller timeout may leave a running OBD process or remote task; reconcile it as succeeded, failed, still running, or unknown before another invocation. A non-zero exit may follow a partial stop or start. Never use destroy, broad restart, or path deletion as generic cleanup.

## Sources

- Official OBD V4.6.0 Command Guide sections 1.1–1.2 and the cluster lifecycle command group.
- Version-matched lifecycle workflows under `workflows/` in the exact inspected checkout, bounded by the [source-evidence rule](../../references/source-baselines.md#source-evidence-boundary).
