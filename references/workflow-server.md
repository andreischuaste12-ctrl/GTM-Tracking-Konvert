# GTM Server container

The Server container receives events and forwards/transforms data. Identify the Client that claimed
each request, the data received, outbound tags, transformations, consent, and destination. A GA4
forwarding tag is not a Google Ads conversion and does not confirm an event was counted.

## Review order

1. Confirm Server container, tagging domain, workspace/publication, and actual Web transport.
2. Inspect Clients and precedence: which Client claims each request; distinguish GA4 from other
formats.
3. Inspect received event data and Client name in Preview; do not infer payload from a trigger name.
4. Check triggers, regex, filters, and dedicated/generic tags. Exclude auxiliary events or events
routed by dedicated tags from a generic rule when they overlap, after checking impact.
5. Check transformations and outputs: events, `event_id`, `transaction_id`, items, currencies,
value, consent, and current template settings.
6. Check external responses and deduplication separately.

Anchor event allowlist regexes (`^(eventA|eventB)$`) when exact matching is intended. `purchase`
inside `.+purchase` can also match `fake_purchase`; validate helper names and capitalization
exactly. “All custom events” is broad; filter by Client and required events.

Treat the installed template as the effective source. GitHub documentation or an upstream template
version does not prove an account's custom template is identical. Inspect permissions, variables,
template code, API version, URLs, fields, and credentials. Never expose tokens in code, logs,
outputs, or examples. Use supported constants/secret storage and confirm rotation with the provider
when a credential has been exposed.

Before updating a template, compare the original code version, local changes, and current
permissions. Do not replace a custom template with an assumed latest version. Preserve paused tags,
permission scopes, and existing triggers until the exact change is understood.

A `POST` response with status 200/204 proves an HTTP response in that test. For Meta, when present,
inspect `events_received` and messages. This does not prove counting in Ads Manager, deduplication,
or persistence in GA4 reports. Distinguish Server acceptance, provider response, Test Events, and
final reporting.
