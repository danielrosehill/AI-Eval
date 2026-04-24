---
name: create-eval
description: Design a custom eval from scratch, or remix an existing benchmark. Use when the user wants to define the eval itself — task framing, dataset composition, scoring rubric, and reporting format — rather than simply wiring up a framework. Produces a fully specified eval definition ready to be run.
---

# Create a Custom Eval

Where `setup-eval` wires up a framework, `create-eval` designs the eval's substance: what's tested, how it's scored, what "good" looks like. Use together — create first, then setup.

## Arguments

`$ARGUMENTS` may include:
- **Name/slug** (required).
- **`--inspired-by=<ref>`** — existing benchmark/eval to remix (e.g. MMLU, HumanEval, MT-Bench, a HF dataset, a paper).
- **`--mode=<scratch|remix>`** — default `scratch` unless `--inspired-by` is set.

## Procedure

1. **Interview the user.** Before writing, answer these in conversation or `BRIEF.md`:
   - What decision does this eval support? (deploy / don't deploy, prompt A vs B, model choice, regression gate)
   - What is the subject under test (SUT)? A model? A prompt? A whole pipeline?
   - What's the input distribution? Representative, adversarial, or both?
   - What's the output shape? Free text, structured, tool calls, classification label?
   - What counts as correct? Deterministic check, human judgment proxy, rubric score, pairwise preference?
   - What is the blast radius of a false pass / false fail?

2. **Task spec.** Write `evals/<slug>/TASK.md`:
   - **Task statement** — one paragraph a stranger could implement from.
   - **Input schema** — JSON schema or typed example.
   - **Output schema** — same.
   - **Examples** — 3–5 worked examples, including at least one failure case.

3. **Dataset design.** Write `evals/<slug>/DATASET.md`:
   - Source (synthetic, scraped, curated, existing benchmark subset).
   - Size and stratification (difficulty tiers, categories, languages).
   - Licensing and redistribution notes.
   - Contamination check — how will you detect the SUT was trained on it?

4. **Scoring rubric.** Write `evals/<slug>/RUBRIC.md`:
   - Metric(s) with formulas.
   - If LLM-as-judge: the full judge prompt, the judge model, whether pairwise or pointwise, tie-breaking, and a short calibration set of gold human ratings.
   - Statistical handling: sample size, confidence interval approach, bootstrap/permutation if comparing two SUTs.

5. **Remix mode.** If `--inspired-by` is set, explicitly record in `TASK.md`:
   - What from the source is kept as-is.
   - What is modified and why.
   - Why the remix is expected to be more informative than the original for the user's use case.

6. **Reporting format.** Write `evals/<slug>/REPORT_TEMPLATE.md` — the structure results will be written into so that `publish-eval` / `document-eval` have a fixed target.

7. **Handoff.** Suggest running `/eval-runner:setup-eval` to wire the design to a framework, or writing a minimal custom runner if nothing in `data/awesome-ai-evaluations-tools.md` fits.
