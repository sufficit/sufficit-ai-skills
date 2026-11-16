# Research and dependencies

Reviewed on 2026-11-16:

- [dedene/youtube-transcript](https://github.com/dedene/skills/tree/main/skills/youtube-transcript): transcript acquisition via yt-dlp, reusable cached artifacts. Transcript-only scope does not provide visual evidence.
- [video-pipeline-skill](https://github.com/baiyuxi930826/video-pipeline-skill): combines downloading, transcription and sampled frames. The Sufficit package adds an explicit timestamp command and separates generated evidence from actual image inspection.
- [yt-dlp](https://github.com/yt-dlp/yt-dlp): media, subtitle and metadata acquisition. YouTube extraction can require a supported JavaScript runtime and current extractor; authentication/rate restrictions remain possible.
- [faster-whisper](https://github.com/SYSTRAN/faster-whisper): local ASR with timestamped segments and CPU int8 execution. A model must be cached or explicitly downloaded.
- [ffmpeg](https://ffmpeg.org/ffmpeg.html): decoding and accurate output-side seeking. A timestamp between frames resolves to a decoded frame, not an invented exact instant.

These projects are references or separately installed dependencies. No upstream
skill files are copied, and this package's MIT-0 declaration applies to Sufficit's
own files only. A skill orchestrates tools; it cannot give a text-only preset visual
perception or guarantee perfect recognition or comprehension.

The tested ASR dependency set pins faster-whisper 1.2.1 and PyAV below 19.
[Upstream issue 1589](https://github.com/SYSTRAN/faster-whisper/issues/1589)
records the removed `metadata_errors` argument; an unconstrained install failed
in the acceptance test before applying this constraint.
