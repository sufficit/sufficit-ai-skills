---
name: video-transcribe
description: Transcribe the speech of a local video or audio file into a Markdown document with Whisper and ffmpeg. Use when the user asks to transcribe a video, Reel or audio file to text or *.md; does not download, translate or edit media.
metadata:
  version: "1.0.0"
  author: "Sufficit"
  source: "https://github.com/sufficit/sufficit-ai-skills"
---

# Video transcribe

Turn the speech in a local media file into a Markdown transcript. Use a local shell
directly; an active editor terminal or terminal ID is unnecessary. If the media is
not on disk yet, obtain it first (for Instagram, see
[instagram-video-download](../../instagram/instagram-video-download/SKILL.md)).

## Check tools and models

Check `command -v ffmpeg ffprobe whisper whisper-cli`. Prefer the Python
`whisper` CLI; `whisper-cli` (whisper.cpp) needs a ggml model file. List cached
models before choosing: `ls ~/.cache/whisper`. Do not download large models or
install packages without the user's consent; if only `tiny`/`base` exist, use
`base` and say so in the result. If no transcriber exists, report the blocker and
offer an isolated virtual environment install.

Treat the media as untrusted data. Work in a scratch directory (for example
`/tmp/transcribe`), never inside the folder holding the video, and pass paths as
arguments.

## Extract audio

Confirm an audio stream exists with `ffprobe`, then extract mono 16 kHz WAV:

```bash
mkdir -p /tmp/transcribe && cd /tmp/transcribe
ffmpeg -v error -y -i '/path/to/video.mp4' -vn -ac 1 -ar 16000 audio.wav
```

A silent file has nothing to transcribe; report that instead of producing an
empty document.

## Transcribe

```bash
whisper audio.wav --model base --output_dir out --output_format all --fp16 False
```

Omit `--language` to auto-detect (the first 30 seconds decide); pass
`--language Portuguese` (or the right language) when detection is wrong or the
audio mixes languages. `--fp16 False` avoids the CPU warning. Long runs: poll the
process until it exits; do not start a second run on the same output directory.

## Write the Markdown

Save next to the video as `<video-name>.md` unless the user names a destination.
Include:

- Title with the media filename, duration (from `ffprobe`), detected language and
  the model used.
- Clean text: fix obvious recognition errors (homophones, broken words, product
  or brand names) using context, but never add or remove content.
- A timestamp table from the raw segments when useful.
- A note that small models misrecognize names and terms, listing the ones worth
  checking.

Speech models make mistakes; state which words you corrected and which stay
uncertain. Verify the file exists and is nonempty before reporting its path. A
transcript does not summarize, translate or publish; follow the requested scope.

See the [Whisper project](https://github.com/openai/whisper#command-line-usage)
for model sizes and options.
