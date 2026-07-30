# Output Contract

Use this order for the default Markdown panel. Omit empty decorative sections; never omit unknowns, provenance, or version when they matter.

## Markdown order

1. `# Name · Archetype`
2. chapter, level system if defined, and completeness
3. core attribute table
4. signature traits, values, and boundaries
5. skill tree
6. equipment and resources
7. main and side quests
8. buffs, debuffs, and recovery
9. unknowns and conflicts
10. next unlocks
11. provenance and version

## Attribute row

```markdown
| Craft | 72/100 | Medium | Observed: three completed brand projects | Reliable in a bounded domain |
```

Use `Unknown` instead of a numeric placeholder.

## Claim annotation

Keep visible annotation compact:

```text
[S] stated
[O] observed
[I] inferred
[?] unknown
[!] conflicted
```

Explain the legend once. For public-facing panels, move annotations into a provenance appendix if the user prefers a cleaner surface.

## JSON top-level fields

Portable profiles use schema version `1.0`:

| Field | Purpose |
|---|---|
| `schema_version` | Contract compatibility |
| `profile` | Display identity, language, archetype, chapter, completeness |
| `domains` | All 18 coverage states for a full profile |
| `core_attributes` | Neutral or user-defined evidence-backed ratings |
| `traits` | Traits, values, preferences, and boundaries |
| `skills` | Demonstrated capabilities and next unlocks |
| `resources` | Equipment, assets, networks, time, and constraints |
| `quests` | Outcomes, status, next action, blocker, success signal |
| `status_effects` | Temporary buffs, debuffs, and mixed effects |
| `unknowns` | Explicit gaps |
| `conflicts` | Preserved incompatible accounts |
| `next_unlocks` | Highest-value optional evidence |
| `provenance` | Source labels, generation date, language |
| `version` | Profile version, update date, change summary |

Validate against `../assets/character-profile.schema.json` and with `../scripts/validate_profile.py`.

## Quality bar

The visible panel should:

- give one clear character read in the first screen;
- use tables only for comparable repeated fields;
- keep evidence concise but inspectable;
- distinguish descriptive snapshot from objective truth;
- make the next action easier to take;
- remain useful when most domains are unknown.
