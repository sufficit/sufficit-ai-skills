"""Behavioral evidence for transcript preservation and precise frame inspection."""
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / 'skills/videos/youtube-video-understand/scripts/video.py'
spec = importlib.util.spec_from_file_location('video_understand', SCRIPT)
video = importlib.util.module_from_spec(spec)
spec.loader.exec_module(video)


class TranscriptTests(unittest.TestCase):
    def test_all_cues_and_timestamps_preserved(self):
        cues = {'events': [
            {'tStartMs': 0, 'dDurationMs': 1000, 'segs': [{'utf8': 'Hello &amp; welcome'}]},
            {'tStartMs': 900, 'dDurationMs': 1000, 'segs': [{'utf8': 'Hello &amp; welcome'}]},
            {'tStartMs': 7200000, 'dDurationMs': 2000, 'segs': [{'utf8': 'Last words'}]}]}
        segments = video.captions(cues)
        self.assertEqual(2, len(segments))
        self.assertEqual(1.9, segments[0]['end'])
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            video.transcript(out, segments, 'source', 'en', 'automatic_captions', 7202)
            doc = (out / 'transcript.md').read_text()
            self.assertIn('Hello & welcome', doc)
            self.assertIn('[02:00:00.000–02:00:02.000] Last words', doc)
            self.assertEqual(segments, json.loads((out / 'transcript.json').read_text())['segments'])

    def test_distinct_overlapping_cues_not_dropped(self):
        cues = {'events': [dict(tStartMs=t, dDurationMs=1000, segs=[dict(utf8=s)])
                           for t, s in [(0, 'one'), (200, 'one two'), (1200, 'one two')]]}
        self.assertEqual(3, len(video.captions(cues)))

    def test_empty_does_not_claim_transcription(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                video.transcript(Path(tmp), [], 'source', 'en', 'asr', 10)
            self.assertFalse((Path(tmp) / 'transcript.md').exists())

    def test_time_formats_and_invalid_positions(self):
        self.assertEqual(150, video.seconds('02:30'))
        self.assertEqual(3750.25, video.seconds('1:02:30.25'))
        for invalid in ['-1', 'nan', 'inf', '1:2:3:4']:
            with self.assertRaises(ValueError):
                video.seconds(invalid)


@unittest.skipUnless(shutil.which('ffmpeg') and shutil.which('ffprobe'), 'ffmpeg not installed')
class RealFrameTests(unittest.TestCase):
    def test_requested_scene_and_transcript_window(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            media = out / 'two scenes.mkv'
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i',
                            'color=red:s=32x32:r=10:d=1', '-f', 'lavfi', '-i',
                            'color=blue:s=32x32:r=10:d=1', '-filter_complex',
                            '[0:v][1:v]concat=n=2:v=1:a=0', '-c:v', 'ffv1', str(media)], check=True)
            segments = [dict(start=0, end=.5, text='red'), dict(start=1, end=2, text='blue')]
            track = out / 'speech.json'
            track.write_text(json.dumps(dict(segments=segments)))
            subprocess.run(['python3', str(SCRIPT), 'frame', str(media), '--at', '00:01.5',
                            '--out', str(out), '--transcript', str(track), '--context', '.1'], check=True,
                           capture_output=True)
            image = out / 'frame-1.500.png'
            pixels = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', str(image),
                                               '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'])
            self.assertGreater(pixels[2], 200)  # blue scene; no earlier red keyframe
            self.assertLess(pixels[0], 20)
            evidence = json.loads((out / 'frame-1.500.json').read_text())
            self.assertEqual(['blue'], [s['text'] for s in evidence['transcriptContext']])
            bad = subprocess.run(['python3', str(SCRIPT), 'frame', str(media), '--at', '2',
                                  '--out', str(out)], capture_output=True, text=True)
            self.assertNotEqual(0, bad.returncode)
            self.assertIn('outside video duration', bad.stderr)
            self.assertFalse((out / 'frame-2.000.png').exists())


if __name__ == '__main__':
    unittest.main()
