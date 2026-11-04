---
name: setup-agent-eval-space
description: Set up an eval that needs no framework - the AI agent is the harness, following a written procedure to call the models, read the outputs and judge them. Use when the user says "just do it with Claude", "no framework", "keep it simple", "have the agent run it", or for a small eval where a framework would be overkill.
---

# Set up an agent-run eval space

For most small evals a framework is overhead. An agent with a short script can call the
models, read every output and judge against the objective. This skill makes that repeatable,
so a later session can run the same eval the same way.

**Use it when** there are up to about 100 outputs, quality takes reading, and the procedure may
still change. **Use a framework instead** (`install-eval-cli`) for standard benchmarks, CI
gates, thousands of items, or results others must reproduce exactly.

## Steps

1. **Pick the location.** `evals/<slug>/` in the project (`setup-repo-eval-space`), or a new
   folder if there's no project.

2. **Write `EVAL.md`,** the procedure a fresh agent follows with no other context:
   ```markdown
   # <Eval name>
   **Question:** the decision this informs (from selection/objective.md)
   **Inputs:** which ones, and where they live
   **Models:** selection/candidates.json
   **Settings:** temperature, reasoning, max_tokens, system prompt or none
   **Procedure:** generate → truncation gate → judge → report
   **Judging:** the rubric, in the user's words, and who judges
   **Budget:** the cap per run
   **Last run:** run_id, date, one-line result
   ```

3. **Add one small script,** `generate.py`, to send the inputs to each model and append to
   `runs/<run_id>/responses.jsonl`. Follow `run-eval` for the spend guard and record fields.
   The agent does the judging, so nothing else needs code.

4. **Keep judging honest.** The agent that chose the models shouldn't know which output is
   which. Blind them with `scripts/blind_items.py rate`, and have a subagent judge the items
   with only the rubric and the outputs. Unblind afterwards with `unblind`. Keep `key.json`
   out of its reach.

5. **Say what an agent judge can't do.** It shares blind spots with models like itself, and
   may favour its own family's style. For taste-led work, the user reads a sample of the
   outputs to confirm the verdicts. Don't include the judge's own family in the panel without
   saying so.

## Next

`define-objective` if `selection/` is empty, otherwise `run-eval`, whose wide-and-shallow
defaults apply. Stop here if the user asked only for the space.
