# Dynamic Tool Provisioning

Use this workflow to inventory or install the exact dynamic tool required by a retained workflow such as `obd obdiag`. A top-level alias can exist even when its backing tool is not installed.

## Inventory Before Alias Invocation

Start with the core tool inventory, local and already known remote repository candidates, installed tool paths, executable entry points, versions, package hashes, and consumers. Do not invoke a dynamic alias or alias-specific `--help` as an inventory probe: alias resolution can refresh metadata, download a package, enter an installation prompt, or attempt an update even when the tool is already installed. Automatic-confirm settings can turn that probe into an installation or replacement.

Read the installed core `obd tool --help` and selected core subcommand help. Inspect version-matched dispatch behavior before the first alias invocation and treat any unsuppressible update check as a potential mutation. Inventory is separate from execution of the tool itself.

## Install

1. Identify the requested capability and prove that the selected tool/version provides it.
2. Resolve one package by tool/component name, version, release, architecture, hash, source, install prefix, and entry point. Do not default to latest.
3. Review network access, download/cache/install paths, dependency changes, privileges, conflicts with other tools, and the rollback artifact.
4. Obtain authorization for the exact download and installation. This does not authorize running the installed tool against a deployment or diagnostic target.
5. Do not add automatic-yes or force options by default. A conflict must be resolved from observed ownership and dependency state.

After installation, verify the OBD tool inventory, actual executable path and version, package hash, ownership, and one minimal non-mutating command that cannot trigger another installation. Only after this exact installed identity is proved may the owning workflow invoke alias-specific help to discover syntax. If alias dispatch attempts an unreviewed install or replacement, stop and reconcile tool state. Confirm unrelated tools did not change. On any partial result, inspect inventory and files before retrying. Tool installation success and successful use of the tool are separate completion results.

Dynamic-tool update and uninstall are [not supported by the current Skill version](../../references/current-version-unsupported.md); do not reinterpret installation or alias discovery as authorization for either operation.

## Sources

- Official OBD V4.6.0 Command Guide tool command group.
- [Source-evidence boundary](../../references/source-baselines.md#source-evidence-boundary): tool installation and dynamic alias dispatch in the exact inspected checkout.
