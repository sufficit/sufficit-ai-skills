# Changelog

Newest first. **required** marks updates to apply before the next voice operation.

## 1.7.0 — 2026-11-14

- **required**: two-way support threads at `endpoints.sufficit.com.br/Support/Threads`, same Fleet token. Check
  threads waiting for you each session; report issues and improvements there instead of e-mail.

## 1.6.0 — 2026-11-13

- Voice-only agents (no executor): persona kept by Fleet (`source: "fleet"`, first revision `"initial"`); no task or
  memory tools on the phone. Previously the persona of such agents could not be saved.

## 1.5.0 — 2026-11-13

- Training by panel whisper: per-agent `whisperApproval` (`manual` default, `auto`).

## 1.4.0 — 2026-11-13

- New `references/prompting.md`: how to write persona and instructions for the phone (structure, each rule once,
  goal first, trust on calls, tools that match the prompt, provider standards, skeleton). Never edit the prompt in
  the ElevenLabs dashboard; fix it in Fleet and publish.

## 1.3.1 — 2026-11-13

- `voice/provider` no longer takes `language`: every agent speaks Portuguese (Brazil) with the São Paulo timezone, and
  its provider name is the agent Id.

## 1.3.0 — 2026-11-13

- A request to put an agent in a queue means overflow (queue exit destination) by default; confirm with the user and
  explain that a queue member takes one call at a time.

## 1.2.0 — 2026-11-13

- The extension number is optional; the agent Id always identifies its virtual extension.
- New `publicAccess` on the voice binding (`none`, `read` default, `full`) for callers from queues, DIDs and IVR.

## 1.1.0 — 2026-11-12

- New: HTTP tools so agents can call your own systems (ERP, CRM; IXC example) through
  `contexts/{contextId}/http-tools` and `agents/{agentId}/http-tools`. See `references/http-tools.md`.
- Voice agents receive tool changes on `voice/publish`.

## 1.0.0 — 2026-11-12

- First release: build, publish, test and operate voice agents through the Fleet API (`voice/provider`,
  `voice/setup`, `voice`, `voice/provision`, `voice/publish`, `voice/calls`, `voice/proposals`).
- Update check against `release.json` and folder replacement procedure.
