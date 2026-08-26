# Taking Over an Existing Cluster with OBD

Use `obd cluster takeover` to register a supported, already running OceanBase cluster under this OBD controller. It is a control-plane ownership change, distinct from OCP takeover/export, a new deployment, host migration, or recovery.

## Capability, Identity, and Ownership Gate

1. Read installed `cluster takeover --help` and workflow. Prove support for the exact community/commercial product form and version.
2. Through SQL and host inspection resolve the database endpoint, cluster unique identity/app name, topology/zones/servers, SQL/RPC ports, component version/release/architecture, binary checksums, paths, service account, and real process owners.
3. Verify the proposed deployment name is unused. Identify every existing OBD/OCP controller or automation owner; stop when concurrent lifecycle ownership is possible.
4. Verify the required database credential and non-interactive SSH path to every discovered server. Do not accept defaults such as loopback, current OS user, default port, or empty password without observation.
5. Map every path and PID to the intended cluster and identify overlaps. Takeover must not claim an unrelated process or directory.
6. Inspect the version-matched workflow for remote reads/writes, generated files, controller repository creation, configuration changes, automatic failure cleanup, or restart behavior. If availability can be affected or controller/host state changes, disclose it and obtain separate authorization; if behavior is unknown, stop.

Current inspected source hard-codes a community `oceanbase-ce` takeover workflow and version-specific repository behavior. Treat that implementation as CE-only. A commercial distributed or standalone takeover requires an installed workflow that explicitly proves support; do not invoke the community path experimentally.

The inspected workflow can copy binaries/directories from production servers to the controller when no matching local package exists, then create a local repository with force semantics. It can also automatically remove the new deployment metadata when an exception occurs. Before execution, inventory and approve the exact remote reads, controller destination and repository mutation, collision behavior, artifact hash, metadata name, and unavoidable failure cleanup.

Avoid literal passwords in command arguments. Prefer SSH keys and a version-supported protected database credential input. If only an argv password option exists, disclose the exposure and use an approved secure local procedure; never copy the value into examples or reports.

## Execute

Construct the command only from verified values and options exposed by installed help. A schematic form is:

```bash
obd cluster takeover <new_deploy_name> \
  --host=<verified_sql_host> \
  --mysql-port=<verified_sql_port> \
  --ssh-user=<verified_ssh_user> \
  --ssh-port=<verified_ssh_port> \
  --ssh-key-file=<approved_key_file> \
  [version-supported protected credential options]
```

Preserve the trace and generated/registered configuration.

## Acceptance and Failure

Verify exactly one new registration and that its component, servers, paths, ports, versions, repositories, and cluster identity match the live system. Independently verify real PIDs/listeners, authenticated SQL, unchanged service start times where no restart was expected, and a read-only OBD management action.

On failure, preserve the trace, whatever metadata remains, generated configuration, controller repository/artifacts, SQL identity, and remote state. Do not promise that partial metadata will remain: inspect whether the workflow already removed it automatically and report that fact. Never run destroy, redeploy, reinstall, force cleanup, or delete live directories: the failed registration can point at pre-existing production data. Remove any remaining OBD metadata only after proving the cleanup action cannot touch remote services/data and obtaining configuration-removal authorization.
