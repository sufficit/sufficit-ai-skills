# Extension NAT and video in the telephony extensions skill

Done on 2026-11-19, from the video-call pilot of the Chrome softphone.

- New reference `sufficit-telephony-extensions/references/nat-and-video.md`, linked from
  `SKILL.md` (package 0.8.4): what the CGNAT switch writes on the native PBX, how one-way
  media shows up (RTP sent to the device's private address, video lost first), how to
  confirm it on the node (`pjsip show endpoint`, a short `rtp set debug ip`) and how video
  calls work (relay only, VP8/H.264 on both ends, browser endpoints opt in per extension).
- Product changes it describes: sufficit-standard `c2add48` (the CGNAT switch also writes
  the PJSIP media overrides) and `d70b29e` (`ApplyWebRTCVideo`), sufficit-blazor `14030f8a`
  (VP8/H.264 offered on the extension page), Chrome softphone 2.21.x (video pilot).
- Found on the owner's test extension 6090: CGNAT on in the panel, `rtp_symmetric` off on
  apoint-voip; audio passed, video from the browser never reached the phone.
