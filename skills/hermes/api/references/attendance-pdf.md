# Open an attendance and send the requested PDF

A request such as "abra um atendimento no grupo do cliente e envie o boleto em PDF
com este texto" authorizes creating the attendance and sending that text/document.
Resolve internal IDs yourself. Ask only about a material ambiguity that account,
contact bindings and history cannot resolve.

1. Authenticate, identify the account, then search the contact by the supplied name.
   A requested WhatsApp **group** must resolve to that group, not an individual's
   similarly named contact. Read the group's context/custom attributes and channel
   identity. Keep Sufficit customer GUID, Hermes contact ID, conversation ID and
   channel source ID distinct.
2. Read this contact's conversations and inbox bindings. An account-wide page is
   not evidence that the contact has no attendance. Resolve the intended inbox
   from its bindings and channel. For the conversation creation API, discover the
   body in live OpenAPI; when `source_id` is required, obtain the real contact/inbox
   binding rather than guessing from a phone number or reusing `contact_id`.
3. Create the requested attendance using the plugin or authenticated API fallback.
   Check the returned conversation belongs to the intended contact/inbox. If inbox
   policy reuses an existing conversation, report that actual result. Do not change
   assignee, team or status beyond what the request requires.
4. Obtain the existing boleto's document URL from the issuing API. Resolve relative
   URLs against that API's configured base; download the document, not an HTML
   preview. Check status, content type and PDF bytes (`%PDF-`). If it is HTML,
   inspect the documented document/download flow instead of renaming it `.pdf`.
   Never issue a second boleto merely to obtain its PDF.
5. Send the supplied text and PDF to the verified conversation. Inspect the plugin
   schema for file support. A text-only `hermes_messages_send` does not prove the
   Hermes API cannot attach files; use [the fallback](connected-execution.md).
   The Hermes message builder supports multipart `attachments[]` containing the
   file, along with `content`, `message_type=outgoing`, `private=false`. Use a
   multipart-aware client that creates the boundary. This is a compatibility
   detail verified in Hermes's `Messages::MessageBuilder#process_attachments`;
   the public Swagger inspected on 2026-11-05 documents the message route but
   omits this field. Recheck the current contract/source when behavior differs.
   Pass the actual PDF bytes and filename, not its local path as message text.
   Do not substitute a URL or a direct QuePasa send for the requested Hermes PDF
   attachment without resolving the requested outcome with the user.
6. Read the conversation's messages again. Verify message ID, outgoing/public
   flags, text and attachment metadata on the correct conversation. Distinguish
   accepted/queued, sent, delivered and failed according to provider evidence.
   An HTTP success is not proof of WhatsApp delivery. Report any pending delivery
   or failure plainly; inspect history before retrying an uncertain send.

Report issuance, attendance and PDF send separately, including a useful attendance
link when returned. A ready boleto alone does not complete this combined request.
