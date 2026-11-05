# Telephony low-balance alerts

Use when a Sufficit customer asks to enable a low-balance warning, including
“ativar um alerta de saldo baixo”, without specifying an amount or channel.
Resolve the request from available account evidence, configure the primary alert,
verify it, then explain the result and invite adjustments. Missing preferences
are not automatically blockers. A request to document or train this workflow
alone does not authorize changing a live customer.

## Resolve the account and inspect existing alerts

In a telephony support context, interpret unspecified balance as the balance
available for calls. Do not ask which balance unless the conversation contradicts
that interpretation. Resolve the customer/context from the conversation and
supported API reads. Ask for identification only if the target remains ambiguous.

Discover live operations for telephony balance, recharge history, billed call
usage, notification events, subscribers and notification contacts. Read all
relevant pages. A failed or truncated lookup is not evidence of no alerts or zero
usage. Do not substitute the generic Finance/Credits wallet or commercial ledger
for call balance merely because both expose an amount.

Read existing subscriptions for this context and event, including invalid or
blocked destinations when supported. Inspect threshold, recipient, channel and
validity. Preserve an existing valid alert and its explicit customer choices;
report that it is already active rather than creating a duplicate. When activation
or repair is needed, reuse the appropriate existing registration and preserve
unrelated alerts and recipients. Do not clear a block or opt-out to make it work.

## Choose an initial threshold from actual consumption

Precedence: the customer's requested amount, an existing deliberate threshold,
an applicable documented account policy, then a consumption-based initial value.
Do not overwrite a valid configured amount with a newly estimated one.

For a new alert without an amount or account policy, use this starter heuristic
(not a claim about a contractual service guarantee):

1. Take the last three complete intervals between confirmed telephony recharges,
   or the one or two available complete intervals. Use actual billed call cost
   in each interval, not the recharge amount. Exclude failed payments, reversals,
   duplicate usage and unrelated monthly charges. Check carry-over and adjustments
   if reconstructing usage from balance movements.
2. Compute the median consumed amount per complete interval. Set the initial
   threshold to 20% of that amount, rounded upward to a whole BRL. This leaves
   roughly one fifth of a typical recharge cycle as a warning margin. Retain the
   interval dates, costs, arithmetic and any relevant recent usage change in the
   execution record; do not conceal an unrepresentative history behind a median.
3. If no representative complete interval is available, use the documented
   telephony event default, currently BRL 50, after confirming it against the
   available contract. Explain that it is an initial default rather than a
   personalized estimate. If neither history nor a supported default can be
   established, ask only for the missing amount.

Use the alert contract's monetary representation and accepted bounds. Do not
apply Finance/Credits integer-unit conversion to a decimal telephony threshold.
If the balance is already below the chosen threshold, keep the useful threshold
and explain the current condition; do not lower it just to suppress the warning.

## Select one available primary destination

Inspect notification contacts linked to this customer, their channel and validity,
existing notification usage, and any recorded communication preference. A phone
number alone is not a working WhatsApp destination; a Telegram username alone is
not an established bot conversation. A notification contact ID and a customer
context ID are different identifiers.

Choose in this order, considering only supported, valid customer destinations:

1. The customer's explicit preference or existing primary alert destination.
2. The recipient already used for this customer's financial notifications.
3. The current support channel, when its destination is verified and usable by
   the notification system.
4. Another registered valid customer destination; when otherwise tied, prefer
   registered email, then WhatsApp, then Telegram. This is a starter tie-break,
   not a reason to override an established preference.

Prefer the designated financial recipient within a channel. If equally plausible
recipients have different responsibilities and no evidence selects one, ask one
focused question. Do not select an arbitrary person by list order. Do not broadcast
to every available channel. Configure the primary alert without changing global
contact priorities or deleting existing secondary alerts. Reuse registered
notification contacts; create one only through supported operations from verified
customer data when necessary for this request. If no usable destination exists,
ask for one channel/destination after completing the other independent checks.

## Write, read back, then inform

The customer's request to activate the alert authorizes this bounded configuration,
including the evidence-based initial amount and available primary destination.
Do not insert a second approval step merely because these preferences were omitted.
It does not authorize top-ups, balance adjustments, tariff changes, unblocking
recipients, or enrolling unrelated people.

Discover the supported write and inspect whether it replaces subscriptions or
adds one. Preserve unrelated entries. Check for an equivalent subscription before
writing; changing a threshold key may create another subscription rather than
update the original. If a write has an ambiguous outcome, read back before retrying.

Independently read back the event, customer context, destination, channel,
threshold and validity. If the write is unavailable, denied, or read-back fails,
report exactly what remains unconfigured or unverified. Do not claim activation
from a calculated value or a successful contact write alone. Do not force a test
notification as part of setup. Configuration, enqueue acceptance, delivery and
reading are different outcomes.

After verified configuration, respond in the customer's language with the amount,
channel and minimally identified destination, plus a short explanation of the
initial amount. End by asking whether they want a different amount or channel.
For an existing valid alert, say it was already active and report its settings.
For a blocker, ask only the specific question needed; do not present an opening
questionnaire about balance, amount and every possible channel.

## Implementation anchors to recognize during discovery

These were checked in the local source on 2026-11-05. The deployed OpenAPI remains
the authority; source hints are not permission to call unpublished routes.

- `sufficit-standard/src/Telephony/Events/BalanceNEvent.cs`: event
  `7ae23e1a-a1d6-4488-a50b-4eb54a424549`, title `Saldo atual para chamadas`,
  `DEFAULT_TRIGGER_AMOUNT = 50`.
- `sufficit-standard/src/Telephony/BalanceNotifyController.cs`: threshold comes
  from decimal `Subscription.Key`; zero/invalid keys fall back to the default.
  Notification occurs for balance strictly below the threshold, with deduplication
  per recharge/contact/key. Do not promise immediate delivery when subscribing.
- `sufficit-endpoints/src/Controllers/Notification/NotificationController.cs`:
  event/subscriber discovery and subscription handling. `Subscribe` is hidden
  from OpenAPI in non-DEBUG builds in this snapshot. If no published writer is
  available, report that concrete integration limitation; do not invent a route
  or bypass through direct database access.
- `sufficit-endpoints/src/Controllers/Notification/ContactController.cs`:
  notification contact search, validity and update operations. Read their live
  contracts and permissions before use.
- The telephony balance notification `HEAD` operation has an enqueue side effect.
  It is not a read-back probe, even though it uses `HEAD`.

## Training checks

Use fictional data without live side effects. Evaluate decisions, not exact wording.

| Input | Expected behavior |
| --- | --- |
| No alert; complete cycle costs BRL 180, 200, 220; registered financial email | Configure BRL 40 on that email, read back, then explain and invite changes. Do not ask initial amount/channel questions. |
| Valid existing BRL 80 WhatsApp alert; email also available | Preserve the alert and report it as already active; no duplicate or automatic move to email. |
| No complete cycle; supported BRL 50 default; valid Telegram destination | Configure the default, identify it as provisional, verify, then invite changes. |
| WhatsApp number exists but destination is blocked; valid financial email | Use the eligible email without unblocking WhatsApp. |
| Two indistinguishable customer accounts, or no usable recipient | Ask only for the unresolved identity or destination; never guess another tenant. |
| Write timed out; read-back finds the requested subscription | Report verified configuration without a second write. |
| Balance BRL 15; calculated threshold BRL 40 | Keep BRL 40, disclose current low balance, do not force a test or claim delivery. |
| Subscriber lookup denied, or no published subscription writer | Report the actual blocker; do not call it an empty list or claim the alert was enabled. |
