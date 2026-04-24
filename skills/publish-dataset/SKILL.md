---
name: publish-dataset
description: Publish an eval dataset to Hugging Face Hub (or GitHub as a fallback). Use when the user wants to share the inputs/labels used by an eval — with a dataset card, licensing, splits, and a content hash so downstream runs can verify integrity.
---

# Publish a Dataset

Packages a dataset from `datasets/<id>/` and pushes it to the Hub.

## Arguments

- **Dataset id** (required) — must match a directory under `datasets/`.
- **`--target=<hf|github>`** — default `hf`.
- **`--private`** — private dataset repo.
- **`--license=<spdx>`** — default `cc-by-4.0` (ask user if unclear).

## Procedure

1. **Pre-flight.**
   - `datasets/<id>/` exists with at least a `data/` folder and a `CARD.md` draft. If no `CARD.md`, stub one and ask the user to fill load-bearing sections before publish.
   - Scan for PII / secrets / copyrighted blobs. Stop and flag anything suspicious.
   - Confirm splits — `train/validation/test` or the user's custom split.

2. **Normalise format.** Prefer Parquet or JSONL with a consistent schema. Generate a `schema.json`. If source is CSV, convert. If source is images/audio, ensure a manifest file exists.

3. **Hash.** Compute a content hash (sha256 over sorted file hashes) and record it in `datasets/<id>/HASH`. This is what `run-eval` verifies.

4. **Dataset card.** Finish `CARD.md` with the HF standard sections: dataset summary, supported tasks, languages, dataset structure, data fields, data splits, source data, annotations, considerations for using the data, licensing, citation. Draft missing sections with `TODO` markers — don't fabricate.

5. **Push.**
   - `hf`: `huggingface-cli repo create` (dataset type), `huggingface-cli upload`. User defaults: the HF user is `danielrosehill` unless stated otherwise — confirm if ambiguous.
   - `github`: create a repo, use Git LFS for anything > 50MB, push.

6. **Cross-link.** Update the relevant eval's `DATASET.md` to point at the published URL and record the hash. If an eval config references the dataset, update it to pull from the Hub.

7. **Record publication.** Append to `docs/publications.md`.

8. **Report.** URL, hash, size, splits, license.
