"""Contract for the actual upstream notification sent to Genius."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class GeniusCatalogNotificationTests(unittest.TestCase):
    def dispatch(self, token="fixture-token"):
        workflow = (ROOT / ".github/workflows/validate.yml").read_text()
        notify = workflow.split("\n  notify-genius:", 1)[1].splitlines()
        start = next(index for index, line in enumerate(notify) if line == "        run: |")
        body = []
        for line in notify[start + 1:]:
            if line and not line.startswith("          "):
                break
            body.append(line[10:] if line else "")
        script = "\n".join(body)
        with tempfile.TemporaryDirectory(prefix="genius-notification-test-") as directory:
            root = Path(directory)
            binary = root / "gh"
            binary.write_text(
                "#!/usr/bin/env python3\n"
                "import json,os,pathlib,sys\n"
                "pathlib.Path(os.environ['REQUEST_FILE']).write_text(json.dumps(sys.argv[1:]))\n")
            binary.chmod(0o755)
            env = dict(os.environ, PATH=str(root) + os.pathsep + os.environ["PATH"],
                       GH_TOKEN=token, REVISION="a" * 40, REQUEST_FILE=str(root / "request.json"))
            env.pop("GITHUB_TOKEN", None)
            result = subprocess.run(["bash", "-e", "-c", script], env=env,
                                    capture_output=True, text=True)
            path = root / "request.json"
            return result, json.loads(path.read_text()) if path.exists() else None

    def test_validated_revision_is_explicitly_marked_as_automatic(self):
        result, request = self.dispatch()
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(["workflow", "run", "skill-catalog-sync.yml"], request[:3])
        self.assertEqual("sufficit/sufficit-ai-genius", request[request.index("--repo") + 1])
        self.assertEqual("main", request[request.index("--ref") + 1])
        fields = dict(request[index + 1].split("=", 1)
                      for index, argument in enumerate(request) if argument == "-f")
        self.assertEqual("a" * 40, fields.get("revision"))
        self.assertEqual("true", fields.get("automatic"))
        self.assertNotIn("fixture-token", result.stdout + result.stderr)

    def test_absent_token_does_not_send_an_unmarked_fallback_dispatch(self):
        result, request = self.dispatch(token="")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIsNone(request)
        self.assertIn("hourly sync", result.stdout)


if __name__ == "__main__":
    unittest.main()
