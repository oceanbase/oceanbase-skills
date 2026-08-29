<!-- Compatibility anchors retained for published 2.x deep links. -->
<a id="config-file-deployment"></a>
<a id="deploy-with-config-file"></a>

# Configuration-File Deployment

Use a reviewed configuration file for reproducible community or commercial OceanBase deployment. This workflow registers a deployment and installs component artifacts; starting it is a separate state transition.

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

## Select the Product Blueprint

Resolve the product form before writing YAML, then read exactly one blueprint:

- [Community distributed](deployment-templates/community.md)
- [Commercial distributed](deployment-templates/commercial-distributed.md)
- [Commercial standalone or centralized](deployment-templates/commercial-standalone.md)

The blueprints are intentionally schema-gated. They identify required decisions and configuration structure without claiming that fields from one OBD/plugin version are valid in another. Produce an executable YAML only after validating every key against the selected installed plugin.

## Discover the Controller and Existing Cluster

Apply the shared [default controller, SSH, and cluster discovery rule](../../references/operation-contract.md#default-controller-ssh-and-cluster-discovery) before package acquisition or YAML construction. This rule is identical for configuration-file, interactive, autodeploy, demo, and perf workflows: OBD stays on a cluster target host by default, and if every target is proved to have no OBD, install it on the first supplied host without asking. When both SSH user and password are absent, try passwordless `root` first and ask only after that attempt fails.

Do not ask whether the cluster is already deployed or whether the machines are clean. Inspect candidate OBD controllers, all target runtimes, listeners, services, relevant paths, and reachable database identity, then classify the observed state. A new deployment can proceed only after the intended name, paths, ports, and machine identities are proved non-conflicting; a registered, stopped, partial, or unmanaged cluster is discovered state to report and handle through its owning workflow, not a question to delegate back to the user.

## Default Maximum-Utilization Sizing

If the user supplies resource values, a cap, reserve, or a non-maximum profile, preserve that sizing. Otherwise, do not ask the user to choose a deployment size and do not fall back to mini, demonstration, or arbitrary OBD defaults. Select the [maximum-utilization workflow](maximum-utilization.md) and derive the largest verified configuration that fits the resolved target hosts, installed product/plugin behavior, filesystem commitments, and required operational reserves.

This default changes resource sizing only. It does not infer additional hosts, replicas, optional components, tenants, or unneeded persistent host mutations. For a new distributed deployment with multiple user-supplied Observer hosts and no explicit zone mapping, assign each distinct host to a distinct new zone in deterministic host order without asking; preserve any explicit mapping. For multi-node sizing, derive every node's candidate independently and take the minimum across all target nodes separately for each resource key. When a target is shared and safe maximum sizing requires an unknown reserve or cap, inspect existing commitments first and ask only for the missing reserve/cap decision if it cannot be derived; do not ask the user to choose a general deployment profile.

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
| Product | product form, exact component key, component/plugin version |
| Artifacts | component, version, release, operating-system suffix when applicable, architecture, hash, source, dependency closure |
| Topology | deployment name, app/cluster identity, zones, server-to-component mapping |
| SSH | target machine identity, management IP, SSH user/port/key and privilege boundary |
| Paths | canonical home, data, log, redo, cache, temporary, and shared-storage paths as applicable |
| Network | management, SQL, RPC, obshell, proxy, monitoring, OCP, and component-specific addresses/ports |
| Resources | CPU, memory, disk, inode, filesystem/mount, cgroup/container limits, and headroom; explicit user sizing when supplied, otherwise the verified maximum-utilization derivation |
| Persistent host behavior | explicit auto-start decision; keep it disabled/unset unless requested and approved through the lifecycle systemd gate |
| Optional scope | requested OBProxy, OBAgent, monitoring, OCP, Config Server, `oceanbase.ai`, `oblogservice`, or shared storage |
| Database bootstrap credential | OBD-generated by default; protected user override only when explicitly supplied |
| Other secrets | approved protected input source and redaction plan; never literal reusable values |

Every component in the manifest must map to a requested outcome or a proved package/plugin dependency. A demo, repository listing, all-in-one bundle, or old YAML is not permission to deploy all contained components or create a tenant.

## Preflight

1. Read `obd --version`, the selected `obd cluster deploy --help`, and the installed public component schema/validation surface. Inspect a packaged workflow only when those interfaces cannot establish an execution-critical behavior.
2. Confirm exactly one compatible artifact for every required entry in the expanded deployment package closure, not only every YAML component. Record version, release, operating-system suffix, architecture, hash, and repository source; repository presence alone does not prove compatibility. Apply the shared exact-suffix, EL8, then EL7 fallback and the [fixed mirror-source order](../../obd-administration/references/mirror-and-repositories.md#fixed-online-package-source-order), and verify every fallback's runtime dependencies.
3. Prove each target's hostname/machine identity, management address, OS, architecture, runtime libraries, time synchronization, routes, firewall boundary, and SSH behavior. Apply the default passwordless-`root` attempt when the user omitted both SSH user and password; do not preemptively ask for credentials.
4. Resolve every path canonically. Inspect owner, mode, free space, inode capacity, mount identity, symlinks, non-empty contents, overlap with other deployments, and cleanup ownership.
5. Map every proposed port to its host and namespace. Check real listeners and processes, not only registered deployments.
6. Check available CPU, memory, log/data capacity, cgroup/container constraints, and topology failure domains. Do not infer usable resources from host totals alone. When the user supplied no sizing, complete the maximum-utilization workflow before rendering resource values.
7. Determine existing cluster state yourself by correlating OBD registrations with remote package/service records, processes, listeners, deployment paths, and SQL/obshell identity when reachable. The deployment name, app identity, paths, and ports must not collide with an existing, stopped, partial, or unmanaged service. Do not ask the user whether deployment already happened in place of these checks.
8. Run only the public version-supported precheck/strict-check path. In reusable deployment instructions spell `--strict-check` in full when the installed command exposes it; never transfer the short option `-S` from another subcommand.

Declare the package-resolution mode before execution. In online mode, prove the exact expected remote winner and retain the source, mechanism, and attempt evidence for each exhausted mirror source; do not require a local download before the first normal online attempt. If online fetch fails but controller-local `curl`, `wget`, the package manager, another applicable downloader, or the bounded relay obtains the exact artifact, switch the complete closure to local-package mode. In a remote workflow, `local-package` and `local closure` mean controller-local, not relay- or runner-local. In local-package mode, prove the complete local closure, disable participating remote repositories through the reviewed mirror workflow, immediately verify their disabled state and the local winning hashes, and keep that isolation through the final package-selecting stage. Stop rather than allowing unresolved local/remote competition. Restore a temporary remote-mirror change after the workflow unless persistent disablement was separately requested.

Stop when the plugin schema, artifact closure, product compatibility, host identity, path ownership, or topology cannot be proved. Do not use `--force`, `redeploy`, path deletion, `init4env`, or a community package as a preflight workaround.

## Render and Review YAML

Render values from the approved manifest and selected plugin schema. For every field, record whether it is required by the schema, derived by the plugin, or explicitly chosen by the user.

Review the rendered file semantically:

- exact product/component keys and dependency relationships;
- server and zone identity, management versus service addresses;
- canonical per-server paths and ports;
- version/release constraints and the separately locked artifact hashes;
- resource values and units;
- the database bootstrap-password field absent unless the user explicitly supplied an override, and every displayed credential value redacted;
- no unrequested component stanza, tenant creation, auto-start, telemetry change, or cleanup behavior.

A syntactically valid YAML is not enough. For an executable plan, use the installed OBD/plugin parsing and precheck path; do not install or start a component merely to discover whether a key exists. In static-review mode, do not invoke OBD parsing, plugin precheck, or any workflow: report schema/runtime validation as not performed and keep every unsupported conclusion conditional.

Keep `enable_auto_start` or an equivalent plugin option false or unset unless persistent startup was explicitly requested. If proposed, read the [automatic-startup and systemd gate](lifecycle.md#automatic-startup-and-systemd) before rendering or executing the configuration.

## Execute

Use the syntax confirmed by the installed command help:

```bash
obd cluster deploy <deploy_name> --config=<reviewed_config.yaml>
obd cluster start <deploy_name> --strict-check
```

When this workflow is entered from an intentionally created `configured` registration, use the stored configuration only after revalidating its parsed semantics and checksum against the approved candidate. If the installed help supports deployment from a registered configuration, use `obd cluster deploy <deploy_name>` without `--config`; do not replace or silently accept different stored content. Keep `start` separate and invoke it only after deployment acceptance.

Use `--strict-check` only when the installed `cluster start --help` exposes it; OBD V4.6.0 documents it on start, not deploy. Preserve the configuration checksum and trace ID for each command. After `deploy`, establish what was registered, copied, installed, or initialized before deciding whether `start` is safe. Do not blindly issue `start` after a partial deploy.

<a id="interactive-deploy"></a>

### Interactive Deployment

Use `obd cluster deploy <deploy_name> --interactive` only when the user chooses the integrated guided workflow, the installed help exposes that long option, and a controllable TTY exists. In inspected builds it always proceeds from configuration generation into deploy and start, and it may then create a tenant; the tenant prompt can default to yes. Explicitly select no when tenant creation was not requested. Do not describe this as a configuration-only wizard or silently accept defaults for product, artifacts, hosts, cluster paths/ports/resources, the decision to create a tenant, non-tenant credentials, or cleanup. For the new-cluster database bootstrap password alone, accept OBD's generated random default without asking the user unless the user already supplied an override, and protect the terminal and resulting controller metadata from disclosure. When tenant creation was explicitly requested, apply the [tenant-creation default workflow](../../tenant-management/references/tenant-creation.md): omitted tenant settings intentionally remain OBD defaults, including `%` and an empty tenant password in the reviewed baseline, and must not become follow-up questions.

Before entering the workflow, inspect an existing deployment with the same name. An inspected implementation can confirm destruction of an already deployed name and use a force-kill path; it also sets force mode for the generated deployment, which can overwrite a home path. Treat either collision branch as a separately reviewed destructive operation, and stop unless every path is proved empty or owned and the impact is authorized.

The pinned caller sends every successfully completed `dev=True` host precheck to a default-yes initialization prompt, even when the precheck reports that no system parameters need changing. The prompt is not evidence that initialization is needed; choose no when there is no required diff. When the exact persistent host diff passes the host-initialization gate and is necessary to the requested deployment, the request already authorizes it, so proceed without another confirmation. An SSH or precheck-workflow failure instead returns false, but this caller does not propagate it: it skips the prompt and can continue into configuration generation, deploy, start, and optional tenant creation. Treat any such error as a hard manual stop and interrupt the wizard before the next stage; do not rely on its eventual exit status. The wizard can also offer password encryption using a fixed, predictable default passkey; do not enable that branch. Configure credential storage separately through the reviewed administration workflow with an approved protected passkey. Preserve and review the generated/registered configuration and the actual host/deploy/start/tenant outcomes after the integrated run.

The pinned interactive implementation asks for an SSH password, then reconnects through a shared precheck whose failure message prints that literal value. Enter this wizard only with an empty password over a proven local, key, or agent-based SSH route. If password authentication is required, use the reviewed configuration-file workflow or a fixed installed build instead. If the affected reconnect fails after a password was supplied, treat terminal output and the OBD trace as credential-bearing incident evidence, restrict access, and rotate the exposed credential; redaction after collection is not prevention.

Interactive deployment can also mutate controller telemetry policy. Before entering it, capture the presence and exact value of `TELEMETRY_MODE`, local telemetry logging/reporting policy, and active controller tasks. Inspect the installed interactive plugin: in the inspected implementation, confirming a non-`oceanbase-ce` product persistently writes `TELEMETRY_MODE=0`. When the user explicitly selected interactive deployment, its unavoidable in-scope policy write is covered by the shared persistent-change default; record and verify it without asking again. For an ordinary deployment request, prefer the reviewed configuration-file path rather than introducing that optional controller-wide side effect.

After the integrated run, compare the controller setting with the recorded absent/value baseline. Restore an authorized temporary change to its exact prior state when the installed product policy permits restoration, and report any intentional persistent difference.

### Autodeploy

Treat `autodeploy` as an integrated mutating workflow, not a YAML generator. Inspected implementations always run configuration generation, deployment, and startup in sequence. Use it only when all three transitions and their exact targets are authorized, after checking name/path/port collisions and all generated defaults. If the user wants only a draft or review, produce a non-executable blueprint or use the static-review boundary instead.

Keep optional destructive/convenience branches absent unless their exact installed behavior is separately requested and authorized. In the inspected command:

- `--force` permits overwriting `home_path`, while `--clean` cleans a `home_path` judged to belong to the invoking user; either branch also suppresses the normal cluster-status check;
- `--auto-create-tenant` creates a tenant named `test` using all resources the workflow considers available; use it only after the user explicitly requests tenant creation, apply the tenant default workflow without asking for omitted settings, and require data-plane acceptance;
- `--force-delete` deletes the registered cluster and is a separate destructive operation, not a name-collision convenience.

Display the canonical paths, existing registration, processes/listeners, tenant/resource outcome, and the equivalent health evidence that would replace any suppressed status check. Do not add any of these options to make the workflow unattended or to repair a partial deployment.

### Maximum-Utilization Default

Use the maximum-utilization workflow when the user explicitly requests it or when a new-cluster request omits resource sizing. An explicit user resource plan or non-maximum profile overrides this default. If the request names `obd perf`, route that exact single-node shortcut through [lifecycle.md](lifecycle.md#quick-deploy-shortcuts); do not replace it with `autodeploy`. For dedicated-host or capped multi-node maximum sizing, read and follow [maximum-utilization.md](maximum-utilization.md). It preserves deterministic per-node candidate calculation, per-key minima across all nodes, 8-core behavior, disk commitment checks, explicit common resource keys, and post-deployment equality checks. “Use all resources” never means zero safety reserve or permission to initialize the host automatically.

## Accept or Recover

Verify the registered component manifest and actual installed artifact identity, every selected process/listener/path, OceanBase topology and server state through SQL, authenticated SQL readiness using the protected OBD-generated or user-supplied credential, and relevant optional-component data planes. Confirm that unselected services were not added and no unexplained partial registration or path remains.

On failure, preserve the trace, registered configuration, generated files, remote processes, listeners, paths, and artifact state. Classify the stage before continuing. Do not delete the registered deployment, remove directories, redeploy, or retry until the shared failure-recovery rules identify the safe next action.
