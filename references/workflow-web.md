# GTM Web container

## Data layer and event flow

Before creating tags, observe the browser event and document its name, timing, `dataLayer`, and
route changes. In any single-page application (SPA), do not assume page load, navigation, DOM Ready,
or application events happen once or on the same page. Use Preview to confirm the event fires a tag
once at the intended time and scenario.

Preserve the producer's data layer. Do not create GTM business events that duplicate the producer
without clearly assigning ownership. For `page_view`, distinguish automatic Google tag sends, manual
tags, route changes, and Server-originated events. `send_page_view: false` proves one tag's
configuration, not that no other emitter exists.

For search events, verify with and without results that the event and approved search attributes
appear at the source. Map actual fields to the destination's documented event contract; zero
results may be valid. Destination configuration does not guarantee that the application emits the
event.

## Preview each event

For every selected event, inspect in order:

1. `dataLayer` at event time.
2. Variables resolved for that event, not just their configuration.
3. Triggers fired and tags executed, including exceptions.
4. Web hit and ecommerce/destination parameters.
5. Corresponding Server Preview data when forwarded.
6. Destination response and DebugView/Event Manager when external receipt is in scope.

Start with representative actions for the project, such as page views, navigation, sign-up, form
submission, content interaction, or commerce steps. Validate each event's required fields and
identity from its producer contract. Earlier funnel steps do not prove a later business outcome such
as an accepted lead, activated account, or completed purchase.

## Consent, identifiers, and personal data

Find the actual CMP. Verify initial consent, update, denial, grant, revocation, and which tags
executed for each state. A `consent` object in the data layer does not prove tags consumed the
changed state. Confirm the GTM Consent Mode integration, API, and ordering in the canonical
[template guidance](custom-templates-api.md) and [official references](official-references.md). Do
not assume the CMP/API name or treat Consent Mode as a banner or compliance proof. Follow the
approved policy.

Keep user data in a platform's dedicated feature where applicable, not generic analytics event
parameters. Verify normalization, hashing, and source against the current official contract. Treat
email, token, and identifier payloads as sensitive; never copy values into reports, tests, or output
files.

## Pixel and Server deduplication

Map every emitter for the same event: application SDKs, native integrations, HTML tags, Server
templates, and backend integrations. Record `event_name`, source, and event ID. Claim deduplication
only after verifying identical names and IDs across channels for the same logical event and
confirming Event Manager evidence. A unique GTM ID per occurrence is not necessarily a stable order
ID. A purchase event ID must follow the provider contract and coordinate browser/Server; do not
invent another emitter to fill a gap.

Do not equate two firings with two counted conversions; also do not assume Meta deduplicated them
without confirmation. Verify standard/custom event type, Pixel ID, and catalog parameters.

The Pixel `eventID` in a custom HTML tag may be computed too late (after the producer's next
message) and differ from the Server ID. In Preview, compare the Pixel ID to the **same event's**
message number, not the following event. See the correction pattern in [technical
pitfalls](technical-pitfalls.md).

## SPA and repeated events

In any SPA, third-party page views may need to fire on the actual route event, not only on “All
Pages.” Producers can repeat events for the same URL or action. Determine whether repeats represent
new business occurrences; use a documented exception or stable deduplication key and test it at
trigger and recording time.
