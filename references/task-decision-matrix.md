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
| Cross-domain / attribution | Journey hostnames, symptom, destination view of source | Linker domains, redirects, referrers, cookie writers | Same identifier before/after each hop; first-hit parameters; consent states | Broken-hop diagnosis; see [attribution](attribution-cross-domain.md) |
| Auto-event / SPA trigger | Page or app, intended interaction, producer capabilities | Producer events, trigger conditions, Enhanced measurement overlap | Fires once; negative and repeated cases; same-event request | Trigger spec or producer request; see [auto-events and SPA](auto-events-spa.md) |
| Warehouse reconciliation | Metric, authoritative system, window, timezone | Grain, filters, identity key, consent gaps | Query definition, row counts per step, classified gap | Gap table with unexplained remainder; see [warehouse reconciliation](warehouse-reconciliation.md) |
| Tag performance | Page type, device class, symptom | Heavy tags, triggers, sequencing, duplicate loaders | Before/after measurement; QA regression | Measured change or stated gap; see [tag performance](tag-performance.md) |
| Other ad/analytics pixel | Destination, business event, policy | Template vs custom HTML, consent, server path | Request fields, consent states, destination diagnostics | Mapping without borrowed fields; see [other pixels](third-party-pixels.md) |
| Build a container | Approved event contract, container state, destinations | Fresh export of target container (`gtm-build-konvert`) | Builder check, import preview, QA matrix | Spec and generated file with unverified items listed |
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
