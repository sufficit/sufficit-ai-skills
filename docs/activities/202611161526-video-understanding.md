# Video understanding skill — delivered

Objective: give Genius agents a reusable skill to obtain full timestamped transcripts and inspect any requested video timestamp, including https://www.youtube.com/watch?v=mRJT_hvYQdM.

1. COMPLETED — Inspect existing media skills, catalog contract and GitHub references; select integration and dependencies.
2. COMPLETED — Implement the skill and reusable transcript/frame helpers; register package provenance and discovery.
3. COMPLETED — Run behavioral tests with generated media and attempt the supplied YouTube video; record exact limitations.
4. COMPLETED — Validate catalog, convert this plan to an activity, commit and push own changes to main; verify Genius catalog synchronization.

Constraints: preserve parallel changes; English package instructions; no channel publishing; no claim of full understanding from captions alone. Native plan panel unavailable: this file is the execution state.

Validation: Python behavioral tests, real ffmpeg extraction, package/catalog validators, markdown coverage, live YouTube acquisition attempt and remote Git state.

Evidence: full Portuguese automatic caption track fetched (401 segments, video duration 1069 seconds); video downloaded and frames extracted/opened at 150 and 600 seconds. At 150s Unity shows the player on the initial flat scene; at 600s it shows a forest terrain and Global Volume/Color Adjustments. These are sampled observations, not a whole-video visual review.

Validation isolation: canonical tree has an unrelated clear-technical-writing edit with stale digest; validation uses an origin/main worktree plus only this task, preserving the remote customer-equipment-access addition. All 195 packages, catalog versions, markdown coverage and 65 tests passed.

ASR smoke: cached base model transcribed the first 15 seconds successfully after pinning av<19; an unconstrained faster-whisper 1.2.1/PyAV 19.0.2 install failed with metadata_errors. Full-media ASR acceptance passed: 221 timestamped segments across 1068.868 seconds; final segment ends at 1063.9 seconds. No model download or cloud ASR was used.

Delivery checkpoint: implementation commit 5ee2f29311cfe9d7921c40bdac0685f5f18686b0 pushed to main. Remote validation and notify-genius both passed: https://github.com/sufficit/sufficit-ai-skills/actions/runs/43927712681 . Automatic Genius sync was deferred by the documented PR validation window: https://github.com/sufficit/sufficit-ai-genius/actions/runs/43927812998 . Manual synchronization used the documented immediate path after remote CI passed.

Tested dependencies: yt-dlp 2026.10.26; faster-whisper 1.2.1; PyAV 18.1.0. Temporary evidence is in /tmp/sufficit-video-mRJT_hvYQdM (captions, ASR transcript, downloaded media, inspected frames). Whisper base can misrecognize words; no claim of perfect verbatim accuracy or exhaustive visual comprehension. Actual agent/session installation and image perception depend on that session's tools and preset; catalog availability is not installation.


Publication verified: https://github.com/sufficit/sufficit-ai-genius/actions/runs/43928076343 completed successfully. Genius pin commit: https://github.com/sufficit/sufficit-ai-genius/commit/4d3b01e6815e8bec3391609d08846b3167af00be . The public catalog at https://storage.googleapis.com/suff-public/sufficit-ai-genius/skills/v2/catalog.json contains video-understand 1.0.0, source pinned to 5ee2f29311cfe9d7921c40bdac0685f5f18686b0. The immutable source manifest's SHA-256 matches the local package. The public runtime catalog itself omits digests by design.

All four checkpoints are complete. The completed plan was converted to this activity and the README link updated. The helper does not call an LLM: agents must actually open extracted frames with an image-capable tool/preset and combine visual evidence with speech. Research references are retained inside the package; all code is original Sufficit, MIT-0. No binary release or agent/session installation is claimed.

Validation commands: `python3 -B -m unittest discover -s tests -v` (65 passed), `python3 -B scripts/validate.py` (195 packages), `python3 -B scripts/build_skill_index.py --check`, `python3 -B scripts/catalog_versions.py --check`, `python3 -B scripts/markdown_coverage.py`, and the skill-creator `quick_validate.py` all passed. Real video commands exercised `fetch`, `frame --at 02:30`, `frame --at 10:00` and full-media `transcribe --model base --language pt`. A test first exposed the erroneous merging of identical cues that merely touch at a boundary; the corrected helper retains consecutive repeated speech while consolidating identical overlapping cues.
