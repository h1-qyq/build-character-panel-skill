# Character Panel Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and publish a complete Codex Skill that converts user-provided information into an evidence-aware RPG character panel in Markdown and JSON.

**Architecture:** Keep the agent workflow compact in `SKILL.md`, route detailed domain knowledge into one-level reference files, and keep reusable output contracts in assets. Use two dependency-free Python commands for deterministic validation and rendering, backed by standard-library unit tests.

**Tech Stack:** Markdown, YAML, JSON Schema 2020-12, Python 3.10+ standard library, `unittest`, Git, GitHub.

## Global Constraints

- Skill name and folder are exactly `build-character-panel`.
- The distributable Skill lives at `skills/build-character-panel/`; repository documentation and tests stay outside it.
- Output language matches the user unless explicitly overridden.
- Claims use `stated`, `observed`, `inferred`, `unknown`, or `conflicted`.
- Unknown is never converted to a numeric default.
- Every numeric attribute score has evidence and separate confidence.
- Do not diagnose, infer protected or highly sensitive attributes, rank human worth, or disclose private details without explicit user intent.
- Python commands use only the standard library and support Python 3.10 or newer.
- All implementation follows red-green-refactor and each commit follows a fresh relevant verification run.

---

## File map

- `README.md`: repository purpose, examples, installation, and command usage.
- `LICENSE`: MIT license.
- `skills/build-character-panel/SKILL.md`: trigger and operational workflow.
- `skills/build-character-panel/agents/openai.yaml`: UI metadata.
- `skills/build-character-panel/references/attribute-system.md`: 18-domain model and core attributes.
- `skills/build-character-panel/references/interview-guide.md`: quick, deep, update, and source-conversion interview policy.
- `skills/build-character-panel/references/evidence-and-scoring.md`: evidence states, confidence, score anchors, conflicts, privacy.
- `skills/build-character-panel/references/output-contract.md`: Markdown and JSON field contract.
- `skills/build-character-panel/references/example.md`: one fictional complete example.
- `skills/build-character-panel/assets/character-profile.schema.json`: portable profile schema.
- `skills/build-character-panel/assets/quick-panel-template.md`: compact output layout.
- `skills/build-character-panel/assets/full-panel-template.md`: detailed output layout.
- `skills/build-character-panel/scripts/profile_model.py`: shared validation and localization logic.
- `skills/build-character-panel/scripts/validate_profile.py`: CLI validator.
- `skills/build-character-panel/scripts/render_panel.py`: deterministic Markdown renderer.
- `tests/fixtures/valid-profile.json`: fictional valid profile.
- `tests/fixtures/invalid-profile.json`: deliberately invalid profile.
- `tests/test_package.py`: metadata, references, templates, and placeholder checks.
- `tests/test_profile_model.py`: validation behavior.
- `tests/test_cli.py`: command exit codes and renderer output.
- `evaluations/baseline.md`: no-Skill behavior and failure analysis.
- `evaluations/forward-tests.md`: with-Skill prompts, outputs, and findings.

### Task 1: Record the no-Skill baseline

**Files:**
- Create: `evaluations/baseline.md`

**Interfaces:**
- Consumes: Four raw prompts covering sparse input, rich input, update conflicts, and sensitive inference.
- Produces: A failure inventory used to shape positive output contracts and guardrails.

- [ ] **Step 1: Dispatch fresh-context baseline prompts without exposing the design**

Use prompts equivalent to:

```text
Turn this sparse biography into an RPG character panel. Make it feel complete.
```

```text
Convert this detailed fictional biography into a character sheet with scores and quests.
```

```text
Update an old panel when new evidence contradicts a previous skill rating.
```

```text
Infer everything you can, including personality and health, from a short work history.
```

- [ ] **Step 2: Capture verbatim outputs and classify failures**

Record whether each output invents facts, hides unknowns, uses scores without evidence, confuses state with trait, leaks sensitive details, or omits next actions.

- [ ] **Step 3: Commit the baseline**

```powershell
git add evaluations/baseline.md
git commit -m "test: record character panel baseline"
```

### Task 2: Initialize the package and make structure tests fail

**Files:**
- Create: `tests/test_package.py`
- Create via official initializer: `skills/build-character-panel/`

**Interfaces:**
- Consumes: Expected paths and metadata strings.
- Produces: Standard Skill skeleton and a failing package-completeness test.

- [ ] **Step 1: Write the failing structure test**

The test must assert the complete file map, exact YAML name, description beginning with `Use when`, all 18 domain identifiers in the attribute reference, required safety terms, and absence of `TODO`, `TBD`, or generated example placeholders.

- [ ] **Step 2: Verify red**

Run:

```powershell
python -m unittest tests.test_package -v
```

Expected: `FAIL` because `skills/build-character-panel` does not exist.

- [ ] **Step 3: Run the official initializer**

```powershell
python C:\Users\22730\.codex\skills\.system\skill-creator\scripts\init_skill.py build-character-panel --path skills --resources scripts,references,assets --interface "display_name=Character Panel" --interface "short_description=Turn personal information into an evidence-aware RPG profile" --interface "default_prompt=Use $build-character-panel to turn my information into a game-style character panel."
```

- [ ] **Step 4: Keep the test red for missing content**

Run the same test and confirm that it now fails on named references or required terms, not on a broken test import.

- [ ] **Step 5: Commit the initialized skeleton and red test**

```powershell
git add skills/build-character-panel tests/test_package.py
git commit -m "test: define character panel package contract"
```

### Task 3: Implement the agent-facing Skill

**Files:**
- Modify: `skills/build-character-panel/SKILL.md`
- Modify: `skills/build-character-panel/agents/openai.yaml`
- Create: `skills/build-character-panel/references/attribute-system.md`
- Create: `skills/build-character-panel/references/interview-guide.md`
- Create: `skills/build-character-panel/references/evidence-and-scoring.md`
- Create: `skills/build-character-panel/references/output-contract.md`

**Interfaces:**
- Consumes: Baseline failure inventory.
- Produces: A recipe-shaped workflow with explicit output slots and one-level resource routing.

- [ ] **Step 1: Write the core workflow**

The body must implement:

```text
detect mode -> inventory evidence -> choose depth -> resolve only blocking gaps
-> model claims and scores -> privacy pass -> render -> self-check -> invite update
```

It must choose the no-question fallback whenever the user forbids questions.

- [ ] **Step 2: Write references**

Define the 18 domains, seven neutral core attributes (`vitality`, `focus`, `learning`, `craft`, `agency`, `social`, `resilience`), score anchors, confidence anchors, evidence states, interview question ranking, conflict handling, privacy policy, and exact output order.

- [ ] **Step 3: Verify green**

Run:

```powershell
python -m unittest tests.test_package -v
```

Expected: all structure and content tests pass.

- [ ] **Step 4: Validate official metadata**

Run:

```powershell
python C:\Users\22730\.codex\skills\.system\skill-creator\scripts\quick_validate.py skills/build-character-panel
```

Expected: `Skill is valid!`

- [ ] **Step 5: Commit**

```powershell
git add skills/build-character-panel
git commit -m "feat: add evidence-aware character panel workflow"
```

### Task 4: Define the portable profile contract

**Files:**
- Create: `skills/build-character-panel/assets/character-profile.schema.json`
- Create: `skills/build-character-panel/assets/quick-panel-template.md`
- Create: `skills/build-character-panel/assets/full-panel-template.md`
- Create: `tests/fixtures/valid-profile.json`
- Create: `tests/fixtures/invalid-profile.json`
- Create: `tests/test_profile_model.py`

**Interfaces:**
- Consumes: The reference field semantics.
- Produces: JSON Schema version `1.0` and fixtures consumed by validator and renderer.

- [ ] **Step 1: Write failing model tests**

Tests import:

```python
from profile_model import load_profile, validate_profile
```

and assert that `validate_profile(data) -> list[str]` returns no errors for the valid fixture, rejects unsupported versions, rejects scores outside 0–100, rejects scored attributes without evidence, rejects invalid evidence states, and accepts `score: null` only with `confidence: "unknown"`.

- [ ] **Step 2: Verify red**

Run:

```powershell
python -m unittest tests.test_profile_model -v
```

Expected: import failure because `profile_model.py` does not exist.

- [ ] **Step 3: Add schema, templates, and fictional fixtures**

The schema must require:

```json
{
  "schema_version": "1.0",
  "profile": {},
  "domains": [],
  "core_attributes": [],
  "traits": [],
  "skills": [],
  "resources": [],
  "quests": [],
  "status_effects": [],
  "unknowns": [],
  "conflicts": [],
  "next_unlocks": [],
  "provenance": {},
  "version": {}
}
```

The valid fixture uses only the fictional person `Lin Qiao`.

- [ ] **Step 4: Keep red on missing implementation**

Re-run and confirm fixture parsing succeeds but function import still fails.

- [ ] **Step 5: Commit the contract and red tests**

```powershell
git add skills/build-character-panel/assets tests
git commit -m "test: define portable character profile contract"
```

### Task 5: Implement validation

**Files:**
- Create: `skills/build-character-panel/scripts/profile_model.py`
- Create: `skills/build-character-panel/scripts/validate_profile.py`

**Interfaces:**
- Produces: `load_profile(path: str | Path) -> dict`, `validate_profile(data: object) -> list[str]`, and CLI exit `0` for valid / `1` for invalid.

- [ ] **Step 1: Implement minimal recursive checks**

Use helpers:

```python
def require_mapping(value: object, path: str, errors: list[str]) -> dict | None: ...
def require_list(value: object, path: str, errors: list[str]) -> list | None: ...
def validate_evidence(items: object, path: str, errors: list[str]) -> None: ...
def validate_profile(data: object) -> list[str]: ...
```

Every error must include a JSON-style path such as `$.core_attributes[0].evidence`.

- [ ] **Step 2: Verify model tests green**

Run:

```powershell
python -m unittest tests.test_profile_model -v
```

Expected: all tests pass.

- [ ] **Step 3: Add CLI behavior test before finishing the command**

Assert valid output contains `VALID`, invalid output contains at least one path, and exit codes are exact.

- [ ] **Step 4: Verify CLI red then green**

Run:

```powershell
python -m unittest tests.test_cli.ValidateCliTests -v
```

Expected final state: all validator CLI tests pass.

- [ ] **Step 5: Commit**

```powershell
git add skills/build-character-panel/scripts tests
git commit -m "feat: validate character profile JSON"
```

### Task 6: Implement deterministic rendering

**Files:**
- Modify: `skills/build-character-panel/scripts/profile_model.py`
- Create: `skills/build-character-panel/scripts/render_panel.py`
- Modify: `tests/test_cli.py`

**Interfaces:**
- Produces: `render_panel(data: dict) -> str` and CLI `render_panel.py INPUT [-o OUTPUT]`.

- [ ] **Step 1: Write failing renderer tests**

Assert the valid fixture renders stable headings, display name, archetype, attribute score/confidence/evidence, quests, unknowns, provenance, and version. Assert Chinese profiles use Chinese headings and invalid profiles do not render.

- [ ] **Step 2: Verify red**

Run:

```powershell
python -m unittest tests.test_cli.RenderCliTests -v
```

Expected: failure because `render_panel.py` does not exist.

- [ ] **Step 3: Implement validation-first rendering**

Rendering must call `validate_profile` first, escape Markdown table pipes, use `—` for explicit missing display values, and preserve deterministic source ordering.

- [ ] **Step 4: Verify green and refactor**

Run:

```powershell
python -m unittest tests.test_cli -v
```

Expected: all CLI tests pass with no traceback.

- [ ] **Step 5: Commit**

```powershell
git add skills/build-character-panel/scripts tests/test_cli.py
git commit -m "feat: render character panels from JSON"
```

### Task 7: Add the canonical example and repository documentation

**Files:**
- Create: `skills/build-character-panel/references/example.md`
- Create: `README.md`
- Create: `LICENSE`
- Modify: `tests/test_package.py`

**Interfaces:**
- Consumes: Valid fixture and renderer output.
- Produces: One end-to-end fictional example and public installation instructions.

- [ ] **Step 1: Extend package tests**

Assert the example contains all required panel sections, uses only the fictional identity, and the README documents Codex installation, direct Skill use, validator use, renderer use, privacy behavior, and repository layout.

- [ ] **Step 2: Verify red**

Run:

```powershell
python -m unittest tests.test_package -v
```

Expected: failure because documentation files are missing.

- [ ] **Step 3: Generate example output**

Run:

```powershell
python skills/build-character-panel/scripts/render_panel.py tests/fixtures/valid-profile.json
```

Use that stable output as the core of `references/example.md`, followed by concise notes about why claims and scores are supported.

- [ ] **Step 4: Verify green**

Run the package test and official Skill validator.

- [ ] **Step 5: Commit**

```powershell
git add README.md LICENSE skills/build-character-panel/references/example.md tests/test_package.py
git commit -m "docs: add character panel usage and example"
```

### Task 8: Forward-test and close gaps

**Files:**
- Create: `evaluations/forward-tests.md`
- Modify only if evidence requires it: files under `skills/build-character-panel/`

**Interfaces:**
- Consumes: Fresh-context sparse, deep, update, and privacy-sensitive prompts.
- Produces: Verbatim forward-test results and targeted fixes tied to observed failures.

- [ ] **Step 1: Run fresh-context prompts with the Skill**

Do not tell test agents the intended output. Point them to the Skill and give only each user request plus fictional input.

- [ ] **Step 2: Compare against baseline**

Score presence of evidence states, unknowns, separate confidence, conflict preservation, no-question fallback, privacy restraint, and next actions.

- [ ] **Step 3: Add a failing regression test for each concrete gap**

Use package tests for missing guidance, model tests for contract errors, or CLI tests for rendering errors.

- [ ] **Step 4: Apply minimal fixes and re-run**

Run the affected test first, then the full suite.

- [ ] **Step 5: Commit**

```powershell
git add evaluations/forward-tests.md skills tests
git commit -m "test: forward-test character panel skill"
```

### Task 9: Final verification and publication

**Files:**
- Create for local delivery: `outputs/build-character-panel-skill.zip`

**Interfaces:**
- Consumes: Complete repository.
- Produces: Verified commit, GitHub repository URL when authentication exists, and local ZIP fallback.

- [ ] **Step 1: Run complete verification**

```powershell
python -m unittest discover -s tests -v
python C:\Users\22730\.codex\skills\.system\skill-creator\scripts\quick_validate.py skills/build-character-panel
rg -n "TBD|TODO|implement later|fill in details|example_placeholder" . -g "!docs/superpowers/plans/*"
git status -sb
git diff --check
```

Expected: all tests pass, `Skill is valid!`, placeholder search has no matches, no whitespace errors, and only the intentional ZIP remains untracked or ignored.

- [ ] **Step 2: Create reproducible ZIP**

Archive `skills/build-character-panel` so the archive root is the Skill folder and list archive contents to verify.

- [ ] **Step 3: Commit final metadata**

Commit any remaining intentional repository files after re-running relevant checks.

- [ ] **Step 4: Publish**

If a GitHub account/repository is connected, create or select the user-owned repository `build-character-panel-skill`, add `origin`, and push `main`. If no GitHub account is connected, do not fabricate success; retain the complete local repository and ZIP and report the exact authentication blocker.

- [ ] **Step 5: Verify remote**

Fetch repository metadata and the pushed commit SHA, then compare it with local `HEAD`.

## Plan self-review

- Spec coverage: every product mode, domain, evidence state, safety rule, output type, deterministic command, test phase, and publication requirement maps to a task above.
- Placeholder scan: the implementation steps contain exact paths, interfaces, commands, and expected outcomes; no implementation work is deferred.
- Type consistency: `load_profile`, `validate_profile`, and `render_panel` have one signature each and are consumed consistently by the CLIs and tests.
- Scope: this is one distributable Skill with two small support commands, not multiple independent products.
