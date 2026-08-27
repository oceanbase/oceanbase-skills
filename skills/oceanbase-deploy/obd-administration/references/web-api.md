# OBD Web and API

Treat OBD Web as a controller-side management service that can expose deployment data and mutating operations. Starting the listener does not authorize any operation offered through it.

## Listener and Security Gate

1. Read the installed `obd web --help` and inspect version-matched implementation or documentation for bind address, port, whitelist, authentication, TLS, foreground/background behavior, idle shutdown, request/response logging, log redaction controls, log paths/permissions/retention, and stop behavior.
2. Record the controller identity, `OBD_HOME`, deployment inventory, active CLI/API tasks, existing Web processes/listeners, firewall or proxy boundary, and exact clients that need access.
3. Verify actual enforcement, not just option names. A build can expose a whitelist option while binding broadly or enforcing access differently than expected. Do not assume loopback binding, authentication, whitelist protection, or request-body redaction without evidence.
4. Choose the least exposed supported design. If the installed build cannot meet the required network and authentication boundary, stop and present the limitation; do not silently open a broad listener or change firewall/proxy configuration.
5. Show process owner, listener, exposed data/operations, credential handling, persistence, and exact stop method, then obtain authorization to start the service.

After start, verify the real command line, process owner, listener addresses, access controls, logs, and an authenticated read-only request from an approved client. Where feasible, verify rejection from an unapproved source. Web availability is not deployment health.

## Credential-Bearing Request Gate

Inspect the running version's server middleware before sending any password, private key, access secret, token, credential-bearing URI, or encrypted credential payload. Verified 4.7-era source enables middleware that logs the full URL, query parameters, and raw request body. Client-side output redaction does not prevent that server-side write.

If the exact version cannot prove server-side field redaction or a supported way to disable sensitive request logging, do not send a credential-bearing API request. Stop and use a reviewed protected CLI or other supported workflow, or require an approved server-side logging remediation and independent verification before the request. Tight file permissions and later log deletion do not make intentional secret logging acceptable; never delete broad logs as a substitute for preventing exposure.

## API Operation Model

Discover endpoints, schemas, task states, and recovery actions from the running version. Do not infer its API from another release.

For each mutation:

1. capture the exact resource and current state;
2. review the redacted payload and expected transition;
3. run a provided precheck when available;
4. obtain operation-specific authorization independently of listener-start authorization;
5. preserve the returned task ID and poll to a terminal state;
6. verify the resulting controller, deployment, component, or data-plane state outside the acceptance response.

An HTTP success or “accepted” response is not completion. Do not issue a conflicting CLI command while a Web/API task for the same resource is active, and do not replay a non-idempotent request after a timeout until server-side task state is known.

Before every request, verify that its URL, query, body, headers, client trace, proxy, and server logs satisfy the credential gate. Treat encrypted credential blobs as sensitive unless the protocol and logging design explicitly make their retention safe. Keep passwords, keys, image/repository credentials, API tokens, and credential-bearing payload fields out of logs and reports. When the scoped task ends, stop only the identified Web process unless the user explicitly requested persistence; service-manager creation or removal is a separate host mutation.

## Sources

- Official OBD V4.6.0 User Guide sections describing the graphical interface and asynchronous tasks.
- [Official public OBD V4.6.0 source baseline](../../references/source-baselines.md#official-obd-v460-baseline): `_cmd.py` `WebCommand`; `service/` listener, middleware, and task implementations.
