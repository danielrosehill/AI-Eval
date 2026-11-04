---
name: install-eval-cli
description: Install an evaluation framework CLI on Linux (Inspect AI, DeepEval, promptfoo, lm-evaluation-harness, LightEval, EvalScope) and confirm it runs. Use when the user says "install promptfoo", "set up Inspect", "I want to use a framework", "which eval CLI should I use", or before setup-framework-eval.
---

# Install an eval framework CLI

Assumes Linux with `uv`. Package names and versions below were checked on 2026-11-04;
confirm the version at install time, as these move quickly.

## Choose

| Tool | Best for | Package | Command | Needs |
|---|---|---|---|---|
| Inspect AI | Agents, tool use, safety, sandboxed tasks | `inspect-ai` | `inspect` | Python 3.11+ |
| promptfoo | Comparing prompts and models from YAML, CI gates, red teaming | `promptfoo` (npm) | `promptfoo` | **Node 22.22+** |
| DeepEval | Pytest-style tests of LLM apps, RAG metrics | `deepeval` | `deepeval` | Python 3.9+ |
| lm-evaluation-harness | Standard academic benchmarks | `lm-eval` | `lm-eval` | Python 3.10+; GPU for local models |
| LightEval | Hugging Face benchmarks and leaderboards | `lighteval` | `lighteval` | Python 3.10+; GPU for local models |
| EvalScope | Broad benchmarks, multimodal, performance tests | `evalscope` | `evalscope` | Python 3.10+ |

Recommend one. If the project already uses a framework, use that. The full list is in
`data/awesome-ai-evaluations-tools.md`, and `setup-framework-eval` maps eval types to tools.

## Install

**Inside a project, install as a dev dependency.** Python frameworks import the project's
code, so they must share its environment:
```bash
uv add --dev inspect-ai openai     # Inspect reaches OpenRouter through the openai package
```

**As a standalone tool:**
```bash
uv tool install inspect-ai --with openai
uv tool install deepeval
uv tool install lm-eval
```

**Just to try it,** with nothing left behind: `uvx --from inspect-ai inspect --version`.

**promptfoo:** check `node --version` first. On anything older than 22.22 it refuses to run,
so switch version (`nvm install 24 && nvm use 24`) rather than forcing it. Then
`npx -y promptfoo@latest --version`, or `npm i -D promptfoo` in a project.

Never use bare `pip install` into the system Python.

## Connect a model provider

The key goes in the environment, never in a config file. With OpenRouter:

| Tool | How |
|---|---|
| Inspect AI | `inspect eval task.py --model openrouter/<lab>/<model>` with `OPENROUTER_API_KEY` |
| promptfoo | `providers: [openrouter:<lab>/<model>]` with `OPENROUTER_API_KEY` |
| DeepEval, lm-eval, LightEval, EvalScope | Their OpenAI-compatible option, pointed at `https://openrouter.ai/api/v1`. Check the current docs, as flags differ by version |

## Telemetry

DeepEval and promptfoo send usage telemetry by default. Tell the user, and turn it off if
they want: `DEEPEVAL_TELEMETRY_OPT_OUT=1`, `PROMPTFOO_DISABLE_TELEMETRY=1`.

## Verify

Run the tool's version or help command, then the smallest real thing it can do without
spending: `inspect list tasks`, `promptfoo validate`, `lm-eval ls tasks`. A clean install isn't
proof that the provider works, so the first paid call is a single sample.

## Report back

Tool, version, where it's installed, and how the key reaches it. Next: `setup-framework-eval`.
