# OBD-Managed `oblogproxy`

Use this workflow for the component named `oblogproxy`, the legacy OceanBase CDC/log-proxy service. It is not OBProxy/ODP, `obbinlog-ce`/`obbinlog`, or the commercial `oblogservice` used by `oceanbase.ai`. The V4.6.0 guide notes that the product evolved into obbinlog from oblogproxy 4.0.1; do not rename or migrate an existing deployment without a product-supported plan.

## Capability and Dependency Gate

Read the shared product/capability and operation gates. Inspect the installed `oblogproxy` schema, workflows, repository artifact, and released example that matches the requested topology. Resolve whether the request is a new full deployment, a standalone `oblogproxy` deployment, or a component add to an existing OceanBase deployment.

For a Binlog Service mode, verify the exact OceanBase, OBProxy/ODP, and Config Server dependencies and the installed compatibility rules. Resolve the `cdcro@sys` user, least privileges, credential ownership, and protected delivery. Do not copy a password into reusable YAML, command output, or reports. If the plugin only renders plaintext or process arguments, disclose the exposure and stop unless the user approves an appropriately protected local method and credential lifecycle.

## Deploy or Change

For a new configuration, use the common [configuration deployment](config-deployment.md) with only installed-schema keys. For an explicitly supported component add/delete, use [component changes](component-changes.md); do not use redeploy. Confirm the installed OBD minimum/version-specific command because V4.6.0 documents different minimum OBD versions for full deployment and component add.

Before execution, show the exact artifact, servers, service and optional Binlog paths, ports, dependencies, users/credentials, consumers, retention boundary, and component-add impact. Do not infer that a generic `oblogproxy` process owns already generated Binlog data.

## Accept or Recover

Verify the registered component/artifact, process/listener, authenticated health check, dependency connectivity, `cdcro` access without revealing its value, and a representative approved CDC/data-plane operation. Verify other cluster components and tenants remain unchanged.

On failure, preserve the trace, registered configuration, dependency/account state, processes, listeners, and files. Do not switch to `obbinlog`, recreate `cdcro`, redeploy OceanBase, or delete Binlog paths as generic recovery.

## Sources

- Official OBD V4.6.0 User Guide section 20 and its released configuration examples.
- [Source-evidence boundary](../../references/source-baselines.md#source-evidence-boundary): `plugins/oblogproxy/2.0.0/` and matching workflows in the exact inspected checkout.
