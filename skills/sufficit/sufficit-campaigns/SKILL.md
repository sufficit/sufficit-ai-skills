---
name: sufficit-campaigns
description: "Create, inspect and run Sufficit outreach campaigns through the corporate API: objective, script, targets, contact window, attempts, results and CRM review. Use when asked to prepare a campaign, import targets, check progress or read what a campaign collected. Activating a voice campaign places real phone calls."
metadata:
  version: "1.0.0"
---

# Sufficit campaigns

Campaigns exist only as an API. There is no management screen, so this skill is how an agent works with them. Use `sufficit_api_search` to confirm each operation in the live OpenAPI, then `sufficit_api_call` to run it. The deployed API is the authority on paths and fields. The connected user's credentials are attached outside the prompt.

A campaign knows nothing about telephony: it holds an objective, targets and attempts. An executor claims a due target, tries it and reports the outcome. Today the only executor is the Fleet voice agent, on channel `voice`.

## Safety first

**Activating a voice campaign dials real people**, immediately, inside the contact window, for every pending target.

- Never set a campaign to `Active` unless the user explicitly asked to activate that campaign in this conversation. Preparing, importing or "getting ready" is not a request to activate.
- Before activating, read the campaign and its summary, then tell the user how many people will be called, the window and the agent. Wait for confirmation.
- Create campaigns as drafts. A draft and a paused campaign never dial.
- To stop calls now, set the status to `Paused`. A call already in progress is not interrupted.
- Other campaigns may hold real people as pending targets. Never change the status of a campaign the user did not name.

## Routes

Base: `https://endpoints.sufficit.com.br`. Permission: entitlement `campaigns` in the campaign's context; manager and administrator reach every context.

| Operation | Route |
|---|---|
| List by context | `GET /campaigns?contextid=&status=` |
| Create a draft | `POST /campaigns` |
| Read | `GET /campaigns/{id}` |
| Edit | `PUT /campaigns/{id}` |
| Change status | `POST /campaigns/{id}/status?status=Active` |
| Counters | `GET /campaigns/{id}/summary` |
| Import targets | `POST /campaigns/{id}/targets` |
| List targets and results | `GET /campaigns/{id}/targets?status=&skip=&take=` |
| Attempts of a target | `GET /campaigns/targets/{targetId}/attempts` |
| Remove a target from the queue | `DELETE /campaigns/targets/{targetId}` |
| Compare results with the CRM | `GET /campaigns/{id}/crm/preview` |
| Write reviewed results to the CRM | `POST /campaigns/{id}/crm/apply` |

`PUT` replaces every editable field: read the campaign first and send the whole object back, or omitted fields are lost. It does not change the context or the status. It also accepts running campaigns, so an edit applies from the next dial.

Status flow: `Draft` → `Active` ↔ `Paused` → `Finished`. A finished campaign cannot be reopened. Campaigns cannot be deleted, so avoid creating test leftovers.

## Campaign fields

`contextId`, `title`, `objective`, `channel`, `instructions`, `maxAttempts`, `retryDelayMinutes`, `timeZone`, `windowStartMinute`, `windowEndMinute` (minutes of the day, default 540 to 1080), `windowDays`, `settings`.

`instructions` is the script the agent follows. Write it in the language of the call, in short sentences, because the voice agent speaks one short sentence at a time.

`settings` is a JSON string. Keys for voice:

```json
{
  "agentEndpointId": "<agent extension id in the campaign's context>",
  "firstMessage": "First sentence of the call",
  "amd": { "enabled": false, "arguments": "2500,1500,800" },
  "crmAttributes": [
    { "data": "instagram", "key": "social", "description": "instagram" },
    { "data": "whatsapp", "key": "phone", "description": "cellular", "requires": "whatsapp_permissao" }
  ]
}
```

Keep answering machine detection off unless asked: it leaves seconds of silence after the person says hello.

## Targets

`[{ "name": "...", "address": "5521...", "contactId": "<optional>", "variables": { "instagram": "@..." } }]`

- Targets are called in import order, so sort before importing, for example by value.
- A repeated address in the same campaign is ignored; the response says how many were added.
- The `instrucao` variable customizes the prompt for one target, for example how to say goodbye. It shares the 480-character limit, and commas and double quotes are removed.
- `variables` reach the agent, up to 480 characters in total, so it does not ask for what is already known. Do not put secrets or sensitive data there.
- Never import a number without a reason to believe it belongs to that target.

## Reading results

Target status: `Pending`, `InProgress`, `Succeeded`, `Failed` (refused), `OptedOut` (permanent, never call again), `Invalid`, `Exhausted`, `Cancelled`.

Attempt outcome: `Succeeded`, `NotAchieved`, `Retry`, `Callback`, `OptOut`, `Invalid`. The attempt's `externalId` is the conversation id. Enums may arrive as numbers in this order.

Report results as counts first and details on request. Target data can hold personal information.

## Moving results to the CRM

Results stay in the campaign until a person reviews them. Manager or administrator only.

1. Call `crm/preview`. It changes nothing and marks each value `New`, `Same`, `Conflict` or `NotAllowed`.
2. Show the user what would be written, especially conflicts.
3. Only after approval, call `crm/apply` with the reviewed `targetIds`. It writes new values only and reads each one back.

A conflict is never overwritten: tell the user so a person can check with the customer. A contact attribute is identified by contact, key and description, so a different description creates a second record.

## Rules for scripts

- The voice agent never denies being an AI when sincerely asked, and no script may tell it to.
- A request not to be contacted becomes `OptedOut`. Do not work around it with a new campaign.
- Do not script discounts, promises or prices the user did not approve.

## Live events

Optional. SignalR hub at `/ws`: call `JoinCampaigns(contextId)` and listen to `CampaignEvent`. Delivery is best effort, so reconcile through `/summary` and `/targets`. The API is the source of truth.
