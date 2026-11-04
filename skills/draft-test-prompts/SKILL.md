---
name: draft-test-prompts
description: Write an eval's test prompts as data/prompts.jsonl with a dataset card, publish them as the eval's Hugging Face dataset, and link it from the README. Use after setup-eval, or when the user says "write the prompts", "publish the prompt set", "push the test set to HF", or "add prompts to the eval".
---

# Draft and publish test prompts

Turns the design in the eval's README into a versioned prompt set. The prompt set's
source of truth is `data/prompts.jsonl` in the GitHub repo, and the HF dataset is
uploaded from `data/`.

**References.** Read `../../references/conventions.md` (prompt record schema) and use
`../../references/templates/dataset-card.md`. If that path doesn't resolve, clone `danielrosehill/AI-Eval` and read it there.
Worked examples:
`danielrosehill/American-Centrism-Eval` `data/` (dimensions + controls) and
`danielrosehill/Israel-Palestine-Framing-Eval` `data/` (mirrored pairs).

## Steps

1. **Read the README's Mechanism and Grading sections.** The prompts implement the
   design exactly. If a design choice is missing, add it to Open questions and ask;
   don't settle it silently in the data.
2. **Draft the prompts.**
   - Balance the dimensions. About 8 per dimension is enough for a v0.1.
   - Keep ambiguous prompts truly ambiguous: no wording that hints at the answer the
     eval is looking for, unless that wording is the test, as with British spellings
     in a US-spelling probe. Note those deliberate cases in the card.
   - Add **controls** that mirror an ambiguous prompt with the ambiguity removed, and
     link them with `control_for`.
   - For framing evals, write **mirrored pairs** (`pair_id`, `side`) that differ only
     in the framing.
   - For loaded-premise prompts, add `premise` and a dated `reality` note. The judge
     grades against the note, so it must be accurate and must say where a topic is
     genuinely debated.
   - If the eval measures a lean towards one side, add counterweight series for the
     other sides (see "Counterweights" in `conventions.md`).
   - Give every record a `*_tell` field describing what a failing answer looks like.
     The judge and the human grader both use it.
3. **Validate** before writing: every line parses as JSON, IDs are unique, every
   `control_for` and `pair_id` resolves, and the counts per dimension match the
   card. Use a short Python check, not a visual skim.
4. **Write `data/README.md`** from the dataset-card template: front matter with a
   `test` split on `prompts.jsonl`, a "Version 0.1 draft (<today>)" note, the counts
   table and the fields table.
5. **Update the repo README.** Fill in the Test prompts section from the template
   comment (badge, counts, upload command), and change the banner to
   `draft prompts, not yet run (<today>)`.
6. **Commit, push, upload.**
   ```bash
   git add -A && git commit -m "Add v0.1 test prompts and link the Hugging Face dataset" && git push
   hf upload <owner>/<Name>-Eval data . --repo-type dataset --commit-message "v0.1 prompts"
   ```
   If the dataset doesn't exist yet, run `hf repo create ... --repo-type dataset`
   first (public; `--private` only for an eval the user asked to keep private).
   Uploading never changes a dataset's visibility.
   The command uploads everything in `data/`, so `data/` must hold only
   `prompts.jsonl` and `README.md`. Check before every upload. Run output belongs
   in `runs/` and the `-Runs` dataset, never in the prompts dataset ("One artifact,
   one job" in `conventions.md`).
7. **Verify the upload itself.** Load the dataset with
   `datasets.load_dataset("<owner>/<Name>-Eval", split="test")` (a private
   dataset needs the `hf` login token), or read the
   dataset viewer through the Hub API, and check the row count equals the local
   line count. A 200 on the upload proves nothing about the viewer parsing the
   file.
8. If the eval is public, run `register-eval`: it moves to stage `prompts`
   (`built` if a harness already exists).
9. **Stop.** Report the counts and the dataset URL, plus anything in the prompts
   that needs the user's review (e.g. balance of anchors or reference notes). The
   task ends here. Don't build a harness, don't run anything, and don't ask whether
   to run. At most, add one line that a wide `run-eval` (default $5 cap) or a
   `full-run` is available. See "Where a task stops" in `conventions.md`.

## Changing prompts later

To **add** prompts to an existing set, use `add-prompts`. It hands the writing to a
Haiku subagent and keeps validation and publishing in the parent. To change existing
prompts, edit `data/prompts.jsonl`, never the Hub copy. Upload again with a commit message
naming the change. Runs record the dataset commit they used (see `run-eval`), so
older results stay interpretable.
