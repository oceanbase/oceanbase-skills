# OceanBase Binlog Service

Use this workflow for an OBD-managed `obbinlog-ce` or commercial `obbinlog` deployment and for tenant Binlog instance operations under `obd binlog`. Do not confuse these with OBProxy/ODP, `oblogproxy`, or `oblogservice`.

## Resolve the Product Pair

Read the shared product/capability and operation gates first. Verify the installed `obd binlog --help`, component plugins, schemas, workflows, repository artifacts, and registered configurations. For the V4.6.0 baseline, the target OceanBase must be 4.2.1 or later and ODP 4.2.1 or later. The inspected source enforces community `obbinlog-ce` with community OceanBase and commercial `obbinlog` with commercial OceanBase; it also requires commercial `obbinlog` 4.3.2 or later. Treat these as version-scoped evidence and fail closed when the installed commercial artifacts or compatibility pair cannot be proved.

Deploy the Binlog service itself through the reviewed [configuration workflow](config-deployment.md), then use [lifecycle.md](lifecycle.md) for its component processes. A Binlog service deployment and a tenant Binlog instance are different objects with different states and cleanup boundaries.

## Preflight an Instance Operation

Resolve and display:

- the running Binlog deployment, exact `obbinlog-ce`/`obbinlog` artifact, servers, service paths, and generated Binlog directories;
- the running OceanBase deployment, exact non-`sys` tenant, cluster identity, and authenticated SQL endpoint;
- the associated ODP deployment, or the separately named ODP deployment when the installed `--obproxy-deployname` option is needed;
- Config Server/`obconfig_url`, or the installed-version support and exact value for `--root-server-list`;
- existing Binlog instances, replica count, consumers, retention/recovery expectation, and the `cdcro` account state.

Creation can create the `cdcro` user when absent, grant it access, generate a password, and persist the credential in the OceanBase deployment configuration. If an existing account requires `--cdcro-password`, the public option exposes the value in the process arguments. Do not print or retain that value; disclose the exposure, use an approved protected local execution method, and verify the resulting stored-secret protection separately.

## Operate Tenant Binlog Instances

Confirm every form with installed help and use explicit deployment and tenant identities:

```bash
obd binlog show <binlog_deploy_name> --deploy-name <oceanbase_deploy_name> --tenant-name <tenant_name>
obd binlog create <binlog_deploy_name> <oceanbase_deploy_name> <tenant_name> --replicate-num <count>
obd binlog start <binlog_deploy_name> <oceanbase_deploy_name> <tenant_name>
obd binlog stop <binlog_deploy_name> <oceanbase_deploy_name> <tenant_name>
```

For `show`, `--deploy-name` and `--tenant-name` must be supplied together or both omitted. Creation mutates the Binlog service, target tenant metadata/account state, and possibly ODP registration; authorize those separately. Start and stop affect every Binlog instance selected for that tenant, not one unnamed replica.

## Destructive Drop

`obd binlog drop <binlog_deploy_name> <oceanbase_deploy_name> <tenant_name>` closes all selected tenant Binlog instances and deletes generated retained Binlog files. Before presenting or running it, enumerate the exact instances, files/directories, consumers, recovery/retention boundary, and retained service/database objects. Obtain destructive authorization bound to that set immediately before execution. Do not use drop as failure cleanup or as a substitute for stop.

## Accept or Recover

After create/start/stop/drop, use the scoped `show` form and independently verify the selected tenant identity, instance count and state, Binlog service health, ODP/Config Server routing where applicable, and a representative approved consumer/data-plane check. Verify that other tenants and instances are unchanged.

On timeout or failure, preserve the OBD trace, Binlog deployment/configuration, target tenant/account state, instance list, generated paths, and consumer evidence. Re-inventory before retrying; create and drop are not safe blind retries. Never destroy the whole `obbinlog` deployment or delete its directories to repair one tenant instance.

## Sources

- Official OBD V4.6.0 Command Guide section 8.
- Official OBD V4.6.0 User Guide section 19.
- [Official public OBD V4.6.0 source baseline](../../references/source-baselines.md#official-obd-v460-baseline): `_cmd.py` `BinlogCommand` family; `core.py` Binlog instance methods; `plugins/obbinlog-ce/4.0.1/`.
