# Container governance, access, and release

Use this reference when a task changes container structure, coordinates work across people/environments, uses the API, prepares publication, or needs to establish who can change what.

## Mental model and scope

- Configuration hierarchy: **account → container → workspace → entities**. A workspace change is not a published version; `create_version` and `publish` are distinct API operations.
- Web, Server, and other product/platform containers have their own IDs, runtimes, and lifecycle. A GTM environment deploys version configuration to a target; it does not replace application QA, feature flags, or site rollout strategy.
- Confirm account/container ID, container type, active workspace, comparison base, live version, and environment/target before interpreting names or proposing changes. A workspace name does not prove production.
- Roles and permissions vary by account/container and may allow editing without publishing or publishing without user administration. Verify effective access and ownership in the product/API; never request or expose credentials as text.

## Change review

Before editing, pin an identifiable snapshot (export/hash, container, workspace, and time) and inventory affected objects/references. Explain semantic changes and dependencies in the diff: tags, triggers/exceptions, variables, sequencing, templates/permissions, consent, Clients, and Transformations as applicable.

Check for conflicts or concurrent workspace changes before syncing/importing. Do not choose replace/combine by option name alone: verify comparison base, existing items, removed/renamed items, and duplicate effects. Preserve active/paused states and out-of-scope dependencies. If the base changed since the snapshot, reassess the diff.

## Preparation and publication

1. State intent, scope, risk, affected objects, and validation criteria before the change.
2. Make the change in the appropriate workspace; run validation/Preview for the scenario and inspect errors, warnings, dependencies, and relevant template code.
3. Review the complete diff against the correct base. An error list does not replace behavior review.
4. Create a version with a name and description that match the actual scope. Record version ID/number and approver when required by the client's process.
5. Publish/deploy only with explicit authorization. Confirm target and version first. After publication, read live state and validate a safe production signal; do not trigger an artificial purchase/financial event.
6. Document rollback path, prior version, and rollback conditions. Rollback is also a publication and requires applicable authorization.

Report the exact state: **changed in workspace**, **Preview observed**, **version created**, **sent to environment**, **published/live**, **request received**, or **counted**. Never use ambiguous “deployed” to mean merely saved.

## Programmatic Tag Manager API use

Use the API only when it reduces repetitive work or enables reproducible inventory/diffs. Prefer reads for audits. For mutations, confirm IDs and target workspace, preserve the initial snapshot, and produce a readable diff. Avoid scripts that automatically sync or publish based only on names.

- Use OAuth and the minimum compatible scope/permission; store tokens outside code and logs.
- Discover entities and IDs through read calls. Numeric IDs, API paths, and user names are not interchangeable.
- Before `sync`, `resolve_conflict`, `create_version`, `publish`, `delete`, or equivalent import, review preconditions and consequences for the exact workspace/version/environment.
- Respect documented quota/QPS; limit calls, distinguish quota from authorization on `403`, and retry with backoff only for transient errors. Do not repeat a non-idempotent operation before checking whether the first completed.
- Record results/errors without capturing secrets or personal payloads. Verify state after each mutation instead of relying on the HTTP response alone.

See Tag Manager API pages in [official references](official-references.md); quotas and methods can change.
