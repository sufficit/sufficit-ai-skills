import hashlib
import sys
sys.dont_write_bytecode = True
import importlib.util
from pathlib import Path
import tempfile
import unittest
from uuid import uuid4
import wave

spec = importlib.util.spec_from_file_location("guard", Path(__file__).resolve().parents[1] / "skills/sufficit/sufficit-api/scripts/customer_write_guard.py")
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)

class GuardTests(unittest.TestCase):
    def setUp(self):
        self.context = str(uuid4())
        self.resource = {"id": str(uuid4()), "contextid": self.context}

    def test_valid_guid_variants_match_without_executing(self):
        result = guard.validate(self.context.replace("-", "").upper(), [self.resource], {"contextId": self.context})
        self.assertEqual(self.context, result["contextId"])
        self.assertFalse(result["executed"])
        self.assertFalse(result["authorizationVerified"])

    def test_missing_global_wrong_and_conflicting_owners_are_rejected(self):
        for context, resource in [(None, self.resource), ("00000000-0000-0000-0000-000000000000", self.resource),
            ("000140", self.resource), (self.context, {"id": self.context}),
            (self.context, {"contextId": str(uuid4())}),
            (self.context, {"contextId": self.context, "contextid": str(uuid4())})]:
            with self.subTest(context=context, resource=resource), self.assertRaises(ValueError):
                guard.validate(context, [resource])

    def test_a_batch_cannot_mix_customers_or_reuse_a_foreign_nested_body(self):
        with self.assertRaises(ValueError):
            guard.validate(self.context, [self.resource, {"contextId": str(uuid4())}])
        with self.assertRaises(ValueError):
            guard.validate(self.context, [self.resource], {"items": [{"contextId": str(uuid4())}]})
        with self.assertRaises(ValueError):
            guard.validate(self.context, [])

    def test_moh_manifest_binds_owned_class_bytes_hash_and_validation_only(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/"hold.wav"
            with wave.open(str(path), "wb") as wav:
                wav.setparams((1, 2, 8000, 0, "NONE", "not compressed"))
                wav.writeframes(bytes(160))
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            result = guard.moh_manifest(self.context, self.resource, path, digest)
            self.assertEqual(self.resource["id"], result["classId"])
            self.assertEqual(self.context, result["contextId"])
            self.assertEqual(digest, result["sha256"])
            self.assertTrue(result["validateOnly"])
            self.assertEqual("music_on_hold_add", result["upload"])
            with self.assertRaises(ValueError):
                guard.moh_manifest(self.context, self.resource, path, "wrong")

    def test_opus_or_renamed_non_pcm_audio_is_not_a_playable_wav(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/"renamed.wav"
            path.write_bytes(b"OggS"+b"OpusHead"+bytes(50))
            with self.assertRaises(ValueError):
                guard.moh_manifest(self.context, self.resource, path, hashlib.sha256(path.read_bytes()).hexdigest())
            with wave.open(str(path), "wb") as wav:
                wav.setparams((2, 2, 48000, 0, "NONE", "not compressed")); wav.writeframes(bytes(160))
            with self.assertRaises(ValueError):
                guard.moh_manifest(self.context, self.resource, path, hashlib.sha256(path.read_bytes()).hexdigest())

if __name__ == "__main__":
    unittest.main()
