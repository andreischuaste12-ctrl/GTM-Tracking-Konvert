#!/usr/bin/env python3
"""Summarize a GTM JSON export without printing configuration values."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
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
ID_KEYS = {
    "tag": "tagId",
    "trigger": "triggerId",
    "variable": "variableId",
    "folder": "folderId",
    "customTemplate": "templateId",
}
TRIGGER_REFERENCE_KEYS = {"firingTriggerId", "blockingTriggerId", "triggerId", "triggerIds"}
FILTER_KEYS = {"customEventFilter", "filter"}
# Heuristic: GTM built-in triggers (for example All Pages) are referenced by IDs in the
# 2147479xxx range and do not appear in the exported trigger list.
BUILTIN_TRIGGER_ID_FLOOR = 2147479000
ALWAYS_RESOLVED_REFERENCES = {"_event"}
REFERENCE = re.compile(r"\{\{([^{}]+)\}\}")
SENSITIVE_NAME = re.compile(r"e[-_]?mail|phone|telefone|cpf|passw|birth", re.IGNORECASE)
SECRET_NAME = re.compile(r"secret|token|passw|api[-_]?key", re.IGNORECASE)
REVIEW_KEYS = (
    "paused_tags",
    "duplicate_ids",
    "duplicate_names",
    "missing_trigger_references",
    "builtin_trigger_references",
    "orphan_triggers",
    "tags_without_firing_trigger",
    "tags_without_consent_settings",
    "custom_html_tags",
    "sensitive_parameter_names",
    "literal_secret_like_parameters",
    "unreferenced_variables",
    "unresolved_variable_references",
    "unanchored_regex_filters",
    "sequencing_references",
    "unresolved_sequencing_references",
    "sequencing_cycle_groups",
)


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


def _sequence_references(tag: dict[str, Any]) -> list[str]:
    references: list[str] = []
    for key in ("setupTag", "teardownTag"):
        value = tag.get(key)
        entries = value if isinstance(value, list) else [value]
        for entry in entries:
            if isinstance(entry, dict) and isinstance(entry.get("tagName"), str):
                references.append(entry["tagName"])
    return references


def _cycle_group_count(graph: dict[int, set[int]]) -> int:
    visited: set[int] = set()
    finish_order: list[int] = []
    for start in graph:
        if start in visited:
            continue
        stack = [(start, False)]
        while stack:
            node, expanded = stack.pop()
            if expanded:
                finish_order.append(node)
                continue
            if node in visited:
                continue
            visited.add(node)
            stack.append((node, True))
            stack.extend((neighbor, False) for neighbor in graph[node] if neighbor not in visited)

    reverse_graph = {node: set() for node in graph}
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            reverse_graph[neighbor].add(node)

    visited.clear()
    cycle_groups = 0
    for start in reversed(finish_order):
        if start in visited:
            continue
        component: list[int] = []
        stack = [start]
        visited.add(start)
        while stack:
            node = stack.pop()
            component.append(node)
            for neighbor in reverse_graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    stack.append(neighbor)
        if len(component) > 1 or start in graph[start]:
            cycle_groups += 1
    return cycle_groups


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
    for key, items in entities.items():
        id_key = ID_KEYS.get(key)
        ids = [str(item[id_key]) for item in items if id_key and id_key in item]
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
    unlisted_references = referenced_from_tags - trigger_ids
    builtin_trigger_references = {
        ref for ref in unlisted_references if ref.isdigit() and int(ref) >= BUILTIN_TRIGGER_ID_FLOOR
    }
    missing_trigger_references = len(unlisted_references - builtin_trigger_references)
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

    tag_indices_by_name: dict[str, list[int]] = {}
    for index, tag in enumerate(entities["tag"]):
        name = tag.get("name")
        if isinstance(name, str):
            tag_indices_by_name.setdefault(name, []).append(index)

    sequencing_graph = {index: set() for index in range(len(entities["tag"]))}
    sequencing_references = 0
    unresolved_sequencing_references = 0
    for index, tag in enumerate(entities["tag"]):
        for name in _sequence_references(tag):
            sequencing_references += 1
            targets = tag_indices_by_name.get(name, [])
            if not targets:
                unresolved_sequencing_references += 1
            sequencing_graph[index].update(targets)
    sequencing_cycle_groups = _cycle_group_count(sequencing_graph)

    tags = entities["tag"]
    variable_names = {item["name"] for item in entities["variable"] if isinstance(item.get("name"), str)}
    resolvable = (
        variable_names
        | {item["name"] for item in entities["builtInVariable"] if isinstance(item.get("name"), str)}
        | ALWAYS_RESOLVED_REFERENCES
    )
    used_references: set[str] = set()
    for collection in ("tag", "trigger", "variable"):
        for item in entities[collection]:
            for node in _walk(item):
                for child in node.values():
                    if isinstance(child, str):
                        used_references.update(REFERENCE.findall(child))

    sensitive_parameter_names = 0
    literal_secret_like_parameters = 0
    for item in tags + entities["variable"]:
        for node in _walk(item.get("parameter", [])):
            key_name, value = node.get("key"), node.get("value")
            if not isinstance(key_name, str) or not isinstance(value, str):
                continue
            if SENSITIVE_NAME.search(key_name) or SENSITIVE_NAME.search(value):
                sensitive_parameter_names += 1
            if SECRET_NAME.search(key_name) and value and not REFERENCE.fullmatch(value):
                literal_secret_like_parameters += 1

    return {
        "sha256": hashlib.sha256(raw_bytes).hexdigest(),
        "entity_counts": counts,
        "paused_tags": sum(item.get("paused") is True for item in entities["tag"]),
        "duplicate_ids": duplicate_ids,
        "duplicate_names": duplicate_names,
        "missing_trigger_references": missing_trigger_references,
        "builtin_trigger_references": len(builtin_trigger_references),
        "orphan_triggers": orphan_triggers,
        "tags_without_firing_trigger": sum(
            not tag.get("firingTriggerId") and tag.get("paused") is not True for tag in tags
        ),
        "tags_without_consent_settings": sum(
            (tag.get("consentSettings") or {}).get("consentStatus", "NOT_SET") == "NOT_SET"
            for tag in tags
        ),
        "custom_html_tags": sum(tag.get("type") == "html" for tag in tags),
        "sensitive_parameter_names": sensitive_parameter_names,
        "literal_secret_like_parameters": literal_secret_like_parameters,
        "unreferenced_variables": len(variable_names - used_references),
        "unresolved_variable_references": len(used_references - resolvable),
        "unanchored_regex_filters": unanchored_regex_filters,
        "sequencing_references": sequencing_references,
        "unresolved_sequencing_references": unresolved_sequencing_references,
        "sequencing_cycle_groups": sequencing_cycle_groups,
        "limitations": [
            "Structural triage only; it does not evaluate runtime behavior, consent, destination acceptance, counting, or reconciliation.",
            "Findings are counts only. Object names, IDs, parameter values, and payloads are not printed.",
            "An unanchored regex is a review prompt, not proof of a defect; anchoring is required only when exact matching is intended.",
            "Sequence references resolve by exact tag name; duplicate names can make a reported cycle ambiguous and need manual review.",
            "Built-in trigger references are recognized by a numeric-ID heuristic (2147479xxx) and are reported separately, not as missing.",
            "Consent, sensitive-name, secret-like, and variable-usage counts are review prompts: they read configuration only and do not prove runtime behavior or policy compliance.",
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
    parser.add_argument(
        "--fail-on",
        default="",
        help="Comma-separated review count names; exit 1 if any is greater than zero",
    )
    args = parser.parse_args()

    fail_keys = [key for key in args.fail_on.split(",") if key]
    unknown = [key for key in fail_keys if key not in REVIEW_KEYS]
    if unknown:
        print(f"Unknown --fail-on count: {', '.join(unknown)}", file=sys.stderr)
        return 2

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

    failed = [key for key in fail_keys if result[key] > 0]
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
        return 1 if failed else 0

    print("GTM export structural inventory (read-only)")
    print(f"SHA-256: {result['sha256']}")
    print("Entity counts:")
    for key, count in result["entity_counts"].items():
        print(f"  {key}: {count}")
    print("Review counts:")
    for key in REVIEW_KEYS:
        print(f"  {key}: {result[key]}")
    for limitation in result["limitations"]:
        print(f"Note: {limitation}")
    if failed:
        print(f"Failing on: {', '.join(failed)}", file=sys.stderr)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
