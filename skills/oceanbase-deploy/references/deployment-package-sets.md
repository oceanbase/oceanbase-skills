# Deployment Package Closure

Read this reference before the first package lookup, download, mirror import, or image load for a new deployment, `autodeploy`, an explicitly selected `demo`/`perf` run, component addition, upgrade, or reinstall. Build the package closure from the final requested component manifest before acquiring the first artifact. The obvious primary package alone is not a complete closure.

The names below are a maintained planning baseline, not permission to deploy every listed component. Select only the rows required by the requested topology. Confirm every component key, package name, version constraint, dependency, and alias against the installed OBD plugin and repository before execution.

## Keep Four Artifact Classes Separate

1. **Controller package:** `ob-deploy`, installed on the selected OBD controller, or supplied by an owning OceanBase/OCP All-in-One bundle.
2. **OBD component artifact:** the RPM, archive, image, or repository object that implements a selected YAML component, such as `oceanbase-ce`, `obproxy-ce`, or `prometheus`.
3. **Companion runtime artifact:** a package selected through the component's requirement map, such as `oceanbase-ce-libs`, `openjdk-jre`, or `libobclient`. It may not have its own YAML stanza but is still part of a deterministic local/offline closure.
4. **External prerequisite:** Docker, `clockdiff`, an existing MetaDB, InfluxDB, object storage, a load balancer, or a system library supplied outside the OBD component repository. Record and verify it separately; do not pretend it is an OBD package.

An artifact already present with the exact reviewed identity can satisfy the closure; do not download it again merely to follow this list. A running dependency does not prove that its package is available to a later package-selecting workflow, and a package in the controller repository does not prove that the corresponding service is running.

## Expand Database Components First

For a controller-local or air-gapped repository, stage both the selected database package and its matching companion library package. For online resolution, prove both are available for the selected version, release family, architecture, and platform candidate even when OBD may skip downloading or installing the companion because the target host already satisfies `ldd`.

| Selected database component | Package closure |
|---|---|
| Community distributed OceanBase, normally `oceanbase-ce` | `oceanbase-ce` + matching `oceanbase-ce-libs` |
| Commercial distributed OceanBase, normally `oceanbase` | `oceanbase` + matching `oceanbase-libs` |
| Commercial standalone/centralized OceanBase, normally `oceanbase-standalone` | `oceanbase-standalone` + matching `oceanbase-standalone-libs` |
| OceanBase AI compute service, `oceanbase.ai` | `oceanbase.ai` + matching `oceanbase.ai-libs` |
| OBD-managed SeekDB, `seekdb` | `seekdb` + matching `seekdb-libs` |

`*-utils` packages are not ordinary database-start prerequisites. Add `oceanbase-ce-utils` only when `install_utils` is selected, an OCP check/export workflow needs it, or the installed workflow explicitly declares it. Add `oceanbase-utils`, `oceanbase-standalone-utils`, or another commercial utility only when the selected commercial workflow or OCP software-catalog plan proves that exact requirement. Never invent a `-utils` package by analogy.

For ARM hosts without LSE support, select the documented `nonlse` OceanBase database variant when the chosen version requires it. OceanBase All-in-One does not supply that variant. Keep its companion closure and architecture consistent with the selected package.

## Community, Proxy, and Monitoring Sets

The following sets describe deployment payloads after the controller itself is available:

| Requested outcome | Required package set |
|---|---|
| Community OceanBase only | `oceanbase-ce`, `oceanbase-ce-libs` |
| Community OceanBase with ODP/OBProxy | Community database closure + `obproxy-ce` |
| OBD V4.6.0 documented default `demo`/`perf` component set | Community database closure + `obproxy-ce` + `obagent` + `prometheus` + `grafana` |
| Metrics collection without Grafana | Selected database closure + `obagent` + `prometheus` |
| Metrics collection with Grafana | Previous row + `grafana` |
| Prometheus alerting through Alertmanager | Selected database closure + `obagent` + `prometheus` + `alertmanager`; add `grafana` only when dashboards are also requested |
| Commercial database with ODP | Selected commercial database closure + `obproxy` |

For component addition to an existing healthy deployment, acquire only the newly selected packages and their companion closure; prove the already deployed dependencies through registration and runtime evidence instead of downloading or redeploying them. Community ODP releases before the documented rename can use `obproxy` rather than `obproxy-ce`; preserve the exact installed-version package name instead of renaming it mechanically.

## Config Server and CDC/Binlog Sets

| Requested outcome | Required package set |
|---|---|
| Config Server only | `ob-configserver` |
| Community OceanBase + ODP + Config Server | Community database closure + `obproxy-ce` + `ob-configserver` |
| Full documented `oblogproxy` topology | Community database closure + `obproxy-ce` + `ob-configserver` + `oblogproxy` |
| `oblogproxy` against already managed dependencies | `oblogproxy`; prove the existing OceanBase/ODP/Config Server services and version-specific CDC library path separately |
| Community Binlog service with an existing MetaDB | `obbinlog-ce` |
| Commercial Binlog service with an existing MetaDB | `obbinlog` from the approved commercial repository |
| V4.6.0-style combined community Binlog + MetaDB example | Community database closure + `obproxy-ce` + `ob-configserver` + `obbinlog-ce` |

Binlog's service MetaDB and the OceanBase tenant whose changes are captured are different dependencies. For target-cluster discovery, include `ob-configserver` when the selected Binlog version/workflow requires Config Server; a version-proved root-server-list path can replace that dependency only when the installed public interface supports it. Do not add Config Server solely because a newer Binlog workflow does not need it, and do not omit it from an older workflow that does.

The `oblogproxy` package carries its own packaged `obcdc` tree in the reviewed implementation. Do not guess and download a separate `obcdc` RPM unless the exact selected product artifact or installed plugin declares one.

## OCP and OCP Express Sets

The official V4.6.0 workflow recommends the matching `ocp-all-in-one-*.tar.gz`. Its installer installs OBD, imports the bundle's RPMs into the controller-local repository, and disables remote repositories. Inventory the imported package identities and repository state after installation; the bundle name alone is not proof that the requested version, edition, architecture, or full catalog is present.

When individual artifacts are used, expand the runtime closure as follows:

| Requested outcome | Required package set |
|---|---|
| OCP Community Edition with an existing external MetaDB | `ocp-server-ce` + the exact `openjdk-jre` selected by its installed requirement map |
| Commercial OCP with an existing external MetaDB | `ocp-server` + the exact `openjdk-jre` selected by its installed requirement map |
| OCP CE with a same-deployment MetaDB and ODP | OCP CE runtime closure + community database closure + `obproxy-ce` |
| Commercial OCP with a same-deployment database and ODP | Commercial OCP runtime closure + the selected commercial database closure + `obproxy` |
| OCP Express with an existing MetaDB | `ocp-express` + the exact plugin-selected `openjdk-jre` |
| OCP Express with a same-deployment database | OCP Express runtime closure + the selected database closure and any explicitly configured ODP |

The OCP server's own runtime closure is different from the software catalog OCP later uses to manage or deploy OceanBase. If that management capability is in scope, seed and verify the catalog separately:

- Community catalog candidates: `ocp-agent-ce` for every managed architecture, `oceanbase-ce`, `oceanbase-ce-libs`, `oceanbase-ce-utils`, and `obproxy-ce` for the versions OCP is expected to manage.
- Commercial catalog candidates: `ocp-agent`, `oceanbase`, `oceanbase-libs`, `oceanbase-utils`, `oceanbase-standalone`, `oceanbase-standalone-libs`, `oceanbase-standalone-utils`, and `obproxy`, limited to the approved products, versions, and architectures.

Catalog packages are conditional management content, not permission to deploy those products and not a reason to import every repository version. OCP takeover/export can also require `oceanbase-ce-utils` on the source Observer hosts; include that mutation and package identity in the operation plan.

## OMS Sets

OMS Community Edition uses a container image archive rather than an ordinary component RPM:

- Acquire the approved `oms_<version>-ce.tar.gz` image archive, verify its checksum and expected image identity, and load it into Docker on **every** selected OMS node.
- Preserve the exact registered OBD component key, commonly `oms` for deployment while some CE upgrade surfaces use `oms-ce`; do not rename it by analogy.
- For OMS with an existing external MySQL/OceanBase MetaDB, the deployment payload is the OMS image; the external database is a separately verified prerequisite.
- For OMS with a same-deployment OceanBase MetaDB, add the selected OceanBase database closure.
- Docker is mandatory host software. InfluxDB 1.8 is an optional separately managed monitoring prerequisite in the V4.6.0 baseline, not an OMS RPM.

Do not use `obd mirror clone` on the OMS image archive. Use the OMS workflow's image/tag identity and prove that every node reports the same loaded image ID or digest before deployment.

## MaaS and PowerRAG Sets

These are container or multi-image bundle workflows, not ordinary single-RPM components. Keep their image and bundle acquisition on the selected controller/target hosts; do not silently pull or unpack them on the automation runner.

| Requested outcome | Required artifact set |
|---|---|
| MaaS | The exact configured MaaS backend image name and tag on its selected node. When the installed workflow derives or saves a corresponding runtime image—reviewed 4.7 source derives it by replacing `ob-maas-backend` with `ob-maas-runtime`—that matching runtime image is also part of the closure. |
| PowerRAG with an existing external database | The exact versioned PowerRAG `dockers` bundle, or the explicitly selected `pkgs_path`, including its Docker Compose/configuration payload and every required image archive under the bundle's `images` tree. |
| PowerRAG with the documented same-deployment database dependency | The PowerRAG bundle closure + matching `oceanbase-standalone` and `oceanbase-standalone-libs`. |

The V4.6.0 guide describes MaaS and PowerRAG as local single-node deployments. Docker is mandatory for MaaS; Docker plus a version-compatible Compose implementation is mandatory for PowerRAG. GPU/NPU drivers and runtimes are external prerequisites when acceleration is selected. For local/offline use, inventory and load every image on the actual selected node, then verify image IDs/digests and the bundle's non-image files before deployment. Do not assume that finding the backend image, one tar file, or the top-level bundle directory proves the runtime image set is complete.

## OceanBase AI, Log Service, and Shared Storage

| Requested outcome | Required package set |
|---|---|
| OceanBase AI compute service only | `oceanbase.ai` + matching `oceanbase.ai-libs` |
| Documented OceanBase AI with independent log service | OceanBase AI closure + `oblogservice` |
| Add ODP or OBAgent to OceanBase AI | Previous selected closure + the exact installed-product proxy package and/or `obagent` |

The V4.6.0 documentation baseline requires OBD 4.5.0 or later, `oblogservice` 1.3.0 or later, and `oceanbase.ai` 4.6.1.0 or later for its worked AI/log-service topology. Reconcile those floors with the exact installed packages rather than replacing them with a lower source-code constant. Object-storage clients, credentials, and buckets are external prerequisites, not packages in this closure.

Shared storage does not have one universal extra package name. Start with the selected commercial database closure, then add only the storage client, driver, or proprietary artifact explicitly required by the exact commercial bundle and installed schema. If that requirement cannot be inspected, the closure is unresolved; do not guess a community package or silently fall back to local storage.

## SeekDB Sets

The V4.6.0 guide explicitly requires both `seekdb` and `seekdb-libs` at version 1.2.0 or later for its documented deployment. For OBD-managed monitoring, extend that closure only as requested:

| Requested outcome | Required package set |
|---|---|
| SeekDB only, primary, or standby | `seekdb` + matching `seekdb-libs` |
| SeekDB metrics | SeekDB closure + `obagent` + `prometheus` |
| SeekDB metrics and dashboards in the V4.6.0 documented path | SeekDB closure + `obagent` + `prometheus` + the exact `ob-dashboard` component artifact selected by that installed workflow |
| SeekDB metrics and dashboards in the reviewed 4.7 development path | SeekDB closure + `obagent` + `prometheus` + `grafana` |

Primary and standby members must resolve to a mutually compatible SeekDB package set; do not let independent “latest” selection choose different artifacts. `ob-dashboard` and Grafana are versioned alternatives, not interchangeable package names: inspect the installed schema, examples, and workflow and acquire only the dashboard implementation it actually exposes.

## Controller-Side SQL Acceptance Tools

The official V4.6.0 command-line deployment workflow expects an OBClient-compatible SQL client for verification, and OceanBase All-in-One installs OBClient. When OBD must supply the managed client tool, its closure is `obclient` + matching `libobclient`. An already approved compatible SQL client can satisfy the acceptance need without downloading OBClient; record its exact executable and version. Do not confuse this operator tool with a cluster component.

## Resolve and Acquire Every Closure Entry

1. Freeze the requested topology and list every selected YAML component, companion requirement, conditional package actually chosen, external prerequisite, and already-satisfied artifact.
2. For each RPM-like artifact, preserve product form, component name, version, release, architecture, and hash. Apply the target-system suffix first, then EL8, then EL7 only when the preceding candidate does not exist and runtime compatibility is verified. Do not apply an EL suffix to an image/archive that does not use one.
3. For each candidate, use the shared fixed source order: `mirrors.oceanbase.com`, then the direct package directory under `mirrors.aliyun.com/oceanbase`, with the defined three attempts per source before advancing. After normal OBD/repository fetching fails, vary those attempts with controller-local `curl`, `wget`, the package manager, or another applicable downloader; use the bounded artifact relay only after controller-local methods are exhausted.
4. In **online mode**, prove a unique remote candidate for every required closure entry. OBD may fetch it during the package-selecting workflow; pre-downloading into the local repository is not required. If online fetching fails but an explicit download or relay obtains the artifact, transition the complete closure to local-package mode rather than mixing local and unresolved remote winners.
5. In **local-package/offline mode**, acquire, verify, and import every required RPM closure entry on the selected remote controller before disabling participating remote repositories. Load node-local image artifacts such as OMS on every required node. Re-list the local repository and image inventory after import/load.
6. Treat an All-in-One bundle as a transport for a tested package set, not as evidence by name. The V4.6.0 OceanBase All-in-One baseline includes deployment components except `obbinlog`, but contents vary by product series and it does not include the ARM `nonlse` database variant. Inventory the actual bundle and add every missing selected artifact explicitly.
7. Before execution, compare the final closure manifest with the rendered component graph and the exact candidates OBD will use. A missing required entry is an incomplete package plan; an unrequested package in a bundle is inventory only and must not become a YAML component implicitly.

Use a closure record with at least:

```text
purpose, yaml_component, artifact_name, requirement_class,
version_or_tag, release, os_suffix, architecture, hash_or_digest,
source, controller_or_node_location, resolution_state
```

On deployment output, reconcile OBD's displayed package table, subsequent companion-package resolution, and actual installed artifacts with this record. Some companion libraries are resolved only after target runtime inspection, so absence from the first displayed primary-component table does not prove they were unnecessary; verify the final runtime and package evidence.

## Evidence Basis

The package topology and bundle behavior above were established first from the official **OceanBase Installation and Deployment Tool V4.6.0** documentation: controller/All-in-One installation, OceanBase deployment, OCP, OMS, MaaS, PowerRAG, SeekDB, Config Server, Alertmanager, Binlog, oblogproxy, and OceanBase AI sections. The official guide explicitly names the main component sets, `seekdb` + `seekdb-libs`, OMS image archive workflow, MaaS image and PowerRAG bundle forms, and All-in-One boundaries.

Where those documents do not enumerate an internal companion package, the closure is filled only from the declaration-oriented requirement maps and released examples in the pinned `ob-deploy` checkout described by the [source-evidence boundary](source-baselines.md#source-evidence-boundary): database/SeekDB `*-libs`, OCP/OCP Express `openjdk-jre`, OBClient `libobclient`, and the optional OCP software-catalog candidates. Those source observations do not map the checkout to an OBD RPM release. The installed plugin, package metadata, public help/schema, and selected repository remain runtime authority.
