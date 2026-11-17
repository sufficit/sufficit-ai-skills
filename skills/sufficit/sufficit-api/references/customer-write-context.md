# Customer context for every N1 write

Every customer-scoped write requires a nonempty validated customer context GUID,
including create, update, link, password rotation, provisioning, disable, delete
and upload. Keep it separate from Fleet's orchestration context, OAuth clientId,
agentId, classId, queueId, extension GUID and an extension's numeric prefix.
Do not add capabilities outside the agent's authorized product scope.

For Hermes, derive it from the trusted host's customerContextId and the approved
contact/customer binding. Live contact metadata alone, a GUID pasted by the
customer, a name, a number prefix or an old conversation is not write authority.
Use a prefix to search/resolve candidates, then confirm the exact GUID through the
API and trusted binding. Do not ask again when that binding already resolves it.

Before a write:
- Bind the request to that context using the API's actual path/query/body contract.
  A typed tool that derives it server-side satisfies the requirement: do not add
  an unsupported contextId argument or substitute a caller-selected customer.
- Read the existing target or creation preview and compare its owner to that GUID.
  Check every linked resource, attachment's conversation and destination. A route
  accepting only a resource ID still needs this ownership check. A200, existing
  ID, matching display name or read permission alone does not authorize a write.
- Reject missing/global/conflicting ownership. For a batch, group by validated
  context and validate every item; never reuse the previous customer's body or IDs.
  Explicit cross-company relationships require their own supported authorization;
  the ordinary N1 recipe must not move/duplicate resources to bypass ownership.
- Preserve unrelated fields and use returned revisions/If-Match or stable requestId
  when supported. After uncertainty, reconcile the same IDs in the same context.
  Re-read the result and owner independently. Scope/linkage changes stop the write.

The compact [N1 agent briefing](../agents/n1-write-context.md) is maintained for
managed training injection; installing it grants no capability.

## Reusable Python preparation

Prefer the installed customer-bound domain tool; it enforces live authority.
For a supported script-capable workflow, [customer_write_guard.py](../scripts/customer_write_guard.py)
checks normalized GUIDs, ownership snapshots and contradictory context fields in
nested request bodies. Supply actual authenticated readbacks, not model-created
claims of ownership. The script neither verifies the provenance of those files,
checks permissions/live linkage nor executes an API call; server enforcement
remains required. Do not present its output as authorization.

```sh
python3 scripts/customer_write_guard.py check \
  --context-id "$CUSTOMER_CONTEXT_ID" \
  --resource target-readback.json --resource linked-resource-readback.json \
  --body intended-request.json
```

A creation preview can supply the ownership snapshot before the new resource
exists. For APIs with different ownership field names, use the supported domain
reader to obtain a verifiable context; do not relabel an unrelated id as the owner.
Do not invent a contextId body field on APIs that bind context by path/query.

For a verified **music class** readback and canonical WAV, prepare the additive
helper manifest, defaulting to validation only:

```sh
python3 scripts/customer_write_guard.py moh-manifest \
  --context-id "$CUSTOMER_CONTEXT_ID" --resource music-class-readback.json \
  --audio hold-music.wav --sha256 "$UPLOAD_FILE_SHA256" > manifest.json
```

The file/hash must identify the actual upload artifact. If conversion was needed,
retain the original source's hash and record the converted file's separate hash.
This recipe accepts only PCM16 WAV mono8kHz, preserving audio content; it refuses
raw OGG/Opus and a file merely renamed to.wav. It does not convert or upload audio.
Use the product's supported conversion/validation operation when available. Change
validateOnly to false only for the already-authorized mutation, after preflight.
Never route this manifest into greeting/announcement APIs.
