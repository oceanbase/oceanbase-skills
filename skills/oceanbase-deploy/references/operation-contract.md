# Operation Contract

Apply this contract to every OceanBase/OBD workflow. Domain references add operation-specific checks; they do not weaken these rules.

## Preserve the Requested Mode

Classify the request before taking action:

- **Explain/review/audit:** read-only analysis of supplied or already available evidence.
- **Diagnose:** bounded read-only inspection first; installation, high-overhead collection, and service changes remain separate.
- **Implement:** mutations limited to the reviewed target and outcome.

Here, read-only means no change to the supplied artifact, installed/controller state, deployment, target host, database, repository, network, or another external object. When a format cannot be inspected in place, a domain workflow may create only a new isolated local scratch directory under the approved workspace or temporary area, copy/extract into it without executing content, and remove only that scratch directory afterward—unless the user required strict zero-write analysis. Record this exception and its cleanup; it does not authorize a download, package installation, repository import, target-host write, or edit to the source artifact.

Do not classify an OBD CLI invocation as strict zero-write merely because the selected operation is inventory. In inspected implementations, ordinary commands initialize `OBD_HOME`, can reconcile version/plugin/workflow/schema state, and create controller trace logs before dispatch. Before `list`, `display`, or another logically read-only OBD query, resolve the exact executable, user, `OBD_HOME`, installed-version relationship, and expected controller-local writes. Disclose and authorize those bookkeeping writes. If the user requires strict zero-write analysis, do not invoke OBD; inspect already available files or output only, or report that live inventory is unresolved.

Authorization for one mode or object does not authorize another. Ask again when new evidence requires a materially broader mutation.

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

Validate every proposed or already registered deployment name before passing it to OBD. For the reviewed V4.6.0 implementation, use the non-interactive safe subset `^[A-Za-z0-9_](?:[A-Za-z0-9_-]*[A-Za-z0-9_])?$`: it permits an interior hyphen, as used by official examples, while rejecting an empty name and a leading or trailing hyphen. Also reject non-ASCII text, whitespace or control characters, shell metacharacters, path separators, dot segments, and absolute paths. Canonicalize the controller metadata root at `OBD_HOME/cluster`, derive the prospective metadata path, and prove it is an immediate child of that root with no symlink traversal before any name-bearing OBD invocation. Stop on an unsafe legacy name rather than inspecting or mutating it through OBD.

Initial shell quoting and `TELEMETRY_MODE=0` do not replace this gate. The reviewed implementation can interpolate the name again into a background shell command before the nested telemetry process reads its mode, and it joins the name directly to controller metadata paths. Permit a broader name syntax only when the selected installed implementation is proved to validate metadata containment and use shell-free argument passing for every downstream invocation.

Deduplicate physical hosts by observed host identity, not only by IP. Normalize paths and detect symbolic links, mount boundaries, overlaps, and non-empty targets before a file-affecting operation. Re-resolve the map whenever the shell, SSH hop, current user, executable, `OBD_HOME`, deployment, target list, or artifact path changes; authorization bound to the former identity does not carry over.

## Minimize Scope

Resolve selectors to explicit objects before execution. Show selected and unselected servers, components, services, tenants, paths, repositories, or storage prefixes. Do not widen a server-, component-, service-, or tenant-scoped request to an entire deployment without explaining why and obtaining authorization for the wider impact.

Both full long options and documented short aliases are allowed in reusable commands when the selected subcommand's installed help confirms their exact mapping. Short options can have different meanings across OBD subcommands, so never transfer an alias from another command. Follow a domain workflow when it requires the long form to avoid a specific ambiguity or safety risk.

## Classify Mutations

Treat these as separate risk classes:

- data destruction or overwrite;
- availability impact, restart, role change, or failover;
- deployment configuration, repository, or artifact replacement;
- persistent host, account, systemd, kernel, limit, or runtime-environment change;
- credential encryption, passkey rotation, secret migration, or exposure change;
- network listener, firewall, whitelist, telemetry, download, or other external side effect.

Immediately before a high-impact mutation, state the exact target, observed current state, intended change, impact, rollback or recovery boundary, and validation plan. Bind authorization to those facts. Do not reuse confirmation for a different object or risk class.

## Protect Credentials and Evidence

Prefer protected interactive input, permission-controlled files, or a version-supported secret reference. If the installed version only accepts a secret through process arguments, disclose that exposure and require an approved local execution method; do not embed the value in the skill or report.

Never “fix” exposure by deleting an entire shell history or unrelated logs. Redact field values in command displays, traces, YAML, URIs, and reports while preserving non-secret identity and error evidence.

## Review Side Effects Before Discovery

Some apparent discovery commands can update repository metadata, download packages, prompt for installation, or persist controller settings. Establish the installed inventory and environment before invoking a dynamic alias. Separate authorization to install a tool from authorization to use it.

## Gate Telemetry and Local Telemetry Logs

Before an OBD command that can submit telemetry, record the installed version, package release and source revision when available, current telemetry submission and telemetry-log settings, applicable organizational policy, expected event categories, network destination when established, local log path, and whether command errors or parameters can enter the report or a child-process argument. The V4.6.0 command guide documents telemetry as enabled by default for `cluster autodeploy`, `deploy`, `start`, `stop`, `reload`, and `upgrade`; inspect the installed dispatch sites rather than assuming this list is exhaustive or unchanged.

Treat telemetry command construction as a fail-closed compatibility gate, separate from telemetry policy. The official OBD V4.6.0 release (`ob-deploy-4.6.0-3`) is known affected: its parent process JSON-encodes an error buffer, interpolates that JSON inside a single-quoted command string, and launches it through a shell. JSON encoding is not shell quoting; an apostrophe or other shell syntax in ordinary plugin, remote-host, path, SQL, or command error text can escape the intended argument. Do not execute any installed path that can dispatch this construction on V4.6.0 or another affected build.

Require an upgrade to a vendor-released fixed OBD build before such a command. This revision does not name a minimum fixed version because no released minimum has been proved; do not invent one. The selected build qualifies only when immutable vendor source or the exact installed implementation proves that both deployment name and telemetry data are passed as an argument vector with no shell (`shell=False` or equivalent), or are transported in-process with arbitrary error text never parsed as command syntax. Record the fixed release/revision and the inspected call path. If either the upgrade or proof is unavailable, stop and offer only non-executable guidance or analysis of already supplied evidence.

`TELEMETRY_MODE=0`, `TELEMETRY_LOG_MODE=0`, sanitizing only the deployment name, or adding outer shell quotes is not a workaround: the affected parent shell parses the constructed command before the nested telemetry process can enforce its mode. Do not patch or replace OBD implicitly; controller update and verification are separate authorized operations.

Only after that command-construction gate passes, preserve the existing telemetry policy by default. If the environment requires no egress or the command can expose unapproved sensitive material and effective redaction cannot be proved, stop before the command. Changing `TELEMETRY_MODE`, `TELEMETRY_LOG_MODE`, or an equivalent value is a separate persistent controller-wide mutation: record the prior presence/value and active tasks, obtain authorization, change only the required key, and restore the exact prior state after the scoped operation unless a persistent policy change was requested. Disabling submission does not prove local logging is disabled, and disabling local logging does not prove submission is disabled.

After the safe-construction gate passes, inspect whether the selected fixed build still launches telemetry posting in a background OBD process and places an error buffer in its payload or child-process arguments. If telemetry was temporarily disabled for policy reasons, do not restore the prior enabled value merely because the parent command returned. First prove that every telemetry child for that command has terminated and that no pending report can submit after restoration; otherwise keep the safer state and report the unresolved controller-wide difference.

## Produce an Execution Record

Before execution, record:

1. the resolved identities and current state;
2. the exact command or API request with secrets redacted;
3. the intended state transition and affected objects;
4. expected persistent and temporary side effects;
5. completion checks and the failure stop condition.

After execution, record observed state rather than merely repeating command output.

## Sources

- Official OBD V4.6.0 Command Guide: environment and telemetry command groups, plus deployment-name examples with interior hyphens.
- [Official public OBD V4.6.0 source baseline](source-baselines.md#official-obd-v460-baseline): `_cmd.py` `ObdCommand.init_home`, `_init_log`, `do_command`, and `ClusterMirrorCommand.background_telemetry_task`; `ssh.py` `LocalClient.execute_command_background`.
