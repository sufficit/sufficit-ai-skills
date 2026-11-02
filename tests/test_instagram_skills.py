"""Behaviour tests for the Instagram skill scripts and profile rubric.

Purpose: keep the caption linter, post audit, beat sheet and rubric correct for Portuguese input.
Usage: python3 -B -m unittest tests.test_instagram_skills -v
Last modified: 2026-11-02
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INSTAGRAM = ROOT / "skills/instagram"
CAPTION = INSTAGRAM / "instagram-caption/scripts/caption_lint.py"
AUDIT = INSTAGRAM / "instagram-audit/scripts/audit_posts.py"
BEATS = INSTAGRAM / "instagram-reel/scripts/beat_sheet.py"
RUBRIC = INSTAGRAM / "instagram-profile-setup/references/rubric.json"


def run(script: Path, *arguments: str, stdin: str = "") -> subprocess.CompletedProcess:
    # -B keeps __pycache__ out of the package, which would change its digest.
    return subprocess.run(
        [sys.executable, "-B", str(script), *arguments],
        input=stdin,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def lint(caption: str, *arguments: str) -> tuple[dict, int]:
    done = run(CAPTION, "-", "--json", *arguments, stdin=caption)
    return json.loads(done.stdout), done.returncode


def status(result: dict, check: str) -> str:
    return next(item["status"] for item in result["checks"] if item["check"] == check)


class CaptionLintTests(unittest.TestCase):
    def test_portuguese_caption_passes(self) -> None:
        caption = (
            "Perdi R$ 18 mil por causa de uma cláusula.\n\n"
            "O fluxo de caixa mostrou o erro.\n\nComente CONTRATO e envio o modelo.\n\n"
            + " ".join(["#contratos", "#gestão"])
        )
        padded = caption.replace("\n\n#", " " + "detalhe " * 15 + "\n\n#")
        result, code = lint(padded, "--keywords", "fluxo de caixa")
        self.assertEqual(code, 0)
        self.assertEqual(result["verdict"], "READY", result["checks"])
        self.assertEqual(result["asks"], ["comment a keyword"])

    def test_accented_hashtag_is_kept_whole(self) -> None:
        result, _ = lint("Texto curto com 3 itens.\n\n#gestão")
        self.assertEqual(result["hashtags"], ["#gestão"])

    def test_more_than_five_hashtags_fail(self) -> None:
        result, code = lint("Temos 3 planos.\n\n" + " ".join(f"#tag{i}" for i in range(6)))
        self.assertEqual(status(result, "HASHTAGS"), "FAIL")
        self.assertEqual(code, 1)

    def test_portuguese_greeting_warns(self) -> None:
        result, _ = lint("Oi gente, hoje vamos falar de conteúdo")
        self.assertEqual(status(result, "FIRST LINE"), "WARN")

    def test_lowercase_prose_is_not_a_keyword_ask(self) -> None:
        result, _ = lint("Please comment on this idea when you can")
        self.assertEqual(result["asks"], [])

    def test_brazilian_domain_is_a_dead_link(self) -> None:
        result, _ = lint("Veja em sufficit.com.br hoje")
        self.assertEqual(status(result, "LINKS"), "WARN")

    def test_search_term_ignores_accents(self) -> None:
        result, _ = lint("Nossa gestão financeira cresceu 3 vezes", "--keywords", "gestao financeira")
        self.assertEqual(status(result, "SEARCH TERMS"), "PASS")


class AuditTests(unittest.TestCase):
    HEADER = "id,date,format,label,views,reach,shares,follows,skip_rate\n"

    def audit(self, body: str, *arguments: str) -> dict:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory, "posts.csv")
            path.write_text(self.HEADER + body, encoding="utf-8")
            done = run(AUDIT, str(path), "--json", "--as-of", "2026-11-02", *arguments)
        self.assertEqual(done.returncode, 0, done.stderr)
        return json.loads(done.stdout)

    def test_ranks_by_own_median_and_diagnoses(self) -> None:
        result = self.audit(
            "hit,2026-10-01,reel,a,1000,800,40,16,20\n"
            "viewsnofollow,2026-10-02,reel,a,900,800,5,1,25\n"
            "mid,2026-10-03,reel,b,100,80,1,1,30\n"
            "flop,2026-10-04,reel,b,10,8,0,1,70\n"
            "low,2026-10-05,reel,b,20,16,0,1,10\n"
        )
        self.assertEqual(result["baselineMedianViews"], 100)
        by_id = {post["id"]: post for post in result["ranked"]}
        self.assertEqual(result["ranked"][0]["id"], "hit")
        self.assertEqual(by_id["hit"]["outlier"], 10)
        self.assertEqual(by_id["hit"]["diagnosis"], "hit")
        self.assertIn("profile", by_id["viewsnofollow"]["diagnosis"])
        self.assertIn("check the hook", by_id["flop"]["diagnosis"])
        self.assertIn("not the cause", by_id["low"]["diagnosis"])
        self.assertIn("insufficient", result["confidence"])

    def test_blank_metric_stays_unknown(self) -> None:
        result = self.audit("a,2026-10-01,,,100,,,,\nb,2026-10-02,,,10,,,,\nc,2026-10-03,,,1,,,,\n")
        worst = result["ranked"][-1]
        self.assertIsNone(worst["sends_per_reach"])
        self.assertIn("unknown", worst["diagnosis"])

    def test_recent_posts_stay_out_of_the_baseline(self) -> None:
        result = self.audit("old,2026-10-01,,,100,,,,\nnew,2026-11-01,,,999999,,,,\n")
        self.assertEqual(result["analysed"], 1)
        self.assertEqual(result["tooRecent"], 1)
        self.assertEqual(result["baselineMedianViews"], 100)

    def test_invalid_number_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory, "posts.csv")
            path.write_text(self.HEADER + "a,2026-10-01,,,muitos,,,,\n", encoding="utf-8")
            done = run(AUDIT, str(path))
        self.assertNotEqual(done.returncode, 0)
        self.assertIn("views is not a number", done.stderr.replace("column ", ""))


class BeatSheetTests(unittest.TestCase):
    def sheet(self, script: str, *arguments: str) -> dict:
        done = run(BEATS, "-", "--json", *arguments, stdin=script)
        self.assertEqual(done.returncode, 0, done.stderr)
        return json.loads(done.stdout)

    def test_portuguese_loop_ignores_accents_and_counts_amount_once(self) -> None:
        result = self.sheet("Perdi R$ 18.000 na gestão.\nHoje a gestao mudou.", "--wpm", "120")
        self.assertEqual(result["beats"][0]["words"], 5)
        self.assertEqual(result["beats"][0]["seconds"], 2.5)
        self.assertTrue(any("echoes the hook: gestao" in note for note in result["notes"]))

    def test_long_hook_and_beat_are_flagged(self) -> None:
        line = " ".join(["palavra"] * 12)
        result = self.sheet(line, "--wpm", "120")
        self.assertTrue(result["beats"][0]["flags"])
        self.assertTrue(any("Cut the hook" in note for note in result["notes"]))

    def test_lone_dash_is_not_a_word(self) -> None:
        self.assertEqual(self.sheet("um - dois")["totalWords"], 2)

    def test_abstract_run_and_uncalibrated_rate_are_reported(self) -> None:
        result = self.sheet("tudo muda sempre\nnada fica igual\nsiga em frente")
        self.assertFalse(result["calibrated"])
        self.assertTrue(any("--wpm" in note for note in result["notes"]))
        self.assertTrue(any("Beats 1-3" in note for note in result["notes"]))

    def test_empty_script_is_rejected(self) -> None:
        self.assertEqual(run(BEATS, "-", stdin="  \n").returncode, 2)


class RubricTests(unittest.TestCase):
    def test_points_add_up_and_items_are_complete(self) -> None:
        rubric = json.loads(RUBRIC.read_text(encoding="utf-8"))
        self.assertEqual(sum(item["points"] for item in rubric["items"]), rubric["total"])
        self.assertEqual(len({item["id"] for item in rubric["items"]}), len(rubric["items"]))
        for item in rubric["items"]:
            self.assertIn(item["visibility"], {"public", "owner"})
            self.assertTrue(item["fullMarks"] and item["commonFail"])


if __name__ == "__main__":
    unittest.main()
