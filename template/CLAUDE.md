# {{WORKSPACE_NAME}}

An evaluation workspace managed with the [ai-eval](https://github.com/danielrosehill/AI-Eval) plugin.

## Purpose

{{ONE_LINE_PURPOSE}}

## Layout

- `evals/<slug>/` — one directory per eval. Each contains `BRIEF.md`, `TASK.md`, `RUBRIC.md`, `config.*`, `run.sh`, `README.md`.
- `datasets/<id>/` — eval datasets (raw + processed, with a `CARD.md` and `HASH`).
- `results/<slug>/<run-id>/` — run outputs, scored, with `manifest.yaml` and `SUMMARY.md`.
- `docs/` — writeups, findings, rationale.

## Commands

- `/ai-eval:new-workspace` — provision a new workspace (use outside an existing one).
- `/ai-eval:create-eval` — design a custom eval (task spec, dataset plan, rubric).
- `/ai-eval:setup-framework-eval` — wire an eval to a framework.
- `/ai-eval:run-framework-eval` — execute an eval and capture results.
- `/ai-eval:document-eval` — write findings into `docs/`.
- `/ai-eval:publish-eval` — publish eval (and optionally results) to GitHub / HF Space.
- `/ai-eval:publish-dataset` — publish a dataset to Hugging Face Hub.

## Conventions

- Eval slugs are kebab-case and descriptive: `translation-he-en-quality`, `tool-use-calendar-agent`, `rag-legal-docs`.
- Run ids are `YYYY-MM-DD-HHMM-<slug>-<shortsha>`.
- Results are never edited after write — rerun with a new run id instead.
- Judges and rubrics are versioned; if you change the rubric, bump it and record the change in `RUBRIC.md`.
