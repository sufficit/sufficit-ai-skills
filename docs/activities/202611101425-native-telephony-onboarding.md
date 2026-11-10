# Native telephony onboarding and current mission guidance

Updated sufficit-api to 1.0.32 and sufficit-telephony-extensions to 0.5.0.
The onboarding reference distinguishes an active native contract from an empty
legacy service projection. It uses the live versioned OpenAPI, sales session
epoch/snapshot headers, initialization state and existing-contract Preparation.
It explicitly forbids creating duplicate free commercial coverage to bypass setup.

Added the current Fleet missionId requirement: retained conversations contain old
IDs, so a rejection for an inactive mission requires checking the current host
guidance before claiming missing write permission. A failed read does not prove
that a document write was refused or that the existing file is empty.

Updated package versions, cards and digests in both catalog and manifest. All 185
public packages validated; Markdown coverage passed. Source 723406c committed/pushed.

Fleet's bound diagnostic package contained an old duplicate onboarding recipe,
while the separate onboarding catalog package was unbound. The native rollout
consolidated the duplicate content into the proper onboarding binding, preserved
password-scope semantics, customer-name lookup, DID/QuePasa diagnostics and clear
writing, and respected four bindings/40000 characters. Native rendered content
was confirmed in the actual executor System trajectory, outside visible user text.
Rafael's real follow-up created/read four endpoints and updated group documents.
Queue/DID completion is tracked in Fleet. No credentials were embedded in packages.
