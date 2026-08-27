# Common Test Workflow

Apply this workflow to Sysbench, TPC-H, TPC-C, and mysqltest. The selected tool reference adds its own data model, artifacts, and result checks.

## Capability and Toolchain Gate

Record the exact OBD executable/build, selected `obd test <tool> --help`, deployment/component/plugin identity, target server, OceanBase version, tenant, database, user, and test-tool versions.

Do not assume OBD always downloads a missing tool, and do not forbid package-manager installation universally. Depending on the installed OBD/plugin and repository state, a tool may be supplied by an OBD tool package, an OceanBase repository package, a local binary path, or a preinstalled external dependency. Resolve one reviewed source and record package name, version, release, architecture, hash, executable path, dependencies, download/install paths, and rollback.

Inventory every required binary before the first `obd test` invocation. Verified 4.7-era core paths can automatically install Sysbench/OBClient, TPC-H/OBClient, or JRE/TPC-C/OBClient when a dependency is absent. Installation can write under the controller user's home, create a global OBClient link, or modify a shell profile. If anything is missing, stop before the test command, present those exact mutations, and obtain installation authorization separately. Re-inventory after installation; permission to install does not authorize data preparation or load execution.

Run an authenticated SQL preflight against the exact endpoint, tenant, user, and database. Verify the account has only the privileges needed by the selected prepare/run/cleanup stages. Do not assume an empty or default password.

Inspect the selected CLI and plugin's credential path. Verified current plugins accept `--password` and can place the value in child-process arguments, verbose command logs, generated client commands, or tool configuration files. When no protected input exists, disclose the tool-specific exposure, use a dedicated least-privilege short-lived test credential and a permission-controlled local execution environment, define revocation/rotation and artifact handling, and obtain approval for that exposure. Do not label an argv or generated-file password as protected.

Treat credential confidentiality and command construction as independent gates. A dedicated or short-lived credential limits exposure impact but does not make shell interpolation safe. If the selected plugin concatenates a credential or another option into a command string executed by a shell, prefer a version proved to pass an argument vector with shell execution disabled. Otherwise apply the tool-specific strict character allowlist proved for every affected field and stop when the actual value cannot satisfy it. Quoting the outer `obd` command, adding ad hoc backslashes, or redacting a log does not make a later plugin-constructed shell command safe.

## Define Workload and Artifacts

Before execution, record:

- whether the target is disposable, reusable, or production-like;
- dataset/schema/table names and whether existing objects may be replaced;
- scale, concurrency, duration/event bound, and expected resource pressure;
- local and remote temporary, dataset, log, result, and report paths;
- free disk, memory, CPU, network, and log-disk headroom;
- artifacts to retain, reuse, or remove after the run.

Normalize every path and inspect pre-existing content and ownership. Do not let a generated-data or cleanup path overlap deployment data, logs, another run, or unrelated user files.

## End-to-End Deadline Gate

A workload option such as Sysbench `--time`, TPC-C `--run-mins`, or mysqltest `--case-timeout` limits only the stage implemented by that option. It is not an end-to-end deadline for connection retries, preparation, data generation or transfer, major freeze/merge, child processes, reporting, parameter restoration, or the complete OBD invocation.

Before execution, inspect the selected workflow and record:

- one absolute wall-clock deadline for the expected complete invocation, plus a separate bounded stop/recovery window if that deadline expires;
- separate bounds for connection/preflight, prepare/load, every freeze or merge wait, every external child process or query, the workload, reporting, and parameter restoration or other finalization;
- which bounds are enforced natively and which require the caller/orchestration layer;
- the exact parent and child process ownership, graceful-stop method, grace period, and database-side state checks if a deadline expires.

Prefer a proved native timeout for the stage it controls. When a stage has no native deadline, use a caller-side watchdog only if it can identify the exact OBD process and its child process group and the stop/recovery behavior has been reviewed. A generic parent-process timeout does not prove Java, OBClient, Sysbench, a remote command, or a database task stopped, and killing the parent can bypass a plugin `finally` path that restores benchmark parameters. If no bounded and observable termination plan can be established, do not start an unattended run.

At a deadline, stop scheduling new work and preserve the trace, process tree/group, child commands with secrets redacted, database objects/tasks, freeze/merge state, generated files, and saved parameter baseline. Run only the pre-authorized graceful-stop and recovery plan. If that plan separately authorizes process termination, terminate only the exact proved process group through the reviewed method; otherwise leave it intact and report the timeout for a new decision. Within the recovery bound, verify every child exited and every temporary parameter was restored. Classify remaining server-side work as `unknown` or `still running`; do not retry or clean until the shared failure-recovery workflow resolves that state.

## Control Benchmark Optimization

For Sysbench, TPC-H, and TPC-C, pass the installed long option explicitly. In verified OBD 4.7-era commands, `--optimization` accepts `0`, `1`, and `2`, defaults to `1`, and has these meanings:

- `0`: no OBD benchmark parameter optimization;
- `1`: change parameters classified by that plugin as not requiring restart;
- `2`: change additional parameters and potentially restart servers.

Treat those as version-specific facts and re-read installed help and plugin behavior. Use `--optimization=0` for the default baseline. It avoids OBD parameter tuning but does not make dataset preparation or the workload read-only.

Before level `1` or `2`, capture every parameter the installed plugin can change, current effective values, deployment health, and the plugin's apply/restore behavior. Verified current Sysbench, TPC-H, and TPC-C core paths restore the saved parameter values unconditionally in a `finally` path. Treat levels `1` and `2` as temporary tuning whose restoration is part of the same workflow, not an optional later cleanup.

Level `2` can restart servers while applying values and can restart them again while restoring the baseline. Obtain availability-impact authorization for both possible transitions after the final health check. If the user does not authorize the automatic restoration or either possible restart, do not run that OBD workflow. Afterward compare the effective values and process start times with the baseline even when the command failed.

Do not write the bare short option `-S`. In verified 4.7-era benchmark commands it means `--skip-cluster-status-check`, the opposite of deployment `--strict-check`. Keep status checking enabled. Use `--skip-cluster-status-check` only after explicit approval and an equivalent gate has verified all intended components, processes, listeners, tenant status, and SQL connectivity.

## Execute in Stages

Treat the applicable stages as separate even when a plugin combines them into one command. Sysbench, TPC-H, and TPC-C commonly use all five stages. For mysqltest, use preflight, optional initialization, run, and report by default; add a prepare/load or cleanup stage only when the installed plugin and reviewed test inputs actually define it, and mark inapplicable stages as `N/A` rather than inventing work:

1. **Preflight:** identity, health, authentication, toolchain, resources, paths, and baseline evidence.
2. **Prepare/load:** generate or locate data, create schema/tables, transfer files, and load data. Record exact objects and counts.
3. **Run:** execute the bounded requested workload under the separate end-to-end deadline while observing errors, latency, throughput, cluster health, and resource saturation.
4. **Report:** preserve raw output and produce a summary tied to exact inputs and versions.
5. **Cleanup/retain:** remove only approved run-owned objects, or preserve the reviewed reusable dataset and artifacts.

Before the cleanup/retain stage, apply [cleanup and ownership boundaries](../../references/cleanup-boundaries.md). Treat database objects, generated secret-bearing files, raw results, downloaded tools, shared caches, and controller profile/link changes as separate object classes.

Do not claim a phase was skipped merely because the CLI has no separate phase command. Inspect the installed workflow to determine what the invocation performs. A `test-only`, `init-only`, reuse, or similar option must be verified in installed help and against the actual dataset state.

Separate execution success from performance evaluation. Complete requested cases, queries, or stages; accepted error behavior; parseable artifacts; and post-test health determine whether the run executed successfully. TPS, QPS, latency, or similar metrics meet a target only when compared with a user-confirmed baseline, SLA, or version-matched acceptance standard. Without one, report the measured values and conditions without inventing a universal pass threshold.

## Non-Interactive Environment

Do not embed a permanent `obd env set IO_DEFAULT_CONFIRM 1` instruction in a test command. If unattended execution requires changing controller-wide auto-confirm or another OBD environment value, first read its presence and exact value, ensure no other task depends on it, obtain authorization, and restore the original present/absent state after the run. If restoration fails, stop and report the persistent controller change. Prefer command-local non-interactive behavior when the installed version provides it.

## Result and Retention Record

Record the redacted exact command, OBD/plugin/tool versions, target identities, dataset identity and checksum/counts, configuration, start/end time, exit code, trace ID, raw logs, result paths, error/failure counts, metrics, and post-test cluster/tenant health.

For a requested suite, continue independent cases when a case failure does not threaten data integrity or cluster health. Stop new load when the target becomes unhealthy, artifact identity becomes ambiguous, or a prior operation has unknown server-side state.

Before cleanup, show the exact run-owned database objects and filesystem paths. Preserve artifacts required to reproduce or audit the result. Never remove a reusable dataset, prior result, downloaded tool, shared cache, or unrelated temporary directory merely because the current run ended.
