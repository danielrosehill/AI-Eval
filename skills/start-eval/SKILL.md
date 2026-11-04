---
name: start-eval
description: The front door for evaluating anything - takes the user through an eval on their project, working out what already exists and routing to the right skills. Use when the user says "I want to do an eval on this project", "help me evaluate this", "set up evals", "how should I test this", "which model should this use", or names an eval goal without a method.
---

# Start an eval

Works out what the user has and what they need, then hands over to the right skills in
order. It does no eval work itself. Don't walk the user through every option: inspect
first, propose a route, and ask only about what inspection can't settle.

## 1. Look at what already exists

Check before asking anything:

| Look for | Means |
|---|---|
| `evals/`, `selection/`, `runs/`, `configs/` | An eval space exists. Extend it |
| `promptfooconfig.yaml`, `inspect_ai`, `deepeval`, `lm-eval`, `ragas` in dependencies or tests | A framework is in use. Use it, not a second one |
| Prompts in the code, model names, an LLM client | The workload, and the incumbent model |
| Hugging Face datasets or Spaces linked in the README, a `space/` folder | Rating infrastructure exists |
| `OPENROUTER_API_KEY`, `hf auth whoami`, `uv`, Node version | What can run now |
| The overlay (`../../references/overlay.md`) | The user's standing conventions |

Existing infrastructure wins. Never build a parallel setup beside it.

## 2. Settle the four choices

Propose an answer to each from what you found. Say what you assumed, and let the user correct it.

**What is being evaluated?**

| The job | Route |
|---|---|
| Choosing a text model for a job | `define-objective` → `define-workload-requirements` → `probe-openrouter` → `shortlist-candidates` → `run-eval` |
| Image generation | `image-gen-eval` (`informal-image-eval` for a quick periodic round) |
| Retrieval or a RAG pipeline | `rag-eval` |
| An agent or tool use | `agent-eval` |
| Speech recognition or synthesis | `speech-eval` |
| Guarding a prompt or model against regressions | `regression-eval` |
| A model behaviour worth publishing | `setup-eval`, then `draft-test-prompts` |
| An existing public benchmark | `new-workspace`, then `setup-framework-eval` |

**Where does it live?**

| Situation | Route |
|---|---|
| It's about this project **(default when inside a repo)** | `setup-repo-eval-space` |
| A standalone, citable eval | `setup-eval` |
| Several evals together, framework-driven | `new-workspace` |

**What runs it?**

| Situation | Route |
|---|---|
| A small eval, no framework needed **(default)** | `setup-agent-eval-space`: the agent is the harness |
| Standard benchmarks, CI, or a large or repeatable run | `install-eval-cli`, then `setup-framework-eval` |

**Who judges?**

| Situation | Route |
|---|---|
| Quality only a reader can judge, few outputs | The user or agent reads them. Nothing to set up |
| Scores or labels against a rubric, from any browser | `setup-annotation-space` |
| Blind A/B between models | `deploy-arena` |
| Human preferences kept as training data | `setup-human-feedback-space` |
| Exact answers or metrics | Scored automatically by the harness |

## 3. Confirm the route, then run it

State the route as a short numbered list with the reason for any non-default choice, and
get a yes. Then run each skill in turn, passing along what's known so nothing is asked twice.

Paid steps keep their own approval: nothing here authorises spending. If the user asked
only to set up, stop when the space exists.

## Report back

What was found, the route taken, what now exists, and the next step.
