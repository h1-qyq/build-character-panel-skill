# Build Character Panel

Your life already has stats. This Skill helps you see them.

Start with honest lines about yourself. The Skill turns them into a
game-style character panel: strengths you can prove, quests you are actually
on, resources you have, and the next unlock worth pursuing.

It feels like a game. It behaves like an evidence-aware profile.

## Try it in 30 seconds

Paste this into Codex:

```text
Use $build-character-panel to turn this into a quick character panel:

I keep starting lesson materials from scratch. I am good at explaining ideas,
but I lose time polishing the same structure again and again. This week I want
to finish one reusable template.
```

You should get a first screen that looks something like this (illustrative):

```text
CHARACTER PANEL
Archetype: The Builder-in-progress
Current chapter: Turning repeated effort into a reusable system

Strengths
  Craft       supported by repeated lesson writing
  Focus       supported by a clear weekly target

Active quest
  Ship one reusable lesson template
  Next action: choose one lesson and outline its repeatable sections

Unknowns / next unlocks
  How long does a first draft take?
  What part of the template saves the most time?
```

The point is not to hand you a flattering score. It gives you a useful read on
where you are, what you can build on, and what to do next.

## What you can make with it

- **A quick panel** from a short self-description, without a long form.
- **A deeper character build** through one useful question at a time.
- **A source conversion** from a resume, biography, notes, or chat history.
- **A living profile** that preserves old and new evidence, conflicts, and
  change over time.
- **A portable profile** in Markdown for people or versioned JSON for tools.

## Pick your mode

| If you want to... | Ask for... |
| --- | --- |
| See a useful first read now | a quick panel |
| Understand yourself more deeply | a one-question-at-a-time interview |
| Turn existing material into a panel | a source conversion |
| Refresh an old panel | an evidence-based update |
| Avoid questions for now | a no-question fallback with visible unknowns |

## Installation, without GitHub

You do not need Git, GitHub, or a separate runtime to try the Skill. Copy the
distributable folder into your Codex skills directory:

```powershell
Copy-Item -Recurse `
  .\skills\build-character-panel `
  "$env:USERPROFILE\.codex\skills\build-character-panel"
```

Refresh Codex if the Skill is not visible.

The panel itself has no required environment variables or external services.
Python powers the optional profile validation and rendering tools below.

Then call it directly:

```text
Use $build-character-panel to make a quick panel from this self-introduction.
Do not ask questions.
```

```text
Use $build-character-panel to interview me one question at a time and build a
full character profile.
```

```text
Use $build-character-panel to update this old panel from the new evidence.
Keep the change log and preserve conflicts.
```

## Why the panel stays honest

Every material claim carries an evidence state: `stated`, `observed`,
`inferred`, `unknown`, or `conflicted`.

Scores are optional. A score appears when evidence supports it, with a separate
confidence level and a short rationale. Unknown is not zero, average, or a
verdict. Think of it as a blank slot you can unlock.

The game layer makes reflection easier to read. The evidence layer keeps it
from becoming fiction.

## Privacy is part of the design

The Skill does not diagnose health or mental conditions, infer protected or
highly sensitive traits, expose secrets or precise private details, or rank
human worth. If a request asks for an unsafe inference, the Skill leaves it
out and still returns the useful, supported part of the panel.

## Portable profiles

Runtime tools require Python 3.10 or newer and use the standard library.

Check a profile:

```powershell
python skills/build-character-panel/scripts/validate_profile.py `
  character-profile.json
```

Render a validated profile to Markdown:

```powershell
python skills/build-character-panel/scripts/render_panel.py `
  character-profile.json
```

Write the rendered panel to a file:

```powershell
python skills/build-character-panel/scripts/render_panel.py `
  character-profile.json `
  -o character-panel.md
```

Rendering validates first, so invalid data never becomes a polished but
misleading panel.

## Behind the first screen

The full Skill lives in `skills/build-character-panel/`:

```text
skills/build-character-panel/
  SKILL.md
  agents/openai.yaml
  assets/                 # schema and panel templates
  references/             # interview, evidence, scoring, and output guidance
  scripts/                # validation, rendering, and profile model
```

The repository-level `tests/` cover package structure, validation behavior, CLI
behavior, localization, and rendering.

## For contributors

Run the test suite:

```powershell
python -m unittest discover -s tests -v
```

Check the Skill with the official checker:

```powershell
$env:PYTHONUTF8 = "1"
$checker = Join-Path $env:USERPROFILE `
  ".codex\.skills\.system\skill-creator\scripts\quick_validate.py"
python $checker `
  skills/build-character-panel
```

## Project status

The Skill is usable locally today. The repository versions its schema and
output contract, while the panel design and examples remain open to
improvement. Contributors maintain the project; when documentation and
behavior disagree, the source and tests are the authority.

## License

MIT. See [LICENSE](LICENSE).
