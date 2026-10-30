# Build workflow and conventions

## Build order

Create objects in dependency order so every reference resolves when the next layer is added:

1. **Folders** (organization only; they never change collection).
2. **Built-in variables** actually used (`Page URL`, `Event`, and so on). Enable only what is read.
3. **Variables:** `Constant` IDs first, then `DLV`, `Cookie`, `JS`, `Lookup`.
4. **Triggers:** one per business event; exceptions (`Exception |`) after the triggers they block.
5. **Tags:** Google tag (configuration) before event tags; event tags after their triggers and
   variables.
6. **Consent:** defaults must run in the Consent Initialization stage before any tag that depends
   on them. Declared per-tag consent checks are additive to, not a substitute for, that default.

## Naming

Preserve the container's existing convention. If none exists, propose this one and get approval:

| Object | Pattern | Example |
|---|---|---|
| Variable | `<Kind> \| <Domain> \| <name>` with kind `DLV`, `Constant`, `JS`, `Cookie`, `Lookup` | `DLV \| Account \| plan_category` |
| Trigger | `Event \| <Domain> \| <event>`; `Exception \| ...` for blockers | `Event \| Account \| trial_activated` |
| Tag | `<Platform> \| <Type> \| <event>` | `GA4 \| Event \| trial_activated` |
| Folder | platform or domain | `GA4` |

Set `naming` in the spec to make the builder enforce the prefixes you approved.

## Minimum set for a new Web container (GA4)

- `Constant | GA4 | Measurement ID`.
- Google tag on the initialization stage (built-in trigger ID taken from an oracle export).
- One `DLV` per contract parameter, one custom-event trigger per business event, one GA4 event tag
  per event with its parameters in the event settings table.
- Consent declared on every tag; consent defaults implemented by the CMP integration or a template,
  per the approved policy and the [Web workflow](../../../references/workflow-web.md).

## Destination notes

Keep destination logic in the existing references and do not duplicate it:

- GA4 parameters, ecommerce, and Measurement Protocol: [GA4](../../../references/ga4-measurement.md).
- Google Ads conversion, Conversion Linker, Enhanced Conversions: [Google
  Ads](../../../references/google-ads-conversions.md).
- Meta Pixel/CAPI and `event_id`: [Meta](../../../references/meta-pixel-capi.md).
- Server containers (Clients, Transformations): [Server workflow](../../../references/workflow-server.md).
  The builder does not model Clients or Transformations; build Server objects only from a Server
  oracle export.

## What the builder checks

Errors (block output): invalid GA4 event or parameter names in `events`, name collisions with the
base export, duplicate names, unknown folder or trigger, unresolved `{{reference}}`,
active tag without a firing trigger, invalid or incomplete consent, unanchored regex filter,
literal value for a secret-like key, `raw` overriding identity fields, naming prefix mismatch.

Warnings (review required): consent `NOT_SET`, Custom HTML, sensitive-looking parameter names,
and, with `--base`, types or parameter keys not seen in the export.

The builder does not check: whether tag `type` values or parameter keys exist in the current GTM
version, runtime behavior, consent legality, destination acceptance, or deduplication.
