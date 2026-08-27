# Top-Level OBD Host Tools

Use this workflow for the installed build's top-level host precheck, initialization, and host-user operations. These are not interchangeable with deployment-scoped environment initialization.

## Resolve the Physical Hosts

Record the controller, target hostname and management address, stable machine identity, SSH user/port/key source, operating system, architecture, current accounts, live kernel/limit values, persistent configuration, and every existing OBD deployment on the host. Deduplicate aliases that identify the same physical machine.

Read the exact installed subcommand help and implementation. Some builds default omitted host or user arguments to localhost or the current user; never rely on those defaults for a remote or privileged operation.

The inspected 4.7 development implementation exposes `-p/--password` on both `obd host precheck` and `obd host init`, then passes that value into an SSH path that formats it into a verbose connection message and again into the connection-failure error. On that implementation, do not invoke either command with a non-empty password, even when a wrapper obtained it from a protected local prompt: use only a proved local, explicit `--ssh-key-file`, or SSH-agent route whose password value is empty. If password authentication is required, stop and require an installed implementation proved not to place the credential in arguments, logs, errors, or trace data; redaction after execution is not prevention.

If an affected invocation has already received a non-empty password, do not assume success kept it secret and do not copy its raw terminal, log, or trace output into ordinary evidence. Treat those locations as credential-bearing incident material, restrict access, preserve only a redacted operational record, and rotate the exposed credential.

## Precheck

Treat a host precheck as read-only only after confirming the installed implementation and selected arguments. Preserve the exact checks, targets, non-secret output, and OBD identity; redact secret values without discarding the trace ID or failure context. A host-level pass does not prove that a particular deployment's packages, topology, paths, ports, resources, or component configuration are valid.

## Host Initialization

Host initialization can persistently change kernel parameters, limits, packages, services, directories, ownership, or permissions. Before execution:

1. derive the exact per-host live and persistent diff from the installed workflow;
2. detect duplicate or conflicting entries and identify file ownership;
3. show reboot/reconnect and availability effects;
4. define itemized rollback to captured original values;
5. obtain authorization per unique physical host.

If the exact changes cannot be established, stop. Do not run initialization first and inspect afterward. Do not use it to bypass port/path overlap, architecture or package mismatch, insufficient resources, network failure, or an unknown process.

## Host User Operations

Resolve whether the operation creates or changes an account, group, home directory, sudo rule, SSH material, credential, or ownership. Preserve existing access and obtain authorization for the exact account and paths. Do not grant passwordless sudo, replace authorized keys, rotate credentials, or recursively change ownership unless explicitly included.

After any mutation, compare live and persistent state with the approved diff, verify the intended SSH/privilege path, and confirm unrelated users and deployments remain functional. Restore item by item; never use broad account, sudoers, limits, or sysctl cleanup.
