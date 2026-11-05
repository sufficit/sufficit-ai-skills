# Skill version metadata and official notification tests

Session: 01a1acef-9b0e-7333-a48f-3c0f3e6b75b1.

sufficit-api 1.0.24 adds the explicitly requested recipient-scoped simulated
low-balance alert test. The official web Subscriptions page's "Enviar teste"
action calls the event's Test method for one contact, using the real balance and
normal notification transport. It does not change thresholds or account balance.
A test triggers a real message; neither a synthetic amount nor a TEST label is
promised. The broad HEAD Balance Force action is explicitly distinguished.

The reviewed catalog now includes versions actually declared in package metadata.
A generator/check prevents stale values without inventing versions for unversioned
upstream packages. The Genius host consumes this field and reads installed versions
from their own package; UI/device validation is tracked in Genius's
PLAN-SKILL-VERSIONS-AND-AGENT-UPDATE.md for this same session.

Validation: package digests updated; 185 packages, catalog/index/Markdown coverage
and the managed installation/parser test suite. Device outcomes are recorded in
the Genius activity after execution, not inferred from this publication.
