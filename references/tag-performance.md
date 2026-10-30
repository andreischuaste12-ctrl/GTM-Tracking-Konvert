# Tag performance and load order

Use this reference when pages are slow, tags fire late or too early, or the container has grown
without review. Performance claims need measurements; do not infer them from tag count.

## What to measure

- Container size and the number of tags that run per page type, from Preview and the network
  panel, not only from the export.
- Main-thread cost and blocking time from a profile on a representative page and device class.
  Use lab tools to find causes and field data to judge impact on users.
- Timing of the critical tags (consent defaults, Google tag, conversion tags) relative to the
  events that depend on them.

## Common causes to inspect

- Custom HTML tags that load libraries synchronously, write to the DOM, or poll in a timer.
- Triggers that fire on every page or every event when the tag needs one route or one event.
- Duplicate loaders for the same vendor (a native integration plus a GTM tag).
- Tag sequencing and "wait for tags" settings that delay user interaction or navigation.
- Large lookup tables or custom JavaScript variables evaluated on every event.

## Load order

1. Consent defaults, in the Consent Initialization stage, before anything that depends on them.
2. The Google tag and shared configuration.
3. Event tags after their producing event or trigger.
4. Third-party marketing tags after consent and on the specific events that need them.

A faster order that breaks consent, event ID, or conversion timing is a regression. Re-run the
[QA matrix](../assets/qa-matrix.template.md) after any ordering change.

## Change discipline

- Remove or pause only after checking references and the destination's use of the tag; record the
  rollback version (see [container governance](container-governance-release.md)).
- Prefer a vendor template over Custom HTML when one exists and its permissions are reviewed.
- Report the before and after measurement with the page, device class, and tool used. If the
  effect was not measured, say it was not measured.
