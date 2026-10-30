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

    def test_non_object_root_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "root must be an object"):
            inventory([], b"[]")


if __name__ == "__main__":
    unittest.main()
