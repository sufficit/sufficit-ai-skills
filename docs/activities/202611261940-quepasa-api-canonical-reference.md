# QuePasa API skill aligned with the reference QuePasa publishes

Updated [quepasa-api](../../skills/quepasa/api/SKILL.md) from 0.1.6 to 0.2.0.

## Why

Two Genius issues stalled for hours because no published description of the QuePasa API had the facts an integrating agent needed: the shape of `GET /api/v5/groups`, that `GET /api/v5/chats` leaves groups out by design, and how to read and set the options of a session. QuePasa now generates a skill of its own API and publishes it with each version ([nocodeleaks/quepasa-#88](https://github.com/nocodeleaks/quepasa-/issues/88)). The copy in this repository did not have that content.

## What changed

- `skills/quepasa/api/references/api/`: the twelve family references QuePasa generates, copied unchanged for version `5.26.1125.1212` (160 operations, with request fields and response schemas). They are credited in [THIRD_PARTY_NOTICES.md](../../THIRD_PARTY_NOTICES.md); the license is MIT No Attribution.
- `SKILL.md`: a section that lists those references and points at the published one for other versions; a section on conversations and groups, which states that `/chats` lists direct chats only and gives the shape of `/groups`; a section on the options of a session, with the three states, the lowercase keys of the patch and the number `0` that returns an option to inherited; the rules for creating a group (25 UTF-8 bytes, at least one participant, the meaning of `Participants[].Error`); two new entries among the traps.
- `references/endpoints.md`: the rows for chats, groups and sessions corrected, and a pointer to the complete reference.
- The release metadata, the skill card and the catalog digest were refreshed.

## Verified

- Each fact added to `SKILL.md` was checked against the published reference and against the QuePasa source at the revision the gateway runs.
- The option route is `POST /api/v5/session/option`, with the option name in the query, the body or the `X-QUEPASA-OPTION` header. It is not a path segment. An earlier note of mine in the Genius repository wrote it with one; that is being corrected there.

No live request was made, and no gateway state changed.
