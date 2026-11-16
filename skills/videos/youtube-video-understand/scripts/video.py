#!/usr/bin/env python3
"""Fetch timestamped evidence and inspect precise video positions. No LLM calls."""
import argparse
import html
import json
import math
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import urlparse


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def run(args):
    return subprocess.check_output(args, text=True, stderr=subprocess.PIPE)


def seconds(value):
    parts = str(value).split(':')
    if len(parts) > 3:
        raise ValueError('Use seconds, MM:SS or HH:MM:SS')
    result = 0.0
    for part in parts:
        number = float(part)
        if number < 0 or not math.isfinite(number):
            raise ValueError('Timestamp must be finite and nonnegative')
        result = result * 60 + number
    return result


def stamp(value):
    millis = round(value * 1000)
    secs, ms = divmod(millis, 1000)
    mins, sec = divmod(secs, 60)
    hour, minute = divmod(mins, 60)
    return f'{hour:02}:{minute:02}:{sec:02}.{ms:03}'


def probe(path):
    return json.loads(run(['ffprobe', '-v', 'error', '-show_format', '-show_streams',
                           '-of', 'json', str(path)]))


def captions(data):
    """Keep timed JSON3 events; collapse only identical adjacent rolling cues."""
    result = []
    for event in data.get('events', []):
        text = html.unescape(''.join(s.get('utf8', '') for s in event.get('segs', [])))
        text = re.sub(r'\s+', ' ', text).strip()
        if not text:
            continue
        start = event['tStartMs'] / 1000
        end = start + event.get('dDurationMs', 0) / 1000
        if result and result[-1]['text'] == text and start < result[-1]['end']:
            result[-1]['end'] = max(end, result[-1]['end'])
        else:
            result.append(dict(start=start, end=end, text=text))
    return result


def transcript(out, segments, source, language, method, duration):
    if not segments:
        raise ValueError('No speech/caption segments obtained; transcript not produced')
    save(out / 'transcript.json', dict(source=source, language=language, method=method,
                                     duration=duration, segments=segments))
    lines = [f'# Transcript\n\nSource: {source}\nLanguage: {language}\nMethod: {method}\n',
             'Timing gaps may be silence or missing captions; coverage is not verified by caption availability.\n']
    lines += [f"[{stamp(s['start'])}–{stamp(s['end'])}] {s['text']}" for s in segments]
    (out / 'transcript.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')


def ydl_options(out, cookies=None):
    options = dict(noplaylist=True, quiet=True, socket_timeout=30, retries=1,
                   fragment_retries=1, outtmpl=str(out / 'media.%(ext)s'))
    if cookies:
        options['cookiefile'] = str(Path(cookies).resolve())
    return options


def fetch(args):
    import yt_dlp
    out = Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    # Separate metadata, captions and media: a caption failure must not trigger ASR silently.
    options = ydl_options(out, args.cookies)
    with yt_dlp.YoutubeDL(options) as dl:
        info = dl.extract_info(args.url, download=False)
    if info.get('_type') in ('playlist', 'multi_video') or info.get('is_live'):
        raise ValueError('Use a single completed video, not a playlist or live stream')
    save(out / 'metadata.json', {k: info.get(k) for k in
         ('id', 'title', 'webpage_url', 'duration', 'language', 'chapters', 'uploader')})
    choices = []
    for kind in ('subtitles', 'automatic_captions'):
        tracks = info.get(kind) or {}
        for lang in args.languages.split(','):
            for code, formats in tracks.items():
                if code == lang or code.startswith(lang + '-'):
                    track = next((f for f in formats if f.get('ext') == 'json3'), None)
                    if track:
                        choices.append((kind, code, track))
    if choices:
        kind, code, track = choices[0]
        with yt_dlp.YoutubeDL(options) as dl:
            with dl.urlopen(track['url']) as response:
                raw = response.read().decode('utf-8')
        (out / 'captions.json3').write_text(raw, encoding='utf-8')
        transcript(out, captions(json.loads(raw)), args.url, code, kind, info.get('duration'))
    else:
        print('No matching captions: fetch audio and run transcribe explicitly.', file=sys.stderr)
    if args.media != 'none':
        options['format'] = ('bestaudio/best' if args.media == 'audio' else
                             'bestvideo[height<=720]+bestaudio/best[height<=720]/best')
        with yt_dlp.YoutubeDL(options) as dl:
            dl.download([args.url])
    print(out)


def transcribe(args):
    from faster_whisper import WhisperModel
    media = Path(args.media).resolve(strict=True)
    details = probe(media)
    if not any(s['codec_type'] == 'audio' for s in details['streams']):
        raise ValueError('Media has no audio stream')
    out = Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    model = WhisperModel(args.model, device='cpu', compute_type='int8',
                         local_files_only=not args.allow_model_download)
    chunks, info = model.transcribe(str(media), language=args.language, vad_filter=True)
    segments = [dict(start=s.start, end=s.end, text=s.text.strip()) for s in chunks]
    transcript(out, segments, str(media), info.language, 'faster-whisper:' + args.model,
               float(details['format']['duration']))
    print(out / 'transcript.md')


def frame(args):
    media = Path(args.media).resolve(strict=True)
    details = probe(media)
    if not any(s['codec_type'] == 'video' for s in details['streams']):
        raise ValueError('Media has no video stream')
    time = seconds(args.at)
    duration = float(details['format']['duration'])
    if time >= duration:
        raise ValueError(f'Timestamp {time} outside video duration {duration}')
    out = Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    image = out / f'frame-{time:.3f}.png'
    # Seek after input: decode to requested position rather than the earlier keyframe.
    run(['ffmpeg', '-v', 'error', '-y', '-i', str(media), '-ss', str(time),
         '-frames:v', '1', str(image)])
    if not image.exists() or image.stat().st_size == 0:
        raise ValueError('Decoder returned no frame at requested position')
    context = []
    if args.transcript:
        data = json.loads(Path(args.transcript).read_text(encoding='utf-8'))
        context = [s for s in data['segments'] if
                   s['end'] >= max(0, time - args.context) and s['start'] <= time + args.context]
    save(out / f'frame-{time:.3f}.json', dict(media=str(media), requestedSeconds=time,
         precision='First decoded frame at/after requested position; limited by media frame rate.',
         image=str(image), transcriptContext=context))
    print(image)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    p = commands.add_parser('fetch')
    p.add_argument('url')
    p.add_argument('--out', required=True)
    p.add_argument('--languages', default='pt,en')
    p.add_argument('--media', choices=['none', 'audio', 'video'], default='none')
    p.add_argument('--cookies', help='Explicitly supplied Netscape cookie file; never auto-read browser cookies')
    p.set_defaults(action=fetch)
    p = commands.add_parser('transcribe')
    p.add_argument('media')
    p.add_argument('--out', required=True)
    p.add_argument('--model', default='base')
    p.add_argument('--language', default=None)
    p.add_argument('--allow-model-download', action='store_true')
    p.set_defaults(action=transcribe)
    p = commands.add_parser('frame')
    p.add_argument('media')
    p.add_argument('--at', required=True)
    p.add_argument('--out', required=True)
    p.add_argument('--transcript')
    p.add_argument('--context', type=float, default=10)
    p.set_defaults(action=frame)
    args = parser.parse_args()
    if args.command == 'fetch' and urlparse(args.url).scheme not in ('http', 'https'):
        parser.error('fetch requires an HTTP(S) video URL')
    if args.command == 'frame' and (not math.isfinite(args.context) or args.context < 0):
        parser.error('context must be finite and nonnegative')
    try:
        args.action(args)
    except subprocess.CalledProcessError as exc:
        parser.exit(1, f'Media tool failed: {exc.stderr}\n')
    except (ValueError, OSError, ImportError) as exc:
        parser.exit(1, f'{exc}\n')


if __name__ == '__main__':
    main()
