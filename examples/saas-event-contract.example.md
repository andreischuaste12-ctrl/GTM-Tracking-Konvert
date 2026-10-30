# Example event contract: SaaS trial activation

This is a synthetic example of an application event. Names, IDs, and lifecycle are illustrative;
replace them with the actual application contract. It is not a Google or GTM recommended event.

## Business fact

- **Event:** `trial_activated`
- **Meaning:** the backend confirms that an account entered the trial state.
- **Grain:** one event per account transition into trial.
- **Producer/source of truth:** subscription backend; the browser click is not authoritative.
- **Destination:** GA4 custom event, if this event is approved and useful for the measurement plan.
- **Retry rule:** retries reuse the same event ID; the receiver's deduplication behavior must be
  confirmed before claiming exactly-once processing.

## Synthetic producer payload

```javascript
window.dataLayer = window.dataLayer || [];
window.dataLayer.push({
  event: "trial_activated",
  event_id: "evt_synthetic_001",
  plan_category: "team"
});
```

The example excludes account email, user name, and raw form data. Add fields only when their source,
purpose, approval, consent, and destination use are documented.

## QA cases

| Scenario | Expected producer behavior | Review evidence |
|---|---|---|
| Backend confirms trial | One event for the state transition | Producer log or test event with synthetic identifiers |
| Visitor only clicks “Start trial” | No `trial_activated` event | Confirm click and backend states are separate |
| Backend retries delivery | Same logical event identity is preserved | Compare producer, data layer, request, and destination diagnostics |
| Consent denies this use | Follow the approved policy for the selected destination | Preview state and actual request, without inferring legal compliance |
