# Video understanding skill

Objective: give Genius agents a reusable skill to obtain full timestamped transcripts and inspect any requested video timestamp, including https://www.youtube.com/watch?v=mRJT_hvYQdM.

1. COMPLETED — Inspect existing media skills, catalog contract and GitHub references; select integration and dependencies.
2. COMPLETED — Implement the skill and reusable transcript/frame helpers; register package provenance and discovery.
3. COMPLETED — Run behavioral tests with generated media and attempt the supplied YouTube video; record exact limitations.
4. IN PROGRESS — Validate catalog, convert this plan to an activity, commit and push own changes to main; verify Genius catalog synchronization.

Constraints: preserve parallel changes; English package instructions; no channel publishing; no claim of full understanding from captions alone. Native plan panel unavailable: this file is the execution state.

Validation: Python behavioral tests, real ffmpeg extraction, package/catalog validators, markdown coverage, live YouTube acquisition attempt and remote Git state.

Evidence: full Portuguese automatic caption track fetched (401 segments, video duration 1069 seconds); video downloaded and frames extracted/opened at 150 and 600 seconds. At 150s Unity shows the player on the initial flat scene; at 600s it shows a forest terrain and Global Volume/Color Adjustments. These are sampled observations, not a whole-video visual review.

Validation isolation: canonical tree has an unrelated clear-technical-writing edit with stale digest; validation uses an origin/main worktree plus only this task, preserving the remote customer-equipment-access addition. All 195 packages, catalog versions, markdown coverage and 65 tests passed.

ASR smoke: cached base model transcribed the first 15 seconds successfully after pinning av<19; an unconstrained faster-whisper 1.2.1/PyAV 19.0.2 install failed with metadata_errors. Full-media ASR acceptance passed: 221 timestamped segments across 1068.868 seconds; final segment ends at 1063.9 seconds. No model download or cloud ASR was used.
