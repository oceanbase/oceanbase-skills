# Install OBD on a Controller

Use this workflow for a new OBD installation. Use [controller-maintenance.md](controller-maintenance.md) when an executable or package already owns the intended controller state.

## Resolve the Installation

Controller bootstrap precedes the installed-build capability gate. If inventory proves there is no OBD executable, no existing OBD metadata owner, and no installation to take over, route directly through this installation workflow; do not require help output from a nonexistent CLI. Establish the OBD/plugin/schema capability record only after installation acceptance. Before then, deployment material is planning-only and commercial artifacts/repositories remain unresolved.

For a workflow that manages remote hosts, use the remote controller selected under the shared [operation contract](../../references/operation-contract.md#keep-remote-execution-identities-stable) as the installation target by default. A failed download or repository request does not justify installing OBD on the automation runner or moving the controller. Follow the [repository availability probe](mirror-and-repositories.md#repository-availability-probe) and same-controller recovery rules first. After the applicable routes are exhausted, ask the user whether to change the network/source, approve an exact artifact relay, select another remote controller, or stop. A relay transfers a verified artifact to the controller; OBD remains installed and run remotely unless the user explicitly changes the control-plane location.

1. Confirm the intended controller host and user. Inventory every existing `obd` executable on `PATH`, package-manager record, profile entry, installation prefix, `OBD_HOME`, registered deployment, active OBD process, and shared automation that invokes OBD.
2. Select an installation method supported for the target operating system and artifact: a released package, an approved all-in-one distribution, or a source/development build. Do not mix methods without an explicit ownership and rollback plan.
3. Resolve the exact OBD version/build, operating system, architecture, runtime requirements, source, checksum/signature, installation prefix, executable path, and expected plugin/repository content. Do not use an unpinned “latest” command when reproducibility matters.
4. Separate authorization to download or copy an artifact from authorization to install it or modify shell profiles. Review network source, destination path, privilege escalation, package dependencies, and files the installer can create or replace.
5. If existing OBD metadata is present, stop and classify the request as maintenance. A new binary with a fresh `OBD_HOME` can hide registered deployments; a new binary pointed at old metadata can migrate it.

Source builds are development artifacts unless an approved release process says otherwise. Record the revision and build inputs; do not present source `HEAD` as a released version.

Build the installation decision from target evidence rather than a remembered platform label:

| Decision | Required evidence | Stop condition |
|---|---|---|
| Operating platform | Distribution and version, kernel, architecture, package manager, container boundary, and available OBD package suffixes | No same-version, same-release, same-architecture candidate remains after the shared exact-suffix, EL8, then EL7 order, or neither fallback is runtime-compatible |
| Runtime compatibility | Dynamic loader, GLIBC and other required libraries/symbols, executable format, and disk/inode capacity for the exact OBD artifact | A required loader/library/symbol is absent; do not transfer an OBServer component requirement to the OBD controller package or vice versa |
| Ownership and privilege | Intended controller user, package/prefix/profile owners, required package-manager or installer privilege, umask, and shared automation | The method requires broader privilege or overwrites another owner without an approved plan; do not assume root is always required or always acceptable |
| Connectivity | Online/offline boundary, approved repositories, proxy/TLS trust, artifact transfer route, and checksum/signature verification | The only available path requires an unreviewed network source, credential exposure, or unpinned package |
| Existing state | Every executable, `OBD_HOME`, registration, active task, package record, profile entry, and rollback artifact | Existing state has no proved owner or safe maintenance/migration path |

For an RPM-based Linux controller, apply the shared [package-source and platform-fallback policy](../../references/product-and-capability-resolution.md#preferred-package-source-and-platform-fallback): first the suffix matching the observed OS major version, then same-version/same-release/same-architecture EL8, then EL7. Verify the selected fallback package's loader, GLIBC/library dependencies, package-manager compatibility, and installed executable on the controller. This is the same suffix order used for every OBD-managed component; each component still requires its own runtime and dependency proof.

For the V4.6.0 official baseline, distinguish the supported methods rather than mixing their ownership:

- **All-in-One:** preferred when a tested compatible component set or offline installation is required; inspect its installer, bundled RPM closure, profile changes, mirror import, and remote-mirror state.
- **Released RPM/repository:** prefer `https://mirrors.oceanbase.com`, use the exact selected `ob-deploy` RPM, and record package-manager/profile ownership; do not use an unpinned latest package when the required version is fixed. If the mirror has no package matching the controller OS major version, use the shared EL8-then-EL7 fallback defined above.
- **Source:** development-only unless the user's release process explicitly approves it; validate the built revision and generated plugin/example content separately.

These are the three installation methods. An offline All-in-One archive does not create a fourth standalone TAR method: extraction only stages the All-in-One distribution whose reviewed `bin/install.sh` owns installation.

## Version-Matched Command Skeletons

Use these only after substituting reviewed absolute paths and confirming them against the selected V4.6.0 artifact/instructions:

- **Offline All-in-One:** verify the exact `oceanbase-all-in-one-*.tar.gz` checksum, extract it into a new empty staging directory, inspect the extracted `bin/install.sh`, then execute that script from the All-in-One tree. Do not call this a standalone TAR installation and do not execute an unrelated `install_obd.sh` or guessed installer name.
- **Local RPM:** install the exact reviewed `ob-deploy` RPM through the target OS package manager, for example `sudo yum install <absolute_reviewed_ob_deploy_rpm>` on a verified compatible YUM-based system. Do not use a glob or remote repository candidate when an exact version was requested.
- **Source:** check out the approved release revision, verify the V4.6.0 build prerequisites and scripts, then run the release's documented `rpm/build.sh` target. Record the resulting executable and generated content as a development/source-owned installation.

The V4.6.0 guide also documents a remote All-in-One bootstrap script, but do not pipe it from the network into a shell without separately reviewing and pinning its content. Prefer a downloaded, checksummed artifact when reproducibility or supply-chain control matters.

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

- Official OBD V4.6.0 Quick Start section 1: All-in-One, RPM, and source installation.
- Exact package metadata, installer content, or source revision selected for the target controller.
