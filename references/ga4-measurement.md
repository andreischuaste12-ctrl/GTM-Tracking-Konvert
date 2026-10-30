# GA4 measurement workflow

Use this guide when a GTM task sends events to Google Analytics 4. Confirm current requirements in
the [official source catalog](official-references.md); do not copy a parameter from a different
destination without checking its semantics.

## Event and parameter contract

- Use a recommended GA4 event name only when its documented meaning matches the source business
fact. A matching name with a different grain or timing is still an incorrect event.
- Define each parameter's type, unit, nullability, sensitivity, owner, and destination. Keep custom
parameters bounded and decision-relevant.
- For ecommerce, map event-level fields and each `items` entry separately. Validate item ID/variant,
quantity, price, currency, discount, shipping, tax, and transaction ID against the source contract.
- Define `value` from the current GA4 ecommerce contract and the producer's explicit monetary unit.
Do not infer currency units from magnitude or copy a Google Ads/Meta amount definition.
- Preserve an order identifier across a purchase and its refund where the GA4 contract requires the
same transaction identity. A `purchase` event is not proof of payment settlement or net revenue.

## Collection paths

Distinguish Google tag/GTM Web collection from Measurement Protocol and server-side forwarding. Each
path has its own required fields, timing, session/context behavior, validation facilities, and
limits. Do not assume a server request is equivalent to a browser event because it uses the same
event name.

For single-page applications, define route ownership and whether page views are automatic or manual.
Prevent the Google tag, a history trigger, application code, and a Server path from sending
overlapping views.

## Validation

1. Inspect the producer event and data-layer message.
2. Confirm resolved GTM variables and event parameters on that same message.
3. Inspect the browser/Server request and verify the destination and payload.
4. Use GA4 DebugView and diagnostics where appropriate; allow for processing latency and feature
limits.
5. Verify report visibility and financial reconciliation separately from request delivery.

Do not place direct identifiers in standard GA4 event parameters. Use platform-specific user-data
features only under approved policy and their current documented controls. See the [evidence
ladder](audit-evidence.md).
