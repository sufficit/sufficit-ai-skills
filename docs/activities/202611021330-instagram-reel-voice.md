# Instagram Reel and brand voice

Second round of the `Jakeschincariol/instagram-agent-skill` review (`d03c56b`). Added `instagram-reel` with hook shapes and a reject checklist, script shape, on-screen rules, a per-brand voice template and `scripts/beat_sheet.py`, an MIT adaptation with Portuguese support. Linked it from `instagram-caption` 1.0.1 and `instagram-profile-setup` 1.2.1.

Not adopted: numeric hook scoring and `hooks.json`, which misrank Portuguese. Sources checked 2026-11-02 did not give a first-party safe zone, a settled Reel limit or a published Brazilian Portuguese speaking rate, so the skill labels those figures as assumptions and asks for a preview, a check in the app and a timed `--wpm`.
