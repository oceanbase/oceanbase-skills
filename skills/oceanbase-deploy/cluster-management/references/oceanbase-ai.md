# Commercial `oceanbase.ai` Component

Use this workflow only when the user requests the commercial OceanBase product/component whose OBD key is proved by the installed build, commonly `oceanbase.ai`, or when an existing deployment already contains it. Do not reinterpret a generic AI or unrelated product request as permission to deploy this component.

## Capability and Artifact Gate

1. Record OBD build, installed `oceanbase.ai` plugin/schema/workflows, component version/release/architecture/hash, artifact source, and commercial access/license boundary.
2. Confirm the component's product role, supported topology, OceanBase/OBD/OS/runtime dependencies, storage modes, network services, resource minimums, lifecycle commands, and integrations from version-matched evidence.
3. Identify required targets, zones/failure domains, canonical paths, ports, CPU/memory/disk or accelerators only if the plugin actually requires them, credentials, and optional dependencies.
4. Verify repository/artifact closure. If the installed OBD package contains a constant or command branch but no deployable plugin/artifact/schema, report that capability as unavailable; do not synthesize it.

Do not substitute `oceanbase-ce`, `oceanbase`, `oceanbase-standalone`, another product, or a public community package when the commercial artifact is missing.

## Schema-Gated Deployment

Use [config-deployment.md](config-deployment.md) and the exact installed `oceanbase.ai` schema. Treat all field names, topology constraints, bootstrap behavior, and dependencies as version-specific. Build a non-secret artifact lock manifest and a fully rendered YAML only after schema validation.

If an existing deployment supports incremental component addition, follow [scale-and-components.md](scale-and-components.md); otherwise stop. Do not redeploy another OceanBase product merely to introduce `oceanbase.ai`.

If the component depends on `oblogservice`, read [oblogservice.md](oblogservice.md) and validate its direction, minimum-version, bootstrap, and resource constraints from the installed workflow.

## Acceptance and Lifecycle

Verify exact artifact identity, registered topology/configuration, processes/listeners/paths, authenticated product-specific SQL/API readiness, storage mode, and every explicitly requested integration. A generic HTTP health endpoint or an ordinary OceanBase process is not sufficient unless the selected product workflow defines it as acceptance.

For configuration, scale, upgrade, reinstall, or removal, use the corresponding cluster reference and the installed component workflow. Preserve commercial data and artifact boundaries. On failure, preserve trace, plugin/configuration, processes/listeners, paths, logs, and data-plane evidence; do not fall back to a different product form or community package.
