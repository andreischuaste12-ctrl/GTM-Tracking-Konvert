# GTM Tracking Konvert

**A practical implementation and audit playbook for reliable Google Tag Manager tracking.**

GTM Tracking Konvert turns measurement requirements into explicit event contracts, maintainable Google Tag Manager (GTM) implementations, and verifiable data flows. It covers GTM Web and server-side GTM, with a focus on Google Analytics 4 (GA4), Google Ads, consent-aware behavior, ecommerce, conversion deduplication, and implementation quality.

This repository is the project's operating guide and reference library. It currently contains documentation only; it is not an application, a published GTM container, or a service that runs tracking code.

## Mission

Deliver tracking implementations that are accurate, privacy-aware, testable, and maintainable. Every event must have a defined business purpose, an explicit data contract, a documented route to its destination, and evidence that it behaves as designed.

## What this project covers

- GTM Web data-layer design, event naming, triggers, variables, and tags.
- GA4 recommended events, custom events, ecommerce payloads, and Measurement Protocol.
- Google Ads conversion tracking and browser/server conversion deduplication.
- Consent Mode, consent defaults, consent updates, and consent-aware tag firing.
- Server-side GTM architecture, request clients, transformations, forwarding, and destination controls.
- Tag templates, Tag Manager API workflows, configuration audits, and troubleshooting.
- Implementation specifications, QA plans, release notes, rollback steps, and monitoring requirements.

## What this project does not cover

- General marketing, go-to-market planning, or analytics strategy without a GTM implementation requirement.
- Legal advice or decisions about the lawful basis for data collection. The applicable policy owner or qualified counsel must define those requirements.
- A guarantee that GTM, GA4, Google Ads, or server-side tagging will produce complete or legally compliant measurement by default.
- A runnable product or automated test suite. No application code, GTM container export, or test harness is currently included.

## Required implementation workflow

1. **State the measurement outcome.** Identify the user action, business purpose, destination, operating regions, consent requirements, and success criteria.
2. **Write the event contract before configuring tags.** Define the event name, trigger condition, required and optional parameters, types, allowed values, ownership, and expected destination.
3. **Map the complete data flow.** Record how application state enters the data layer, how GTM processes it, and how each tag, request, server-side transformation, and destination handles it.
4. **Apply privacy controls at every layer.** Minimize collection, enforce the approved consent policy, and prevent prohibited or unnecessary data from entering tags, requests, logs, or forwarded payloads.
5. **Define conversion counting and deduplication.** Name the authoritative conversion event and document the destination-supported identifier and matching behavior for browser and server events.
6. **Validate real behavior.** Inspect trigger timing, tag firing, request payloads, consent-allowed and consent-denied paths, repeated events, and destination debug tools.
7. **Prepare a controlled release.** Record the affected containers, tags, triggers, variables, approvals, test evidence, rollout plan, rollback procedure, and monitoring signals.

## Non-negotiable engineering rules

- **Every event has a contract.** Do not create production tags from undocumented assumptions.
- **Business events come from application state.** Prefer explicit data-layer events over DOM scraping, page-text parsing, or inferred user intent.
- **Collect only approved fields.** Never send direct identifiers such as email addresses or phone numbers to GA4 as standard event parameters. Use a platform's documented customer-data feature only when the policy owner has approved it and its consent and handling requirements are met.
- **Consent is runtime state.** Set the required defaults before relevant tags execute, apply user updates reliably, and test both granted and denied states.
- **One conversion must not count twice.** Document event ownership and use the receiving platform's documented deduplication mechanism whenever browser and server paths can report the same action.
- **Web and server containers have explicit boundaries.** Document what each layer receives, changes, removes, and forwards. Server-side routing does not by itself establish consent or data safety.
- **Secrets never belong in documentation or container exports.** Keep API keys, tokens, passwords, and other credentials in approved secret storage; redact them from examples, logs, and support artifacts.
- **Platform behavior follows current official documentation.** Recheck linked documentation before relying on a feature, limit, or API contract.
- **Legal requirements come from the approved policy owner.** Do not infer consent obligations from a tag configuration or a product document.

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

## Official references

These primary sources define platform behavior. Recheck the relevant documentation before implementation because product interfaces and specifications can change.

### Google Tag Manager and Tag Platform

- [Google Tag Manager Help Center](https://support.google.com/tagmanager/)
- [Google Tag Platform developer guides](https://developers.google.com/tag-platform)
- [The data layer](https://developers.google.com/tag-platform/tag-manager/datalayer)
- [Server-side tagging](https://developers.google.com/tag-platform/tag-manager/server-side)
- [Tag Manager API v2](https://developers.google.com/tag-manager/api/v2)
- [Consent settings in Tag Manager](https://support.google.com/tagmanager/answer/10718549?hl=en)
- [Consent APIs for tag templates](https://developers.google.com/tag-platform/tag-manager/templates/consent-apis)
- [Tag Assistant](https://tagassistant.google.com/)
- [Preview and debug containers](https://support.google.com/tagmanager/answer/6107056?hl=en)

### Google Analytics 4

- [GA4 event reference](https://developers.google.com/analytics/devguides/collection/ga4/reference/events)
- [GA4 ecommerce measurement](https://developers.google.com/analytics/devguides/collection/ga4/ecommerce)
- [GA4 Measurement Protocol](https://developers.google.com/analytics/devguides/collection/protocol/ga4)
- [GA4 DebugView](https://support.google.com/analytics/answer/7201382?hl=en)
- [Google Analytics policies](https://support.google.com/analytics/answer/6366371?hl=en)

### Consent and advertising conversions

- [Google tag consent mode](https://developers.google.com/tag-platform/security/guides/consent)
- [Google Ads website conversion tracking](https://support.google.com/google-ads/answer/6095821?hl=en)
- [Enhanced conversions for web](https://support.google.com/google-ads/answer/13258081?hl=en)

## License

This project is licensed under the [MIT License](LICENSE). Copyright © 2026 Andrei Schuaste.
