# Product and Capability Resolution

Use this gate before selecting commands, YAML keys, packages, or upgrade paths. It supports community and commercial OceanBase deployments without duplicating the common operating workflow.

Before obtaining evidence from a live controller, host, deployment, SSH session, SQL endpoint, API, repository, or network, read the [operation contract](operation-contract.md). Supplied files and already available local evidence may be reviewed without live access. Product resolution does not itself authorize a discovery command whose side effects have not been classified.

## Controller Bootstrap Exception

When the request is to install OBD on a new controller, first use non-OBD inventory to determine whether any executable, package-manager record, installation prefix, `OBD_HOME`, metadata owner, registered deployment data, or active OBD process already exists. If none exists, route to the [OBD installation workflow](../obd-administration/references/installation.md). Do not require `obd --version`, subcommand help, plugins, or repository state from a tool that is not installed. After installation acceptance, return here and build the normal installed capability record before any cluster, tenant, test, or diagnostic execution.

If an executable or metadata exists, this is controller maintenance or takeover, not a clean bootstrap. Preserve that identity and do not hide it with a fresh `OBD_HOME`.

## Establish the Controller Identity

Record the controller host, current user, exact `obd` executable, OBD version and build or revision, runtime, `OBD_HOME`, and active OBD processes. Do not assume the first executable on `PATH` owns the registered deployments or plugins under inspection.

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

1. Read the exact target subcommand's `--help`; prefer unambiguous long options.
2. Inspect the selected component schema or workflow when the documented command leaves a version-specific field or behavior unresolved.
3. Inspect registered deployment state and effective configuration when the target already exists.
4. List repository candidates by component, version, release, architecture, hash, and source.
5. Resolve dependencies and compatibility edges that apply to the selected components, operating system, and architecture.
6. Select a compatible artifact per component; use an exact reviewed artifact when reproducibility or an existing deployment requires it.

The evidence priority is:

1. the installed command help and installed plugin/schema;
2. the registered configuration and resolved repository artifacts;
3. version-matched official documentation or released examples;
4. implementation source for unresolved behavior, clearly identified as implementation evidence.

If these layers disagree on a material behavior, report the conflict and resolve it from the installed command or version-matched documentation before relying on that behavior.

## Preferred Package Source

For every package acquired by this skill bundle, use `https://mirrors.oceanbase.com` as the preferred mirror. Search it first for the exact component, version, release, operating-system package suffix, and architecture. Use another source only when the required artifact is unavailable there or the user explicitly selects a different source, and record that fallback in the execution record.

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
