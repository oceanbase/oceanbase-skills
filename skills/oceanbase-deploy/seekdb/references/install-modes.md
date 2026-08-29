# SeekDB Install and Takeover Modes

Read the shared [product/capability gate](../../references/product-and-capability-resolution.md), [operation contract](../../references/operation-contract.md), [completion criteria](../../references/completion-criteria.md), and [failure recovery](../../references/failure-recovery-and-evidence.md) first. The commands on this page are mutating workflows, not discovery probes.

## Interactive Install Is a Compound Transaction

`obd seekdb install`, with or without a role option, requires a real TTY and continues through configuration, host precheck, optional host initialization, deployment, and start. It is not a configuration-only wizard. Before entering it, resolve and display the unused deployment name, exact OBD/SeekDB/plugin/artifact identities, target host and SSH identity, canonical paths, ports, resources, credentials, role/topology, every optional branch, and stage-specific acceptance checks.

In the inspected source baseline, the wizard has these material branches:

- Every successfully completed `dev=True` host precheck returns the same sentinel and reaches a **default-yes** initialization prompt, even when the precheck reports that no system parameters need changing. The prompt is not evidence that initialization is needed. That branch can stop/disable the firewall, disable SELinux, recursively change ownership of `/data/1` and `/data/log1`, disable transparent hugepages, rewrite MTU configuration and restart networking, and change kernel or limit settings. Explicitly answer **no** unless the exact initialization diff, outage, rollback, and ownership set were separately reviewed and authorized.
- An SSH connection or precheck-workflow failure returns a different false result, but the integrated caller does not propagate it: it skips the prompt and can continue into configuration, deploy, and start. Treat any such error as a hard manual stop and interrupt the wizard before the next stage; do not rely on the compound command's eventual exit status.
- The integrated path reconnects through a shared precheck whose failure message can include the SSH password. Prefer a key or agent route; when password authentication is required, use protected local input, restrict terminal/trace access, redact reports, and rotate the credential if it is exposed.
- The wizard can enable persistent systemd auto-start. In the inspected implementation, that branch creates a privileged unit and can broaden permissions on the deployment `tmp` directory. Keep it disabled unless the user requests persistent startup; that request authorizes the exact reviewed unit/permission diff, so show and verify the credential and rollback effects without asking for another confirmation solely because the change persists.
- The inspected path can place SSH and primary credentials in generated YAML. Keep the generated file permission-controlled, keep values out of chat and reports, and include its storage and later rotation in the credential plan.

Authorization for installation does not implicitly authorize host initialization, auto-start, modification of an existing primary, a primary outage, or start of the new target. Reject every unapproved branch rather than relying on the final confirmation prompt.

## Standalone Mode

```bash
obd seekdb install
```

This selects standalone mode when neither role option is present. Confirm the full generated configuration and every branch above. Accept only after deployment registration, artifact/path ownership, real process and listener identity, authenticated SQL, OBShell state when expected, and unrequested host/systemd changes have all been checked.

## Primary Mode

```bash
obd seekdb install --primary
```

Primary mode enables the RPC service required for standby synchronization. Verify the selected RPC address/port, firewall and routing path, TLS behavior when applicable, `enable_rpc_service`, `log_disk_size`, and replay capacity before deployment. The install still includes the compound host/deploy/start transaction above.

## Standby Mode

```bash
obd seekdb install --standby
```

Before entering the wizard:

1. Prove the selected primary and proposed standby are different machines/IPs, are both managed by the intended OBD controller as applicable, and that the primary is running and healthy.
2. Record the complete existing HA graph, primary version/artifact/configuration, `enable_rpc_service`, RPC endpoint, `memory_limit`, `log_disk_size`, replay state, clients, and availability constraints.
3. The V4.6.0/current inspected rule is **primary `log_disk_size >= 3 × max(primary memory_limit, standby memory_limit)`**. If it is smaller, the wizard can rewrite the existing primary's pending configuration and reload the primary automatically. Show the exact old/new value and reload impact and obtain separate configuration/availability authorization; otherwise exit before that branch.
4. If RPC is disabled, a plain restart is insufficient. The inspected wizard can set `enable_rpc_service=true`, apply the changed primary configuration, then stop and start the primary. Obtain authorization for that exact diff and outage before choosing “Restart now”; choose “Exit” otherwise.
5. Verify the actual synchronization source, role startup parameters, log capacity, and credential path. Do not infer readiness from deployment names.

After the integrated deploy/start, verify both old and new targets independently: primary role and availability, standby role, `log_restore_source`, replay/SCN advancement and lag, OBD graph, listeners, authenticated read behavior, client routing, and the absence of unapproved primary/host/systemd changes. A successful wizard exit is not sufficient.

## Same-Host Restriction

Primary and standby must use different IPs. In the inspected implementation, same-host conflict avoidance can suppress the `--role=STANDBY` startup parameter, causing the intended standby to start as a primary and preventing log synchronization. Stop rather than treating a same-host deployment as HA.

## Configuration-File Deployment

```bash
obd seekdb deploy <deploy_name> -c <reviewed_config.yaml>
obd seekdb start <deploy_name> --strict-check
```

Use this staged path for scripted or CI deployment after reviewing installed help, schema, artifacts, paths, credentials, and start behavior. Keep `enable_auto_start` disabled by default; enable it when persistent startup is requested after reviewing the resulting unit, permissions, credentials, and rollback. Preserve deploy and start as separate acceptance stages, and do not start after a partial deploy.

Setting `log_restore_source` in a configuration file does not make the process a standby in the inspected non-interactive workflow: it does not pass `--role=STANDBY`, so the process starts as a primary. Use the reviewed interactive standby workflow for real primary/standby creation, or a later installed workflow whose role behavior is proved. Do not advertise configuration-file deployment as a non-interactive HA substitute.

## Takeover of a Non-OBD Instance

The V4.6.0 baseline requires OBD 4.3.0 or later, SeekDB 1.2.0 or later, a healthy running instance, controller-to-target connectivity, and available OBShell `ocs.all_agent` metadata. These are necessary baseline conditions, not a substitute for checking the installed workflow.

Before constructing a takeover command:

1. Require the proposed deployment name to be completely unused immediately before execution. The inspected implementation accepts a `configured` or `destroyed` name, overwrites its `config.yaml`, `.data`, and `inner_config.yaml`, and can remove the registration after a later failure.
2. Identify every existing OBD/OCP/controller or automation owner. Resolve the SQL identity/version, real PID and binary hash, listeners, canonical home/data/redo paths, OBShell record, process/path owner, service/autostart state, and client routes. Stop on concurrent ownership or any mismatch.
3. Read `home_path` through the authenticated SQL/OBShell metadata path before invoking takeover. Match the `ocs.all_agent` record to the intended host and port, canonicalize the selected path, and verify it belongs to the intended process. When several records match the port, resolve the correct record explicitly rather than relying on first-row behavior. Use an SSH identity that can safely manage the resolved paths and process.
4. Inventory the exact repository candidates, downloads/installations, and controller metadata writes that can follow registration. Obtain separate network/package/controller authorization when any artifact is missing; takeover permission alone does not authorize an unreviewed package installation.
5. Prefer key-based/passwordless SSH. The inspected path accepts database and SSH passwords in argv and can persist them through plain generated YAML. If a non-empty credential is unavoidable, disclose process/history and metadata exposure, use only an approved private local procedure and protected controller, and define encryption/rotation and trace custody before execution. Stop when policy forbids that exposure.

Use only options confirmed by installed help; there is no `--home-path` option:

```bash
obd seekdb takeover <new_deploy_name> \
  -h <verified_host> \
  -P <verified_mysql_port> \
  --ssh-user <verified_process_owner> \
  --ssh-key-file <absolute_key_path>
```

Afterward, do not trust command exit or its internal display call. Independently verify the one new registration, generated configuration and permissions, exact artifact, process/PID/start time, listeners, canonical paths, SQL identity/version/role, OBShell state, OBD lifecycle readability, unchanged service availability, and absence of unrelated repository or deployment changes.

On failure, preserve the trace, before/after deployment-name state, generated metadata, package/repository state, remote process/path evidence, and credentials exposure record. Do not run destroy, retry takeover, prune metadata, or delete a live path as generic recovery. Remove residual controller metadata only after proving that the action cannot touch the pre-existing instance and obtaining configuration-removal authorization.

## Sources

- Official OBD V4.6.0 User Guide: SeekDB interactive deployment, role operations, and takeover prerequisites.
- Official OBD V4.6.0 Command Guide: `obd seekdb` command group.
- [Source-evidence boundary](../../references/source-baselines.md#source-evidence-boundary): `core.py` SeekDB install/takeover methods; interactive, host-tool, SeekDB HA, auto-start, and takeover plugins in the exact inspected checkout.
