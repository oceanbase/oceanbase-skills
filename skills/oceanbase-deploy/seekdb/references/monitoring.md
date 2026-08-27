# OBD-Managed SeekDB Monitoring

Use this workflow only when OBD will manage monitoring components for a SeekDB deployment. It covers OBAgent collection, Prometheus storage/query, and Grafana visualization; deploy only the layers the user requested.

## Resolve the Installed Capability

Record the exact OBD build and `OBD_HOME`, SeekDB deployment and role, registered configuration, component plugins/workflows, repositories and artifact hashes, and current monitoring ownership. Resolve hosts, ports, canonical home/data/log paths, resource and retention budgets, TLS/authentication, firewall routes, and existing collectors or dashboards before rendering configuration.

Do not reuse an OceanBase monitoring YAML by renaming its database component. The V4.6 release record describes SeekDB monitoring with OBAgent, Prometheus, and `ob-dashboard`, while the inspected 4.7 development source contains a Grafana-specific integration. Treat those as different versioned capabilities and select only components proved by the installed schemas, examples, and workflows.

In the inspected 4.7 implementation, the automatic integration requires the components to be visible in the same deployment configuration and uses this dependency chain:

```text
obagent depends on seekdb
prometheus depends on obagent
grafana depends on prometheus
```

Re-prove that chain from the installed build. A separately registered monitoring deployment is not automatically equivalent: the inspected Prometheus and Grafana plugins choose SeekDB-specific behavior by detecting `seekdb` in their own deployment configuration.

## Account and Secret Side Effects

When OBAgent depends on SeekDB, the inspected generator can create `seekdb_monitor_user` and a random `seekdb_monitor_password` in generated configuration. During bootstrap on a non-standby instance, the SeekDB plugin can create that SQL user and grant `SELECT` on `oceanbase.*`. Surface the exact account, privilege, secret-storage path, and creation stage before authorization; a request for charts is not permission to reuse root credentials or expose an auto-generated password.

The same inspected generator can include generated global key/value pairs in verbose output. Use a dedicated monitor credential, restrict terminal, OBD log, and trace access, redact the value from reports, and rotate it if the selected build exposes it. Do not delete or rewrite diagnostic evidence as cleanup.

Use a protected local secret path and keep the value out of chat, reusable YAML, process listings when avoidable, display output, and reports. On a standby or an existing deployment, verify the actual account source and role behavior rather than assuming bootstrap created or replicated it. Authenticate the monitor account directly and prove its effective privileges are no broader than the installed workflow requires.

The inspected OBAgent path disables ordinary OceanBase collection and enables SeekDB collection when it depends on SeekDB. Verify the effective values rather than setting both pipelines active by analogy.

## New Deployment

For a new deployment, render one complete, reviewed configuration containing SeekDB and exactly the requested monitoring dependency chain. Validate every field with the installed component schemas; include no placeholder or unrequested component. After applying the shared authorization rules, the command shape is:

```bash
obd seekdb deploy <deploy_name> -c <reviewed_config.yaml>
obd seekdb start <deploy_name> --strict-check
```

Keep deploy and start as separate stages. Do not start after a partial deploy, and do not use the interactive install wizard as a substitute for a reviewed multi-component configuration.

## Existing Deployment

Do not redeploy a running SeekDB deployment to add monitoring. First prove from installed help and workflows whether in-place component addition supports the exact SeekDB/component versions and whether it restarts or rewrites any existing component. When proved, the public command commonly has this shape:

```bash
obd cluster component add <deploy_name> --config=<reviewed_monitoring_increment.yaml>
```

Read the [component-add restart and recovery gate](../../cluster-management/references/scale-and-components.md#add-a-component) before execution. The increment must preserve the existing SeekDB configuration and add only the requested dependency chain. If the installed build cannot prove safe in-place addition, stop and report that limitation; do not use `redeploy`, hidden metadata edits, or a separate deployment while claiming the same automatic SeekDB integration.

## Version-Specific Data Path

For the inspected 4.7 implementation, verify all of these installed behaviors before relying on them:

- OBAgent uses the generated SeekDB monitor credential and enables the SeekDB metrics pipeline;
- Prometheus uses SeekDB rules and scrapes `/metrics/seekdb/basic` and `/metrics/seekdb/extra`, not the ordinary `/metrics/ob/*` paths;
- Grafana provisions the SeekDB dashboard and its datasource points to the intended Prometheus instance.

Do not hard-code those paths or dashboard names for another plugin version. Record target-file generation and synchronization ownership, Prometheus retention and disk growth, Grafana persistence, and every HTTP/basic-auth or TLS boundary.

## Acceptance and Failure

Verify each requested layer independently:

1. SeekDB retains the intended role, configuration, SQL availability, and client routing.
2. Every requested monitoring component is registered once and has the intended process, listener, path owner, artifact, and effective configuration.
3. The monitor SQL account authenticates with the intended least privilege and its secret is not exposed.
4. OBAgent returns current SeekDB samples for the intended instance; ordinary host metrics alone are insufficient.
5. Every intended Prometheus target is healthy and a known SeekDB series returns current samples with the correct labels.
6. Grafana uses the intended datasource and the SeekDB dashboard renders current data; a login page alone is insufficient.
7. No unrequested OceanBase pipeline, duplicate collector, account, component, listener, or monitoring deployment was created.

On failure, preserve the OBD trace, before/after configuration, account and privilege state with secrets redacted, component processes/listeners, generated target/rule files, Prometheus target/query evidence, Grafana datasource/dashboard state, and unchanged SeekDB health. Do not delete monitoring data, drop the monitor account, remove components, or redeploy as generic recovery. Removal of a component, retained metrics, or the SQL account is a separate ownership and authorization decision.

## Maintainer Evidence

The inspected 4.7 behavior is implemented in `plugins/seekdb/1.0.0/generate_config_pre.py`, `plugins/seekdb/1.2.0.0/bootstrap.py`, `plugins/obagent/1.3.0/obagent_const.py`, `plugins/prometheus/2.37.1/start_pre.py`, and `plugins/grafana/7.5.17/init.py`. Use the installed plugin versions when applying these version-specific details.
