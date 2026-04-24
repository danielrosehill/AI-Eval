---
name: publish-eval
description: Publish an eval (definition + results) so others can reproduce it. Use when the user wants to share an eval publicly — as a GitHub repo, Hugging Face space, or a standalone writeup. Produces a clean, self-contained bundle with README, task spec, rubric, dataset pointer, and a run report.
---

# Publish an Evaluation

Takes a completed eval and packages it for external consumption.

## Arguments

- **Eval slug** (required).
- **`--target=<github|hf-space|local>`** — where to publish. Default `github`.
- **`--include-results=<run-id|latest|all|none>`** — whether to include run outputs. Default `latest`.
- **`--private`** — private GitHub repo (ignored for HF Space).

## Procedure

1. **Validate readiness.**
   - `evals/<slug>/` must contain `BRIEF.md`, `TASK.md` (or equivalent), `RUBRIC.md`, runnable config, and `README.md`.
   - At least one run under `results/<slug>/` (unless `--include-results=none`).
   - No secrets in files (scan for `sk-`, `hf_`, `Bearer`, `API_KEY=` etc. — flag and stop if found).

2. **Assemble the bundle.** Create a staging directory with:
   ```
   README.md             # pitch, how to run, how to interpret
   TASK.md
   RUBRIC.md
   DATASET.md            # (or pointer)
   config.<ext>
   run.sh
   judges/
   results/              # only if --include-results != none
   LICENSE               # default MIT unless user says otherwise
   CITATION.cff          # auto-generated; ask user to review
   ```

3. **Write the README.** Sections: What & why, Frameworks required, Quickstart (one command), Dataset provenance, Scoring approach, Known limitations, Results summary (if included), How to cite.

4. **Target-specific steps.**
   - `github`: `gh repo create danielrosehill/eval-<slug>` (Train-Case per user preference — confirm name), push, add topics `evaluation`, `llm-eval`, plus eval-type tag.
   - `hf-space`: scaffold a Gradio/Streamlit app shell that lets a visitor run the eval against their own model; push with `huggingface-cli`.
   - `local`: tar.gz the bundle into `published/eval-<slug>-<date>.tar.gz`.

5. **Record publication.** Append to `docs/publications.md` in the workspace: slug, target URL, date, included run ids.

6. **Report.** URL(s), any follow-ups (add a DOI via Zenodo? submit to a leaderboard?).
