# Source and application integration adapters

GTM contracts begin at the actual event producer. This skill is industry- and platform-neutral.
Sources may include a website, browser application, mobile-to-web bridge, SaaS backend, lead form,
content system, commerce platform, webhook, or server integration. Identify the producer and inspect
the installed application, integration, source contract, and payload before mapping anything.

## Adapter contract

For each source or integration, document:

- the authoritative producer and business fact (for example, submitted form, accepted lead, trial
  started, subscription changed, content viewed, or order completed);
- event name, timing, grain, and retry behavior;
- actual field paths, types, units, nullability, and IDs;
- consent/privacy API and when it becomes available;
- runtime restrictions, browser/server emitters, and supported integration or extension points;
- lifecycle states and transitions relevant to the business fact, such as lead acceptance, account
  activation, subscription changes, or payment, cancellation, and refund.

Map source fields to the stable business contract and then to destination-specific parameters. Do
not copy a field path, event name, ID, or lifecycle rule from another platform.

## Source-specific guardrails

- **Websites and web apps:** inspect the router, application event producer, consent integration,
  and whether browser navigation or history changes emit page views.
- **SaaS and subscriptions:** distinguish user intent (for example, clicking “start trial”) from a
  backend-confirmed state change; document account, subscription, and occurrence identity only as
  approved and required.
- **Lead generation and content:** distinguish form interaction/submission from backend acceptance
  or qualification. Do not send form contents or direct identifiers as generic analytics fields.
- **Commerce examples:** VTEX `orderFormId`, Pixel apps, and IO event names; Shopify Web Pixels and
  customer events; and WooCommerce hooks/plugins are source-specific. Confirm the installed version
  and actual payload before mapping identity, lifecycle, or monetary units.
- **APIs and server integrations:** inspect authentication boundaries, retry behavior, idempotency,
  event timestamps, and redaction before using request data in GTM Server.

When a required source field is unavailable, report the exact gap and identify whether it belongs in
the application/backend, integration, or a supported GTM layer. Do not create a misleading fallback
in GTM. Consult the [official reference catalog](official-references.md) for current platform and
destination documentation when a decision depends on vendor behavior.
