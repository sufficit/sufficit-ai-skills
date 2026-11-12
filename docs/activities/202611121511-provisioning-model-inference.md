# Provision first with an informed model inference

The owner corrected the preceding review: a MAC prefix is a useful way to deduce
a likely device model. Minimize blocking questions, register the plausible model
first, then disclose the assumption and ask for confirmation/correction. This
supersedes the model-confirmation gate in the earlier review; it does not change
its call-correlation or multiple-device guidance.

Published sufficit-telephony-extensions 0.7.6 in commit 999f029. The
[provisioning reference](../../skills/sufficit/sufficit-telephony-extensions/references/device-provisioning.md)
now uses OUI/vendor, historical profiles, customer fleet and request evidence to
select a supported provisional model. It distinguishes inference from certainty,
keeps target MAC/customer/extension explicit, and permits an already authorized
replacement to proceed before the model answer. It does not authorize disabling
an unrelated device or guessing the target identity. Unknown model alone is not
a reason to block a plausible registration; no plausible supported profile or
materially conflicting evidence still calls for the missing information.

An isolated snapshot excluding the parallel writing draft passed validation of
185 packages, catalog versions, skill index, Markdown coverage and whitespace
checks. No executable product code or device configuration changed. No live model
behavioral test was performed.

Atomically updated the executor guide at
/data/support/provisioning/DEVICE-PROVISIONING.md with an expected-old-hash guard.
Read-back hash: 7b3dda128cb24fef8fc6522060815ec93bac44761f8c41b9552820cbff0b3774.
Replaced only the existing inbound/provisioning skill's model sentence through
the native revision-checked installer. Other three bindings and its queue resource
were preserved. Combined instruction length 39922 remains within the budget.
Persisted content hash: a67b4b4a10965a068c0b5889e16f1db839878d575986ee6ab83dfd61f7e8adfa.
Native install returned installed-pending-session; no active turn was interrupted.
Voice version 1ed25b8e-c212-4593-a4c5-0b8621cb0f6b returned synced, confirmed by
provider read-back. Future model compliance has not been observed.

All checkpoints (policy update, validated publication/native synchronization,
verified delivery record) are complete. This activity replaces
PLAN-PROVISIONING-MODEL-INFERENCE.md. Private receipts: workspace
tmp/rafael-inference-20261112. No group messages were sent.
