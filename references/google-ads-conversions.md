# Google Ads conversion workflow

Use this guide when GTM implements or audits Google Ads website conversions, Enhanced Conversions,
or later conversion adjustments. Verify current requirements in the [official source
catalog](official-references.md).

## Define the conversion action

- Name the business outcome, conversion action, source event, owner, and counting rule.
- Set the conversion trigger from an observed source fact. Do not fire a purchase from a
  confirmation
page alone if the application can revisit that page or the transaction is not validated.
- Define whether the action counts one or multiple conversions per ad interaction according to the
business use case and current Ads setting.
- Map value and currency from the source contract. State whether the value represents item revenue,
buyer-paid total, margin, or another explicit measure.
- Preserve a stable order/transaction identifier when the destination's current conversion contract
requires it. Keep the ID consistent across retries and supported browser/server paths.

## Enhanced Conversions and user-provided data

Enhanced Conversions are a platform-specific user-data feature, not permission to place personal
identifiers in generic analytics parameters. Confirm approved purpose, consent, allowed fields,
normalization, hashing/transport responsibilities, retention, and redaction from current Google Ads
documentation and the responsible policy owner. Never copy submitted email/phone values into GTM
examples, logs, reports, or this repository.

## Conversion Linker and click identifiers

- Check whether auto-tagging is enabled and whether the landing URL carries the expected click
  identifier for the account and traffic type. Do not assume every click uses `gclid`; current
  Google Ads flows can use other identifiers.
- Use the Google Tag Manager Conversion Linker guidance for the selected site and consent setup.
  Verify tag scope, firing order, domain/cookie behavior, redirects, and cross-domain journeys where
  relevant; do not copy cookie settings from another site.
- Test landing, navigation, and conversion paths with consent states required by the approved
  policy. Confirm what identifier state survives to the conversion tag without exposing click IDs
  in logs or unrelated destinations.
- A stored click identifier does not prove a conversion fired, was accepted, or was attributed.
  Keep linker configuration, conversion request evidence, and Ads reporting as separate checks.

The [official source catalog](official-references.md) links to Google's current Conversion Linker
and auto-tagging documentation. Confirm the applicable identifier and consent behavior there before
production changes.

## Validate and reconcile

- Inspect the actual conversion tag/action ID, trigger, exception, consent behavior, value/currency,
and transaction ID.
- Confirm the source event and outbound request in Preview/network evidence.
- Use Google Ads diagnostics and conversion reporting after the documented processing delay.
- If conversions are adjusted for cancellation/refund, verify the current adjustment workflow,
matching identity, eligibility, and timing.
- Report tag firing, request receipt, conversion action acceptance, Ads reporting, and financial
reconciliation as separate evidence states.

Do not claim a conversion is counted from a tag name or HTTP response. Do not transfer GA4
deduplication, value, or user-data rules to Google Ads without a current Ads source.
