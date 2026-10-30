# Container JSON format and the spec

This is the shape the builder emits. It reflects the commonly observed export layout
(`exportFormatVersion: 2`); it has not been verified against a live import from this environment.
Treat a fresh export from the target container as the authority for every `type` and `key`.

## Export layout

```text
exportFormatVersion: 2
containerVersion
  container { name, publicId, usageContext }
  folder[]  builtInVariable[]  variable[]  trigger[]  tag[]  customTemplate[]
```

- IDs are strings, unique per entity type within the container. The builder assigns sequential IDs
  and resolves names to IDs; account and container IDs are placeholders replaced on import.
- Fingerprints, `path`, and `tagManagerUrl` are omitted. Whether import accepts that is unverified;
  check in the import preview.

## Parameter encoding

Every parameter is an object with `type` and `key`. Values are strings, including booleans and
integers.

| Spec value | Emitted |
|---|---|
| `"text"` or `"{{Var}}"` | `{"type":"TEMPLATE","key":k,"value":"text"}` |
| `true` / `false` | `{"type":"BOOLEAN","key":k,"value":"true"}` |
| `2` | `{"type":"INTEGER","key":k,"value":"2"}` |
| `{"table":{"columns":[...],"rows":[[...]]}}` | `LIST` of `MAP`, one `MAP` per row |
| `{"type":"LIST"\|"MAP"...}` | passed through with `key` added |

## Spec fields

| Entity | Fields |
|---|---|
| top level | `container`, `naming`, `ga4`, `events`, `builtinTriggerIds`, `folders`, `builtInVariables`, `variables`, `triggers`, `tags`, `allowReferences` |
| `ga4` | `measurementIdVariable` (required with `events`), `folder`, `variableFolder` |
| event | `name`, `domain`, `parameters[]` (`name`, optional `path`, `variableName`), `consent`, `triggerName`, `tagName` |
| variable | `name`, `type`, `params`, `parameter`, `folder`, `raw` |
| trigger | `name`, `type`, `eventName` (custom event, exact match), `params`, `parameter`, `folder`, `raw` |
| tag | `name`, `type`, `params`, `parameter`, `firingTriggers`, `blockingTriggers`, `firingOption`, `paused`, `consent`, `folder`, `raw` |

- `params` is the shorthand above; `parameter` is a raw list appended after it; `raw` merges extra
  entity fields (for example `customEventFilter`) but cannot set identity or reference fields.
- `consent`: `{"status":"NEEDED","types":["analytics_storage"]}`, `NOT_NEEDED`, or `NOT_SET`
  (default).
- `builtinTriggerIds` maps a display name to a trigger ID that exists outside the trigger list
  (for example All Pages or Initialization). Copy the ID from an oracle export of the target
  container; never guess it. Without the mapping, a tag naming that trigger fails as unknown.
- `firingOption` defaults to `ONCE_PER_EVENT`.

## Base export mode

`--base <export.json>` reads a fresh export of the target container. It provides: the highest
existing ID per entity type (new IDs continue after it), existing names (collisions are errors),
existing variables, built-ins, triggers, and folders (references resolve against them), the
parameter keys seen per `type` (anything else is reported as unverified), and the trigger IDs
tags actually use (a `builtinTriggerIds` value missing from that set is reported). Existing
Data Layer variables are reused by `events` when their path matches. Absence of a warning means
the key appeared in some object of that type in the export, not that it is valid for this use.

## Known gaps

- Without `--base`, tag, trigger, and variable `type` codes and parameter keys are not validated;
  with it, they are only compared with what that export happens to contain.
- Custom templates (`cvt_*`) are not generated; reference an installed template only from an oracle
  export, with its permissions reviewed.
- Server containers differ (Clients, Transformations); they are out of scope without an oracle.
