---
name: clear-technical-writing
description: "Write and revise documentation, procedures, operational notifications and technical explanations with clear language inspired by ASD-STE100. Use for requests involving STE, simplified technical English, or clearer technical prose; supports adaptation into Portuguese without claiming compliance with the English standard. Do not automatically apply this style to creative writing or any future conversation."
metadata:
  version: "1.1.0"
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

Do not impose arbitrary word count, fixed number of paragraphs or a single response format. Use the structure that facilitates the reader's task.

## Technical Invariants

- Preserve negations, conditions, exceptions, warnings, permissions, sequence and requirements. Do not turn “can” into “must”, recommendation into obligation or a hypothesis into a fact.
- Preserve numbers, units, versions, deadlines, limits and qualifiers as “at most”, “only if” and “at least”.
- Maintain API identifiers, commands, flags, paths, configuration names, URLs, and literal messages. Simplifying the prose does not allow changing code or translating labels that the reader needs to locate on the interface.
- Preserve details necessary for the execution and recovery of failures. Conciseness does not justify removing a safety step or a prerequisite.
- Do not add features, guarantees, test results or operational instructions that are not supported by the material provided.

## Notifications for people

For incident notices, support messages and status updates sent by WhatsApp or email, read [notification writing and channel formatting](references/notifications.md). Lead with the recipient’s task; use a short title, readable sections and blank lines. Keep detailed diagnostic evidence separate from the message body.

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
