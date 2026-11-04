# Conventions for an authored eval

Personal settings (`<owner>`, `<evals-dir>`, indexes, spend rules) live in the private
overlay and win over this file: see `overlay.md`.

These conventions come from the evals built this way on 2026-10-19: `Dan-Eval`
(composite), `Israel-Palestine-Framing-Eval`, `American-Centrism-Eval` and
`Propaganda-Bait-Eval`. When something here
conflicts with what those repos actually do, the repos win; update this file.

## Lifecycle: public by default

An eval is **public from creation**. These evals are deliberate public seeds, run for
the author's own use and for anyone interested, so keeping them private defeats the
purpose. A public placeholder or an unrun prompt set is a
legitimate state: the banner says what exists.

| Stage | Banner word | Typical visibility |
|---|---|---|
| Design only | `placeholder` | public |
| Prompts drafted | `draft prompts, not yet run` | public |
| Harness checked on a subset, or a wide run done | `proof of concept` | public |
| Full run, results reviewed | `v1 results` | public; `go-public` review before results are cited |

**Each artifact has its own visibility.** The code repo, the prompts dataset and the
runs dataset are decided separately. Skills create each one **public**, and private
only when the user asks for that eval or that artifact, e.g. prompts held back to
avoid contaminating training data. A private artifact goes public through `go-public`.
Record the current state in the README's `Visibility` line (see the template) so an
agent can read it without calling the GitHub and HF APIs.

The ratings dataset and the arena Space are always private: a public arena would let
anyone write ratings.

## Where a task stops

**Setting up is the whole task by default.** "Set up an eval", "draft the prompts" or
"make this into an eval" ends when the repo and the prompts dataset exist. Don't
assume running comes next, don't ask "shall I run it?", and don't build a harness
ahead of a run nobody asked for. In the report, one line can say which run options
exist.

Running happens only when the user asks, at one of three tiers:

| The user says | Tier | Skill | Spend |
|---|---|---|---|
| nothing about running | none | stop after `setup-eval` / `draft-test-prompts` | $0 |
| "run it", "test run", "try some models", "spend ~$N", "get some examples" | wide | `run-eval` | hard cap, default **$5** of OpenRouter credit; estimate approved first |
| "run the whole thing", "full run", "every prompt" | full | `full-run` | whatever the panel costs; estimate approved first |

When the user asks to run and the tier isn't clear, choose wide.

## Where each thing lives

| Thing | Home | Name |
|---|---|---|
| Design, rubric, harness, reports, exports, findings | GitHub repo | `<owner>/<Name>-Eval` (Train-Case) |
| Test prompts | HF dataset | `<owner>/<Name>-Eval` (same name as the repo) |
| Raw run data | HF dataset | `<owner>/<Name>-Eval-Runs`, one config per run |
| Human A/B ratings (optional) | HF dataset, always private | `<owner>/<Name>-Eval-Ratings` |
| Human A/B arena (optional) | HF Space (docker), always private | `<owner>/<Name>-Eval-Arena` |
| Local clone | `<evals-dir>/<Name>-Eval` | |

`<owner>` and `<evals-dir>` come from the overlay (`references/overlay.md`). Without one,
use the authenticated GitHub user and ask once for the directory.

**One artifact, one job: the prompts dataset never carries results.** Keeping the artifacts clean matters more than keeping their number down.
The prompts dataset holds the test set and its card, nothing else. It has no response,
score, verdict or model columns, no `<run_id>/` folders, no run configs, and no results
in the card beyond a link. Results go to `<Name>-Eval-Runs`, which is created at the
first published run even when that run is small. If you find results in a prompts
dataset, move them to the runs dataset; don't add more. The rule works in both
directions: the runs dataset doesn't re-host the prompts. Each run records the prompts
dataset revision it used.

**The three artifacts link to one another.** The repo README links both datasets.
The prompts card links the repo and, once one exists, the runs dataset. The runs card
links the repo, the prompts dataset and each run's report. A missing link is a defect;
fix it in the same step that created the artifact.

**Run data lives in two places, by weight.** The `-Runs` dataset is the canonical
home of raw data: every response, judge score and rating, loadable with
`load_dataset` and viewable on the Hub. The GitHub repo holds only small derived
files: `runs/<run_id>/report.*`, `exports/`, `findings/`. Raw JSONL stays out of git.
It grows with every run and model, git history keeps it forever, and in git it gets
neither the Hub viewer nor `load_dataset`. Anyone reading the repo sees the results
there. Anyone re-analysing them pulls the dataset.

**Source of truth for prompts is the GitHub repo** (`data/prompts.jsonl`). The HF
dataset is uploaded from `data/`, so it is never edited on the Hub.

**Raw run JSONL goes to HF, and the summary stays in GitHub.** `.gitignore` holds
`runs/*/*.jsonl`. GitHub keeps `runs/<run_id>/report.md` and `report.json`. Dan-Eval's
`poc-01` predates this rule and keeps its JSONL files in git. Do not copy that.

## Repo layout

```
<Name>-Eval/
├── README.md            # banner + visibility, question, mechanism, grading, results, open questions, origin, disclaimer, licence
├── data/
│   ├── prompts.jsonl    # source of truth for the test prompts
│   └── README.md        # the HF dataset card
├── docs/method.md       # pipeline, judge rules, scoring formulas, outputs table, findings per run
├── config.json          # the default (or smoke) run
├── configs/<panel>.json # named model panels, e.g. chinese-labs.json
├── <pkg>/               # harness: generate.py, judge.py, report.py (+ arena.py)
├── runs/<run_id>/       # report.md + report.json only
├── exports/<run_id>/    # package-results: tables, charts, excerpts, brief PDF
└── findings/<run_id>/   # analyse-findings + draft-article: findings.md, article drafts
```

Create folders as the first file goes in. Never scaffold empty ones.

## Run IDs

`smoke-01` for a harness check on a subset (the config's `ids` or `series` lists), then
`<YYYY-MM-DD>-<panel>` or `v1-<panel>` for full runs. `wide-01`, `wide-02`, … for wide-and-shallow runs (`run-eval`): a screen of many models, not a ranking. `poc-NN` is the older name for the same kind of run; treat it the same. A smoke run is never cited as a
result.

## Status banner

The first lines under the title of the README:

```
> **Status: <stage> (<YYYY-MM-DD>).** <one or two sentences on what exists and what doesn't>
>
> **Visibility:** repo <private|public> · prompts <private|public|none> · runs <private|public|none>
```

A new eval starts with `repo public · prompts public · runs none`. Update the line on
every stage or visibility change. It is the first thing an agent reads.
Dataset cards carry the same status sentence.

## Prompt record schema

Every prompt record has `id` and `prompt`. Add the fields that fit the eval:

| Field | Use |
|---|---|
| `id` | Short prefix + number, e.g. `amc-01`, `pbe-ccp-01`; controls `amc-c01`, `pbe-ccp-c01` |
| `dimension` or `series` | Which sub-question or line the prompt probes |
| `kind` / `is_control`, `control_for` | Controls: an ambiguous prompt with the ambiguity removed, or the same prompt form with an accurate premise. They catch models that fail by reflex the other way, e.g. over-challenging |
| `pair_id`, `side` | Mirrored pairs (same event, opposite framing) |
| `prompt` | The exact text sent to the model |
| `premise`, `reality` | For loaded-premise prompts: the claim taken for granted, and the author's reference note on what is wrong with it. The judge treats `reality` as ground truth, so date it |
| a `*_tell` field (e.g. `us_default_tell`) | What a failing answer looks like. Guidance for a human or LLM grader |

**Counterweights.** When an eval measures a lean towards one side, include the other
sides as series too (Propaganda-Bait-Eval added `kremlin` and `us_progressive`). Without
them, a lean can't be told apart from general compliance. Comparing a model against
itself across series (**selectivity**) is usually the headline number.

## Rubric

The default is severity 0–3, with 0 = clean, written as a table in the README. The
scale is the same across evals, so Dan-Eval can put them side by side. A response that
asks a clarifying question instead of assuming scores 0.

The user may specify a different rubric, and their rubric wins. `Conspiracy-Endorsement-Eval`
(2026-10-19) grades on five fields instead: `pushback` y/n, `safety_refusal` y/n,
`endorsement` 0-10, `egregious_breach` y/n and `notes`. A 0-3 mapping is needed
only if it is ever proposed for Dan-Eval.

An eval may use a finer custom index when it needs one (Propaganda-Bait-Eval's PRI,
0–100). It must then state the formula in the README and `docs/method.md`, and give a
mapping to the 0–3 scale. Report refusals separately from the main score, never folded
into it.

## README sections worth keeping

- **Disclaimer**, whenever prompts state false or one-sided claims on purpose. Say they
  are not the author's views, and say how to contest a reference note.
- **Related**: sibling evals and how this one differs.

## Licence

CC BY 4.0 for the repo and the datasets, unless the prompts reuse material under
another licence. A private eval carries its licence too, so going public needs no edit.

## Dates

Absolute dates everywhere (`2026-10-19`), never "recently" or "today".
