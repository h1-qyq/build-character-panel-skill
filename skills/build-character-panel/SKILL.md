---
name: build-character-panel
description: Use when a user wants to define, understand, gamify, document, or update a real person's identity or personal information as an RPG character sheet, character panel, persona card, stats profile, skills inventory, life dashboard, or growth record.
---

# Build Character Panel

## Overview

Turn user-authorized information into an RPG-style character panel that is vivid without pretending guesses are facts. Preserve the game feel through attributes, skills, equipment, quests, buffs, debuffs, and unlocks; preserve trust through evidence states, confidence, unknowns, conflicts, and privacy control.

## Core contract

Build the panel in this order:

1. detect the operating mode;
2. inventory available evidence;
3. select quick or full depth;
4. resolve only blocking gaps;
5. model claims, attributes, skills, and quests;
6. run privacy and evidence checks;
7. render the requested format;
8. end with useful next unlocks.

Match the user's language. Treat game labels as presentation, not as permission to invent biography, ability, health, personality, family, finances, or motives.

## Select a mode

| Observable request | Mode | Default action |
|---|---|---|
| Sparse self-description or “make me a panel” | Quick scan | Use available facts, then show unknowns |
| “Interview me,” “complete,” or “deep profile” | Deep build | Ask one high-yield question at a time |
| Existing panel plus new information | Update | Preserve history and isolate affected fields |
| Resume, biography, notes, or chat supplied | Source conversion | Extract before asking anything |
| User forbids questions or is unavailable | No-question fallback | Produce a partial panel and “next unlocks” |

Read [interview-guide.md](references/interview-guide.md) when selecting questions, merging a prior panel, or handling the no-question fallback.

## Inventory evidence first

Create a private working ledger before drafting:

```text
claim | domain | state | source | confidence | display permission
```

Assign every material claim exactly one state:

- `stated`: directly supplied by the person or an explicitly identified source;
- `observed`: directly visible in a supplied artifact;
- `inferred`: conservative interpretation with a visible rationale;
- `unknown`: not supported;
- `conflicted`: sources disagree or old and new claims cannot both stand.

Never silently turn `unknown` into `0`, `50`, “average,” a personality label, or decorative lore. Keep old and new evidence when a claim is `conflicted`.

Read [evidence-and-scoring.md](references/evidence-and-scoring.md) before assigning numeric scores, confidence, sensitive claims, or conflict resolutions.

## Choose depth

### Quick panel

Use the compact shape when the user supplied little information or asked for speed:

1. identity, archetype, current chapter;
2. supported core attributes;
3. signature traits, values, and skills;
4. available equipment/resources;
5. active quest and next action;
6. current buffs/debuffs only when supported;
7. unknowns and next unlocks;
8. provenance and version.

Do not force all 18 domains into the visible response. Track uncovered domains as unknowns.

### Full panel

Cover all 18 domains and mark each `known`, `partial`, `unknown`, or `conflicted`. Read [attribute-system.md](references/attribute-system.md) for field meanings and neutral core attributes. Use [full-panel-template.md](assets/full-panel-template.md) as the visible structure.

## Ask only when useful

Use supplied material before asking questions. A question is justified only when its answer would materially change the panel or the user's next action.

- Ask one question at a time in deep build.
- Prefer a concrete recent example over self-rating.
- Ask at most five questions before returning a first quick panel.
- Never repeat an answer already present in the sources.
- When the user says “不要问,” “直接做,” “do not ask,” is asleep, or is unavailable, use the **no-question fallback**: deliver the best supported panel now, make gaps visible, and list up to five high-value next unlocks. Do not block.

## Model the character

### Attributes

Use only attributes relevant to available evidence. The neutral default set is `vitality`, `focus`, `learning`, `craft`, `agency`, `social`, and `resilience`.

A numeric attribute requires:

```text
score + confidence + at least one evidence item + one-sentence rationale
```

Use `score: unknown` when evidence cannot support an anchor. Confidence measures evidence quality, not the person's worth.

### Skills

Name a specific demonstrated capability. Include level, confidence, evidence, and next unlock condition. Distinguish:

- knowledge from repeated performance;
- one success from reliable skill;
- interest from ability;
- tool access from tool mastery;
- lack of evidence from lack of ability.

### Traits and values

Write behavioral patterns, not diagnoses. Use conditional language for `inferred` traits and show the evidence. Keep values and boundaries separate from personality.

### Equipment and resources

Include only authorized tools, credentials, networks, time, capital, environments, or reusable assets. Describe constraints as constraints, not moral defects.

### Quests

Turn explicit goals into playable quests:

```text
outcome | stakes | status | next action | blocker | success signal
```

Never invent a goal merely to fill a quest slot. Offer a proposed quest only when clearly labeled `inferred`.

### Status effects

Use buffs, debuffs, and mixed effects for temporary or context-dependent conditions. Do not convert a temporary state into a stable trait.

## Handle updates

When updating an existing panel:

1. retain the prior version and source date;
2. add new evidence without erasing the old record;
3. mark incompatible claims `conflicted`;
4. recalculate only affected ratings;
5. remove an unsupported score rather than replacing it with a new guess;
6. add a concise change log explaining what changed and why.

## Run the privacy pass

Before displaying the panel:

- exclude private details that do not serve the user's request;
- do not infer protected or highly sensitive attributes;
- do not diagnose mental or medical conditions;
- do not infer health or family situations from gaps in public activity;
- do not expose contact, payment, account, precise location, credential, or secret data;
- do not rank human worth or present the panel as an objective assessment;
- distinguish a fictional character inspired by a person from a factual profile of that person.

If a request asks for unsupported sensitive inference, decline that inference briefly and still produce a safe partial panel from supported facts.

## Render

Use the visible order in [output-contract.md](references/output-contract.md). For Markdown, start from [quick-panel-template.md](assets/quick-panel-template.md) or [full-panel-template.md](assets/full-panel-template.md). For portable data, conform to [character-profile.schema.json](assets/character-profile.schema.json).

If JSON is created, validate it:

```powershell
python scripts/validate_profile.py character-profile.json
```

Render validated JSON to stable Markdown:

```powershell
python scripts/render_panel.py character-profile.json -o character-panel.md
```

Read [example.md](references/example.md) only when a complete fictional example would materially help.

## Self-check before delivery

- Every material claim has a state.
- Every numeric score has evidence and separate confidence.
- No numeric performance score rests only on age, role, job title, intent, tool access, or a self-label.
- Unknowns are visible and are not numeric defaults.
- Conflicts preserve both sides and source labels.
- Temporary state is not presented as a stable trait.
- Sensitive details are absent unless clearly authorized and necessary.
- The first screen is useful; deep detail does not bury the main character read.
- Every active quest has a next action and success signal.
- The panel ends with provenance, version, and high-value next unlocks.

## Common mistakes

| Mistake | Correction |
|---|---|
| Making sparse input “feel complete” with invented lore | Use unknowns and next unlocks |
| Scoring every domain | Score only evidence-backed attributes |
| Treating age as level | Define level from milestones or leave it unranked |
| Calling anxiety, perfectionism, or burnout a diagnosis | Describe only supplied behavior or temporary context |
| Replacing a contradicted score with another guess | Mark conflict or remove the score |
| Asking a long intake form before showing value | Return a quick panel first |
| Refusing the entire request because one field is sensitive | Omit the unsafe inference and deliver the supported panel |
