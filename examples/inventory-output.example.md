# Example inventory output

Command:

```sh
python3 scripts/inventory_gtm_export.py evals/fixtures/duplicate-purchase-export.json
```

The SHA-256 and counts below are generated from the synthetic fixture in this repository:

```text
GTM export structural inventory (read-only)
SHA-256: 9d7b14bc9116139ffd4de56534c70c79ec3dc4297deca72bd2a2a98a4699d4d5
Entity counts:
  tag: 2
  trigger: 1
  variable: 0
  folder: 0
  customTemplate: 0
  builtInVariable: 0
Review counts:
  paused_tags: 1
  duplicate_ids: 0
  duplicate_names: 0
  missing_trigger_references: 1
  builtin_trigger_references: 0
  orphan_triggers: 0
  tags_without_firing_trigger: 0
  tags_without_consent_settings: 2
  custom_html_tags: 0
  sensitive_parameter_names: 0
  literal_secret_like_parameters: 0
  unreferenced_variables: 0
  unresolved_variable_references: 0
  unanchored_regex_filters: 1
  sequencing_references: 0
  unresolved_sequencing_references: 0
  sequencing_cycle_groups: 0
```

This is structural triage. It does not validate runtime behavior, consent, destination acceptance,
conversion counting, or reconciliation. An unanchored regex is a review prompt, not automatically a
defect. Built-in trigger IDs (such as All Pages) are counted separately by an ID-range heuristic
instead of as missing references. In CI, `--fail-on <count>[,<count>]` returns exit code 1 when a
selected count is greater than zero.
