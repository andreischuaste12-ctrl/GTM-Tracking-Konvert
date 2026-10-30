import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "evals"))

from build_review_sheet import render  # noqa: E402


class ReviewSheetTests(unittest.TestCase):
    def test_every_criterion_gets_a_row_for_both_skills(self):
        for evals_path in (ROOT / "evals/evals.json", ROOT / "skills/gtm-build-konvert/evals/evals.json"):
            data = json.loads(evals_path.read_text(encoding="utf-8"))
            sheet = render(data)
            expected = sum(
                len(item["assertions"]["must_include"]) + len(item["assertions"]["must_not_claim"])
                for item in data["evals"]
            )
            self.assertEqual(sheet.count("| [ ] |"), expected)
            self.assertIn("NOT EXECUTED", sheet)

    def test_cli_runs(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "evals/build_review_sheet.py"), str(ROOT / "evals/evals.json")],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
