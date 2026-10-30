# Official source catalog

**Catalog update:** 2026-10-30. The current managed environment blocks requests to some vendor
documentation hosts. Links below are official-source entry points, but live reachability and the
current contents of every page have not been verified from this environment. Do not state that a
page or feature was checked unless it was opened during the task.

Use these sources to verify current implementation rules. The live platform documentation and the
installed container/template remain authoritative for the specific task. Record the page, feature,
date accessed, and relevant version when an implementation decision depends on a platform rule.

## Google Tag Manager and Tag Platform

- [Tag Platform developer guides](https://developers.google.com/tag-platform) — entry point for
Google tag, GTM, measurement, security, and server-side documentation.
- [Google Tag Manager Help Center](https://support.google.com/tagmanager/) — product UI, Preview,
workspaces, imports, versions, and container administration.
- [The data layer](https://developers.google.com/tag-platform/tag-manager/datalayer) — event pushes,
queue/state behavior, naming, and data-layer implementation.
- [Tag Assistant](https://tagassistant.google.com/) — browser-assisted tag diagnostics.
- [Preview and debug containers](https://support.google.com/tagmanager/answer/6107056?hl=en) —
Preview setup and browser-side inspection.
- [Tag Manager API v2 overview](https://developers.google.com/tag-platform/tag-manager/api/v2) —
API resources, account/container/workspace/version hierarchy, and operations.
- [Tag Manager API REST
reference](https://developers.google.com/tag-platform/tag-manager/api/reference/rest) — method-level
request and response schemas.
- [Tag Manager API
quotas](https://developers.google.com/tag-platform/tag-manager/api/v2/limits-quotas) — current quota
and rate limits.

## Consent, security, and privacy

- [Consent Mode overview](https://developers.google.com/tag-platform/security/concepts/consent-mode)
— consent signals, tag behavior, and Basic/Advanced mode concepts.
- [Set up Consent Mode on
websites](https://developers.google.com/tag-platform/security/guides/consent) — supported APIs and
implementation ordering. Align the implementation with the approved CMP and jurisdiction-specific
policy.
- [Consent settings in Tag Manager](https://support.google.com/tagmanager/answer/10718549?hl=en)
— Consent Initialization, built-in/additional checks, and Consent Overview.
- [Consent APIs for tag
templates](https://developers.google.com/tag-platform/tag-manager/templates/consent-apis) — template
APIs for default and updated consent state.
- [Tag Platform security and privacy](https://developers.google.com/tag-platform/security) —
platform security and privacy guidance.
- [Google Analytics policies](https://support.google.com/analytics/answer/6366371?hl=en) —
Analytics data collection and policy requirements, including prohibited data.

Consent Mode is a technical signal/behavior mechanism. It is not a consent banner, CMP, legal basis,
or compliance determination.

## GTM templates

- [Custom template quick start](https://developers.google.com/tag-platform/tag-manager/templates)
— template structure and workflow.
- [Sandboxed
JavaScript](https://developers.google.com/tag-platform/tag-manager/templates/sandboxed-javascript) —
Web template runtime restrictions.
- [Custom template APIs](https://developers.google.com/tag-platform/tag-manager/templates/api)
— supported template APIs.
- [Custom template
permissions](https://developers.google.com/tag-platform/tag-manager/templates/permissions) —
declared capabilities and constraints.
- [Template tests](https://developers.google.com/tag-platform/tag-manager/templates/tests)
— unit test behavior and limits.
- [Custom template
policies](https://developers.google.com/tag-platform/tag-manager/templates/policies) — page policies
that can restrict template permissions.

Template unit tests and mocks do not prove real network access, production permission behavior, or
destination acceptance.

## Server-side Tag Manager

- [Server-side tagging
introduction](https://developers.google.com/tag-platform/tag-manager/server-side/intro) —
architecture, Clients, event data, and controls.
- [Send data to server-side Tag
Manager](https://developers.google.com/tag-platform/tag-manager/server-side/send-data) — traffic
sources, Client configuration, priority, and event data.
- [Server-side consent
mode](https://developers.google.com/tag-platform/tag-manager/server-side/consent-mode) — consent
propagation and server-container behavior.
- [Transformations](https://developers.google.com/tag-platform/tag-manager/server-side/transformations)
— include, enrich, or exclude event fields exposed to tags.
- [Preview and debug server
containers](https://developers.google.com/tag-platform/tag-manager/server-side/debug) — inspect
requests, Client selection, events, and outbound tags.
- [Server-side template
APIs](https://developers.google.com/tag-platform/tag-manager/server-side/api) — APIs and permissions
for Server templates.
- [Manual setup
guide](https://developers.google.com/tag-platform/tag-manager/server-side/manual-setup-guide) —
infrastructure setup and maintenance.
- [Cloud Run
setup](https://developers.google.com/tag-platform/tag-manager/server-side/cloud-run-setup-guide) —
supported Cloud Run deployment guidance.
- [Cloud Run pricing](https://cloud.google.com/run/pricing) — current pricing; estimates depend on
traffic, region, execution time, and configuration.
- [Google Ads user-provided data in Server-side
GTM](https://developers.google.com/tag-platform/tag-manager/server-side/ads-user-data) — supported
architecture and handling requirements.

Verify topology and instance requirements for the selected hosting model. Do not generalize Preview
server constraints to production tagging-server scaling.

## Google Analytics 4

- [GA4 event
reference](https://developers.google.com/analytics/devguides/collection/ga4/reference/events) —
recommended event names and parameters.
- [GA4 ecommerce
measurement](https://developers.google.com/analytics/devguides/collection/ga4/ecommerce) — ecommerce
event and item schemas, currency, shipping, tax, and value.
- [Validate ecommerce
setup](https://developers.google.com/analytics/devguides/collection/ga4/validate-ecommerce) —
DebugView and diagnostics for ecommerce payloads.
- [GA4 Measurement
Protocol](https://developers.google.com/analytics/devguides/collection/protocol/ga4) —
server-to-server collection requirements and payload behavior.
- [Measurement Protocol validation
server](https://developers.google.com/analytics/devguides/collection/protocol/ga4/validating-events)
— development-time event validation.
- [GA4 DebugView](https://support.google.com/analytics/answer/7201382?hl=en) — debug event
visibility and limitations.
- [Measure single-page applications with
GTM](https://developers.google.com/analytics/devguides/collection/ga4/measure-spa-gtm) — route
changes, page views, and duplicate prevention.
- [Enhanced measurement](https://support.google.com/analytics/answer/9216061?hl=en) — automatic
measurement configuration and limits.

## Google Ads

- [Website conversion tracking](https://support.google.com/google-ads/answer/6095821?hl=en) —
conversion setup and implementation options.
- [Enhanced conversions for web](https://support.google.com/google-ads/answer/13258081?hl=en) —
supported user-provided data and implementation requirements.
- [Google Ads conversion adjustments](https://support.google.com/google-ads/answer/7686447?hl=en)
— adjustments for later conversion changes; verify current eligibility and API/UI workflow.

## Meta Pixel and Conversions API

- [Meta Pixel documentation](https://developers.facebook.com/docs/meta-pixel/) — browser Pixel
setup and event implementation.
- [Conversions API
documentation](https://developers.facebook.com/docs/marketing-api/conversions-api/) — server event
setup, fields, and operational requirements.
- [Deduplicate Pixel and server
events](https://developers.facebook.com/docs/marketing-api/conversions-api/deduplicate-pixel-and-server-events/)
— event name/ID matching and deduplication behavior.

Confirm exact event name, ID field/casing, user-data handling, consent, diagnostics, and
deduplication requirements in the current Meta docs. Never infer acceptance from an HTTP response
alone.

## Source commerce platforms

The skill is source-platform-neutral. Use a platform's current official contract and installed
implementation; never copy fields such as VTEX `orderFormId` into another platform's schema.

- [VTEX developer documentation](https://developers.vtex.com/docs/) — search for the installed
Pixel app, event APIs, order lifecycle, and data-layer integrations.
- [Shopify developer documentation](https://shopify.dev/docs) — search for Web Pixels, customer
events, privacy settings, and storefront/checkout constraints.
- [WooCommerce documentation](https://woocommerce.com/documentation/) — verify order lifecycle,
checkout hooks, and the exact installed analytics integration/plugin.

## Link and content review

This catalog is a set of official starting points, not proof that every URL is reachable or every
listed behavior is current. A CI link check can flag reachability regressions; it cannot establish
that a platform rule applies to a specific account, region, product version, or consent policy.
Record `checked_on`, product/version, exact feature, and source URL when a live decision is
verified. If network access is unavailable, mark the source unverified and continue with local
evidence without claiming a current-doc check.
