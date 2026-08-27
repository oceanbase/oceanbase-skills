# Reproducible Source Baselines

Use this reference to distinguish released, publicly reproducible implementation evidence from post-release development observations. Installed command, plugin, workflow, schema, registered state, and selected artifacts remain the runtime authority.

## Official OBD V4.6.0 Baseline

- Release: [OBD V4.6.0](https://github.com/oceanbase/obdeploy/releases/tag/v4.6.0), published with RPM `ob-deploy-4.6.0-3`.
- Immutable public source: [`oceanbase/obdeploy` commit `344fa3be9fd154303d878876531321c188c2870e`](https://github.com/oceanbase/obdeploy/tree/344fa3be9fd154303d878876531321c188c2870e).
- Telemetry call path: [`_cmd.py` constructs the background command](https://github.com/oceanbase/obdeploy/blob/344fa3be9fd154303d878876531321c188c2870e/_cmd.py#L766-L770), and [`ssh.py` executes command strings with `shell=True`](https://github.com/oceanbase/obdeploy/blob/344fa3be9fd154303d878876531321c188c2870e/ssh.py#L186-L208).

Source citations in this bundle that name V4.6.0 refer to that commit unless they link a more specific public revision. A file path or symbol names the inspected implementation location, not a guarantee that every packaged build or plugin exposes the behavior. Verify the installed artifact before execution.

The public V4.6.0 source constructs background telemetry as a shell command containing the deployment name and JSON error payload. It therefore fails this bundle's arbitrary-error-text safety gate. V4.6.0 documentation remains usable as a command/schema baseline, but V4.6.0 is not an executable compatibility claim for commands that can dispatch that telemetry path.

## Post-V4.6 Development Observations

Some reviewed development code is not present in the public V4.6.0 commit, including the standalone management-IP command and its persisted loopback Observer-identity model. Such observations may guide capability discovery but are not released-version evidence.

The reviewed development behavior uses these linked conditions:

- normal fresh `oceanbase-standalone` loopback identity requires component version `4.4.2.3` or later;
- a lower-version legacy deployment is considered only when it explicitly uses `local_ip=127.0.0.1` and the installed implementation can persist and verify that identity;
- `change-ip` requires a running, single-server `oceanbase-standalone` deployment with unchanged configuration and a verified loopback identity marker.

Do not infer an OBD release floor from those observations. Before emitting or executing `obd cluster change-ip`, prove the command, options, version gate, topology gate, and identity checks from the installed executable and its shipped implementation. If the installed source or equivalent vendor evidence is unavailable, provide only a non-executable capability note.

## Evidence Maintenance Rule

Do not cite an internal-only hash as reproducible evidence. For a released behavior, link an immutable public commit or tag. For an unreleased behavior, label it as non-release evidence, include the exact runtime checks needed to prove it, and keep execution fail-closed until the installed build supplies that proof.
