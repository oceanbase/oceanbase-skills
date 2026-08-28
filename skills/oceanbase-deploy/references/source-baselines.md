# Evidence Baselines

Use this reference to keep documentation, inspected source, and installed runtime evidence separate. Do not bind an OBD product version or RPM release to a source commit or implementation behavior without immutable provenance for that exact artifact. Installed command, plugin, workflow, schema, registered state, and selected artifacts remain the runtime authority.

## Evidence Escalation

Begin with the applicable Skill workflow, then use installed public help/schema surfaces, released examples, registered state, public command output, and actual runtime or data-plane results. Use version-matched official documentation to interpret that evidence. Inspect an installed packaged plugin or workflow only when those layers cannot explain an execution-critical field, side effect, selector, confirmation path, or partial state.

Do not repeat source analysis merely to reconfirm behavior already captured by the Skill. Do not decompile or disassemble binaries, modify OBD or its plugins, execute extracted implementation code, or treat a development checkout as the default diagnostic interface. When packaged implementation inspection is necessary, keep it read-only, identify the exact installed artifact, and limit the conclusion to that evidence.

## Documentation Baseline

Official OBD documentation can establish the commands, options, schemas, and behavior documented by that publication. It does not prove the implementation of an installed package, map an RPM release to a source commit, or classify a whole product version as affected or fixed. Reconcile every execution-sensitive claim with the installed artifact.

<a id="source-evidence-boundary"></a>

## Source Evidence Boundary

A source path, symbol, or behavior in this revision refers only to the inspected `ob-deploy` checkout at commit `4ef23088b04cbba82793dbc718d3b844bcd0fdb5`. That hash identifies review evidence only; it is not mapped to an OBD product version or RPM release. Do not relabel the observation as released-version evidence or infer that another package, RPM revision, branch, or product version contains the same implementation. Use the installed implementation as the runtime authority for behavior that depends on it.

<a id="post-v460-development-observations"></a>

## Development Source Observations

Some reviewed development code, including the standalone management-IP command and its persisted loopback Observer-identity model, is development-source evidence rather than released-version evidence. Such observations may guide capability discovery but cannot establish package availability.

The reviewed development behavior uses these linked conditions:

- normal fresh `oceanbase-standalone` loopback identity requires component version `4.4.2.3` or later;
- a lower-version legacy deployment is considered only when it explicitly uses `local_ip=127.0.0.1` and the installed implementation can persist and verify that identity;
- `change-ip` requires a running, single-server `oceanbase-standalone` deployment with unchanged configuration and a verified loopback identity marker.

Do not infer an OBD release floor from those observations. Before using `obd cluster change-ip`, confirm the command and options from the installed help and apply the topology and identity checks documented for that operation.

## Evidence Maintenance Rule

Record the exact inspected checkout for a source observation, but do not infer a package mapping from its branch, tag, or version-like name. Label source-only behavior clearly and prefer the Skill, installed public help, registered/runtime behavior, and version-matched released documentation for operational decisions.
