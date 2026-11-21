# Extension channel variables (managers only)

Variables the voice servers attach to every channel of one extension (Asterisk PJSIP
`set_var`). Only users with the `manager` role can read or change them; a customer user gets
403. If the caller is not a manager, explain the effect and route the request to Sufficit
support instead of attempting the call.

## Keys

| Key | Values | Use |
| --- | --- | --- |
| `pjsip.node_relay_media` | `direct`, `relay` | Media of calls forwarded between voice servers to this extension. Default (no property) is the server setting, currently `direct`. Set `relay` when forwarded calls are answered but silent or one-way. |
| `pjsip.var.<NAME>` | 1-256 chars without `&`, `%`, line breaks | Generic variable `NAME=value`. `NAME` matches `[A-Za-z_][A-Za-z0-9_]{0,63}`; `SUFFICIT_NODE_RELAY_MEDIA` is reserved (use `pjsip.node_relay_media`). |

Typical reasons for `relay`: a customer firewall that allows only one voice server, a router
with SIP ALG, a device that ignores the re-INVITE that moves the media, a restrictive NAT or
carrier CGNAT. Check the extension's CGNAT switch first
([nat-and-video.md](nat-and-video.md)). Public explanation for customers:
<https://wiki.sufficit.com.br/Sufficit/Telephony/servidores-voz.html#áudio-das-chamadas-encaminhadas>.

## Flow

1. Confirm the company (context GUID) and the extension (endpoint GUID), as for any
   customer-bound write.
2. Read the current values:
   `GET /Telephony/EndPoint/Properties?contextid=<context>&endpointid=<extension>&prefix=pjsip.`
3. Write one key: `POST /Telephony/EndPoint/Property` with
   `{ "contextid", "endpointid", "key", "value" }`. A missing or null `value` removes the key.
   Invalid names or values are rejected by the server; do not retry with variations.
4. Read again and report the stored value. Changes apply to the next calls; calls in progress
   do not change and nothing needs to be restarted.

Routes and payloads follow the current API contract; confirm them in the deployed API before
relying on this summary. Managers can also use the screen *Variáveis do ramal* (extension page,
"..." menu).

## Scope

- Extension values only through this flow. A value for every extension of a company uses an
  empty endpoint GUID; do it only when the request explicitly says so.
- Browser softphone endpoints never receive these variables.
- Do not use generic variables to change call routing or billing; they only label channels for
  the dialplan of the voice servers.
