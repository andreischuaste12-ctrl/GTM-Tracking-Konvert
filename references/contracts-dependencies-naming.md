# Contracts, dependencies, and naming

## Variables

For each variable, verify type, path/code, Data Layer version, default, returned types, references,
and availability at the event where it is used. Consider `undefined`, `null`, empty string, zero,
`false`, unexpected types, and a source API/SDK that is not ready. Prevent a missing value from
breaking a tag or being silently converted to zero.

Follow the prefix convention the user defines:

- `DLV | ...` — data-layer variable.
- `JS | ...` — custom JavaScript.
- `Cookie | ...` — first-party cookie.
- `Constant | ...` — constant value.
- `Lookup | ...` — lookup table.

Complete the name with the data domain and purpose in unambiguous language. Distinguish entity
identity from occurrence identity (for example, an account ID from an event ID). For financial
events, distinguish order/transaction ID, event ID, cart ID, value in major currency units, and
value in minor units; `orderFormId` is a VTEX-specific example. Do not assume `id`, `value`, `total`,
or `transaction_id` mean the same thing across producers.

Use paths that actually exist in the `dataLayer`. `transaction_id`, `transactionId`,
`ecommerce.transaction_id`, and `orderFormId` are different fields until evidence establishes equal
meaning. Data from one step (for example, `add_payment_info`) does not prove a field exists on
`purchase`.

## Triggers

Name triggers by role, source, and event, for example `Event | Account | trial_started`, `Event |
Lead | accepted`, `Event | Ecommerce | purchase`, `Event | Navigation | pageView`, or `Exception |
...`. Use labels that match the actual trigger type.

Verify type, exact event/capitalization, regex and anchoring, filters, exceptions, referenced tags,
page conditions, and trigger groups. Multiple triggers on one tag are generally alternative firing
paths; check tag exceptions and do not infer behavior from names. Anchor the full regex with `^` and
`$` when exact event matching is intended. Test paths with/without `/`, subpaths, and similar names.

## Tags and folders

Name tags by platform, type/event, and scope. Preserve the container's existing convention; do not
copy prefixes, years, or IDs from another environment. If there is no convention, propose a short
standard and confirm it before renaming existing objects.

Verify independently: tag name; type/template; destination ID; outgoing event name; parameters/event
settings; ecommerce object; consent; firing triggers; exceptions; sequencing; firing option;
paused/active state. Renaming a tag does not change the event it sends.

Folders are visual organization and do not alter collection. Move an item only when organization was
requested. Before copying a tag, confirm the original remains and the new tag's name/trigger/event
is distinct as intended.

## Structural export audit

Inventory items and relationships before fixing them: duplicates, missing references, template
dependencies, triggers/exceptions, setup/teardown tags, sequencing cycles, and executable code. When
claiming code passed syntax validation, record method and scope. Normal JavaScript syntax does not
prove a template compiles in GTM sandbox, its permissions allow real URLs, or the platform accepts
its payload.

Valid structure and existing references do not prove business fields, type, currency, consent,
delivery, or counting are correct. Do not report zero issues if the parser ignored fields or
built-ins.
