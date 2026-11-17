# Carrier SIP line onboarding training

The maintainer asked to improve Rafael's handling of a TIP Brasil SIP line using
the Datora workflow as a reference. The conversation showed that Rafael started
with the trunk catalog, received a scope refusal and suggested access or a shared
trunk before resolving the operation. No line was created during the exchange.

The Endpoints controller and Standard provisioning code distinguish a SIP peer
from a REGISTER entry. The Datora activation API is scoped to its dedicated
worker and carrier profile. The shared interconnection controller has read,
aggregate write and operational status routes restricted to Administrators.
These findings are reflected in
[carrier SIP line onboarding](../../skills/sufficit/sufficit-telephony-dialplan/references/carrier-sip-line-onboarding.md),
published as part of dialplan skill 0.7.7. The guidance covers trusted customer
and duplicate lookups, verified carrier parameters, private handling of secrets
and separate register and call evidence.

Rafael's existing native persona was updated through the conditional Fleet API.
An independent GET confirmed the exact updated content and the native
`agent-file` revision
`5F20C7EECF45E0C6902A28FC77C38611991F9257A691BAB66CD84AB92956C2E0`.
The rollout used no PBX or carrier write. The scoped TIP registration path
and end-to-end use on a real line were outside this training validation.

All 70 repository tests passed. Package validation covered all 195 public skills.
The catalog version, index and Markdown checks also passed.
