#!/usr/bin/env python3
"""Generate a Markdown scoring sheet for a manual evaluation run of one skill's scenarios."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _commit() -> str:
    try:
        return subprocess.run(
            ["git", "-C", str(ROOT), "rev-parse", "--short", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def _fixture_hash(paths: list[str]) -> str:
    digest = hashlib.sha256()
    for relative in sorted(paths):
        digest.update((ROOT / relative).read_bytes())
    return digest.hexdigest()[:12] if paths else "none"


def render(data: dict) -> str:
    lines = [
        f"# Evaluation run: {data['skill_name']}",
        "",
        "Status: NOT EXECUTED until every field below is filled by a reviewer.",
        "",
        f"- Date prepared: {date.today().isoformat()}",
        f"- Skill commit: {_commit()}",
        "- Model/version: ",
        "- Evaluator: ",
        "- Skill enabled / disabled baseline run: ",
        "",
    ]
    for item in data["evals"]:
        lines += [
            f"## Scenario {item['id']}",
            "",
            f"Prompt: {item['prompt']}",
            f"Fixture hash: {_fixture_hash(item.get('files', []))}",
            "",
            "| Criterion | Type | Pass | Response excerpt |",
            "|---|---|---|---|",
        ]
        for kind in ("must_include", "must_not_claim"):
            for criterion in item["assertions"][kind]:
                lines.append(f"| {criterion} | {kind} | [ ] | |")
        lines += ["", "Failure notes: ", ""]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evals", type=Path, help="Path to an evals.json file")
    parser.add_argument("--output", type=Path, help="Write the sheet here instead of stdout")
    args = parser.parse_args()
    try:
        data = json.loads(args.evals.read_text(encoding="utf-8"))
        sheet = render(data)
    except (OSError, json.JSONDecodeError, KeyError) as exc:
        print(f"Unable to build sheet ({exc.__class__.__name__}).", file=sys.stderr)
        return 2
    if args.output:
        args.output.write_text(sheet + "\n", encoding="utf-8")
    else:
        print(sheet)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
