# Extension provisioning runbook

Create an extension (ramal) for a company and hand it over safely. Flow-first:
discover each call in the live OpenAPI before running it, then record what the
deployed API actually offered (field names, required arguments, response shape)
in this file as part of the change that first validated it.

## Pre-flight

1. Confirm the authorizing user, the target company and the person who will use
   the extension (name; e-mail when applicable).
2. Resolve the company through the API. When several companies are visible,
   confirm the identity (name or GUID) back to the requester before writing.
3. List the company's existing extensions: confirm the intended number is free
   and consistent with the numbering already in use (for example a sequential
   60xx next to existing 60xx extensions).
4. Map what the extension will serve: queue membership, attendance flows and
   voicemail notification reference extensions; creating the extension alone
   wires none of them.

## Creation

1. Discover the creation operation (search terms: `extension`, `telephony
   extension create`, `endpoint create`).
2. One call per logical effect: create the extension with the confirmed number
   and the minimal required fields. Do not bundle preference changes into the
   creation call unless the contract requires it.
3. The response may include SIP registration data (secret, realm, host). Treat
   every such field as a secret: never echo it into logs, reports or summaries.
4. Verify by an independent read: the new number appears in the company's
   extension list with the expected state.

## Preferences after creation

Apply per-extension preferences (for example recording — see
[preferences.md](preferences.md)) as separate, individually verified updates.

## Handover

1. Deliver the SIP credentials (extension number, secret, host/port) to the
   named user through the channel the authorizing user explicitly authorized.
2. Registering a softphone and making the first test call is the user's step;
   offer to check registration state through the API when such a read exists.
3. Record the completion target (company, extension number, date) without any
   secret.

## Rollback

If creation partially succeeded, re-read the extension state before retrying —
do not blindly repeat a write with an ambiguous outcome. Disabling the
just-created extension is the reversal when the API offers it; confirm nothing
started referencing it first.
