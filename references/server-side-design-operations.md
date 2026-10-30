# Server-side tagging design and operations

Use this reference when a decision concerns GTM Server-side design, provisioning, migration, cost,
performance, privacy, availability, or operations.

## Decide from a requirement

State the problem to solve: reduce browser script execution, standardize routing, filter/enrich
payloads, control data access, collect on a first-party domain, or integrate server data. Compare
source-side alternatives (backend/webhook), GTM Web, SDKs, and data pipelines. Do not promise “more
cookies,” “more attribution,” or bypassing browser blocks/consent.

Server-side GTM processes requests in infrastructure controlled by the organization. Browser
interactions still require a Web emitter to collect and send events; moving a tag to Server does not
create facts the producer never emitted. Received data remains under the organization's operational
control only until forwarded, subject to hosting infrastructure, access, and provider contracts.

## Request lineage

For each flow, map:

`producer → transport/URL → request → claiming Client → event data → trigger → Transformation →
outbound tag → external endpoint → response`

- Confirm method, path, headers, payload, IDs, consent, and request source. In Server Preview, the
highest-priority matching Client claims the request; verify the winning Client and event data
instead of inferring from a tag name.
- Clients are adapters that interpret requests and build event data. One request can produce
multiple events; an HTTP request and a logical event are not the same count. GA4 can group several
events in one request.
- Verify which additional parameters a Client interprets; unmapped fields may not become event data.
Some tags forward fields without extra setup, so use Transformations to remove or minimize data that
must not leave.
- Use Transformations as explicit controls over fields exposed to tags by tag/type/context. Check
priority and conditions, then inspect in Preview what each tag actually received. Filtering only in
a final tag can leave data available to other tags.
- Account for retries, latency, timeouts, external responses, and failures. A GTM container is not a
durable queue or financial system. If reliable retries, auditable replay, or exactly-once behavior
are requirements, implement them in an appropriate architecture.

## Consent and privacy

Consent is signaled through the flow according to the implementation and signals recognized by
products. For the GA4 Client and Google tags in Server-side GTM, verify propagation of Web consent
parameters, state observed in Server Preview, and destination configuration. Google's guidance
describes setting up Consent Mode on Web for this flow; a specific CMP/integration may add
requirements.

Consent Mode is a technical mechanism, not a banner or legal-basis decision. Server-side processing
does not anonymize identifiable data; hashing alone is not anonymization. Define purpose, applicable
legal basis, retention, access, minimization, recipients, and exclusions with privacy/security
owners.

## Infrastructure and operations

Compare managed and manual hosting across actual requirements: regions, first-party domain/TLS,
variable costs, scaling, request limits, cold starts/latency, availability, logs, access controls,
deployment, updates, and incident ownership. Check current pricing/capacity in official
calculators/docs; estimates vary with traffic, template load, and Cloud Run or alternative
configuration.

Plan and measure at least:

- availability and latency by endpoint and region;
- volume received, claimed by Client, rejected/unclaimed, and sent by destination;
- failure/timeout rate and reason, event delay, and saturation signals;
- infrastructure, network transfer, and logging cost changes;
- Preview-version testing and isolation of the Preview server, which needs supported
topology/configuration and may require exactly one instance;
- configuration/service rollback, ownership, and alerts.

Configure DNS/HTTPS, source controls, network, and authentication according to the architecture and
provider documentation. Avoid logging full request bodies, PII, or sensitive headers. Do not confuse
the public tagging URL with the admin interface.

## Validation and cutover

Before migration, enumerate current emitters and destinations to avoid keeping the old path while
adding another in parallel. Test non-financial and negative events, granted/denied consent, IDs,
currency, removed fields, correct Client, multiple events per request, error responses, and
unavailability. Compare Web and Server to prove each scenario's transformation and endpoint.

Roll out by environment or cohort where possible. Define comparable denominators and rollback
criteria before cutover. After activation, verify requests, destination diagnostics, and
reconciliation separately. More requests or HTTP 2xx do not prove success.
