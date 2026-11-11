# Internal queue-number diagnostic training

Updated sufficit-telephony-dialplan to0.4.0. Queue numbers are compatibility
projections separate from native queue policy, members and DIDs. Training now
uses the actual registered caller context and loaded numeric map, then matches
the GUID against the customer's catalog. A route present in a global context
may be unreachable from a tenant context; an endpoint404 or metadata search
cannot decide that question. Queue destination is an exit/fallback, not ingress.

Documented catalog list-then-select reads (a single-resource GET can return405),
exact digit preservation, safe read-only diagnostics, and CDR evidence limits.
No customer number, identity, private mapping or credential is included in the
public package. Business writes remain API-only; shared reloads require approval.

Updated entrypoint, reference, release/card/catalog versions and package digest.
Validator passed all185packages. The support deployment also updates its existing
private inbound-lookup binding rather than adding a fifth skill; prior DID/QuePasa
rules are consolidated to retain the existing40000character configuration limit.
No PBX mutation, call or production restart is part of this correction.
