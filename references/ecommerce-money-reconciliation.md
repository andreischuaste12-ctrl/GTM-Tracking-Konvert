# Ecommerce, money, and reconciliation

## One contract per producer and event

Before normalizing amounts, build a source/consumer/event table with data path, currency, unit
(reais/centavos), discount/shipping/tax inclusion, order ID, and Preview evidence. Only then define
conversion. Never divide every amount by 100 or infer a unit from magnitude. `899` could mean
R$899.00; `89900` could mean centavos; the source defines the interpretation.

Separate:

- GA4 `purchase.value`: item value after discount, excluding separately included shipping and taxes,
according to current GA4 documentation.
- Buyer-paid total: transaction total defined by the source contract.
- Meta/Google Ads value: each integration's contract and fields; verify current documentation and
the installed tag/template.
- `shipping`, `tax`, item `price`, quantity, and currency: explicit fields with defined units.

Do not equate platform reports until window, currency, attribution, revenue definition,
refunds/cancellations, and actual receipt are aligned. An order cancelled after `purchase` fired
does not prove the event was wrong; inspect refund/cancellation and reporting policy.

## Order integrity

For a purchase, resolve ID, items, currency, net subtotal, shipping, tax, and total as **one
validated order**. Do not select an ID from one object and value/items from another transaction
without proof they belong to the same event. `orderFormId`, `transaction_id`, and payment ID are not
interchangeable.

Validate items and calculations at platform precision/cent units: valid non-negative price, valid
quantity, consistent currency, present IDs, and total reconciled with the source definition. Reject
explicitly with a useful reason. Do not remove `discount` or allocate a global discount by SKU
without evidence about the allocation. The order sum can match while item revenue is wrong.

Do not let a fallback send a `purchase` rejected by primary validation. If recovery is necessary,
apply the same financial and identity criteria and record status/reason. If insufficient data is
common, report an unreconciled purchase in controlled diagnostics; an `undefined` variable does not
automatically prevent a tag from firing.

## Evidence and reconciliation

Use the canonical [evidence ladder](audit-evidence.md) for each purchase. One stage does not prove
the next. If a store event is absent, its absence from a report does not locate the failure. Without
browser, consent, Server, and response logs, state the cause is unknown and seek denominators and
controls. Do not attribute causality to payment method, antifraud delay, source, or discount from a
few examples without comparison groups and denominators.

For quantification, deduplicate by the appropriate order ID; align range/timezone, final states,
currency, gross/net, shipping/fees, and cancellation/refund. Separate unmatched orders, revenue
differences, and duplicates; use category rates only with comparable denominators.

## Order financial lifecycle

`purchase` records the sale at the moment defined by the source contract; realized revenue can
change after payment, cancellation, and refund. For net revenue, use financial-source states and
send `refund` or conversion adjustments according to each destination's current contract. Preserve
the same transaction ID; a payment update must not emit a second purchase. See [business metrics and
measurement](business-metrics-measurement.md).

Verify current official Google Analytics, GTM, Ads, or Meta requirements before implementing any
decision that depends on them.
