---
name: package-results
description: Turn an eval run into shareable outputs beyond the raw dataset. Produces tidy CSV tables with n and confidence intervals, charts, an excerpt sheet of verbatim answers, and an optional results brief PDF, all in exports/<run_id>/. Use when the user says "package the results", "export the results", "make charts", "give me a spreadsheet of the scores", or "make a results brief".
---

# Package results

The `-Runs` dataset is the complete record and is very data-heavy: one row per
answer. Most readers need something in between that and an article. This skill builds
that layer from a finished run. Everything goes in `exports/<run_id>/` in the eval repo
and inherits the repo's visibility.

**References.** Read `../../references/pitfalls.md` items 17–19 (smoke runs, small n,
checking numbers). If that path doesn't resolve, clone `danielrosehill/AI-Eval` and read it there.
Before drawing any chart, load the `dataviz` skill and follow it.

## Inputs

- A run in `runs/<run_id>/` that passed the truncation gate. The raw JSONL is either
  local or pulled from the `-Runs` dataset.
- Which formats the user wants. The default is tables + charts + excerpts. The brief
  PDF is opt-in.

## Outputs

| File | Built from | Contents |
|---|---|---|
| `tables/scores_by_model.csv` | report.json + raw | One row per model: headline score, n, 95% bootstrap interval, refusal rate, control failure rate |
| `tables/scores_by_model_dimension.csv` | raw | Long format: `model, dimension, metric, value, n, ci_low, ci_high` |
| `tables/per_answer.csv` | raw | Flat join of prompt fields + response + judge labels: one row per answer, for spreadsheet readers |
| `results.xlsx` (optional) | the CSVs | One sheet per CSV, header row frozen, plus a README sheet saying what each column means |
| `charts/*.svg` + `.png` | the CSVs | Headline per-model chart with intervals, a model × dimension heatmap, and the eval's own headline metric if it has one (e.g. selectivity) |
| `excerpts.md` | responses.jsonl | Verbatim answers that show each pattern: for every model, its best and worst scored answers, the borderline cases, and any control failures. Each has `prompt_id`, model, score and a truncation mark where shortened |
| `brief.pdf` (optional) | all of the above | 2–4 pages: question, method in one paragraph, headline chart, table, three excerpts, limitations |
| `MANIFEST.json` | | `run_id`, prompt dataset revision, runs dataset revision, generation date, and the list of files with sha256 |

## Steps

1. **Refuse smoke, wide and PoC runs.** If `run_id` starts with `smoke`, `wide` or `poc`, stop and say why.
2. **Write the script once, in the repo**: `<pkg>/export.py --run <run_id>`. It must
   regenerate every output from the raw files, so a corrected run re-exports in one
   command. Use pandas, plus matplotlib for charts. Install with `uv pip install`.
   Compute bootstrap intervals by resampling prompts (not answers) within each model
   and dimension, with 2,000 resamples and a fixed seed.
3. **Charts.** Follow `dataviz`: one message per chart, intervals shown, n in the
   axis labels or a footnote, the run date and the judge model in the caption. Save
   SVG for the web and PNG at 2x for documents.
4. **Excerpts.** Select them with code (by score), then read them yourself.
   Quote verbatim. Shorten only with `[…]`, never by paraphrasing.
5. **Brief PDF (if asked).** Use the `typst-document-generator` plugin's `briefing`
   or `public-doc` template (from the catalogue), feeding it the CSVs and SVGs. Put
   the Typst source in `exports/<run_id>/brief/`, so it can be rebuilt.
6. **Verify.** Re-read `scores_by_model.csv` against `runs/<run_id>/report.json`. The
   headline numbers must match exactly. A mismatch means the exporter and the report
   compute differently: find out which one is right before going on.
7. **Commit** `exports/<run_id>/` and the export script. Exports are small and
   derived, so they belong in git. If `per_answer.csv` is over ~5 MB, keep it out of
   git and add it to the `-Runs` dataset under `<run_id>/exports/` instead.
8. Report the file list and the headline table. Next: `analyse-findings`.
