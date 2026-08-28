# Tenant Creation

Use this workflow to plan, create, or inspect an OceanBase tenant. Read the installed `obd cluster tenant create --help` and `show --help` before constructing a command; option names, defaults, supported modes, and resource semantics vary by OBD and component version.

## Resolve the Tenant Plan

Record the exact deployment, OceanBase product form and component, cluster identity, target tenant name, compatibility mode, zone list, locality, replica and log-only-replica policy, primary zone, resource-unit count, minimum/maximum CPU, memory, log disk, minimum/maximum IOPS and IOPS weight, time zone, charset/collation, tablegroup when applicable, workload optimization choice, variables, and credential source.

Do not rely on a default tenant name or copy resource values from an unrelated topology. Check database-side capacity in every selected zone, including:

- available CPU and memory;
- log-disk capacity and required headroom;
- Unit and resource-pool occupancy;
- eligible OBServer nodes and zone placement;
- existing tenant, Unit, resource-pool, or account objects with the proposed names.

Stop when the requested locality cannot be satisfied, a zone lacks resources, or the intended tenant identity conflicts with a partial earlier attempt.

## Set the Network Allowlist Deliberately

Collect every source that must connect: application clients, OBProxy, OCP, the OBD controller when needed, backup/restore workers, and a controlled emergency-management path. Present the resulting IP/CIDR allowlist for review.

Verified OBD 4.7-era implementations can default `ob_tcp_invited_nodes` to `%` when tenant variables are omitted. Treat that as version-specific evidence, not a safe default. Pass the final reviewed allowlist in the same tenant-create request through the installed command's supported variables syntax. Use `%` only when it is itself the reviewed final value for an isolated environment and the user accepts that exposure.

Before submission, prove that the installed create workflow carries the final `ob_tcp_invited_nodes` value into initial tenant creation. If it cannot do so, stop. Never create with `%` or another temporary broad value and tighten it after creation; successful post-create correction does not make the exposure atomic.

## Protect the Initial Credential

Determine how the installed build accepts the tenant credential. Prefer a protected interactive input, permission-controlled file, or supported secret reference. If the only supported path is a command argument such as `--password`, disclose process-list and shell-history exposure and use an approved local execution procedure; never print the value.

When the installed OBD command offers only argv password input and argv exposure is not accepted, do not invent stdin, file-descriptor, environment-variable, or file options. A separately authorized fallback may create the tenant without the final password and immediately set it through an already available SQL client using a permission-controlled local credential file. This fallback is not atomic: require the final restricted allowlist in the original create request, define the bounded empty-password window and controller source, protect the file and process output, and record its retention/cleanup. Stop when that window is unacceptable or the intended password cannot be set without exposing it.

Verify the intended account and password immediately after creation. Tenant existence with a failed intended login is a partial result, not success.

## Construct and Execute

Use only options confirmed by the installed help. In the V4.6.0 command guide, Community Edition supports MySQL mode only; commercial capability must still be proved from the installed product/plugin. For OceanBase 4.0 and later use `--memory-size` rather than the legacy min/max-memory options. The documented minimum log-disk size is 2G, and `--optimize` requires a supporting OceanBase release (documented as 4.2.5 or later in this guide).

Choose one internally consistent placement model from installed help: do not combine locality, replica-count, zone-list, and primary-zone values that describe different topologies. A reviewed command can have this shape:

```bash
obd cluster tenant create <deploy_name> \
  --tenant-name=<tenant_name> \
  --mode=<compatibility_mode> \
  --zone-list=<zone_list> \
  --primary-zone=<primary_zone> \
  --replica-num=<replica_count> \
  [--logonly-replica-num=<log_only_replica_count>] \
  [--locality=<reviewed_locality>] \
  --unit-num=<units_per_zone> \
  --min-cpu=<minimum_cpu> \
  --max-cpu=<cpu> \
  --memory-size=<memory> \
  --log-disk-size=<log_disk> \
  --min-iops=<minimum_iops> \
  --max-iops=<maximum_iops> \
  --iops-weight=<iops_weight> \
  --time-zone=<time_zone> \
  --charset=<charset> \
  --collate=<collation> \
  [--tablegroup=<tablegroup>] \
  [--optimize=<workload>] \
  --variables=<shell_quoted_reviewed_variables> \
  [version-supported credential option; value supplied only through the approved local procedure]
```

Omit unsupported or unnecessary fields rather than guessing; bracketed fields above are conditional, and installed help decides whether a value is optional or mutually exclusive. The final `ob_tcp_invited_nodes` value is not optional merely because the CLI has a broad default: verify it is present in the redacted create plan before execution. Show the redacted final plan and obtain authorization for the tenant, resources, topology, credential procedure, variables, and network exposure immediately before creation.

Preserve the ordinary read-only inspection command from the installed interface:

```bash
obd cluster tenant show <deploy_name>
```

Use the version-supported tenant selector when the installed help exposes one. This output proves only OBD/database-reported tenant state; apply the database-side and data-plane checks below before declaring the tenant usable.

## Accept the Result

Verify all applicable layers:

1. the OBD task reached a successful terminal state and `tenant show` identifies exactly one intended tenant;
2. database-side tenant status is terminal and healthy rather than creating or deleting;
3. locality, replicas, primary zone, Units, resource pool, and effective resource values match the plan;
4. the effective `ob_tcp_invited_nodes` value equals the reviewed allowlist;
5. the intended account authenticates and can execute a bounded identity query in the intended compatibility mode, following [version-adaptive SQL evidence](../../references/sql-evidence.md);
6. no unexplained partial Unit, pool, user, or tenant object remains.

If the client times out or disconnects, do not classify the create as failed and do not submit it again. Under the same controller identity, correlate the Trace/task, `tenant show`, database tenant/Unit/pool objects, effective allowlist, and authenticated SQL state within a bounded deadline. Accept a server-side success only when the exact tenant passes every required layer; otherwise classify it as failed, still running, or unknown through the shared failure-recovery workflow.

If creation fails after any object appears, freeze retries and inventory the tenant, Units, pools, accounts, variables, trace, and real SQL state. Do not rerun creation or drop the partial tenant as generic cleanup; follow the shared failure-recovery reference.
