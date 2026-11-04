---
name: analyse-findings
description: Write the analytical findings memo for an eval run. States what the numbers show, with evidence tiers, tests the author's hypotheses (including those that didn't hold), and covers limitations. An adversarial check against the raw data runs before anything is kept. Writes findings/<run_id>/findings.md. Use when the user says "analyse the results", "what did we find", "write up the findings", or "LLM analysis of the run".
---

# Analyse findings

Turns a packaged run into prose in analytical language: what was measured, what it
shows, how sure we can be, and what it doesn't show. This memo is the source for any
blog post or article (`draft-article`), so its accuracy caps theirs.

**References.** Read `../../references/pitfalls.md` items 9, 11 and 17–19. If that path doesn't resolve, clone `danielrosehill/AI-Eval` and read it there.

## Inputs

- `runs/<run_id>/report.json`, `exports/<run_id>/` (run `package-results` first if it
  is missing) and the raw `responses.jsonl` and judge files.
- The eval README (question, mechanism, grading, open questions) and
  `docs/method.md`.
- Optional: the user's hypotheses ("I expect DeepSeek to carry the CCP line but not
  the Kremlin one"). Ask once if none are given. Testing a stated hypothesis makes a
  sharper memo than describing everything.

## Evidence tiers

Tag every claim with one tier. Never mix two tiers in one sentence.

| Tier | Means | Example |
|---|---|---|
| **MEASURED** | Arithmetic over the run, reproducible by script | "DeepSeek challenged 2 of 10 `ccp` premises (20%, CI 0–45%) against 9 of 10 `kremlin` premises" |
| **TEXTUAL** | A verbatim excerpt and where it comes from | `pbe-ccp-02`, DeepSeek: "…" |
| **READING** | Interpretation, with the fair alternative stated | "This fits training-data alignment with state media. An alternative is provider-side filtering on OpenRouter, which this run cannot distinguish" |

## Structure of `findings.md`

1. **Header**: eval, `run_id`, run date, models, judge, prompt and runs dataset
   revisions, n.
2. **Headline findings** (3–5): each is one MEASURED sentence, the TEXTUAL evidence
   under it, then an optional READING.
3. **Hypotheses tested**: each stated hypothesis, with a verdict of held, did not
   hold, or inconclusive, and the numbers behind it. Report the ones that failed as
   plainly as the ones that held. An eval that confirms everything it expected is
   suspect.
4. **Per-model notes**: one short paragraph each.
5. **Surprises and anomalies**: odd refusals, judge disagreements, provider effects.
6. **Limitations**: n per cell, a single judge and whether it was validated, the
   prompt version, language, date sensitivity, and the author-written reference
   notes.
7. **What would change the conclusions**: the next run that would test them.

## Steps

1. **Refuse smoke, wide and PoC runs** (`run_id` starting `smoke`, `wide` or `poc`).
2. **Compute first, write second.** Write `findings/<run_id>/numbers.json` with a
   short script: every figure the memo will cite, each with n and an interval. Draft
   only from that file and the excerpts. Never write a number from memory of the
   report.
3. **Draft** `findings.md` in the structure above. Write plainly: no "notably",
   "striking" or "alarming". Let the numbers carry the weight.
4. **Adversarial check.** Launch a subagent with the draft, `numbers.json` and the
   raw files, briefed to refute each headline: wrong arithmetic, an excerpt that
   isn't verbatim or that cuts out a qualifying sentence, a cherry-picked example
   that the overall distribution contradicts, or a READING with a likelier
   alternative. Fix or drop what it breaks. Treat its report as claims to check,
   not facts.
5. **Mechanical verification.** Run a script that finds every number in
   `findings.md` and checks it against `numbers.json`, and checks every quoted
   excerpt as a substring of `responses.jsonl`. Both must pass.
6. Add the memo's headline findings to the "Findings" section of `docs/method.md`
   (short, with a link). Commit `findings/<run_id>/` and push.
7. Report the headline findings and the hypothesis verdicts. Next: `draft-article`
   if the user wants a post or a pitch.
