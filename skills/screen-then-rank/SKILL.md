---
name: screen-then-rank
description: Two-pass human evaluation of model outputs - first a fast pass/fail screen (every output, failures must say why), then blind pairwise head-to-heads among the outputs that passed, ranked with Bradley-Terry. The default way to judge outputs by hand when the question is "which of these is acceptable, and which acceptable one is best" (TTS voices, image models, rewrites, translations). Use when the user says "pass/fail then pairwise", "screen then rank", "first say which ones are fine, then compare the good ones", "two-pass annotation", or sets up human judgement for an eval and has not asked for a rating scale.
---

# Screen, then rank

The author's preferred method for human judgement of model outputs (Daniel, 2026-11-18, first used on the Hebrew
TTS bake-off): don't score everything on 1-5 scales first. Make two passes.

1. **Screen.** Listen to or read each output whole and give it **Pass** or **Fail**, and nothing more qualitative. A
   Fail takes one tap on an output-level reason category made for the task (for TTS: mispronunciation, wrong emphasis,
   glitch, truncated or skipped words, wrong voice or language, other). Record any attribute the selection depends on
   as you go (for TTS: the voice's gender). **Detail is a separate, optional layer**: which word failed, the syllable
   stressed vs the one that should be, IPA heard vs expected, quality scores. Add it when it's useful, and never
   require it to save a verdict.
2. **Rank.** Take only the outputs that passed. For each item (prompt or sentence), compare them **head to head,
   blind**, in random left/right order: A better, B better, tie, or both bad. "Both bad" sends both back as late fails,
   with a reason. Fit a **Bradley-Terry** model to the outcomes, counting a tie as half a win to each side, to get a
   ranking overall and per item. Report win rates and the number of comparisons beside it.

Quality scales (1-5 naturalness, clarity...) are an optional third pass, only if a finer read of the finalists is needed.

**Either pass can be done by voice** (`spoken-annotations`): say the verdict, reason and detail for each output, and a
model applies them to the structure afterwards.

**Generate in rounds, only for survivors** (Daniel, 2026-11-18). Don't generate the full item set for every system up
front. Round 1 is one short item per system (and per variant). Screen it, and then generate the next, harder or longer
item only for the systems that passed (for TTS: a paragraph of 3-4 sentences, then specific traps), until a few remain
for pass 2. The first Hebrew TTS bake-off made 500 clips, most of them for voices excluded after one listen. Cheap
automatic measurements (loudness, pace) can run on everything; generation spend and listening time go only to survivors.

## Why this order

- **Pass/fail is fast and consistent.** "Is this fine or is it a problem?" is the decision people actually make.
  Absolute 1-5 scores drift across a session and between annotators.
- **The reasons are data.** Structured failure reasons (which word, what went wrong) replace free-form comments, and
  they show what fails as well as how often. The detail layer, when used, says exactly where.
- **Pairwise is where the effort goes.** Head-to-heads among acceptable outputs are more reliable than absolute scores,
  and they are spent only where the choice is real.
- **It scales down.** Pass 1 alone already answers "which can we use". Pass 2 is needed only when several pass.

## Steps

1. **Requires outputs** from a run (`run-eval`, `full-run`, or a bake-off's own generator), with a manifest of items
   x systems (one output per pair).
2. **Write the failure taxonomy** from the objective's failure wording before anyone annotates. Keep it short: a
   handful of output-level reason categories plus "other + comment" for the screen, and, for the optional detail layer,
   two or three structured word- or span-level types (for TTS: stress, mispronunciation in IPA). Decide
   which attributes to record in pass 1 (gender, language, length...).
3. **Build the Space.** Private, with a private annotations dataset (`<owner>/<Name>-Eval-Ratings`, see
   `../../references/conventions.md`), blind by default. Store each pass in its own file: `screen.jsonl` (system,
   item, verdict, fail_reasons, attributes, optional detail, note, annotator, timestamp; the latest line per (system, item) wins) and
   `pairs.jsonl` (item, left, right, outcome, note, annotator, timestamp).
   - **Audio:** use `danielrosehill/TTS-Pronunciation-Annotation-Starter`, the reference implementation of both
     passes. It is a Docker Space with a config, so a new eval writes a config, not code. It also has word-level stress
     and IPA tags and per-language IPA packs.
   - **Text or images:** adapt `setup-annotation-space` for pass 1 and `deploy-arena` for pass 2. They are the same
     two forms, fed from the screen's survivors.
4. **Run pass 2 through `pairwise-eval`** when it's available (the author's plugin for blind A/B:
   `start-pairwise-eval`, `package-pairwise-round`, `run-playoff`, `pairwise-results`). Feed it only the survivors of
   each item. Its adaptive play-off (knock out anything with a head-to-head loss, send only the deciding pairs, repeat
   to a winner) needs far fewer votes than all pairs. Its `pairwise-results` fits Bradley-Terry and unblinds. If it's
   not available, schedule the pairs yourself:
5. **Schedule the pairs.** Pass 2 uses only the systems that passed screening on that item. With up to 6 survivors,
   compare every pair. With more, take a balanced random subset in which each system appears about equally often.
   Show progress.
6. **Report.**
   - Pass rate per system, and failures by reason and by item (most-failed words or spans).
   - Bradley-Terry ranking with win rates and comparison counts.
   - Where an LLM judge also ran, its view kept apart from the human one, and the disagreements listed.
7. **Record the method** in the eval's README: the two passes, the failure taxonomy, where the annotations live, and
   how the ranking was fitted.

## Don't

- Don't ask for quality scores in pass 1. That is the slow, drifting part the method exists to avoid.
- Don't accept a Fail with no reason category, and don't require the detail layer to save one.
- Don't run pass 2 on outputs that failed the screen, or show system names before a verdict is saved.
- Don't rank from fewer than about 3 comparisons per system. Say the ranking is provisional instead.
