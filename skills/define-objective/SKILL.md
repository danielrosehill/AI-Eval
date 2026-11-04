---
name: define-objective
description: Pin down what an eval is for before any model is chosen - the decision it informs, what a win looks like, who judges, and what's out of scope. First step of model selection. Use when the user says "I want to find the best model for X", "I'm running an eval for X", "help me work out what I'm testing", or starts an eval without a stated goal.
---

# Define the objective

An eval with no stated decision behind it produces numbers nobody can act on. This skill
writes the one page everything downstream reads: `selection/objective.md`.

`selection/` sits at the eval repo root, or under `evals/<slug>/` in a framework workspace.

## Establish

Take what the user has already said. Ask only for what's missing, in one short round.

| Field | Question it answers | Example |
|---|---|---|
| Decision | What changes depending on the result? | Which model writes the production podcast scripts |
| Task | What is the model actually asked to do, in one sentence? | Turn a research brief into a two-host dialogue script |
| Win | What does a clearly better output look like, in the user's words? | The dialogue has life; the hosts sound like people |
| Failure | What output would be unacceptable, however good the rest? | Refuses the topic; loses the thread halfway |
| Incumbent | What's used today, and what's wrong with it? | Model X: competent but shallow |
| Judge | Who decides: the user reading, an LLM judge, a metric? | The user reads; an LLM judge pre-sorts |
| Budget | What will this eval spend, and what can each production output cost? | $5 for the eval, about $0.12 per script |
| Out of scope | What is this eval deliberately not measuring? | Coding, agents, general intelligence |

The win and failure fields matter most. Keep the user's words rather than tidying them
into benchmark language: the judge and the report are built from them.

## Output

Write `selection/objective.md` with those fields as headed sections, and a dated first
line. If the user has an unresolved trade-off (quality against cost, say), record it as
an open question rather than deciding it.

## Next

`define-workload-requirements`. Carry on into it if the user asked for model selection
as a whole. Otherwise stop.
