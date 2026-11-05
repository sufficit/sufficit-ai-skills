# Extension preferences

Per-extension settings of Sufficit Telephony. The semantics below come from the
product guides; the deployed API is the authority on field names and values.

## Call recording

- Calls handled by a company extension are recorded by default; recording only
  stops when the company itself turns it off **on that extension**.
- The switch lives in the extension details of the panel; through the API,
  discover the extension update operation and the recording field it exposes.
- Recorded: direct inbound calls answered by the extension, queue calls answered
  by it, internal extension-to-extension calls, outbound calls from it, and
  transferred or picked-up calls (also on the receiving end).
- Outbound calls that fall into the carrier voicemail usually count as answered
  and may be recorded (dialing, ring and carrier messages included): the system
  cannot identify carrier voicemail.
- Ring-only, unanswered calls have no conversation to record.

## Changing a preference

1. Read the extension and its current preference values first; report them as
   they are, not as the requester expects them to be.
2. Change one logical preference per call, with company and extension confirmed;
   do not batch unrelated preferences.
3. Re-read the extension and confirm the new value; report the final state.
4. If the API does not expose the preference, say so plainly; do not simulate
   the change or present a panel-only effect as done.
