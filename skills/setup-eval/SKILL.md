---
name: setup-eval
description: Set up an evaluation in the current workspace. Use when the user wants to scaffold a single eval — choosing an existing framework (DeepEval, Inspect AI, OpenAI Evals, lm-evaluation-harness, LightEval, OLMES, Promptfoo, etc.), adapting an existing benchmark, or preparing a clean slate for a custom eval. Writes a brief, installs deps, and stubs the eval directory.
---

# Set Up an Evaluation

Scaffolds one eval inside an eval-runner workspace. Output lives under `evals/<eval-slug>/`.

## Arguments

`$ARGUMENTS` may include:
- **Name/slug** (required) — kebab-case identifier, e.g. `translation-he-en-quality`.
- **`--framework=<name>`** — one of the frameworks in `data/awesome-ai-evaluations-tools.md`, or `custom`.
- **`--type=<type>`** — `tool-use`, `translation`, `rag`, `agent`, `classification`, `summarisation`, `multimodal`, `vision`, `code-gen`, `safety`, `custom`.
- **`--basis=<ref>`** — existing benchmark/eval to adapt (URL, HF dataset id, or paper id).

## Procedure

1. **Confirm context.** Verify the working directory looks like an eval-runner workspace (has `evals/`, `datasets/`, `results/`, `docs/`). If not, offer to run `/eval-runner:new-workspace` first.

2. **Pick a framework.** If `--framework` not supplied, read `data/awesome-ai-evaluations-tools.md` (bundled with the plugin) and propose 2–3 good fits for the stated eval `--type`. Call out trade-offs (language, judge model cost, parallelism, reporting). Default recommendations by type:
   - `tool-use`, `agent` → Inspect AI, OpenAI Evals, Harbor
   - `translation`, `summarisation`, `classification` → DeepEval, lm-evaluation-harness, LightEval, OLMES
   - `rag` → DeepEval, OpenEvals, Phoenix, Evidently
   - `multimodal`, `vision` → EvalScope, LightEval
   - `safety` → Giskard OSS, Inspect AI
   - Quick/TypeScript → Evalite, Promptfoo
   - General judge-only → simple-llm-eval, OpenEvals

3. **Write a brief.** Create `evals/<slug>/BRIEF.md` capturing:
   - Why this eval exists (what decision it informs)
   - What is being evaluated (model, prompt, pipeline, agent)
   - Input distribution / dataset source
   - Scoring approach (exact match, LLM-as-judge, pairwise, rubric, custom metric)
   - Success criteria (thresholds, acceptance)
   - Out of scope

4. **Scaffold the directory:**
   ```
   evals/<slug>/
   ├── BRIEF.md
   ├── config.{yaml|py|ts}   # framework-native config
   ├── dataset/              # eval inputs (or pointer to datasets/<id>/)
   ├── judges/               # rubric prompts / graders
   ├── run.sh                # one-line invocation
   └── README.md             # how to run + interpret
   ```

5. **Install deps.** Add the framework to the workspace's chosen dep manager (Python: uv/pip, TS: pnpm/npm). Prefer `uv` if `pyproject.toml` exists. Don't assume — ask if unclear.

6. **Stub the judge / scorer.** If LLM-as-judge, write the rubric in `judges/` as a standalone prompt with explicit input/output contract and failure handling.

7. **Report.** Summarise what was created, what the user needs to fill in (dataset pointer, API keys), and the command to run it.
