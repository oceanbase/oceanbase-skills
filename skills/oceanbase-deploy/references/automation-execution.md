# Non-Interactive Automation Execution

Use this workflow for unattended or multi-stage OBD automation. It supplements the [operation contract](operation-contract.md); it does not authorize a mutation, package installation, credential exposure, or a broader target.

## Preflight the Runner

Before the first OBD, SSH, SQL, or helper invocation, record and verify:

- the automation runner, selected controller, artifact-acquisition host, managed hosts, user and SSH hop for each, working directory, shell, and non-secret environment; for remote workflows, confirm that OBD execution and metadata remain on the remote controller unless the user explicitly selected otherwise;
- the exact controller-side `obd` executable/build and resolved controller home;
- whether `OBD_HOME` was originally unset or explicitly configured, and which registered deployments and traces prove that the resolved controller is the intended one;
- whether stdin is attached to a controllable TTY, which steps can prompt, and how each supported prompt will be handled;
- the exact SQL client or OBD database helper, endpoint mode, and protected credential source;
- every external interpreter and module required by an auxiliary script under the exact executable that will run it;
- the installed public helper/action inventory and the spelling, target scope, interaction mode, and exit behavior of every selected action;
- caller-side and OBD-native timeouts, process ownership, and the state checks that follow either timeout.

Do not assume that OBD's private Python environment, the system Python, or an automation runner contains `mysql.connector` or another client module. Test the required import with the exact interpreter before starting the workflow, or use an already available, supported SQL client. Missing runtime support does not authorize package installation, modification of OBD, or switching to an unrelated interpreter.

Validate helper and action names through the installed public inventory or help first. Inspect a packaged helper template only when the public surface cannot establish a critical name or side effect. Do not invoke a guessed action merely to see whether it exists.

## Handle Confirmation Without Expanding Semantics

For each potentially prompting command, determine before launch whether the installed build provides a command-local, public confirmation option whose only reviewed effect is acknowledging that exact prompt. Use it only after the target, impact, and required authorization have passed their normal gates.

Do not use a controller-wide automatic-confirm setting, generic `yes` input, an unrelated `--force` option, or hidden input to make a workflow unattended. Some command-local options named `--confirm` also trigger restarts or other work; their exact installed semantics still control. If no safe command-local form exists and the command must be answered interactively, use a real PTY with controllable stdin rather than an ordinary pipe, or stop before launching the command.

Immediately before confirmation, display the deployment, component, repository object, or fully expanded deletion set named by the prompt and compare it with the authorized inventory. A confirmation session must acknowledge only that unique named object or exact enumerated set; do not reuse one session or response across adjacent objects.

If an automation client has already left an OBD process waiting for input, identify the caller-owned PID and children, determine whether any mutation began, interrupt only that invocation through its normal caller/session boundary, and reconcile controller and target state before another attempt. Retry only after the first invocation is terminal or absent and idempotence is proved. Never leave an unidentified prompt-waiting process attached to the controller.

## Record Structured Events

For unattended or multi-stage work, write an append-only JSON Lines record in an approved, permission-controlled local path. Use one event per line and keep raw secrets out of every field. At minimum record:

```text
run_id, operation_id, phase, event, wall_time_utc, monotonic_time,
runner, controller, artifact_acquisition_host, attempted_route, target,
redacted_command, command_pid, target_pids,
listeners, obd_state, data_plane_probe, trace_or_task_id, result
```

Also record the input/configuration checksum, artifact source and checksum, relevant proxy/repository state, stdout/stderr artifact paths, exit code or caller timeout, selected and unselected objects, and the final removed/retained object sets when relevant. Use a stable run ID across the lifecycle and a distinct operation ID per command. Wall-clock timestamps support correlation; monotonic timestamps support duration calculation.

For measured stop, start, or restart availability, capture separate events for the last successful authenticated data-plane probe, listener loss, expected PID transition, listener recovery, and first successful authenticated probe. Command start/end time alone is not database downtime.

## Reconcile the End State

After every invocation, close or account for the local command process, SSH session, helper wrapper, and child task. A caller timeout or disconnected terminal does not prove that OBD or the server-side task stopped. Follow the shared [failure-recovery workflow](failure-recovery-and-evidence.md), append the reconciled terminal or unknown state, and do not submit a duplicate operation while the first invocation remains unresolved.
