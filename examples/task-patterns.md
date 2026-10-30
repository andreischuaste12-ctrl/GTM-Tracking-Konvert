# Synthetic task patterns

These examples demonstrate reasoning patterns. Names, IDs, and payloads are synthetic; they do not
describe a customer implementation. They are not proof that a production platform behaves the same.

## Duplicate purchase investigation

**Prompt:** “Two GTM tags appear to send `purchase`. Is the order counted twice?”

**Expected response pattern:** inspect both tag configurations, triggers, exceptions, sequencing,
consent, and paused state. Report configuration overlap separately from observed requests and
destination counting. Ask for Preview/request/destination evidence only for the unresolved layer.

## Currency-unit discrepancy

**Prompt:** “The source contract says `amount=89900`, currency `BRL`, unit `minor`.”

**Expected response pattern:** derive BRL 899.00 for a destination requiring major units, preserve
the stated source contract, and never infer units from magnitude or apply a global divide-by-100.

## Denied consent

**Prompt:** “All four Consent Mode signals are denied. Should there be no request?”

**Expected response pattern:** inspect the approved policy, tag checks, consent ordering, configured
Consent Mode, and actual requests. Do not assume denied consent means zero network traffic or claim
legal compliance from the technical signal.

## Late Pixel event ID

**Prompt:** “The browser Pixel and Server events have different IDs in Preview.”

**Expected response pattern:** compare the IDs against the same producer message, inspect event
ordering and asynchronous callbacks, and move ID creation into the producer's event payload when
needed. Verify the destination's exact field contract before claiming deduplication.

## Ambiguous acronym

**Prompt:** “Create a GTM plan for launch.”

**Expected response pattern:** clarify Google Tag Manager versus go-to-market if context does not
resolve the acronym. Do not start tag configuration for an explicitly go-to-market request.
