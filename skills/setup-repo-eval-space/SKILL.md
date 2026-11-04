---
name: setup-repo-eval-space
description: Add an eval space inside an existing project repo, so evals live next to the code and prompts they test. Use when the user says "put the evals in this repo", "add an eval folder here", "set up evals for this project", or when start-eval routes here. For a standalone citable eval use setup-eval; for a multi-eval framework workspace use new-workspace.
---

# Set up an eval space in the repo

Evals about one project belong with that project: they test its real prompts, and they
change when it changes.

## Steps

1. **Check the repo.** Note its visibility (`gh repo view --json visibility`), language,
   and any existing `evals/` or `tests/` conventions, and follow them. If a space exists, add to it.

2. **Create the layout.** Make folders as their first file goes in, never empty ones.
   ```
   evals/
   ├── README.md               # what's evaluated here, how to run it, latest result per eval
   └── <slug>/
       ├── selection/          # objective.md, requirements.json, candidates.json
       ├── data/               # inputs, or a pointer to where they live
       ├── configs/            # one file per run plan; never edit one that has run
       └── runs/<run_id>/      # report.md, report.json, examples.md, spend.json
   ```

3. **Ignore raw output.** Add these to `.gitignore`: `evals/*/runs/*/*.jsonl`,
   `evals/*/runs/*/images/`, `evals/*/runs/*/audio/`, and `evals/*/runs/*/key.json`.

4. **Test the real thing.** The eval calls the project's actual prompt or pipeline by
   importing it or reading the file. A copied prompt goes stale and the eval then tests
   something production no longer does. If that's impossible, say so in `evals/README.md`.

5. **Keep it out of the product.** Eval dependencies go in a dev group
   (`uv add --dev`, `npm i -D`). Exclude `evals/` from packaging and deployment if
   the build would otherwise include it.

6. **Add the pointer.** One line in the project README, and in `CLAUDE.md` or `AGENTS.md`
   if the repo has one, saying where evals live and how to run them.

## Private data

Eval inputs and outputs can carry whatever the project handles. In a private repo, or with
real user data, everything stays private: no public datasets or Spaces, and any Hugging Face
artifact is created private. The public-by-default rule in `conventions.md` is for
standalone evals, not for this.

## Next

Stop here if the user asked only for the space. Otherwise carry on with the route from
`start-eval`, usually `define-objective`.
