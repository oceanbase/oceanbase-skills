# Cleanup and Ownership Boundaries

Read this reference before any cleanup, removal, reset, prune, drop, uninstall, or deletion. An operation may complete while leaving objects by design, and one authorization never implies removal of adjacent controller, host, database, repository, test, or external state.

## Resolve the Exact Object Set

Inventory the requested objects and their owners from current evidence. Canonicalize every filesystem path; identify mounts, symlinks, hard links when relevant, shared directories, package owners, deployment references, database references, and active tasks. Show the exact retained set as well as the proposed removal set.

Do not use a mutating command as discovery or treat a confirmation prompt as the inventory. If the installed workflow, object ownership, or deletion set cannot be proved before execution, stop. Bind destructive authorization to the displayed identities, paths, hashes, database objects, and impact immediately before the mutation.

## Cleanup Matrix

| Object class | What a deployment destroy or redeploy may do | Default disposition | Separate owner action and acceptance |
|---|---|---|---|
| Managed processes, listeners, PID files, helpers, and service units | May stop processes and remove some plugin-owned runtime files; version-specific systemd or helper residue can remain | Remove only objects proved to be owned by the selected deployment and covered by the reviewed workflow | Inspect actual process/unit ownership and installed cleanup code; verify selected objects are absent and unrelated services are unchanged |
| Component home, data, redo, log, temporary, and generated configuration paths | May delete some deployment-owned paths, including database data; path behavior differs by component and version | Retain unless the exact canonical path and its contents are displayed and included in destructive authorization | Treat unowned, shared, non-empty, mounted, symlinked, or colliding paths as a stop condition; verify both removals and retained paths |
| OBD deployment registration, configuration, metadata, and traces | Destroy can leave a destroyed registration and evidence; it does not imply metadata pruning | Preserve registration and traces needed for recovery or audit | `prune-config` or metadata removal is a separate controller mutation; verify only the named registration was removed |
| Tenants, schemas, tables, resource pools, Unit Configs, backup sets, and archive logs | Cluster destroy/redeploy or a benchmark cleanup has product- and workflow-specific data effects | Preserve unless the exact database objects and recovery boundary are separately authorized | Tenant drop, benchmark dataset cleanup, backup deletion, and archive deletion are distinct operations; verify unrelated tenants and recoverability artifacts remain |
| Mirror definitions, local repositories, cached or downloaded packages, and artifact tags | Not implied by deployment, tenant, component, or test cleanup | Preserve | Repository cleaning requires an independently enumerated hash/path set and repository authorization; verify retained candidates and tags |
| OBD installation, plugins, profiles, environment values, stored credentials, and controller tools | Not implied by managed-object cleanup | Preserve | Controller uninstall, tool removal, profile edits, environment restoration, and credential deletion each follow their owning administration workflow |
| Benchmark/test schemas, datasets, generated properties, binaries, raw results, and logs | Test workflows can create both database and controller artifacts; ordinary completion does not define their disposition | Follow the recorded per-run retain/remove decision | Enumerate run-owned objects; remove only approved items, preserve audit results, and verify reusable datasets, shared tools, and prior runs remain |
| Monitoring, OCP, Config Server, external registrations, routes, credentials, and consumers | A component or cluster operation may leave external records or break dependants | Preserve until consumers and ownership are resolved | Migrate or remove references first; verify each remaining management and data plane independently |
| Shared storage, mounts, volumes, snapshots, backup media, and external paths | A deployment workflow can detach from or alter references without owning the underlying storage | Never infer deletion, unmount, formatting, or snapshot removal | Require storage-owner authorization and a storage-specific recovery plan; verify mount identity, retained data, and all other consumers |

## Execute and Verify

Use the narrowest installed public command that selects the authorized objects. Do not add force, recursive deletion, ignore-safety, automatic-confirm, broad glob, or unfiltered cleanup behavior. A partial result or timeout leaves server-side state unknown; preserve evidence and re-inventory before retrying.

After cleanup, verify every selected object is absent or in the documented retained state, every object promised to remain is still present and usable, and no active task can recreate or continue deleting state. Report intentional residue and unsupported cleanup separately from failure.
