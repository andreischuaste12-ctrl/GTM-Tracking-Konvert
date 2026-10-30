# Event contracts and tracking architecture

## What a reliable contract contains

Describe events in business language, not button or tag terms. For each event, record:

- **Name and definition:** observable fact, exact timing, and condition for occurrence.
- **Grain:** what one event/row represents (action, session, item, order, payment, shipment, refund). Do not mix grains in one parameter.
- **Producer and source of truth:** application, backend, checkout, webhook, or integration that originated the fact; technical owner and data owner.
- **Identity:** logical event ID and required entity IDs (order, payment, user, item/variant). Explain scope, stability, uniqueness, retry behavior, and survival across browser/server flows.
- **Time:** event time versus send/ingestion time, timezone, and late/replay policy when analysis depends on it.
- **Fields:** key, description, type, format/unit, nullability, enumerations, validation, sensitivity, and authorized destinations.
- **Monetary semantics:** ISO 4217 currency, major/minor units, inclusion of shipping/tax/discount, rounding, and expected total. Never convert by heuristic.
- **Operations:** retry policy, idempotency/deduplication, corrections, cancellation/refund, compatible version, and accountable contact.

Keep a versioned catalog/specification outside scattered tags. A table or JSON Schema helps when it automates validation; do not create ceremonial schemas with no consumers. Breaking changes (name, grain, type, semantics, unit, identity) require a coordinated migration and explicit compatibility.

## Layered architecture

Keep these layers distinct:

1. **Fact production:** application/backend emits the correct fact once per business condition and preserves authoritative identifiers/data.
2. **Collection:** data layer/GTM Web receives structured events or requests; avoid depending on visual text/DOM when a reliable contract exists.
3. **Interpretation:** variables, triggers, or Clients identify the message and resolve data without mixing messages or events.
4. **Transformation and routing:** validate, normalize only by explicit rule, enforce consent/minimization, and map to destinations.
5. **Delivery:** browser or Server sends a destination-compliant payload. GTM Server is not a durable queue, transaction system, exactly-once guarantee, or warehouse; verify actual provider/infrastructure guarantees.
6. **Consumption and control:** platforms, warehouse/BI, and financial sources can apply different rules. Reconcile with aligned definitions, windows, and grain.

Document the flow and owner for each critical event. A simple matrix helps:

| Event | Producer/source of truth | Grain/ID | Web | Server | Destinations | Owner |
|---|---|---|---|---|---|---|

## Data layer and SPAs

- Initialize the object before the container when pre-load events must be available; use the configured data-layer name.
- Each event should carry a coherent snapshot of the fields used for that fact where practical. The data layer retains state; stale fields can remain after a partial push. Explicitly handle missing, stale, and cleared ecommerce state according to documentation and contract.
- Do not associate `visitorType`, currency, cart, or shipping from a previous push with the current order without a key that proves the relationship.
- In an SPA, observe actual navigation, automatic/manual `page_view` policy, and which system emits route changes. Do not infer a page view from All Pages or DOM Ready on every navigation.
- Count producer occurrences and assess reentrancy/repetition. A GTM time rule does not replace idempotent identity for payments/orders.
- Prefer one responsible source per event. If browser, checkout, backend, and Server send the same event, document why and how the destination deduplicates it.

## Destination names and contracts

Keep a stable business name and map it to each destination's names/parameters. Do not force all destinations to share an incompatible payload.

- Use GA4 recommended names when semantics match; send the parameters required by the current official ecommerce schema.
- Preserve event/order IDs in the format and scope defined by the destination; the presence of a field does not prove deduplication.
- Distinguish user ID, session ID, order ID, and event ID. Never substitute one for another.
- For items, maintain catalog ID, variant, quantity, and price according to the catalog and destination; verify SKU/variant compatibility with ad feeds.

## Contract tests

Use synthetic, PII-free fixtures covering valid payloads, omitted fields, invalid values, different currencies, disallowed decimal quantities, empty item arrays, partial orders/refunds, retries, duplicate events, denied consent, and schema changes. Automate local validation where feasible; GTM Preview complements these tests but does not replace them.
