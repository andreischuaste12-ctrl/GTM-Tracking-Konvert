# GTM Web container

## Data layer and event flow

Before creating tags, observe the browser event and document its name, timing, `dataLayer`, and route changes. In SPA/VTEX applications, do not assume page load, navigation, DOM Ready, and ecommerce events happen once or on the same page. Use Preview to confirm the event fires a tag once at the intended time/scenario.

Preserve the producer's data layer. Do not create GTM business events that duplicate the producer without clearly assigning ownership. For `page_view`, distinguish automatic Google tag sends, manual tags, route changes, and Server-originated events. `send_page_view: false` proves one tag's configuration, not that no other emitter exists.

For internal-search events, verify with and without results that event and query appear at the source. Map actual fields to `view_search_results`; zero results may be valid. GA4 search configuration does not guarantee the VTEX app emits the event.

## Preview each event

For every selected event, inspect in order:

1. `dataLayer` at event time.
2. Variables resolved for that event, not just their configuration.
3. Triggers fired and tags executed, including exceptions.
4. Web hit and ecommerce/destination parameters.
5. Corresponding Server Preview data when forwarded.
6. Destination response and DebugView/Event Manager when external receipt is in scope.

Start with non-financial actions—page view, list, product, search, cart, and checkout steps. Confirm currency, items, variant/SKU ID, and `event_id` for downstream-useful events. Earlier steps do not prove `purchase`.

## Consent, identifiers, and personal data

Find the actual CMP. Verify initial consent, update, denial, grant, revocation, and which tags executed for each state. A `consent` object in the data layer does not prove tags consumed the changed state. In GTM, confirm a Consent Mode-compatible template/API and correct ordering; current Google guidance uses `setDefaultConsentState` and `updateConsentState` in GTM templates. In `gtag.js`, consent commands use a different interface. Do not replace GTM API with queued commands without validating order. Do not assume the CMP/API name or treat Consent Mode as a banner or compliance proof. Check [official references](official-references.md) and applicable policy.

Keep user data in a platform's dedicated feature where applicable, not generic analytics event parameters. Verify normalization, hashing, and source against the current official contract. Treat email, token, and identifier payloads as sensitive; never copy values into reports, tests, or output files.

## Pixel and Server deduplication

Map every emitter for the same event: app/checkout native pixel, HTML tags, Server Meta template, and integrations. Record `event_name`, source, and event ID. Claim deduplication only after verifying identical names and IDs across channels for the same logical event and confirming Event Manager evidence. A unique GTM ID per occurrence is not necessarily a stable order ID. A purchase event ID must follow the provider contract and coordinate browser/Server; do not invent another emitter to fill a gap.

Do not equate two firings with two counted conversions; also do not assume Meta deduplicated them without confirmation. Verify standard/custom event type, Pixel ID, and catalog parameters.

The Pixel `eventID` in a custom HTML tag may be computed too late (after the producer's next message) and differ from the Server ID. In Preview, compare the Pixel ID to the **same event's** message number, not the following event. See the correction pattern in [technical pitfalls](technical-pitfalls.md).

## SPA and repeated events

In an SPA (VTEX IO), third-party page views must fire on the route event, not only on “All Pages.” The producer may repeat `pageView` for the same URL, `view_cart` for a mini-cart, or `add_payment_info` after each payment-method change. Use an exception or deduplication key tested at both trigger and recording time.
