---
name: register-eval
description: "Keep the user's eval indexes in step with a public eval: add it or update its stage in whichever index, registry or scorecard the user keeps, and retire the plan file it graduated from. Called by setup-eval, draft-test-prompts, publish-run and go-public on stage changes; also when the user says \"index this eval\" or \"this plan is now a repo\"."
---

# Register an eval

Evals are public from creation, so they are registered at setup and updated at each
stage change. Indexes drift unless each stage change updates them.

**Where to register comes from the overlay.** Read `register.md` in the overlay directory
(`../../references/overlay.md`). It names the user's indexes and how each one is
edited, and it wins over this file. With no overlay file, ask once whether the user
keeps an index. If not, stop: nothing here is required for the eval to exist.

## Stages

| What exists | Stage | Typically after |
|---|---|---|
| Public repo with the design only | `planned` | `setup-eval` |
| Repo + published prompts, no harness | `prompts` | `draft-test-prompts` |
| Repo, prompts and harness, no full run | `built` | `run-eval` / `full-run` smoke |
| Published results | `results` | `publish-run` |

A repo with prompts is a legitimate public seed, not a plan. Never file it under planned.

## Steps

1. **Graduating a plan.** If the eval came from a plan file, delete that file and link
   its old URL from the eval README's Origin section. Keep no duplicate copy.
2. **Update each index** named in the overlay, reading its current files first. An
   index's own conventions override this skill.
3. **Never link a private repo from a public index.** It is a dead link that also
   announces the private work. An eval created private waits for `go-public`.
4. Commit each repo with a message naming the eval, and push.
