# Failure Recovery and Evidence

Read this reference after a failure, timeout, interruption, or mixed result and before retrying, cleaning, or changing the plan.

Any proposed cleanup must also pass [cleanup and ownership boundaries](cleanup-boundaries.md). Failure recovery does not expand the original authorization or transfer ownership of residual objects.

## Freeze the Observed State

Do not assume a non-zero exit means nothing changed or that a timeout means the task stopped. Preserve:

- OBD executable/build and plugin identities;
- exact redacted command or API request and input configuration checksum;
- trace or task ID, timestamps, terminal output, task phase, and logs;
- deployment/component/tenant state before and after;
- target processes, listeners, paths, mounts, resources, and relevant component logs;
- package/repository candidates and actual installed artifact identity.

Collect only evidence needed for the failure. Route high-overhead production collection to the obdiag skill.

## Classify the Actual State

Use observed evidence to classify the target, for example:

- configured but not deployed;
- deployed but not running;
- partially running;
- running but unhealthy;
- healthy at control plane but unavailable at data plane;
- timeout with server-side state unknown;
- destroyed or dropped with residual objects;
- asynchronous task accepted, running, failed, or recoverable.

Do not choose a recovery command until the state and completed stage are known.

## Reconcile Caller Timeouts and Asynchronous Tasks

A caller timeout, lost terminal, or interrupted SSH session does not cancel an OBD or server-side task. Before retrying, use the same controller identity and resolved `OBD_HOME` to identify the original local OBD process and children, correlate its trace/task ID and time window, and query the narrowest public control-plane and domain state available. Corroborate that state with runtime and data-plane evidence such as the exact deployment/component/tenant object, processes/listeners, authenticated SQL, task rows, or storage artifacts.

Define a bounded observation deadline and classify the original invocation as exactly one of:

- **succeeded:** the intended terminal control-plane state and every required acceptance layer are present;
- **failed:** the task reached a proved failed terminal state, with partial objects inventoried;
- **still running:** the original process or task is active and remains the only authorized invocation;
- **unknown:** evidence is unavailable, contradictory, or cannot distinguish a live task from a partial result.

When the caller timed out but the exact task and target subsequently satisfy acceptance, continue from that successful state; do not report failure or submit a duplicate. When it is still running, continue bounded observation rather than launching another invocation. For failed or unknown states, freeze retries until idempotence, residual ownership, and the narrowest next action are proved. Trace text alone never supplies the terminal classification.

## Choose the Narrowest Recovery

For the classified state, decide whether the safe action is to continue the original task, repair one failed target, use a documented recover operation, restore a saved configuration/artifact, roll back, or stop for operator input.

The following are never generic recovery steps:

- `redeploy` or a second deploy;
- `destroy`, tenant drop, or metadata deletion;
- `--force` or ignore-safety options;
- mirror/repository clean or broad cache deletion;
- clearing OBD environment state, locks, or stored credentials;
- editing hidden `.obd` metadata or installed plugins;
- changing unrelated network, path, resource, or kernel parameters.

If recovery would introduce a new destructive, availability, persistent-host, repository, or credential mutation, present it as a new operation and obtain its own authorization.

## Retry Rules

Before retrying:

1. resolve whether the previous operation is still active;
2. determine whether the operation is idempotent for the observed stage;
3. identify partial objects and whether the command resumes, duplicates, overwrites, or rejects them;
4. confirm inputs and repository resolution have not changed;
5. define a stop condition that prevents repeated blind attempts.

One unexplained repeated failure is enough to stop automated retries when another attempt can expand damage or ambiguity. Online package acquisition from the fixed OceanBase public mirror sources is a narrower non-mutating exception: it follows the explicit three-attempt-per-source rule below.

### Network and Artifact-Acquisition Failures

A DNS, connection, proxy, TLS, HTTP, metadata, or download failure establishes only one failed package-source attempt and observation window; it does not by itself prove that the controller has no usable network path. For OBD packages and components, keep the selected controller and acquisition location stable and follow the repository workflow's [fixed mirror-source order](../obd-administration/references/mirror-and-repositories.md#fixed-online-package-source-order): three failed actual acquisitions on source 1 before source 2, then three on source 2 before advancing to another compatible suffix or asking the user after the full matrix. A generic connectivity probe neither counts as an attempt nor permits a source to be skipped.

Do not silently move a download to the automation runner, install or run OBD there, introduce a third mirror source, or select another controller as recovery. Once every required source attempt and compatible suffix on the controller has been exhausted, present the attempt evidence and ask the user to choose the next source or location. A user-approved artifact relay changes only artifact transport unless the user separately authorizes a control-plane move.

## Report the Outcome

Separate confirmed facts, tool suggestions, and inference. State:

- which stage completed and which did not;
- current availability and data-safety status;
- residual objects or active tasks;
- evidence supporting the suspected cause;
- the narrowest safe next action and whether it needs new authorization.

An obdiag rule, log pattern, or RCA suggestion is not a confirmed root cause until it agrees with independent runtime, SQL/API, or system evidence.
