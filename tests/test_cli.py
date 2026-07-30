from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "build-character-panel" / "scripts"
FIXTURES = ROOT / "tests" / "fixtures"
VALIDATOR = SCRIPTS / "validate_profile.py"
RENDERER = SCRIPTS / "render_panel.py"


def run_cli(script: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment["PYTHONUTF8"] = "1"
    return subprocess.run(
        [sys.executable, str(script), *map(str, arguments)],
        cwd=ROOT,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )


class ValidateCliTests(unittest.TestCase):
    def test_valid_profile_exits_zero(self) -> None:
        result = run_cli(VALIDATOR, FIXTURES / "valid-profile.json")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("VALID", result.stdout)

    def test_invalid_profile_exits_one_with_paths(self) -> None:
        result = run_cli(VALIDATOR, FIXTURES / "invalid-profile.json")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("INVALID", result.stdout)
        self.assertIn("$.schema_version", result.stdout)
        self.assertIn("$.core_attributes[0].score", result.stdout)

    def test_malformed_json_exits_two_without_traceback(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "broken.json"
            path.write_text("{broken", encoding="utf-8")
            result = run_cli(VALIDATOR, path)
        self.assertEqual(result.returncode, 2)
        self.assertIn("ERROR", result.stderr)
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
