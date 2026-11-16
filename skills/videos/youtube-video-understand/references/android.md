# Android tablet workflow

Use the current tablet's native Genius tools. Do not probe for or install desktop
Python/ffmpeg before checking `video_transcript` and `video_frame` in `catalog`.
These tools run acquisition and Android media decoding on the tablet; no remote
agent/session or separate computer is required.

1. Call `video_transcript` with the YouTube URL/id and, when known, the original
   language (for the user's example, `language: "pt"`). The tool acquires the whole
   track and saves the complete Markdown/JSON before returning a segment page.
2. Read all segment pages: start with `offset: 0`, follow `next_offset` with the
   same URL/language until `has_more` is false. A paged response is not a truncated
   download. Use the returned Markdown artifact for the full transcript, not a
   summary substituted into a transcript file.
3. Call `video_frame` with the original URL and `timestamp_seconds: 600` for 10:00
   (150 for 02:30). The tool returns the actual decoded image to the model and
   a downloadable PNG artifact. Inspect that image before describing the screen;
   for an action, inspect neighboring timestamps as well.
4. Explain using the full transcript and observed images, including timestamp
   links and the actual intervals inspected. Keep the returned artifact links in
   this tablet conversation. A thumbnail or screenshot of the Genius interface
   does not satisfy a requested video frame.

For example, discover the exact tools then invoke:

```json
{"url":"https://www.youtube.com/watch?v=mRJT_hvYQdM","language":"pt","offset":0,"limit":100}
```

```json
{"url":"https://www.youtube.com/watch?v=mRJT_hvYQdM","timestamp_seconds":600}
```

If captions are absent, `video_transcript` can send the original audio stream to
Genius's existing configured audio-transcription provider, as normal speech
inference. This fallback is explicitly untimed: it does not invent word timestamps.
Set `transcribe_if_missing: false` for captions only. The acquisition, files and
frame decoding remain on the tablet. Automatic captions/recognition may contain
errors and caption availability alone does not prove complete speech coverage.

Frame precision is the closest decoded frame, limited by frame rate and Android's
decoder. The exact returned presentation timestamp is unavailable; do not claim
millisecond accuracy. Native decoding currently selects compatible H.264/MP4 up to
720p and uses HTTP range reads rather than downloading the entire video.

If the exact native tool names are absent, report the missing Genius capability
and required app update. If a tool reports an access/codec/decoder failure, retain
the real error and completed artifacts. Do not claim success from metadata or a
saved file that was never decoded/seen, and do not change machines to hide the
failure. The desktop Python helper remains available when the user actually asks
to work on a desktop.
