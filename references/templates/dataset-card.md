---
license: cc-by-4.0
language:
- en
pretty_name: <Name> Eval (prompts)
task_categories:
- text-generation
tags:
- evaluation
- <topic tags>
size_categories:
- n<1K
configs:
- config_name: default
  data_files:
  - split: test
    path: prompts.jsonl
---

# <Name> Eval: test prompts

Test prompts for an evaluation of <the question>.

- **Code, design and results:** [github.com/<owner>/<Name>-Eval](https://github.com/<owner>/<Name>-Eval)
<- **Run data:** [<owner>/<Name>-Eval-Runs](https://huggingface.co/datasets/<owner>/<Name>-Eval-Runs) (add once the first run is published)>

This dataset contains the test prompts only. Model responses and scores are in the runs dataset, never here.

> **Version 0.1 draft (<YYYY-MM-DD>).** The prompts were drafted from the design and have not yet been piloted. Expect wording to change. Pin a commit if you use them.

## Contents

N prompts:

- **<n> <main> prompts** across <k> dimensions:

  | Dimension | Count | What it probes |
  |---|---|---|
  | `<dimension>` | n | <...> |

- **<n> controls** that <...>.

<Note any deliberate oddities, e.g. misspellings on purpose.>

## Fields

| Field | Description |
|---|---|
| `id` | <format> |
| `prompt` | The text sent to the model |
| <...> | <...> |

## Scoring

Score each response from 0 to 3: <one line per level>. See the GitHub repo for the full rubric.
