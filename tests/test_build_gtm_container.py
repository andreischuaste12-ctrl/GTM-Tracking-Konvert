import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/gtm-build-konvert"
sys.path.insert(0, str(SKILL / "scripts"))

from build_gtm_container import build, encode_parameter  # noqa: E402


class BuildContainerTests(unittest.TestCase):
    def setUp(self):
        self.spec_path = SKILL / "examples/saas-trial-activated.spec.json"
        self.spec = json.loads(self.spec_path.read_text(encoding="utf-8"))

    def test_example_spec_builds_without_errors(self):
        document, errors, warnings = build(self.spec)
        version = document["containerVersion"]
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])
        self.assertEqual((len(version["tag"]), len(version["trigger"])), (1, 1))
        self.assertEqual(len(version["variable"]), 3)
        tag = version["tag"][0]
        self.assertEqual(tag["firingTriggerId"], [version["trigger"][0]["triggerId"]])
        self.assertEqual(tag["consentSettings"]["consentStatus"], "NEEDED")

    def test_custom_event_trigger_uses_exact_match_not_regex(self):
        document, _, _ = build(self.spec)
        event_filter = document["containerVersion"]["trigger"][0]["customEventFilter"][0]
        self.assertEqual(event_filter["type"], "EQUALS")

    def test_parameter_encoding(self):
        self.assertEqual(encode_parameter("a", True)["value"], "true")
        self.assertEqual(encode_parameter("a", 2), {"type": "INTEGER", "key": "a", "value": "2"})
        with self.assertRaises(ValueError):
            encode_parameter("a", ["not", "supported"])
        with self.assertRaises(ValueError):
            encode_parameter("a", {"table": {"columns": ["x", "y"], "rows": [["only-one"]]}})

    def test_unknown_trigger_unresolved_reference_and_naming_are_errors(self):
        spec = copy.deepcopy(self.spec)
        spec["tags"][0]["firingTriggers"] = ["Event | Missing"]
        spec["tags"][0]["params"]["eventName"] = "{{DLV | Not defined}}"
        spec["variables"][1]["name"] = "event_id"
        _, errors, _ = build(spec)
        joined = "\n".join(errors)
        self.assertIn("unknown firing trigger", joined)
        self.assertIn("unresolved reference", joined)
        self.assertIn("approved prefix", joined)

    def test_unanchored_regex_and_missing_consent_types_are_errors(self):
        spec = copy.deepcopy(self.spec)
        spec["triggers"][0].pop("eventName")
        spec["triggers"][0]["raw"] = {
            "customEventFilter": [
                {
                    "type": "MATCH_REGEX",
                    "parameter": [
                        {"type": "TEMPLATE", "key": "arg0", "value": "{{_event}}"},
                        {"type": "TEMPLATE", "key": "arg1", "value": "trial"},
                    ],
                }
            ]
        }
        spec["tags"][0]["consent"] = {"status": "NEEDED", "types": []}
        _, errors, _ = build(spec)
        joined = "\n".join(errors)
        self.assertIn("anchored", joined)
        self.assertIn("requires at least one consent type", joined)

    def test_literal_secret_is_error_and_pii_name_is_warning(self):
        spec = copy.deepcopy(self.spec)
        spec["tags"][0]["params"]["api_secret"] = "literal-value"
        spec["variables"][2]["params"]["name"] = "user.email"
        _, errors, warnings = build(spec)
        self.assertTrue(any("secret-like" in message for message in errors))
        self.assertTrue(any("sensitive-looking" in message for message in warnings))

    def test_untriggered_active_tag_is_error_but_paused_is_allowed(self):
        spec = copy.deepcopy(self.spec)
        spec["tags"][0]["firingTriggers"] = []
        _, errors, _ = build(spec)
        self.assertTrue(any("no firing trigger" in message for message in errors))
        spec["tags"][0]["paused"] = True
        _, errors, _ = build(spec)
        self.assertEqual(errors, [])

    def test_raw_cannot_override_identity_fields(self):
        spec = copy.deepcopy(self.spec)
        spec["tags"][0]["raw"] = {"tagId": "99"}
        _, errors, _ = build(spec)
        self.assertTrue(any("'raw' may not set" in message for message in errors))

    def test_events_contract_expands_to_variables_triggers_and_tags(self):
        spec = json.loads((SKILL / "examples/saas-events-contract.spec.json").read_text())
        document, errors, warnings = build(spec)
        version = document["containerVersion"]
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])
        self.assertEqual(len(version["tag"]), 2)
        self.assertEqual(len(version["trigger"]), 2)
        # shared event_id variable is created once; plan_category and lead_source add two more
        self.assertEqual(len(version["variable"]), 1 + 3)
        names = {item["name"] for item in version["variable"]}
        self.assertIn("DLV | Event | event_id", names)
        lead_var = next(v for v in version["variable"] if v["name"] == "DLV | Lead | lead_source")
        self.assertIn({"type": "TEMPLATE", "key": "name", "value": "lead.source"}, lead_var["parameter"])

    def test_events_validate_ga4_names_and_conflicting_variable_paths(self):
        spec = json.loads((SKILL / "examples/saas-events-contract.spec.json").read_text())
        spec["events"][0]["name"] = "Subscription Upgraded"
        spec["events"][1]["name"] = "ga_lead_accepted"
        spec["events"][1]["parameters"][1]["name"] = "ga_source"
        spec["events"][1]["parameters"][0]["path"] = "other.event_id"
        _, errors, _ = build(spec)
        joined = "\n".join(errors)
        self.assertIn("name must match", joined)
        self.assertIn("reserved prefix", joined)
        self.assertIn("another path", joined)
        self.assertIn("parameter 'ga_source' uses a reserved prefix", joined)

    def test_events_require_measurement_variable(self):
        spec = json.loads((SKILL / "examples/saas-events-contract.spec.json").read_text())
        del spec["ga4"]["measurementIdVariable"]
        _, errors, _ = build(spec)
        self.assertTrue(any("measurementIdVariable" in message for message in errors))

    def test_base_export_continues_ids_resolves_references_and_checks_evidence(self):
        base = json.loads((ROOT / "evals/fixtures/realistic-web-export.json").read_text())
        spec = {
            "ga4": {"measurementIdVariable": "Constant | GA4 | Measurement ID"},
            "builtinTriggerIds": {"Initialization": "2147479572", "Guess": "2147479999"},
            "events": [
                {
                    "name": "plan_changed",
                    "domain": "Account",
                    "parameters": [{"name": "event_id", "variableName": "DLV | Event | event_id"}],
                    "consent": {"status": "NEEDED", "types": ["analytics_storage"]},
                }
            ],
        }
        document, errors, warnings = build(spec, base)
        version = document["containerVersion"]
        self.assertEqual(errors, [])
        self.assertEqual(version["tag"][0]["tagId"], "4")
        self.assertEqual(version["trigger"][0]["triggerId"], "11")
        self.assertEqual(version["variable"], [])  # event_id already exists in the base
        joined = "\n".join(warnings)
        self.assertIn("measurementIdOverride", joined)  # key not seen for gaawe in base
        self.assertIn("2147479999", joined)  # built-in ID with no evidence in base
        self.assertNotIn("2147479572", joined)

    def test_base_export_rejects_name_collisions(self):
        base = json.loads((ROOT / "evals/fixtures/realistic-web-export.json").read_text())
        spec = json.loads((SKILL / "examples/saas-trial-activated.spec.json").read_text())
        _, errors, _ = build(spec, base)
        joined = "\n".join(errors)
        self.assertIn("already exists in the base export", joined)

    def test_cli_writes_file_and_refuses_overwrite_without_force(self):
        script = SKILL / "scripts/build_gtm_container.py"
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "container.json"
            command = [sys.executable, str(script), str(self.spec_path), "--output", str(output)]
            first = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(json.loads(output.read_text())["exportFormatVersion"], 2)
            second = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(second.returncode, 2)
            self.assertIn("--force", second.stderr)

    def test_cli_writes_nothing_when_errors_exist(self):
        script = SKILL / "scripts/build_gtm_container.py"
        spec = copy.deepcopy(self.spec)
        spec["tags"][0]["firingTriggers"] = ["Event | Missing"]
        with tempfile.TemporaryDirectory() as directory:
            spec_path = Path(directory) / "spec.json"
            spec_path.write_text(json.dumps(spec), encoding="utf-8")
            output = Path(directory) / "container.json"
            result = subprocess.run(
                [sys.executable, str(script), str(spec_path), "--output", str(output)],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 1)
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
