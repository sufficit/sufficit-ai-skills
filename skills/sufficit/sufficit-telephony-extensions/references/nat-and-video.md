# NAT and video on extensions

How an extension behaves on the native PBX (Asterisk 18 with PJSIP realtime served by
sufficit-asterisk-api) when the device is behind NAT or the call carries video. Confirm
values on the deployed PBX; this note explains what to look for.

## CGNAT switch

- The extension page in the panel has a **CGNAT** switch. Through the API it is the
  endpoint property `cgnat` (`true`/`false`).
- Turning it on writes the PJSIP media overrides the native PBX reads:
  `pjsip.rtp_symmetric=yes`, `pjsip.force_rport=yes`, `pjsip.rewrite_contact=yes`,
  `pjsip.direct_media=no`, `pjsip.rtp_keepalive=15`. Turning it off removes them.
  It also keeps writing the legacy FreePBX settings while FreePBX exists.
- Before sufficit-standard `c2add48` (2026-11-19) the switch only wrote the FreePBX
  table: an extension with CGNAT "on" could still have `rtp_symmetric` off on the
  native PBX. Re-save the switch on such extensions.

## Symptom: one-way media, video worst

- With `rtp_symmetric` off, Asterisk sends RTP to the address in the device's SDP,
  usually its private LAN address. Small audio packets may still arrive through some
  internal route, so the call "works", while video (large packets) never arrives.
- Read the endpoint on the PBX node that serves the device:
  `pjsip show endpoint <endpoint id>` → `rtp_symmetric`, `direct_media`.
- During a call, `rtp set debug ip <device public IP>` for a few seconds shows where
  Asterisk sends; a private address (192.168.x, 10.x) as destination is this problem.
  Turn the debug off right after.
- Fix: turn CGNAT on for that extension and place a new call (a running call keeps
  its media setup).

## Video calls

- The PBX only relays video, it never converts it: both ends need one codec in
  common. Allow `vp8` and/or `h264` in the extension's codecs (panel or
  PUT `/Telephony/EndPoint/Update` with the full allowed list).
- SIP devices (Sufficit Phone, Linphone, Zoiper) negotiate video once a video codec
  is allowed.
- Browser endpoints (`wss-<endpoint id>`, the Chrome softphone) stay audio only unless
  the extension explicitly allows VP8 or H.264; the default codec list never turns
  video on for them (sufficit-standard `ApplyWebRTCVideo`). As of 2026-11-19 this is
  deployed on apoint-voip only; the Chrome softphone (2.21 pilot) reaches it through
  Settings › Diagnostics › Voice server.
- A computer without a camera still receives the other side's video in the Chrome
  softphone; it just sends none.
