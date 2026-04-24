# {{WORKSPACE_NAME}}

An evaluation workspace managed with the [eval-runner](https://github.com/danielrosehill/Claude-Eval-Runner-Plugin) plugin.

## Purpose

{{ONE_LINE_PURPOSE}}

## Layout

- `evals/<slug>/` — one directory per eval. Each contains `BRIEF.md`, `TASK.md`, `RUBRIC.md`, `config.*`, `run.sh`, `README.md`.
- `datasets/<id>/` — eval datasets (raw + processed, with a `CARD.md` and `HASH`).
- `results/<slug>/<run-id>/` — run outputs, scored, with `manifest.yaml` and `SUMMARY.md`.
- `docs/` — writeups, findings, rationale.

## Commands

- `/eval-runner:new-workspace` — provision a new workspace (use outside an existing one).
- `/eval-runner:create-eval` — design a custom eval (task spec, dataset plan, rubric).
- `/eval-runner:setup-eval` — wire an eval to a framework.
- `/eval-runner:run-eval` — execute an eval and capture results.
- `/eval-runner:document-eval` — write findings into `docs/`.
- `/eval-runner:publish-eval` — publish eval (and optionally results) to GitHub / HF Space.
- `/eval-runner:publish-dataset` — publish a dataset to Hugging Face Hub.

## Conventions

- Eval slugs are kebab-case and descriptive: `translation-he-en-quality`, `tool-use-calendar-agent`, `rag-legal-docs`.
- Run ids are `YYYY-MM-DD-HHMM-<slug>-<shortsha>`.
- Results are never edited after write — rerun with a new run id instead.
- Judges and rubrics are versioned; if you change the rubric, bump it and record the change in `RUBRIC.md`.
