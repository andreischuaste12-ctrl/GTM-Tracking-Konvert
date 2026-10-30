#!/usr/bin/env python3
"""Build a GTM container import file from a declarative spec, with pre-import checks.

The output is a local file only. It is never imported or published by this tool, and it is not
proof that Google Tag Manager will accept it: review it in the import preview of a scratch workspace.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

PLACEHOLDER = "0"
REFERENCE = re.compile(r"\{\{([^{}]+)\}\}")
ALWAYS_RESOLVED_REFERENCES = {"_event"}
SENSITIVE_NAME = re.compile(r"e[-_]?mail|phone|telefone|cpf|passw|birth", re.IGNORECASE)
SECRET_NAME = re.compile(r"secret|token|passw|api[-_]?key", re.IGNORECASE)
PARAMETER_TYPES = {"TEMPLATE", "BOOLEAN", "INTEGER", "LIST", "MAP"}
CONSENT_STATUSES = {"NOT_SET", "NOT_NEEDED", "NEEDED"}
RESERVED_RAW_KEYS = {
    "accountId",
    "containerId",
    "tagId",
    "triggerId",
    "variableId",
    "folderId",
    "name",
    "type",
    "parameter",
    "firingTriggerId",
    "blockingTriggerId",
    "parentFolderId",
    "fingerprint",
}


def _walk(value: Any):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from _walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk(child)


def _strings(value: Any):
    for node in _walk(value):
        for child in node.values():
            if isinstance(child, str):
                yield child


def encode_parameter(key: str, value: Any) -> dict[str, Any]:
    """Convert a spec value to a GTM parameter object."""
    if isinstance(value, bool):
        return {"type": "BOOLEAN", "key": key, "value": "true" if value else "false"}
    if isinstance(value, int):
        return {"type": "INTEGER", "key": key, "value": str(value)}
    if isinstance(value, str):
        return {"type": "TEMPLATE", "key": key, "value": value}
    if isinstance(value, dict) and set(value) == {"table"}:
        table = value["table"]
        columns, rows = table["columns"], table["rows"]
        if any(len(row) != len(columns) for row in rows):
            raise ValueError(f"table for '{key}' has a row whose length differs from its columns")
        return {
            "type": "LIST",
            "key": key,
            "list": [
                {
                    "type": "MAP",
                    "map": [
                        encode_parameter(column, cell) for column, cell in zip(columns, row)
                    ],
                }
                for row in rows
            ],
        }
    if isinstance(value, dict) and value.get("type") in PARAMETER_TYPES:
        return {**value, "key": key}
    raise ValueError(f"unsupported value for parameter '{key}'")


def _parameters(spec: dict[str, Any]) -> list[dict[str, Any]]:
    result = [encode_parameter(key, value) for key, value in spec.get("params", {}).items()]
    result.extend(spec.get("parameter", []))
    return result


def _raw_fields(spec: dict[str, Any], label: str, errors: list[str]) -> dict[str, Any]:
    raw = spec.get("raw", {})
    clash = sorted(set(raw) & RESERVED_RAW_KEYS)
    if clash:
        errors.append(f"{label}: 'raw' may not set {', '.join(clash)}")
        return {}
    return raw


def _duplicates(label: str, names: list[str]) -> list[str]:
    return [
        f"duplicate {label} name: {name}" for name, count in Counter(names).items() if count > 1
    ]


def _check_prefix(kind: str, name: str, naming: dict[str, list[str]], errors: list[str]) -> None:
    prefixes = naming.get(kind)
    if prefixes and not any(name.startswith(prefix) for prefix in prefixes):
        errors.append(f"{kind} '{name}' does not use an approved prefix: {', '.join(prefixes)}")


def _check_regex_filters(trigger: dict[str, Any], errors: list[str]) -> None:
    for node in _walk(trigger):
        if "REGEX" not in str(node.get("type", "")).upper():
            continue
        for param in node.get("parameter", []):
            pattern = param.get("value") if param.get("key") == "arg1" else None
            if isinstance(pattern, str) and not (pattern.startswith("^") and pattern.endswith("$")):
                errors.append(
                    f"trigger '{trigger['name']}': regex filter must be anchored with ^ and $"
                )


EVENT_NAME = re.compile(r"^[a-z][a-z0-9_]{0,39}$")
RESERVED_EVENT_PREFIXES = ("google_", "ga_", "firebase_")


def _base_info(base: dict[str, Any]) -> dict[str, Any]:
    """Collect names, ID ceilings, parameter-key evidence, and trigger IDs from a real export."""
    version = base.get("containerVersion", base)
    if not isinstance(version, dict):
        raise ValueError("base containerVersion must be an object")
    info: dict[str, Any] = {"names": {}, "ids": {}, "max": {}, "keys": {}, "trigger_refs": set()}
    for kind, id_key in (
        ("folder", "folderId"),
        ("variable", "variableId"),
        ("trigger", "triggerId"),
        ("tag", "tagId"),
    ):
        items = [item for item in version.get(kind, []) if isinstance(item, dict)]
        info["names"][kind] = {item["name"] for item in items if isinstance(item.get("name"), str)}
        info["ids"][kind] = {
            item["name"]: str(item[id_key])
            for item in items
            if isinstance(item.get("name"), str) and id_key in item
        }
        numeric = [int(item[id_key]) for item in items if str(item.get(id_key, "")).isdigit()]
        info["max"][kind] = max(numeric, default=0)
    info["dlv_paths"] = {
        item["name"]: next(
            (p.get("value") for p in item.get("parameter", []) if p.get("key") == "name"), None
        )
        for item in version.get("variable", [])
        if isinstance(item, dict) and item.get("type") == "v" and isinstance(item.get("name"), str)
    }
    info["builtins"] = {
        item["name"] for item in version.get("builtInVariable", []) if isinstance(item, dict)
        and isinstance(item.get("name"), str)
    }
    for kind in ("tag", "variable", "trigger"):
        for item in version.get(kind, []):
            if not isinstance(item, dict) or not isinstance(item.get("type"), str):
                continue
            keys = info["keys"].setdefault((kind, item["type"]), set())
            keys.update(
                param["key"] for param in item.get("parameter", [])
                if isinstance(param, dict) and isinstance(param.get("key"), str)
            )
    for tag in version.get("tag", []):
        if isinstance(tag, dict):
            for ref in tag.get("firingTriggerId", []) + tag.get("blockingTriggerId", []):
                info["trigger_refs"].add(str(ref))
    return info


def expand_events(
    spec: dict[str, Any], existing_paths: dict[str, str | None] | None = None
) -> tuple[dict[str, Any], list[str]]:
    """Expand the `events` contract section into variables, triggers, and GA4 event tags.

    `existing_paths` maps base-container Data Layer variable names to their paths, so shared
    variables are reused instead of recreated.
    """
    errors: list[str] = []
    events = spec.get("events", [])
    if not events:
        return spec, errors
    ga4 = spec.get("ga4", {})
    measurement_variable = ga4.get("measurementIdVariable")
    if not measurement_variable:
        errors.append("events require ga4.measurementIdVariable (a Constant variable name)")
    expanded = {
        **spec,
        "variables": list(spec.get("variables", [])),
        "triggers": list(spec.get("triggers", [])),
        "tags": list(spec.get("tags", [])),
    }
    variable_paths = {
        **(existing_paths or {}),
        **{item["name"]: item.get("params", {}).get("name") for item in expanded["variables"]},
    }
    for event in events:
        name = event["name"]
        label = f"event '{name}'"
        if not EVENT_NAME.match(name):
            errors.append(f"{label}: name must match {EVENT_NAME.pattern}")
        if name.startswith(RESERVED_EVENT_PREFIXES):
            errors.append(f"{label}: name uses a reserved prefix {RESERVED_EVENT_PREFIXES}")
        domain = event.get("domain", "General")
        rows: list[list[str]] = []
        seen: set[str] = set()
        for parameter in event.get("parameters", []):
            key = parameter["name"]
            if not EVENT_NAME.match(key):
                errors.append(f"{label}: parameter name '{key}' must match {EVENT_NAME.pattern}")
            if key.startswith(RESERVED_EVENT_PREFIXES):
                errors.append(f"{label}: parameter '{key}' uses a reserved prefix")
            if key in seen:
                errors.append(f"{label}: duplicate parameter '{key}'")
            seen.add(key)
            variable_name = parameter.get("variableName", f"DLV | {domain} | {key}")
            path = parameter.get("path", key)
            if variable_name in variable_paths:
                if variable_paths[variable_name] != path:
                    errors.append(f"{label}: variable '{variable_name}' is defined with another path")
            else:
                variable_paths[variable_name] = path
                expanded["variables"].append(
                    {
                        "name": variable_name,
                        "type": "v",
                        "params": {"name": path, "dataLayerVersion": 2, "setDefaultValue": False},
                        **({"folder": ga4["variableFolder"]} if ga4.get("variableFolder") else {}),
                    }
                )
            rows.append([key, "{{" + variable_name + "}}"])
        trigger_name = event.get("triggerName", f"Event | {domain} | {name}")
        expanded["triggers"].append(
            {"name": trigger_name, "type": "CUSTOM_EVENT", "eventName": name}
        )
        params: dict[str, Any] = {
            "eventName": name,
            "measurementIdOverride": "{{" + str(measurement_variable) + "}}",
        }
        if rows:
            params["eventSettingsTable"] = {
                "table": {"columns": ["parameter", "parameterValue"], "rows": rows}
            }
        expanded["tags"].append(
            {
                "name": event.get("tagName", f"GA4 | Event | {name}"),
                "type": "gaawe",
                "params": params,
                "firingTriggers": [trigger_name],
                "consent": event.get("consent", {"status": "NOT_SET"}),
                **({"folder": ga4["folder"]} if ga4.get("folder") else {}),
            }
        )
    return expanded, errors


def build(
    spec: dict[str, Any], base: dict[str, Any] | None = None
) -> tuple[dict[str, Any], list[str], list[str]]:
    """Return (export document, errors, warnings). Errors block writing the output.

    With `base` (a real export), only new objects are emitted: IDs continue after the base,
    names may not collide, references resolve against both, and type/key evidence is checked.
    """
    info = _base_info(base) if base is not None else None
    spec, event_errors = expand_events(spec, info["dlv_paths"] if info else None)
    errors: list[str] = list(event_errors)
    warnings: list[str] = []
    naming = spec.get("naming", {})
    builtin_triggers: dict[str, str] = spec.get("builtinTriggerIds", {})

    folder_specs = [{"name": name} for name in spec.get("folders", [])]
    variable_specs = spec.get("variables", [])
    trigger_specs = spec.get("triggers", [])
    tag_specs = spec.get("tags", [])

    for label, items in (
        ("folder", folder_specs),
        ("variable", variable_specs),
        ("trigger", trigger_specs),
        ("tag", tag_specs),
    ):
        errors.extend(_duplicates(label, [item["name"] for item in items]))

    def id_start(kind: str) -> int:
        return (info["max"][kind] if info else 0) + 1

    folder_ids = {
        item["name"]: str(i) for i, item in enumerate(folder_specs, start=id_start("folder"))
    }
    trigger_ids = {
        item["name"]: str(i) for i, item in enumerate(trigger_specs, start=id_start("trigger"))
    }
    variable_names = {item["name"] for item in variable_specs}
    builtin_names = {item["name"] for item in spec.get("builtInVariables", [])}
    if info:
        for kind, items in (
            ("folder", folder_specs),
            ("variable", variable_specs),
            ("trigger", trigger_specs),
            ("tag", tag_specs),
        ):
            for item in items:
                if item["name"] in info["names"][kind]:
                    errors.append(f"{kind} '{item['name']}' already exists in the base export")
        folder_ids = {**info["ids"]["folder"], **folder_ids}
        trigger_ids = {**info["ids"]["trigger"], **trigger_ids}
        for given in builtin_triggers.values():
            if str(given) not in info["trigger_refs"]:
                warnings.append(
                    f"builtinTriggerIds: ID {given} is not referenced by any tag in the base export"
                )
    resolvable = (
        variable_names
        | builtin_names
        | (info["names"]["variable"] | info["builtins"] if info else set())
        | ALWAYS_RESOLVED_REFERENCES
        | set(spec.get("allowReferences", []))
    )

    def folder_fields(item: dict[str, Any], label: str) -> dict[str, str]:
        folder = item.get("folder")
        if folder is None:
            return {}
        if folder not in folder_ids:
            errors.append(f"{label}: unknown folder '{folder}'")
            return {}
        return {"parentFolderId": folder_ids[folder]}

    def check_references(item: dict[str, Any], label: str) -> None:
        for text in _strings(item):
            for ref in REFERENCE.findall(text):
                if ref not in resolvable:
                    errors.append(f"{label}: unresolved reference {{{{{ref}}}}}")

    def check_values(item: dict[str, Any], label: str) -> None:
        for node in _walk(item.get("parameter", [])):
            key, value = node.get("key"), node.get("value")
            if not isinstance(key, str) or not isinstance(value, str):
                continue
            if SECRET_NAME.search(key) and value and not REFERENCE.fullmatch(value):
                errors.append(f"{label}: literal value for secret-like parameter '{key}'")
            if SENSITIVE_NAME.search(value) or SENSITIVE_NAME.search(key):
                warnings.append(f"{label}: sensitive-looking name in '{key}'; confirm policy")

    def check_schema(kind: str, entity: dict[str, Any], label: str) -> None:
        if not info:
            return
        known = info["keys"].get((kind, entity["type"]))
        if known is None:
            warnings.append(f"{label}: type '{entity['type']}' is not in the base export; unverified")
            return
        for param in entity.get("parameter", []):
            if param["key"] not in known:
                warnings.append(
                    f"{label}: parameter key '{param['key']}' not seen for type "
                    f"'{entity['type']}' in the base export"
                )

    folders = [
        {
            "accountId": PLACEHOLDER,
            "containerId": PLACEHOLDER,
            "folderId": folder_ids[item["name"]],
            "name": item["name"],
        }
        for item in folder_specs
    ]

    variables: list[dict[str, Any]] = []
    for index, item in enumerate(variable_specs, start=1):
        label = f"variable '{item['name']}'"
        _check_prefix("variable", item["name"], naming, errors)
        entity = {
            "accountId": PLACEHOLDER,
            "containerId": PLACEHOLDER,
            "variableId": str(id_start("variable") + index - 1),
            "name": item["name"],
            "type": item["type"],
            "parameter": _parameters(item),
            **folder_fields(item, label),
            **_raw_fields(item, label, errors),
        }
        check_values(entity, label)
        check_references(entity, label)
        check_schema("variable", entity, label)
        variables.append(entity)

    triggers: list[dict[str, Any]] = []
    for item in trigger_specs:
        label = f"trigger '{item['name']}'"
        _check_prefix("trigger", item["name"], naming, errors)
        entity = {
            "accountId": PLACEHOLDER,
            "containerId": PLACEHOLDER,
            "triggerId": trigger_ids[item["name"]],
            "name": item["name"],
            "type": item["type"],
            **folder_fields(item, label),
        }
        if "eventName" in item:
            entity["customEventFilter"] = [
                {
                    "type": "EQUALS",
                    "parameter": [
                        {"type": "TEMPLATE", "key": "arg0", "value": "{{_event}}"},
                        {"type": "TEMPLATE", "key": "arg1", "value": item["eventName"]},
                    ],
                }
            ]
        if item.get("params") or item.get("parameter"):
            entity["parameter"] = _parameters(item)
        entity.update(_raw_fields(item, label, errors))
        _check_regex_filters(entity, errors)
        check_references(entity, label)
        check_schema("trigger", entity, label)
        triggers.append(entity)

    tags: list[dict[str, Any]] = []
    for index, item in enumerate(tag_specs, start=1):
        label = f"tag '{item['name']}'"
        firing = item.get("firingTriggers", [])
        blocking = item.get("blockingTriggers", [])
        if not firing and not item.get("paused"):
            errors.append(f"{label}: has no firing trigger and is not paused")

        def resolve(names: list[str], role: str) -> list[str]:
            ids: list[str] = []
            for name in names:
                if name in trigger_ids:
                    ids.append(trigger_ids[name])
                elif name in builtin_triggers:
                    ids.append(str(builtin_triggers[name]))
                else:
                    errors.append(f"{label}: unknown {role} trigger '{name}'")
            return ids

        consent = item.get("consent", {"status": "NOT_SET"})
        status = consent.get("status")
        consent_settings: dict[str, Any] = {"consentStatus": status}
        if status not in CONSENT_STATUSES:
            errors.append(f"{label}: consent.status must be one of {sorted(CONSENT_STATUSES)}")
        elif status == "NEEDED":
            types = consent.get("types", [])
            if not types:
                errors.append(f"{label}: consent NEEDED requires at least one consent type")
            consent_settings["consentType"] = {
                "type": "LIST",
                "list": [{"type": "TEMPLATE", "value": value} for value in types],
            }
        elif status == "NOT_SET":
            warnings.append(f"{label}: consent not declared (NOT_SET); decide per approved policy")

        if item["type"] == "html":
            warnings.append(f"{label}: Custom HTML needs code review before import")

        entity = {
            "accountId": PLACEHOLDER,
            "containerId": PLACEHOLDER,
            "tagId": str(id_start("tag") + index - 1),
            "name": item["name"],
            "type": item["type"],
            "parameter": _parameters(item),
            "firingTriggerId": resolve(firing, "firing"),
            "tagFiringOption": item.get("firingOption", "ONCE_PER_EVENT"),
            "consentSettings": consent_settings,
            **folder_fields(item, label),
            **_raw_fields(item, label, errors),
        }
        if blocking:
            entity["blockingTriggerId"] = resolve(blocking, "blocking")
        if item.get("paused"):
            entity["paused"] = True
        check_values(entity, label)
        check_references(entity, label)
        check_schema("tag", entity, label)
        tags.append(entity)

    container = spec.get("container", {})
    document = {
        "exportFormatVersion": 2,
        "containerVersion": {
            "accountId": PLACEHOLDER,
            "containerId": PLACEHOLDER,
            "container": {
                "accountId": PLACEHOLDER,
                "containerId": PLACEHOLDER,
                "name": container.get("name", "Generated container"),
                "publicId": container.get("publicId", "GTM-XXXXXXX"),
                "usageContext": container.get("usageContext", ["WEB"]),
            },
            "folder": folders,
            "builtInVariable": [
                {"accountId": PLACEHOLDER, "containerId": PLACEHOLDER, **item}
                for item in spec.get("builtInVariables", [])
            ],
            "variable": variables,
            "trigger": triggers,
            "tag": tags,
        },
    }
    return document, errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", type=Path, help="Path to the build spec JSON")
    parser.add_argument("--output", type=Path, help="Where to write the import JSON")
    parser.add_argument("--force", action="store_true", help="Overwrite an existing output file")
    parser.add_argument(
        "--base",
        type=Path,
        help="Fresh export of the target container: avoids ID/name collisions, checks type/key evidence",
    )
    args = parser.parse_args()

    try:
        spec = json.loads(args.spec.read_bytes())
        base = json.loads(args.base.read_bytes()) if args.base else None
        document, errors, warnings = build(spec, base)
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        print(f"Invalid spec ({exc.__class__.__name__}: {exc}).", file=sys.stderr)
        return 2

    version = document["containerVersion"]
    print("GTM container build (local file only; nothing is imported or published)")
    for key in ("folder", "builtInVariable", "variable", "trigger", "tag"):
        print(f"  {key}: {len(version[key])}")
    if args.base is None:
        print("NOTE: no --base export; tag/variable types and parameter keys are unverified.")
    for message in warnings:
        print(f"WARNING: {message}")
    for message in errors:
        print(f"ERROR: {message}")
    if errors:
        print("No file written.")
        return 1

    if args.output is None:
        print("Validation passed; no --output given, no file written.")
        return 0
    if args.output.exists() and not args.force:
        print(f"{args.output} exists; pass --force to overwrite.", file=sys.stderr)
        return 2
    args.output.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {args.output}. Review it in the import preview of a scratch workspace.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
