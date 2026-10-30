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


DESCRIPTION = re.compile(r"(?ms)^description:\s*>-?\n((?:[ ]{2}.*\n?)+)")


def check_skill_metadata() -> list[str]:
    errors: list[str] = []
    for skill_root in SKILL_ROOTS:
        skill_path = skill_root / "SKILL.md"
        label = skill_path.relative_to(ROOT)
        parts = skill_path.read_text(encoding="utf-8").split("---", 2)
        frontmatter = parts[1] if len(parts) > 1 else ""
        name = SKILL_NAME.search(frontmatter)
        if skill_root != ROOT and (not name or name.group(1) != skill_root.name):
            errors.append(f"{label}: name must equal its directory name")
        description = DESCRIPTION.search(frontmatter)
        text = " ".join(line.strip() for line in description.group(1).splitlines()) if description else ""
        if not text:
            errors.append(f"{label}: description is missing")
        elif len(text) > 1024:
            errors.append(f"{label}: description is {len(text)} characters (limit 1024)")
        references = skill_root / "references"
        body = parts[2] if len(parts) > 2 else ""
        if references.is_dir():
            for reference in sorted(references.glob("*.md")):
                if reference.name not in body and reference.name not in "".join(
                    other.read_text(encoding="utf-8")
                    for other in references.glob("*.md")
                    if other != reference
                ):
                    errors.append(f"{reference.relative_to(ROOT)}: not linked from SKILL.md or another reference")
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


SKILL_ROOTS = (ROOT, ROOT / "skills/gtm-build-konvert")


def check_evaluations() -> list[str]:
    return [error for skill_root in SKILL_ROOTS for error in check_skill_evaluations(skill_root)]


def check_skill_evaluations(skill_root: Path) -> list[str]:
    errors: list[str] = []
    eval_path = skill_root / "evals/evals.json"
    skill_path = skill_root / "SKILL.md"
    eval_label = eval_path.relative_to(ROOT)
    data = json.loads(eval_path.read_text(encoding="utf-8"))
    frontmatter = skill_path.read_text(encoding="utf-8").split("---", 2)
    skill_match = SKILL_NAME.search(frontmatter[1] if len(frontmatter) > 1 else "")
    skill_name = skill_match.group(1) if skill_match else None

    if not skill_name or data.get("skill_name") != skill_name:
        errors.append(f"{eval_label}: skill_name does not match SKILL.md frontmatter")

    ids: set[int] = set()
    for index, item in enumerate(data.get("evals", [])):
        label = f"{eval_label}: eval index {index}"
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
        errors.append(f"{eval_label}: evaluation_type must disclose manual, unexecuted behavior criteria")
    return errors


def main() -> int:
    errors = check_markdown_links() + check_json_files() + check_skill_metadata() + check_evaluations()
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
