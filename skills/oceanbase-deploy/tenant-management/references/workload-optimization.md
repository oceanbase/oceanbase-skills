# Tenant Workload Optimization

Use this workflow for `obd cluster tenant optimize`. Optimization changes tenant or cluster parameters; it is not a read-only label change.

## Resolve the Change

Read the installed `optimize --help` and selected component plugin. Record the deployment, tenant, current workload/scenario, health, application workload, and the exact supported scenario values. Do not use an open-ended value such as `etc.` or copy a scenario list from another version.

Determine the parameter set the installed workflow can change. For each parameter, capture the current effective value, intended value, scope, persistence, and whether it is dynamic or restart-sensitive. If the actual diff cannot be established, stop and request a controlled environment or a separately reviewed manual tuning plan.

Determine the required tenant-root credential option from installed help. The verified V4.6.0/current command exposes the long option `--tenant-root-password`; use that exact name when the selected build confirms it rather than emitting a generic credential placeholder. Prefer protected input. If the selected command accepts the value only in argv, disclose process-list/shell-history exposure and use an approved local procedure; do not embed the password in examples, output, or saved transcripts.

Before optimization, use the same protected tenant-root credential source that will supply the OBD option to open an authenticated SQL session to the exact tenant. Verify the endpoint, tenant identity, compatibility-mode administrator identity, and current effective values of every parameter in the proposed diff. Do not treat a successful system-tenant connection or an empty-password assumption as tenant authentication.

## Execute

After reviewing the exact parameter diff and impact, use the installed syntax, typically shaped as:

```bash
obd cluster tenant optimize <deploy_name> <tenant_name> \
  --optimize=<reviewed_scenario> \
  --tenant-root-password=<value_supplied_only_through_the_approved_local_procedure>
```

Do not treat permission only to benchmark or create a tenant as permission to optimize it. When the user explicitly requested optimization of the identified tenant, that request authorizes the reviewed scenario's ordinary persistent parameter changes; do not ask again solely because they persist. Ask again only when the resolved target, parameter diff, restart/outage, or other impact expands beyond the requested optimization.

## Accept and Restore

Reconnect to the exact tenant using the same credential source and verify the task, authenticated tenant identity, effective database-side parameter values, tenant status, SQL availability, application routing, and representative workload health. Report any parameter whose effective value differs from the requested scenario. Revoke or rotate a short-lived credential according to the predeclared plan after both the OBD operation and postflight SQL verification are complete.

Restore the previous values only when the user requested temporary tuning or recovery from a failed change. Restore only values changed by this operation and verify them independently.
