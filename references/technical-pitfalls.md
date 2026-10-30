# Technical pitfalls and how to prove them

These are investigation risks, not universal rules. Verify producer code, current documentation, and the real scenario before choosing a fix.

## Message state and variable evaluation

- The `dataLayer` accumulates state. A partial push can leave earlier values available. Verify that the event carries a coherent snapshot and that variables are evaluated in the expected context/time.
- Custom HTML tags, callbacks, sequencing, and asynchronous processing can change read timing. Do not use a later message/event ID to fill the current event. Compare fields with the message/occurrence observed in Preview.
- Prefer reading the business message that originated the event through a supported interface. If the contract requires a specific snapshot technique, prove it with synchronous and delayed execution cases before generalizing.
- Do not use a constant fallback for `event_id`; it can collapse distinct events. If reliable identity is unavailable, report the gap rather than inventing stability.

## Compilation and Preview state

- Reference errors, export format, and template permissions can block save, Preview, or publication. Validate in the workspace and verify Preview is tied to the expected version/code.
- A Preview with no apparent change may use another workspace/container or an old build. Check IDs, workspace, time, selected event, variables, and version.
- GTM template JavaScript is sandboxed and has its own APIs/permissions. Browser-console syntax does not prove template compilation or execution permission.
- Inspect variable values on the actual event. Variable configuration does not prove a value exists, has the expected type, or belongs to that occurrence.

## Repetition and deduplication

- SPAs and widgets may emit a navigation/action more than once; inspect producer sequence before changing triggers.
- Idempotent identity must come from the event/order and follow the destination contract. A timer, URL, SKU, or session ID rarely identifies a financial occurrence by itself.
- Call Pixel + server-side API deduplicated only when the destination confirms the same event name/key according to current rules. An `event_id` in exports is not that confirmation.
- Distinguish a duplicate browser event, two requests, two received records, and two counted conversions.

## Export and import

- Exports are snapshots; filenames such as `final` and UI counts do not prove they are the live version/current workspace. Pin hash, container, version, and source.
- Before importing, inspect preview and merge/replace effects in the chosen workspace; after an authorized action, inspect the workspace contents and diff. Import preview can compare against a different base than expected.
- Preserve templates, paused tags, and dependencies until their use is understood. Renaming/moving folders does not fix behavior.

## Minimum proof by claim

- “Fired”: tag and trigger on the correct Preview event.
- “Sent”: observed request and outbound payload.
- “Accepted”: applicable product confirmation; do not infer from tag name or HTTP status alone.
- “Deduplicated”: destination diagnostics for events from the same occurrence.
- “Purchase reconciled”: order ID/items/values compared with the financial source and documented definition.

Record only metadata required to reproduce the scenario. Use synthetic fixtures; never copy PII or credentials into logs or reports.
