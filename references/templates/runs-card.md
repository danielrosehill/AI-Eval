---
license: cc-by-4.0
language:
- en
pretty_name: <Name> Eval (runs)
tags:
- evaluation
- model-outputs
- llm-as-judge
configs:
# One config per run. Add a block for each new run_id; keep the old ones.
- config_name: <run_id>
  data_files:
  - split: responses
    path: <run_id>/responses.jsonl
  - split: judge_scores
    path: <run_id>/judge_scores.jsonl
---

# <Name> Eval: runs

Raw outputs from runs of [<Name>-Eval](https://github.com/<owner>/<Name>-Eval): every model response, the judge's scores and, where collected, human A/B preferences. The summarised reports live in the GitHub repo under `runs/<run_id>/`.

Test prompts: [<owner>/<Name>-Eval](https://huggingface.co/datasets/<owner>/<Name>-Eval).

## Runs

| Run | Date | Prompts (dataset revision) | Models | Judge | Report |
|---|---|---|---|---|---|
| `<run_id>` | <YYYY-MM-DD> | <n> (`<commit sha>`) | <slugs> | <slug> | [report](https://github.com/<owner>/<Name>-Eval/blob/main/runs/<run_id>/report.md) |

## Files per run

| File | One row per | Key fields |
|---|---|---|
| `responses.jsonl` | (prompt, model) | `prompt_id`, `model`, `response`, `usage`, `finish_reason` |
| `judge_scores.jsonl` | (prompt, model) | `prompt_id`, `model`, `scores`, `rationale` |
| `judge_pairs.jsonl` | (prompt, model pair) | `prompt_id`, `a`, `b`, `winner`, `rationale` |
| `human_prefs.jsonl` | rated pair | `prompt_id`, `choice`, `tags`, `note` |

<Correct the key fields to what the harness actually writes.>

## Caveats

<Known problems with a run, e.g. truncated responses, a judge known to misjudge recent events.>
