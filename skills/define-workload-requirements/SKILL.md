---
name: define-workload-requirements
description: Turn a specific workload into concrete model requirements - real context load, output length, modalities, capabilities, cost per output - with each requirement traced to a feature of the work. The foundation for intelligent model selection. Use when the user says "what does this workload need", "what should I look for in a model for X", "work out the requirements for X", or before drawing up candidates.
---

# Define the workload requirements

This is the foundational step of model selection. A general question ("which model is
best?") has no answer. A workload does. The job here is to look hard at what this
particular work demands and say which requirements follow from it, so that candidates can
be chosen for a reason and not from a leaderboard.

Read `selection/objective.md` first. If it doesn't exist, run `define-objective`.

## 1. Look at real work, not a description of it

Get an actual example: a real prompt, a real input, a real good output. Measure them.
Estimate tokens as characters ÷ 4 for English, and ÷ 2 for Hebrew, Arabic or CJK text.
If no example exists, say the figures are assumed and mark them `"assumed": true`.

## 2. Work through each axis

| Axis | What to establish | Why it's easy to get wrong |
|---|---|---|
| Context load | Tokens actually sent per call: system prompt, retrieved material, history | The advertised window isn't the need. Size for the real input plus output, with margin |
| Context use | Must the model use all of it, or only find one fact? | A big window doesn't mean holding the middle of it. Long-range use is a capability, not a number |
| Output length | Tokens per output, single pass or several | `max_output` is often far below the context window, and long output degrades before it truncates |
| Reasoning | Does thinking help this work, and at what setting will production run? | Thinking tokens are billed as output and can triple the cost. State a setting, then test at that setting |
| Modalities | What goes in and what comes out | Includes audio and images hidden inside "documents" |
| Structure | Free text, or a strict format or tool calls? | Needs `structured_outputs`, `response_format` or `tools` in the catalogue |
| Language | Which languages, how well, any mixing | Multilingual claims rarely cover the user's language at production quality |
| Content tolerance | Will the topics trigger refusals or sanitising, from the model or the host's filter? | Often the first thing to fail, and invisible on general boards |
| Cost | Price per output at the real token mix, with no cache hits unless production gets them | Input can dominate: a shorter output may save almost nothing |
| Latency and volume | Interactive or batch, calls per day | Decides whether a slow reasoning model is even a candidate |
| Constraints | Data policy, region, provider, quantization, open weights | Filters the catalogue before quality comes into it |

## 3. Separate hard from soft, and name the irrelevant

- **Hard:** a model failing this can't do the job. These filter the catalogue.
- **Soft:** qualities that rank the survivors. The catalogue can't see them; the eval
  exists to measure them. Rank them, and note which public evidence bears on each, if any.
- **Irrelevant:** what general rankings measure but this work doesn't need. Write this
  down: it stops an impressive score from steering the shortlist.

Every requirement carries a `because`, naming the feature of the work that forces it. If
you can't name one, it isn't a requirement.

## Worked example: a long-form podcast script

> Task: read a ~28k-token prompt, write a ~3,800-word two-host comedic dialogue in one pass.

- **Context load:** ~28k in, ~6k out, so `min_context` 40,000 with margin. A 1M window buys nothing.
- **Output:** `min_max_output` 8,000, because a script must complete in one pass.
- **Reasoning:** production runs it off, so test with it off.
- **Cost:** input dominates, so a shorter test script hardly saves money. The lever is how many runs.
- **Soft, in order:** dialogue has life; holds the middle of a long piece; host voices stay distinct; length discipline.
- **Irrelevant:** coding, maths and agentic scores. General intelligence ranks say almost nothing here.

## Output

Write `selection/requirements.json`. `scripts/openrouter_catalogue.py filter` reads
`tokens` and `hard`. Omit any hard key that doesn't apply.

```json
{
  "workload": "One-sentence description",
  "measured_from": "path or description of the real example",
  "tokens": {"input": 28000, "output": 6000, "reasoning_overhead": 1.0, "assumed": false},
  "hard": {
    "min_context": 40000,
    "min_max_output": 8000,
    "input_modalities": ["text"],
    "output_modalities": ["text"],
    "required_parameters": ["max_tokens"],
    "max_cost_per_output_usd": 0.12,
    "released_after": null,
    "exclude_labs": [],
    "exclude_ids": [],
    "exclude_free": true
  },
  "hard_reasons": {"min_context": "because ...", "max_cost_per_output_usd": "because ..."},
  "soft": [{"rank": 1, "quality": "...", "because": "...", "evidence": "public board or none"}],
  "irrelevant": ["..."],
  "run_settings": {"reasoning": "off", "temperature": null},
  "sampling": {"outputs_per_model": 2}
}
```

`reasoning_overhead` multiplies output tokens in cost estimates: 1.0 with reasoning off,
2–3 with it on, unless measured. `required_parameters` uses the catalogue's
`supported_parameters` names.

## Report back

A short table of hard requirements with their reasons, the ranked soft qualities, and
what was marked irrelevant. Name any figure that was assumed. The user should correct
this before candidates are drawn up, because everything after it inherits its mistakes.

## Next

`probe-openrouter`, then `shortlist-candidates`.
