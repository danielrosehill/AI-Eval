---
name: run-framework-eval
description: Execute an eval defined in the current workspace and capture results with full metadata. Use when the user wants to actually run an eval (one or many SUTs), collect scored outputs under results/, and produce a run manifest so findings are reproducible and comparable over time.
---

# Run an Evaluation

Executes an eval from `evals/<slug>/`, captures outputs and scores under `results/<slug>/<run-id>/`, and writes a run manifest.

## Arguments

- **Eval slug** (required) — must match a directory under `evals/`.
- **`--sut=<name>[,<name>...]`** — models / prompts / pipelines under test. Required unless the eval has a default SUT list.
- **`--n=<int>`** — sample size override (for smoke runs).
- **`--tag=<label>`** — free-form label recorded in the manifest (e.g. `baseline`, `post-prompt-fix`).
- **`--dry-run`** — validate config, print the plan, do not call any model.

## Procedure

1. **Locate the eval.** Read `evals/<slug>/BRIEF.md`, `TASK.md` (if present), `RUBRIC.md`, and the framework config. If any are missing, stop and suggest `create-eval` / `setup-eval`.

2. **Pre-flight checks.**
   - API keys / env vars present for each SUT and the judge model.
   - Dataset exists and hash matches what's recorded in `DATASET.md` (if recorded).
   - Estimate cost (tokens × price) and latency. Print the estimate. For runs > $5 or > 15 min, confirm before proceeding.

3. **Assign a run id.** `YYYY-MM-DD-HHMM-<slug>-<shortsha>` where shortsha is `git rev-parse --short HEAD` if the workspace is a repo, else a random 6-char nonce.

4. **Execute.** Invoke the framework's runner (prefer `evals/<slug>/run.sh`). Stream outputs to `results/<slug>/<run-id>/raw/`.

5. **Score.** Apply the rubric. For LLM-as-judge: call the judge model on each item, cache judgments, and store the full trace (not just the score).

6. **Write the manifest.** `results/<slug>/<run-id>/manifest.yaml`:
   ```yaml
   run_id: ...
   eval_slug: ...
   started_at: ...
   finished_at: ...
   suts: [ ... ]
   judge_model: ...
   dataset_hash: ...
   framework: ...
   framework_version: ...
   sample_size: ...
   cost_usd: ...
   tag: ...
   git_sha: ...
   overall_scores: { sut_a: 0.82, sut_b: 0.79 }
   ```

7. **Write a short summary.** `results/<slug>/<run-id>/SUMMARY.md` — headline number, per-stratum breakdown, notable failures (link to `raw/`), comparison to prior runs if any exist.

8. **Offer follow-ups.** Suggest `/ai-eval:document-eval` to write up findings, or `/ai-eval:publish-eval` to share.
