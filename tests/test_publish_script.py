from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "publish-to-github.ps1"


class PublishScriptTests(unittest.TestCase):
    def test_publish_script_has_safety_and_complete_flow(self) -> None:
        text = SCRIPT.read_text(encoding="utf-8")
        for expected in [
            "SupportsShouldProcess",
            'ValidateSet("private", "public", "internal")',
            'Visibility = "private"',
            'cmd /d /c "gh auth status >nul 2>nul"',
            "GitHub CLI is not authenticated.",
            "git status --porcelain",
            "gh api user --jq .login",
            "gh repo create",
            "git remote add origin",
            "git push -u origin",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, text)

    def test_publish_script_never_embeds_credentials(self) -> None:
        text = SCRIPT.read_text(encoding="utf-8").lower()
        for forbidden in ["github_token", "gh_token", "password =", "token ="]:
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, text)

    def test_readme_keeps_publish_mechanics_out_of_product_entrypoint(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        maintainer_doc = (
            ROOT / "docs" / "maintainers" / "github-publishing.md"
        ).read_text(encoding="utf-8")
        self.assertNotIn("publish-to-github.ps1", readme)
        self.assertIn(
            "powershell -NoProfile -ExecutionPolicy Bypass -File "
            r".\scripts\publish-to-github.ps1",
            maintainer_doc,
        )


if __name__ == "__main__":
    unittest.main()
