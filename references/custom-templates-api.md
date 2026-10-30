# Custom GTM templates and APIs

Use this reference to create/review tag or variable templates, evaluate Community Template Gallery templates, modify sandboxed code, or investigate permissions/execution.

## Provenance and review

Identify type (Web or Server), name/ID, source (built-in, Gallery, internal template, export, or local code), installed version, date, and local changes. Compare effective code and permissions with declared source. Do not update to “latest” without a diff; keep a backup and identify dependent tags/variables.

Review separately:

- metadata, fields, defaults, validation, and configuration UX;
- executed code and success/failure paths;
- declared/effectively required permissions and minimum scope;
- behavior for missing values, invalid types, repetition, timeout, and callback;
- data handling and network destinations, cookies, globals, storage, and consent;
- tests, test limits, and compatibility with installed version.

A granted permission enables a capability; it does not prove its use is necessary or correct. Broad permissions increase potential impact. Restrict URLs/resources to destinations and data justified by the contract.

## Sandboxed Web runtime

Custom templates do not run in the global `window` like ordinary JavaScript. Use only runtime/APIs supported through `require()` and documented types/methods. Requested APIs may require template permissions. Code that works in the browser console can fail in sandbox, permission validation, or production.

For a consent template, use GTM APIs `setDefaultConsentState` and `updateConsentState`. Do not call `gtag('consent', ...)` from inside the template: `gtag()` commands are queued and might not be processed before the next event. Do not confuse this rule with CMP interfaces or `gtag.js` integration; identify the runtime in use.

## Sandboxed Server runtime

Server templates have different APIs/permissions from Web APIs. Check server-specific docs, available `require()` modules, data types, event-data access, HTTP responses, and SSRF risk. Do not copy Web code to Server or treat Server as a browser. For outbound calls, validate host/URL, method, data, timeout, and response against supported APIs and actual risk.

## Tests and limits

Use Template Editor unit tests for positive cases, missing/malformed input, API called/not called, return values, and errors. Mocks do not test real network integration and may not exercise actual permission checks. Run code/permission validation and Preview in a non-production container/environment when available.

Capture evidence without credentials/PII. Report what ran in sandbox, what was observed in Preview, and what still requires an external request/provider acceptance. Template publication and adoption by tags are separate changes.

`gtag('policy', ...)` policies can restrict template permissions on a page; inspect effective CSP/policy if a failure occurs only on specific routes/pages. Do not remove security policy automatically: identify the denied permission and validate with the application owner.

Current links are in [official references](official-references.md).
