# AI-Eval

Agent skills for evaluating AI models for a real job, from working out what the job needs
to a published write-up. Formerly `Claude-Eval-Runner-Plugin` (`eval-runner`), merged on
2026-11-04 with the author's private eval-authoring skills.

> **Status: v0.8.0 (2026-11-04).** `openrouter_catalogue.py` is tested against the live OpenRouter
> API, and `blind_items.py` on sample data. No eval has yet been taken end to end through the
> merged plugin, and no Space has been built from the new Space skills.

**Start here:** `start-eval` inspects the project, finds what's already set up, and routes to the
right skills.

## The default path

| Step | Skill | Produces |
|---|---|---|
| 1 | `define-objective` | `selection/objective.md`: the decision, what a win looks like, who judges |
| 2 | `define-workload-requirements` | `selection/requirements.json`: context load, output, capabilities and cost, each traced to the work |
| 3 | `probe-openrouter` | A dated catalogue snapshot; what's new; key and liveness checks |
| 4 | `shortlist-candidates` | `selection/candidates.json`: a wide, varied field with a reason for each |
| 5 | `run-eval` | A wide-and-shallow run under a hard spend cap, sorted into tiers |

### Wide and shallow

Many evals are narrow and long: a few models, many iterations. `run-eval` does the opposite:
12–20 models, about two outputs each. For model selection the larger risk is never having
tested the best model, and a second output is enough to rule out a fluke. A wide run is a
screen, so it reports tiers (advance, maybe, out), not a ranking. Spending stops at a hard cap,
$5 by default, and nothing paid starts until the estimate is approved.

## All skills

| Stage | Skill | Does |
|---|---|---|
| Where it lives | `setup-repo-eval-space` | An eval space inside an existing project repo |
| | `setup-agent-eval-space` | No framework: the agent is the harness, following a written procedure |
| | `install-eval-cli` | Install Inspect AI, promptfoo, DeepEval, lm-eval, LightEval or EvalScope on Linux |
| Methodology | `image-gen-eval` | Generative image models: sourcing, per-image pricing, human grading |
| | `rag-eval` | Retrieval and generation measured apart |
| | `agent-eval` | Tasks with checkable end states, sandboxing, reliability |
| | `speech-eval` | ASR with WER on real audio; TTS by blind listening |
| | `regression-eval` | A fixed test set against a baseline, for CI |
| Human judgement | `setup-annotation-space` | Blind grading on a private Hugging Face Space |
| | `deploy-arena` | Blind A/B between models |
| | `setup-human-feedback-space` | Preference data for RLHF, DPO or reward models |
| Build a standalone eval | `setup-eval` | Exists check, then a public repo with question, mechanism and rubric, plus a reserved dataset |
| | `draft-test-prompts`, `add-prompts` | Write or extend `data/prompts.jsonl` and its dataset card |
| Other runs | `full-run` | Every prompt across a panel, with judge and report. Explicit request only |
| | `informal-image-eval` | A few image models on fal, graded by hand in an annotation Space |
| Share | `publish-run`, `go-public`, `register-eval` | Raw data to Hugging Face, pre-publication review, index upkeep |
| Write up | `package-results`, `analyse-findings`, `draft-article` | Tables and charts, a verified findings memo, articles |
| Framework workspaces | `new-workspace`, `create-eval`, `setup-framework-eval`, `run-framework-eval`, `publish-eval`, `publish-dataset` | Many evals in one workspace, wired to third-party frameworks (DeepEval, Inspect AI, lm-evaluation-harness and others) |

The workspace skills also have `/ai-eval:` commands, and the `eval-engineer` agent coordinates a whole
eval. `references/` holds conventions, pitfalls from real runs and templates. `data/` holds a
snapshot of the [Awesome AI Evaluations & Benchmarks](https://github.com/danielrosehill/Awesome-AI-Evaluations-Tools)
list, which the framework skills read before recommending a tool.

## Install

```bash
/plugin marketplace add danielrosehill/Claude-Code-Plugins
/plugin install ai-eval@danielrosehill
```

Needs `OPENROUTER_API_KEY` in the environment for paid calls. `fetch`, `new` and `endpoints` work
without it. The scripts in `scripts/` need only the Python 3 standard library.

## Personal settings

The plugin is generic. Your GitHub owner, evals directory, indexes and spend rules go in a private
overlay directory that it reads at run time: see [`references/overlay.md`](references/overlay.md).

## Licence

MIT.
