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
- network listener, firewall, whitelist, download, or other external side effect.

Immediately before a high-impact mutation, state the exact target, observed current state, intended change, impact, rollback or recovery boundary, and validation plan. Bind authorization to those facts. Do not reuse confirmation for a different object or risk class.

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

## Sources

- Official OBD V4.6.0 Command Guide: environment commands and deployment-name examples with interior hyphens.
- [Source-evidence boundary](source-baselines.md#source-evidence-boundary): `_cmd.py` `ObdCommand.init_home` and `_init_log` in the exact inspected checkout.
