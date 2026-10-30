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
