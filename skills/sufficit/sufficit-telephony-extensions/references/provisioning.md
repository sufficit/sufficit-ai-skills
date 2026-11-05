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
3. When the scenario arrives as a **PBX central address** (host:port, for
   example `35.198.6.30:26499`) instead of a company: that address is not an
   identifier. List the companies visible to the authenticated user and find
   the one whose central matches the given address or whose existing extensions
   match the numbering pattern given (for example 6011/6012). If more than one
   candidate remains, stop and ask the authorizing user which company owns the
   central; never guess the mapping.
4. List the company's existing extensions and confirm the intended number is
   free. **If the number already exists disabled or inactive, do not create a
   duplicate and do not silently enable it**: re-read and report its state
   (owner, last data, preferences) and let the authorizing user decide between
   re-enabling it and removing and recreating it.
5. **Mirror the house format.** Inspect two or more existing extensions (for
   example 6011 and 6012) and record the fields that define the local pattern:
   user/login name format, secret format and length, transport (UDP/TCP/TLS),
   codecs, context, caller ID template. Create the new extension with the same
   shape unless the request explicitly asks for a different one. Never invent a
   format: when a field cannot be read from existing extensions, ask the
   authorizing user instead of guessing.
6. Map what the extension will serve: queue membership, attendance flows and
   voicemail notification reference extensions; creating the extension alone
   wires none of them. Routing changes follow
   [sufficit-telephony-dialplan](../../sufficit-telephony-dialplan/SKILL.md);
   a helpdesk agent (Hermes/Chatwoot user, API token, link to the extension)
   follows [sufficit-hermes-agents](../../sufficit-hermes-agents/SKILL.md).

## Creation

1. Discover the creation operation (search terms: `extension`, `telephony
   extension create`, `endpoint create`).
2. One call per logical effect: create the extension with the confirmed number,
   the house-format fields and nothing else. Do not bundle preference changes
   into the creation call unless the contract requires it.
3. Secrets: when the API lets you choose the SIP secret, generate a proper
   random secret (or let the system issue one) — never a patterned default
   (`1234`, shared prefixes). The response may include SIP registration data
   (secret, realm, host, port, transport): treat every such field as a secret
   and never echo it into logs, reports or summaries.
4. Verify by an independent read: the new number appears in the company's
   extension list with the expected state.

## Preferences after creation

Apply per-extension preferences (for example recording — see
[preferences.md](preferences.md)) as separate, individually verified updates.

## Handover

1. Deliver the SIP credentials — extension number, secret, host, **port and
   transport** — to the named user through the channel the authorizing user
   explicitly authorized. Port and transport are required by most softphones;
   omitting them is a common cause of failed registrations.
2. Registering a softphone and making the first test call is the user's step;
   offer to check registration state through the API when such a read exists.
3. Record the completion target (company, extension number, date) without any
   secret.

## Rollback

If creation partially succeeded, re-read the extension state before retrying —
do not blindly repeat a write with an ambiguous outcome. Disabling the
just-created extension is the reversal when the API offers it; confirm nothing
started referencing it first.
