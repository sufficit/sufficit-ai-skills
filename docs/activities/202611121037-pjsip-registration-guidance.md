# PJSIP registration guidance

Corrected reusable registration guidance after an agent treated a masked API password as a real credential, copied a hostname from OCR and interpreted normal GUID endpoint/AOR identities as a provisioning defect. It subsequently advised a GUID User with a numeric Login; the canonical profile requires the endpoint GUID in N format for both.

The native EndPointRegistrationProfile and read-only loaded endpoint/auth output agreed: voip.sufficit.com.br:26498 over TCP, endpoint/User/Login/auth/AOR using the endpoint ID without hyphens. Numeric extension titles and customer contexts are distinct. Port 26499 is the legacy chan_sip profile. Customer identifiers and credentials are intentionally excluded from this public record.

## Published packages

Commit e191f6e published sufficit-telephony-extensions 0.7.3 and sufficit-api 1.0.39. The [registration reference](../../skills/sufficit/sufficit-telephony-extensions/references/registration.md) defines the diagnostic flow and masked-credential boundary; provisioning and API guidance link to it.

## Managed agent delivery

Updated Rafael's existing private onboarding bundle through Fleet's revision-checked InstallSkill service. Preserved its two resource files byte-for-byte and the other three managed skill hashes. The always-injected root now includes the registration profile and masked-password rule. The four bindings total 39926 instruction characters, below the 40000-character budget. No additional skill or wider authority was introduced.

Installed content hash: `5d5a7e202d147539ef26dd7f8b5e59326e4e7aa41a6ea170d992bcb24b246c03`. Fleet confirmed the enabled executor package and persisted binding; independent read-back confirmed the hash, rule and unchanged companion skills. Installation returned installed-pending-session: it did not interrupt an active turn. Fleet composes settings for subsequent replies; actual receipt by a later conversation turn was not observed in this delivery.

Voice training version `874b40c4-6fd7-46fc-84c0-4395a218df5e` returned synced, confirmed by provider read-back. No voice tools, permissions or phone bindings were changed.

## Validation and limits

An isolated snapshot containing only the reviewed changes passed validation of 185 packages, skill-index and catalog-version checks, Markdown coverage and 47 unit tests. The first isolated snapshot lacked Git metadata; coverage-dependent checks passed after initializing that validation-only repository. Final delivery documentation passed Markdown coverage and whitespace checks.

Read-only runtime diagnostics confirmed matching GUID endpoint, AOR and authentication username. No credential rotation, generated peer edit, PBX reload, registration attempt or WhatsApp message was performed. Successful device registration remains unverified until the technician applies both GUID fields and retries. The unrelated clear-technical-writing draft was preserved.
