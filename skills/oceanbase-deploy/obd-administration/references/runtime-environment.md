# OBD Runtime Environment

Use this workflow for the tested controller-identity behavior around `OBD_HOME` and for narrowly scoped automatic-confirm handling.

## Resolve OBD_HOME

Record the controller host, user, exact OBD executable/build, registered deployments, trace location, and whether `OBD_HOME` was originally unset or explicitly configured. Resolve controller state under the unchanged caller environment first.

Do not export an observed metadata directory as `OBD_HOME`. A path such as `/root/.obd` can be interpreted as a base and create an unintended `/root/.obd/.obd`. If a scoped operation requires an explicit override, verify the resulting registration and trace location before continuing and restore the original unset/value state afterward.

Re-resolve controller identity after an SSH hop, user change, executable replacement, or environment change. A new empty OBD home is not evidence that no deployment exists and must not be used as repair.

## Automatic Confirmation

Automatic confirmation is persistent controller state and can suppress prompts for unrelated later commands. Do not enable it merely because automation lacks a TTY, and never treat it as user authorization.

Use it only when the exact target and mutation have already been authorized, the installed version proves which prompt it answers, no unrelated OBD task is active, and a command-local public confirmation form is unavailable. Record whether the key was absent as well as its value, run only the scoped command, then restore the exact prior state immediately.

For interactive commands, prefer a real PTY. If a confirmation session stalls, identify and stop only the caller-owned waiting OBD process, reconcile server-side state, and retry only after proving that the original mutation did not continue.

## Accept

Compare final `OBD_HOME`, registration visibility, trace location, automatic-confirm state, and active tasks with the baseline. Report intentional differences and verify that no unrelated deployment or controller setting changed.
