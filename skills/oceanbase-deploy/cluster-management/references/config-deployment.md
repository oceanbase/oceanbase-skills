<!-- Compatibility anchors retained for published 2.x deep links. -->
<a id="config-file-deployment"></a>
<a id="deploy-with-config-file"></a>

# Configuration-File Deployment

Use a reviewed configuration file for reproducible OceanBase Community Edition deployment. This workflow registers a deployment and installs component artifacts; starting it is a separate state transition.

<a id="cluster-operations-after-deployment"></a>
<a id="edit-config"></a>
<a id="reload-config"></a>
<a id="upgrade-component"></a>
<a id="add-delete-component"></a>
<a id="add--delete-component"></a>

## Legacy Operation Links

Published 2.x links for post-deployment operations resolve here. Continue with the matching dedicated workflow:

- `edit-config` or `reload-config`: [edit or reload configuration](configuration-changes.md)
- `upgrade-component`: [upgrade a component](upgrade.md)
- `add-delete-component` or `add--delete-component`: [add or delete components](component-changes.md)

<a id="component-selection"></a>

## Select the Deployment Blueprint

Read the [Community Edition distributed blueprint](deployment-templates/community.md). It is schema-gated and does not claim that fields from one OBD/plugin version are valid in another. Produce an executable YAML only after validating every key against the selected installed plugin.

## Discover the Controller and Existing Cluster

Apply the shared [default controller, SSH, and cluster discovery rule](../../references/operation-contract.md#default-controller-ssh-and-cluster-discovery) before package acquisition or YAML construction. OBD stays on a cluster target host by default, and if every target is proved to have no OBD, install it on the first supplied host with package-manager non-interactive acceptance and without asking. Use the user's supplied SSH login user on every deployment machine; if no login user is specified, use `root`, and if no authentication material is supplied, use passwordless SSH. After login, retain that login-session user for every operation, including OBD ownership and controller-to-node SSH. If passwordless controller-to-node access is absent, directly append the controller login user's public key to the same login user's `authorized_keys` through already-verified access without another prompt.

Do not ask whether the cluster is already deployed or whether the machines are clean. Inspect candidate OBD controllers, all target runtimes, listeners, services, relevant paths, and reachable database identity, then classify the observed state. A new deployment can proceed only after the intended name, paths, ports, and machine identities are proved non-conflicting; a registered, stopped, partial, or unmanaged cluster is discovered state to report and handle through its owning workflow, not a question to delegate back to the user.

## Default Maximum-Utilization Sizing

If the user supplies resource values, a cap, reserve, or a non-maximum profile, preserve that sizing. Otherwise, do not ask the user to choose a deployment size and do not fall back to mini or arbitrary OBD defaults. Select the [maximum-utilization workflow](maximum-utilization.md) and derive the largest verified configuration that fits the resolved target hosts, installed product/plugin behavior, filesystem commitments, and required operational reserves.

This default changes resource sizing only. It does not infer additional hosts, replicas, optional components, tenants, or unneeded persistent host mutations. For a new distributed deployment with multiple user-supplied Observer hosts and no explicit zone mapping, assign each distinct host to a distinct new zone in deterministic host order without asking; preserve any explicit mapping. For multi-node sizing, derive every node's candidate independently and take the minimum across all target nodes separately for each resource key. When a target is shared and safe maximum sizing requires an unknown reserve or cap, inspect existing commitments first and ask only for the missing reserve/cap decision if it cannot be derived; do not ask the user to choose a general deployment profile.

## Default Deployment Base Directory

Apply this default only to a new deployment when the user did not specify the relevant deployment or storage paths. Preserve every explicit user path. Never apply it to an existing registered, stopped, partial, or unmanaged deployment, and never relocate an initialized `home_path`, `data_dir`, `redo_dir`, log path, or other owned path as a repair or optimization.

Resolve the base independently on every target while logged in as the same login-session user that will run OBD and own the deployment:

1. Enumerate canonical mounted filesystems and their available bytes, inode capacity, mount options, quota visible to the login user, persistence, and underlying mount identity. Rank candidates by usable free bytes after known commitments and required reserves—not by directory entry count, `du`, nominal device size, or a remembered path name.
2. Exclude read-only, virtual, pseudo, volatile-memory, package-image, container-overlay, inaccessible, unknown-ownership, symlinked, non-empty deployment, or conflicting filesystems and paths. A network or shared filesystem is eligible only when the selected component and operational model explicitly support it.
3. On each remaining filesystem, resolve a safe canonical parent that the login-session user can read, write, and traverse. In implementation mode, prove those effective permissions with a bounded uniquely named create/remove probe in that parent before rendering YAML. Do not `chmod` or `chown` an existing directory merely to make a larger filesystem win.
4. Select the eligible filesystem with the greatest usable free capacity. On an exact tie, prefer the candidate with greater usable inode capacity, then the lexically first canonical parent for determinism. Do not fall back to the login user's home while a larger eligible filesystem exists, and do not assume that `/data/1`, `/data`, or `/mnt` exists or is largest without inspection.
5. Create one new, empty, non-symlinked, deployment-specific base beneath the selected parent, owned by the login-session user. Resolve component `home_path`, `data_dir`, `redo_dir`, log, cache, and temporary deployment-owned paths beneath that base as the installed schema and component layout permit. When the schema supports host-specific paths, retain each host's independently selected base; when it requires one common path string, use a path that is eligible on every target and record that constraint.

Record the selected canonical base, filesystem, usable free bytes, ownership, mode, quota, and rejected larger candidates for each host. If no eligible persistent parent has enough capacity for the verified deployment commitments, stop and request a path or permission decision instead of silently using a smaller or unwritable location.

## Database Bootstrap Password Default

For a new OceanBase cluster, default every OBD-generated database bootstrap credential—especially the initial `root`/`sys` password—to OBD ownership. Unless the user explicitly supplied an override, do not ask for a password, generate one in the agent, or render the password key with an empty, null, placeholder, or guessed value. Prove that the installed deployment workflow generates a random value when the field is absent, then omit that field from the source YAML and let OBD materialize and retain the credential through its normal controller configuration path, treating that path as secret-bearing evidence.

When the user explicitly supplies an override, preserve that choice and pass it only through the approved protected local procedure; do not replace it with an OBD-generated value. If the installed build cannot prove the required random-generation path, report that version limitation instead of asking the user to invent a password or silently creating an empty-password database.

After deployment, verify without displaying the value that OBD generated or retained a non-empty credential, the controlling metadata/configuration has appropriate ownership and permissions, and an authenticated identity query succeeds. This default applies only to new-cluster database bootstrap credentials that the installed OBD workflow owns; it does not fabricate SSH, existing-database, tenant-create, storage, KMS, or external-service credentials.

## Static Component Inspection

When the user says “static analysis only,” “do not deploy,” or equivalent, treat that as a hard boundary. Inspect only supplied/local package metadata and file lists, an installed read-only OBD/plugin tree, and source/configuration artifacts. If extraction is necessary, use a new isolated temporary directory and record the artifact path and checksum.

By default, this static boundary permits only that isolated local scratch write; it keeps the inspected artifact, installed tree, controller state, target hosts, and deployments read-only. If the user explicitly requires strict zero-write analysis, do not extract or create temporary files. Report any conclusion that would require extraction as unresolved instead.

Do not install/uninstall a package, mutate a mirror or repository, register a deployment, run any deploy/start/component/lifecycle/plugin workflow, connect to a live database, or change a target host merely to test a prediction. Never execute extracted plugin, pre/post-install, bootstrap, start, or cleanup code. If a branch depends on runtime state, report it as conditional or unknown.

Classify the report explicitly:

1. **Packaged files** present before deployment.
2. **Controller metadata** OBD would maintain locally.
3. **Deploy-time target paths** an inspected workflow explicitly creates or copies.
4. **Runtime-conditional paths** created only after start or when an option is enabled.
5. **Unknown/not established statically** behavior requiring supported runtime or authoritative version-matched evidence.

Identify host role, owner when derivable, persistence/cleanup boundary, and evidence source for every path or effect. Remove only the isolated extraction directory created for this inspection, then verify that no deployment, process, listener, repository entry, service unit, or target-host path was created. Report the result as static, never deployment-tested.

## Build the Deployment Manifest

Before resolving artifacts, expand the selected topology through the shared [deployment package closure](../../references/deployment-package-sets.md). Record primary component packages, companion runtime packages, selected conditional utilities, image archives, and external prerequisites separately. The YAML component list alone is not the package closure.

Record these inputs before downloading artifacts or writing YAML:

| Area | Required inputs |
|---|---|
| Controller | host, user, exact OBD executable/build, `OBD_HOME`, active tasks |
| Product | exact Community Edition component key and component/plugin version |
| Artifacts | component, version, release, operating-system suffix when applicable, architecture, hash, source, dependency closure |
| Topology | deployment name, app/cluster identity, zones, server-to-component mapping |
| SSH | target machine identity, management IP, SSH user/port/key and privilege boundary |
| Paths | explicit user paths, or each host's verified largest writable persistent deployment base and the canonical home, data, log, redo, cache, and temporary paths beneath it |
| Network | management, SQL, RPC, obshell, proxy, monitoring, and component-specific addresses/ports |
| Resources | CPU, memory, disk, inode, filesystem/mount, cgroup/container limits, and headroom; explicit user sizing when supplied, otherwise the verified maximum-utilization derivation |
| Optional scope | requested OBProxy, OBAgent, monitoring, or Config Server |
| Database bootstrap credential | OBD-generated by default; protected user override only when explicitly supplied |
| Other secrets | approved protected input source and redaction plan; never literal reusable values |

Every component in the manifest must map to a requested outcome or a proved package/plugin dependency. A repository listing or old YAML is not permission to deploy all contained components or create a tenant.

## Preflight

1. Immediately after each bounded login and before invoking OBD or performing any other deployment preflight, apply the shared [highest-priority OBD privilege gate](../../references/operation-contract.md#highest-priority-obd-privilege-gate). Every required machine's login-session user must be root or pass `sudo -n true`; otherwise stop the whole workflow and ask the user to switch users or configure usable sudo.
2. Read `obd --version`, the selected `obd cluster deploy --help`, and the installed public component schema/validation surface. Inspect a packaged workflow only when those interfaces cannot establish an execution-critical behavior.
3. Confirm exactly one compatible artifact for every required entry in the expanded deployment package closure, not only every YAML component. Record version, release, operating-system suffix, architecture, hash, and repository source; repository presence alone does not prove compatibility. Apply the shared exact-suffix, EL8, then EL7 fallback and the [fixed mirror-source order](../../obd-administration/references/mirror-and-repositories.md#fixed-online-package-source-order), and verify every fallback's runtime dependencies.
4. Prove each target's hostname/machine identity, management address, OS, architecture, runtime libraries, time synchronization, routes, firewall boundary, and SSH behavior. Record the successful login-session user with `id -un`, retain it as the OBD and host-operation user, and complete the shared bounded passwordless bootstrap from that controller user to the same user on every target without a separate permission prompt when access is absent.
5. Resolve every path canonically. When paths were omitted for a new deployment, first apply the default deployment-base selection above under the login-session user. Inspect owner, effective read/write/traverse access, mode, free space, inode capacity, mount identity, quota, symlinks, non-empty contents, overlap with other deployments, and cleanup ownership.
6. Map every proposed port to its host and namespace. Check real listeners and processes, not only registered deployments.
7. Check available CPU, memory, log/data capacity, cgroup/container constraints, and topology failure domains. Do not infer usable resources from host totals alone. When the user supplied no sizing, complete the maximum-utilization workflow before rendering resource values.
8. Determine existing cluster state yourself by correlating OBD registrations with remote package/service records, processes, listeners, deployment paths, and SQL/obshell identity when reachable. The deployment name, app identity, paths, and ports must not collide with an existing, stopped, partial, or unmanaged service. Do not ask the user whether deployment already happened in place of these checks.
9. Run only the public version-supported precheck/strict-check path. In reusable deployment instructions spell `--strict-check` in full when the installed command exposes it; never transfer the short option `-S` from another subcommand.

<a id="host-environment-initialization"></a>

### Initialize the Host Environment Before Deployment

Do not wait for `deploy`, `start`, or integrated `autodeploy` to fail before preparing the targets. Read the installed help and run the narrow public OBD host-environment path supported by that build for every target under the same user and login mechanism the deployment will use. The bounded new-deployment capability family includes `obd host precheck`, `obd host user init`, and `obd host init`. Do not invent syntax or run every initializer indiscriminately: start with the public precheck, apply the supported user-limit or host-environment initializer that owns the reported findings, then repeat the precheck. This narrow deployment preflight does not restore the separately unsupported `cluster init4env` or general-purpose host-administration workflows.

If an initializer prompts, use the real-PTY rules in [automation execution](../../references/automation-execution.md), not an ordinary input pipe. Record every affected node and setting. Derive required and recommended values from the installed OBD/plugin output rather than hard-coding one test run's thresholds. Verify current kernel values directly, verify their persistent configuration, and establish a new SSH/login session as the deployment user before accepting PAM limits such as `nofile` or `nproc`; an old shell does not prove the persisted limit. Complete this flow before an integrated `autodeploy`, because that command can register or initialize deployment state before a later environment/start check fails.

If the installed public initializer is unavailable or reaches a proved failure, use manual remediation only for the exact reported setting and documented value. Preserve the prior value and persistence owner, apply the narrow equivalent change on every affected target, open a fresh deployment-user session when required, and rerun the public precheck. Do not replace this with broad guessed `sysctl`, limits, firewall, SELinux, repository, or path changes.

Declare the package-resolution mode before execution. In online mode, select the effective artifact source before the mechanism, prove the exact expected remote winner and final package URL, and retain source, mechanism, and attempt evidence for each exhausted source; do not require a local download when an enabled repository is proved to resolve the right source and candidate. If one online mechanism fails, keep the current source while trying another applicable controller-local `curl`, `wget`, package-manager, or OBD path. If an explicit download or bounded relay obtains the exact artifact, switch the complete closure to local-package mode. In a remote workflow, `local-package` and `local closure` mean controller-local, not relay- or runner-local. In local-package mode, prove the complete local closure, disable participating remote repositories through the reviewed mirror workflow, immediately verify their disabled state and the local winning hashes, and keep that isolation through the final package-selecting stage. Stop rather than allowing unresolved local/remote competition. Restore a temporary remote-mirror change after the workflow unless persistent disablement was separately requested.

Stop when the plugin schema, artifact closure, compatibility, host identity, path ownership, or topology cannot be proved. Do not use `--force` or path deletion as a preflight workaround.

## Render and Review YAML

Render values from the approved manifest and selected plugin schema. For every field, record whether it is required by the schema, derived by the plugin, or explicitly chosen by the user.

Review the rendered file semantically:

- exact component keys and dependency relationships;
- server and zone identity, management versus service addresses;
- canonical per-server paths and ports;
- version/release constraints and the separately locked artifact hashes;
- resource values and units;
- the database bootstrap-password field absent unless the user explicitly supplied an override, and every displayed credential value redacted;
- no unrequested component stanza, tenant creation, or cleanup behavior.

A syntactically valid YAML is not enough. For an executable plan, use the installed OBD/plugin parsing and precheck path; do not install or start a component merely to discover whether a key exists. In static-review mode, do not invoke OBD parsing, plugin precheck, or any workflow: report schema/runtime validation as not performed and keep every unsupported conclusion conditional.

Keep unrequested persistent startup behavior absent from the rendered configuration.

<a id="storage-initialization-invariants"></a>

### Preserve the Initialized Storage Topology

Treat `home_path`, `data_dir`, and `redo_dir` as initialization-time storage topology, not ordinary retry knobs. Before deployment, retain their canonical parent paths, mount identities, expected ownership, and empty-state evidence. After the deploy stage initializes the component and before a separate start, compare the registered configuration and deploy trace with the actual version-matched layout: resolve `home_path/store`, the data path and its `sstable` path, the `clog` and `slog` paths, every symlink target, owner, mode, and filesystem. A custom data or redo path is supported when the selected schema/plugin accepts it; its existence is not a reason to remove it.

Changing or deleting a registered storage-path value after deploy does not prove that OBD will rerun initialization or migrate the existing layout during start. Do not remove custom `data_dir` or `redo_dir`, replace initialized symlinks, delete an empty-looking `store`, or manually create `store/{clog,slog,sstable}` as a generic way around a start error. If the storage topology differs from the deploy-time configuration, preserve both states and use the [failed-initial-start recovery](../../references/failure-recovery-and-evidence.md#failed-initial-start-and-storage-topology) before another command.

## Execute

Use the syntax confirmed by the installed command help:

```bash
obd cluster deploy <deploy_name> --config=<reviewed_config.yaml>
obd cluster start <deploy_name> --strict-check
```

When this workflow is entered from an intentionally created `configured` registration, use the stored configuration only after revalidating its parsed semantics and checksum against the approved candidate. If the installed help supports deployment from a registered configuration, use `obd cluster deploy <deploy_name>` without `--config`; do not replace or silently accept different stored content. Keep `start` separate and invoke it only after deployment acceptance.

Use `--strict-check` only when the installed `cluster start --help` exposes it; OBD V4.6.0 documents it on start, not deploy. Preserve the configuration checksum and trace ID for each command. After `deploy`, establish what was registered, copied, installed, or initialized and verify the [initialized storage topology](#storage-initialization-invariants) before deciding whether `start` is safe. Do not blindly issue `start` after a partial deploy.

### Maximum-Utilization Autodeploy

The retained maximum-utilization workflow uses `autodeploy` as an integrated configuration-generation, deployment, and startup path. Use it only through [maximum-utilization.md](maximum-utilization.md), after completing host-environment initialization and checking name/path/port collisions, complete package closure, generated defaults, and all three transitions.

Keep optional destructive or convenience branches absent. Do not add `--force`, `--clean`, `--force-delete`, or `--auto-create-tenant`. Preserve the generated and registered configuration, and verify the same deployment, runtime, topology, SQL, and resource outcomes required for a configuration-file deployment.

### Maximum-Utilization Default

Use the maximum-utilization workflow when the user explicitly requests it or when a new-cluster request omits resource sizing. An explicit user resource plan or non-maximum profile overrides this default. Read and follow [maximum-utilization.md](maximum-utilization.md). It preserves deterministic per-node candidate calculation, per-key minima across all nodes, 8-core behavior, disk commitment checks, explicit common resource keys, and post-deployment equality checks. “Use all resources” never means zero safety reserve.

## Accept or Recover

Verify the registered component manifest and actual installed artifact identity, every selected process/listener/path, OceanBase topology and server state through SQL, authenticated SQL readiness using the protected OBD-generated or user-supplied credential, and relevant optional-component data planes. Confirm that unselected services were not added and no unexplained partial registration or path remains.

On failure, preserve the trace, registered configuration, generated files, remote processes, listeners, paths, and artifact state. Classify the stage before continuing. Do not delete the registered deployment, remove directories, or retry until the shared failure-recovery rules identify the safe next action.
