# OceanBase Config Server

Use this workflow for the OBD component commonly named `ob-configserver`. It supplies registered OceanBase cluster metadata to supported consumers; component process health, metadata registration, and consumer retrieval are separate outcomes.

## Capability and Scope Gate

1. Verify the exact component key, installed plugin/schema/workflow, package version/release/architecture/hash, and repository source.
2. Establish version compatibility with the selected community or commercial OceanBase product, OBProxy/ODP, and the exact metadata protocol expected by each consumer.
3. Record deployment, Config Server nodes, listen and advertised addresses, ports, canonical home/log/storage paths, resources, TLS/authentication or network-access boundary, and every intended consumer.
4. Check host identity, path/port conflicts, disk/resources, network reachability, metadata-store ownership, and exposure boundary.
5. Decide whether this is a combined new deployment, incremental component add, Config-Server-only deployment, scale/restart/reload, address replacement, or deletion. Use only the installed supported workflow.

Do not add Config Server solely because it appears in a bundle or an unrelated product error; first prove that the requested consumer and version require it.

## V4.6.0 Structural Baseline

Derive every executable value and key from the installed `ob-configserver` schema. The released V4.6.0 example and plugin establish this real-key structural baseline:

```yaml
ob-configserver:
  servers:
    - CHANGE_ME_CONFIG_SERVER_IP
  global:
    listen_port: 8080
    server_ip: CHANGE_ME_REVIEWED_BIND_ADDRESS
    home_path: CHANGE_ME_CONFIG_SERVER_HOME
    log_level: info
    log_maxsize: 30
    log_maxage: 7
    log_maxbackups: 10
    log_localtime: true
    log_compress: true
    storage:
      database_type: sqlite3
      # connection_url: CHANGE_ME_ABSOLUTE_SQLITE_URI
```

This fragment is not deployable until every placeholder, host, path, exposure decision, and installed-schema default is reviewed. In the V4.6.0 schema, `storage.database_type` supports `sqlite3` or `mysql`. A SQLite URL can be omitted to use the version's derived database under `home_path`; a MySQL or OceanBase MetaDB URL can contain a username and password, so construct it only in a protected local procedure and never place the literal URI in reusable YAML, chat, or reports. Verify the MetaDB database and least-privilege DDL/DML account separately.

For multiple Config Server nodes, configure and prove a reachable load balancer before setting `vip_address` and `vip_port`. Do not use an arbitrary server address as a VIP. Verify backend health, failover, advertised URL, metadata-store concurrency, and every consumer path.

## Select One V4.6.0 Topology Branch

### Combined OceanBase, ODP, and Config Server

The official V4.6.0 community example uses these dependency edges:

```yaml
oceanbase-ce:
  depends:
    - ob-configserver
  global:
    appname: CHANGE_ME_NONEMPTY_CLUSTER_NAME

obproxy-ce:
  depends:
    - oceanbase-ce
    - ob-configserver
```

Use the exact database and proxy component keys exposed for the selected community or commercial product; do not rename the community example speculatively. A non-empty database `appname` is required for registration in this branch. Omit `rs_list` when the reviewed intent is for ODP to start through the Config Server URL; verify the installed proxy schema derives that URL and preserves the required database/proxy authentication relationship.

### Add Config Server to an Existing OBD Deployment

Use a config file containing only the reviewed Config Server stanza and the installed long option:

```bash
obd cluster component add <deploy_name> --config=<config_server.yaml>
```

Do not redeploy merely to add Config Server. In the V4.6.0 documented flow, a deployment with ODP can prompt to restart `obproxy-ce,oceanbase-ce` so ODP changes from root-server-list mode to the Config Server URL; declining leaves the prior ODP mode in place. Resolve the exact installed restart set, outage, and consumer transition, then authorize it separately.

Do not add `--confirm` as a generic non-interactive flag. In inspected implementations it can accept restart-causing behavior rather than mean “do not restart”; without a proved selector, an empty restart selection can widen to the whole deployment. Stop when the exact transition cannot be controlled.

### Deploy Config Server Alone

Deploy and start the reviewed `ob-configserver` configuration as its own OBD deployment. It does not register an existing database merely by becoming healthy. Register only an already running, identified OceanBase cluster through the version-supported `obconfig_url`/SQL workflow, then configure each intended ODP with the reviewed `obproxy_config_server_url`. Treat the database reload/restart and ODP route change as separate availability/configuration operations. Preserve the previous endpoint or `rs_list` route until rollback is proved.

## Acceptance and Removal

After deployment or change, verify:

1. exact OBD registration, artifact, process, listener, bind/advertised address, path ownership, and metadata-store identity;
2. a bounded request for the supported `GetObProxyConfig` action returns the expected registered cluster identity, with approved TLS/authentication when supported and network access restricted when it is not;
3. the intended database is registered under the exact non-empty application/cluster identity and stale or unrequested clusters are absent;
4. every intended ODP retrieves the current metadata and its authenticated SQL data plane reaches the intended cluster;
5. direct database access and unrelated consumers remain healthy.

Initialization or registration may be asynchronous. Poll a documented bounded status with a deadline and preserve intermediate errors; do not use an unexplained fixed sleep or infer readiness from an open port.

Before address replacement or removal, list every configuration, runtime, database, ODP, and external reference; migrate consumers first and preserve the prior endpoint/configuration as rollback. The official V4.6.0 Web component guide states that uninstalling Config Server is not supported there. Do not infer that the generic CLI component-delete path supports it: require exact installed help and workflow evidence, or report removal as unsupported. Apply [cleanup and ownership boundaries](../../references/cleanup-boundaries.md) to any supported removal.

On failure preserve trace, plugin/configuration, component logs, actual endpoint, metadata response, registration state, and consumer errors. Do not remove the component, edit consumer files ad hoc, or redeploy until the failed layer is identified.
