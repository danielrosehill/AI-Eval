---
name: new-workspace
description: Provision a new eval-runner workspace on disk. Use when the user wants to start a new evaluation project — scaffolds evals/, datasets/, results/, and docs/ directories, personalises CLAUDE.md, and (by default) creates a GitHub repo.
disable-model-invocation: true
allowed-tools: Bash(mkdir *), Bash(cp *), Bash(cat *), Bash(git init *), Bash(git add *), Bash(git commit *), Bash(gh repo create *), Bash(gh auth status), Bash(git push *), Read, Write
---

# Provision Eval-Runner Workspace

Creates a new workspace for evaluation work. The plugin's commands
(`/eval-runner:setup-eval`, `/eval-runner:create-eval`, `/eval-runner:run-eval`,
`/eval-runner:publish-eval`, `/eval-runner:publish-dataset`,
`/eval-runner:document-eval`) operate against this scaffold.

## Arguments

`$ARGUMENTS` is parsed as:

- **First positional**: workspace name (Train-Case — e.g. `My-Eval-Project`). Required.
- **Second positional** (optional): target parent path. Defaults to `~/repos/github/my-repos`.
- **`--private`** (optional): create the GitHub repo as private. Default: public.
- **`--local-only`** (optional): skip GitHub repo creation.

## Scaffold

```
<workspace>/
├── CLAUDE.md               # workspace-level context for Claude
├── README.md
├── evals/                  # one subfolder per eval
│   └── .gitkeep
├── datasets/               # eval datasets (raw + processed)
│   └── .gitkeep
├── results/                # run outputs, scored, with metadata
│   └── .gitkeep
├── docs/                   # rationale, findings, writeups
│   └── .gitkeep
└── .gitignore
```

## Procedure

1. Parse arguments. If name missing, ask.
2. Copy `template/` from the plugin into `<parent>/<name>/`.
3. Personalise `CLAUDE.md` — inject workspace name, date, and a short preamble describing what is being evaluated (ask the user in one line if not obvious).
4. `git init`, initial commit.
5. Unless `--local-only`, `gh repo create` (public by default, private with `--private`) and push.
6. Report the workspace path and repo URL.
