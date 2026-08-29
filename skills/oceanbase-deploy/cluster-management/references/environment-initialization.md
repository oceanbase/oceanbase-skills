# Host Environment Initialization

Use `obd cluster init4env` only when a version-supported deployment check identifies a host setting that the installed workflow is designed to initialize. It is a persistent operating-system mutation; stopping, destroying, redeploying, or pruning the deployment does not roll it back.

Do not use it to bypass port conflicts, occupied/overlapping paths, incompatible packages, architecture/runtime mismatches, cgroup or CPU-affinity constraints, insufficient resources, network failures, or unknown processes.

## Capability and Diff Gate

1. Record the OBD build, `cluster init4env --help`, deployment/configuration, selected plugins, targets, SSH identity, and current status.
2. Reproduce the relevant environment/strict check and preserve trace/evidence. Map each finding to a specific setting supported by the installed init workflow.
3. Inspect the installed workflow and capture every live value, persistent file, service/unit, account, ownership, or permission it can change.
4. Produce a per-host diff: current value, intended value, persistent location, runtime/reboot effect, exact rollback, and any reconnect/reboot requirement.
5. Detect duplicate or conflicting entries and other automation that owns those settings. Stop when the intended final value or owner is ambiguous.

Do not invent a dry-run option. A verified OBD 4.7.x surface does not expose one, so derive the diff from version-matched implementation evidence before executing. If the exact persistent changes cannot be identified, stop and report that host initialization cannot be bounded.

When `init4env` is a necessary, version-supported step of the user's requested execution, the request already authorizes its exact reviewed per-host persistent diff. Record the targets, effects, and rollback, but do not ask for a second confirmation merely because the changes persist. Optional or broader host changes remain out of scope.

## Execute and Verify

Use the installed syntax, commonly:

```bash
obd cluster init4env <deploy_name>
```

Preserve the trace. On every target verify live and persistent values, ownership/permissions, expected boot behavior, absence of duplicate/unrelated changes, and the original failed check. A successful exit is insufficient.

If a host is partially changed, freeze cluster retries. Before rollback, re-inventory every deployment, process, and organization-owned baseline that may now depend on the changed host settings. Complete only the original exact diff, or treat a reviewed itemized rollback as a new recovery action after proving that it will not break those dependencies. Do not broaden sysctl/limits edits, force the workflow, or redeploy.

Track host changes separately from deployment metadata. Deployment removal must not trigger automatic host rollback. When the deployment is later removed, report retained settings and re-inventory current dependants. Apply a rollback only when the user requests that separate recovery outcome; do not infer it from deployment removal.
