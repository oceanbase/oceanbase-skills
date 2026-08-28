# Commercial Standalone or Centralized Deployment Blueprint

Use this blueprint only when the installed OBD build and supplied commercial artifacts expose the requested standalone/centralized OceanBase form, commonly `oceanbase-standalone`. Do not model it as a one-node distributed `oceanbase` deployment.

## Required Inputs

- product terminology and intended operating mode confirmed by the user;
- component key, version, release, architecture, artifact hash, plugin identity, and approved source;
- supported host count and topology from the installed plugin;
- controller management address, Observer service identity, SQL/RPC/obshell addresses, and client routing;
- canonical home/data/log paths, storage mode, resources, non-database credentials, any explicitly supplied database bootstrap-password override, and lifecycle expectations; do not request an override when none was supplied;
- explicit persistent auto-start choice; keep the schema option false or unset unless requested and approved through the lifecycle systemd gate;
- version-specific evidence for takeover, management-IP change, upgrade, backup, monitoring, OCP, and other requested integrations; for the maintainer-observed normal `change-ip` path, the standalone component floor is `4.4.2.3`, subject to the exact installed-build and identity gates in [change-ip](../change-ip.md).

## Identity Gate

Standalone implementations can distinguish the OBD management address from Observer's self-registration or service address. Derive that behavior from the selected plugin/workflow. Do not hard-code loopback, copy distributed `local_ip`/`devname` rules, or use `change-ip` until the installed command proves support for the exact component and current state.

## Schema-Gated Structure

This is a non-executable rendering blueprint:

```yaml
user:
  username: <approved_ssh_user>
  <schema-supported-auth-key>: <protected_ssh_credential_reference>

<verified-commercial-standalone-component-key>:
  version: <locked_version_if_supported_here>
  release: <locked_release_if_supported_here>
  servers:
    - ip: <obd_management_ip>
      <other-required-server-identity-keys>: <schema-derived-values>
  global:
    <verified-home-path-key>: <canonical_home_path>
    <verified-data-and-log-keys>: <canonical_paths_or_storage_values>
    <verified-sql-rpc-obshell-keys>: <approved_addresses_and_ports>
    <verified-resource-keys>: <approved_values>
    # Omit the verified database bootstrap-credential key by default so the
    # proved OBD workflow generates it; add it only for an explicit protected override.
```

Do not add distributed zones, OBProxy, monitoring, OCP, Config Server, or another component unless the installed standalone workflow supports it and the user requested the resulting capability.

## License Management

The OBD V4.6.0 command guide limits the top-level license commands to OBD-deployed centralized commercial OceanBase whose package/component is `oceanbase-standalone`. Do not offer them for Community Edition, commercial distributed OceanBase, an unmanaged process, or another similarly named product.

Before `load`, verify the exact deployment and installed component identity, current license state, requested license file provenance, checksum, product/customer/scope binding when inspectable, validity period, owner/mode, and approved custody. Treat the license file and displayed license details as sensitive commercial material: do not copy them into the Skill, logs, chat, or reports. Loading changes the deployment's effective license state and requires authorization bound to that deployment and file hash.

The installed workflow can copy the controller file to `<home_path>/license.key` on every configured server before loading it. Resolve the source and every destination, confirm they belong to the intended deployment, inspect an existing destination before overwrite, and include the persistent host copies and effective license change in the authorization. Preserve the prior checksum and file metadata when a rollback copy is required; do not assume OBD tightens permissions or removes the transferred files.

Use only the installed long-option syntax:

```bash
obd license show <deploy_name>
obd license load <deploy_name> --file=<approved_license_file>
```

After load, verify every target `license.key` has the intended checksum, type, owner, and mode, then run the supported redacted show/health checks and verify the deployment remains manageable and its licensed capability/validity matches the intended file. A successful command exit without both per-server transfer and effective-license checks is partial. On failure, inventory changed and unchanged servers and preserve the original license state, before/after destination metadata, source checksum, trace, and service state. Do not retry, load another key, delete a host copy, restore an old copy, redeploy, or replace metadata until the observed partial state supports a separately authorized recovery.

## Acceptance

Verify the management address and Observer identity separately, actual listeners, authenticated SQL, the installed artifact hash, storage/path ownership, and standalone product identity. A successful direct SQL connection does not prove that OBD registered the intended management identity or that later lifecycle operations are supported.
