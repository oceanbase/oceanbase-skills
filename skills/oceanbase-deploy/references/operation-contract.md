# Operation Contract

Apply this contract to every OceanBase/OBD workflow. Domain references add operation-specific checks; they do not weaken these rules.

## Preserve the Requested Mode

Classify the request before taking action:

- **Explain/review/audit:** read-only analysis of supplied or already available evidence.
- **Diagnose:** bounded read-only inspection first; installation, high-overhead collection, and service changes remain separate.
- **Implement:** mutations limited to the reviewed target and outcome.

Here, read-only means no change to the supplied artifact, installed/controller state, deployment, target host, database, repository, network, or another external object. When a format cannot be inspected in place, a domain workflow may create only a new isolated local scratch directory under the approved workspace or temporary area, copy/extract into it without executing content, and remove only that scratch directory afterward—unless the user required strict zero-write analysis. Record this exception and its cleanup; it does not authorize a download, package installation, repository import, target-host write, or edit to the source artifact.

An OBD inventory command can initialize `OBD_HOME` and write controller-local traces. Treat those as ordinary CLI bookkeeping for a requested live inventory. If the user explicitly requires strict zero-write analysis, inspect already available files or output instead of invoking OBD.

Authorization for one mode or object does not authorize another. Ask again when new evidence requires a materially broader mutation.

## Default Consent for In-Scope Persistent Changes

An explicit request to execute a non-destructive workflow authorizes the ordinary persistent configuration, package, repository, host-setting, and service-state changes that are necessary and intrinsic to that requested outcome after their exact targets have been resolved. Record those effects and verify them, but do not ask for a second confirmation merely because they persist across process exit or reboot.

This default does not activate optional persistent features the user did not request, widen the target set, or authorize destroy, prune, drop, overwrite, forced operation, failover, secret exposure, unrelated cleanup, or a materially different recovery action. Those remain separate operations under their own boundaries.

## Resolve Every Identity

Build an identity map appropriate to the task:

| Layer | Record |
|---|---|
| Orchestration origin | local workstation or automation runner, current directory, session/SSH hop, and approved artifact source/destination |
| Controller | host, user, executable, OBD version, `OBD_HOME`, active tasks |
| Target host | management address, hostname/machine identity, SSH user/port, OS and architecture |
| Deployment | OBD deployment name, product form, app/cluster identity, current state |
| Component | exact component key, version, release, architecture, artifact hash, plugin |
| Runtime target | server, zone, service/process, paths, ports, unit or container identity |
| Data target | tenant, backup set, SCN/time, repository object, storage prefix, or credential set |

Use the exact registered name for an existing deployment and follow the installed command's documented naming rules for a new one. Do not rewrite a legacy name or construct controller metadata paths manually.

Deduplicate physical hosts by observed host identity, not only by IP. Normalize paths and detect symbolic links, mount boundaries, overlaps, and non-empty targets before a file-affecting operation. Re-resolve the map whenever the shell, SSH hop, current user, executable, `OBD_HOME`, deployment, target list, or artifact path changes; authorization bound to the former identity does not carry over.

### Default Controller, SSH, and Cluster Discovery

For an OBD-based cluster deployment, preserve the user's target-host order. Unless the user explicitly selected a separate controller, the controller must be one of those cluster deployment hosts. Before choosing or installing it, inspect every reachable target for `obd` executables, package-manager ownership, candidate controller homes under the unchanged login environment, registered deployments, and active tasks. Prefer the target host whose registration identifies the intended deployment. If there is no such registration, reuse an otherwise unambiguous usable OBD installation on a target host. If multiple target hosts remain plausible controllers with conflicting or unrelated state, present the observed ambiguity and ask only after completing the safe inspection.

Only when every supplied cluster host has been reached and confirmed to contain no OBD executable, package record, controller metadata, or registration may the workflow select the first supplied host and install OBD there without asking. This default applies to configuration-file and maximum-utilization autodeploy workflows with either online repositories or local packages. Do not install or run OBD on the automation runner as a fallback. A host that is unreachable has not been confirmed empty.

For each target where the user supplied neither an SSH user nor an SSH password, first attempt bounded, non-interactive passwordless SSH as `root`, using only the runner's existing key or agent and disabling password prompts. Do not ask for credentials before this attempt. If it fails, record whether the failure was name resolution, route, timeout, host-key, authentication, or remote execution, then ask the user for the missing or corrected access information for that host. Do not guess alternate users, passwords, private keys, privilege escalation, or tunnels. When the user supplied an SSH user, preserve it; when the user supplied authentication material, use only its approved protected path.

A deployment request includes read-only discovery needed to determine existing state. Do not ask the user whether the cluster is deployed, whether a host is clean, or which target owns it before checking. Correlate candidate-controller registrations and deployment status with target-host package/service records, processes, listeners, expected or discovered deployment directories, and SQL/obshell identity when safely reachable. No single missing layer proves absence: an unregistered runtime can be unmanaged, a registered deployment can be stopped, and stopped processes can leave deployment data. Classify the result as registered and running, registered and stopped/partial, unmanaged or conflicting, or absent. Ask the user only for failed access or a material identity/ownership decision that remains after those observations; ask for that missing decision, not for facts the workflow can inspect.

### Resolve the Controller Home Without Guessing

Start from the caller's actual environment and record whether `OBD_HOME` is unset or explicitly configured. Correlate the exact executable and controller user with public inventory, registered deployment metadata, and trace locations under that unchanged environment before naming the controlling home.

Do not export a path merely because it looks like the default metadata directory. For example, observing `/root/.obd` does not justify setting `OBD_HOME=/root/.obd`; an installed build can derive another `.obd` child and resolve `/root/.obd/.obd`. Set or replace `OBD_HOME` only when the user, runner configuration, or proved existing controller identity requires it. After an explicit setting, verify the resolved registration and trace location and stop on an unexpected nested suffix, empty deployment inventory, ownership mismatch, or competing controller home.

Keep the resolved environment unchanged for every command and trace that belongs to one operation. Re-resolve it after an SSH hop, user or executable change, or automation-worker handoff; never switch homes merely to find a missing deployment or trace.

## Keep Remote Execution Identities Stable

For a workflow that manages remote hosts, distinguish the automation runner or workstation from the OBD controller, artifact-acquisition host, and managed hosts. For cluster deployment, select the controller through the target-host discovery rule above; for another remote workflow, select an approved remote host. Install and run OBD there. Keep its `OBD_HOME`, deployment metadata, traces, package resolution, and lifecycle commands on that controller unless the user explicitly chooses a different control-plane location. The runner is transport and evidence-capture infrastructure by default, not an implicit fallback controller.

In a remote workflow, an unqualified **local repository**, **local package**, **local path**, or **local download** means controller-local. Do not reinterpret it as runner-local merely because a network, proxy, repository, or package command failed.

Do not silently change the controller or execution host after a failure. For online packages from the OceanBase public repositories, the fixed [mirror-source workflow](../obd-administration/references/mirror-and-repositories.md#fixed-online-package-source-order) takes precedence over generic connectivity diagnosis: make the first actual request to `https://mirrors.oceanbase.com`, remain on that source for up to three meaningful attempts, then use the direct package directories under `https://mirrors.aliyun.com/oceanbase`. After a normal OBD/repository fetch fails, vary the controller-local mechanism with `curl`, `wget`, the operating-system package manager, or another applicable downloader instead of repeating only the same path. Verify and import/register the exact artifact locally before retrying. Never use `obd mirror` as a network downloader.

Only after the complete controller-local suffix-by-source-and-mechanism matrix is exhausted may another reachable host become a bounded checksummed artifact relay for the same exact artifact from the same ordered sources. The relay must transfer the artifact to the existing controller for verification and local import/install; it does not become the controller and must not run OBD or the requested operation. Ask the user only after that relay also fails, or before introducing an unlisted source or different controller.

For non-package transfers, make bounded, meaningful attempts through applicable existing or user-approved routes on the same controller and preserve evidence for each route rather than blindly repeating one request. A user-approved relay may acquire, verify, and transfer an exact artifact; it does not move OBD or its metadata off the remote controller unless the user separately and explicitly changes that requirement.

## Minimize Scope

Resolve selectors to explicit objects before execution. Show selected and unselected servers, components, services, tenants, paths, repositories, or storage prefixes. Do not widen a server-, component-, service-, or tenant-scoped request to an entire deployment without explaining why and obtaining authorization for the wider impact.

Both full long options and documented short aliases are allowed in reusable commands when the selected subcommand's installed help confirms their exact mapping. Short options can have different meanings across OBD subcommands, so never transfer an alias from another command. Follow a domain workflow when it requires the long form to avoid a specific ambiguity or safety risk.

## Classify Mutations

Treat these as separate risk classes:

- data destruction or overwrite;
- availability impact, restart, role change, or failover;
- deployment configuration, repository, or artifact replacement;
- persistent host, account, systemd, kernel, limit, or runtime-environment change;
- secret exposure or replacement;
- network listener, firewall, whitelist, download, or other external side effect.

Immediately before a high-impact mutation, state the exact target, observed current state, intended change, impact, rollback or recovery boundary, and validation plan. For a requested non-destructive workflow, this record does not trigger duplicate confirmation for its intrinsic persistent changes. Obtain new authorization only when the action is destructive, forced, materially broader than the request, or belongs to another risk class that the request did not cover.

## Protect Credentials and Evidence

Prefer protected interactive input, permission-controlled files, or a version-supported secret reference. If the installed version only accepts a secret through process arguments, disclose that exposure and require an approved local execution method; do not embed the value in the skill or report.

Never “fix” exposure by deleting an entire shell history or unrelated logs. Redact field values in command displays, traces, YAML, URIs, and reports while preserving non-secret identity and error evidence.

## Account for Discovery Side Effects

Some discovery commands can update repository metadata, download packages, prompt for installation, or persist controller settings. Use the installed command's normal inventory/help path, record any resulting setup or package change, and surface a material side effect before proceeding when it falls outside the requested task. Tool setup does not by itself broaden the authorized diagnostic or operational target.

## Produce an Execution Record

Before execution, record:

1. the resolved identities and current state;
2. the exact command or API request with secrets redacted;
3. the intended state transition and affected objects;
4. expected persistent and temporary side effects;
5. completion checks and the failure stop condition.

After execution, record observed state rather than merely repeating command output.

For unattended or multi-stage work, read [non-interactive automation execution](automation-execution.md) before the first command and use its runtime preflight, prompt handling, structured event record, and timeout-reconciliation rules.

## Sources

- Official OBD V4.6.0 Command Guide: environment commands and deployment-name examples with interior hyphens.
- [Source-evidence boundary](source-baselines.md#source-evidence-boundary): `_cmd.py` `ObdCommand.init_home` and `_init_log` in the exact inspected checkout.
