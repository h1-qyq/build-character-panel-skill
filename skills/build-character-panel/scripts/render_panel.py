#!/usr/bin/env python3
"""Render a validated character profile JSON file as deterministic Markdown."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from profile_model import load_profile, validate_profile


STATE_TAGS = {
    "stated": "S",
    "observed": "O",
    "inferred": "I",
    "unknown": "?",
    "conflicted": "!",
}

EN = {
    "unranked": "Unranked",
    "unknown": "Unknown",
    "completeness": "Completeness",
    "version": "Version",
    "level": "Level",
    "chapter": "Current chapter",
    "attributes": "Core attributes",
    "attribute": "Attribute",
    "score": "Score",
    "confidence": "Confidence",
    "evidence": "Evidence",
    "rationale": "Rationale",
    "domains": "Domain map",
    "domain": "Domain",
    "coverage": "Coverage",
    "summary": "Summary",
    "traits": "Traits, values, preferences, and boundaries",
    "skills": "Skill tree",
    "skill": "Skill",
    "skill_level": "Level",
    "next_unlock": "Next unlock",
    "resources": "Equipment and resources",
    "quests": "Quests",
    "status_effects": "Buffs, debuffs, and recovery",
    "stakes": "Stakes",
    "status": "Status",
    "next_action": "Next action",
    "blocker": "Blocker",
    "success_signal": "Success signal",
    "recovery": "Recovery",
    "unknowns": "Unknowns",
    "conflicts": "Conflicts",
    "resolution": "Resolution",
    "next_unlocks": "Next unlocks",
    "provenance": "Provenance and version",
    "sources": "Sources",
    "generated": "Generated",
    "updated": "Updated",
    "change": "Change",
    "legend": "Evidence legend",
    "none": "None recorded",
}

ZH = {
    "unranked": "未评级",
    "unknown": "未知",
    "completeness": "完整度",
    "version": "版本",
    "level": "等级",
    "chapter": "当前章节",
    "attributes": "核心属性",
    "attribute": "属性",
    "score": "分数",
    "confidence": "置信度",
    "evidence": "证据",
    "rationale": "判断",
    "domains": "领域地图",
    "domain": "领域",
    "coverage": "覆盖状态",
    "summary": "摘要",
    "traits": "特质、价值、偏好与边界",
    "skills": "技能树",
    "skill": "技能",
    "skill_level": "等级",
    "next_unlock": "下一解锁",
    "resources": "装备与资源",
    "quests": "任务线",
    "status_effects": "增益、减益与恢复",
    "stakes": "意义",
    "status": "状态",
    "next_action": "下一步",
    "blocker": "阻碍",
    "success_signal": "完成信号",
    "recovery": "恢复策略",
    "unknowns": "未知项",
    "conflicts": "冲突项",
    "resolution": "处理",
    "next_unlocks": "下一解锁",
    "provenance": "来源与版本",
    "sources": "来源",
    "generated": "生成时间",
    "updated": "更新时间",
    "change": "变更",
    "legend": "证据图例",
    "none": "暂无记录",
}

CONFIDENCE_EN = {
    "low": "Low",
    "medium": "Medium",
    "high": "High",
    "unknown": "Unknown",
}
CONFIDENCE_ZH = {
    "low": "低",
    "medium": "中",
    "high": "高",
    "unknown": "未知",
}


class ProfileValidationError(ValueError):
    """Raised when rendering is requested for an invalid profile."""

    def __init__(self, errors: list[str]):
        super().__init__("Profile is invalid")
        self.errors = errors


def markdown_text(value: object, fallback: str = "—") -> str:
    if value is None or value == "":
        return fallback
    return str(value).replace("\\", "\\\\").replace("|", "\\|").replace("\n", " ")


def evidence_text(items: list[dict[str, Any]]) -> str:
    if not items:
        return "—"
    rendered: list[str] = []
    for item in items:
        tag = STATE_TAGS.get(item.get("state"), "?")
        summary = markdown_text(item.get("summary"))
        source = markdown_text(item.get("source"))
        rendered.append(f"[{tag}] {summary} ({source})")
    return "; ".join(rendered)


def render_panel(data: dict[str, Any]) -> str:
    """Validate and render profile data as Markdown."""
    errors = validate_profile(data)
    if errors:
        raise ProfileValidationError(errors)

    profile = data["profile"]
    language = str(profile.get("language", "en")).lower()
    is_zh = language.startswith("zh")
    labels = ZH if is_zh else EN
    confidence_labels = CONFIDENCE_ZH if is_zh else CONFIDENCE_EN
    unknown = labels["unknown"]
    lines: list[str] = []

    name = markdown_text(profile["display_name"])
    archetype = markdown_text(profile.get("archetype"), unknown)
    lines.append(f"# {name} · {archetype}")
    lines.append("")
    chapter = markdown_text(profile.get("current_chapter"), unknown)
    lines.append(f"> **{labels['chapter']}:** {chapter}")
    lines.append("")
    level = markdown_text(profile.get("level"), labels["unranked"])
    level_system = profile.get("level_system")
    level_display = (
        f"{level} ({markdown_text(level_system)})" if level_system else level
    )
    completeness = markdown_text(profile.get("completeness")).title()
    lines.append(
        f"**{labels['level']}:** {level_display} · "
        f"**{labels['completeness']}:** {completeness} · "
        f"**{labels['version']}:** {markdown_text(data['version']['profile_version'])}"
    )

    _render_attributes(
        lines, data["core_attributes"], labels, confidence_labels, unknown
    )
    if profile.get("completeness") == "full":
        _render_domains(lines, data["domains"], labels, unknown)
    _render_traits(lines, data["traits"], labels, confidence_labels)
    _render_skills(lines, data["skills"], labels, confidence_labels, unknown)
    _render_resources(lines, data["resources"], labels)
    _render_quests(lines, data["quests"], labels)
    _render_status_effects(lines, data["status_effects"], labels)
    _render_bullets(lines, labels["unknowns"], data["unknowns"], labels["none"])
    _render_conflicts(lines, data["conflicts"], labels)
    _render_bullets(
        lines, labels["next_unlocks"], data["next_unlocks"], labels["none"]
    )
    _render_provenance(lines, data, labels)
    lines.append("")
    lines.append(
        f"*{labels['legend']}: [S] stated · [O] observed · "
        "[I] inferred · [?] unknown · [!] conflicted*"
    )
    return "\n".join(lines).rstrip() + "\n"


def _render_attributes(
    lines: list[str],
    items: list[dict[str, Any]],
    labels: dict[str, str],
    confidence_labels: dict[str, str],
    unknown: str,
) -> None:
    lines.extend(
        [
            "",
            f"## {labels['attributes']}",
            "",
            f"| {labels['attribute']} | {labels['score']} | "
            f"{labels['confidence']} | {labels['evidence']} | {labels['rationale']} |",
            "|---|---:|---|---|---|",
        ]
    )
    if not items:
        lines.append(f"| {unknown} | {unknown} | {unknown} | — | — |")
        return
    for item in items:
        score = (
            f"{item['score']:g}/100" if item.get("score") is not None else unknown
        )
        confidence = confidence_labels[item["confidence"]]
        lines.append(
            f"| {markdown_text(item['name'])} | {score} | {confidence} | "
            f"{evidence_text(item['evidence'])} | "
            f"{markdown_text(item['rationale'])} |"
        )


def _render_domains(
    lines: list[str],
    items: list[dict[str, Any]],
    labels: dict[str, str],
    unknown: str,
) -> None:
    lines.extend(
        [
            "",
            f"## {labels['domains']}",
            "",
            f"| {labels['domain']} | {labels['coverage']} | {labels['summary']} |",
            "|---|---|---|",
        ]
    )
    for item in items:
        lines.append(
            f"| `{markdown_text(item['id'])}` | {markdown_text(item['status'])} | "
            f"{markdown_text(item.get('summary'), unknown)} |"
        )


def _render_traits(
    lines: list[str],
    items: list[dict[str, Any]],
    labels: dict[str, str],
    confidence_labels: dict[str, str],
) -> None:
    lines.extend(["", f"## {labels['traits']}", ""])
    if not items:
        lines.append(f"- {labels['none']}")
        return
    for item in items:
        lines.append(
            f"- **{markdown_text(item['kind'])} · {markdown_text(item['name'])}:** "
            f"{markdown_text(item['summary'])} — "
            f"{confidence_labels[item['confidence']]}; "
            f"{evidence_text(item['evidence'])}"
        )


def _render_skills(
    lines: list[str],
    items: list[dict[str, Any]],
    labels: dict[str, str],
    confidence_labels: dict[str, str],
    unknown: str,
) -> None:
    lines.extend(
        [
            "",
            f"## {labels['skills']}",
            "",
            f"| {labels['skill']} | {labels['skill_level']} | "
            f"{labels['confidence']} | {labels['evidence']} | "
            f"{labels['next_unlock']} |",
            "|---|---:|---|---|---|",
        ]
    )
    if not items:
        lines.append(f"| {unknown} | {unknown} | {unknown} | — | — |")
        return
    for item in items:
        level = item.get("level") if item.get("level") is not None else unknown
        lines.append(
            f"| {markdown_text(item['name'])} | {level} | "
            f"{confidence_labels[item['confidence']]} | "
            f"{evidence_text(item['evidence'])} | "
            f"{markdown_text(item.get('next_unlock'), unknown)} |"
        )


def _render_resources(
    lines: list[str], items: list[dict[str, Any]], labels: dict[str, str]
) -> None:
    lines.extend(["", f"## {labels['resources']}", ""])
    if not items:
        lines.append(f"- {labels['none']}")
        return
    for item in items:
        lines.append(
            f"- **{markdown_text(item['category'])} · {markdown_text(item['name'])}:** "
            f"{markdown_text(item['summary'])} — {evidence_text(item['evidence'])}"
        )


def _render_quests(
    lines: list[str], items: list[dict[str, Any]], labels: dict[str, str]
) -> None:
    lines.extend(["", f"## {labels['quests']}", ""])
    if not items:
        lines.append(f"- {labels['none']}")
        return
    for item in items:
        lines.extend(
            [
                f"### {markdown_text(item['title'])}",
                "",
                f"- **{labels['status']}:** {markdown_text(item['status'])}",
                f"- **{labels['stakes']}:** {markdown_text(item['stakes'])}",
                f"- **{labels['next_action']}:** "
                f"{markdown_text(item.get('next_action'))}",
                f"- **{labels['blocker']}:** {markdown_text(item.get('blocker'))}",
                f"- **{labels['success_signal']}:** "
                f"{markdown_text(item['success_signal'])}",
                f"- **{labels['evidence']}:** {evidence_text(item['evidence'])}",
                "",
            ]
        )
    if lines[-1] == "":
        lines.pop()


def _render_status_effects(
    lines: list[str], items: list[dict[str, Any]], labels: dict[str, str]
) -> None:
    lines.extend(["", f"## {labels['status_effects']}", ""])
    if not items:
        lines.append(f"- {labels['none']}")
        return
    for item in items:
        lines.append(
            f"- **{markdown_text(item['effect'])} · {markdown_text(item['name'])}:** "
            f"{markdown_text(item['scope'])} · **{labels['recovery']}:** "
            f"{markdown_text(item.get('recovery'))} · {evidence_text(item['evidence'])}"
        )


def _render_bullets(
    lines: list[str], heading: str, items: list[str], empty_text: str
) -> None:
    lines.extend(["", f"## {heading}", ""])
    if not items:
        lines.append(f"- {empty_text}")
        return
    lines.extend(f"- {markdown_text(item)}" for item in items)


def _render_conflicts(
    lines: list[str], items: list[dict[str, Any]], labels: dict[str, str]
) -> None:
    lines.extend(["", f"## {labels['conflicts']}", ""])
    if not items:
        lines.append(f"- {labels['none']}")
        return
    for item in items:
        accounts = " ↔ ".join(markdown_text(account) for account in item["accounts"])
        lines.append(
            f"- **{markdown_text(item['topic'])}:** {accounts} · "
            f"**{labels['resolution']}:** {markdown_text(item.get('resolution'))}"
        )


def _render_provenance(
    lines: list[str], data: dict[str, Any], labels: dict[str, str]
) -> None:
    provenance = data["provenance"]
    version = data["version"]
    sources = ", ".join(
        markdown_text(source["label"]) for source in provenance["sources"]
    )
    lines.extend(
        [
            "",
            f"## {labels['provenance']}",
            "",
            f"- **{labels['sources']}:** {sources or labels['none']}",
            f"- **{labels['generated']}:** {markdown_text(provenance['generated_at'])}",
            f"- **{labels['updated']}:** {markdown_text(version['updated_at'])}",
            f"- **{labels['version']}:** {markdown_text(version['profile_version'])}",
            f"- **{labels['change']}:** {markdown_text(version['change_summary'])}",
        ]
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Render build-character-panel profile JSON as Markdown."
    )
    parser.add_argument("profile", type=Path, help="Path to a profile JSON file")
    parser.add_argument("-o", "--output", type=Path, help="Write Markdown to this path")
    return parser


def main(argv: list[str] | None = None) -> int:
    arguments = build_parser().parse_args(argv)
    try:
        profile = load_profile(arguments.profile)
        markdown = render_panel(profile)
    except ProfileValidationError as error:
        print(f"INVALID: {arguments.profile} ({len(error.errors)} error(s))", file=sys.stderr)
        for message in error.errors:
            print(f"- {message}", file=sys.stderr)
        return 1
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2

    if arguments.output:
        arguments.output.parent.mkdir(parents=True, exist_ok=True)
        arguments.output.write_text(markdown, encoding="utf-8", newline="\n")
        print(f"WROTE: {arguments.output}")
    else:
        sys.stdout.write(markdown)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
