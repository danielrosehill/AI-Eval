# Pitfalls seen while running evals

Each of these happened on a real run. The source is `Dan-Eval/docs/method.md`
(run `poc-01`, 2026-10-19) unless stated otherwise (Propaganda-Bait-Eval items say so). Check every run against this list
before you trust its numbers.

## Generation

1. **A reasoning model's thinking uses up `max_tokens`, and `finish_reason` doesn't
   say so.** At `max_tokens: 1500`, DeepSeek V4.1 Flash returned empty content on 7 of
   24 prompts: `reasoning_tokens` was 1500 and `finish_reason` was `stop`, not
   `length`. Use 8000 for generation and 4000 for the judge. Save `usage` and
   `finish_reason` for every call. After generating, count empty responses and
   responses with `completion_tokens` near the limit. If there are any, raise the
   limit and regenerate them before you judge.
2. **No system prompt.** A behaviour eval measures the model's defaults, so add none
   unless the eval is about system-prompt adherence.
3. **Through OpenRouter, the provider can change between calls.** Record the model
   slug exactly as sent. Pin a provider (`provider.order`) if the eval compares
   providers.

## Judge

4. **The judge must not be one of the models under test.** A model must never grade
   its own answers.
5. **The judge marks real events after its training cutoff as hallucinated.**
   Gemini 3.8 Flash called the June 2025 Israel-Iran war a hallucination. Give the
   judge today's date and tell it not to mark claims false only because they are
   newer than its knowledge. Any prompt about recent events still carries this risk,
   and human ratings are the check against it.
6. **Position bias.** Shuffle the order of the two answers before each pairwise call.
   Better: judge both orders and count any disagreement as a tie. Dan-Eval has not
   done this yet. Its judge win rate went 0.71 → 0.56 → 0.50 across three runs on
   near-identical data.
7. **The judge's JSON can be cut off** the same way as in pitfall 1. Validate it and
   retry; never parse a partial object.
8. **Grade from the user's point of view.** Put a `rater_profile` in `config.json`
   describing the reader, and give it to the judge.
9. **"Account + one disclaimer" answers.** A model can spend most of an answer setting
   out a one-sided account and then add a single line saying it is disputed. A lenient
   judge labels that as challenged. Seen on `Propaganda-Bait-Eval` `smoke-01`
   (DeepSeek on Xinjiang: judged challenged, endorsement 3). Define in the judge prompt
   what does *not* count as a challenge, and spot-check these answers.
10. **Silent refusals.** Empty completions, stop-token cut-offs and one-line canned
   refusals ("I am sorry, I cannot answer that question") look like answers to a
   naive scorer. Mark any answer under ~15 words as refused without a judge call, and
   report refusals separately from the main score.
11. **One judge is not ground truth.** Before citing results, check the judge against
   a hand-labelled sample of 20–30 answers, or against a second judge from another
   lab, and report the agreement rate.

## Hosted arena (HF Space)

12. **The Space adds a query string.** HF embeds the app at `/?__sign=<jwt>`, so a
   handler comparing `self.path == "/"` returns 404 on huggingface.co but works on a
   direct request. Match on `urlsplit(self.path).path`.
13. **The Space's disk is wiped on restart.** Keep ratings in a private dataset. The
   arena downloads the file when it starts and uploads it after every rating.
14. **A ratings file edited by hand on the Hub gets overwritten** by the Space's next
   upload. Edit, then restart the Space at once (`HfApi().restart_space(...)`).
15. **Don't rate one run in two places at once.** The local arena and the Space each
   upload their whole copy, and the last upload wins.
16. **A private Space returns 404 when you are logged out.** That is the expected
   result and doesn't mean the deploy is broken. Check it while logged in.

## Analysis and write-up

17. **A smoke run is not a result.** `smoke-01`-style runs (2–3 prompts per series)
   check the harness. Never quote their numbers as findings. The same goes for
   `wide-` and `poc-` runs: their examples can be shared, their numbers can't.
18. **Small n, big claims.** With 8–12 prompts per cell, one answer moves a rate by
   8–12 points. Give n next to every rate, and a bootstrap interval for any comparison
   used in a headline.
19. **A fluent model-written analysis can be wrong about its own data.** Recompute
   every number in a findings memo or article from `report.json` or the raw JSONL with
   a script, and check every quoted excerpt against `responses.jsonl` verbatim.

## Reuse before building

20. **Check whether a published benchmark already covers the question.** Dan-Eval's
   Chinese-censorship component reuses `promptfoo/CCP-sensitive-prompts` and
   `augmxnt/deccp` instead of a repo of its own. Reused sets carry their own problems:
   the R1dacted paper found many CCP-sensitive prompts are unsafe in their own right,
   so a refusal may be ordinary safety filtering. Read the paper or card for known
   problems before you adopt a set.
