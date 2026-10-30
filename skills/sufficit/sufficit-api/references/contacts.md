# Contacts

## Identity and discovery

Contacts are identified exclusively by GUID. Search the live OpenAPI by `contact search`, `contact attribute`, `contact important` or `contact delete` before calling. Use the default authenticated user context; inform `contextId` only when the user has clearly chosen another context he is allowed to manage. The server only answers for the caller's own context, contexts granted to it by entitlement, and any context for managers; `403` means that context is not accessible, so report it instead of trying other contexts or GUIDs.

The usual attribute keys are:

| Information | `key` | Use of `value` and `description` |
| --- | --- | --- |
| Name/title | `titulo` | name in `value` |
| Email | `email` | `value` address; optional `description` label |
| Telephone | `phone` | `value`; type as `cellular` or `business` in `description` |
| CPF/CNPJ | `cadastro` | `value` document |
| Tag | `marcador` | category in `value`; tag label in `description` |
| Owner | `idproprietario` | link managed by server in creation |

Do not invent keys for known data. Preserve the received spelling in existing custom attributes.

## Search and check

Prefer `POST /Contact/Search` as it accepts filters and attribute projection. A typical text search has this form, adapted to the context and request:

```json
{
  "contextId": "CONTEXT-GUID",
  "value": {
    "text": "search term",
    "exactmatch": false,
    "keys": ["titulo", "email", "phone", "cadastro"]
  },
  "keys": ["titulo", "email", "phone", "cadastro", "marcador"],
  "limit": 20
}
```

For a known GUID, use `contactId` and limit 1. Reading one contact by GUID (card, attribute, important flag) also requires access to it through its owner or group; changing it requires being its owner or a manager. Answer `204` means that nothing was found in the scope consulted. Do not conclude that contact does not exist in all contexts and does not extend the search without authorization.

Before changing, mark or delete, recover the contact and confirm GUID, title and relevant attribute. If name, phone number or email matches multiple people, present the options and do not choose by yourself.

## Create and update

`POST /Contact` creates when `id` is the empty GUID and updates when it receives an existing GUID. The body contains `attributes`, each with `key`, `value` and `description`. In creation, the server generates GUID and adds the session owner. Include at least `titulo` and only the requested data.

To edit an isolated attribute, prefer `POST /Contact/Attribute?contactid=...` with body as:

```json
{
  "key": "email",
  "value": "person@example.com",
  "description": "work"
}
```

This operation identifies an attribute by combining `key` and `description`. Read the existing value before: changing the description can create another attribute instead of renaming the previous one. To remove a specific attribute, discover and use `DELETE /Contact/Attribute` with exact `contactid`, `key` and `description`. Do not use empty value as shortcut for deletion.

When full update by `POST /Contact` is required, preserve existing attributes that are not part of the request. The endpoint adds or changes the attributes sent, but the agent should not treat a short answer as proof that the entire record remains correct; rereads the contact after writing.

## Importance and deletion

`POST /Contact/Important` receives `contactid`, `status` and an optional description. Marking as important protects contact against ordinary deletion. When removing the important flag, use the same description when it exists and validate the state afterwards.

`DELETE /Contact?contactid=...` permanently removes all contact attributes. Run only when the user requests deletion after an immediate reading that confirms the exact target. Inform that it is permanent and obtain confirmation if the initial request does not demonstrate knowledge of it. Do not automatically remove the important mark to make the deletion pass. Administrators may ignore this protection on the server, so the prior verification remains mandatory.

After any writing, do a new search by GUID and report the observed state. Minimize CPF/CNPJ, phones, addresses and emails in the user response.
