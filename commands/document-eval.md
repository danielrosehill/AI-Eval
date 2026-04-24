---
description: Write up the rationale and findings of an eval into a durable document under docs/.
---

Produce a writeup for eval `$ARGUMENTS` covering: why this eval exists, what was tested, how it was scored, headline findings, per-stratum breakdown, notable failures with examples, caveats, and next steps.

## Procedure

1. Read `evals/<slug>/BRIEF.md`, `TASK.md`, `RUBRIC.md`, and the latest (or user-specified) manifest under `results/<slug>/<run-id>/`.
2. Write to `docs/<slug>-<run-id>.md`. Use the structure from `evals/<slug>/REPORT_TEMPLATE.md` if present; otherwise:
   - **Context** — why this eval, what decision it supports.
   - **Setup** — SUTs, dataset, scoring, sample size.
   - **Results** — headline number(s), tables, plots if requested.
   - **Failure analysis** — 3–5 representative failing items with commentary.
   - **Limitations** — known weaknesses of the eval itself.
   - **Recommendation** — what the user should do with this result.
3. Link the writeup from the workspace `README.md` under a `## Findings` section.
4. Do not fabricate numbers. If a metric is missing, write `N/A` and note why.
