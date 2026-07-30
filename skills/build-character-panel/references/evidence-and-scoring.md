# Evidence and Scoring

Use this reference whenever a panel contains a claim, numeric score, confidence label, contradiction, or sensitive field.

## Evidence states

| State | Use when | Display pattern |
|---|---|---|
| `stated` | The person or named source said it directly | “User-stated…” |
| `observed` | A supplied artifact directly demonstrates it | “Observed in…” |
| `inferred` | Evidence supports a conservative interpretation | “Likely… because…” |
| `unknown` | No adequate support exists | “Unknown; unlock with…” |
| `conflicted` | Sources or contexts disagree materially | Show both claims and sources |

Do not upgrade `inferred` to `stated` during rewriting.

## Confidence

Confidence describes support for the claim, never the value of the person.

| Confidence | Anchor |
|---|---|
| `high` | Multiple independent, recent, specific evidence items or direct repeatable artifact |
| `medium` | One strong item or several consistent but indirect items |
| `low` | Sparse, old, context-limited, or inference-heavy evidence |
| `unknown` | No basis for a claim or score |

Source authority and recency matter only relative to the claim. First-person experience is authoritative for preference and felt state; an artifact may be stronger for artifact quality.

## Numeric scoring

Scores are optional snapshots. Use them only when they improve comparison, tracking, or prioritization.

### Universal 0–100 anchors

| Range | Meaning |
|---:|---|
| 0–19 | Evidence shows the capability is not yet available in the tested context |
| 20–39 | Early, inconsistent, or heavily supported performance |
| 40–59 | Functional in familiar bounded contexts |
| 60–79 | Reliable across meaningful variation |
| 80–94 | Advanced, repeated, high-quality performance |
| 95–100 | Exceptional sustained evidence across difficult contexts |

These anchors describe evidence-backed performance, not potential. Do not use extreme scores from adjectives alone.

A role or job title alone cannot support a numeric score. Age, intent, tool access, credentials, a self-label, or one unverified adjective also cannot establish a performance range. These facts may identify a relevant domain or unlock a skill slot, but the score stays unknown until an outcome, artifact, repeated example, or comparable observation meets an anchor.

Every scored attribute requires:

```json
{
  "score": 72,
  "confidence": "medium",
  "evidence": [
    {
      "state": "observed",
      "summary": "Completed three comparable projects",
      "source": "portfolio"
    }
  ],
  "rationale": "Repeated delivery supports reliable performance in a bounded domain."
}
```

If evidence is missing:

```json
{
  "score": null,
  "confidence": "unknown",
  "evidence": [],
  "rationale": "No performance evidence supplied."
}
```

Unknown is not zero and is not average.

## Inference rules

An inference must:

1. be necessary to the user's purpose;
2. name its evidence;
3. use conditional language;
4. remain easy to correct;
5. avoid protected or highly sensitive attributes.

Good:

> `inferred`, low confidence: External deadlines may improve follow-through; two client projects were delivered while an unstructured personal project stalled.

Bad:

> Execution 73. Perfectionist. Probably anxious.

## Conflict handling

Store both accounts:

```text
topic: public speaking
old: “expert speaker,” source unknown
new: “no public speaking experience; feels nervous on stage,” first-person, current
resolution: old score removed; ability remains unknown; current status effect recorded
```

Do not average contradictory scores. Re-score only when the resolved evidence meets an anchor.

## Sensitive-data boundary

Do not infer or expose:

- health or diagnoses;
- family circumstances;
- protected identity;
- precise finances, location, contact, account, payment, or credential data;
- intimate life or trauma;
- beliefs or affiliations not explicitly supplied for this purpose.

When sensitive context is voluntarily supplied, summarize only what is necessary and honor display permission. A private working fact is not automatically a public panel field.

## Privacy display levels

- `public`: safe for a public bio or shared panel;
- `private`: show only in the user's private version;
- `omit`: use neither in reasoning nor display unless necessary for immediate safety;
- `unspecified`: default to private for sensitive details.
