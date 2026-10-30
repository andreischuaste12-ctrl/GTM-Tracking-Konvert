# Source-platform adapters

GTM contracts begin at the actual event producer. This skill is platform-neutral; examples from
VTEX, Shopify, and WooCommerce do not define a universal ecommerce schema. Read the current platform
material through the [official source catalog](official-references.md), then inspect the installed
app, theme, checkout, integration, and payload.

## Adapter contract

For each source platform, document:

- the authoritative producer and business fact;
- event name, timing, grain, and retry behavior;
- actual field paths, types, units, nullability, and IDs;
- consent/privacy API and when it becomes available;
- checkout restrictions, browser/server emitters, and supported extension points;
- how the source order lifecycle represents payment, cancellation, and refund.

Map source fields to the stable business contract and then to destination-specific parameters. Do
not copy a field path, event name, ID, or lifecycle rule from another platform.

## Platform-specific guardrails

- **VTEX:** `orderFormId`, Pixel apps, and IO event names are VTEX-specific. Confirm the installed
Pixel app/version and event payload before mapping order or checkout identity.
- **Shopify:** use the current Web Pixels/customer-events and privacy model for the actual checkout
surface. Do not assume storefront JavaScript has the same access in checkout or customer events.
- **WooCommerce:** inspect the installed theme, checkout extensions, hooks, plugins, and order
lifecycle. A plugin's display name does not prove its emitted schema or duplicate behavior.
- **Other commerce sources:** follow the same source-contract method; do not invent a presumed
`orderId`, `transaction_id`, cart ID, or currency unit.

When a required source field is unavailable, report the exact gap and identify whether it belongs in
the application/backend, platform extension, or a supported GTM layer. Do not create a misleading
fallback in GTM.
