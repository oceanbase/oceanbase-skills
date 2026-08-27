# Evidence Baselines

Use this reference to keep documentation, inspected source, and installed runtime evidence separate. Do not bind an OBD product version or RPM release to a source commit or implementation behavior without immutable provenance for that exact artifact. Installed command, plugin, workflow, schema, registered state, and selected artifacts remain the runtime authority.

## Documentation Baseline

Official OBD documentation can establish the commands, options, schemas, and behavior documented by that publication. It does not prove the implementation of an installed package, map an RPM release to a source commit, or classify a whole product version as affected or fixed. Reconcile every execution-sensitive claim with the installed artifact.

<a id="source-evidence-boundary"></a>

## Source Evidence Boundary

A source path, symbol, or behavior in this revision refers only to the inspected `ob-deploy` checkout at commit `4ef23088b04cbba82793dbc718d3b844bcd0fdb5`. That hash identifies review evidence only; it is not mapped to an OBD product version or RPM release. Do not relabel the observation as released-version evidence or infer that another package, RPM revision, branch, or product version contains the same implementation. For shell construction, credential handling, destructive behavior, or completion semantics, inspect the installed implementation before execution and fail closed when it cannot be proved.

<a id="post-v460-development-observations"></a>

## Development Source Observations

Some reviewed development code, including the standalone management-IP command and its persisted loopback Observer-identity model, is development-source evidence rather than released-version evidence. Such observations may guide capability discovery but cannot establish package availability.

The reviewed development behavior uses these linked conditions:

- normal fresh `oceanbase-standalone` loopback identity requires component version `4.4.2.3` or later;
- a lower-version legacy deployment is considered only when it explicitly uses `local_ip=127.0.0.1` and the installed implementation can persist and verify that identity;
- `change-ip` requires a running, single-server `oceanbase-standalone` deployment with unchanged configuration and a verified loopback identity marker.

Do not infer an OBD release floor from those observations. Before emitting or executing `obd cluster change-ip`, prove the command, options, version gate, topology gate, and identity checks from the installed executable and its shipped implementation. If the installed source or equivalent vendor evidence is unavailable, provide only a non-executable capability note.

## Evidence Maintenance Rule

Record the exact inspected checkout for a source observation, but do not infer a package mapping from its branch, tag, or version-like name. For a released behavior, require immutable provenance that connects the exact artifact to the cited source. Otherwise label the behavior as source-only evidence, include the runtime checks needed to prove it, and keep execution fail-closed until the installed build supplies that proof.
