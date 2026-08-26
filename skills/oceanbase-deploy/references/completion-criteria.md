# Completion Criteria

Declare success only after the layers relevant to the requested outcome have passed. An earlier layer cannot substitute for a later one.

## Acceptance Layers

1. **Invocation:** the intended command or request was submitted with the reviewed target and inputs.
2. **Task:** the OBD trace or asynchronous task reached a successful terminal state.
3. **Control plane:** registered configuration, deployment/component/tenant state, and actual artifact identity match the plan.
4. **Runtime:** intended processes, listeners, paths, service manager units, or containers exist; objects that should be stopped or removed do not.
5. **Data plane:** an authenticated SQL, HTTP/API, metrics, backup-catalog, replication, or test-result check proves the requested capability.
6. **Isolation:** unselected objects remain unchanged and no unexplained residual object or task remains.

Use only the applicable layers, but explicitly mark a skipped layer and why it is not needed.

## Common Lifecycle Outcomes

| Operation | Required outcome |
|---|---|
| Deploy | exact artifacts and registered configuration; verified `deployed` state for an ordinary deploy; require processes, listeners, and data-plane readiness only when the authorized operation also includes start |
| Start | every selected target running; dependencies healthy; representative data-plane check |
| Stop | every selected target stopped; listeners closed; unselected targets unchanged |
| Restart | stop/start transition completed for selected targets; runtime identity is new where expected; data plane recovered |
| Reload/configure | registered, generated, and effective runtime values agree; restart-required values are not reported as dynamically applied |
| Upgrade/reinstall | actual per-node artifact version/release/hash matches the target; mixed versions are only those allowed by the reviewed path; data plane remains usable |
| Scale out | new nodes/components are registered, running, and visible from product-side topology; existing members remain healthy |
| Component add/delete | dependency references, component-specific health, and data plane match the new topology; no residual references remain after deletion |
| Destroy/drop/overwrite | the exact authorized object is absent or replaced; separately owned or external data is preserved unless explicitly included |

## Domain Additions

Domain workflows must add their own proof:

- tenants: login with the intended credential, topology/resources, allowlist, role, or restored data;
- backup/restore: terminal task, manifest/catalog identity, SCN/time coverage, and representative restored data;
- monitoring: exporter metric, Prometheus target/query, Grafana datasource/dashboard, and alert delivery when requested;
- OCP: process, authenticated API/UI, MetaDB, terminal background task, and correct managed-cluster identity;
- benchmarks: required phases, result files, failure counts, metrics, and post-test database health;
- diagnostics: artifact integrity and independently corroborated findings.

Report `partial`, `not completed`, or `unknown` when a required layer is missing. Never collapse a mixed state into a single healthy status.
