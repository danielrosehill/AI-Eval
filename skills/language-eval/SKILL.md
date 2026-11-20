---
name: language-eval
description: Evaluate models for one non-English language: find that language's leaderboards and benchmarks first, then handle script, tokeniser, judge and contamination pitfalls. Use on "which model is best for <language>", "evaluate Hebrew/Arabic/Japanese quality", "language-specific leaderboard", "is this benchmark valid for my language".
---

# Evaluate models for a specific language

Generic English leaderboards say little about another language. Run this before `shortlist-candidates` or
`run-eval` when the work is in one non-English language.

## 1. Find the language's existing benchmarks

- Search for a curated index first (for Hebrew: the Hebrew-AI-Benchmarks index, reached through the
  `hebrew-ai-ecosystem` skill in the hebrew-ai-tools plugin), then a Hugging Face leaderboard Space for
  the language, then the Hub itself: datasets `filter=language:<iso>`, models `filter=<iso>`. Note
  `language=<iso>` returns noise.
- Separate benchmarks built natively for the language from machine translations of English ones
  (translated MMLU variants exist in many languages; forks are not comparable, so name the fork).
- A leaderboard built for base models and few-shot prompts does not transfer to chat APIs. Say which
  you are comparing.
- Check licences on the cards (some language benchmarks are non-commercial or `other`).

## 2. Include a native baseline

Add at least one model built for the language, or the comparison says nothing language-specific.
Do not compare base models zero-shot against chat models. Do not mix reasoning-enabled and disabled models,
and size `max_tokens` for the most verbose, since an empty answer scores as wrong.

## 3. Language-specific pitfalls

- **Normalise before string-match scoring.** Diacritics, final or variant letter forms, punctuation
  variants and invisible bidi marks differ between reference and output. Write the normalisation
  once, apply to both sides, record it. Exact match is often brittle; prefer F1 or chrF.
- **Tokeniser fertility.** Tokens per word can be 3 to 5 times higher for under-served scripts, so cost, latency
  and context limits skew. Log tokens in and out, and truncate fairly.
- **LLM judges are biased** toward English-style long, hedged answers and miss local context. Use two judges from
  different vendors, calibrate on 30 to 50 human-rated examples, prefer reference-based metrics.
- **Small test sets.** Report n and a bootstrap CI; paired comparison on the same examples; state the minimum
  detectable effect before calling a winner.
- **Contamination.** Public benchmarks, often Wikipedia-derived, are likely in training data, and native models
  trained on that Wikipedia are the most exposed. Anchor the decision on a private held-out set of 100 to
  200 of the user's own examples, never published; treat public scores as sanity checks.
- **Pin and log** dataset revision, model IDs as returned by the API, and date. Re-run before reusing old numbers.

## 4. Hand off

Then continue with `define-objective`, `shortlist-candidates` and `run-eval`; use `speech-eval` for ASR or TTS.

Worked example: Hebrew. The `hebrew-ai-tools` plugin (github.com/danielrosehill/Hebrew-AI-Tools) ships
`hebrew-llm-eval` (tasks, Hebrew normalisation rules, scripts) and `hebrew-ai-ecosystem` /
`hebrew-datasets` for the Hebrew indexes; use it rather than reimplementing for Hebrew.

## Sources

Generalised from [hebrew-llm-eval-suite](https://github.com/skills-il/developer-tools/tree/9b1ec48acf2354150d5963f7e6c18b8e28eae8b6/hebrew-llm-eval-suite) by Skills IL (MIT): the Hebrew-specific guidance is abstracted to any language.
