# ISP service manual

Use the scenario matching the customer's problem. Read the shared entrypoint for
identity verification, evidence boundaries and execution permissions. Examples
below are original training language; adapt them to the customer's language and
confirmed facts. Replace placeholders before use. Do not invent a commitment to
make a sentence sound complete.

## 1. Connection failure and safe first checks

Establish whether the failure affects all devices, only Wi-Fi, one device or one
application; when it started; and whether any connection still works. Check known
outages and existing tickets before repeating local troubleshooting. Ask what has
already been attempted and distinguish the router from a separate optical terminal
(ONT) where applicable.

Describe indicators by label and behavior, not just color: power, LOS, PON,
internet/WAN and Wi-Fi vary by device. A red light alone does not diagnose the
fault. Use the provider's device-specific runbook and available telemetry. Guide
only simple, reversible steps the customer can safely perform; do not ask them to
handle exposed wiring, climb or disconnect optical fiber as a generic test.

A power cycle interrupts service: explain that and check whether the customer can
do it now. Do not force repeated restarts after an outage is confirmed or after
the same step has failed. Escalate with observations and previous results.

Example: “You have already restarted the equipment and both devices remain
without internet. I will use that result in the diagnosis rather than ask you to
repeat it. The next check is [specific available check].” Use future wording only
when that action is actually available and will be performed.

## 2. Failure after changing a password or following a bot

Clarify what the customer changed: Wi-Fi password, Wi-Fi name, router admin
password, WAN credentials, power connection or a physical Reset/WPS button. Ask
what instructions they followed and on which channel. Do not assume the phone
menu and a WhatsApp bot presented the same instructions.

Restarting preserves configuration in normal operation; a factory reset can erase
provider settings. Do not tell a customer to hold Reset or WPS without an approved
model-specific procedure and a recovery path. Do not ask them to send credentials.
If the equipment was reset, stop the repeated reset loop and route to authorized
configuration recovery or a technical visit. Record the model and observed state.

A changed Wi-Fi password can require devices to reconnect with the new password;
that differs from loss of WAN provisioning. Establish which layer is affected
before giving instructions. If automated guidance may have contributed, preserve
the relevant bot flow/version through authorized internal records for review.
Acknowledge the sequence without declaring causation from chronology alone.

Example: “The connection stopped after those instructions. Let's identify which
setting changed so we can choose the correct recovery step. Please do not press
Reset again.”

## 3. Repeated contact, missed estimates and work disruption

Read the original opening time, promised updates, recent notes and attempted
repairs. Restate the unresolved issue so the customer does not repeat the whole
story. Recognize the specific impact, such as inability to work, without promising
priority unsupported by the provider's criteria.

If a deadline has passed or no owner is assigned, route the existing case to the
responsible queue or supervisor under the provider's escalation rules. Record
what response you need from that team. Repeatedly saying “urgent” without an owner
or tracked action does not advance the case. Do not open an unrelated duplicate
or quietly reset the deadline.

Distinguish:

| Statement | Required basis |
| --- | --- |
| Repair estimate | Estimate supplied by the responsible team, with uncertainty |
| Appointment window | Confirmed booking and customer availability |
| Next status update | Named owner and an update mechanism the provider can fulfill |
| Escalation requested | Successful recorded request; no implication it was accepted |

If there is no confirmed repair time, say so. Obtain an update arrangement through
the actual workflow; if you cannot, explain which team must confirm it. Do not
invent a callback time or claim a reminder has been created.

Example: “The earlier estimate has passed and the problem is still open. There
is no confirmed repair time in the record. [Verified escalation or next available
action].” Explain any confirmed interim option and its limitations; do not promise
credits, reimbursement or a backup connection without applicable policy.

## 4. Visit recorded but disputed by the customer

Record both accounts neutrally: the system entry's reason and timestamp, and the
customer's statement that they were present or saw no technician. Neither source
alone settles the disagreement. Do not say the customer is mistaken or accuse the
technician of falsification.

Check the service address, appointment window, contact number and access
instructions. Ask the field-service owner to review dispatch records, attempted
contacts and available visit evidence. Restrict employee/location evidence to the
internal review; do not expose tracking details to the caller.

Preserve the original history. Reopen or create a linked investigation according
to policy and authorization; do not overwrite the disputed reason as if verified.
Restore service handling while the discrepancy is reviewed. A new visit needs a
confirmed booking, not merely a reopened ticket.

Example: “The record says the visit could not be completed, and you report being
home without receiving a visit. These accounts differ. [Verified review action].
Let's confirm the address and contact details for the next step.”

## 5. Field team cannot access the location

Confirm the operational status with dispatch: inability to contact the customer,
physical access, temporary restriction or another documented issue. If the reason
is unknown, state that instead of repeating an unexplained “access difficulty.”
Do not label a neighborhood or speculate about crime.

Explain the service impact without exposing sensitive staff or security details.
Do not pressure a customer to meet a technician in an unsafe place or override
field safety decisions. Obtain a safe next step from the responsible team:
rescheduling, approved remote assistance or another available service option.
Record who will review the restriction and when an update is actually confirmed.
If the provider cannot confirm continued service, escalate that decision rather
than leaving a repair ticket indefinitely described as routine waiting.

## 6. Installation feasibility, old accounts and unpaid invoices

Separate technical availability, commercial eligibility, overdue invoices and
installation scheduling. A nearby active subscriber does not guarantee an
available port or service at the requested address. A paid invoice does not prove
technical feasibility or reserve an installation slot.

Check the provider's current process for preliminary coverage checks and technical
surveys. Do not create a rule requiring settlement before any information can be
given merely because an agent said so in a sample call. If a policy restricts an
action, explain the verified restriction, what can still be checked and the route
for a billing dispute. Do not promise approval or advise bypassing the policy.

For an old account, route disputed equipment return and outstanding charges to
their respective records. Never assume a router was returned because the caller
no longer sees it, or assume the debt is valid solely from the customer's history.
Give the next documented verification step.

Example: “Coverage at your new address has not yet been confirmed. The account
also has an item that needs billing review. These are separate checks; payment
alone would not guarantee installation.”

## 7. Invoice, payment link and email delivery

Verify the account through the approved process. Use the official billing system
and approved delivery channel; do not invent a payment URL, QR code or Pix key.
Never substitute an employee's personal payment destination. Explain how the
customer can check the beneficiary against the verified provider billing record.
If the destination appears inconsistent, stop the payment instruction and route
for verification through an official channel. Do not conclude fraud without evidence.

If a link changed, provide only the current verified link and an accessible
alternative. A customer without WhatsApp must not be trapped in a WhatsApp-only
script when another supported channel is available. Confirm email spelling with
minimal disclosure after verification; editing the registered email and sending a
copy to another address may require different permissions.

Check the send operation, ask the customer to confirm receipt, and suggest spam
inspection once if appropriate. A successful send is not proof of receipt. If it
still fails, inspect the delivery result or use an approved alternative rather
than endlessly resending. Do not attribute email delays to weather without evidence.

Do not mark an invoice paid because a link was sent or the customer says they paid.
Use reconciliation or the provider's authorized payment-verification procedure.

## 8. Phone, bot and WhatsApp handoff

Confirm the customer can use the destination channel. Carry the issue summary,
verified account reference and ticket identifier across an authorized handoff so
that the customer need not restart. Do not send the entire conversation when a
minimal summary is enough, or include secrets in handoff notes.

Check that a transfer was accepted or explain the actual queue state. If a bot
loops or closes a conversation prematurely, use the supported human escalation
path. A chatbot's completion status does not establish that the service issue was
resolved. Do not require the customer to send a ceremonial “thank you” solely to
make an agent's software close the chat.

For silence, ask whether the customer can hear you, explain necessary holds and
return with an update under the provider's hold procedure. On an actual dropped
call, use the authorized callback process and existing ticket. Transcript gaps
alone do not prove a dropped call or deliberate disconnection.

## 9. Closing the interaction

Summarize what was done and what remains open. Give the real protocol/reference
and an approved way to follow progress; never invent a number. State the confirmed
owner, next step and any supported update arrangement. Distinguish ending this
conversation from resolving the underlying incident.

Where a repair is claimed, obtain an appropriate service check and customer
confirmation when possible. If the customer is unreachable, use the documented
unreachable status rather than “resolved” without support. Do not promise
cancellation, compensation or a fee waiver without the relevant authority.

Use the [record and review guide](record-and-review.md) for internal notes and
coaching. Deliver a short customer-facing summary, not the internal evidence log.
