# Changelog

Newest first. **required** marks updates to apply before the next voice operation.

## 1.1.0 — 2026-11-12

- New: HTTP tools so agents can call your own systems (ERP, CRM; IXC example) through
  `contexts/{contextId}/http-tools` and `agents/{agentId}/http-tools`. See `references/http-tools.md`.
- Voice agents receive tool changes on `voice/publish`.

## 1.0.0 — 2026-11-12

- First release: build, publish, test and operate voice agents through the Fleet API (`voice/provider`,
  `voice/setup`, `voice`, `voice/provision`, `voice/publish`, `voice/calls`, `voice/proposals`).
- Update check against `release.json` and folder replacement procedure.
