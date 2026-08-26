# Deployment-Bound OBD Tools

Use this workflow for `obd tool command`, database connection helpers, interactive monitors, and similar tools that operate against a registered deployment.

## Resolve the Helper and Target

1. Record the exact OBD build, deployment state, registered components and servers, and selected package repositories.
2. Read the installed helper's help. For `obd tool command`, inspect the commands plugin/template shipped with that OBD build to determine available command names, supported components, wrappers, interaction mode, and side effects.
3. Resolve component and server selectors explicitly. Defaults can select the first target for an interactive helper or a broader set for a non-interactive helper, and unsupported deployed components can fail before filtering.
4. Verify the execution environment has a controllable TTY for every interactive command and define its exit sequence and session boundary.

Commands such as PID lookup, a remote shell, log-directory access, a pager, or debugger attachment are build/plugin-dependent examples, not a universal command list. Treat a resulting shell as ordinary remote access: stay read-only unless a separate mutation is authorized. Treat debugger attachment as availability-impacting and bind it to the verified component PID immediately before use.

## Database Connection and Interactive Monitoring

For `obd tool db_connect`, `obd tool dooba`, or an equivalent helper under the installed `obd tool` command group:

- verify the helper and required client binary are already available, or route installation through [tool-lifecycle.md](tool-lifecycle.md);
- resolve deployment, component, server, endpoint, tenant, database user, database, and intended access mode;
- prefer protected interactive credential input or an existing protected source; do not place a password in displayed arguments;
- run read-only identity, endpoint, tenant, and version checks first;
- do not infer SQL mutation permission from permission to open a session;
- confirm the client process and any wrapper exit when the session ends.

A connection to one endpoint does not prove deployment-wide health.

## Timeout and Per-Target Evidence

Determine whether the selected helper exposes a documented OBD-native timeout. If it does not, apply any required deadline only in the approved caller/orchestration layer and label it as caller-side; never invent a reusable OBD timeout option. A caller timeout means the remote or server-side task state is unknown, not that it terminated. Inspect the exact target process, session, child task, and trace before retrying or detaching.

For every invocation, preserve the redacted command, OBD build, plugin/template identity and checksum, resolved deployment/component/server targets, working directory, relevant non-secret environment, exact remote command or wrapper, start/end time, exit code, stdout, stderr, trace/task ID, and generated artifact paths. Keep evidence per target: a combined exit or one successful host must not hide a non-zero, timed-out, or partial result elsewhere.

When a helper generates a script, configuration, dump, pager file, log, or other artifact, record its canonical path, owner/mode, sensitivity, retention decision, and whether creation occurred before failure. Apply [cleanup and ownership boundaries](../../references/cleanup-boundaries.md) before removing it.

## Failure and Acceptance

Preserve the trace ID and inspect it with the public trace-display command supported by the installed build. Recheck plugin/template identity, deployment state, target spelling, and client/tool path before changing anything.

A missing template, unsupported command, empty log directory, failed wrapper, and unavailable component process are different failures. Do not modify installed plugins or hidden OBD metadata as a runtime workaround.

For non-interactive helpers, verify returned rows correspond to every intended target. For interactive helpers, verify the session opened on the intended host/directory or endpoint and exited cleanly. Report helper success separately from the health of the underlying component.
