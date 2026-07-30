#!/usr/bin/env python3
"""Load and validate portable character profile JSON without third-party packages."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "1.0"
EVIDENCE_STATES = {"stated", "observed", "inferred", "unknown", "conflicted"}
CONFIDENCE_LEVELS = {"low", "medium", "high", "unknown"}
DOMAIN_STATUSES = {"known", "partial", "unknown", "conflicted"}
DOMAIN_IDS = {
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
}
TOP_LEVEL_FIELDS = {
    "schema_version",
    "profile",
    "domains",
    "core_attributes",
    "traits",
    "skills",
    "resources",
    "quests",
    "status_effects",
    "unknowns",
    "conflicts",
    "next_unlocks",
    "provenance",
    "version",
}


def load_profile(path: str | Path) -> dict[str, Any]:
    """Load a UTF-8 JSON profile from path."""
    with Path(path).open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("Profile root must be a JSON object")
    return data


def require_mapping(
    value: object, path: str, errors: list[str]
) -> dict[str, Any] | None:
    if not isinstance(value, dict):
        errors.append(f"{path}: expected an object")
        return None
    return value


def require_list(value: object, path: str, errors: list[str]) -> list[Any] | None:
    if not isinstance(value, list):
        errors.append(f"{path}: expected an array")
        return None
    return value


def require_string(
    value: object,
    path: str,
    errors: list[str],
    *,
    allow_empty: bool = False,
    allow_null: bool = False,
) -> str | None:
    if value is None and allow_null:
        return None
    if not isinstance(value, str):
        errors.append(f"{path}: expected a string")
        return None
    if not allow_empty and not value.strip():
        errors.append(f"{path}: must not be empty")
    return value


def require_fields(
    mapping: dict[str, Any], fields: set[str], path: str, errors: list[str]
) -> None:
    for field in sorted(fields):
        if field not in mapping:
            errors.append(f"{path}.{field}: required field is missing")


def validate_iso_datetime(value: object, path: str, errors: list[str]) -> None:
    text = require_string(value, path, errors)
    if text is None:
        return
    try:
        datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        errors.append(f"{path}: expected an ISO 8601 date-time")


def validate_evidence(items: object, path: str, errors: list[str]) -> None:
    evidence = require_list(items, path, errors)
    if evidence is None:
        return
    for index, raw_item in enumerate(evidence):
        item_path = f"{path}[{index}]"
        item = require_mapping(raw_item, item_path, errors)
        if item is None:
            continue
        require_fields(item, {"state", "summary", "source"}, item_path, errors)
        state = item.get("state")
        if state not in EVIDENCE_STATES:
            errors.append(
                f"{item_path}.state: expected one of {sorted(EVIDENCE_STATES)}"
            )
        require_string(item.get("summary"), f"{item_path}.summary", errors)
        require_string(item.get("source"), f"{item_path}.source", errors)


def validate_profile(data: object) -> list[str]:
    """Return path-specific validation errors; an empty list means valid."""
    errors: list[str] = []
    root = require_mapping(data, "$", errors)
    if root is None:
        return errors

    require_fields(root, TOP_LEVEL_FIELDS, "$", errors)
    for extra in sorted(set(root) - TOP_LEVEL_FIELDS):
        errors.append(f"$.{extra}: unexpected top-level field")

    if root.get("schema_version") != SCHEMA_VERSION:
        errors.append(
            f"$.schema_version: expected {SCHEMA_VERSION!r}; "
            f"got {root.get('schema_version')!r}"
        )

    _validate_profile_header(root.get("profile"), "$.profile", errors)
    _validate_domains(root.get("domains"), root.get("profile"), errors)
    _validate_attributes(root.get("core_attributes"), errors)
    _validate_traits(root.get("traits"), errors)
    _validate_skills(root.get("skills"), errors)
    _validate_resources(root.get("resources"), errors)
    _validate_quests(root.get("quests"), errors)
    _validate_status_effects(root.get("status_effects"), errors)
    _validate_string_list(root.get("unknowns"), "$.unknowns", errors)
    _validate_conflicts(root.get("conflicts"), errors)
    _validate_string_list(root.get("next_unlocks"), "$.next_unlocks", errors)
    _validate_provenance(root.get("provenance"), errors)
    _validate_version(root.get("version"), errors)
    return errors


def _validate_profile_header(value: object, path: str, errors: list[str]) -> None:
    profile = require_mapping(value, path, errors)
    if profile is None:
        return
    required = {
        "display_name",
        "language",
        "archetype",
        "current_chapter",
        "completeness",
    }
    require_fields(profile, required, path, errors)
    require_string(profile.get("display_name"), f"{path}.display_name", errors)
    require_string(profile.get("language"), f"{path}.language", errors)
    require_string(
        profile.get("archetype"), f"{path}.archetype", errors, allow_null=True
    )
    require_string(
        profile.get("current_chapter"),
        f"{path}.current_chapter",
        errors,
        allow_null=True,
    )
    if profile.get("completeness") not in {"quick", "full"}:
        errors.append(f"{path}.completeness: expected 'quick' or 'full'")


def _validate_domains(
    value: object, profile_value: object, errors: list[str]
) -> None:
    domains = require_list(value, "$.domains", errors)
    if domains is None:
        return
    seen: set[str] = set()
    for index, raw_item in enumerate(domains):
        path = f"$.domains[{index}]"
        item = require_mapping(raw_item, path, errors)
        if item is None:
            continue
        require_fields(item, {"id", "status", "summary", "evidence"}, path, errors)
        domain_id = item.get("id")
        if domain_id not in DOMAIN_IDS:
            errors.append(f"{path}.id: unknown domain {domain_id!r}")
        elif domain_id in seen:
            errors.append(f"{path}.id: duplicate domain {domain_id!r}")
        else:
            seen.add(domain_id)
        if item.get("status") not in DOMAIN_STATUSES:
            errors.append(
                f"{path}.status: expected one of {sorted(DOMAIN_STATUSES)}"
            )
        require_string(
            item.get("summary"), f"{path}.summary", errors, allow_null=True
        )
        validate_evidence(item.get("evidence"), f"{path}.evidence", errors)
        if item.get("status") == "unknown" and item.get("summary") is not None:
            errors.append(f"{path}.summary: unknown domains must use null")
    profile = profile_value if isinstance(profile_value, dict) else {}
    if profile.get("completeness") == "full":
        missing = sorted(DOMAIN_IDS - seen)
        if missing:
            errors.append(
                "$.domains: full profiles must include all domains; "
                f"missing {', '.join(missing)}"
            )


def _validate_attributes(value: object, errors: list[str]) -> None:
    attributes = require_list(value, "$.core_attributes", errors)
    if attributes is None:
        return
    seen: set[str] = set()
    for index, raw_item in enumerate(attributes):
        path = f"$.core_attributes[{index}]"
        item = require_mapping(raw_item, path, errors)
        if item is None:
            continue
        require_fields(
            item,
            {"id", "name", "score", "confidence", "evidence", "rationale"},
            path,
            errors,
        )
        attribute_id = require_string(item.get("id"), f"{path}.id", errors)
        if attribute_id:
            if attribute_id in seen:
                errors.append(f"{path}.id: duplicate attribute {attribute_id!r}")
            seen.add(attribute_id)
        require_string(item.get("name"), f"{path}.name", errors)
        require_string(
            item.get("rationale"), f"{path}.rationale", errors, allow_empty=True
        )
        score = item.get("score")
        confidence = item.get("confidence")
        if confidence not in CONFIDENCE_LEVELS:
            errors.append(
                f"{path}.confidence: expected one of {sorted(CONFIDENCE_LEVELS)}"
            )
        evidence = item.get("evidence")
        validate_evidence(evidence, f"{path}.evidence", errors)
        if score is None:
            if confidence != "unknown":
                errors.append(
                    f"{path}.confidence: a null score requires 'unknown' confidence"
                )
        elif isinstance(score, bool) or not isinstance(score, (int, float)):
            errors.append(f"{path}.score: expected a number or null")
        else:
            if not 0 <= score <= 100:
                errors.append(f"{path}.score: expected a value from 0 to 100")
            if confidence == "unknown":
                errors.append(
                    f"{path}.confidence: a numeric score requires known confidence"
                )
            if not isinstance(evidence, list) or not evidence:
                errors.append(
                    f"{path}.evidence: a numeric score requires at least one item"
                )


def _validate_traits(value: object, errors: list[str]) -> None:
    _validate_claim_items(
        value,
        "$.traits",
        {"name", "kind", "summary", "confidence", "evidence"},
        errors,
        enum_fields={
            "kind": {"trait", "value", "preference", "boundary"},
            "confidence": CONFIDENCE_LEVELS,
        },
    )


def _validate_skills(value: object, errors: list[str]) -> None:
    items = require_list(value, "$.skills", errors)
    if items is None:
        return
    for index, raw_item in enumerate(items):
        path = f"$.skills[{index}]"
        item = require_mapping(raw_item, path, errors)
        if item is None:
            continue
        require_fields(
            item, {"name", "level", "confidence", "evidence", "next_unlock"}, path, errors
        )
        require_string(item.get("name"), f"{path}.name", errors)
        level = item.get("level")
        if level is not None and (
            isinstance(level, bool) or not isinstance(level, int) or not 1 <= level <= 5
        ):
            errors.append(f"{path}.level: expected an integer from 1 to 5 or null")
        confidence = item.get("confidence")
        if confidence not in CONFIDENCE_LEVELS:
            errors.append(
                f"{path}.confidence: expected one of {sorted(CONFIDENCE_LEVELS)}"
            )
        evidence = item.get("evidence")
        validate_evidence(evidence, f"{path}.evidence", errors)
        if level is None and confidence != "unknown":
            errors.append(f"{path}.confidence: a null level requires 'unknown'")
        if level is not None and (not isinstance(evidence, list) or not evidence):
            errors.append(f"{path}.evidence: a level requires at least one item")
        require_string(
            item.get("next_unlock"),
            f"{path}.next_unlock",
            errors,
            allow_null=True,
        )


def _validate_resources(value: object, errors: list[str]) -> None:
    _validate_claim_items(
        value,
        "$.resources",
        {"name", "category", "summary", "evidence"},
        errors,
        enum_fields={
            "category": {
                "tool",
                "credential",
                "network",
                "time",
                "capital",
                "asset",
                "environment",
                "constraint",
            }
        },
    )


def _validate_quests(value: object, errors: list[str]) -> None:
    items = require_list(value, "$.quests", errors)
    if items is None:
        return
    for index, raw_item in enumerate(items):
        path = f"$.quests[{index}]"
        item = require_mapping(raw_item, path, errors)
        if item is None:
            continue
        required = {
            "title",
            "status",
            "stakes",
            "next_action",
            "blocker",
            "success_signal",
            "evidence",
        }
        require_fields(item, required, path, errors)
        for field in ("title", "stakes", "success_signal"):
            require_string(item.get(field), f"{path}.{field}", errors)
        status = item.get("status")
        if status not in {"active", "planned", "blocked", "complete"}:
            errors.append(f"{path}.status: invalid quest status")
        next_action = require_string(
            item.get("next_action"),
            f"{path}.next_action",
            errors,
            allow_null=True,
        )
        require_string(
            item.get("blocker"), f"{path}.blocker", errors, allow_null=True
        )
        if status == "active" and not next_action:
            errors.append(f"{path}.next_action: active quests require a next action")
        validate_evidence(item.get("evidence"), f"{path}.evidence", errors)


def _validate_status_effects(value: object, errors: list[str]) -> None:
    _validate_claim_items(
        value,
        "$.status_effects",
        {"name", "effect", "scope", "recovery", "evidence"},
        errors,
        enum_fields={"effect": {"buff", "debuff", "mixed"}},
        nullable_strings={"recovery"},
    )


def _validate_conflicts(value: object, errors: list[str]) -> None:
    items = require_list(value, "$.conflicts", errors)
    if items is None:
        return
    for index, raw_item in enumerate(items):
        path = f"$.conflicts[{index}]"
        item = require_mapping(raw_item, path, errors)
        if item is None:
            continue
        require_fields(item, {"topic", "accounts", "resolution"}, path, errors)
        require_string(item.get("topic"), f"{path}.topic", errors)
        accounts = require_list(item.get("accounts"), f"{path}.accounts", errors)
        if accounts is not None:
            if len(accounts) < 2:
                errors.append(f"{path}.accounts: expected at least two accounts")
            for account_index, account in enumerate(accounts):
                require_string(
                    account, f"{path}.accounts[{account_index}]", errors
                )
        require_string(
            item.get("resolution"), f"{path}.resolution", errors, allow_null=True
        )


def _validate_provenance(value: object, errors: list[str]) -> None:
    path = "$.provenance"
    item = require_mapping(value, path, errors)
    if item is None:
        return
    require_fields(item, {"generated_at", "language", "sources"}, path, errors)
    validate_iso_datetime(item.get("generated_at"), f"{path}.generated_at", errors)
    require_string(item.get("language"), f"{path}.language", errors)
    sources = require_list(item.get("sources"), f"{path}.sources", errors)
    if sources is None:
        return
    for index, raw_source in enumerate(sources):
        source_path = f"{path}.sources[{index}]"
        source = require_mapping(raw_source, source_path, errors)
        if source is None:
            continue
        require_fields(source, {"label", "kind"}, source_path, errors)
        require_string(source.get("label"), f"{source_path}.label", errors)
        if source.get("kind") not in {
            "user",
            "artifact",
            "interview",
            "prior-profile",
            "other",
        }:
            errors.append(f"{source_path}.kind: invalid source kind")


def _validate_version(value: object, errors: list[str]) -> None:
    path = "$.version"
    item = require_mapping(value, path, errors)
    if item is None:
        return
    require_fields(
        item, {"profile_version", "updated_at", "change_summary"}, path, errors
    )
    require_string(item.get("profile_version"), f"{path}.profile_version", errors)
    validate_iso_datetime(item.get("updated_at"), f"{path}.updated_at", errors)
    require_string(
        item.get("change_summary"),
        f"{path}.change_summary",
        errors,
        allow_empty=True,
    )


def _validate_string_list(value: object, path: str, errors: list[str]) -> None:
    items = require_list(value, path, errors)
    if items is None:
        return
    for index, item in enumerate(items):
        require_string(item, f"{path}[{index}]", errors)


def _validate_claim_items(
    value: object,
    path: str,
    required: set[str],
    errors: list[str],
    *,
    enum_fields: dict[str, set[str]],
    nullable_strings: set[str] | None = None,
) -> None:
    nullable_strings = nullable_strings or set()
    items = require_list(value, path, errors)
    if items is None:
        return
    for index, raw_item in enumerate(items):
        item_path = f"{path}[{index}]"
        item = require_mapping(raw_item, item_path, errors)
        if item is None:
            continue
        require_fields(item, required, item_path, errors)
        for field in required - {"evidence"} - set(enum_fields):
            require_string(
                item.get(field),
                f"{item_path}.{field}",
                errors,
                allow_null=field in nullable_strings,
            )
        for field, allowed in enum_fields.items():
            if item.get(field) not in allowed:
                errors.append(
                    f"{item_path}.{field}: expected one of {sorted(allowed)}"
                )
        validate_evidence(item.get("evidence"), f"{item_path}.evidence", errors)
