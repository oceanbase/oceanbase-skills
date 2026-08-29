# Standalone Management-IP Change

No released-version availability baseline or minimum OBD version is established here for `change-ip`. Use `obd cluster change-ip` only when the installed command help and implementation prove support for the exact deployment; do not infer availability from a development branch name, tag, product version, or nearby release.

In the maintainer-observed development implementation, the normal fresh-deployment path requires the OceanBase component to be `oceanbase-standalone` version `4.4.2.3` or later. That component-version floor enables the loopback Observer identity required by management-IP replacement; it is separate from the OBD version that provides the command. A pre-`4.4.2.3` standalone deployment is not supported by version inference. It may qualify only when the installed implementation explicitly recognizes a legacy configuration with `local_ip=127.0.0.1` and has persisted and live-verified the same loopback identity. See the [development source evidence boundary](../../references/source-baselines.md#post-v460-development-observations).

The reviewed implementation additionally requires a running deployment, unchanged registered configuration with no pending temporary config, exactly one `oceanbase-standalone` OceanBase component, exactly one configured server whose management address is the old IP, and a verified loopback Observer-identity marker. Treat every condition as version-specific and re-prove it from the installed build.

This operation changes OBD's management address for the supported deployment. It is not a host replacement, distributed Observer addition/removal/migration, VIP move, or generic change to `local_ip`/`devname`.

## Identity and Scope Gate

1. Resolve controller, `OBD_HOME`, deployment, product/component, status, registered host, old management IP, and intended new IP.
2. Prove old and new IP belong to the same intended physical host. Stop if machine identity, paths, process ownership, or storage identity changes.
3. Distinguish OBD management IP from SQL/RPC/obshell addresses, Observer self-registration identity, `local_ip`, `devname`, OBProxy/VIP/OCP endpoints, DNS, and certificates. List consumers that embed the old IP.
4. Verify the new IP exists on the target, is reachable from controller and peers, is not owned by another host, and satisfies routing, firewall, SSH host-key, port, certificate, and name-resolution requirements.
5. Capture registered configuration and metadata with secrets redacted, real processes/listeners, SQL/API health, cluster identity, and the rollback address.

## Dry Run and Execute

If installed help exposes the public dry run, use the exact confirmed syntax, schematically:

```bash
obd cluster change-ip <deploy_name> \
  --old-ip=<old_ip> \
  --new-ip=<new_ip> \
  --dry-run
```

Resolve every warning. A successful dry run authorizes nothing. Show the final mapping, affected components, connectivity impact, external configuration OBD will not update, and rollback plan; obtain availability/configuration authorization.

Execute only with the installed confirmation option after that gate. Do not infer an option spelling from this document if help differs.

## Acceptance and Recovery

Verify registered management identity, real processes and listeners on the same intended host, component status, authenticated SQL/API health, peer reachability, and a client path. Search deployment-owned configuration for unexplained old-IP references without displaying secrets; separately report external consumers that still require updates.

On partial failure, preserve trace, backup metadata produced by the workflow, before/after registration, processes/listeners, and both routes. Do not manually edit `.obd`, reverse the command, restart all components, or redeploy until the observed state proves the action safe and its impact is authorized.
