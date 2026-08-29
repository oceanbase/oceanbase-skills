# Configuration Changes

Use this workflow only for `edit-config`, `reload`, `chst` configuration-style conversion, and classifying how configuration fields become effective. Lifecycle operations, component changes, upgrade/reinstall, tenant operations, and deployment rebuilds belong to their dedicated workflows. A text edit, a successful reload, and an effective runtime change are distinct outcomes.

A deployed component's server-set change is a topology operation, not an ordinary configuration edit. Adding or removing Observer servers from a registered deployment is unsupported. Do not use `edit-config`, its complete-YAML standard-input path, a generated-file editor, SQL, obshell, component operations, process control, or metadata edits to perform or reconcile that transition. Generic access to a `servers` field is not evidence of support.

## Select an Existing or New Registered Configuration

Resolve the exact controller, OBD executable, `OBD_HOME`, and `deploy_name`, then determine whether that name is already registered. Do not assume that `edit-config` requires an existing deployment: the official V4.6.0 command guide and inspected current implementation support creating a registered deployment configuration when the name does not exist.

For an absent name:

1. Recheck immediately before the command that the name is still unused on the selected controller. Review one complete candidate deployment YAML, including product/component identities, versions, servers, paths, ports, resources, repositories, and secret handling.
2. Treat creation as a controller-local configuration registration and obtain authorization for that exact name and complete YAML. It does not authorize package installation, target-host changes, deployment, start, or tenant creation.
3. With a controlled TTY, `obd cluster edit-config <deploy_name>` can prompt to create the missing deployment and then open the editor. In an installed build proven to match the inspected implementation, non-empty standard input is treated as the complete YAML and can enter the creation path without that interactive prompt; therefore obtain authorization before invocation rather than relying on the prompt.
4. Accept success only when the registered deployment exists with state `configured`, its stored YAML parses, and its semantic content and checksum match the reviewed candidate. Confirm that no component was deployed or started and do not run `reload`. Route a later deployment request through the [configuration deployment workflow](config-deployment.md), revalidate the stored configuration, and treat `obd cluster deploy <deploy_name>` as a separate mutation. Route a later start request through the [lifecycle workflow](lifecycle.md) only after deployment succeeds and the registered and installed state has been verified.

If the name appears concurrently, the stored content differs, or any target-host/runtime side effect is observed, stop and preserve the controller trace and configuration evidence.

## Build the Change Set

1. For an existing deployment, record the OBD build, deployment identity and state, selected component/plugin versions, registered configuration checksum, and effective database/component values.
2. Read the installed command help and plugin parameter schema/workflows. Classify every field as:
   - dynamically applicable;
   - accepted by OBD but requiring a component restart;
   - immutable or unsupported after deployment;
   - requiring a supported upgrade, reinstall, component transition, or destructive rebuild path.
3. Show the semantic before/after values, target servers/components, generated-file impact, availability effect, persistence boundary, and rollback value.
4. Save a protected, redacted-for-display snapshot outside deployment-owned paths. Preserve the unredacted source only with permissions appropriate for its credentials.

If the installed plugin cannot establish the apply class, stop. Do not assume `reload` makes every accepted field dynamic.

## Auditable Editing

`obd cluster edit-config <deploy_name>` can open an editor. Use the editor-driven path only through a real, controllable PTY and a version-proven editor integration. In a tested build, invoking the command without a TTY caused standard input to be treated as replacement configuration; empty input failed with `Empty configuration` instead of opening the editor. Do not use an empty pipe or a non-PTY session to trigger the editor. A non-TTY invocation is appropriate only when deliberately using the complete-YAML standard-input path described below.

The inspected current implementation first reads standard input and, when it receives non-empty content, treats that content as the complete candidate deployment YAML instead of opening an editor. For non-interactive automation, use this path only when the installed implementation proves the same behavior: submit exactly one complete, reviewed YAML through protected standard input, preserve its checksum, and require the resulting semantic diff to match the approved change set. This is whole-document replacement, not a field-patch interface. Do not send a fragment, omit unchanged secret-bearing fields, or invent a `--set` option.

For automation, first inspect how the installed OBD build selects and invokes its editor. If it honors a command-local editor variable, use a narrowly scoped wrapper that:

- accepts only the exact generated configuration path supplied by OBD;
- verifies the expected pre-edit checksum;
- changes only the reviewed keys;
- records the file device and inode, rewrites and truncates that same file in place, and verifies that its device and inode remain unchanged;
- rejects a missing, symlinked, or unexpected path;
- writes no secret into terminal output;
- returns failure unless the post-edit YAML parses and the semantic diff matches the approved change set.

Do not use `sed -i`, temporary-file replacement, rename-based atomic writing, or an editor that swaps the generated file's inode in this path. In the tested build, such a replacement made OBD report `config unchange`; an in-place rewrite under a controlled editor and PTY was observed correctly. This is an editor-path compatibility requirement, not permission to edit hidden OBD metadata.

Do not invent a `--set` option, leave a persistent global editor override, or edit hidden `.obd` files directly. If no safe PTY/editor path or deliberate complete-YAML standard-input path is supported, stop.

## Apply and Verify

Use only the installed syntax, commonly:

```bash
obd cluster edit-config <deploy_name>
obd cluster reload <deploy_name>
```

Before reload, inspect the recorded diff and refresh component health. Obtain availability authorization if the installed workflow can restart any target. Current inspected OBD HEAD exposes no component/server selector for reload and applies it across the deployment; on a stopped or unhealthy deployment it may first start the whole deployment. Display and authorize that full scope and implicit start, or stop when the requested scope is narrower. Preserve the trace ID.

For a field already proved dynamically applicable by the installed plugin, capture Observer PIDs and start times and run a bounded authenticated SQL continuity probe before, throughout, and after reload. The tested dynamic-parameter path changed the effective value without restarting Observer and kept SQL continuously available. Treat that as the expected no-restart acceptance result only for fields classified dynamic in the selected build; do not generalize it to restart-required or unresolved fields. Any PID/start-time change or SQL interruption disproves a no-restart claim even when final health recovers, and inability to observe the reload interval means uninterrupted availability was not established.

Afterward compare:

- registered configuration and generated per-server files;
- component command line or local configuration where relevant;
- database/API-side effective values;
- selected process PIDs/start times and service health;
- SQL continuity across the reload interval when a dynamic no-restart result is expected;
- unselected fields and targets.

Report values that remain pending restart. Never report a field as applied solely because `reload` exited successfully.

## Configuration Style Conversion

Use `obd cluster chst` only when the installed help and selected plugins expose the requested style. Treat it as a configuration mutation, not display formatting.

Before conversion, save the registered configuration and metadata checksums, enumerate supported styles and field mappings, and produce a semantic preview covering components, servers, zones, paths, ports, resources, dependencies, secrets references, and artifact constraints. Use the exact version-supported syntax; do not assume a style name or option from another release.

After conversion, prove semantic equivalence and that OBD can parse/display the deployment. Do not reload or restart merely because conversion succeeded. If a field was lost or changed meaning, stop and restore only from the validated snapshot.

## Failure Boundary

If `edit-config` fails while loading the unchanged generated YAML, before an approved semantic edit has occurred, classify the editor path as unavailable for that exact OBD build and registered configuration. Preserve the unchanged checksum, temporary-YAML parsing error, trace, registered configuration, and runtime state, then stop. Do not automatically switch editors, submit the whole document through standard input, or edit hidden metadata to bypass the failing parser.

On any edit, reload, or conversion failure, preserve both configurations, trace, generated files, real process state, and effective runtime values. Do not apply a second edit or restart all components until the observed state identifies the narrow recovery action.

## Sources

- Official OBD V4.6.0 Command Guide cluster configuration command group.
- [Source-evidence boundary](../../references/source-baselines.md#source-evidence-boundary): `_cmd.py` `ClusterEditConfigCommand`; `core.py` `edit_deploy_config` in the exact inspected checkout.
