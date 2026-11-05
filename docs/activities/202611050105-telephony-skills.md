# Sufficit telephony management skills

Created `sufficit-telephony-extensions` and `sufficit-telephony-dialplan` from
the telephony gap found while handling a customer request (SIP extension 6013 +
helpdesk agent). The system is too broad for one skill, so it starts split by
domain, following the sufficit collection conventions (front matter, references,
skill card, release.json, MIT-0).

## Design

- `sufficit-telephony-extensions`: extensions (ramais) and per-extension
  preferences. The provisioning runbook is flow-first: discover each call in
  the live OpenAPI, then record the real fields in the reference as part of the
  change that first validated them. Call-recording semantics come from the
  product guide (on by default per extension; carrier-voicemail caveat).
  Credentials policy: issue once, deliver only through the channel the
  authorizing user explicitly authorized; sending credentials to a third party
  is a separate explicit decision.
- `sufficit-telephony-dialplan`: routing layer — attendance flows, applications
  and destinations, queues and members, voicemail as a destination, inbound
  DIDs and outbound trunk rules (individual trunk limits, 72-hour window).
  DID-vs-voicemail distinction and `configuredWaitSeconds` semantics carried
  over from the sufficit-api telephony reference.

Both cross-link `sufficit-api`, `asterisk-dialplan` and each other instead of
duplicating scope. Versions start at 0.1.0: flows and semantics only; exact API
calls must be confirmed against the live OpenAPI on first real use and recorded
in the references in that same change.

## Validation and scope

- `scripts/validate.py` passes with 183 packages (digests recomputed).
- `scripts/build_skill_index.py` regenerated; `scripts/markdown_coverage.py`
  passes (all documents reachable from README.md).
- Full test suite passes; README collection counts corrected: the Hermes row
  was missing and `catalogEntries` in `catalog/upstream-v2.json` was stale
  (180) against the 181 skills already on `main`; both now reflect 183.
- No telephony API was called and nothing was provisioned; no secrets involved.
