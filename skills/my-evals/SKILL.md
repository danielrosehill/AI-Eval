---
name: my-evals
description: The user's own index of evals they run (TTS, ASR, image, LLM, RAG, agent, security...), kept privately in the ai-eval overlay as evals.json. Resolves a loose reference ("the Hebrew TTS eval", "the bake-off", "my image eval") to its repos, datasets, Spaces, leaderboard and eval-specific skills, so the user never has to re-explain which eval they mean. Use whenever the user mentions one of their evals by name or nickname, asks "what evals do I have", "add this eval to my index", "where does X live", or starts work that may continue an existing eval; start-eval calls it first.
---

# My evals: the index of the user's own evals

The plugin is public and generic; the user's evals are not all public. Two layers, both named in the private overlay
directory (`../../references/overlay.md`):

- **The list of evals** is the user's own registry, if they keep one: `evals.json` → `sources` names it (e.g. a public
  `benchmarks.json` with `id`, `name`, `category`, `stage`, `repo`, `dataset`, `space`). Read it from the local clone
  (`git pull` first) or its raw URL. Never duplicate public facts from it.
- **Private extras** in `<overlay>/evals.json` → `evals`, keyed by the registry `id`: nicknames, local paths, private
  repos and Spaces, the eval's own skills, records. An eval with nothing private needs no entry here.
No registry named: `evals.json` → `evals` is the whole index (full entries, schema below).

## Resolve (the common case)

1. Read the sources and the private extras. Match the user's words against `id`, `name`/`title`, `aliases` and repo
   names (case-insensitive, partial match fine). One clear match: use it without asking. Several: ask once, naming
   them. None: say so, and offer `register-eval` (public) or an extras entry (private), or `start-eval` if it is not an
   eval yet.
2. Load the eval's context **before acting**:
   - the local clone of each repo (registry `repo` plus extras `repos`; find a clone by repo name under the user's
     repos folder) and its `CLAUDE.md` and `README.md`;
   - its eval-specific skills: every `SKILL.md` under the extras' `skills` paths, and any `<repo>/.claude/skills/*/`.
     Prefer one of them over a generic ai-eval skill when it matches the task: it carries what this eval has learned;
   - its log or decisions file if the extras name one.
3. Work from there. If something is stale (a path moved, a new Space, a new skill), fix it where it lives: public
   facts in the registry (`register-eval`), private ones in `evals.json`.

## Add or update an entry

Write JSON (agent-first: explicit paths, IDs, URLs, absolute dates). With a registry, an extras entry holds only `id`,
`aliases` and the private fields (`repos` that are private or local-only, `hf` private items, `skills`, `records`,
`updated`). Without one, the full schema, one object per eval in `evals`:

```json
{
  "id": "hebrew-tts-bakeoff-1126",
  "title": "Hebrew TTS Bake-off 11/26",
  "aliases": ["hebrew tts eval", "the bake-off", "tts bakeoff"],
  "domain": "tts",
  "status": "active",
  "started": "2026-11-18",
  "question": "One sentence: what the eval decides.",
  "method": "e.g. screen-then-rank, spoken annotations",
  "repos": [{"role": "code and results", "path": "~/repos/...", "github": "owner/name", "visibility": "public"}],
  "hf": {"datasets": ["owner/name"], "spaces": ["owner/name"]},
  "leaderboard": "https://...",
  "skills": ["~/repos/.../.claude/skills"],
  "records": {"log": "<repo>/docs/log.md", "decisions": "hf:owner/dataset/annotations/<id>/decisions.jsonl"},
  "updated": "YYYY-MM-DD"
}
```

`domain` is one of: `tts`, `asr`, `image`, `video`, `llm`, `rag`, `agent`, `security`, `other` (add a new one only if
none fits). `status`: `planned`, `active`, `paused`, `done`. Keep `aliases` to what the user actually calls it; add a
nickname the moment they use one.

## List

From the registry plus extras: group by domain/category, then status/stage, with title, one-line question and leaderboard link. Machine-readable on request.

## Rules

- `evals.json` is private (it names private repos and Spaces). Never copy it into a public repo; a public index of
  published evals is `register-eval`'s job.
- An eval-specific skill belongs in the eval's own repo (private if the repo is), not in this plugin: `eval-skill`.
