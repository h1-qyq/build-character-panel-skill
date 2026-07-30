# build-character-panel

An evidence-aware Codex Skill that turns user-authorized information into an RPG character panel: attributes, skills, traits, equipment, quests, buffs, debuffs, unknowns, conflicts, and growth history.

The central rule is simple: keep the game feel, never turn missing information into fake certainty.

## What it handles

- A quick panel from a short self-description
- A deep, one-question-at-a-time character interview
- Conversion from a resume, biography, notes, or chat
- Updates when new evidence supports or contradicts an old panel
- Markdown output for people
- Versioned JSON output for tools
- Offline validation and Markdown rendering
- Chinese, English, and other user languages by instruction

Every material claim can be `stated`, `observed`, `inferred`, `unknown`, or `conflicted`. Numeric scores require evidence and separate confidence.

## Installation

Copy the distributable Skill folder into your Codex skills directory:

```powershell
Copy-Item -Recurse `
  .\skills\build-character-panel `
  "$env:USERPROFILE\.codex\skills\build-character-panel"
```

Or clone the repository, then copy or link `skills/build-character-panel` into the same location. Restart or refresh Codex after installation if the Skill is not immediately discovered.

## Use

Invoke it explicitly:

```text
Use $build-character-panel to turn this self-introduction into a quick RPG character panel. Do not ask questions.
```

```text
Use $build-character-panel to interview me one question at a time and build a full character profile.
```

```text
Use $build-character-panel to update this old panel from the new evidence. Preserve contradictions and show the change log.
```

The default result is Markdown. Ask for portable JSON when you want a stable profile that can be validated, versioned, or rendered later.

## Validate profile JSON

Runtime tools require Python 3.10 or newer and use only the standard library.

```powershell
python skills/build-character-panel/scripts/validate_profile.py character-profile.json
```

Exit codes:

- `0`: valid
- `1`: structurally invalid, with JSON-style error paths
- `2`: unreadable file or malformed JSON

## Render Markdown

```powershell
python skills/build-character-panel/scripts/render_panel.py character-profile.json
```

Write to a file:

```powershell
python skills/build-character-panel/scripts/render_panel.py `
  character-profile.json `
  -o character-panel.md
```

Rendering validates first, so invalid data never becomes a polished but misleading panel.

## Privacy and evidence

The Skill does not infer protected or highly sensitive attributes, diagnose health or mental conditions, expose secrets or precise private details, or rank human worth. When a request includes unsafe inference, it omits that inference and still returns a useful supported panel.

Unknown is not zero and not average. A sparse brief can still produce an attractive panel, but unsupported fields remain visible as unknown or appear in “next unlocks.”

## Repository layout

```text
skills/build-character-panel/
├── SKILL.md
├── agents/openai.yaml
├── assets/
│   ├── character-profile.schema.json
│   ├── quick-panel-template.md
│   └── full-panel-template.md
├── references/
│   ├── attribute-system.md
│   ├── interview-guide.md
│   ├── evidence-and-scoring.md
│   ├── output-contract.md
│   └── example.md
└── scripts/
    ├── profile_model.py
    ├── validate_profile.py
    └── render_panel.py
```

Repository-level `tests/` cover package structure, validation behavior, CLI behavior, localization, and rendering.

## Development

Run the test suite:

```powershell
python -m unittest discover -s tests -v
```

Validate the Skill with the official skill creator:

```powershell
$env:PYTHONUTF8 = "1"
python "$env:USERPROFILE\.codex\skills\.system\skill-creator\scripts\quick_validate.py" `
  skills/build-character-panel
```

## Publish to GitHub

After authenticating GitHub CLI, the repository can create and verify its own remote:

```powershell
gh auth login
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\publish-to-github.ps1
```

The default repository is private and named `build-character-panel-skill`. To publish it publicly:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File `
  .\scripts\publish-to-github.ps1 `
  -Visibility public
```

The process-scoped execution policy leaves the system policy unchanged. The script refuses to publish a dirty worktree, never embeds credentials, verifies an existing `origin`, and supports PowerShell `-WhatIf`.

## License

MIT. See [LICENSE](LICENSE).
