# Deployment Package Closure

Use this reference before acquiring packages for a retained deployment, component change, reinstall, upgrade, diagnostic, or `obd test` workflow. A primary RPM alone is not a complete plan when the selected workflow requires a companion library, client, tool, or rollback artifact.

## Retained Package Sets

Resolve names against the installed OBD plugins and repository metadata; the table records the tested closure shape, not permission to choose an unpinned latest build.

| Workflow | Required closure |
|---|---|
| OBD controller installation or maintenance | Exact `ob-deploy` package for the selected controller version, release, architecture, and compatible platform suffix; preserve the prior exact package for rollback during maintenance |
| OceanBase Community Edition deployment | `oceanbase-ce` plus the matching `oceanbase-ce-libs` when that release publishes or declares it |
| Deployment with OBProxy | Community database closure plus the exact compatible `obproxy-ce` |
| Config Server component | Exact `ob-configserver` plus the already proved OceanBase/OBProxy dependency closure selected by the installed component graph |
| Monitoring without an existing OBAgent | Exact compatible `obagent`, `prometheus`, and `grafana`, plus the retained database closure they observe |
| Monitoring with an existing compatible OBAgent | Exact compatible `prometheus` and `grafana`; prove the existing OBAgent endpoint and authentication instead of installing a duplicate |
| Component reinstall | Current artifact, exact target artifact, and the prior compatible artifact required for the reviewed rollback; distinguish same-version packages by release and hash |
| Cluster upgrade | Exact OceanBase artifact for every supported hop and each hop's declared companion libraries; retain the source-hop artifacts required by the proved recovery path |
| SQL and mysqltest acceptance | Exact `obclient` plus matching `libobclient` when declared; verify that the installed client payload contains the required `mysqltest` executable |
| Sysbench | Exact `ob-sysbench` package and its installed external runtime dependencies |
| TPC-H | Exact `obtpch` package, generator/query assets, and the reviewed server-visible table-data path |
| TPC-C | Exact `obtpcc` package plus the version-proved Java/runtime prerequisite |
| obdiag | Exact dynamic diagnostic-tool identity selected through the tested OBD tool lifecycle; use its supported local registration/install path when it is not an OBD component RPM |

Do not infer a companion package solely by naming analogy. Read the installed requirement map, RPM metadata, released example, or tool-install workflow. Already installed dependencies may satisfy a closure entry only after their exact owner, version, architecture, executable/library path, and runtime compatibility are verified.

## Platform Candidate Order

For every RPM-like closure entry, preserve component, version, release, and architecture, then try:

1. the suffix matching the target operating-system major version;
2. EL8 when no exact-suffix artifact exists;
3. EL7 when neither the exact suffix nor EL8 exists.

The fallback is accepted only after verifying package-manager compatibility, executable format, dynamic loader, GLIBC, and required libraries/symbols. Apply the fixed source order and acquisition fallback in [mirror and repositories](../obd-administration/references/mirror-and-repositories.md#fixed-online-package-source-order) independently to each candidate.

## Resolve and Acquire the Complete Closure

1. Freeze the requested topology or operation and enumerate every selected component, companion requirement, test tool, external prerequisite, current artifact, target artifact, rollback artifact, and already-satisfied dependency.
2. Record component/package name, version, release, architecture, platform suffix, source, size, and hash for every candidate.
3. In online mode, prove one exact remote winner for every closure entry before the package-selecting operation. The normal OBD/repository path may fetch it directly.
4. If normal online fetching fails but controller-local `curl`, `wget`, the operating-system package manager, another applicable downloader, or the bounded checksummed relay obtains the exact artifact, transition the complete operation to local-package mode.
5. In local-package mode, place and verify every required RPM on the selected controller, import each already-local OBD-consumed RPM with `obd mirror clone <path>`, use the proved local registration/install path for other artifact types, disable participating remote repositories for the selection window, and verify the local hashes are the only winners.
6. Re-list repository/tool inventory and compare it with the final component graph or test plan immediately before execution. Do not mix proved local artifacts with unresolved remote candidates.
7. Restore any temporary remote-repository state after the final package-selecting stage unless persistent local-only behavior was explicitly requested.

## Acceptance

Package preparation is complete only when every closure entry is present exactly where its consumer expects it, identity and checksum are verified, the installed OBD/plugin/tool resolves the intended winner, and no unreviewed candidate can replace it. Preserve the closure manifest and repository-state evidence with the operation Trace.
