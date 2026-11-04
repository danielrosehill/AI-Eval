---
name: deploy-arena
description: "Add human A/B rating to an eval: a blinded pairwise arena (local, or hosted on a private Hugging Face Space) whose ratings are kept in a private dataset and folded into the report alongside the LLM judge. Use when the user says \"I want to rate these myself\", \"set up the arena\", \"human eval\", \"deploy the arena to HF\", or \"compare the judge with my ratings\"."
---

# Deploy the human A/B arena

Pairwise human preference evaluation, as in Chatbot Arena: the same answer pairs the
judge saw are shown blind, in random left/right order. Nothing is trained on the
choices. The report then shows a judge view, a human view, a weighted composite, and
every pair where the judge and the human disagree.

**References.** Read the "Hosted arena" items in `../../references/pitfalls.md`. All
of them happened on the first deploy. If that path doesn't resolve, clone `danielrosehill/AI-Eval` and read it there.

**Reference implementation:** `danielrosehill/Dan-Eval`, which has
`daneval/arena.py` + `arena.html`, `space/Dockerfile`, `space/README.md`,
`space/deploy.sh`, and the "Hosted arena" section of `docs/method.md`. Copy and
adapt it.

## Steps

1. **Requires a run** with `responses.jsonl` (`run-eval` or `full-run`).
2. **Arena code.** Copy `arena.py` and `arena.html` into the eval's package. Keep
   these behaviours, which were each asked for:
   - Two-step rating: `1`–`4` or a click only selects, and `Enter` or Confirm saves.
     `Esc` clears the selection. `U` undoes the last saved rating and shows that pair
     again in the same order.
   - The choices are A, B, tie, and both bad, plus an optional note.
   - Preset per-answer tags from the eval's dimensions, e.g. Refusal, Hedging, US
     default. The server only accepts tags valid for that prompt.
   - Route on `urlsplit(self.path).path`, never `self.path`.
3. **Run it locally first:** `.venv/bin/python <pkg>/arena.py`, then open
   http://localhost:8765. Rate one pair, undo it, and check `human_prefs.jsonl`.
4. **Hosted (optional, private).**
   - `hf repo create <owner>/<Name>-Eval-Ratings --repo-type dataset --private`
   - `hf repo create <owner>/<Name>-Eval-Arena --repo-type space --space_sdk docker --private`
   - Set once, through `HfApi().add_space_secret(space, "HF_TOKEN", <token with write to the ratings dataset>)`
     and `add_space_variable(space, "RATINGS_REPO", "<owner>/<Name>-Eval-Ratings")`.
     Take the token from the environment or the `hf` login; never write it into a file
     in the repo.
   - Adapt `space/deploy.sh` (bundles `config.json`, prompts and the current run's
     `responses.jsonl`) and run it. Run it again whenever `run_id` changes or
     responses are regenerated.
   - **Verify while logged in** through the real huggingface.co URL, not the direct
     `*.hf.space` one, because the query-string bug only shows up there. Rate one pair
     and check that a commit appears on the ratings dataset.
5. **Report.** Extend `report.py` with the human view, the composite
   (`human_weight` in `config.json`, default 0.5), agreement on pairs rated by both,
   and the list of disagreements with the judge's rationale next to the human note.
   Tags are shown as counts and are not part of the win rate.
6. Document the arena in `docs/method.md` (where ratings live, how to deploy, how to
   pull ratings for the report). Commit and push.

## Filing and serving files

- If the overlay names a Hugging Face collection for rating Spaces, add the Space to it with a one-line note.
- An app that shows images or audio pulled with `snapshot_download` needs
  `demo.launch(allowed_paths=[HF_HUB_CACHE])`, or Gradio raises `InvalidPathError` on every item.
  Verify with `gradio_client` that a handler returns a file.

## Don't

- Don't rate one run locally and on the Space at the same time. The last upload
  overwrites the other.
- Don't edit the ratings file on the Hub without restarting the Space at once.
