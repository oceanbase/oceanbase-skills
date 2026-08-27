# OBD Runtime Environment

Treat `obd env` values and developer mode as persistent controller-wide policy. They can change later commands for every deployment and user of the same OBD home.

## Baseline and Concurrency Gate

Before a change, record the controller, user, executable/build, `OBD_HOME`, active CLI/Web/API tasks, developer-mode state, and the installed version's complete OBD environment view. Determine the storage scope and which processes read values only at startup.

If another task depends on a value or the baseline cannot be read, do not mutate it. Prefer a command-local option when the installed build provides an equivalent.

## Change One Policy at a Time

- Use exact set or unset operations for the required key. Never use environment clear as cleanup.
- Automatic confirmation can suppress destructive prompts for unrelated later commands. Do not enable it as a benchmark or automation prerequisite, and never treat it as user authorization. If temporarily approved, restore its exact prior state immediately after the scoped command.
- Developer mode can expose hidden commands, accept undefined options, or weaken validation. Enable it only for an explicit development workflow with a reviewed reason and stop condition; restore it afterward.
- Lock-mode changes can weaken controller concurrency protection. Do not downgrade or disable locks to bypass an active task or lock error.
- Transfer, repository-install, SSH-algorithm, base-directory, and Web-idle settings can change persistent paths, security, or runtime behavior. Review the installed meaning and consumers before changing one.

Do not guess an environment key or value from another OBD version. Save whether the key was absent as well as its value so restoration can distinguish `unset` from a configured default.

## Telemetry

Before work in an offline, regulated, or sensitive environment, inspect the installed build's telemetry submission and local telemetry logging behavior. Record the current organizational policy, configured values, local log path, and operations that can attempt submission.

Preserve the existing policy by default. Change telemetry submission, logging, or reporter settings only when the user or organization requires it. Submission and local logging are independent; disabling one does not prove the other is disabled. When no-egress behavior matters, verify it under the environment's approved network controls.

Redact deployment names, addresses, usernames, paths, command parameters, and business data before sharing telemetry artifacts. A telemetry failure does not by itself mean the requested OBD operation failed, and telemetry success does not prove it succeeded.

## Restore and Accept

After the scoped operation, restore every temporary key and developer/lock setting to the recorded baseline, including removal of keys that were originally absent. Compare the final environment with the baseline and report intentional persistent differences. Verify that no unrelated active task or deployment changed because of the temporary policy.
