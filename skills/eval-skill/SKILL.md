---
name: eval-skill
description: Write a skill specific to one of the user's own evals (apply this eval's annotations, run its next round, refresh its metrics, file its notes), in that eval's repo, and register it in the user's eval index so it is found the next time the eval is mentioned. Use when the user says "make a skill for this eval", "this should be a skill for the X eval", or when the same eval-specific sequence has been done twice.
---

# Write an eval-specific skill

Generic method lives in ai-eval (`screen-then-rank`, `speech-eval`, ...). What one eval has learned (its file layout,
dataset names, quirks, the annotator's conventions) lives with that eval, as skills in its own repo.

## Steps

1. **Resolve the eval** with `my-evals`. No entry yet: add one first.
2. **Pick the repo:** the eval's private working repo if it has one (annotations, notes), else its main repo. Skills go
   in `<repo>/.claude/skills/<name>/SKILL.md`, where Claude Code loads them when working in that repo, and
   `my-evals` loads them from anywhere through the index.
3. **Write it** for an agent opening the repo cold: frontmatter `name` and a `description` that says when to use it
   in the user's own words ("apply my notes", "next round"); then steps with explicit paths, commands, dataset and
   Space IDs; then rules (append-only data, what is public). Point to the generic ai-eval skill it specialises
   instead of repeating its method.
4. **Helpers:** a script the skill runs goes in the same repo's `scripts/`, with a docstring that is enough to run it.
5. **Register:** add the skills path to the entry's `skills` in `evals.json` (if not already there), bump `updated`,
   and mention the skill in the repo's `CLAUDE.md` "Common jobs".
6. **Generic part?** If a step would help any eval of this kind, also add it to the matching generic ai-eval skill,
   with no user-specific details (habit: build it public, then bring it in).
7. Commit and push the eval repo.
