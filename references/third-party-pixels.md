# Other advertising and analytics pixels

Use this reference for destinations without a dedicated workflow here (for example TikTok,
LinkedIn, Pinterest, Microsoft Ads, Reddit, affiliate or email platforms). Meta has its own
[workflow](meta-pixel-capi.md); Google Ads has [its own](google-ads-conversions.md).

Do not copy event names, parameters, or ID formats from another platform. Take every platform
contract from the destination's current documentation and the installed template.

## Intake

For each destination, record: the business event it should receive, the platform event name, the
required and optional parameters and their units, the identifier fields allowed (and whether
hashing is required), the consent category, the browser and server paths, and the deduplication
key if both paths send the same event.

## Choose the implementation

1. A vendor-maintained template from the Template Gallery, after reviewing its permissions and
   source.
2. A reviewed community template, pinned to a version, with the same review.
3. Custom HTML only when no template exists; review it as code and see
   [custom templates](custom-templates-api.md).

## Rules

- One consent category decision per destination, from the approved policy. Without it, leave the
  consent setting undeclared and report the gap.
- Do not send direct identifiers except through the destination's documented customer-data
  feature, with approval, normalization, and hashing as that feature requires.
- If the platform has a server API in addition to the pixel, design the shared event ID in the
  event contract and verify deduplication with destination diagnostics; two tags are not
  deduplication.
- Map events from the contract. A funnel step is not a conversion; separate "form submitted" from
  "lead accepted".
- Keep the tag, trigger, and variable names consistent with the container convention, and store
  destination IDs in `Constant |` variables.

## Evidence

Tag fired once on the intended event, outgoing request fields match the contract, consent granted
and denied behavior observed, and the destination's diagnostic view for acceptance. Report which of
these were observed, per [audit evidence](audit-evidence.md).
