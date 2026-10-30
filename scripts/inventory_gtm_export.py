#!/usr/bin/env python3
"""Summarize a GTM JSON export without printing configuration values."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ENTITY_KEYS = (
    "tag",
    "trigger",
    "variable",
    "folder",
    "customTemplate",
    "builtInVariable",
)
TRIGGER_REFERENCE_KEYS = {"firingTriggerId", "blockingTriggerId", "triggerId", "triggerIds"}
FILTER_KEYS = {"customEventFilter", "filter"}


def _entity_list(version: dict[str, Any], key: str) -> list[dict[str, Any]]:
    value = version.get(key, [])
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def _walk(value: Any):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from _walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk(child)


def _values(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value if isinstance(item, (str, int))]
    if isinstance(value, (str, int)):
        return [str(value)]
    return []


def inventory(document: Any, raw_bytes: bytes) -> dict[str, Any]:
    if not isinstance(document, dict):
        raise ValueError("The JSON root must be an object.")

    version = document.get("containerVersion", document)
    if not isinstance(version, dict):
        raise ValueError("The containerVersion field must be an object.")

    entities = {key: _entity_list(version, key) for key in ENTITY_KEYS}
    counts = {key: len(items) for key, items in entities.items()}

    duplicate_ids = 0
    duplicate_names = 0
    for items in entities.values():
        ids = [str(item["tagId"] if "tagId" in item else item["triggerId"] if "triggerId" in item else item["variableId"] if "variableId" in item else item["folderId"] if "folderId" in item else item["templateId"] if "templateId" in item else item["builtInVariableId"] if "builtInVariableId" in item else "") for item in items]
        names = [item.get("name") for item in items if isinstance(item.get("name"), str)]
        duplicate_ids += sum(count - 1 for count in Counter(item for item in ids if item).values() if count > 1)
        duplicate_names += sum(count - 1 for count in Counter(names).values() if count > 1)

    triggers = entities["trigger"]
    trigger_ids = {str(item.get("triggerId")) for item in triggers if item.get("triggerId") is not None}
    referenced_ids: set[str] = set()
    for tag in entities["tag"]:
        for node in _walk(tag):
            for key in TRIGGER_REFERENCE_KEYS:
                referenced_ids.update(_values(node.get(key)))
    for trigger in triggers:
        for node in _walk(trigger):
            for key in TRIGGER_REFERENCE_KEYS:
                if key in node:
                    referenced_ids.update(_values(node[key]))

    referenced_from_tags: set[str] = set()
    for tag in entities["tag"]:
        for node in _walk(tag):
            for key in ("firingTriggerId", "blockingTriggerId"):
                referenced_from_tags.update(_values(node.get(key)))
    missing_trigger_references = len(referenced_from_tags - trigger_ids)
    orphan_triggers = len(trigger_ids - referenced_ids)

    unanchored_regex_filters = 0
    for trigger in triggers:
        for node in _walk(trigger):
            if not any(key in node for key in FILTER_KEYS):
                continue
            for filter_item in _values_as_dicts(node.get("customEventFilter")) + _values_as_dicts(node.get("filter")):
                filter_type = str(filter_item.get("type", "")).upper()
                if "REGEX" not in filter_type:
                    continue
                params = filter_item.get("parameter", [])
                if not isinstance(params, list):
                    continue
                for param in params:
                    if not isinstance(param, dict) or param.get("key") not in {"arg1", "value"}:
                        continue
                    pattern = param.get("value")
                    if isinstance(pattern, str) and pattern and not (pattern.startswith("^") and pattern.endswith("$")):
                        unanchored_regex_filters += 1

    return {
        "sha256": hashlib.sha256(raw_bytes).hexdigest(),
        "entity_counts": counts,
        "paused_tags": sum(item.get("paused") is True for item in entities["tag"]),
        "duplicate_ids": duplicate_ids,
        "duplicate_names": duplicate_names,
        "missing_trigger_references": missing_trigger_references,
        "orphan_triggers": orphan_triggers,
        "unanchored_regex_filters": unanchored_regex_filters,
        "limitations": [
            "Structural triage only; it does not evaluate runtime behavior, consent, destination acceptance, counting, or reconciliation.",
            "Findings are counts only. Object names, IDs, parameter values, and payloads are not printed.",
            "An unanchored regex is a review prompt, not proof of a defect; anchoring is required only when exact matching is intended.",
        ],
    }


def _values_as_dicts(value: Any) -> list[dict[str, Any]]:
    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]
    return []


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("export", type=Path, help="Path to a GTM container JSON export")
    parser.add_argument("--json", action="store_true", help="Print the summary as JSON")
    args = parser.parse_args()

    try:
        raw = args.export.read_bytes()
    except OSError as exc:
        print(f"Unable to read export ({exc.__class__.__name__}).", file=sys.stderr)
        return 2

    try:
        document = json.loads(raw)
        result = inventory(document, raw)
    except (json.JSONDecodeError, ValueError) as exc:
        if isinstance(exc, json.JSONDecodeError):
            message = f"Invalid JSON at line {exc.lineno}, column {exc.colno}."
        else:
            message = str(exc)
        print(message, file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0

    print("GTM export structural inventory (read-only)")
    print(f"SHA-256: {result['sha256']}")
    print("Entity counts:")
    for key, count in result["entity_counts"].items():
        print(f"  {key}: {count}")
    print("Review counts:")
    for key in (
        "paused_tags",
        "duplicate_ids",
        "duplicate_names",
        "missing_trigger_references",
        "orphan_triggers",
        "unanchored_regex_filters",
    ):
        print(f"  {key}: {result[key]}")
    for limitation in result["limitations"]:
        print(f"Note: {limitation}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
