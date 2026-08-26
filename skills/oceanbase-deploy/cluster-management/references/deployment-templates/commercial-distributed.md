# Commercial Distributed Deployment Blueprint

Use this blueprint for an authorized commercial distributed OceanBase artifact set. The component is commonly named `oceanbase`, but the installed OBD plugin and repository are authoritative. Commercial support does not permit substituting public community packages or fabricating proprietary fields.

## Required User and Artifact Inputs

- approved repository, all-in-one bundle, or local artifacts with provenance and access/license boundary;
- exact OceanBase version, release, architecture, hash, plugin/workflow identity, and full dependency closure;
- supported upgrade/deployment compatibility evidence for OBD, OS/runtime, OBProxy, OBAgent, OCP, Config Server, log service, and storage mode as selected;
- cluster identity, multi-zone topology, host failure domains, paths, ports, resources, and credential sources;
- explicit persistent auto-start choice; keep the schema option false or unset unless requested and approved through the lifecycle systemd gate;
- explicit choice between the plugin's supported local/shared-nothing layout and any supported shared-storage layout.

If a required artifact, schema, dependency, or entitlement cannot be inspected, stop. Do not create a hybrid commercial/community deployment.

## Version Gate

Inspect the exact commercial plugin delivered with the target OBD/artifact set. Record all required parameters, defaults, generated values, topology constraints, supported lifecycle workflows, and whether any operation invokes proprietary bootstrap or storage steps.

If shared storage is requested, read [../shared-storage.md](../shared-storage.md) before rendering paths. If `oceanbase.ai` or `oblogservice` is requested, keep each as an explicit component workflow rather than treating it as an ordinary Observer field.

## Schema-Gated Structure

This blueprint is intentionally non-executable until every bracketed item is replaced from the installed commercial schema.

```yaml
user:
  username: <approved_ssh_user>
  <schema-supported-auth-key>: <protected_ssh_credential_reference>

<verified-commercial-distributed-component-key>:
  version: <locked_version_if_supported_here>
  release: <locked_release_if_supported_here>
  servers:
    - name: <server_name_if_supported>
      ip: <management_ip>
      <verified-zone-or-failure-domain-key>: <approved_value>
  global:
    <verified-home-path-key>: <canonical_home_path>
    <verified-data-layout-keys>: <approved_local_or_shared_storage_values>
    <verified-log-layout-keys>: <approved_values>
    <verified-service-address-and-port-keys>: <approved_values>
    <verified-resource-keys>: <approved_values>
    <verified-bootstrap-credential-key>: <protected_secret_reference>
```

Maintain a separate artifact lock manifest containing component, version, release, architecture, hash, source, and plugin identity. Prove the repository resolves to it before deployment and verify the installed binaries afterward.

## Commercial Acceptance

In addition to ordinary cluster checks, verify the effective storage mode, licensed/proprietary component identity, intended topology and failure domains, actual package hashes, and every commercial component data plane. Do not declare support or success merely because OBD parsed the YAML or found a package with the same version string.
