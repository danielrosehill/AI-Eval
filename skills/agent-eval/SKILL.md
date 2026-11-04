---
name: agent-eval
description: Evaluate an AI agent or tool-using model - tasks with checkable end states, sandboxing, and repeat-attempt reliability. Use when the user says "evaluate my agent", "test tool calling", "how reliable is this agent", "which model is best for agents", or "does it complete the task".
---

# Evaluate an agent

**Grade the end state, not the transcript.** Did the file change, the test pass, the record
appear? An agent can narrate success it didn't achieve, and reach the right result by a route
you wouldn't have predicted. Checking state handles both.

## Steps

1. **Write real tasks.** 5–15, taken from what the agent will actually do, each with a script that
   checks the outcome and returns pass or fail. Include a task that can't be done, as agents
   that claim success on the impossible are the most dangerous kind.

2. **Sandbox it.** Each attempt starts from a clean state, in a container or throwaway copy, with
   no real credentials and no write access to anything real. Mock external services. Agent runs
   can do real damage, so never test against production.

3. **Pin the setup.** Same tools, system prompt, step limit and token limit for every model.

4. **Go wide first.** Run many models × 2 attempts per task, as in `run-eval`, to drop the ones
   that can't do it at all.

5. **Measure reliability on the survivors.** This is the one place where repeats earn their
   cost: agent outcomes vary between attempts, and a task passed 3 times in 5 won't be
   dependable in production. For the Advance tier only, run about 5 attempts and report how
   many passed. Say so when asking for approval.

6. **Budget for it.** A single attempt can be many calls, each re-sending a growing context, so
   cost per task can be far above a single-turn estimate. Measure one attempt per model before
   estimating the rest, and set a hard step limit.

7. **Record more than pass or fail:** steps, tokens, cost and time per task, tool-call errors, and
   for failures, which step went wrong. Failure patterns are the most useful output.

8. **Choose tooling.** Inspect AI has sandboxing and agent scaffolds built in, and Harbor runs
   agent tasks (`install-eval-cli`). Use `setup-agent-eval-space` only for a few simple tasks, and
   have the checks done by script, not by the agent's own reading.

## Don't

- Don't let the agent under test grade itself.
- Don't count a run as a pass if the checker couldn't run. Report it as an error.
- Don't compare models with different tool definitions or step limits.
