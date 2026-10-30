# Response contract

Respond in the user's language. Preserve exact product/UI labels and code identifiers when needed.
State what the evidence supports; label uncertainty and the next check that would resolve it.

## Audit

Use [`assets/audit-report.template.md`](../assets/audit-report.template.md) for durable reports. For
a chat-sized audit, include:

1. **Finding summary:** highest-impact proven issue first.
2. **Scope/source:** artifact, container/workspace/version, and what was unavailable.
3. **Evidence:** observed behavior and the layer reached (configuration, Preview, request, accepted,
counted, reconciled).
4. **Impact and confidence:** consequence, alternatives, and confidence supported by evidence.
5. **Action:** minimal prioritized fix, what to preserve, and safe validation.
6. **Limits:** unknowns, unverified external documentation, or missing access.

Do not call configuration overlap a duplicate conversion unless destination evidence proves
counting.

## Implementation

Report the requirement and assumptions; files/objects changed; the exact behavior changed; relevant
validation and results; rollback or compatibility notes; and remaining decisions. Separate local
files, workspace state, Preview, external requests, destination acceptance, and publication.

## Incident or troubleshooting

State the last confirmed-good checkpoint. Separate observed facts from hypotheses, rank the likely
causes, and propose the next safe discriminating check. Do not repeat an action that could create a
real order or conversion when existing evidence can answer the question.

## Consent or privacy review

Report consent state and tag/request behavior separately. Identify the approved policy source or
state that it is unavailable. Never make legal-compliance claims from GTM configuration alone.

## Release or import

Name the exact container/workspace/target, change set, validation state, approval status, and
rollback path. State whether it is proposed, saved, versioned, deployed, or live. Do not use these
states interchangeably.

## Confidence labels

- **Confirmed:** directly supported by the artifact, Preview, request, destination, or
reconciliation evidence appropriate to the claim.
- **Likely:** supported by evidence but has plausible alternatives.
- **Unverified:** depends on inaccessible state, unavailable vendor documentation, or a missing
artifact.
- **Blocked:** a specific missing input or permission prevents the next requested action.

Avoid numerical confidence percentages unless a defined statistical method supports them.
