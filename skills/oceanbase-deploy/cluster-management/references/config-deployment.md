<!-- Compatibility anchors retained for published 2.x deep links. -->
<a id="config-file-deployment"></a>
<a id="deploy-with-config-file"></a>

# Configuration-File Deployment

Use a reviewed configuration file for reproducible community or commercial OceanBase deployment. This workflow registers a deployment and installs component artifacts; starting it is a separate state transition.

<a id="cluster-operations-after-deployment"></a>
<a id="edit-config"></a>
<a id="reload-config"></a>
<a id="upgrade-component"></a>
<a id="scale-out"></a>
<a id="add-delete-component"></a>
<a id="add--delete-component"></a>

## Legacy Operation Links

Published 2.x links for post-deployment operations resolve here. Continue with the matching dedicated workflow:

- `edit-config` or `reload-config`: [edit or reload configuration](configuration-changes.md)
- `upgrade-component`: [upgrade a component](upgrade.md)
- `scale-out`, `add-delete-component`, or `add--delete-component`: [scale or add/delete components](scale-and-components.md)

<a id="component-selection"></a>

## Select the Product Blueprint

Resolve the product form before writing YAML, then read exactly one blueprint:

- [Community distributed](deployment-templates/community.md)
- [Commercial distributed](deployment-templates/commercial-distributed.md)
- [Commercial standalone or centralized](deployment-templates/commercial-standalone.md)

The blueprints are intentionally schema-gated. They identify required decisions and configuration structure without claiming that fields from one OBD/plugin version are valid in another. Produce an executable YAML only after validating every key against the selected installed plugin.

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

Record these inputs before downloading artifacts or writing YAML:

| Area | Required inputs |
|---|---|
| Controller | host, user, exact OBD executable/build, `OBD_HOME`, active tasks |
| Product | product form, exact component key, component/plugin version |
| Artifacts | component, version, release, architecture, hash, source, dependency closure |
| Topology | deployment name, app/cluster identity, zones, server-to-component mapping |
| SSH | target machine identity, management IP, SSH user/port/key and privilege boundary |
| Paths | canonical home, data, log, redo, cache, temporary, and shared-storage paths as applicable |
| Network | management, SQL, RPC, obshell, proxy, monitoring, OCP, and component-specific addresses/ports |
| Resources | CPU, memory, disk, inode, filesystem/mount, cgroup/container limits, and headroom |
| Persistent host behavior | explicit auto-start decision; keep it disabled/unset unless requested and approved through the lifecycle systemd gate |
| Optional scope | requested OBProxy, OBAgent, monitoring, OCP, Config Server, `oceanbase.ai`, `oblogservice`, or shared storage |
| Secrets | approved protected input source and redaction plan; never literal reusable values |

Every component in the manifest must map to a requested outcome or a proved package/plugin dependency. A demo, repository listing, all-in-one bundle, or old YAML is not permission to deploy all contained components or create a tenant.

## Preflight

1. Read `obd --version`, the selected `obd cluster deploy --help`, and the installed component schema/workflows.
2. Confirm exactly one compatible artifact for every selected component. Record version, release, architecture, hash, and repository source; repository presence alone does not prove compatibility.
3. Prove each target's hostname/machine identity, management address, OS, architecture, runtime libraries, time synchronization, routes, firewall boundary, and SSH behavior.
4. Resolve every path canonically. Inspect owner, mode, free space, inode capacity, mount identity, symlinks, non-empty contents, overlap with other deployments, and cleanup ownership.
5. Map every proposed port to its host and namespace. Check real listeners and processes, not only registered deployments.
6. Check available CPU, memory, log/data capacity, cgroup/container constraints, and topology failure domains. Do not infer usable resources from host totals alone.
7. Inspect existing OBD registrations and remote processes. The deployment name, app identity, paths, and ports must not collide with an existing or unmanaged service.
8. Run only the public version-supported precheck/strict-check path. In reusable deployment instructions spell `--strict-check` in full when the installed command exposes it; never transfer the short option `-S` from another subcommand.

Stop when the plugin schema, artifact closure, product compatibility, host identity, path ownership, or topology cannot be proved. Do not use `--force`, `redeploy`, path deletion, `init4env`, or a community package as a preflight workaround.

## Render and Review YAML

Render values from the approved manifest and selected plugin schema. For every field, record whether it is required by the schema, derived by the plugin, or explicitly chosen by the user.

Review the rendered file semantically:

- exact product/component keys and dependency relationships;
- server and zone identity, management versus service addresses;
- canonical per-server paths and ports;
- version/release constraints and the separately locked artifact hashes;
- resource values and units;
- credential references with displayed values redacted;
- no unrequested component stanza, tenant creation, auto-start, telemetry change, or cleanup behavior.

A syntactically valid YAML is not enough. For an executable plan, use the installed OBD/plugin parsing and precheck path; do not install or start a component merely to discover whether a key exists. In static-review mode, do not invoke OBD parsing, plugin precheck, or any workflow: report schema/runtime validation as not performed and keep every unsupported conclusion conditional.

Keep `enable_auto_start` or an equivalent plugin option false or unset unless persistent startup was explicitly requested. If proposed, read the [automatic-startup and systemd gate](lifecycle.md#automatic-startup-and-systemd) before rendering or executing the configuration.

## Execute

Apply the shared telemetry gate immediately before `deploy` or `autodeploy`. These commands are documented telemetry triggers in OBD V4.6.0. Do not rely on a general controller setting remembered from another session; capture the current value on the resolved controller. A temporary telemetry change is a separately authorized controller-wide mutation. Restore its recorded baseline only after the shared child-process race gate proves that restoration cannot release a pending report; otherwise defer restoration and report the safer persistent difference.

Use the syntax confirmed by the installed command help:

```bash
obd cluster deploy <deploy_name> --config=<reviewed_config.yaml>
obd cluster start <deploy_name> --strict-check
```

When this workflow is entered from an intentionally created `configured` registration, use the stored configuration only after revalidating its parsed semantics and checksum against the approved candidate. If the installed help supports deployment from a registered configuration, use `obd cluster deploy <deploy_name>` without `--config`; do not replace or silently accept different stored content. Keep `start` separate and invoke it only after deployment acceptance.

Use `--strict-check` only when the installed `cluster start --help` exposes it; OBD V4.6.0 documents it on start, not deploy. Preserve the configuration checksum and trace ID for each command. After `deploy`, establish what was registered, copied, installed, or initialized before deciding whether `start` is safe. Do not blindly issue `start` after a partial deploy.

<a id="interactive-deploy"></a>

### Interactive Deployment

Use `obd cluster deploy <deploy_name> --interactive` only when the user chooses the integrated guided workflow, the installed help exposes that long option, and a controllable TTY exists. In inspected builds it always proceeds from configuration generation into deploy and start, and it may then create a tenant; the tenant prompt can default to yes. Explicitly select no when tenant creation was not requested. Do not describe this as a configuration-only wizard or silently accept defaults for product, artifacts, hosts, paths, ports, resources, tenant creation, credentials, or cleanup.

Before entering the workflow, inspect an existing deployment with the same name. An inspected implementation can confirm destruction of an already deployed name and use a force-kill path; it also sets force mode for the generated deployment, which can overwrite a home path. Treat either collision branch as a separately reviewed destructive operation, and stop unless every path is proved empty or owned and the impact is authorized.

The pinned caller sends every successfully completed `dev=True` host precheck to a default-yes initialization prompt, even when the precheck reports that no system parameters need changing. The prompt is not evidence that initialization is needed; explicitly choose no unless the exact persistent host diff passed the host-initialization gate and was separately authorized. An SSH or precheck-workflow failure instead returns false, but this caller does not propagate it: it skips the prompt and can continue into configuration generation, deploy, start, and optional tenant creation. Treat any such error as a hard manual stop and interrupt the wizard before the next stage; do not rely on its eventual exit status. The wizard can also offer password encryption using a fixed, predictable default passkey; do not enable that branch. Configure credential storage separately through the reviewed administration workflow with an approved protected passkey. Preserve and review the generated/registered configuration and the actual host/deploy/start/tenant outcomes after the integrated run.

The pinned interactive implementation asks for an SSH password, then reconnects through a shared precheck whose failure message prints that literal value. Enter this wizard only with an empty password over a proven local, key, or agent-based SSH route. If password authentication is required, use the reviewed configuration-file workflow or a fixed installed build instead. If the affected reconnect fails after a password was supplied, treat terminal output and the OBD trace as credential-bearing incident evidence, restrict access, and rotate the exposed credential; redaction after collection is not prevention.

Interactive deployment has an additional controller-policy branch that is not covered merely by treating the later deploy/start as telemetry triggers. Before entering it, capture the presence and exact value of `TELEMETRY_MODE`, local telemetry logging/reporting policy, and active controller tasks. Inspect the installed interactive plugin: in the inspected implementation, confirming a non-`oceanbase-ce` product persistently writes `TELEMETRY_MODE=0`. Treat that write as a separate controller-wide mutation. Do not use the interactive path for a commercial product unless that persistent policy change is authorized; use the reviewed configuration-file path when it is not.

After the integrated run, compare the controller setting with the recorded absent/value baseline. Restore a prior value only when the installed product policy permits restoration and the [telemetry race gate](../../obd-administration/references/runtime-environment.md#telemetry) proves that no current or earlier child/report can submit after re-enablement. Otherwise keep the safer state and report the intentional or safety-deferred difference. An early interactive return does not prove that a reporter from an earlier controller task is absent.

### Autodeploy

Treat `autodeploy` as an integrated mutating workflow, not a YAML generator. Inspected implementations always run configuration generation, deployment, and startup in sequence. Use it only when all three transitions and their exact targets are authorized, after checking name/path/port collisions and all generated defaults. If the user wants only a draft or review, produce a non-executable blueprint or use the static-review boundary instead.

Keep optional destructive/convenience branches absent unless their exact installed behavior is separately requested and authorized. In the inspected command:

- `--force` permits overwriting `home_path`, while `--clean` cleans a `home_path` judged to belong to the invoking user; either branch also suppresses the normal cluster-status check;
- `--auto-create-tenant` creates a tenant named `test` using all resources the workflow considers available; it requires a separate tenant identity/resource/credential review and data-plane acceptance;
- `--force-delete` deletes the registered cluster and is a separate destructive operation, not a name-collision convenience.

Display the canonical paths, existing registration, processes/listeners, tenant/resource outcome, and the equivalent health evidence that would replace any suppressed status check. Do not add any of these options to make the workflow unattended or to repair a partial deployment.

### Maximum-Utilization Requests

Use a maximum-utilization or auto-generated workflow only when explicitly requested. If the request names `obd perf`, route that exact single-node shortcut through [lifecycle.md](lifecycle.md#quick-deploy-shortcuts); do not replace it with `autodeploy`. For dedicated-host or capped multi-node maximum sizing, read and follow [maximum-utilization.md](maximum-utilization.md). It restores the deterministic per-node candidate calculation, weakest-node resource minima, 8-core behavior, disk commitment checks, explicit common resource keys, and post-deployment equality checks. “Use all resources” never means zero safety reserve or permission to initialize the host automatically.

## Accept or Recover

Verify the registered component manifest and actual installed artifact identity, every selected process/listener/path, OceanBase topology and server state through SQL, authenticated SQL readiness, and relevant optional-component data planes. Confirm that unselected services were not added and no unexplained partial registration or path remains.

On failure, preserve the trace, registered configuration, generated files, remote processes, listeners, paths, and artifact state. Classify the stage before continuing. Do not delete the registered deployment, remove directories, redeploy, or retry until the shared failure-recovery rules identify the safe next action.
