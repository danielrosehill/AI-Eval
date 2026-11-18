---
name: screen-then-rank
description: Two-pass human evaluation of model outputs - first a fast pass/fail screen (every output, failures must say why), then blind pairwise head-to-heads among the outputs that passed, ranked with Bradley-Terry. The default way to judge outputs by hand when the question is "which of these is acceptable, and which acceptable one is best" (TTS voices, image models, rewrites, translations). Use when the user says "pass/fail then pairwise", "screen then rank", "first say which ones are fine, then compare the good ones", "two-pass annotation", or sets up human judgement for an eval and has not asked for a rating scale.
---

# Screen, then rank

The author's preferred method for human judgement of model outputs (Daniel, 2026-11-18, first used on the Hebrew
TTS bake-off): don't score everything on 1-5 scales first. Make two passes.

1. **Screen.** Give every output **Pass** or **Fail**, and nothing more qualitative. A Fail must carry at least one
   structured reason, drawn from a short list made for the task (for TTS: a word with the stress on the wrong syllable,
   a mispronounced word with the IPA heard and expected, a glitch, truncation, wrong voice or language). Record any
   attribute the selection depends on as you go (for TTS: the voice's gender).
2. **Rank.** Take only the outputs that passed. For each item (prompt or sentence), compare them **head to head,
   blind**, in random left/right order: A better, B better, tie, or both bad. "Both bad" sends both back as late fails,
   with a reason. Fit a **Bradley-Terry** model to the outcomes, counting a tie as half a win to each side, to get a
   ranking overall and per item. Report win rates and the number of comparisons beside it.

Quality scales (1-5 naturalness, clarity...) are an optional third pass, only if a finer read of the finalists is needed.

## Why this order

- **Pass/fail is fast and consistent.** "Is this fine or is it a problem?" is the decision people actually make.
  Absolute 1-5 scores drift across a session and between annotators.
- **The reasons are data.** Structured failure reasons (which word, what went wrong) replace free-form comments, and
  they show what fails as well as how often.
- **Pairwise is where the effort goes.** Head-to-heads among acceptable outputs are more reliable than absolute scores,
  and they are spent only where the choice is real.
- **It scales down.** Pass 1 alone already answers "which can we use". Pass 2 is needed only when several pass.

## Steps

1. **Requires outputs** from a run (`run-eval`, `full-run`, or a bake-off's own generator), with a manifest of items
   x systems (one output per pair).
2. **Write the failure taxonomy** from the objective's failure wording before anyone annotates. Keep it short: two or
   three structured, word- or span-level types plus a handful of output-level chips plus "other + comment". Decide
   which attributes to record in pass 1 (gender, language, length...).
3. **Build the Space.** Private, with a private annotations dataset (`<owner>/<Name>-Eval-Ratings`, see
   `../../references/conventions.md`), blind by default. Store each pass in its own file: `screen.jsonl` (system,
   item, verdict, reasons, attributes, note, annotator, timestamp; the latest line per (system, item) wins) and
   `pairs.jsonl` (item, left, right, outcome, note, annotator, timestamp).
   - **Audio:** use `danielrosehill/TTS-Pronunciation-Annotation-Starter`, the reference implementation of both
     passes. It is a Docker Space with a config, so a new eval writes a config, not code. It also has word-level stress
     and IPA tags and per-language IPA packs.
   - **Text or images:** adapt `setup-annotation-space` for pass 1 and `deploy-arena` for pass 2. They are the same
     two forms, fed from the screen's survivors.
4. **Schedule the pairs.** Pass 2 uses only the systems that passed screening on that item. With up to 6 survivors,
   compare every pair. With more, take a balanced random subset in which each system appears about equally often.
   Show progress.
5. **Report.**
   - Pass rate per system, and failures by reason and by item (most-failed words or spans).
   - Bradley-Terry ranking with win rates and comparison counts.
   - Where an LLM judge also ran, its view kept apart from the human one, and the disagreements listed.
6. **Record the method** in the eval's README: the two passes, the failure taxonomy, where the annotations live, and
   how the ranking was fitted.

## Don't

- Don't ask for quality scores in pass 1. That is the slow, drifting part the method exists to avoid.
- Don't accept a Fail with no reason.
- Don't run pass 2 on outputs that failed the screen, or show system names before a verdict is saved.
- Don't rank from fewer than about 3 comparisons per system. Say the ranking is provisional instead.
