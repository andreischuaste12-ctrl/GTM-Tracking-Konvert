---
name: gtm-build-konvert
description: >-
  Build or extend a Google Tag Manager (GTM) container from an approved event contract: variables,
  triggers, tags, folders, consent settings, naming, and an import-ready container JSON generated
  from a declarative spec and checked before import. Use when asked to create, scaffold, configure,
  or "set up" GTM tags, triggers, and variables for GA4, Google Ads, or Meta, or to produce an
  import file. Web containers first; Server containers only with an observed reference export. For
  auditing an existing container, event contracts, or release review use gtm-tracking-konvert. GTM
  means Google Tag Manager, not go-to-market. Never imports or publishes.
metadata:
  short-description: "Spec-to-container GTM construction"
---
# GTM container construction

Build containers from a contract, not from tag names. A container is production code: every object
must trace to an approved event contract, and the generated file is a proposal until it has been
previewed in a scratch workspace.

This skill builds. For audits, contracts, consent policy, deduplication, or release governance,
load the sibling skill [`gtm-tracking-konvert`](../../SKILL.md) and follow its evidence rules; do
not restate them here.

## Inputs required before building

1. **Approved event contract** per event (see the [event contract
   template](../../assets/event-contract.template.md)). If the producer payload is unknown, stop
   and ask; do not invent `dataLayer` keys, IDs, or event names.
2. **Container type and state:** Web or Server; new container, or extension of an existing one. For
   an existing container, a fresh export is required (see below).
3. **Destinations and IDs:** use placeholders (`G-XXXXXXXXXX`, `AW-XXXXXXXXX`) unless the user
   supplies real, non-secret IDs.
4. **Naming convention** of the container, or the default in [build
   workflow](references/build-workflow.md#naming).
5. **Approved consent policy** per destination. Without it, leave consent as `NOT_SET` and report
   the gap; do not choose consent types.

## Workflow

1. **Establish the schema oracle.** Parameter keys, tag `type` values, and built-in trigger IDs vary
   by template and version. Take them from a fresh export of the target container that already
   contains the same kind of object (for example one GA4 event tag), never from memory. Without
   one, mark every vendor-specific key as unverified. See [container JSON
   format](references/container-json-format.md).
2. **Write the build spec** (JSON). For GA4 events, list them under `events` and let the builder
   expand each contract into its Data Layer variables, exact-match trigger, and GA4 event tag
   ([`examples/saas-events-contract.spec.json`](examples/saas-events-contract.spec.json)). For
   anything else, declare folders → built-in variables → variables → triggers → tags explicitly
   ([`examples/saas-trial-activated.spec.json`](examples/saas-trial-activated.spec.json)).
3. **Check, then generate** (commands run from the repository root):

   ```bash
   python3 skills/gtm-build-konvert/scripts/build_gtm_container.py spec.json
   python3 skills/gtm-build-konvert/scripts/build_gtm_container.py spec.json --output container.json --base target-export.json
   ```

   The first call only validates. With `--base` (a fresh export of the target container) IDs
   continue after the existing ones, a name that already exists is an error, references resolve
   against existing variables and triggers, and any tag/variable type or parameter key not seen in
   that export is reported as unverified. Only the new objects are emitted. Fix every `ERROR`;
   justify or resolve every `WARNING`. No file is written while errors exist, and an existing
   output is never overwritten without `--force`.
4. **Structural review:** run `python3 scripts/inventory_gtm_export.py container.json --fail-on
   missing_trigger_references,unresolved_variable_references,literal_secret_like_parameters` for
   references, consent, and secret-like checks; it does not validate runtime behavior.
5. **Hand off to the human for import:** give the exact steps from [working mode and
   release](../../references/working-mode-release.md): new scratch workspace, **Merge** into an
   empty workspace unless told otherwise, read the import preview before confirming.
6. **Validate with the QA matrix** ([template](../../assets/qa-matrix.template.md)): positive,
   negative, repeated, consent-granted, and consent-denied cases in Preview.
7. **Report the state precisely:** `generated locally`, `import previewed`, `in workspace`,
   `Preview observed`, `version created`, `published`. Claim only what was observed.

## Build rules

- One tag per destination event, one trigger per business event. Do not create GTM events to
  compensate for a missing producer event.
- Custom-event triggers are generated with exact matching (`EQUALS` on `{{_event}}`), never regex.
  Regex filters supplied through `raw` must be anchored with `^` and `$`.
- Every `{{reference}}` must resolve to a defined variable, a declared built-in variable, or
  `_event`. Add outside names to `allowReferences` only when verified in the container.
- Measurement and conversion IDs belong in `Constant |` variables, not repeated in tags.
- Never place secrets, tokens, or API keys in the spec; the builder rejects literal values for
  secret-like keys. Do not place personal data in parameters; the builder warns on sensitive-looking
  names. Enhanced Conversions and Meta customer data need explicit policy approval first.
- Declare consent on every tag (`NEEDED` with types, or `NOT_NEEDED`); `NOT_SET` is a decision left
  open and is reported as a warning. The builder does not know your policy and does not prove
  consent behavior.
- Custom HTML only when no template exists; it is reported as a warning and needs code review.
- Do not rename or reuse IDs of objects in an existing container. When extending, always pass the
  target export with `--base`, build only the new objects, and import with Merge into a scratch
  workspace.
- Event and parameter names in `events` must match `^[a-z][a-z0-9_]{0,39}$` and avoid the
  `google_`, `ga_`, and `firebase_` prefixes; confirm against the current GA4 documentation.
- Deduplication of Pixel/CAPI or browser/server events is designed in the event contract and
  verified with destination evidence; building both tags is not deduplication.

## Safety

Building authorizes local files only. Import into a workspace, version creation, publication, real
conversions, and production consent changes require explicit authorization for the exact account,
container, workspace, and environment. Never print or store credentials or personal-data values.

## Output

Return: the spec path, the generated file path and its checks (errors/warnings and how each was
resolved), what is unverified (schema keys without an oracle export, built-in trigger IDs), the
import instructions, and the QA cases still to run. Keep it short when only a few objects changed.
