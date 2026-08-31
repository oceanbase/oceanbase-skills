# Current Skill-Version Unsupported Capabilities

This reference defines the intentional coverage boundary of the current `oceanbase-deploy` Skill version. It does not claim that the underlying OBD product or a future Skill version cannot provide the listed capabilities.

When a request requires one of the capabilities below, report `UNSUPPORTED — the current Skill version does not support this workflow` before proposing or executing commands for it. Do not reconstruct a deleted workflow from repository history, route it through a generic component/tool command, or probe a live system merely to invent an execution path. A supplied configuration or already available local evidence may still be reviewed, but no executable plan is provided by this Skill version.

If a request mixes retained and unsupported work, handle the retained portion through its normal route and report the unsupported portion separately.

## Cluster and Product Workflows

- commercial distributed OceanBase, commercial standalone/centralized OceanBase, related license handling, and commercial-tenant operations;
- interactive deployment and the `obd demo` or `obd perf` shortcut workflows;
- `cluster redeploy`, takeover of an already running cluster, `cluster init4env`, deployment auto-start/systemd management, and standalone management-IP change;
- adding or removing Observer servers from an existing registered deployment;
- OCP CE, commercial OCP, OCP Express, OCP takeover, and OCP-aware lifecycle operations;
- Alertmanager, `oceanbase.ai`, `oblogservice`, `oblogproxy`, `obbinlog-ce`/`obbinlog`, tenant Binlog/CDC, and OMS workflows;
- shared-storage deployment topologies;
- OBD-managed `local_ip`/`devname` changes, VIP management, or external load-balancer configuration;
- OBD-managed SeekDB deployment, lifecycle, takeover, HA, or monitoring;
- generic component add/delete outside `obproxy-ce`, `obagent`, `prometheus`, `grafana`, and `ob-configserver`;
- component upgrade outside the retained OceanBase Community Edition rolling-upgrade workflow, and component reinstall outside the retained `obproxy-ce` exact-hash workflow.

## Controller Workflows

- uninstalling OBD or an owning OceanBase All-in-One installation;
- OBD stored-credential encryption or encryption-passkey management;
- generic dynamic-tool update or uninstall;
- deployment-bound helper commands such as `obd tool command`, `obd tool db_connect`, or `obd tool dooba`;
- top-level `obd host` precheck, initialization, or user-management operations;
- OBD Web or its API;
- developer mode, generic environment/lock/transfer-policy administration, and telemetry administration.
