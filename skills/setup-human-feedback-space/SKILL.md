---
name: setup-human-feedback-space
description: Set up a private Hugging Face Space that collects human preference feedback as training data - chosen and rejected pairs for RLHF, DPO or reward models - rather than for scoring an eval. Use when the user says "human feedback", "RLHF", "collect preferences", "preference data", "DPO dataset", "train a reward model", or "fine-tune on my ratings".
---

# Set up a human feedback Space

| | `deploy-arena` | This skill |
|---|---|---|
| Purpose | Measure which model is better | Build data a model will be trained on |
| Output | Win rates in a report | `prompt`, `chosen`, `rejected` records |
| What matters | Blinding, fair sampling | Coverage, consistency, a clear preference signal |

If the ratings won't be trained on, use `deploy-arena`. Building this collects data nobody uses.

## Before building

Settle these with the user, because they can't be fixed after collection:

- **What's being trained,** on what base model, and how much data that needs. DPO usually
  wants hundreds of pairs at the least, and a reward model far more. One person rating
  takes a while, so check the target is realistic before building.
- **What "better" means,** written as a one-paragraph guideline shown in the Space. Without it,
  preferences drift between sessions and the data teaches noise.
- **Licensing.** Some providers' terms restrict training competing models on their outputs. Check
  the terms of each model whose outputs will be used, and tell the user what you find.
- **Which outputs.** Pairs should be close enough to teach something. Outputs from the base
  model being trained are worth more than outputs from unrelated models, and a strong model
  against a weak one teaches little.

## Steps

1. **Generate candidates:** two or more outputs per prompt, from `run-eval` or a dedicated
   generation run. Paid generation needs its own approval, as in `run-eval`.

2. **Make pairs.**
   ```bash
   python3 scripts/blind_items.py pairs --responses <responses.jsonl> \
     --out items.jsonl --key key.json --per-output 2
   ```
   This randomises left and right. `key.json` stays local.

3. **Build the Space** as in `setup-annotation-space` steps 4–5, with the same invariants and
   the reviewer action "choose between A and B". Name it `<Name>-Feedback`, with the dataset
   `<Name>-Feedback-Data`. Both are always private. The form needs:
   - A, B, tie, both bad, with the guideline always visible,
   - an optional **strength** (slight or clear), as slight preferences are often dropped from training,
   - an optional note on why,
   - a correction box, as a human rewrite of a bad answer is the most valuable record there is.

4. **Check agreement early.** After about 30 ratings, re-show 5 earlier pairs. If the rater often
   disagrees with themselves, tighten the guideline before collecting more.

5. **Export.**
   ```bash
   python3 scripts/blind_items.py preferences --reviews reviews.jsonl \
     --items items.jsonl --key key.json --out preferences.jsonl
   ```
   Records carry `prompt`, `chosen` and `rejected`, the format TRL's `DPOTrainer` and
   `RewardTrainer` take. Ties and both-bad are dropped and counted. Report the counts, and check
   the balance across prompts and across which model won.

6. **Hold out a test split** before training, and keep it out of every training run, so the
   trained model can be evaluated on preferences it never saw.

## Don't

- Don't reuse arena or annotation ratings as training data without checking they were collected
  under one consistent guideline.
- Don't make the feedback dataset public until the user has reviewed it and the licensing is clear.
