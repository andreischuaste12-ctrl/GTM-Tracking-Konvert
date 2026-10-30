# Official documentation and platform details to recheck

Consult these pages for production decisions. Link and guidance review date: 2026-10-16. Platform details change; confirm current versions, destination requirements, region/consent, and deployed architecture. This list directs research; it does not replace reading the documentation.

## Web and data layer

- [The data layer — Tag Platform](https://developers.google.com/tag-platform/tag-manager/datalayer): `dataLayer.push` events, message queue, state, and naming requirements.
- [Google tag — Tag Platform](https://developers.google.com/tag-platform/gtagjs): Google tag configuration and events.
- [Measure single-page applications with Google Tag Manager — GA4](https://developers.google.com/analytics/devguides/collection/ga4/measure-spa-gtm): route changes, manual page views, history triggers, and duplicate prevention.
- [Custom templates quick start — GTM Templates](https://developers.google.com/tag-platform/tag-manager/templates): templates, fields, permissions, and tests.
- [Sandboxed JavaScript — GTM Templates](https://developers.google.com/tag-platform/tag-manager/templates/sandboxed-javascript): runtime restrictions; custom templates are not ordinary browser JavaScript.
- [Custom template APIs](https://developers.google.com/tag-platform/tag-manager/templates/api): Web template APIs and tests.
- [Custom template permissions](https://developers.google.com/tag-platform/tag-manager/templates/permissions): capabilities granted and restrictions for Web templates.
- [Template tests](https://developers.google.com/tag-platform/tag-manager/templates/tests): mocks and assertions; unit tests do not verify validation rules or real API permissions.
- [Custom template policies](https://developers.google.com/tag-platform/tag-manager/templates/policies): page policies can restrict template permissions.

## Consent, security, and privacy

- [Consent mode overview](https://developers.google.com/tag-platform/security/concepts/consent-mode): responsibility for choice/signals and tag behavior; Basic vs. Advanced.
- [Set up consent mode on websites](https://developers.google.com/tag-platform/security/guides/consent): APIs and ordering; implement according to CMP and jurisdiction.
- [Consent mode with server-side Tag Manager](https://developers.google.com/tag-platform/tag-manager/server-side/consent-mode): Web-to-Server flow and container requirements.
- [Tag Manager consent mode support](https://support.google.com/tagmanager/answer/10718549): Consent Initialization, built-in/additional checks, and Consent Overview.
- [Tag Platform security and privacy](https://developers.google.com/tag-platform/security): permissions, container governance, and privacy.

Consent Mode is a technical mechanism for communicating signals and tag behavior. It is not a banner, CMP, legal basis, or compliance determination. Permitted configuration depends on current business and legal requirements.

## Server-side Tag Manager

- [Introduction to server-side tagging](https://developers.google.com/tag-platform/tag-manager/server-side/intro): architecture, Clients, event data, and controls.
- [Send data to server-side Tag Manager](https://developers.google.com/tag-platform/tag-manager/server-side/send-data): traffic sources, Client configuration, priority, and event data.
- [Transformations](https://developers.google.com/tag-platform/tag-manager/server-side/transformations): include, enrich, or exclude fields exposed to tags and verify in Preview.
- [Preview and debug server containers](https://developers.google.com/tag-platform/tag-manager/server-side/debug): inspect requests, winning Client, events, and outputs.
- [Server-side tagging APIs](https://developers.google.com/tag-platform/tag-manager/server-side/api): APIs and template permissions.
- [Manual setup guide](https://developers.google.com/tag-platform/tag-manager/server-side/manual-setup-guide): infrastructure provisioning, configuration, and maintenance.
- [Google Ads user-provided data in Server-side GTM](https://developers.google.com/tag-platform/tag-manager/server-side/ads-user-data): architecture and migration; verify current identity and consent requirements.

Evaluate first-party domain, TLS, latency, availability, scalability, observability, access, cost, retention, and environment ownership. Server-side enables processing/routing controls, but the hosting provider still operates infrastructure. Do not claim it removes browser restrictions, guarantees attribution, makes data first-party by itself, or bypasses consent.

For cost and sizing, check current official [Server-side Tag Manager](https://developers.google.com/tag-platform/tag-manager/server-side/overview), [Cloud Run setup](https://developers.google.com/tag-platform/tag-manager/server-side/cloud-run-setup-guide), and Cloud Run pricing documentation. Published price and instance recommendations are snapshots, not current quotes.

## Governance, APIs, and single-page applications

- [Tag Manager API overview](https://developers.google.com/tag-platform/tag-manager/api/v2): resources and account/container/workspace/version hierarchy.
- [Tag Manager API developer guide](https://developers.google.com/tag-platform/tag-manager/api/v2/devguide): programmatic workflows and OAuth.
- [Tag Manager API reference](https://developers.google.com/tag-platform/tag-manager/api/reference/rest): workspace, status, version, and publish methods.
- [Tag Manager API quotas](https://developers.google.com/tag-platform/tag-manager/api/v2/limits-quotas): current limits and quota policies.

In Server-side GTM, distinguish requests received by a Client from calls to the Measurement Protocol endpoint. Check Client and destination capabilities before selecting a route.

## Analytics and ecommerce

- [Measure ecommerce — GA4](https://developers.google.com/analytics/devguides/collection/ga4/ecommerce): events, ecommerce parameters, `items`, currency, and values.
- [Recommended events — Analytics Help](https://support.google.com/analytics/answer/9267735): recommended names and parameters.
- [Validate ecommerce setup](https://developers.google.com/analytics/devguides/collection/ga4/validate-ecommerce): DebugView and duplicate/structure diagnostics.
- [Ecommerce scopes — Analytics Help](https://support.google.com/analytics/answer/12947610): event- and item-scoped parameters.

Verify current destination, required/recommended parameters, limits, deduplication, modeling, attribution, and latency in each platform's documentation. Do not generalize a GA4 rule to Ads, Meta, or another endpoint.

## Review log

When adding platform-dependent rules, record the official link, review date, and confirmed version/feature. Remove obsolete details instead of accumulating conflicting instructions.
