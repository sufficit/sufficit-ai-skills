# QuePasa API diagnostics guidance

Updated [quepasa-api](../../skills/quepasa/api/SKILL.md) from 0.1.5 to 0.1.6. The installed copy matched the previous canonical release, so the guidance was corrected in the source package and synchronized to the local Codex installation.

A read-only check returned `401 missing user id` on session lookup and `503 owner_unknown` with `X-QuePasa-Forward-Error` on a test-gateway group lookup. The latter matched the gateway forwarding logic. The update distinguishes service health from per-session health, authentication from session routing, and an accepted Fleet turn from an accepted WhatsApp send. It requires the gateway receipt before reporting accepted delivery and reconciliation before retrying an uncertain send.

The release metadata and catalog digest were refreshed. The package and installed copy passed the skill schema check and matched file for file. The first repository test run found the temporary plan unlinked. The plan was replaced with this activity under the repository’s history convention before final validation.

No live send, pairing, deployment or gateway state change was part of this skill update.

Final validation passed for all 195 packages, the generated index, catalog versions, Markdown coverage and all 70 repository tests.
