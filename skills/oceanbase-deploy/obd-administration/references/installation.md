# Install OBD on a Controller

Use this workflow for a new OBD installation. Use [controller-maintenance.md](controller-maintenance.md) when an executable or package already owns the intended controller state.

## Resolve the Installation

Controller bootstrap precedes the installed-build capability gate. If inventory proves there is no OBD executable and no existing OBD metadata owner, route directly through this installation workflow; do not require help output from a nonexistent CLI. Establish the OBD/plugin/schema capability record only after installation acceptance.

For a cluster deployment, select the installation target through the shared [default controller, SSH, and cluster discovery rule](../../references/operation-contract.md#default-controller-ssh-and-cluster-discovery). Inspect every supplied cluster host first. Reuse the target host that owns the intended registration or another unambiguous usable target-host OBD installation. Only after all targets are reachable and all are confirmed to have no OBD executable, package ownership, controller metadata, or registration, install OBD on the first supplied cluster host without asking the user to choose. This applies to every deployment mode and package-acquisition mode. A user-explicit separate controller overrides the default; an unreachable target does not count as empty.

A failed download or repository request does not justify installing OBD on the automation runner or moving the controller. Follow the [fixed mirror-source order and acquisition fallback](mirror-and-repositories.md#fixed-online-package-source-order): after one controller-local package-manager or repository path fails, try the exact OBD artifact there with `curl`, `wget`, or another applicable downloader across the required source/suffix attempts. If no controller-local method works, use another reachable host only as a checksummed artifact relay, transfer the exact package to the controller, verify it again, and install it there. Because this is controller bootstrap, install the local OBD package directly rather than requiring a nonexistent OBD to import it. Ask only after the relay also fails, or before using an unlisted source or different controller.

1. Resolve the intended controller host and user through inspection rather than asking for facts that can be observed. When both SSH user and password are omitted, first try non-interactive passwordless `root` access as required by the shared contract. Inventory every existing `obd` executable on `PATH`, package-manager record, profile entry, installation prefix, `OBD_HOME`, registered deployment, active OBD process, and shared automation that invokes OBD.
2. Select the exact released RPM supported for the target operating system and architecture.
3. Resolve the exact OBD version/build, operating system, architecture, runtime requirements, source, checksum/signature, installation prefix, executable path, and expected plugin/repository content. Do not use an unpinned “latest” command when reproducibility matters.
4. Review the network source, destination path, privilege escalation, package dependencies, and files the installer can create or replace. An explicit request to install OBD authorizes the controller-local artifact acquisition, package installation, and necessary profile changes intrinsic to that selected method; record them but do not ask for separate confirmations solely because they are separate persistent stages. Overwriting another owner or changing the installation/controller identity remains out of scope.
5. If existing OBD metadata is present, stop and classify the request as maintenance. A new binary with a fresh `OBD_HOME` can hide registered deployments; a new binary pointed at old metadata can migrate it.

Build the installation decision from target evidence rather than a remembered platform label:

| Decision | Required evidence | Stop condition |
|---|---|---|
| Operating platform | Distribution and version, kernel, architecture, package manager, container boundary, and available OBD package suffixes | No same-version, same-release, same-architecture candidate remains after the shared exact-suffix, EL8, then EL7 order, or neither fallback is runtime-compatible |
| Runtime compatibility | Dynamic loader, GLIBC and other required libraries/symbols, executable format, and disk/inode capacity for the exact OBD artifact | A required loader/library/symbol is absent; do not transfer an OBServer component requirement to the OBD controller package or vice versa |
| Ownership and privilege | Intended controller user, package/prefix/profile owners, required package-manager or installer privilege, umask, and shared automation | The method requires broader privilege or overwrites another owner without an approved plan; do not assume root is always required or always acceptable |
| Connectivity | Online/offline boundary, approved repositories, proxy/TLS trust, artifact transfer route, and checksum/signature verification | The only available path requires an unreviewed network source, credential exposure, or unpinned package |
| Existing state | Every executable, `OBD_HOME`, registration, active task, package record, profile entry, and rollback artifact | Existing state has no proved owner or safe maintenance/migration path |

For an RPM-based Linux controller, apply the shared [package-source and platform-fallback policy](../../references/product-and-capability-resolution.md#fixed-package-sources-and-platform-fallback): first the suffix matching the observed OS major version, then same-version/same-release/same-architecture EL8, then EL7. Verify the selected fallback package's loader, GLIBC/library dependencies, package-manager compatibility, and installed executable on the controller. This is the same suffix order used for every OBD-managed component; each component still requires its own runtime and dependency proof.

Use controller-local `curl`, `wget`, or the operating-system package manager—not `obd mirror`—for any explicit remote download, following the fixed source order `https://mirrors.oceanbase.com` then the direct package directories under `https://mirrors.aliyun.com/oceanbase`, with three failed attempts per source before switching. Use the exact selected `ob-deploy` RPM and record package-manager/profile ownership; do not use an unpinned latest package when the required version is fixed. If neither source yields a package matching the controller OS major version, use the shared EL8-then-EL7 fallback with the same source order.

## Version-Matched Command Skeletons

After substituting a reviewed absolute path, install the exact `ob-deploy` RPM through the target OS package manager, for example `sudo yum install <absolute_reviewed_ob_deploy_rpm>` on a verified compatible YUM-based system. Do not use a glob or remote repository candidate when an exact version was requested.

## Install

Use the selected method's version-matched instructions and the reviewed controller-local absolute artifact path. Install only on the controller. Do not copy the OBD package to every managed host merely because OBD will later connect to them, and do not install it on the runner merely because the controller needed an approved artifact relay.

Keep privilege scope narrow. Do not pipe an unreviewed remote installer into a shell, overwrite another package owner's files, or create a second implicit `OBD_HOME`. Preserve existing shell and service configuration unless the chosen method requires a reviewed change.

## Accept

Verify independently:

- the executable path, owner, package/build identity, version, runtime, and installation prefix;
- the intended user resolves that executable in a fresh shell;
- `OBD_HOME` and its permissions are the intended ones;
- shipped plugins and repository definitions can be read without an unintended network update;
- any pre-existing registered deployments remain visible and parseable through logical list/display inventory, allowing for ordinary controller-local CLI bookkeeping;
- no managed component process, listener, configuration, or target-host path changed during controller installation.

On failure, preserve installer output and the before/after executable and metadata inventory. Do not delete `OBD_HOME`, reinstall through a second method, or remove profile/package files until ownership and the completed installation stage are known.

## Sources

- Official OBD V4.6.0 released-RPM installation guidance.
- Exact package metadata, installer content, or source revision selected for the target controller.
