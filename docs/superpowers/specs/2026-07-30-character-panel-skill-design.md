# Character Panel Skill Design

## Decision record

The user requested a complete, reusable Skill that turns a person's information into a game-style character panel, asked for direct GitHub publication, authorized all in-scope actions, and explicitly requested no interim questions. This design therefore records autonomous product decisions in place of interactive approval.

## Product approaches considered

### A. Exhaustive questionnaire

Collect every field before producing anything. This maximizes completeness but creates high abandonment risk, repeats questions when source material already contains answers, and delays the moment of value.

### B. Layered, evidence-aware character panel — selected

Produce a useful quick panel from available evidence, then deepen only the areas that matter. Separate stated facts, supported inferences, and unknowns. Attach confidence and evidence to ratings. This balances game feel, usefulness, honesty, privacy, and repeatability.

### C. Automated personality scoring

Infer numeric attributes immediately from sparse input. This is visually impressive but creates false precision, invites unsupported psychological claims, and can turn a playful panel into an untrustworthy assessment.

## Product promise

`build-character-panel` helps an agent organize information supplied by or about a user into a readable RPG-style character sheet. It supports sparse prompts, long autobiographical material, resumes, interview notes, and iterative updates. It never treats style as permission to invent facts.

## Primary use cases

1. “把我做成一个游戏人物面板。”
2. “根据这份自我介绍，整理我的属性、技能、天赋和任务线。”
3. “采访我，做一份完整的人物档案。”
4. “把我的旧面板根据这些新信息更新一下。”
5. “输出 Markdown 面板和可保存的 JSON。”

## Core modes

- **Quick scan:** Use existing material first. Ask at most five high-yield questions only when key gaps prevent a useful result.
- **Deep build:** Build a comprehensive profile across all domains with one focused question at a time.
- **Update:** Preserve supported existing facts, merge new evidence, mark conflicts, and recalculate only affected fields.
- **Source conversion:** Extract a panel from resumes, biographies, notes, chats, or other user-provided material without unnecessary interviewing.

When the user has explicitly asked not to be questioned, the agent must produce the best partial panel, label unknowns, and provide a compact “unlock next” list instead of blocking.

## Character model

The full panel covers:

1. identity and presentation;
2. current roles and life context;
3. origin story and formative events;
4. values, principles, and boundaries;
5. motives, needs, fears, and anti-goals;
6. personality and behavioral tendencies;
7. cognition, learning, and decision style;
8. communication and social style;
9. relationships, teams, and environments;
10. capabilities, knowledge, and craft skills;
11. habits, systems, energy, and health context;
12. resources, constraints, and leverage;
13. aesthetic identity and public image;
14. digital presence and reputation;
15. achievements, evidence, and unfinished arcs;
16. current quests, long-term missions, and next actions;
17. risks, blind spots, debuffs, and recovery strategies;
18. growth log, version, and change history.

The panel distinguishes:

- **Core attributes:** a small 0–100 overview with evidence-based confidence.
- **Skills:** named abilities with level, evidence, and next unlock condition.
- **Traits:** descriptive patterns, not diagnoses.
- **Equipment/resources:** tools, credentials, networks, capital, time, and environments.
- **Quests:** active outcomes with stakes, next action, blocker, and success signal.
- **Status effects:** temporary conditions explicitly separated from stable traits.

## Evidence and scoring contract

Every material claim is one of:

- `stated`: directly supplied by the user or source;
- `observed`: visible in supplied artifacts;
- `inferred`: a conservative interpretation with rationale;
- `unknown`: not supported yet;
- `conflicted`: sources disagree.

Numeric ratings require at least one piece of evidence. Ratings are descriptive snapshots, not objective measurements. The output must show confidence separately from score. Unknown values remain unknown; they are never silently converted to zero or fifty.

The system must not diagnose mental or medical conditions, infer protected or highly sensitive attributes, rank human worth, or expose private details the user did not ask to display.

## Output contract

The default response is a concise Markdown panel in this order:

1. title block and one-line archetype;
2. level and current chapter;
3. core attribute table;
4. signature traits and values;
5. skills and evidence;
6. equipment/resources;
7. quests;
8. buffs, debuffs, and recovery;
9. unknowns and contradictions;
10. next unlocks;
11. provenance note and version.

The Skill also provides:

- a full Markdown template;
- a compact Markdown template;
- a JSON Schema for portable structured profiles;
- a deterministic renderer from valid JSON to Markdown;
- a deterministic validator with actionable messages;
- bilingual guidance, with output language matching the user by default;
- a complete fictional example that demonstrates the contract without using real personal data.

## Architecture

The repository contains a distributable Skill at `skills/build-character-panel/`.

- `SKILL.md` contains only the trigger, core workflow, decision rules, privacy guardrails, and resource routing.
- `references/attribute-system.md` defines domains and field semantics.
- `references/interview-guide.md` defines question selection and the no-question fallback.
- `references/evidence-and-scoring.md` defines evidence states, score anchors, confidence, conflicts, and sensitive-data rules.
- `references/output-contract.md` defines Markdown and JSON output shapes.
- `references/example.md` provides one fictional end-to-end example.
- `assets/character-profile.schema.json` is the portable data contract.
- `assets/quick-panel-template.md` and `assets/full-panel-template.md` are reusable output templates.
- `scripts/validate_profile.py` validates JSON using only the Python standard library.
- `scripts/render_panel.py` renders valid profile JSON to Markdown.
- `tests/` verifies schema rules, validator behavior, renderer behavior, content completeness, and package structure.

## Error handling

- Sparse evidence yields an explicitly incomplete panel, never fabricated detail.
- Contradictions remain visible with source labels until resolved.
- Invalid JSON produces path-specific validation errors and a non-zero exit code.
- Unsupported schema versions fail closed with an upgrade hint.
- Rendering first validates input, preventing malformed panels.
- Sensitive details are summarized or omitted unless the user explicitly requests inclusion.

## Testing strategy

1. Run realistic prompts without the Skill and record omissions or unsupported inference.
2. Add content tests that fail before the Skill exists.
3. Implement validator and renderer through red-green-refactor.
4. Run fresh-context forward tests with the Skill on sparse, rich, update, and privacy-sensitive scenarios.
5. Validate the Skill with the official `quick_validate.py`.
6. Run the full standard-library test suite.
7. Search for placeholders and verify package paths and metadata.
8. Inspect the final Git diff and remote commit after publication.

## Success criteria

- A user can get a useful panel from one paragraph without mandatory questioning.
- A deep profile covers all 18 domains without presenting unknowns as facts.
- Every numeric score has evidence and separate confidence.
- The JSON validator rejects missing evidence, invalid ranges, and unknown schema versions.
- The renderer creates stable, readable Markdown from valid JSON.
- The Skill passes official validation and all repository tests.
- The repository contains no placeholder text or real personal data.
- The final verified commit is available in the user's accessible GitHub account, or the local deliverable clearly records the external authentication blocker if no account is connected.
