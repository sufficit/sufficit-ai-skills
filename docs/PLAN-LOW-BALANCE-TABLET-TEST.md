# Low-balance tablet acceptance test

Scope: session 01a1acef-9b0e-7333-a48f-3c0f3e6b75b1. Test the low-balance workflow on the connected tablet for customer Sufficit and the owner's personal WhatsApp. Use a fresh layperson request with misspellings, without supplying a threshold, channel or implementation guidance initially.

1. Completed — inspect tablet UI and available test controls; identify current app and avoid existing conversations.
2. Completed — latest blind run on 0.164.0-dev.13 (2aa61195) read the low-balance reference and live request schemas. It found three similar corporate records and asked a valid identity question. The recorded selection was acknowledged, but subsequent calls used a different GUID and the agent ended asking for the threshold. Automatic refresh is verified; service acceptance remains failed.
3. Completed — redacted test record in docs/activities/20261105-low-balance-tablet-acceptance.md; validation passed for 185 packages; delivery commit includes this checkpoint. No alert write or delivery verified.
4. Blocked acceptance — selected customer identity and threshold policy are not reliably followed in the live default-preset run; personal WhatsApp gateway credential is rejected. Preserve these failures for the next implementation decision; do not claim the customer setup complete.

Do not edit the conversation database or seed the expected answer. Do not select another customer or message unrelated recipients. Preserve existing alerts. Store sensitive raw evidence outside the public repository; publish only redacted observations.

5. In progress — harden customer/contact lookup after the event-test run asked for internal GUIDs without querying by supplied name/number; validate and publish the skill, then retry the still-unsent official test. The unrelated native crash and original setup acceptance remain open.
