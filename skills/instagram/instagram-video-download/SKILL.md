---
name: instagram-video-download
description: Download Instagram Reels and videos from user-supplied Instagram post URLs to local files with yt-dlp and verify their media streams. Use for saving Instagram videos; does not perform transcription, editing or publishing.
metadata:
  version: "1.0.0"
  author: "Sufficit"
  source: "https://github.com/sufficit/sufficit-ai-skills"
---

# Instagram video download

Save the requested Instagram video locally and return its verified file path. Use a local
shell directly; an active editor terminal or terminal ID is unnecessary.

## Choose the tool and destination

Check available executables with `command -v`: `yt-dlp`, `uvx`, `python3`,
`ffmpeg`, and `ffprobe`. A missing `python` command does not mean `python3` is
missing. Prefer an installed `yt-dlp`; otherwise use
`uvx --from yt-dlp yt-dlp`, which worked for the Instagram Reel below without a
global install. If neither is available, use an isolated Python virtual environment
and install `yt-dlp` there if dependency installation is permitted. Do not modify
system Python or unrelated projects to obtain the downloader.

Use the user's destination when specified. Otherwise use `downloads/` under the
current workspace. Create the directory and use an ID-based filename. Keep the
`%(ext)s` template: the final container is determined by the selected streams.
Quote paths and URLs as shell arguments; do not use `eval` or interpolate raw
user text into shell code.

For Instagram, retain the `/reel/<id>/` or `/p/<id>/` URL and omit share-tracking
parameters when unneeded. Keep parameters required for access.

## Download

A page-fetch or search failure does not establish that the video is unavailable.
Try yt-dlp's extractor before scraping HTML, searching for mirrors, or asking the
user to upload the file. Ordinary Instagram HTML may contain no direct media URL.

Example using the successful session's Reel (replace URL and destination with the
current request):

```bash
mkdir -p downloads
uvx --from yt-dlp yt-dlp \
  --ignore-config --no-playlist --no-overwrites \
  --socket-timeout 25 --retries 1 --fragment-retries 1 \
  --print 'after_move:filepath' \
  -o 'downloads/instagram-DekknYUiuIX.%(ext)s' \
  -- 'https://www.instagram.com/reel/DekknYUiuIX/'
```

For an installed executable, replace the `uvx --from yt-dlp yt-dlp` prefix with
`yt-dlp`. For other Instagram posts, use `instagram-%(id)s.%(ext)s` in the output
template. These options limit the request to the linked item and preserve existing
files. Check an existing file before treating a skipped download as success.

Allow yt-dlp to select video and audio and let `ffmpeg` merge separate streams.
Wait for merging to finish; intermediate `.f...mp4`, `.m4a`, and `.part` files are
not the final artifact. Do not force an `.mp4` filename or transcode solely to
match an extension. If `ffmpeg` is missing and a merge is required, obtain it using
the environment's normal dependency procedure or select a combined format with
`-f b` when one exists, explaining the possible quality reduction.

If the command returns a running process/session ID, poll that process until it
exits. Classify failures before another attempt: stop on manual cancellation;
retry transient network failures only within a bounded attempt count. For
unsupported extractors, inspect the installed version and current official
instructions before trying an update. For login, private-media, or access errors,
report the concrete blocker. Use credentials only through a user-authorized
mechanism; do not harvest browser cookies or bypass access restrictions.

## Verify and report

Use the final path emitted after post-processing, then inspect it:

```bash
ffprobe -v error \
  -show_entries format=duration,size \
  -show_entries stream=codec_type \
  -of json 'downloads/instagram-DekknYUiuIX.mp4'
```

Confirm a nonempty file, a plausible duration, and a video stream. Check whether
an audio stream exists before reporting that audio was saved; some sources are
silent. If `ffprobe` is unavailable, use an available media inspector or state
that stream verification remains incomplete. Report the clickable local path,
duration and size only from observed results. Saving media does not itself
transcribe, summarize or publish it; follow the user's requested scope. To turn
the saved video into text, use the
[video-transcribe](../../videos/video-transcribe/SKILL.md) skill.

See the [official yt-dlp options](https://github.com/yt-dlp/yt-dlp#usage-and-options)
for extractor behavior and supported flags.
