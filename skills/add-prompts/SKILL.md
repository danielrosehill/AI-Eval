---
name: add-prompts
description: Add test prompts to an existing eval's prompt set by delegating the writing to a Haiku subagent at once, then validating, merging and republishing in the parent. Use when the user says "add some prompts", "write more prompts for this", "extend the prompt set", "add a series on X", or "we need more controls". For an eval with no prompts yet, use draft-test-prompts.
---

# Add prompts through a Haiku prompt writer

Prompt writing is the separable, high-volume part of an eval, so it goes to a
subagent straight away. Don't ask whether to delegate, and don't write the prompts in
the parent first. The parent does what needs judgement: the brief, validation, the
merge and publishing. The subagent only writes candidates.

**References.** `../../references/conventions.md` (prompt record schema,
counterweights, "One artifact, one job"). If that path doesn't resolve, clone `danielrosehill/AI-Eval` and read it there.

## Inputs

- The eval: a local clone at `<evals-dir>/<Name>-Eval` with `data/prompts.jsonl`.
- What to add, in the user's words: a count, a dimension or series, controls, pairs,
  or "more of the same". With no count given, use 8 per dimension or series named,
  or 10 in all.

## Steps

1. **Read, don't write.** Read the README's Mechanism and Grading sections, the
   `data/README.md` card, and `data/prompts.jsonl`. Note the ID prefix and the
   highest number in use per series, the exact field set records use, and how
   controls and pairs are linked. If the request needs a design decision the README
   doesn't settle, such as a new dimension, add it to Open questions and ask before
   delegating.
2. **Delegate immediately.** Spawn one Agent with `model: "haiku"` (subagent type
   `general-purpose`). For large or independent additions, such as two new series,
   spawn one per series in a single message. Fill in this brief in full, because the
   subagent has no other context:

   ```
   You are writing test prompts for a model-behaviour eval. Write candidates only;
   do not edit any repo file.

   EVAL: <Name>-Eval. The question it answers: <one line from README>.
   WHAT A FAILING ANSWER LOOKS LIKE: <from Grading / the *_tell convention>.
   ADD: <n> prompts for <dimension/series>, <plus n controls / mirrored pairs>.
   IDS: continue from <last id>, e.g. <next id>, <next+1>. Controls use <control id form>.
   FIELDS (every record has exactly these keys, same types as the examples): <list>.
   EXAMPLES (existing records, match their style and length):
   <3–5 verbatim JSONL lines, including a control and a pair if the eval has them>
   EXISTING PROMPTS TO AVOID DUPLICATING (texts only):
   <every existing `prompt` value in that dimension or series>

   RULES:
   - Ambiguous prompts stay genuinely ambiguous: no wording that hints at the
     answer the eval is looking for.
   - Each control mirrors one of your new prompts with the ambiguity removed and
     sets control_for to that prompt's id.
   - Mirrored pairs differ only in framing (pair_id, side).
   - Loaded-premise prompts get a `premise` and a `reality` note dated <today>
     that says where a topic is genuinely debated. Do not invent facts; if unsure,
     say so in the note.
   - Every record gets the *_tell field describing a failing answer.
   - Vary phrasing, length and register like real users would.

   OUTPUT: write the records as JSONL to <scratchpad>/<name>-candidates-<series>.jsonl,
   one object per line, nothing else in the file. Then reply with the path and a
   one-line count.
   ```

   The subagent writes only into the scratchpad, never into the repo. That keeps
   writes in one place when several run at once.
3. **Validate the candidates** with a script, not a skim. It must check that every
   line parses, the keys match the existing records' key set exactly, IDs are new
   and unique and follow the prefix, every `control_for` and `pair_id` resolves
   within the merged set and every pair has both sides, and no `prompt` duplicates
   or near-duplicates an existing one (normalised lowercase match). Fix or drop
   failures. Don't re-delegate for a handful.
4. **Read every candidate.** Haiku is fast, not careful. Check each prompt
   against the eval's question: it probes the thing, it doesn't give the answer
   away, its `reality` note is accurate, and its `*_tell` is specific. Rewrite or
   drop weak ones. Check the `reality` notes hardest, because the judge treats them
   as ground truth.
5. **Merge.** Append to `data/prompts.jsonl`, keeping the file's existing order
   convention (grouped by series, controls after their series). Update
   `data/README.md`: counts per dimension, the fields table if anything changed,
   and the version note (e.g. 0.1 → 0.2 with today's date). Update the README's
   Test prompts counts.
6. **Publish.** This follows `draft-test-prompts` steps 6–7. Check `data/` holds
   only `prompts.jsonl` and `README.md`, commit
   ("Add <n> <series> prompts (v0.2)"), push,
   `hf upload <owner>/<Name>-Eval data . --repo-type dataset --commit-message "v0.2: add <n> <series> prompts"`,
   then verify that the loaded row count equals the local line count.
7. **Stop.** Report how many were added, how many were dropped or rewritten and
   why, and the dataset URL. Earlier runs stay valid: they recorded the dataset
   revision they used. Don't rerun anything.

## Don'ts

- Don't let the subagent edit `data/prompts.jsonl` or push. It writes candidates only.
- Don't put any model output in `data/`, including Haiku's reasoning or notes.
- Don't change existing records here. Rewording a published prompt is a deliberate
  change: name it in the commit, and note it in the card as invalidating comparisons
  for that ID.
