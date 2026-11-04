---
name: setup-eval
description: Start a new eval of your own, one repo per eval. Checks whether one already exists, then creates a public GitHub repo with the design and rubric, reserves a public Hugging Face dataset for the prompts, and registers it in the public indexes. Private only when the user asks for it. Use when the user says "set up an eval for X", "new eval", "I want to test whether models do X", or "make this plan into an eval".
---

# Set up an eval

The first step for an eval the user designs themselves. It ends with a **placeholder**:
a **public** GitHub repo whose README sets out the question, the mechanism and the
rubric. Prompts come next (`draft-test-prompts`), then runs (`run-eval`, `full-run`,
`publish-run`). Don't ask about visibility: public is the default, and a placeholder
repo is a legitimate public seed.

Lifecycle and visibility rules: "Lifecycle" in `conventions.md`.

**References.** Read `../../references/conventions.md` first, and use
`../../references/templates/README.md`. If that path doesn't resolve, clone `danielrosehill/AI-Eval` and read it there.

## Inputs

- The question the eval answers, in the user's words.
- Optional: a plan file it graduates from, and example prompts. Everything is created public unless the user asks for
  this eval to be private.

## Steps

1. **Exists check: run these lookups in parallel.**
   - The user's own work: `<evals-dir>`, their repos, and any plan locations the
     overlay lists. An existing plan becomes the design; it does not mean the eval is
     already done.
   - Published benchmarks: Hugging Face (`hf` CLI or the Hub API, datasets search)
     and a web search for the topic plus "benchmark" / "eval dataset".
   - If a published set already answers the question, recommend reusing it rather
     than building a repo. Note its licence and any known problems.
     Then stop, and run `register-eval` if the user keeps an index. Building a
     duplicate is the failure to avoid here.
2. **Name it.** `<Subject>-Eval`, Train-Case, as specific as possible
   (`Israel-Palestine-Framing-Eval`, not `Bias-Eval`). State the name you chose in one
   line and go ahead. Rename it now if needed, before anything links to it.
3. **Write the README** from the template. Fill in:
   - The status banner: `placeholder (<today>)`, and the Visibility line
     `repo public · prompts public · runs none`.
   - The question.
   - **Mechanism**: the dimensions, each with two or three example prompts, and the
     controls. Every eval of a default behaviour needs controls that remove the
     ambiguity, to show the model can move off the default when told.
   - **Grading**: the shared 0–3 severity scale (0 = clean). Say how scores
     aggregate, per model and per dimension.
   - **Open questions**: anything you'd otherwise have to guess.
   - **Origin**: the plan file or notes it came from, with links.
   - **Related** and, if prompts will state false claims on purpose, **Disclaimer**.
   Keep the README for the design. Prompts, harness and results come later.
4. **Create the repo** in `<evals-dir>/<Name>-Eval`:
   ```bash
   cd <evals-dir> && mkdir <Name>-Eval && cd <Name>-Eval && git init
   # write README.md
   git add -A && git commit -m "Placeholder: scope and design"
   gh repo create <owner>/<Name>-Eval --public --source . --push \
     --description "<one-line question>"
   ```
   Use `--private` only when the user asked for this eval to be private.
5. **Reserve the prompts dataset.** Create it empty now, so the name is held and the
   link in the README isn't dead:
   ```bash
   hf repo create <owner>/<Name>-Eval --repo-type dataset
   ```
   Add `--private` only for an eval the user asked to keep private.
   Uploading content is `draft-test-prompts`'s job.
6. **Register.** Run `register-eval` (stage `planned`), and retire the plan file if
   it graduated from one. A public index never links a private repo.
7. **Report** the repo and dataset URLs, and the next step: `draft-test-prompts`.
   If the user asked for prompts in the same request, carry on into it. Otherwise
   stop here.

**Stop at setup.** This skill never leads into a run. Don't build a harness, and
don't propose or ask about running. See "Where a task stops" in `conventions.md`.

## Don't

- Don't write prompts into the README. They go in `data/prompts.jsonl`.
- Don't scaffold empty `data/`, `runs/` or harness folders.
- Don't make a combined repo for several evals. Each eval is atomic.
