# GTM QA matrix: `<project_or_release>`

Include only scenarios relevant to the approved measurement requirements. Mark a scenario `N/A`
with a reason when the event or path does not apply. Use synthetic data; do not copy PII or secrets.

| Event/scenario | Producer expectation | Consent state | Repeat/retry behavior | GTM trigger/tag | Request/destination expectation | Evidence state and artifact | Result/owner |
|---|---|---|---|---|---|---|---|
| Valid occurrence | | Granted/approved state | | | | | |
| Consent denied or withdrawn | | Denied/withdrawn | | | | | |
| Repeated occurrence/retry | | | | | | | |
| Missing or invalid required field | | | | | | | |
| SPA navigation/re-entry | | | | | | | |
| Web-to-Server forwarding, if used | | | | | | | |
| Destination diagnostic/report, if in scope | | | | | | | |

## Evidence and limits

- Source artifact/version and observation time:
- Test environment/container/workspace:
- Highest evidence level reached for each result:
- Scenarios not run and reason:
- Destination processing delay or diagnostic limitations:
- Reviewer and date:
