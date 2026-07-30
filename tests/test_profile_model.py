from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "build-character-panel" / "scripts"
FIXTURES = ROOT / "tests" / "fixtures"
sys.path.insert(0, str(SCRIPTS))

from profile_model import load_profile, validate_profile  # noqa: E402


class ProfileModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.valid = json.loads(
            (FIXTURES / "valid-profile.json").read_text(encoding="utf-8")
        )

    def test_valid_fixture_has_no_errors(self) -> None:
        self.assertEqual(validate_profile(self.valid), [])

    def test_load_profile_reads_utf8_json(self) -> None:
        loaded = load_profile(FIXTURES / "valid-profile.json")
        self.assertEqual(loaded["profile"]["display_name"], "Lin Qiao")

    def test_rejects_unsupported_schema_version(self) -> None:
        data = copy.deepcopy(self.valid)
        data["schema_version"] = "2.0"
        self.assertHasError(data, "$.schema_version")

    def test_rejects_score_outside_zero_to_one_hundred(self) -> None:
        data = copy.deepcopy(self.valid)
        data["core_attributes"][0]["score"] = 101
        self.assertHasError(data, "$.core_attributes[0].score")

    def test_rejects_scored_attribute_without_evidence(self) -> None:
        data = copy.deepcopy(self.valid)
        data["core_attributes"][0]["evidence"] = []
        self.assertHasError(data, "$.core_attributes[0].evidence")

    def test_rejects_invalid_evidence_state(self) -> None:
        data = copy.deepcopy(self.valid)
        data["skills"][0]["evidence"][0]["state"] = "guessed"
        self.assertHasError(data, "$.skills[0].evidence[0].state")

    def test_accepts_unknown_score_with_unknown_confidence(self) -> None:
        data = copy.deepcopy(self.valid)
        data["core_attributes"][0]["score"] = None
        data["core_attributes"][0]["confidence"] = "unknown"
        data["core_attributes"][0]["evidence"] = []
        self.assertEqual(validate_profile(data), [])

    def test_rejects_unknown_score_with_claimed_confidence(self) -> None:
        data = copy.deepcopy(self.valid)
        data["core_attributes"][0]["score"] = None
        data["core_attributes"][0]["confidence"] = "medium"
        data["core_attributes"][0]["evidence"] = []
        self.assertHasError(data, "$.core_attributes[0].confidence")

    def assertHasError(self, data: object, path: str) -> None:
        errors = validate_profile(data)
        self.assertTrue(
            any(error.startswith(path) for error in errors),
            f"Expected an error at {path}; got {errors}",
        )


if __name__ == "__main__":
    unittest.main()
