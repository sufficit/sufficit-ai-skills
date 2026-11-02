# Instagram caption, audit and profile score

Reviewed `Jakeschincariol/instagram-agent-skill` at `d03c56b` and adopted what our Instagram skills lacked. Added `instagram-caption` (adapted Portuguese and English linter) and `instagram-audit` (per-post ranking against the account's own median, with blank metrics kept unknown), both MIT with upstream attribution. `instagram-profile-setup` 1.2.0 gained a 100-point business rubric with an `unknown` state for items a logged-out read cannot see.

Not adopted: the hook scorer and humanizer lexicon, which are calibrated for English and misranked Portuguese samples, and the AI-detection score. Platform limits were checked on 2026-11-02: the five-hashtag cap has several secondary sources; the 125-character cut has no first-party source and stays configurable.

Validation: `scripts/validate.py`, `scripts/build_skill_index.py --check`, `scripts/markdown_coverage.py` and `tests/` passed before push.
