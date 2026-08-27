# Cluster and Component Upgrade

Use the supported upgrade workflow for a version transition that requires compatibility checks or upgrade scripts. Use [component-reinstall.md](component-reinstall.md) only for a supported artifact/release reassignment that is not an upgrade.

## Build the Upgrade Path

1. Record the current OBD build, product form, component/plugin versions, per-node binary versions/checksums, repository hashes, deployment configuration, topology, health, tenants, dependencies, and backup state.
2. Read the installed `obd cluster upgrade --help` and exact source/target component workflows.
3. Establish a version-matched supported path for every hop. Check OBD/plugin, OceanBase, OS/runtime, data format, OBProxy, OBAgent, monitoring, OCP, Config Server, log service, and storage-mode compatibility as applicable.
4. Enumerate repository candidates for the final version and every intermediate upgrade hop by component, version, release, architecture, hash, and source. Select exactly one reviewed candidate per hop. Do not describe `--usable` as a strict hash selector: in inspected OBD code it is a priority list, and when none of its hashes match, resolution falls back to all non-disabled candidates. An absent requested hash can therefore select a different sole candidate.
5. For an exact-hash requirement, prove every selected hop hash exists and matches its component/version/release/architecture, freeze the candidate set against repository refresh or concurrent mutation, pass all reviewed hop hashes to the installed `--usable` list, and exclude every other candidate for the involved versions with `--disable`. Re-enumerate immediately before execution. If any selected hash can disappear, a new candidate can appear, or the installed build cannot make a no-match fail closed, stop: that build cannot satisfy an exact-hash upgrade safely.
6. Determine from the installed workflow whether the upgrade is rolling, component-wide, or full-outage. Record order, health gates between units, expected mixed-version window, irreversible stage, and rollback artifact/data requirements.
7. Verify a restorable backup appropriate to the operation and separately verify metadata/configuration snapshots. A package downgrade is not necessarily a data-format rollback.

Commercial and community paths must be resolved independently. Do not infer commercial upgrade support from an equivalent community version string, or select public community packages when a commercial artifact is missing.

## Preflight and Authorization

Refresh product-side topology, tenant and replication health, active workloads/tasks, disk/log capacity, package integrity, network/SSH, and dependency health. Define stop thresholds for each unit/hop.

Show the exact source and target identities, upgrade sequence, rolling/outage behavior, client impact, backup evidence, irreversible boundary, and recovery plan. Obtain availability/configuration authorization after this final health gate.

## Execute

Construct the command only from installed help, for example:

```bash
obd cluster upgrade <deploy_name> \
  --component=<component> \
  --version=<target_version> \
  --usable=<comma_separated_reviewed_hashes_for_every_hop> \
  --disable=<all_other_frozen_candidate_hashes_for_involved_versions>
```

This command shape is usable only after verifying the installed long options and the fail-closed candidate-set procedure above; `--usable` alone is insufficient. Preserve every trace ID. Between units or components, verify the expected version state, process/listener health, cluster topology, replication, and authenticated data plane before continuing.

## Acceptance

Verify:

- registered target version/release/hash and actual binary/package identity on every selected node;
- no unexpected mixed version, plugin, or repository state;
- process start times, listeners, OceanBase topology and upgrade status;
- authenticated SQL and representative read/write behavior;
- OBProxy, OCP, monitoring, Config Server, log service, and shared-storage integrations selected by the deployment;
- configuration and tenant/data integrity, plus no unexplained residual task or artifact.

## Failure and Rollback

Stop the sequence at the first failed health gate. Preserve the trace, completed unit/hop, real versions, processes, logs, upgrade metadata, and data-plane state. Use only the version-matched documented resume/recover/rollback path.

Do not blindly rerun, reinstall the old RPM, force a downgrade, restart every node, or redeploy. If the target workflow crossed an irreversible data/schema stage, report that boundary and use the proved recovery plan rather than describing binary replacement as rollback.
