# Network Identity and Client Access

Use this workflow for the tested controller SSH path, Observer/OBProxy access, SQL/RPC/obshell listeners, inter-node reachability, tenant allowlists, and monitoring or Config Server endpoints.

## Resolve the Access Topology

Record each layer separately:

| Layer | Resolve |
|---|---|
| OBD management | controller-to-target SSH address, machine identity, route, SSH user/host-key policy |
| Observer | advertised/bound SQL, RPC, obshell addresses and ports; zone/server identity |
| OBProxy | Community Edition component key, backend discovery, listener, tenant routing, and credentials |
| Config Server | endpoint and the exact OceanBase/OBProxy consumers that reference it |
| Client | source networks, proxy/direct endpoint, tenant/user syntax, and allowlist/firewall |

Direct Observer SQL access is valid when it meets the request. Add OBProxy only for a required routing/availability outcome. Nginx, HAProxy, a cloud load balancer, VIP manager, DNS, and firewall are external systems; describe their boundary but do not install or mutate them without explicit scope.

## Access and Security Gate

Build an approved source-to-destination matrix with protocol, address/port, authentication, allowlist/firewall owner, and health check. Preserve at least one reviewed management path before tightening access. Never expose database, obshell, proxy, or monitoring listeners broadly merely to pass a check.

Keep database and proxy credentials out of argv, YAML displays, and reports when the installed client offers a protected channel. If it accepts a required secret only in argv, disclose the exposure and use an approved permission-controlled local procedure; never call that path protected. A TCP connection does not prove authentication or routing to the intended tenant.

## Acceptance

Verify registered and generated configuration, actual bind/advertised listeners and process owners, product-side server addresses, peer RPC connectivity, OBProxy backend/route health when selected, and authenticated client access from an approved source. Where feasible verify rejection from a non-approved source without disrupting production.

Test direct Observer, OBProxy, Config Server, and monitoring paths separately when selected. Report which path was tested; one working endpoint does not prove all nodes or access layers.

On failure preserve the access matrix, routes, listeners, effective configuration, and Trace. Do not change firewall or proxy topology as a generic response to an unrelated OBD error.
