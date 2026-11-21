# Extension channel variables in the telephony extensions skill

Done on 2026-11-21.

- New reference `sufficit-telephony-extensions/references/channel-variables.md`, linked from
  `SKILL.md` (package 0.8.6): manager-only extension channel variables (PJSIP `set_var`), the known
  key `pjsip.node_relay_media` (`direct`/`relay` media for calls forwarded between voice servers),
  generic `pjsip.var.NAME` keys with their validation, the read/write/remove API flow and when to
  use `relay`.
- Product changes it describes: sufficit-base `59aac8c` (`EndPointChannelVariables`),
  sufficit-standard `0560b18` (generic variables, one `set_var` per variable), sufficit-endpoints
  `6efdf5d` (`GET /Telephony/EndPoint/Properties`), sufficit-blazor `f2166d66` (screen
  *Variáveis do ramal*, extension "..." menu). API usage: sufficit-endpoints
  `docs/USAGE-EXTENSION-CHANNEL-VARIABLES.md`.
- Validated on google-voip: two generic variables on a test extension reached Asterisk as two
  channel variables; a live call with `relay` kept the media on the registering node.
