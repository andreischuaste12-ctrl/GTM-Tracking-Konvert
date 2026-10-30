# Event contract: `<business_event_name>`

> Copy one contract per event. Replace every placeholder. Use synthetic data in examples.

## Purpose and ownership

- Business purpose:
- Business fact represented:
- Accountable data owner:
- Technical producer/owner:
- Source of truth:
- Approved destinations:
- Applicable regions and approved consent policy:

## Event semantics

- Destination event name(s):
- Exact firing condition:
- Explicit non-firing conditions:
- Grain (one event represents):
- Producer timestamp and timezone:
- Ingestion/send timestamp, if needed:
- Retry/replay behavior:
- Idempotency and deduplication rule:

## Identity

| Identifier | Source field | Scope | Stable across retries? | Destination use |
|---|---|---|---|---|
| Event ID | | | | |
| Entity ID (order/item/payment) | | | | |

## Parameters

| Field | Meaning | Type | Unit/format | Required? | Nullable? | Sensitive? | Allowed destinations | Validation |
|---|---|---|---|---|---|---|---|---|
| | | | | | | | | |

## Monetary semantics, if applicable

- Currency (ISO 4217):
- Amount unit (major/minor):
- Includes discounts:
- Includes shipping:
- Includes tax:
- Rounding rule:
- Expected reconciliation formula/source:

## Consent and privacy

- Consent signals required before collection:
- Behavior when consent is denied or withdrawn:
- Data minimization/removal rules:
- Personal/sensitive fields expressly prohibited:
- Retention/access requirements from approved policy:

## Data flow and validation

`producer → data layer/request → GTM Web → optional GTM Server → destination → reporting/reconciliation`

| Scenario | Input/consent state | Expected producer event | Expected tag/request | Expected destination result | Evidence collected |
|---|---|---|---|---|---|
| Valid event | | | | | |
| Missing/invalid field | | | | | |
| Duplicate/retry | | | | | |
| Consent denied/withdrawn | | | | | |

## Change control

- Version/date:
- Compatibility/migration notes:
- Test owner and result:
- Release/rollback plan:
- Open assumptions:
