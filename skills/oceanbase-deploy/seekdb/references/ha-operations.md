# SeekDB HA Operations Through OBD

Read the shared [product/capability gate](../../references/product-and-capability-resolution.md), [operation contract](../../references/operation-contract.md), [completion criteria](../../references/completion-criteria.md), and [failure recovery](../../references/failure-recovery-and-evidence.md) before any live inspection or role change.

## Capability and Topology Gate

The V4.6.0 guide requires SeekDB 1.2.0 or later for switchover, failover, and decouple. That version floor and command presence in OBD help are necessary but not sufficient. Inspected OBD builds register the HA commands unconditionally and request missing workflows with ignore semantics, so an unsupported target can return command-level success after running no role-change stage. Prove that the exact target version selects a non-empty installed workflow and the required plugins before execution.

Every HA command below takes the **standby deployment name**, not the primary name or an arbitrary member. Before choosing an operation, record:

- controller, deployment names, SeekDB versions/artifacts, real database roles, OBD states, process identities, and health for every member;
- the complete primary, direct-standby, sibling, and cascading graph from both OBD metadata and database-side evidence;
- each member's RPC endpoint, `log_restore_source`, replay/synchronization SCN and timestamp, lag, and last independently verified writable/readable state;
- client, proxy, DNS, service-discovery, monitoring, backup, and automation routes;
- the fencing or traffic-isolation mechanism, recovery plan, accepted RPO/outage, and exact postconditions.

Do not use an HA mutation as discovery.

## Display the Graph

```bash
obd seekdb display <standby_deploy_name> -g
```

Treat this as one control-plane view. Corroborate it with authenticated database role, log-source, and replay evidence from every reachable member. A missing connection does not prove that a member is stopped or fenced.

## Switchover: Planned Transition

```bash
obd seekdb switchover <standby_deploy_name>
```

Use switchover for planned maintenance or a routine HA exercise. Require the selected relationship to be healthy and synchronized and all involved members to be online. The V4.6.0 guide describes an ordinary primary/standby switchover as RPO 0, but verify the actual replay state and installed workflow rather than promising zero loss from the command name alone.

Resolve the topology before describing the outcome:

- In an ordinary pair, the old primary becomes standby and the selected standby becomes primary.
- In a cascading topology supported by the inspected source, the selected node and its upstream can both remain `STANDBY`; the workflow changes their cascade positions/log sources instead of promoting either to the top-level primary.
- Sibling and child relationships can also be rewritten. The inspected workflow logs some `log_restore_source` update failures and can continue, so a successful exit can still leave database and OBD graphs inconsistent.

Authorize the exact role/topology and client-route transition, not a generic “swap.”

## Failover: Emergency Promotion

```bash
obd seekdb failover <standby_deploy_name>
```

Failover is for an unrecoverable primary, not ordinary maintenance or a generic HA test. Even a normally synchronized standby can lose data; the V4.6.0 guide describes a possible hundreds-of-milliseconds loss window.

Before authorization:

1. Independently fence the old primary from client and peer writes and prevent automatic restart. OBD controller-to-primary connection failure is **not** fencing: the inspected precheck rejects failover only when it obtained a primary cursor, then promotes the standby with `ALTER SYSTEM ACTIVATE STANDBY`. A network-isolated old primary can therefore remain writable while OBD promotes another member.
2. Record the last primary/standby synchronization SCN/time and lag, state the maximum unreplicated window that can be proved, and obtain explicit acceptance of possible data loss and divergent-history recovery.
3. In a one-primary/multiple-standby graph, record every sibling. The V4.6.0 guide states that siblings do not automatically attach to the newly promoted primary; each needs a separately reviewed decouple/failover/rebuild decision.
4. Prepare client routing, old-primary quarantine, backup/CDC/monitoring updates, and one recovery owner before promotion.

Keep the old primary fenced after the command until its divergent-state disposition is separately reviewed. Never rejoin or start it merely because the new primary is available.

## Decouple: Planned Split

```bash
obd seekdb decouple <standby_deploy_name>
```

Decouple turns the selected standby into an independent primary while the original primary remains primary. Require both managed members to be online as required by the V4.6.0 baseline, verify replay state, and allocate distinct client routes, service identity, backup/monitoring ownership, and writable-data responsibility before the split. Isolate traffic until those identities are unambiguous. Decouple authorization does not authorize deleting either side or discarding the prior relationship evidence.

## HA Drills

Use a reviewed switchover for a planned exercise when its topology and RPO requirements are satisfied. A failover drill is a destructive disaster-recovery exercise: it requires independent old-primary fencing, accepted data-loss bounds, sibling handling, client cutover, and an explicit old-primary recovery/rebuild plan. Do not instruct an operator merely to stop the primary and run failover.

## Destroying a Primary with Standbys

```bash
obd seekdb destroy <primary_deploy_name> --ignore-standby
```

The flag bypasses OBD's standby guard. The V4.6.0 command guide states that the standbys become unusable after the primary is destroyed. Enumerate the complete graph and every affected deployment/data/recovery object, then obtain topology-specific destructive authorization immediately before execution. Do not add the flag as failure cleanup or a convenience retry.

## Acceptance and Mixed-State Recovery

After any HA operation, independently verify all applicable layers:

1. exact database roles on every member and no unintended writable primary;
2. `log_restore_source`, replay SCN/time and advancement, lag, and the complete OBD/database topology;
3. process/listener/OBShell state and OBD registration for every member;
4. intended write endpoint, authenticated read/write behavior, client/proxy/DNS routing, and rejected access to fenced targets;
5. sibling/cascading relationships, backup/CDC/monitoring ownership, and unselected members unchanged.

Command exit, an updated graph, and one successful SQL connection are not interchangeable. If any role change, relationship rewrite, OBShell action, or metadata update fails or warns, freeze retries and keep ambiguous former primaries fenced. Preserve traces, before/after roles, SCNs, log sources, OBD configuration, routes, and process state. Do not run the inverse command, restart all members, edit hidden metadata, destroy a deployment, or rebuild a member until the observed state proves the narrow recovery action and its impact is authorized.

## Sources

- Official OBD V4.6.0 User Guide, “角色切换与解耦.”
- Official OBD V4.6.0 Command Guide, `obd seekdb switchover/failover/decouple/destroy`.
- [Official public OBD V4.6.0 source baseline](../../references/source-baselines.md#official-obd-v460-baseline): SeekDB relation, connection, switchover, failover/decouple, and metadata-update workflows.
