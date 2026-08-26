# Standalone Management-IP Change

Use `obd cluster change-ip` only when installed help/workflow proves support for the exact deployment. In one verified OBD 4.7.x implementation it is limited to a running `oceanbase-standalone` deployment and exposes old/new IP, dry-run, and confirmation options; treat those details as version-specific.

This operation changes OBD's management address for the supported deployment. It is not a host replacement, distributed Observer migration, scale operation, VIP move, or generic change to `local_ip`/`devname`.

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
