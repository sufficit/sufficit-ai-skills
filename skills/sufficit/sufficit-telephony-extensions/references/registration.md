# Device registration and authentication diagnostics

## Canonical PJSIP device profile

The native `EndPointRegistrationProfile` in sufficit-blazor is the device setup
contract; `PJSIPRuntimeId` in sufficit-base defines the same runtime identity.
Current new-device defaults:

- Host/domain: `voip.sufficit.com.br`, port `26498`, transport TCP.
- Account/user and authentication login: the ENDPOINT `id` in GUID N format
  (32 hexadecimal characters, no hyphens). Use it as the registration/AOR user too.
- Password: that endpoint's actual password from the authorized portal/device
  provisioning flow; never substitute the customer default or another endpoint.
- Extension `title`/friendly number, customer `contextId` and linked Identity
  `userId` are different identifiers. A numeric legacy title such as `0000006001`
  is not this PJSIP login. `6001` is a number to dial, not the registration identity.

Resolve GET `/Telephony/EndPoint/ById?id=<endpoint GUID>` or the scoped extension
list. A known legacy title can be resolved with GET
`/Telephony/EndPoint/ByExtension?extension=<title>`; verify the returned `contextid`.
Derive the login from `id`, not a guessed prefix or customer GUID. If a supplied
"context GUID" resolves to an endpoint, obtain its owning context through the API.
A GUID is not a context merely because it has GUID syntax.

Example: endpoint id `0f8fad5b-d9cb-469f-a165-70867728950e` registers as
`0f8fad5bd9cb469fa16570867728950e`, even if its title is numeric. Do not ask the
technician to copy an ID that the authorized API already returns unambiguously.

Port26499 is legacy chan_sip, distinct from PJSIP26498. A missing chan_sip peer
does not establish a PJSIP failure. SIP/PJSIP creation flags do not change the
canonical PJSIP registration username; do not disable a protocol to fix a login.
An explicitly verified server may accept UDP too; do not diagnose credentials
from a transport label alone. New setup follows the native TCP profile.

## Read the failure at the correct layer

1. Confirm the endpoint and owner, then host, protocol/port, registration user,
   auth login and the actual AOR. Treat screenshot OCR as a hint: validate the
   official hostname rather than repeating a misspelling as configuration.
2. Distinguish challenged authentication from its outcome. InvalidPassword or a
   phone's "Senha incorreta" does not prove a person mistyped the password:
   wrong driver, account/auth identity or realm can also invalidate the digest.
3. A GUID-named endpoint/AOR/auth is normal. `AOR '' not found` or404 with a
   numeric PJSIP user first calls for correcting the device identity. Do not
   declare corrupt AOR generation or ask engineering to rename GUIDs until the
   canonical profile was actually used and server evidence still shows a defect.
4. The API helper can redact `password` as a marker. A redacted/masked string,
   even with the expected length, is NOT a password and cannot be compared with
   the technician's value. State that comparison is unavailable. Never disable
   masking, inspect token files or read raw secrets just to bypass this boundary.
5. Offer the complete verified device profile, keeping the existing secret. Do
   not reset credentials, recreate the endpoint, edit generated files or touch
   another driver to compensate for an untested client configuration. If the
   technician retries with the canonical account, correlate time/endpoint and
   actual registration state; a config read alone does not prove registration.

Do not solicit or repeat plaintext secrets in a group or summary. A secret already
posted there is not authorization to rotate it. Follow the existing scoped
password-change request and secure-delivery rules when a change is requested.
