# Skill evaluation guide

`evals.json` defines manual scenarios and binary review criteria. The repository does not include a
model runner, and these scenarios have not been behaviorally executed against a model. Do not report
them as passing evals until a reviewer or a configured evaluation harness has run them.

## Manual run

1. Run each prompt with the skill enabled and disabled against the same fixture/context.
2. Score each `must_include` and `must_not_claim` criterion as pass/fail; cite the response text.
3. Fail the scenario if any `must_not_claim` criterion is violated. Report partial credit for
missing positive criteria rather than rounding to an overall “pass.”
4. Compare factual accuracy, evidence boundaries, safety, scope, and response usefulness.
5. Record model/version, skill commit, date, fixture hash, evaluator, scores, and failure notes.
6. Change one skill component at a time and rerun failed and regression scenarios.

Fixtures in `fixtures/` are synthetic. They intentionally distinguish configuration evidence from
runtime/destination evidence and must not be replaced with client exports unless they are approved
and fully anonymized.
