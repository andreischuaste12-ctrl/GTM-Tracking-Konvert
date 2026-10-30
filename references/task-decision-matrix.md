# Task decision matrix

Choose one primary path, then load only the references needed for that path. These inputs are
minimum evidence, not a form the user must complete before any work can begin.

| Task | Minimum input | Inspect first | Validation/evidence | Deliverable |
|---|---|---|---|---|
| Export/workspace audit | Export or identified live workspace; question/impact | Inventory, object dependencies, source/version | Static structure → Preview → requests → destination as available | Prioritized findings with evidence state and limits |
| Event contract | Business fact, producer payload/schema, destination if known | Producer and existing data-layer conventions | Synthetic valid/invalid fixtures; consent/retry scenarios | Completed event contract and open decisions |
| SaaS sign-up/subscription | Intended business fact, producer/backend state, destination if known | Existing application events and authoritative lifecycle | Distinguish intent from backend-confirmed state; verify consent and retries | Event contract and evidence gaps |
| Lead form/content | Form or content source, intended outcome, destination if known | Source producer, backend acceptance, approved attributes | Separate interaction/submission from accepted or qualified outcome; minimize data | Event contract and privacy-aware mapping |
| GA4 measurement | Source event, GA4 property/use case, payload if available | GA4 event semantics, applicable event contract, collection path | Same-event Preview/request, DebugView/report as available | Parameter mapping and evidence state; see [GA4 workflow](ga4-measurement.md) |
| Google Ads conversion | Conversion action, source fact, value/counting intent | Trigger, action ID, consent, identity, value | Tag/request, Ads diagnostics/report, adjustment state | Action mapping and unsupported assumptions; see [Ads workflow](google-ads-conversions.md) |
| Meta Pixel/CAPI | Logical event, emitting paths, destination diagnostics if available | All emitters, event name/ID, consent, data fields | Same occurrence across browser/Server and Meta diagnostics | Pairing/dedup state; see [Meta workflow](meta-pixel-capi.md) |
| Source integration adapter | Actual source/application and producer payload | Installed implementation and official source contract | Source event, field paths, lifecycle, consent | Source-specific mapping without borrowed fields; see [source integration adapters](source-platform-adapters.md) |
| Consent issue | Approved policy or clear note it is unavailable; CMP and actual state | Defaults, updates, tag consent checks, runtime order | Granted, denied, updated/revoked state; Preview and requests | State-by-state behavior and policy-dependent gaps |
| Duplicate conversion | Logical event, browser/server paths, relevant IDs, destination | All emitters, triggers, exceptions, IDs, destination rules | Same logical event and ID at each layer; destination diagnostics | Proven overlap vs. proven counted duplicate, clearly separated |
| Ecommerce value/reconciliation | Producer amount/unit/currency; source of truth and destination | Order grain, items, discounts, shipping, tax, lifecycle | Order-level reconciliation and refund/cancel cases | Field contract, mismatch classification, formula |
| Server-side routing | Request sample with sensitive values removed; Client, destinations | Winning Client, event data, Transformations, outbound tags | Web→Server trace, payload minimization, destination response | Data-flow map, controls, gaps, and operating impact |
| Custom template | Web/Server type, installed code/version, source, failure | Code, fields, permissions, APIs, dependencies | Sandbox tests, permission validation, non-prod Preview | Findings or minimum code change with test limits |
| Container release/import | Exact account/container/workspace, target, diff, authorization | Current state, import base, dependencies, paused items | Preview/validation, full diff, rollback readiness | Exact release state; never conflate save, version, and publish |
| Platform-only analytics | No GTM implementation dependency | Do not load this skill | Route to the relevant analytics workflow | No GTM-specific recommendation |
| Go-to-market strategy | Clarify if “GTM” is ambiguous | Do not load this skill for go-to-market | Not applicable | Route to go-to-market planning |

## Minimum-information rules

- For a local export audit, the file and the user's question are enough to start. Container ID and
workspace are needed only for claims that depend on live state.
- For an implementation, a missing field/source/destination is a conditional requirement. Identify
exactly what cannot be decided; do not invent it or block unrelated analysis.
- For consent, distinguish technical state from approved policy. If the policy is unavailable,
inspect implementation but do not declare the behavior legally allowed or disallowed.
- For ecommerce, never infer major/minor currency units from the number's magnitude.
- For production mutation, confirm the exact target and authorization before the mutation.

## Evidence checkpoints

Use [audit evidence](audit-evidence.md) as the single canonical evidence ladder. Capture the minimum
data needed to show each checkpoint. Do not copy PII or credentials into evidence files.
