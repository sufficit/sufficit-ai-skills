# PJSIP-first provisioning training

Owner asked for PJSIP priority to prepare legacy SIP retirement. Published
sufficit-telephony-extensions 0.7.7 in d5a06f7 with a device-provisioning section:
choose PJSIP/GUID when enabled, keep account/auth/server consistent, use the
configured PJSIP endpoint and default TCP, retain numeric SIP for unsupported or
SIP-only cases. Do not disable SIP, rotate credentials or alter technology flags
as an implicit side effect. Registration and configuration delivery are separate.

Isolated validation passed 185 packages, catalog versions/index and Markdown
coverage; skill-creator validation and whitespace checks passed. The parallel
clear-technical-writing draft was preserved. No live agent behavior was tested.

Executor guide read-back SHA256:
6321f80488c2269caabcf67229eead6bd36bf313aee996fcc6ee78b70b08fd64.
Managed inbound/provisioning skill content SHA256:
8fd3148c5893f1bc68229bd1b3a8e21e379cba7306c240db71798cef1fa14b1c.
The other three bindings and queue resource remain unchanged. Combined length
39930 respects the existing budget. Native installer confirmed the enabled
package, persisted read-back confirmed the preference; no active turn was stopped.

A parallel Fleet restart interrupted the first voice pin before save. The binding
was then verified enabled, same-context and non-expired. With the service stable,
one retry returned synced for version 5639b6f5-d213-4553-80f6-2f79bca98f55, confirmed
by provider read-back. No new WhatsApp message, device write or call was sent.

Runtime renderers were implemented separately in sufficit-provisioning ca43d34:
all 77 modern tests passed and eveo-apps was deployed first. The owner then
permanently authorized castrum-apps provisioning publications; the same reviewed
release 20261112T182828Z-pjsip-first was deployed there successfully. Both hosts
confirmed identical Core hashes and Healthy. The completed service execution plan
was incorporated into its production activity and removed; no physical phone
registration/audio acceptance or blanket retirement of SIP is claimed. The
service README/config now carry the permanent authorization within authorized
changes, preserving validation, configuration and rollback requirements.
