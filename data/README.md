# Ground Truth Data

Reference material bundled with the plugin. Skills and agents in this plugin read from these files when suggesting frameworks, benchmarks, or eval patterns.

## Files

- `awesome-ai-evaluations-tools.md` — curated list of open-source eval tools, frameworks, benchmarks (platforms/software, benchmarks, agentic/tool use, multimodal, vision, RAG/retrieval, search). Mirror of [danielrosehill/Awesome-AI-Evaluations-Tools](https://github.com/danielrosehill/Awesome-AI-Evaluations-Tools).

## Refresh

This copy is a snapshot. To refresh:

```bash
curl -sSL https://raw.githubusercontent.com/danielrosehill/Awesome-AI-Evaluations-Tools/main/README.md \
  -o data/awesome-ai-evaluations-tools.md
```

## How the plugin uses this

When a skill or the `eval-engineer` agent is asked to recommend a framework or benchmark, it grounds the recommendation in this file before web search — so suggestions stay consistent with the user's curated canon. The user treats this as an authoritative shortlist; prefer entries here unless the task genuinely requires something not listed, and flag when you go off-list.
