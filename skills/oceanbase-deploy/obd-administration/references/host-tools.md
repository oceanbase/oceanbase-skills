# Top-Level OBD Host Tools

Use this workflow for the installed build's top-level host precheck, initialization, and host-user operations. These are not interchangeable with deployment-scoped environment initialization.

## Resolve the Physical Hosts

Record the controller, target hostname and management address, stable machine identity, SSH user/port/key source, operating system, architecture, current accounts, live kernel/limit values, persistent configuration, and every existing OBD deployment on the host. Deduplicate aliases that identify the same physical machine.

Read the exact installed subcommand help and implementation. Some builds default omitted host or user arguments to localhost or the current user; never rely on those defaults for a remote or privileged operation.

Prefer an explicit SSH key or agent route. When password authentication is required, collect the value through a protected local input path, avoid displaying the command with the value, restrict terminal and trace access, and redact it from reports. Inspected development implementations can include the password in verbose connection failures; if that occurs, treat the affected output as sensitive and rotate the credential when exposure warrants it.

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
