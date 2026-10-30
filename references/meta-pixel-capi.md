# Meta Pixel and Conversions API workflow

Use this guide for browser Pixel, server-side Conversions API (CAPI), or a combined event path.
Check the current Meta sources in the [official source catalog](official-references.md) before
making production claims.

## Map the event pair

For each logical business event, inventory every emitter: native storefront integration, Pixel tag,
custom HTML, server-side template, backend, and any partner integration. Record event name, source,
event time, ID, action source, value/currency, and approved user-data fields using synthetic or
redacted examples.

When browser and server report the same occurrence, use the current destination contract for the
event name and event ID. Generate a stable ID at the producer and carry it with the same business
event into both paths. Match the exact destination field/casing; a GTM variable named `event_id` is
not proof that the Meta payload contains the required field.

## Privacy and delivery

- Forward only approved, necessary fields. Hashing is not anonymization and does not replace
consent/purpose controls.
- Keep access tokens in approved secret storage. Never include tokens in templates, exports, logs,
fixtures, screenshots, or responses.
- Inspect Server Client selection, event data, Transformations, outbound template configuration,
endpoint, and response without exposing payload values.
- Treat an HTTP success as transport evidence only. Use the current Meta diagnostics/Test Events and
Events Manager evidence for receipt and deduplication; reporting can have additional latency and
limits.

## Debug a mismatch

1. Identify one logical event and its producer message.
2. Compare Pixel and CAPI event names, IDs, timestamps, and approved values for that same
   occurrence.
3. Inspect tag timing, retries, later data-layer messages, and any source that emits a second event.
4. Confirm the destination's diagnostics for the matched event pair.
5. Classify the outcome as configuration overlap, browser firing, server request, provider receipt,
deduplicated pair, or reported conversion. Do not collapse these states.
