# Mirrors and Repositories

Use this workflow to inspect or change OBD mirror sections, local repository artifacts, remote repository definitions, and package candidates.

## Keep the Layers Distinct

- A **mirror section** describes a local or remote source and its enabled/available state.
- The **local repository** contains artifacts OBD can select, identified by component, version, release, architecture, hash, tags, and source.
- A **compatible package set** is a reviewed selection for one product form and workflow. Mirror visibility or repository presence alone does not prove compatibility.

Read the installed `obd mirror` and `obd repo` help before constructing commands; available subcommands and argument forms vary by OBD build.

## Preferred Online Mirror

Use `https://mirrors.oceanbase.com` as the preferred online source for every package. Resolve the required component, version, release, operating-system package suffix, architecture, and checksum there before considering another source. Fall back only when the required artifact is unavailable or the user explicitly chooses another source, and record the selected fallback source.

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

Changing a mirror's enabled state is controller-wide and can affect every later resolution. Capture the original state and active tasks, change only the named section, then verify the candidate-set delta.

Repository or mirror cleaning is destructive. The V4.6.0 guide documents that `obd mirror clean` without filters removes all currently unused component files while retaining only a version-sorted latest RPM per component; that is still a broad deletion, not maintenance discovery. Do not invoke the clean command to obtain a preview: inspected code can continue from its listing directly into deletion, and a controller-wide automatic-confirm setting can suppress the prompt.

Read [cleanup and ownership boundaries](../../references/cleanup-boundaries.md) before producing the repository deletion set. Deployment, component, tenant, test, or controller-maintenance authorization never implies mirror, cache, downloaded-package, or tag cleanup.

The installed V4.6.0 command supports filters such as `--components=<names>`, `--type=<rpm|repository>`, and `--hash=<exact_hash>`, plus `--confirm`. These options select or confirm deletion; none is a dry-run. Do not emit an executable clean command until the exact selected objects have been independently enumerated and authorized.

Build the preview from read-only mirror/repository inventory and exact filesystem identities. Record automatic-confirm state, active tasks, deployment and rollback references, then enumerate the precise hashes and paths proposed for deletion. Prefer an exact supported `--hash` filter. A component/type filter still selects a set and must be expanded before authorization. Never run an unfiltered clean unless the user explicitly requested that complete enumerated set after seeing its impact. If automatic confirmation is enabled, stop or separately authorize a temporary controller setting change and restore its exact prior state before any other task.

Rollback restores the original repository definition and enabled state, refreshes only the affected metadata, and proves that the candidate set matches the recorded baseline. Do not delete unrelated cache, credentials, or mirror files.
