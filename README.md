# GTM Tracking Konvert

**A practical implementation and audit playbook for reliable Google Tag Manager tracking.**

GTM Tracking Konvert is an industry- and platform-neutral skill for turning measurement requirements
into explicit event contracts, maintainable Google Tag Manager (GTM) implementations, and verifiable
data flows. It supports websites, web applications, SaaS products, lead-generation flows, content
experiences, and commerce when they use GTM Web or server-side GTM. GA4, Google Ads, and Meta
Pixel/Conversions API are supported destinations. VTEX, Shopify, ecommerce, and BRL are examples or
optional specialized topics, never defaults; use the actual source and destination contracts for
each implementation.

This repository packages the project's operating guide, a routed skill, focused references, reusable
templates, synthetic evaluation fixtures, example audit/inventory outputs, and a read-only GTM export
inventory tool. It is not an application, a published GTM container, or a service that runs tracking
code.

## Mission

Deliver tracking implementations that are accurate, privacy-aware, testable, and maintainable. Every
event must have a defined business purpose, an explicit data contract, a documented route to its
destination, and evidence that it behaves as designed.

## What this project covers

- GTM Web data-layer design, event naming, triggers, variables, and tags.
- Measurement for page views, navigation, sign-ups, subscriptions, leads, forms, content engagement,
  and other application-defined business events.
- GA4 recommended and custom events, optional ecommerce payloads, and Measurement Protocol.
- Google Ads conversion tracking, including Conversion Linker, click identifiers, Enhanced
  Conversions, consent, and conversion validation.
- Meta Pixel/Conversions API event routing and browser/server deduplication.
- Consent Mode, consent defaults, consent updates, and consent-aware tag firing.
- Server-side GTM architecture, request clients, transformations, forwarding, and destination
controls.
- Tag templates, Tag Manager API workflows, configuration audits, and troubleshooting.
- Implementation specifications, QA plans, release notes, rollback steps, and monitoring
requirements.
- Structural inventory of GTM exports with a SHA-256 digest, entity/reference counts, regex review
  prompts, and tag-sequencing cycle warnings.

## What this project does not cover

- General marketing, go-to-market planning, or analytics strategy without a GTM implementation
requirement.
- Legal advice or decisions about the lawful basis for data collection. The applicable policy owner
or qualified counsel must define those requirements.
- A guarantee that GTM, GA4, Google Ads, or server-side tagging will produce complete or legally
compliant measurement by default.
- A live tracking application or GTM container.
- Platform-specific field names, currency units, or consent requirements inferred from VTEX, BRL, or
any other example.
- Tracking projects that do not use Google Tag Manager.

## Required implementation workflow

For the agent's canonical task sequence, see [Work sequence in SKILL.md](SKILL.md#work-sequence).
This checklist is a short project-owner summary for planning and review.

1. **State the measurement outcome.** Identify the user action, business purpose, destination,
operating regions, consent requirements, and success criteria.
2. **Write the event contract before configuring tags.** Define the event name, trigger condition,
required and optional parameters, types, allowed values, ownership, and expected destination.
3. **Map the complete data flow.** Record how application state enters the data layer, how GTM
processes it, and how each tag, request, server-side transformation, and destination handles it.
4. **Apply privacy controls at every layer.** Minimize collection, enforce the approved consent
policy, and prevent prohibited or unnecessary data from entering tags, requests, logs, or forwarded
payloads.
5. **Define conversion counting and deduplication.** Name the authoritative conversion event and
document the destination-supported identifier and matching behavior for browser and server events.
6. **Validate real behavior.** Inspect trigger timing, tag firing, request payloads, consent-allowed
and consent-denied paths, repeated events, and destination debug tools.
7. **Prepare a controlled release.** Record the affected containers, tags, triggers, variables,
approvals, test evidence, rollout plan, rollback procedure, and monitoring signals.

## Non-negotiable engineering rules

- **Every event has a contract.** Do not create production tags from undocumented assumptions.
- **Business events come from application state.** Prefer explicit data-layer events over DOM
scraping, page-text parsing, or inferred user intent.
- **Collect only approved fields.** Never send direct identifiers such as email addresses or phone
numbers to GA4 as standard event parameters. Use a platform's documented customer-data feature only
when the policy owner has approved it and its consent and handling requirements are met.
- **Consent is runtime state.** Set the required defaults before relevant tags execute, apply user
updates reliably, and test both granted and denied states.
- **One conversion must not count twice.** Document event ownership and use the receiving platform's
documented deduplication mechanism whenever browser and server paths can report the same action.
- **Web and server containers have explicit boundaries.** Document what each layer receives,
changes, removes, and forwards. Server-side routing does not by itself establish consent or data
safety.
- **Secrets never belong in documentation or container exports.** Keep API keys, tokens, passwords,
and other credentials in approved secret storage; redact them from examples, logs, and support
artifacts.
- **Platform behavior follows current official documentation.** Recheck linked documentation before
relying on a feature, limit, or API contract.
- **Legal requirements come from the approved policy owner.** Do not infer consent obligations from
a tag configuration or a product document.

## Audit checklist

### Event contract and payload

- Does every event have a documented purpose, owner, trigger, schema, and destination?
- Are event names and parameter types consistent across application, GTM, and destination?
- Are ecommerce items, value, currency, and transaction identifiers populated consistently?
- Are fields constrained to the approved minimum, with no prohibited personal data?

### GTM behavior and consent

- Does each trigger fire at the correct point and only the intended number of times?
- Are consent defaults established before tags that depend on them can run?
- Do consent updates change tag behavior correctly in both granted and denied states?
- Are tag, trigger, and variable dependencies documented and maintainable?

### Conversion and server-side flow

- Is the authoritative conversion action identified?
- Are browser and server reports deduplicated using the destination's documented method?
- Do server-side clients parse only intended requests?
- Do transformations remove unapproved fields and forward data only to approved destinations?
- Are failures, retries, and monitoring signals defined?

### Release evidence

- Was the implementation inspected in GTM Preview or Tag Assistant?
- Were representative network requests and payloads checked?
- Was GA4 DebugView or the applicable destination diagnostic used where supported?
- Were repeated events and both consent paths exercised?
- Are test evidence, release steps, rollback, and monitoring documented?

## Deliverables

Each implementation or audit must produce the relevant subset of these artifacts:

- Measurement requirements and event contract.
- Data-flow diagram or written flow from application to destination.
- GTM configuration specification, including triggers, variables, tags, and consent behavior.
- Server-side processing and forwarding rules, when applicable.
- QA matrix with expected and observed results.
- Findings prioritized by impact, with concrete remediation steps.
- Release, rollback, ownership, and monitoring notes.

Reusable event-contract, QA-matrix, audit-report, and reconciliation templates are in [`assets/`](assets/);
filled audit and inventory examples are in [`examples/`](examples/). Run
the read-only inventory tool with `python3 scripts/inventory_gtm_export.py
path/to/container-export.json`; it reports structural checks only and does not validate runtime
behavior, destination acceptance, consent compliance, or reconciliation. The synthetic scenarios in
[`evals/`](evals/) include manual response criteria; they are not an automated model-evaluation
harness.

Run local repository checks with `python3 scripts/check_docs.py` and `python3 -m unittest discover
-s tests -v`.

## Official reference catalog

Keep platform links and verification status in one place: [official
references](references/official-references.md). This environment cannot reach every vendor
documentation host, so unverified links are labeled accordingly; never claim a page was checked
unless the page was actually opened.

See the [changelog](CHANGELOG.md) for repository changes and [examples](examples/) for synthetic
task, event-contract, audit-report, and inventory-output examples.

## Quick start

Provide the task, the relevant artifact (export, workspace evidence, payload, or source contract),
and the expected decision. Example prompts:

- “Audit this GTM export for duplicate purchase paths. Keep the audit read-only and cite the
evidence for each finding.”
- “Create an event contract for this checkout event using the attached producer payload; do not
invent missing fields.”
- “Audit the SaaS trial signup flow from application event through GTM to GA4. Separate
  configuration evidence from observed delivery.”
- “Design a privacy-aware lead form measurement plan. Distinguish a submitted form from a lead
  accepted by the backend.”
- “Investigate whether this Web/Server Meta event pair is deduplicated. Separate configuration from
destination evidence.”
- “Review this consent-denied Preview trace against the approved policy. Do not assume denied
consent means no request.”

## License

This project is licensed under the [MIT License](LICENSE). Copyright © 2026 Andrei Schuaste.
