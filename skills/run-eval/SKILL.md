---
name: run-eval
description: Run an eval the wide-and-shallow way - many candidate models, about two outputs each - under a hard spend cap, and report which models are worth a closer look. The default way to run. Use when the user says "run the eval", "run it", "test these models", "do a test run", "try it on a bunch of models", "spend about $N on it", or "get some examples". For every prompt across a panel, use full-run. For a third-party framework workspace, use run-framework-eval.
---

# Run an eval: wide and shallow

**Test many candidates a little, rather than a few candidates a lot.** Many evals go
narrow and long: a handful of models, many iterations each, to see how they hold up. This
one goes the other way. The default is **12–20 models × 2 outputs each**, on the same one
or two real tasks. For a script-writing eval, that's two scripts from every candidate.

Why wide wins for model selection:

- The biggest risk is that the best model was never tested, not that a tested model's
  score is imprecise.
- The gap between models is usually far larger than the variation within one. Two outputs
  show a model's character, and the second rules out a fluke.
- Money spent repeating a model already seen buys little. The same money buys another model.

**Don't turn this into a long run.** No extra iterations on a few models, and no raising
outputs per model to look rigorous, unless the user asks. The exception is when the user
is targeting one specific behaviour that only shows up intermittently, and they say so.

## Before running

- Needs `selection/candidates.json`. If it's missing, run `define-objective`,
  `define-workload-requirements`, `probe-openrouter` and `shortlist-candidates` first, or
  take the user's own model list and ping it.
- Read `../../references/pitfalls.md`. Every item on it has already cost a run. Read the
  overlay's `conventions.md` if there is one (`../../references/overlay.md`). If these
  paths don't resolve, clone `danielrosehill/AI-Eval` and read them there.

**Budget.** The default is a hard cap of **$5 of OpenRouter credit**, judge calls included.
A figure the user gives wins. A cap isn't a target; spending well under it is fine.

## Steps

1. **Fix the task.** One or two real inputs, the same for every model, chosen because they
   exercise the workload's top soft requirements. Same settings for every model too:
   `run_settings` from `requirements.json`, with no system prompt unless the workload has
   one. Write the plan to `configs/wide.json`: `run_id` (`wide-01`, then `wide-02`, …),
   inputs, models, outputs per model, `max_tokens`, judge, budget.

2. **Estimate and get a yes.** Run `openrouter_catalogue.py estimate` and show the user the
   model count, outputs per model and total. **Nothing paid runs before they agree.** If the
   estimate passes 80% of the cap, drop the most expensive models first. Keep two outputs
   each. Set reasoning models to the stated setting, as thinking bills as output.

3. **Harness.** If the repo has none, adapt `danielrosehill/Propaganda-Bait-Eval` (`pbe/`)
   or `danielrosehill/Dan-Eval` (`daneval/`) as described in `full-run` step 2. It needs a
   **spend guard:** OpenRouter returns `usage.cost` (USD) on every response, so keep a running
   total of generation and judge costs in `runs/<run_id>/spend.json`, and start no new call
   once the next could pass the cap. Don't meter on `GET /api/v1/key`, which includes other
   traffic on the same key. `/api/v1/credits` needs a management key.

4. **Generate.** Run models concurrently and save every output with its model, sample
   number, provider, tokens, cost and latency to `runs/<run_id>/responses.jsonl`. Interleave
   models rather than finishing one at a time, so that a guard stop still leaves a wide
   result. A model that errors gets one retry, then it's recorded as failed. Its failure is
   a finding, so don't substitute another model mid-run.

5. **Truncation gate.** Count empty outputs and any with `completion_tokens` within 5% of
   the limit. Regenerate those with a higher limit, if the budget allows. Never judge a
   truncated output.

6. **Judge against the objective.** Use the win and failure wording in
   `selection/objective.md` and the ranked soft requirements. For quality you have to read,
   the most useful judge is often a reader: read the outputs in session or hand them to the
   user, and use an LLM judge to pre-sort a large field. Judge each output once. Name each
   model's habit or tic as you go.

7. **Sort into tiers, not a ranking.** Two outputs can't support a leaderboard, and fine
   score gaps mean nothing at this n.

   | Tier | Meaning |
   |---|---|
   | Advance | Both outputs clearly meet the objective |
   | Maybe | One strong output, or strong with a named flaw |
   | Out | A hard failure: refusal, truncation, ignored brief, or simply weak |

8. **Write up.** `runs/<run_id>/report.md` and `report.json`: tiers, measured cost per output
   next to the estimate, latency, failures, the dataset or input revision, panel, judge and
   spend against cap. `runs/<run_id>/examples.md`: verbatim excerpts showing the clearest
   contrasts, each checked against `responses.jsonl` with a script. Update the README banner
   to `proof of concept (<date>): <n> models × <k> outputs, $<spent>`. Commit the configs,
   `selection/`, reports, `examples.md` and `spend.json`. Raw JSONL stays out of git. Push.

9. **Stop.** Don't start a follow-up run, `publish-run` or `analyse-findings`.

## Report back

Spend against cap, n models × k outputs, the tiers with one line per model on why, measured
cost per output for the Advance tier, and two or three short quoted contrasts. Say this is a
screen, not a ranking. If the user wants more confidence in a choice, the follow-up is a
second wide pass with different inputs across the Advance and Maybe tiers, or `full-run`.

## Don't

- Don't rank models or quote score differences from a wide run, and don't feed one to
  `package-results` or `analyse-findings`, which refuse `wide-` runs.
- Don't raise the cap mid-run. If the guard stops the run, report what finished.
- Don't quietly narrow the field to save money. Say what was dropped.
