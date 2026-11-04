---
name: publish-run
description: Push an eval run's raw data (responses, judge scores, human ratings) to the eval's <Name>-Eval-Runs Hugging Face dataset (public by default), one config per run, and add the results to the README. Use after run-eval, or when the user says "publish the run", "push the results to HF", or "make a dataset of the run".
---

# Publish a run

Each eval has one runs dataset, `<owner>/<Name>-Eval-Runs`. Each run is a
folder `<run_id>/` in it and a `config_name` in its card, so new runs add to the
dataset and old ones stay intact. The GitHub repo keeps only the summary
(`runs/<run_id>/report.md`, `report.json`).

**References.** Use `../../references/templates/runs-card.md` and
`../../references/conventions.md`. If that path doesn't resolve, clone `danielrosehill/AI-Eval` and read it there.

Results never go into the prompts dataset `<owner>/<Name>-Eval`, not even a
small PoC run and not "just for now". See "One artifact, one job" in `conventions.md`.

## Steps

1. **Pre-flight.** The run passed the truncation gate: no empty responses, nothing
   truncated, and the report has been read against the raw answers. If not, say so
   and stop. A published run gets cited.
2. **Check the files** in `runs/<run_id>/`: every JSONL line parses, and every
   response row has `prompt_id`, `model` and `response`. Correct the runs card's
   "key fields" table to what the files actually contain.
3. **Human ratings.** If the run was rated in the hosted arena, pull the ratings
   first:
   ```bash
   hf download <owner>/<Name>-Eval-Ratings <run_id>/human_prefs.jsonl --repo-type dataset --local-dir runs/
   ```
   Rebuild the report so it includes them.
4. **Create the dataset once:**
   `hf repo create <owner>/<Name>-Eval-Runs --repo-type dataset`.
   Public, like the rest of the eval. Add `--private` only if the eval was created
   private, or the user asks to hold this run's raw data back.
5. **Card.** On the first run, write `README.md` from the template. On later runs,
   download the existing card, add a `configs` block and a Runs table row for the new
   run, and keep the old ones.
6. **Upload** into a staging folder laid out as on the Hub:
   ```bash
   STAGE=$(mktemp -d -p "$SCRATCH") && mkdir -p "$STAGE/<run_id>"
   cp runs/<run_id>/*.jsonl "$STAGE/<run_id>/" && cp <card> "$STAGE/README.md"
   hf upload <owner>/<Name>-Eval-Runs "$STAGE" . --repo-type dataset --commit-message "Add run <run_id>"
   ```
7. **Verify** with `load_dataset("<owner>/<Name>-Eval-Runs", "<run_id>", split="responses")`.
   The row count should equal the local file's. If a split's schema varies between
   rows (e.g. `scores` dicts with different keys), the viewer fails; fix it by
   making the fields uniform, not by dropping the split.
   Also list the prompts dataset's files
   (`HfApi().list_repo_files("<owner>/<Name>-Eval", repo_type="dataset")`).
   It should hold only the card and the prompts file. Anything run-shaped there
   breaks the separation rule; move it to `-Runs`.
   **Cross-links:** add a "Runs" link to `-Runs` in the prompts card if it isn't
   there yet, and upload that card change from `data/README.md`.
8. **Link from GitHub.** In the README, fill the Results section: a short table of
   headline scores per model, the run date, a badge to the runs dataset, and a link
   to `runs/<run_id>/report.md`. Update the banner. Commit and push.
9. If the eval is public, run `register-eval` to update its stage. Update the README
   Visibility line (`runs public`, or `runs private` if held back).
