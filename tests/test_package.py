from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "build-character-panel"

CORE_FILES = [
    "SKILL.md",
    "agents/openai.yaml",
    "references/attribute-system.md",
    "references/interview-guide.md",
    "references/evidence-and-scoring.md",
    "references/output-contract.md",
]

DOMAIN_IDS = [
    "identity",
    "roles-context",
    "origin-story",
    "values-boundaries",
    "motives-needs",
    "personality-behavior",
    "cognition-learning",
    "communication-social",
    "relationships-environments",
    "capabilities-craft",
    "habits-energy",
    "resources-constraints",
    "aesthetic-public-image",
    "digital-presence",
    "achievements-arcs",
    "quests-missions",
    "risks-recovery",
    "growth-history",
]


class SkillPackageTests(unittest.TestCase):
    def test_core_files_exist(self) -> None:
        missing = [relative for relative in CORE_FILES if not (SKILL / relative).is_file()]
        self.assertEqual(missing, [])

    def test_frontmatter_and_agent_metadata(self) -> None:
        skill_text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        frontmatter = re.match(r"\A---\n(.*?)\n---\n", skill_text, re.DOTALL)
        self.assertIsNotNone(frontmatter)
        metadata = frontmatter.group(1)
        self.assertIn("name: build-character-panel", metadata)
        self.assertRegex(metadata, r"(?m)^description: Use when ")
        self.assertNotRegex(metadata, r"(?m)^(?!name:|description:)[a-z_]+:")

        agent_text = (SKILL / "agents" / "openai.yaml").read_text(encoding="utf-8")
        self.assertIn('display_name: "Character Panel"', agent_text)
        self.assertIn("$build-character-panel", agent_text)

    def test_attribute_reference_covers_all_domains_and_attributes(self) -> None:
        text = (SKILL / "references" / "attribute-system.md").read_text(
            encoding="utf-8"
        )
        for domain_id in DOMAIN_IDS:
            with self.subTest(domain_id=domain_id):
                self.assertIn(f"`{domain_id}`", text)
        for attribute in [
            "vitality",
            "focus",
            "learning",
            "craft",
            "agency",
            "social",
            "resilience",
        ]:
            with self.subTest(attribute=attribute):
                self.assertIn(f"`{attribute}`", text)

    def test_workflow_contains_evidence_and_safety_contracts(self) -> None:
        combined = "\n".join(
            (SKILL / relative).read_text(encoding="utf-8")
            for relative in CORE_FILES
            if (SKILL / relative).is_file()
        ).lower()
        for term in [
            "stated",
            "observed",
            "inferred",
            "unknown",
            "conflicted",
            "confidence",
            "evidence",
            "diagnos",
            "sensitive",
            "no-question",
        ]:
            with self.subTest(term=term):
                self.assertIn(term, combined)

    def test_skill_contains_no_authoring_placeholders(self) -> None:
        placeholders = re.compile(
            r"\b(TBD|TODO|implement later|fill in details|example_placeholder)\b",
            re.IGNORECASE,
        )
        matches: list[str] = []
        if SKILL.exists():
            for path in SKILL.rglob("*"):
                if path.is_file() and path.suffix.lower() in {".md", ".yaml", ".json", ".py"}:
                    text = path.read_text(encoding="utf-8")
                    if placeholders.search(text):
                        matches.append(str(path.relative_to(SKILL)))
        self.assertEqual(matches, [])


if __name__ == "__main__":
    unittest.main()
