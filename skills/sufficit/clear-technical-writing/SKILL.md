---
name: clear-technical-writing
description: "Write and revise documentation, procedures, support chat replies, operational notifications and technical explanations with clear language inspired by ASD-STE100. Use for requests involving STE, simplified technical English, or clearer technical prose; supports adaptation into Portuguese without claiming compliance with the English standard. Use for ongoing support conversations when explicitly assigned to the agent; do not impose this style on creative writing."
metadata:
  version: "1.2.3"
  author: "Sufficit"
---

# Clear technical writing

Produce instructions that are easy to follow and understand, preserving technical meaning. This skill contains original Sufficit guidelines inspired by STE; it is not the official standard, an authorized translation or a compliance checker.

## Choose a mode

- Clear writing (default): Simplify the text in the requested language. In Portuguese, apply the principles of clarity as editorial adaptation. Do not translate into English just because the user mentioned STE.
- Standards-based review: When the user requires compliance with ASD-STE100, see the applicable edition of the official rules and dictionary. Read [sources and limits](references/sources.md). Record the edition and which checks were performed. If the source is not accessible, provide the clarity review you can complete and state that compliance remains unverified. Do not invent rule numbers, limits, or claims that words are approved.

## How to write and review

1. Identify the reader, the purpose, and what needs to remain accurate. Use the available context; ask only when ambiguity changes the meaning.
2. Organize the content in the order of use. In procedures, put the condition before the action that depends on it. Use numbered steps when there is real sequence.
3. Prefer direct verbs and identifiable subjects. Separate independent actions without breaking conditions, dependencies or the necessary order.
4. Keep a consistent term for each concept. In English, STE uses a controlled vocabulary; in editorial mode, consistency does not mean that the word was checked in the official dictionary. Preserve necessary technical names.
5. Replace vague pronouns with the correct component or responsible party. Do not guess what an ambiguous pronoun refers to; identify the ambiguity or ask for context.
6. Compare the result with the original to detect loss of requirements, change of obligation or certainty and changes in the described behavior.

Use the structure that facilitates the reader's task. Apply the channel-specific length rule below to chat messages; do not impose it on documentation or email.

## Technical Invariants

- Preserve negations, conditions, exceptions, warnings, permissions, sequence and requirements. Do not turn “can” into “must”, recommendation into obligation or a hypothesis into a fact.
- Preserve numbers, units, versions, deadlines, limits and qualifiers as “at most”, “only if” and “at least”.
- Maintain API identifiers, commands, flags, paths, configuration names, URLs, and literal messages. Simplifying the prose does not allow changing code or translating labels that the reader needs to locate on the interface.
- Preserve details necessary for the execution and recovery of failures. Conciseness does not justify removing a safety step or a prerequisite.
- Do not add features, guarantees, test results or operational instructions that are not supported by the material provided.

## Evidence and chronology in support conclusions

- Before saying "before", "after", "since", "still" or "resolved", compare the actual event timestamps against the referenced report, deployment or test. Normalize dates and time zones first; keep the query time separate from the event time. Do not infer chronology from row order, a shared day or a recent query.
- When the distinction matters, make the comparison explicit: an event at 10:19 precedes a report at 10:28 on the same date and time zone; it cannot establish behavior after that report. If an event lacks a date or offset that changes the ordering, preserve that uncertainty.
- A successful event before a reported failure does not disprove the later symptom or show recovery. Evidence from another number, endpoint or interval does not validate the affected path. State what the observed interval supports and what remains untested.
- Before finalizing, audit each temporal or causal claim against its cited observations. Delete or qualify conclusions that outrun the evidence. Different registration IPs do not by themselves establish different physical devices, and SIP registration does not prove call delivery.

## Readable support chat replies

Apply these rules when drafting or sending messages in WhatsApp and other chat apps:

- By default, use **at most two short text lines and about 30 words total per message**. Longer messages are appropriate only when the user explicitly requests a technical assessment (parecer técnico) or a more detailed explanation (resposta mais explicada). Multiple findings or an internal diagnosis do not by themselves create that exception.
- Lead with the current answer or verified conclusion, then include only the next useful action or question. Preserve uncertainty and the essential identifier; keep detailed logs and secondary findings out of the ordinary chat reply.
- Do not split a long answer into several messages to evade the limit, or compress a report into two oversized lines. Line wrapping depends on the app and screen; keep the text short as well as limiting deliberate line breaks.
- When a technical assessment or a more detailed explanation is explicitly requested, separate findings, evidence limits and necessary next actions with short paragraphs or simple bullets. Keep identifiers, dates and confidence attached to the findings they qualify; registration success is not proof that calls work.
- In WhatsApp, use single-asterisk emphasis sparingly and real newlines; avoid tables, HTML and Markdown # headings. Serialize newlines correctly in JSON, without visible backslash-n sequences. Other chat apps use their supported formatting. Do not repeat a signature supplied by the channel.
- Before sending, check the exact text for the two-line/about-30-word default, or verify that a technical assessment or a more detailed explanation was explicitly requested. Do not append a generic offer or question that does not advance the current request. This writing skill does not authorize an external send or resend.

Example (fictional ordinary chat reply, not a live diagnostic):

```text
Identificamos quedas após o atendimento no ramal 1002; a causa ainda precisa de confirmação.
Qual equipamento está usando nesse ramal? Precisamos acompanhar uma chamada com falha.
```

## Notifications for people

For incident notices, support messages and status updates sent by WhatsApp or email, read [notification writing and channel formatting](references/notifications.md). Lead with the recipient’s task and keep detailed diagnostic evidence separate. For chat, retain the two-line/about-30-word default unless a technical assessment or a more detailed explanation was explicitly requested; use longer sections when appropriate for email or the requested detail.

## Delivery

Deliver directly the text drafted or revised. Add observations only for unresolved ambiguities, material changes or relevant revision limits. Do not attach an explanation about STE to each response.

When asked for a diagnosis, show problematic excerpts, the proposal and the concrete reason. When compliance is requested, distinguish verified items from pending checks; do not treat the execution of this skill as certification.

## Editorial examples (not evidence of compliance)

Before: “If the service is unavailable, a new attempt must be made after a 30-second interval.”

After: “If the service is unavailable, try again after 30 seconds.”

Before: “You can run `worker --dry-run` to simulate the operation, provided the `enabled` configuration is `true`.”

After: “If `enabled` is `true`, you can run `worker --dry-run` to simulate the operation.”

Ambiguous: “Restart the server after disconnecting the client and updating it.”

Do not choose which component to update without evidence. Ask the author to identify whether “it” refers to the client or the server.
