# Product and Capability Resolution

Use this gate before selecting commands, YAML keys, packages, or upgrade paths. It supports community and commercial OceanBase deployments without duplicating the common operating workflow.

Before obtaining evidence from a live controller, host, deployment, SSH session, SQL endpoint, API, repository, or network, read the [operation contract](operation-contract.md). Supplied files and already available local evidence may be reviewed without live access. Product resolution does not itself authorize a discovery command whose side effects have not been classified.

## Controller Bootstrap Exception

When the request is to install OBD on a new controller, first use non-OBD inventory to determine whether any executable, package-manager record, installation prefix, `OBD_HOME`, metadata owner, registered deployment data, or active OBD process already exists. If none exists, route to the [OBD installation workflow](../obd-administration/references/installation.md). Do not require `obd --version`, subcommand help, plugins, or repository state from a tool that is not installed. After installation acceptance, return here and build the normal installed capability record before any cluster, tenant, test, or diagnostic execution.

If an executable or metadata exists, this is controller maintenance or takeover, not a clean bootstrap. Preserve that identity and do not hide it with a fresh `OBD_HOME`.

## Establish the Controller Identity

Record the controller host, current user, exact `obd` executable, OBD version and build or revision, runtime, resolved `OBD_HOME`, and active OBD processes. Apply the operation contract's controller-home resolution; do not assume the first executable on `PATH` owns the registered deployments or plugins under inspection, and do not set `OBD_HOME` to a guessed default metadata directory.

For development builds, record the source revision as additional evidence. A source revision does not replace the identity of the installed executable and plugin tree.

## Resolve the Product Form

Determine the product form from the user's stated goal plus observable evidence:

- registered deployment configuration and component keys;
- package names, version, release, architecture, and hashes;
- installed component plugins, schemas, and workflows;
- repository source and any commercial all-in-one or local artifact set;
- the existing process identity when taking over or maintaining a deployment.

OBD builds commonly use `oceanbase-ce` for community distributed deployments, `oceanbase` for commercial distributed deployments, and `oceanbase-standalone` for the standalone or centralized commercial form. Treat these as candidates, not universal aliases: confirm the exact component key in the installed build before using it.

Do not copy a community template and replace only the component name. Product forms can differ in package closure, topology, required parameters, supported lifecycle commands, and compatibility rules.

## Build a Capability Record

Use the evidence needed for the requested operation:

1. Follow the routed workflow in this Skill; do not rediscover an implementation detail that it already establishes unless installed evidence conflicts.
2. Read the exact target subcommand's public `--help`; prefer unambiguous long options. Use installed validation/schema output and released examples when they expose the required field.
3. Inspect registered deployment state, effective configuration, public command results, and actual runtime/data-plane state when the target already exists.
4. List repository candidates by component, version, release, operating-system suffix, architecture, hash, and source.
5. Resolve dependencies and compatibility edges that apply to the selected components, operating system, and architecture.
6. Select a compatible artifact per component; use an exact reviewed artifact when reproducibility or an existing deployment requires it.
7. Inspect the installed packaged plugin or workflow only when the public surface and observed state cannot establish an execution-critical behavior.

The evidence priority is:

1. this Skill's applicable workflow and invariants;
2. installed public help, validation/schema surfaces, and released examples;
3. registered configuration, resolved artifacts, public command output, and observed runtime/data-plane state;
4. version-matched official documentation;
5. installed packaged implementation for a still-unresolved critical behavior, clearly labeled as implementation evidence.

If these layers disagree on a material behavior, report the conflict and prefer the installed public surface and observed state. Do not decompile or disassemble binaries, modify OBD/plugins, execute extracted code, or inspect a development checkout as routine capability discovery.

## Fixed Package Sources and Platform Fallback

For every package acquired online from the OceanBase public repositories, use this fixed mirror-source order:

1. `https://mirrors.oceanbase.com`;
2. the direct package directories under `https://mirrors.aliyun.com/oceanbase`.

For an RPM or another package family that publishes EL operating-system suffixes, preserve the exact product form, component, version, release, and architecture, then select the suffix in this order:

1. the suffix matching the observed target operating-system major version;
2. EL8 when no exact-suffix artifact exists;
3. EL7 when neither an exact-suffix nor EL8 artifact exists.

This suffix order applies to the OBD RPM and every OBD-managed component RPM; packages that do not publish EL suffixes retain their own format/platform compatibility rules. It is a candidate-selection policy, not proof of compatibility: for an EL8 or EL7 fallback, inspect the exact RPM requirements and verify the target package manager, executable format, dynamic loader, GLIBC and required libraries/symbols before use. Stop if the fallback changes product/component/version/release/architecture, crosses the community/commercial boundary, or cannot be proved runnable.

For each candidate suffix, attempt the two mirror sources in the fixed order above. Keep the current source until the same exact package acquisition has failed three times, then move to the next source; after both sources fail three times, move to the next suffix. A generic Internet-connectivity test cannot precede or substitute for the first actual source request. Downloading an Aliyun-hosted `.repo` file does not count as source 2 if its effective package `baseurl` points to source 1. Follow the detailed [fixed online package-source workflow](../obd-administration/references/mirror-and-repositories.md#fixed-online-package-source-order), and ask the user before introducing a third source or another acquisition host.

Choose the repository-resolution mode explicitly. Online mode may resolve the reviewed artifact from an enabled remote repository and does not require downloading it into the local repository first. Local-package mode requires the complete selected dependency closure in the local repository and follows the mirror workflow's remote-disable gate for the package-resolution window. Do not leave local and remote candidates to compete without proving the exact winner.

For a remote workflow, `local` in these modes means local to the selected remote OBD controller. Do not move package acquisition or OBD execution to the automation runner after a failed route. Follow the operation contract's [remote execution identity](operation-contract.md#keep-remote-execution-identities-stable) and the mirror workflow's [same-controller acquisition](../obd-administration/references/mirror-and-repositories.md#keep-acquisition-on-the-selected-controller). A user-approved runner relay may transfer a checksummed artifact to the controller without becoming the controller.

Before classifying an exact artifact or platform path as `UNSUPPORTED`, complete the standard [repository availability probe](../obd-administration/references/mirror-and-repositories.md#repository-availability-probe). A disabled remote section, stale or unreadable metadata, a generic connectivity failure, or an empty candidate list for only the current `$releasever` is not proof of absence. Resolve the target operating-system suffix and EL8/EL7 candidates per component, then complete all three attempts on each fixed mirror source in order. Repository access that remains inconclusive after the required attempts is `BLOCKED` or unresolved, not `UNSUPPORTED`.

## Maintainer Evidence Baseline

This revision was reviewed against the official OBD V4.6.0 Quick Start, User Guide, Command Guide, and OBD Upgrade Guide, plus an explicitly identified development checkout under the [source-evidence boundary](source-baselines.md#source-evidence-boundary). The documentation is not mapped to that checkout or to an RPM release. Use development-source observations to explain implementation details, not to impose release-wide restrictions without matching runtime evidence.

## Commercial Artifact Boundary

Commercial requests are supported, but the skill must not invent unavailable commercial material. Determine how the user supplies the artifacts: an approved repository, all-in-one bundle, local RPM/TAR set, or an already registered deployment. Verify provenance, license/access boundary, checksum, dependency closure, and the target operating system before generating a commercial configuration.

Do not fall back to public community packages when a required commercial component is missing. Report the exact missing component, version, release, architecture, plugin, or compatibility evidence.

## Component Scope

Start from the components explicitly requested by the user. Additional components require a reason tied to the requested outcome and a review of dependencies, resources, ports, paths, credentials, and lifecycle impact.

Before execution, present the final component manifest and map every component to the user request. Remove components that have no justified mapping.

## Stop Conditions

Stop before mutation when:

- the product form or target deployment identity is ambiguous;
- the installed OBD build does not expose the required command or option;
- the exact package set or compatibility relationship cannot be proved;
- a schema or workflow for another product form would have to be guessed;
- the required commercial artifact or authorization boundary is unavailable;
- current deployment state makes the proposed transition unsupported.

Offer only alternatives proven for the resolved product form. Do not translate the request into another product merely because its artifacts are easier to obtain.
