---
name: regression-eval
description: Guard a working prompt, model or pipeline against regressions - a fixed test set that runs on every change and fails when quality drops. Use when the user says "make sure this doesn't break", "test prompt changes", "evals in CI", "can I safely swap the model", or "did my change make it worse".
---

# Set up a regression eval

A different job from model selection. This compares **one system with its past self** on a
fixed test set, so here the same inputs are meant to run again and again. The wide-and-shallow
default doesn't apply.

## Steps

1. **Build the test set from real cases.** 20–50 inputs: typical cases, hard cases, and
   **every bug found so far**. A failure fixed once gets a test so that it stays fixed. Keep it in
   the repo (`evals/regression/`, see `setup-repo-eval-space`).

2. **Prefer deterministic checks.** Valid JSON, required fields, contains or doesn't contain,
   length limits, regex. They're free and don't flicker. Use an LLM judge only for what code can't
   check, with a pinned judge model and a fixed rubric.

3. **Allow for noise.** Model output varies, so a single failure may mean nothing. Pin the model
   version and set temperature to 0 if the workload allows. Run each flaky case about 3 times
   and take the majority, and set thresholds a little under the baseline score.

4. **Record a baseline** from the current good version: scores per case, model, prompt
   revision and date. A later run compares with this, and it's only updated deliberately,
   in its own commit.

5. **Wire it in.** promptfoo suits this well: test cases in YAML, a non-zero exit on failure, and a
   CI action (`install-eval-cli`). DeepEval suits a pytest-based project. A small script is fine.

6. **Control the cost.** Run deterministic checks on every change. Run the judged, paid set when
   prompts, models or pipeline code change, not on every commit. The API key goes in CI secrets.

7. **Report differences, not totals:** which cases went from pass to fail, with both outputs side by
   side. A total that holds steady can hide new failures offset by new passes.

## Swapping models

Before changing a production model, run the regression set on the new one. Passing shows nothing
broke. It doesn't show the new model is better: that's `run-eval`.

## Don't

- Don't tune the prompt on the test set until it passes, then treat the pass as evidence.
- Don't update the baseline to make a failure go away.
