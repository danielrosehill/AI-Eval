---
name: probe-openrouter
description: Probe OpenRouter for the current state of its catalogue - snapshot every model with context, output limits, prices, modalities and parameters, list what's new, check the API key, inspect who serves a model, and confirm models actually answer. Use when the user says "what's on OpenRouter", "what's new on OpenRouter", "is this model on OpenRouter", "check OpenRouter", or before choosing candidates.
---

# Probe OpenRouter

Model names and prices in memory go stale within weeks. Everything downstream works from
a dated snapshot of the live catalogue, never from recall.

All commands are in `scripts/openrouter_catalogue.py` (`../../scripts/` from this skill;
standard library only, JSON on stdout). If that path doesn't resolve, clone
`danielrosehill/AI-Eval` and run it there.

## Free, no key needed

```bash
python3 scripts/openrouter_catalogue.py fetch --out selection/openrouter-catalogue-<YYYY-MM-DD>.json
python3 scripts/openrouter_catalogue.py new --catalogue <file> --days 14
python3 scripts/openrouter_catalogue.py endpoints <slug>
```

- `fetch` writes one normalised record per model: `id`, `lab`, `released`, `context`,
  `max_output`, modalities, `usd_per_m_in`, `usd_per_m_out`, `parameters`, reasoning
  support, `expires`.
- `new` lists recent releases, which is often the reason for running an eval at all.
- `endpoints` shows the providers behind one model, with quantization and uptime. Use it
  when quantization or provider matters. A model can be listed yet served only at fp4.

One snapshot per eval run is enough. Reuse a snapshot from the same day.

## Needs `OPENROUTER_API_KEY`

```bash
python3 scripts/openrouter_catalogue.py key
python3 scripts/openrouter_catalogue.py ping --candidates selection/candidates.json
python3 scripts/openrouter_catalogue.py ping <slug> <slug>
```

- `key` shows the key's limit and usage. A `null` limit means the key has no cap of its own.
- `ping` sends one 64-token call per model and reports status, the provider that served
  it, latency and cost. It's the only proof a model is callable for this account:
  listing doesn't cover account data policy, regional blocks or provider outages. Cost is
  a fraction of a cent per model, so pings need no approval.

## What the catalogue can't tell you

- Price is per token, so a model that thinks costs more than its listed price implies.
  Reasoning is on by default for many models (`reasoning_default`).
- `max_output: null` means the catalogue doesn't say. Treat it as unverified.
- `id`s ending `:free` and models at zero price are usually rate-limited and may log
  prompts. Stealth models change without notice. Neither suits a repeatable eval unless
  the user asks.
- Nothing here measures quality. That's what the eval is for.

## Report back

Date of the snapshot, model count, what's new, and key status. For a lookup about one
model, give its record rather than the summary.
