# Changelog

## Unreleased

- Inventory: built-in trigger IDs (for example All Pages) are no longer reported as missing
  references; added counts for tags without a firing trigger or consent settings, Custom HTML,
  sensitive and secret-like parameters, and unreferenced or unresolved variables; added `--fail-on`
  for CI gating and a realistic-shape synthetic fixture with golden tests.
- Builder: `events` contract expansion with GA4 name validation, `--base` mode (ID continuation,
  collision errors, reference resolution, type/key evidence, built-in trigger ID evidence).
- Added references for attribution and cross-domain, auto-events and SPA navigation, warehouse
  reconciliation, tag performance, and other pixels; extended routing, the task matrix, and evals.
- Validation: skill metadata checks (description length, name/directory match, unlinked
  references), a manual review-sheet generator, and new eval scenarios for both skills.
- Added the `gtm-build-konvert` skill: spec-to-container builder with pre-import checks (name,
  reference, trigger, consent, regex-anchoring, and secret checks), workflow and JSON-format
  references, an example spec, manual evals, and unit tests.
- Generalized source guidance and examples for websites, SaaS, lead generation, and content
  projects using GTM.
- Added a synthetic audit report and inventory-output example.
- Extended the read-only inventory to report unresolved tag-sequencing references and cycle groups.
- Added Google Ads Conversion Linker and click-identifier guidance, plus a fuller Measurement
  Protocol workflow.
- Improved skill routing terms and added a reusable QA matrix template and HTTP-success evidence eval.
- Kept the external URL probe visible as a best-effort check; local documentation validation,
  Markdown lint, and utility tests remain required checks.
