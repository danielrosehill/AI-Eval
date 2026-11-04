---
name: full-run
description: Full run of an authored eval — every prompt against a model panel, with an LLM judge scoring every answer against the rubric. Adds the harness to the eval repo if there isn't one (generate → judge → report, resumable, via OpenRouter) and writes runs/<run_id>/. Use only when the user explicitly asks for the whole thing ("run the whole eval", "full run", "score these models on all of it"). For "a test run", trying many models, or a spend figure, use run-eval instead.
---

# Run an eval (full)

Produces a run: one answer per (prompt, model), judge scores, pairwise judge
verdicts, and a report. Publishing the raw data is a separate step (`publish-run`).

**Only on an explicit request for a full run.** "Run it" with no scope means
`run-eval`, the wide-and-shallow default. Before generating, state the cost estimate
(`scripts/openrouter_catalogue.py estimate`) and wait for a yes. If a `wide-` run
already checked the harness, skip step 4.

**References.** Read `../../references/pitfalls.md` **before** the first call. Every
item on it has already cost a run. If that path doesn't resolve, clone `danielrosehill/AI-Eval` and read it there.

**Reference implementation:** `danielrosehill/Dan-Eval` (`daneval/`)
(`common.py`, `generate.py`, `judge.py`, `report.py`) with `config.json` and
`docs/method.md`. Copy and adapt it. Don't write a harness from scratch, and don't
reach for an external eval framework unless the user asks for one.

## Inputs

- The eval repo (must have `data/prompts.jsonl`).
- Models to test (OpenRouter slugs), and a judge model that is **not** one of them.
- Optional: a `run_id` (see "Run IDs" in `conventions.md`) and a named panel
  (`configs/<panel>.json`).

Model selection is the part most likely to change between runs, so keep each panel in
its own config file and never edit a panel that has already been run. Copy it to a new
name instead.

## Steps

1. **Check the model slugs exist** on OpenRouter (`GET https://openrouter.ai/api/v1/models`)
   rather than trusting memory. Key: `OPENROUTER_API_KEY`. If it's missing or dead,
   say so before going further.
2. **Harness.** If the repo has no harness, copy Dan-Eval's into `<pkg>/` (a short
   name such as `amceval/`) and adapt:
   - Prompts are read from `data/prompts.jsonl`. Dan-Eval's lenses become this
     eval's dimensions.
   - The judge prompt carries the README rubric, the record's `*_tell` field, the
     `rater_profile`, and today's date with the "don't mark newer claims false" rule.
   - Mirrored pairs and controls are scored the way the README's Grading section
     says: e.g. compare a model's two answers to a pair, or check that a control
     moved off the default.
   - `config.json`: `run_id`, `prompts`, `ids` / `series` filters (empty = all),
     `models`, `judge`, `max_tokens: 8000`, `concurrency`, and `rater_profile` where
     the reader's viewpoint matters. Judge max tokens: 4000. Panels go in
     `configs/<panel>.json` and are selected with `--config`, as in
     `Propaganda-Bait-Eval/pbe/`, a second reference implementation that is closer
     to a single-eval harness than Dan-Eval's.
   - Mark answers under ~15 words as silent refusals without calling the judge, and
     keep refusals out of the main score.
   - Add `runs/*/*.jsonl` to `.gitignore`.
   - Python env via `uv` only (`uv venv && uv pip install httpx`).
   Write `docs/method.md` as you go: the pipeline table, judge rules, and run commands.
3. **Record the prompt revision.** Save the HF dataset commit
   (`HfApi().dataset_info("<owner>/<Name>-Eval").sha`) or the git SHA of
   `data/prompts.jsonl` in the run's `report.json`. A run without it can't be
   compared later.
4. **Smoke run first.** Run `smoke-01` on 2–3 prompts per dimension against two
   models, and read every answer and judge label. Fix the harness, then start the
   real run. Smoke numbers are never findings.
   A clean smoke run means the harness works: run `register-eval` to move the eval
   to stage `built` (if it was at `prompts`) before going on. Stopping here is fine.
   A built eval is finished work, and the full run can come later.
5. **Generate:** `.venv/bin/python <pkg>/generate.py --config <config>`. No system prompt.
6. **Gate before judging.** Count empty responses and responses with
   `completion_tokens` within 5% of the limit. If there are any, raise the limit and
   regenerate those rows. Don't judge truncated answers.
7. **Judge:** `.venv/bin/python <pkg>/judge.py`. Shuffle pair order and, where the
   harness supports it, judge both orders. Validate the judge's JSON.
8. **Report:** `.venv/bin/python <pkg>/report.py` → `runs/<run_id>/report.md` +
   `report.json`. Read the report and check it against a sample of the raw answers
   (at least three per model, including the best and worst scored) before stating
   any conclusion. The scores are a signal; the answers are the thing.
9. **Write up.** Add anything new to the Findings section of `docs/method.md`:
   the symptom, the measured numbers, and the fix. Change the README banner to
   `proof of concept` or `v1 results`. Commit the harness, config, `docs/` and
   `runs/<run_id>/report.*`. Do **not** commit the raw JSONL; `.gitignore` should
   hold `runs/*/*.jsonl`. Push.
10. Next: `publish-run` to put the raw data on HF (public by default),
   `package-results` for tables, charts and a brief, and `analyse-findings` for the
   analytical write-up. Optionally run `deploy-arena` for human A/B ratings.

## Report back

Give per-model scores with n for each, the judge used, any rows regenerated or
excluded and why, and two or three quoted answer excerpts that show the headline
result. Lead with the numbers.
