# Evidence, audits, and data quality

## Identify the source examined

For a GTM export, record the file, SHA-256, container ID, acquisition date, declared
version/workspace, and counts of tags, variables, triggers, templates, and folders. Preserve the
original. An export alone does not identify what is published. For a UI review, record the
container, workspace/version, screen, and observation time. Reconfirm the hash/version at the end if
files could change during analysis.

Inventory structure—duplicate IDs/names, missing references, orphan triggers, paused tags,
sequencing, and template permissions—as leads for investigation, not proof of execution or a defect.
Inspect configuration fields and dependencies for each event path.

## Evidence ladder

Use the highest label the source supports, with timestamp, scenario, and limits:

1. **Declared in the contract/source code** — the producer intends to emit the event.
2. **Configured in export/workspace** — the object and rule exist; execution is not proven.
3. **Observed in browser/data layer** — the event and payload occurred in that scenario.
4. **Resolved in GTM/Preview** — variables, triggers, tags, and consent behaved as observed in the
tested scenario.
5. **Outbound request observed** — destination, endpoint, and payload were sent by browser or
Server.
6. **Received/accepted by destination** — destination diagnostics or reliable logs confirm receipt;
HTTP 2xx alone proves only a transport response.
7. **Counted** — the event appears in the product UI/report/API after applicable processing and
latency.
8. **Reconciled** — identity and values match the financial/operational source with the same
definition, grain, timezone, currency, period, filters, and window.

Deduplication is a separate evidence requirement: obtain destination diagnostics for the event pair
and IDs expected to deduplicate. Do not infer it from tag names, present IDs, or aggregate totals.

## Diagnose each path

Walk every critical event in order and retain only the evidence needed, with minimized payloads:

`action/fact → producer → data layer/request → variable/Client → trigger and exceptions → tag →
transformation → outbound request → destination confirmation → consumption/finance`

Compare source and destination by logical event, ID, timestamp, typed parameters, currency/unit, and
consent. In Server, inspect the winning Client, event data, consent, applied Transformations,
outbound tag, and request. In Web, inspect the message number/time and resolved values in that
message.

## Data-quality metrics

Choose controls that match the risk and denominator: event/step volume and coverage; null/invalid ID
rate; out-of-range values; currency/type/unit; items without ID/price; duplicate rate by identity;
delay from fact to receipt; destination differences; reconciled share; and failures by
consent/session/route. Define window, segment, source, and alert threshold before interpreting
movement.

Equal counts do not prove quality: missing and duplicate events can offset; payload, grain, and
value can differ while totals match. Do not compare users, sessions, events, and orders as the same
entity. Separate loss, delay, wrong value, duplication, attribution, and revenue-definition
differences.

## Classification and reporting

Prioritize findings by impact (revenue, optimization, privacy, decision) and evidence strength. For
each finding state the observation, source, scenario, likely consequence, hypothesis/alternatives,
confidence, recommendation, and verification method. Preserve correct items and explain remediation
risks. Never use a subjective percentage as confidence or guarantee.
