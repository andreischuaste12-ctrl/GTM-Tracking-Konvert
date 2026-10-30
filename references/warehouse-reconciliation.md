# Warehouse export and reconciliation

Use this reference when GA4 numbers must be compared with a backend, billing system, CRM, or ad
platform, or when the GA4 BigQuery export is used for audit or reporting.

For revenue-specific rules (units, refunds, currency), use [ecommerce, money, and
reconciliation](ecommerce-money-reconciliation.md). This file covers the comparison method.

## Choose the right source of truth

- The backend or billing system is authoritative for orders, subscriptions, and leads. GA4 is a
  measurement of what was collected, subject to consent, blockers, and processing rules.
- Document, per metric, the authoritative system, its grain, timezone, and lifecycle state
  (created, paid, shipped, canceled, refunded).

## Align before comparing

Compare only after these match, and record each:

1. **Grain:** event, session, user, order, or line item.
2. **Time window and timezone:** the property reporting timezone versus the backend timezone;
   event timestamp versus processing or export time.
3. **Filters and definitions:** internal traffic, test data, bots, and the exact event or key-event
   definition on each side.
4. **Identity:** the shared key (transaction or lead ID), its stability across retries, and
   whether it is present on every event.
5. **Consent and collection gaps:** denied consent and blockers reduce collected volume; do not
   attribute the whole gap to implementation.

## BigQuery export checks

- Confirm the export type available for the property (daily, streaming) and which tables are final
  versus intraday; late-arriving events can change a day after first export.
- Deduplicate on the shared business key when the contract allows retries, and count distinct
  keys, not rows. Inspect event timestamps in the unit the export documents before converting.
- Parameters are nested and typed by value field; confirm the right value field per parameter
  before aggregating.
- Reported GA4 interface numbers can include modeled or thresholded data and may differ from the
  raw export. Name which surface each number came from.

## Classify the gap

For every mismatch, classify it as one of: definition difference, timing/timezone, filter,
identity gap, consent or blocking, duplicate collection, missing collection, destination
processing, or unexplained. Quantify each class and leave the remainder labeled unexplained;
do not force the totals to match. Use the [reconciliation template](../assets/reconciliation.template.md).

## Evidence

State the query or report definition, the date range and timezone, row counts at each filter step,
and the destination layer reached (see [audit evidence](audit-evidence.md)). Never include
personal data in query output kept as evidence.
