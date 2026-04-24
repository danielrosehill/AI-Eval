# Claude-Eval-Runner-Plugin

A Claude Code plugin for setting up, running, documenting, and publishing AI evaluations — whether you're using an existing eval framework, adapting an existing benchmark, or designing a custom one from scratch.

## What it's for

Evaluating AI systems is the unglamorous half of AI work. This plugin is a harness for the harness work: scaffold an eval workspace, pick (or remix) a framework, design a rubric, run the thing, write down what you found, and publish it when it's worth sharing.

## Install

```bash
# from inside Claude Code
/plugin marketplace add <your-marketplace>
/plugin install eval-runner
```

Or add as a local plugin by pointing Claude Code at this directory.

## Commands

| Command | Purpose |
|---|---|
| `/eval-runner:new-workspace <name>` | Provision a new eval workspace (Train-Case name; optional `--private` / `--local-only`). |
| `/eval-runner:create-eval <slug>` | Design a custom eval — task spec, dataset plan, rubric. Use `--inspired-by` to remix an existing benchmark. |
| `/eval-runner:setup-eval <slug>` | Wire an eval to a framework. Use `--framework=` to pin, or let the plugin suggest based on `--type=`. |
| `/eval-runner:run-eval <slug>` | Execute an eval across one or more SUTs (`--sut=`), with manifest + summary under `results/`. |
| `/eval-runner:document-eval <slug>` | Write up rationale and findings into `docs/`. |
| `/eval-runner:publish-eval <slug>` | Publish the eval (and optionally results) to GitHub, a Hugging Face Space, or a local bundle. |
| `/eval-runner:publish-dataset <id>` | Publish a dataset to Hugging Face Hub with a dataset card and content hash. |

## Agent

- `eval-engineer` — autonomous subagent that coordinates the full design → setup → run → document → publish loop for non-trivial eval work.

## Ground truth

Bundled under `data/awesome-ai-evaluations-tools.md` is a snapshot of the [Awesome AI Evaluations & Benchmarks](https://github.com/danielrosehill/Awesome-AI-Evaluations-Tools) list — a curated canon of open-source eval frameworks, benchmarks, and observability platforms. The plugin reads this before recommending any tool, and flags when it goes off-list.

See [`data/README.md`](data/README.md) for refresh instructions.

## Workspace shape

```
<workspace>/
├── CLAUDE.md
├── README.md
├── evals/<slug>/           # BRIEF.md, TASK.md, RUBRIC.md, config, run.sh, judges/
├── datasets/<id>/          # data/, CARD.md, HASH
├── results/<slug>/<run>/   # manifest.yaml, SUMMARY.md, raw/
└── docs/                   # writeups and findings
```

## Conventions

- Eval slugs: kebab-case, descriptive (`translation-he-en-quality`, `rag-legal-docs`).
- Run ids: `YYYY-MM-DD-HHMM-<slug>-<shortsha>`.
- Results are append-only — rerun with a new id instead of editing.
- Every run has a manifest (dataset hash, framework version, git sha, cost) so it's reproducible.
- Repo names: Train-Case.

## License

MIT.
