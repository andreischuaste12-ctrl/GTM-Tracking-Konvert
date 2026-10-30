#!/usr/bin/env python3
"""Validate local Markdown links, JSON files, and skill evaluation metadata."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
SKILL_NAME = re.compile(r"(?m)^name:\s*([a-z0-9-]+)\s*$")


def check_markdown_links() -> list[str]:
    errors: list[str] = []
    for source in sorted(ROOT.rglob("*.md")):
        if ".git" in source.parts:
            continue
        text = source.read_text(encoding="utf-8")
        for target in MARKDOWN_LINK.findall(text):
            target = target.strip().split(maxsplit=1)[0].strip("<>")
            if target.startswith(("https://", "http://", "mailto:", "#")):
                continue
            path = unquote(target.split("#", 1)[0].split("?", 1)[0])
            if path and not (source.parent / path).resolve().exists():
                errors.append(f"{source.relative_to(ROOT)}: missing local link target {path}")
    return errors


def check_json_files() -> list[str]:
    errors: list[str] = []
    for path in sorted(ROOT.rglob("*.json")):
        if ".git" in path.parts:
            continue
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{path.relative_to(ROOT)}: invalid JSON ({type(exc).__name__})")
    return errors


def check_evaluations() -> list[str]:
    errors: list[str] = []
    eval_path = ROOT / "evals/evals.json"
    skill_path = ROOT / "SKILL.md"
    data = json.loads(eval_path.read_text(encoding="utf-8"))
    frontmatter = skill_path.read_text(encoding="utf-8").split("---", 2)
    skill_match = SKILL_NAME.search(frontmatter[1] if len(frontmatter) > 1 else "")
    skill_name = skill_match.group(1) if skill_match else None

    if not skill_name or data.get("skill_name") != skill_name:
        errors.append("evals/evals.json: skill_name does not match SKILL.md frontmatter")

    ids: set[int] = set()
    for index, item in enumerate(data.get("evals", [])):
        label = f"evals/evals.json: eval index {index}"
        eval_id = item.get("id")
        if not isinstance(eval_id, int) or eval_id in ids:
            errors.append(f"{label} has a missing or duplicate integer id")
        else:
            ids.add(eval_id)
        if not isinstance(item.get("prompt"), str) or not item["prompt"].strip():
            errors.append(f"{label} has no prompt")
        assertions = item.get("assertions")
        if not isinstance(assertions, dict) or not all(
            isinstance(assertions.get(key), list) and assertions[key]
            for key in ("must_include", "must_not_claim")
        ):
            errors.append(f"{label} must define non-empty must_include and must_not_claim lists")
        for attached in item.get("files", []):
            if not isinstance(attached, str) or not (ROOT / attached).is_file():
                errors.append(f"{label} references a missing fixture")
    if data.get("evaluation_type") != "scenario_specification_with_manual_assertions_not_behaviorally_executed":
        errors.append("evals/evals.json: evaluation_type must disclose manual, unexecuted behavior criteria")
    return errors


def main() -> int:
    errors = check_markdown_links() + check_json_files() + check_evaluations()
    if errors:
        print("Documentation validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    markdown_count = sum(1 for _ in ROOT.rglob("*.md"))
    json_count = sum(1 for _ in ROOT.rglob("*.json"))
    print(f"Documentation validation passed ({markdown_count} Markdown files, {json_count} JSON files).")
    print("External vendor links are not checked by this local validator.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
