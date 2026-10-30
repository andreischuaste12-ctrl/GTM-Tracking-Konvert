# Example GTM audit report (synthetic)

This example is based only on [`duplicate-purchase-export.json`](../evals/fixtures/duplicate-purchase-export.json).
The names, IDs, and configuration are synthetic. No runtime or destination evidence is included.

## Scope and result

- **Question:** Does the export prove that a purchase is counted twice?
- **Artifact:** Synthetic GTM JSON export, SHA-256 `9d7b14bc9116139ffd4de56534c70c79ec3dc4297deca72bd2a2a98a4699d4d5`.
- **Evidence reached:** Configured in export. No Preview, request, destination, or reporting evidence.
- **Conclusion:** The export shows overlapping configuration that warrants a runtime check. It does
  not prove two requests, two accepted events, or two counted purchases.

## Findings

| ID | Impact | Confidence | Evidence | Observation | Consequence | Recommendation | Verification |
|---|---|---|---|---|---|---|---|
| F-01 | Medium | High | Export configuration | Two purchase tags reference the same trigger; one tag is paused. | An active overlap may exist, but the paused tag does not fire in the inspected configuration. | Confirm intended ownership and inspect the active tag's full trigger, exceptions, and sequencing. | In the matching workspace, use Preview and inspect one synthetic purchase occurrence and its requests. |
| F-02 | Medium | High | Export structure | One tag references a trigger ID that is absent from this export. | The reference may be stale, unavailable, or invalid; this snapshot alone does not show the live workspace state. | Recheck the exact workspace and resolve the reference only after reviewing the intended behavior. | Compare the current workspace/export and validate the affected tag in Preview. |
| F-03 | Low | High | Export configuration | An event-matching regex is not anchored. | Similar event names may match if exact matching was intended. | Confirm the intended match set; anchor the pattern only if exact matching is required. | Exercise exact, prefixed, and suffixed event names in Preview. |

## Preserve and next steps

- Preserve the paused state until its purpose and dependencies are understood.
- Keep export findings separate from runtime execution and destination counting.
- Do not publish a change from this static example; use a reviewed workspace diff, Preview evidence,
  and an approved release plan for any real container change.
