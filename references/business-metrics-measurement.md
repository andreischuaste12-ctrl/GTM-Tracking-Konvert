# Business metrics and measurement plans

Use this reference for measurement plans, KPIs, BI/dashboard requirements, data prioritization
beyond the funnel, or revenue reconciliation.

## 1. Define each metric before instrumentation

For every dashboard metric, record:

- formula and denominator;
- unit and currency;
- time window and timezone;
- source (GA4, ad platform, ecommerce/ERP, Merchant Center);
- owner;
- refresh frequency;
- allowed segments;
- known limits (consent, blockers, attribution, cancellations).

Keep denominators and cohorts consistent across periods. A metric without a source and owner does
not belong on the dashboard.

## 2. Ecommerce metric tree

Business outcome → eligible visitors → conversion (`view_item` → `add_to_cart` → `begin_checkout` →
`add_shipping_info` → `add_payment_info` → `purchase`) → repeat purchase/retention → net revenue and
margin.

Guardrails that must not deteriorate while optimizing the primary metric: cancellations/refunds,
unreconciled orders, duplicate events, purchases blocked by validation, complaints, and support
load.

## 3. Financial definitions tracking must support

- **Net revenue:** after discounts, cancellations, returns, and applicable taxes. `purchase` alone
measures recorded sales, not realized revenue; use the order's financial lifecycle
(paid/cancelled/refunded; GA4 `refund` with same `transaction_id`; Google Ads conversion
adjustments).
- **Gross margin:** (net revenue − direct costs) ÷ net revenue. For Google Ads, this can use cart
data on the conversion plus product cost in Merchant Center feed.
- **CAC:** attributable acquisition cost ÷ **new customers** for the same segment/period. It
requires a reliable new-customer rule (purchase history, not just a cookie/visitor).
- **LTV and retention:** state model, margin, and horizon; do not extrapolate immature cohorts.
- LTV/CAC alone is misleading when churn, margin, attribution, or period are poorly defined.

## 4. Attribution and evidence

- Channel attribution is an approximation. For investment decisions, triangulate with
incrementality/experiments and the financial source.
- Classify claims as **observed fact** (verifiable data), **reported statement** (what someone
says), **interpretation**, or **hypothesis**. Align these with tracking evidence (configured →
Preview → hit → accepted → deduplicated → reconciled).
- A small/convenience sample (few test orders) does not represent real behavior.

## 5. Select additional data based on the decision

Collect only data that changes the decision and has an observable source:

1. For net revenue, join orders to payment/cancellation/refund states from the financial source.
2. For margin, obtain direct item costs and align currency, period, and revenue definition.
3. For platform discrepancies, reconcile order by order before comparing aggregate totals.
4. For acquisition/retention, use reliable customer history; a cookie or visitor does not prove
someone is new.
5. For checkout abandonment, instrument failures only when the source platform exposes the result
and the denominator is definable.

## 6. Measurement experiment brief

Business question · hypothesis/mechanism · cohort · change tested · baseline · primary metric and
guardrails · success/failure threshold set in advance · duration/limits · cost/owner · result ·
decision (continue, adjust, pause, stop).

## 7. Data launch checklist

Before activating a campaign or significant change: funnel events instrumented; consent verified;
primary attribution/conversions validated; cancellation/refund handling defined; success and pause
criteria recorded before launch.
