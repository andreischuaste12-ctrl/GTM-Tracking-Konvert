import hashlib
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.inventory_gtm_export import inventory  # noqa: E402


class InventoryExportTests(unittest.TestCase):
    def setUp(self):
        self.fixture_path = ROOT / "evals/fixtures/duplicate-purchase-export.json"
        self.raw = self.fixture_path.read_bytes()
        self.document = json.loads(self.raw)

    def test_synthetic_fixture_reports_structural_findings(self):
        result = inventory(self.document, self.raw)
        self.assertEqual(result["entity_counts"]["tag"], 2)
        self.assertEqual(result["entity_counts"]["trigger"], 1)
        self.assertEqual(result["paused_tags"], 1)
        self.assertEqual(result["missing_trigger_references"], 1)
        self.assertEqual(result["orphan_triggers"], 0)
        self.assertEqual(result["unanchored_regex_filters"], 1)
        self.assertEqual(result["sequencing_cycle_groups"], 0)

    def test_sequence_cycle_and_missing_target_are_reported_without_names(self):
        document = {
            "containerVersion": {
                "tag": [
                    {"tagId": "1", "name": "A", "setupTag": [{"tagName": "B"}]},
                    {"tagId": "2", "name": "B", "setupTag": [{"tagName": "A"}]},
                    {"tagId": "3", "name": "C", "teardownTag": [{"tagName": "Missing"}]},
                ]
            }
        }
        result = inventory(document, json.dumps(document).encode())
        self.assertEqual(result["sequencing_references"], 3)
        self.assertEqual(result["sequencing_cycle_groups"], 1)
        self.assertEqual(result["unresolved_sequencing_references"], 1)

    def test_summary_hash_matches_exact_input_bytes(self):
        result = inventory(self.document, self.raw)
        self.assertEqual(result["sha256"], hashlib.sha256(self.raw).hexdigest())

    def test_cli_does_not_print_object_names_or_payload_values(self):
        completed = subprocess.run(
            [sys.executable, str(ROOT / "scripts/inventory_gtm_export.py"), "--json", str(self.fixture_path)],
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertNotIn("Synthetic GA4 purchase Web", completed.stdout)
        self.assertNotIn("Synthetic purchase event", completed.stdout)
        self.assertNotIn("purchase", completed.stdout)

    def test_realistic_fixture_golden_review_counts(self):
        path = ROOT / "evals/fixtures/realistic-web-export.json"
        raw = path.read_bytes()
        result = inventory(json.loads(raw), raw)
        expected = {
            "missing_trigger_references": 0,
            "builtin_trigger_references": 1,
            "orphan_triggers": 0,
            "tags_without_firing_trigger": 1,
            "tags_without_consent_settings": 2,
            "custom_html_tags": 1,
            "sensitive_parameter_names": 1,
            "literal_secret_like_parameters": 1,
            "unreferenced_variables": 1,
            "unresolved_variable_references": 1,
            "duplicate_ids": 0,
            "unanchored_regex_filters": 0,
        }
        for key, value in expected.items():
            self.assertEqual(result[key], value, key)

    def test_builtin_trigger_ids_are_not_reported_as_missing(self):
        document = {
            "containerVersion": {
                "tag": [{"tagId": "1", "name": "A", "firingTriggerId": ["2147479553", "99"]}]
            }
        }
        result = inventory(document, b"{}")
        self.assertEqual(result["builtin_trigger_references"], 1)
        self.assertEqual(result["missing_trigger_references"], 1)

    def test_paused_tag_without_trigger_is_not_flagged(self):
        document = {"containerVersion": {"tag": [{"tagId": "1", "name": "A", "paused": True}]}}
        self.assertEqual(inventory(document, b"{}")["tags_without_firing_trigger"], 0)

    def test_fail_on_sets_exit_code_and_rejects_unknown_counts(self):
        script = str(ROOT / "scripts/inventory_gtm_export.py")
        fixture = str(ROOT / "evals/fixtures/realistic-web-export.json")
        failing = subprocess.run(
            [sys.executable, script, fixture, "--fail-on", "custom_html_tags"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(failing.returncode, 1)
        passing = subprocess.run(
            [sys.executable, script, fixture, "--fail-on", "missing_trigger_references"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(passing.returncode, 0)
        unknown = subprocess.run(
            [sys.executable, script, fixture, "--fail-on", "nope"], capture_output=True, text=True
        )
        self.assertEqual(unknown.returncode, 2)

    def test_non_object_root_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "root must be an object"):
            inventory([], b"[]")


if __name__ == "__main__":
    unittest.main()
