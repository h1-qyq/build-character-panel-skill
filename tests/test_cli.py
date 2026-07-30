from __future__ import annotations

import os
import json
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
        encoding="utf-8",
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


class RenderCliTests(unittest.TestCase):
    def test_valid_profile_renders_stable_english_panel(self) -> None:
        result = run_cli(RENDERER, FIXTURES / "valid-profile.json")
        self.assertEqual(result.returncode, 0, result.stderr)
        for text in [
            "# Lin Qiao · Evidence-minded independent maker",
            "## Core attributes",
            "62/100",
            "Medium",
            "Release a first designer tool",
            "## Unknowns",
            "## Provenance and version",
            "1.0.0",
        ]:
            with self.subTest(text=text):
                self.assertIn(text, result.stdout)

    def test_output_flag_writes_utf8_markdown(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "panel.md"
            result = run_cli(
                RENDERER,
                FIXTURES / "valid-profile.json",
                "-o",
                output,
            )
            rendered = output.read_text(encoding="utf-8")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("WROTE:", result.stdout)
        self.assertIn("# Lin Qiao", rendered)

    def test_chinese_language_uses_chinese_headings(self) -> None:
        profile = json.loads(
            (FIXTURES / "valid-profile.json").read_text(encoding="utf-8")
        )
        profile["profile"]["display_name"] = "林乔"
        profile["profile"]["language"] = "zh-CN"
        profile["provenance"]["language"] = "zh-CN"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "zh-profile.json"
            path.write_text(
                json.dumps(profile, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            result = run_cli(RENDERER, path)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("# 林乔", result.stdout)
        self.assertIn("## 核心属性", result.stdout)
        self.assertIn("## 来源与版本", result.stdout)

    def test_invalid_profile_does_not_render(self) -> None:
        result = run_cli(RENDERER, FIXTURES / "invalid-profile.json")
        self.assertEqual(result.returncode, 1)
        self.assertIn("INVALID", result.stderr)
        self.assertNotIn("# Invalid Example", result.stdout)
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
