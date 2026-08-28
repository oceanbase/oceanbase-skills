# Mirrors and Repositories

Use this workflow to inspect or change OBD mirror sections, local repository artifacts, remote repository definitions, and package candidates.

When acquisition serves a deployment, component addition, upgrade, or reinstall, first build the full [deployment package closure](../../references/deployment-package-sets.md). Apply mirror and operating-system candidate resolution to every required closure entry; do not begin with one obvious component and discover its companion libraries, JRE, client library, or node-local image only after deployment has started.

## Keep the Layers Distinct

- A **mirror section** describes a local or remote source and its enabled/available state.
- The **local repository** contains artifacts OBD can select, identified by component, version, release, architecture, hash, tags, and source.
- A **compatible package set** is a reviewed selection for one product form and workflow. Mirror visibility or repository presence alone does not prove compatibility.

Read the installed `obd mirror` and `obd repo` help before constructing commands; available subcommands and argument forms vary by OBD build.

## Fixed Online Package Source Order

For every package carried by the OceanBase public repositories, use these mirror sources in exactly this order:

1. `https://mirrors.oceanbase.com`
2. the direct package directories under `https://mirrors.aliyun.com/oceanbase`

The second source means its actual `community/stable`, `development-kit`, or other proved package directory. Merely downloading or registering `https://mirrors.aliyun.com/oceanbase/OceanBase.repo` does not count as trying the second source when that file's resolved `baseurl` points back to `mirrors.oceanbase.com`. Record and use the package request's effective base URL, not the repository-definition download host.

Build operating-system candidates in the shared exact-suffix, EL8, then EL7 order. For each candidate suffix, walk the two mirror sources above in order. One attempt is one complete source-specific pass to resolve and acquire the same exact component/version/release/suffix/architecture, including source metadata and the exact package object when resolved; individual HTTP subrequests are not separate attempts. The first package network action must be an actual attempt against source 1. A ping, generic public-Internet test, unrelated website request, DNS-only check, or proxy inspection does not count and cannot gate that first attempt.

Keep the same mirror source until that exact acquisition has failed three times, recording attempts 1, 2, and 3. After the third failure, move to the next mirror source. After source 2 has also failed three times, move to the next compatible suffix. Stop immediately when the artifact is acquired and its identity and checksum are verified. If every suffix and both mirror sources are exhausted, ask the user before using a download center, GitHub release, OSS installer, another host, or any unlisted source.

The V4.6.0 command surface preserves these ordinary operation shapes:

```bash
obd mirror list [mirror_repo_name]
obd mirror update
obd mirror clone <reviewed_rpm_path>
obd mirror create --name=<component_name> --path=<reviewed_install_tree> --version=<component_version> [--tag=<reviewed_tags>]
obd mirror disable <mirror_repo_name>
obd mirror enable <mirror_repo_name>
obd mirror add-repo <reviewed_repository_definition_url>
```

Confirm each form with the installed help. `list` is inventory; `update`, `clone`, `create`, `disable`, `enable`, and `add-repo` mutate controller state or future candidate resolution and require the matching gates below. The available `--force` options are intentionally omitted from reusable examples; do not add them automatically.

## Baseline and Selection

1. Record the controller identity, `OBD_HOME`, existing mirror definitions and enabled state, metadata timestamps, local repository inventory, active repository mutation, and package candidates relevant to the request.
2. For every artifact, record component, version, release, architecture, checksum/hash, size, source mirror, and provenance. Select one reviewed artifact per component; do not let version-only or “latest” matching choose among multiple releases.
3. Resolve dependency and compatibility edges separately. A repository can contain individually valid packages that cannot be used together.

Listing the mirror and listing the local repository answer different questions. Preserve both views when diagnosing why resolution changed.

## Keep Acquisition on the Selected Controller

In a remote workflow, `local repository`, `local package`, and `download locally` refer to the selected OBD controller, not the automation runner. Keep package discovery, candidate selection, download, checksum verification, import, and OBD execution on that controller by default.

Before the first package network request, use controller-local inventory to confirm remote-repository enabled state, effective base URLs, metadata state, the target suffix, and the exact requested package identity. This local preparation must not be replaced by a generic Internet-connectivity test. Then make the first actual network attempt against source 1. After a mirror-source attempt fails, inspect DNS, route, proxy, TLS trust, HTTP response or redirect, metadata refresh, package-manager resolution, authentication, or local capacity as needed to explain that failure and prepare the remaining attempts on the same source. Such diagnostics are not a mirror source, do not increment the three-attempt count, and cannot justify skipping to the next source or changing machines. Do not make persistent proxy, trust, repository, or host changes without their normal authorization.

Record the mirror-source priority, effective base URL, component/version/release/suffix/architecture, attempt number from 1 through 3, exact package URL when known, relevant proxy/repository state, timestamps, and result. Restore any authorized temporary state. Ask the user how to proceed only after the full suffix-by-source attempt matrix is exhausted. Do not autonomously download on the runner, install or run OBD there, or switch to another controller. If the user approves the runner only as an artifact relay, acquire and verify the exact artifact there, transfer it to a reviewed controller-local path, verify the checksum again on the controller, and continue package resolution and installation remotely.

## Repository Availability Probe

Do not classify a package, platform, or component as unsupported merely because the currently enabled remote sections return no candidate or the repository substituted the target system's current `$releasever`. Before an `UNSUPPORTED` verdict:

1. Record the target `/etc/os-release` identity and major version, architecture, package manager, OBD's resolved `$releasever`, and the fully substituted URL of every relevant repository section.
2. List all remote sections, including disabled ones, with enabled/available state, base URL, metadata age, refresh errors, and relevant local candidates.
3. For each required component and dependency, preserve product form, version, release, and architecture while probing the target-system suffix, EL8, and EL7 in that order. Do not stop after only the current `$releasever` returns no package.
4. For each suffix, probe `https://mirrors.oceanbase.com` first and the direct package directories under `https://mirrors.aliyun.com/oceanbase` second. Do not pre-filter either source through a generic reachability verdict. A source is exhausted only after three failed complete acquisition attempts for that exact candidate.
5. For each source and suffix, establish three independent layers: repository metadata/index presence and freshness; effective base, metadata, and candidate-object URL behavior including TLS/redirects; and an exact package filename or NEVRA candidate for the required component plus its dependency closure. Confirm that the effective base URL still belongs to the mirror source being counted.

If a trusted relevant section is disabled, a package-resolution or compatibility-test plan may temporarily enable that exact section only when this controller-wide mutation is within the reviewed authorization. Capture its original state, refresh and inspect the candidate set, and restore the exact state after the probe unless an authorized online workflow still needs it enabled through final package selection. Verify restoration. If enabling is not authorized, report that limitation as `BLOCKED`; do not infer package absence or switch machines to evade it.

Only a conclusive negative result at the metadata, URL, and exact-package layers after three failed attempts on each fixed mirror source for every required suffix supports an `UNSUPPORTED` package verdict. A generic connectivity result, timeout, authentication failure, certificate failure, stale metadata, skipped source or suffix, disabled untested source, or omitted attempt does not. In a test report, omitting a required in-scope source or attempt is an incomplete or failed test execution, not a blocked product capability.

## Choose Online or Local-Package Resolution

Choose one resolution mode before a deployment or other package-selecting workflow:

- **Online mode:** keep the reviewed remote repository enabled and prove the exact remote source and winning component/version/release/suffix/architecture/hash. Online mode does not require downloading or importing the package into the local repository first.
- **Local-package mode:** prove that the exact selected artifacts and complete dependency closure already exist in the local repository. Capture the enabled-state baseline, use the installed public command to disable every remote section that can participate in resolution—commonly the section named `remote`—and immediately re-list mirror state and eligible candidates. Do not execute the package-selecting workflow unless remote resolution is absent and the expected local hashes are the only proved winners.

Disabling a remote section is a controller-wide repository mutation, so include it in the reviewed deployment plan and do not infer permission from package or deployment authorization alone. Keep remote resolution disabled through the final package-selecting stage in that local-package workflow. Unless the user requested a persistent local-only controller policy, restore every temporarily disabled section to its exact prior state afterward and verify the candidate-set baseline. Do not use an unresolved hybrid mode; acquire the remaining closure locally or choose online mode explicitly.

## Register or Update a Remote Source

Before `mirror add-repo` or an equivalent supported command:

- resolve the repository definition or URL to the exact reviewed input;
- verify its name does not collide with an existing section;
- review transport, certificate validation, authentication source, OS/architecture scope, component scope, ownership, and permissions;
- reject embedded clear-text credentials, unapproved redirects, disabled certificate verification, and unexpected symlinks;
- explain that registration or metadata update changes future package candidates but does not itself select or install a package.

Update only the intended source. Afterward, compare mirror state and candidate inventory with the baseline. Stop if an existing deployment workflow could now resolve to a different artifact without an explicit hash or other unambiguous constraint.

## Import or Create Local Artifacts

Treat `mirror clone`, `mirror create`, and comparable operations as repository mutations. Inspect the source artifact or build directory, metadata, checksum, ownership, and destination behavior first. Do not use force automatically; overwriting an existing artifact or tag can change future resolution.

For `mirror clone`, record both the incoming RPM MD5 and its package filename. Independently inventory (a) any local-repository record with the same MD5 and its current path and (b) any record or file that uses the destination filename. In the inspected implementation, the overwrite prompt and `--force` gate are keyed by the incoming MD5, while the copy target is keyed by package filename. These are different collision identities: the same MD5 can replace/move its recorded file, while a different MD5 with the same filename can overwrite the bytes beneath an older MD5 record. `--force` only bypasses the same-MD5 prompt; it does not make a filename collision safe.

Before any authorized forced clone, show the exact old/new MD5, package metadata, source and destination paths, affected repository records/tags, active consumers, and candidate-resolution delta. Retain the exact prior RPM and its checksum plus a version-supported re-import plan; do not promise rollback by editing hidden repository metadata. Afterward verify the destination bytes, every affected MD5 record/path, tags, and selected candidates. Stop if a stale record or supported restoration path cannot be ruled out.

For `mirror create`, first identify the selected installed component plugin and its required file list, then prove the build/install tree contains every required path with the expected file type, executable bit, symlink target, architecture, and version metadata. The V4.6.0 guide's source-build example runs the build system's staged install before `mirror create`; OBD collecting files from a directory is not proof that the directory is complete. If the installed plugin file list or any required object cannot be established, do not invoke `mirror create`. Treat `--force` as replacement of an existing image or tag and authorize that exact repository object separately.

After import, verify the local repository shows the expected exact artifact and that no unrelated entry changed. For `mirror create`, verify the main repository's real hash/file list and every requested tag independently: inspected code can create the main repository, fail one or more tag operations, print errors, and still leave a partial result. A successful exit is not proof that all tags point to the intended hash. Repository registration is not installation acceptance.

## Enable, Disable, and Clean

Changing a mirror's enabled state is controller-wide and can affect every later resolution. Capture the original state and active tasks, change only the named section, then verify the candidate-set delta. The local-package isolation window above is conditional on choosing local packages; it is not a requirement to pre-download packages for an online deployment.

Repository or mirror cleaning is destructive. The V4.6.0 guide documents that `obd mirror clean` without filters removes all currently unused component files while retaining only a version-sorted latest RPM per component; that is still a broad deletion, not maintenance discovery. Do not invoke the clean command to obtain a preview: inspected code can continue from its listing directly into deletion, and a controller-wide automatic-confirm setting can suppress the prompt.

Handle a `mirror clean` confirmation through [non-interactive automation execution](../../references/automation-execution.md). If the installed command needs an interactive answer, use a real PTY rather than an ordinary pipe, display the exact expanded hash/path selection before confirmation, and confirm only that reviewed selection.

Read [cleanup and ownership boundaries](../../references/cleanup-boundaries.md) before producing the repository deletion set. Deployment, component, tenant, test, or controller-maintenance authorization never implies mirror, cache, downloaded-package, or tag cleanup.

The installed V4.6.0 command supports filters such as `--components=<names>`, `--type=<rpm|repository>`, and `--hash=<exact_hash>`, plus `--confirm`. These options select or confirm deletion; none is a dry-run. Do not emit an executable clean command until the exact selected objects have been independently enumerated and authorized.

Build the preview from read-only mirror/repository inventory and exact filesystem identities. Record automatic-confirm state, active tasks, deployment and rollback references, then enumerate the precise hashes and paths proposed for deletion. Prefer an exact supported `--hash` filter. A component/type filter still selects a set and must be expanded before authorization. Never run an unfiltered clean unless the user explicitly requested that complete enumerated set after seeing its impact. If automatic confirmation is enabled, stop or separately authorize a temporary controller setting change and restore its exact prior state before any other task.

Rollback restores the original repository definition and enabled state, refreshes only the affected metadata, and proves that the candidate set matches the recorded baseline. Do not delete unrelated cache, credentials, or mirror files.
