---
name: obd-seekdb
description: >-
  Operate SeekDB through OBD: install or deploy, lifecycle, takeover, primary-standby HA, and OBD-managed OBAgent/Prometheus/Grafana monitoring for a SeekDB deployment. Use only when the requested mechanism is obd seekdb or the task is an OBD controller lifecycle, HA, or monitoring operation on an OBD-managed SeekDB deployment. Do not use for a generic SeekDB mention or for product documentation, non-OBD installation/build, SQL/CLI work, data import, or querying; route those to the top-level SeekDB product skill.
metadata:
  author: oceanbase
  version: "1.0"
---

# obd-seekdb: SeekDB Operations Through OBD

This skill covers operations performed through `obd seekdb` and OBD-managed monitoring components attached to the same SeekDB deployment. It is not the product-level SeekDB skill. A generic mention of SeekDB does not activate this route.

Before any package network request, apply the shared [fixed mirror-source order](../obd-administration/references/mirror-and-repositories.md#fixed-online-package-source-order): actual controller-side acquisition from `https://mirrors.oceanbase.com` first, then the direct package directories under `https://mirrors.aliyun.com/oceanbase`, switching only after three failed attempts on the current mirror source. A generic Internet-connectivity test cannot precede or replace those attempts.

Use the installed OBD help and version-matched SeekDB guidance to select the command. Inspected builds can expose an HA command that performs no role-change stage for an unsupported target, so verify the resulting database roles and topology rather than treating command exit as proof of the transition.

Route product documentation, installation or build work that does not use OBD, `seekdb-cli`, SQL, import, and query/export tasks to the top-level [SeekDB product skill](../../seekdb/SKILL.md). Keep the product task there even when the target instance was originally deployed by OBD, unless the requested action itself is an OBD controller operation.

Before any live `obd seekdb` or monitoring query or mutation, read the shared [operation contract](../references/operation-contract.md). Use the shared [completion criteria](../references/completion-criteria.md), [failure recovery](../references/failure-recovery-and-evidence.md), and [cleanup boundaries](../references/cleanup-boundaries.md); listing a command below is not authorization to run it.

## When to Use This Skill

- Installing or deploying SeekDB through `obd seekdb`
- Managing an OBD-registered SeekDB lifecycle (start, stop, restart, destroy)
- Setting up primary-standby replication through OBD
- Performing OBD switchover, failover, or decouple operations
- Taking over an existing SeekDB instance into OBD management
- Deploying or operating OBAgent, Prometheus, or Grafana monitoring that OBD associates with a SeekDB deployment

**For OceanBase cluster management:** Use [cluster-management](../cluster-management/SKILL.md).
**For tenant operations:** Use [tenant-management](../tenant-management/SKILL.md).

---

## Command Reference

| Command | Description |
|---------|-------------|
| `obd seekdb install` | Integrated interactive host precheck/init, deploy, and start (requires TTY; see the install workflow below) |
| `obd seekdb install --primary` | Integrated primary install with RPC enabled for standby sync |
| `obd seekdb install --standby` | Integrated standby install that can also reconfigure/reload/restart the selected primary |
| `obd seekdb deploy <name> -c <config>` | Deploy with config file |
| `obd seekdb list` | List seekdb deployments only |
| `obd seekdb start <name>` | Start |
| `obd seekdb stop <name>` | Stop |
| `obd seekdb restart <name>` | Restart |
| `obd seekdb display <name>` | Show info |
| `obd seekdb display <name> -g` | Show topology graph |
| `obd seekdb destroy <name>` | Destroy (see safety rules below) |
| `obd seekdb takeover <name> -h <host> -P <port> [SSH options]` | Take over a non-OBD instance by connection endpoint |
| `obd seekdb switchover <standby_deploy_name>` | Planned role/topology transition |
| `obd seekdb failover <standby_deploy_name>` | Emergency promotion after independent old-primary fencing |
| `obd seekdb decouple <standby_deploy_name>` | Planned split of a standby into an independent primary |
| OBD-managed SeekDB monitoring | Use the version-gated [monitoring workflow](references/monitoring.md); new and existing deployments have different command paths |

---

## Critical Safety Rules

### Destroy with Standby
Destroying a primary that still has standby clusters requires `--ignore-standby`:
```bash
obd seekdb destroy <name> --ignore-standby
```
Without this flag, OBD refuses and warns about the risk. The V4.6.0 command guide states that forcing destruction of the primary makes its standby instances unusable. Inventory the complete relationship graph, recovery boundary, and affected standbys and obtain topology-specific destructive authorization; do not add this option merely to bypass the refusal.

### HA Operations Are Topology Transitions

Do not execute an HA command from the table above alone. Read [HA operations](references/ha-operations.md) and resolve the complete primary, standby, cascading, and sibling graph first.

- Use `switchover` for a planned transition only after both selected members are online, synchronized, and supported by an applicable installed workflow. In a cascading topology, the selected members can both remain standbys while their upstream positions change.
- Use `failover` only for an unrecoverable primary after independently proving that the old primary cannot accept or resume client/peer writes. OBD controller unreachability is not fencing: the inspected workflow can promote the standby when it cannot obtain a primary cursor even if the old primary is still writable elsewhere. Disclose the possible data-loss window and one-primary/multiple-standby consequences before authorization.
- Use `decouple` only after isolating client routing and identities for the two resulting independent primaries.
- Every command operand above is the **standby deployment name**. Verify database roles, replay/log-source state, the OBD graph, write endpoint, and client routing afterward; command exit alone is not success.

### Same-Host Restriction
Primary and standby **must be on different IPs**. If deployed on the same IP, OBD suppresses `--role=STANDBY`, causing the standby to start as a primary — log sync will not work.

---

## Install Modes

See [references/install-modes.md](references/install-modes.md) for the compound install transaction, host/primary mutation checks, TTY requirements, non-interactive limitations, and takeover boundary. Review the branches that apply to the requested installation before entering the wizard.

## Monitoring

See [references/monitoring.md](references/monitoring.md) when OBD must deploy or operate OBAgent, Prometheus, or Grafana for SeekDB. Do not route this through the OceanBase monitoring template or assume a separate monitoring deployment receives the current implementation's SeekDB-specific account, scrape paths, rules, or dashboard.

## HA Operations

See [references/ha-operations.md](references/ha-operations.md) for detailed switchover, failover, and decouple procedures.

---

## Usage Examples

### Deploy and Start seekdb
```bash
obd seekdb deploy my-seekdb -c seekdb-config.yaml
obd seekdb start my-seekdb --strict-check
```

### View Topology
```bash
obd seekdb display my-seekdb -g
```

### Takeover Existing Instance
```bash
obd seekdb takeover my-seekdb \
  -h 10.10.10.1 \
  -P 2881 \
  --ssh-user admin \
  --ssh-key-file /home/admin/.ssh/id_rsa
```

The command has no `--home-path` option. This is only a syntax illustration: before execution, confirm the installed version's accepted connection and SSH options and apply the takeover trust, collision, path, credential, repository, and completion gates in [install-modes.md](references/install-modes.md).

---

## Related Skills

- [SeekDB product skill](../../seekdb/SKILL.md) — Product docs, non-OBD installation/build, SQL/CLI, import, and querying
- [cluster-management](../cluster-management/SKILL.md) — OceanBase cluster lifecycle
- [tenant-management](../tenant-management/SKILL.md) — Tenant operations
- [testing-and-benchmark](../testing-and-benchmark/SKILL.md) — Performance testing
