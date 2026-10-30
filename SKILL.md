---
name: gtm-tracking-konvert
description: >-
  Design, implement, and audit Google Tag Manager (GTM) tracking for websites, web applications,
  SaaS products, lead-generation flows, content experiences, and commerce using Web or server-side
  containers. Use for dataLayer, GA4, Consent Mode, Meta Pixel/CAPI, Google Ads conversions,
  deduplication, templates, the Tag Manager API, and server-side architecture. VTEX, Shopify, and
  WooCommerce are example source integrations, not required platforms. GTM means Google Tag
  Manager, not go-to-market. Do not invoke for GA4 reporting without GTM, Adobe Analytics, Segment,
  or go-to-market strategy.
metadata:
  short-description: "Google Tag Manager tracking engineering"
---
# Google Tag Manager tracking engineering

Treat tracking as a production data system. Events represent business facts with defined meaning,
identity, timing, unit, source, and consumers. Produce accurate, minimized, observable, and
reconcilable data. Do not maximize tag count or promise perfect collection.

GTM executes and routes instrumentation. It does not replace a transactional system, durable
integration layer, data warehouse, data governance, consent management platform (CMP), or financial
reconciliation. Server-side GTM changes where some processing occurs; it does not make data
complete, consented, attributable, or accepted by destinations.

## Select the route and read only what the task needs

- Tracking or data-layer design: [event contracts and
architecture](references/event-contracts-architecture.md), then [Web
workflow](references/workflow-web.md).
- GA4 event/ecommerce collection: [GA4 measurement workflow](references/ga4-measurement.md).
- Google Ads conversions or Enhanced Conversions: [Google Ads
  workflow](references/google-ads-conversions.md).
- Meta Pixel/CAPI pairing or deduplication: [Meta workflow](references/meta-pixel-capi.md).
- Source integration or application event producer: [source integration
adapters](references/source-integration-adapters.md).
- JSON export audit: run [`inventory_gtm_export.py`](scripts/inventory_gtm_export.py) for a
value-free structural summary, then use [audit evidence](references/audit-evidence.md); consult
[contracts, dependencies, and naming](references/contracts-dependencies-naming.md) when container
organization matters.
- SPA, consent, or browser investigation: [Web workflow](references/workflow-web.md).
- Server-side clients, transformations, templates, infrastructure, or outbound-data privacy: [Server
workflow](references/workflow-server.md).
- Permissions, workspaces, environments, API, versioning, or publication: [container governance and
release](references/container-governance-release.md).
- Custom Web or Server template development/review: [custom templates and
APIs](references/custom-templates-api.md).
- Server-side architecture, provisioning, operations, or cost: [server-side design and
operations](references/server-side-design-operations.md).
- CMP, Consent Mode, or page permission policy: consult [official
references](references/official-references.md) and the [Web workflow](references/workflow-web.md);
read template and Server guidance as needed.
- Ecommerce, orders, refunds, currency, revenue, or reconciliation: [ecommerce, money, and
reconciliation](references/ecommerce-money-reconciliation.md).
- Measurement plans, KPIs, or financial definitions: [business metrics and
measurement](references/business-metrics-measurement.md).
- Changes, imports, publication, production tests, or UI actions: [working mode and
release](references/working-mode-release.md).
- Review of another model's recommendation: check every claim against current artifacts using [audit
evidence](references/audit-evidence.md). Do not accept or reject the recommendation as a whole.
- A documented technical failure: [technical pitfalls](references/technical-pitfalls.md).
- A decision that depends on a platform feature, parameter, or requirement: verify [official
references](references/official-references.md) and the destination's current documentation.
- New event contract or audit deliverable: start from the [event contract
template](assets/event-contract.template.md) or [audit report
template](assets/audit-report.template.md).
- Ambiguous or multi-step request: use the [task decision
matrix](references/task-decision-matrix.md) to select a minimal workflow.
- Revenue reconciliation: use the [reconciliation template](assets/reconciliation.template.md) and
[ecommerce guidance](references/ecommerce-money-reconciliation.md).
- Example prompt/response patterns: [synthetic task patterns](examples/task-patterns.md).

## Invocation and context policy

Use this skill when the task requires Google Tag Manager configuration, GTM Web/Server behavior, or
an evidence-based decision about GTM tracking, regardless of industry or source platform. Common
projects include marketing sites, web apps, SaaS, lead generation, content, and commerce. Identify
the actual producer and source contract; do not assume an ecommerce event model, platform, currency,
or set of business events unless the supplied implementation supports it.

Do not use it for go-to-market strategy, GA4 reporting that does not involve GTM, or implementation
work centered on Adobe Analytics, Segment, or another tag manager. If the request mentions only
“GTM” ambiguously, clarify whether it means Google Tag Manager or go-to-market before applying this
workflow.

### Missing information

- Do not request a container ID or workspace just to inspect a supplied local export. State which
conclusions require live state and proceed with the available artifact.
- Before a live workspace mutation, identify the exact account/container, workspace, target
environment, intended change, and rollback boundary. If any is unknown, ask only for the missing
information and continue independent read-only work.
- If the source platform, destination, trigger condition, currency unit, or approved consent policy
is material but absent, do not infer it. Ask the smallest question that changes the recommendation
or label the conclusion as blocked/conditional.
- A request to implement tracking authorizes local/file changes in scope; it does not authorize
importing, publishing, sending a real financial event, or changing production settings.

### Operational safety

- **Hard block:** never disclose credentials or repeat personal-data values. Report only the
presence, location, and risk; redact values in notes and examples.
- **Explicit authorization required:** production publication, real purchases/conversions, imports
that overwrite a workspace, consent changes in production, or other external mutations.
- **Evidence required:** do not claim a tag fired, a destination accepted/counts an event, or
browser and server events deduplicated without evidence at the corresponding layer.
- **No network:** use the local artifact and this repository's reference snapshot; state that
current vendor behavior and link availability could not be verified. Never claim current
documentation was checked unless it was actually opened.

Use the [task decision matrix](references/task-decision-matrix.md) for minimum inputs, evidence, and
outputs by task type. Read only the references needed for the chosen path.

## Engineering principles

1. **Start with the business fact and its source.** Find who produces the event, when it becomes
true, which system is authoritative, and who consumes it. Do not create a GTM event to compensate
for a missing or ambiguous source fact.
2. **Define the contract before mapping tags.** Specify name, grain, semantic trigger, identity,
timestamp and timezone when relevant, properties, types, units, nullability, consent, destinations,
and duplicate policy. See [event contracts and
architecture](references/event-contracts-architecture.md).
3. **Trace end-to-end lineage.** For each critical event, map producer → data layer/request →
variable or Client → trigger → tag → outbound request → destination → report or reconciliation
system. Record the evidence for every observed step.
4. **Keep Web and Server separate.** They are different containers and runtimes. A Server Client
interprets requests and produces event data; outbound tags consume that data. Do not assume
variables, triggers, consent checks, or Preview behave identically in both.
5. **Apply purpose limitation and minimization.** Identify personal data and identifiers, justify
every destination, enforce consent, and remove unnecessary fields before forwarding. Hashing alone
is not anonymization. Never expose sensitive values in logs, exports, responses, or examples.
6. **Design for quality and maintenance.** Avoid duplicating business rules across tags, names that
conceal behavior, implicit currency conversions, fallbacks that turn invalid values into zero, and
timer-based deduplication without stable identity.
7. **Validate each layer with the right evidence.** Configuration does not prove execution;
execution does not prove a request; a request does not prove acceptance; acceptance does not prove
reporting or reconciliation. Use the evidence levels and limits in [audit
evidence](references/audit-evidence.md).
8. **Verify platform-dependent decisions against current official documentation.** APIs, destination
requirements, consent, recommended parameters, deduplication, limits, and infrastructure change.
Check the current page before advising on production.
9. **Govern changes as releases.** Distinguish workspaces, created versions, test environments, and
live versions. Review diffs, dependencies, conflicts, scope, and rollback. Creating a version is not
publishing; Preview is not production. See [container governance and
release](references/container-governance-release.md).
10. **Treat custom templates as executable code with limited capabilities.** Review implementation,
fields, permissions, and provenance; validate in the sandbox and with dedicated tests. A Gallery or
upstream template is not proof that installed code is equivalent. See [custom templates and
APIs](references/custom-templates-api.md).
11. **Evaluate Server-side by requirements and total cost.** Define what must be processed or routed
on the server and which controls that actually provides. Include event source, consent, domain,
availability, observability, latency, limits, scalability, and cost. See [server-side design and
operations](references/server-side-design-operations.md).

## Work sequence

Use the sequence that fits the request. Do not turn an audit into a refactor.

Carry out the requested work within its authorized scope. For implementation, modify available
artifacts and validate the result; do not stop at recommendations when a change was requested. For
an audit, remain read-only. Respond in the user's language by default; preserve exact English
product labels when needed.

1. Fix the objective, scope, source system, destinations, container/ID, and source state (export,
workspace, published, or observed in production).
2. Read existing implementation and conventions. Separate facts, inferences, unknowns, and required
data. Never invent event names, keys, IDs, CMPs, or contracts.
3. Define or verify the event contract and expected business outcome, including grain, identity,
currency/unit, and resend behavior.
4. Map Web and Server dependencies: data-layer ordering, resolved variables, conditions, exceptions,
consent, templates/permissions, and outbound routes.
5. Make the smallest coherent change and preserve unrelated behavior. Distinguish a proposal, file
edit, workspace edit, and publication.
6. Validate positive, negative, and repeated cases; applicable consent states; missing/invalid
fields; types/units; SPA behavior; and alternate routes. Use offline exports, template tests,
Preview, requests, destination tools, and reconciliation as relevant.
7. Report observations, passed/failed checks, test scope, destination differences, and remaining
environment or access dependencies.
8. For container changes, document before/after state, diff, affected dependencies, validation,
version/workspace, and whether the change was saved, versioned, sent to an environment, or
published.

## Interpretation and risk rules

- Read tag type, destination, configuration, triggers, exceptions, consent, sequencing, and status.
An object's name does not prove its behavior.
- Do not assume `purchase`, `page_view`, `event_id`, a GA4 tag, Pixel/CAPI, or an HTTP response
means what its name suggests. Verify payload and semantics at source and destination.
- Do not infer missing or duplicate events from aggregate counts alone. Align grain, time period,
timezone, filters, consent, identity, and platform rules.
- Check references and dependencies before renaming, pausing, deleting, importing, or reorganizing
objects. Folder and name changes do not fix tracking behavior.
- Do not publish, import into a workspace, trigger a real purchase, change production consent, or
make other external changes without applicable explicit authorization. Keep analysis read-only
unless the user explicitly authorizes a mutation.
- Never repeat tokens, credentials, email addresses, phone numbers, or personal-data payloads in
responses or files. Report presence, source, and risk without echoing values.
- If an external analysis conflicts with the export or UI, identify the current snapshot, verify its
hash/version, and reassess only affected components and dependencies.
- When guiding a UI action, use exact observed names and give one executable step at a time.
Distinguish saving a workspace from publishing.

## Audit delivery

Summarize the source and state examined; objective and scope; evidence-backed facts; issues by
impact and confidence; correct items to preserve; dependency-ordered remediation; validation and its
limits; and additional data needed. For changes, list modified files or objects and their final
state (local, workspace, Preview, destination, reconciled, or published). Never claim production
validation based only on configuration, simulation, or Preview.

Use the [response contract](references/response-contract.md) for audit, implementation, incident,
and release outputs. Keep simple factual answers concise; do not force a long report when the task
does not need one.
