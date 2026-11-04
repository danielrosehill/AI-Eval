---
name: shortlist-candidates
description: Draw up the list of candidate models for an eval from the OpenRouter catalogue - filter on the workload's hard requirements, then pick a wide, varied field with a reason for each. Use when the user says "which models should I test", "draw up candidates", "build the model list", or after define-workload-requirements.
---

# Shortlist candidates

Turns the catalogue into `selection/candidates.json`, the panel `run-eval` runs.

Needs `selection/requirements.json` (run `define-workload-requirements` if it's missing)
and a catalogue snapshot from today (`probe-openrouter`).

## Steps

1. **Filter on hard requirements.**
   ```bash
   python3 scripts/openrouter_catalogue.py filter --catalogue <snapshot> \
     --requirements selection/requirements.json --out selection/filtered.json
   ```
   Read the `dropped` counts. If a filter dropped nearly everything, a requirement is
   probably too tight: say so instead of quietly loosening it.

2. **Pick wide.** The default field is **12–20 models**. The point of a wide field is to
   be surprised, so favour variety over the expected leaders:
   - Spread across labs and countries of origin, and across open and closed weights.
   - Spread across price: a few at the top of the budget, several mid-range, a few cheap
     ones that might do the job at a fraction of the cost.
   - Include new releases and lesser-known labs. A model with no public scores isn't
     disqualified. It's what an eval can find out that a leaderboard can't.
   - Include the incumbent, if there is one and the user wants the comparison.

3. **Cut what can't add information.**
   - Older generations of a family when the newest is callable and no dearer.
   - Near-duplicates: the same model under variant suffixes or a rebrand. Keep one.
   - Lines built for something else, such as code-only, OCR, retrieval or extraction models,
     unless the workload is that. Price-sorted lists fill up with these.
   - Anything the workload's `irrelevant` list suggests was only there on reputation.

4. **Use public evidence as a tiebreak, not a filter.** Where a soft requirement has a
   relevant public board, use it to choose between otherwise similar models. Don't use
   general intelligence rankings.

5. **Choose the judge,** if one is needed: capable, cheap, not in the panel, and ideally
   from a lab that isn't heavily represented in it.

6. **Write `selection/candidates.json`:**
   ```json
   {
     "date": "YYYY-MM-DD",
     "catalogue": "selection/openrouter-catalogue-YYYY-MM-DD.json",
     "requirements": "selection/requirements.json",
     "candidates": [
       {"id": "lab/model", "why": "One line tied to the workload", "reasoning": "off"}
     ],
     "considered_and_cut": [{"id": "lab/model", "reason": "Older generation of X"}],
     "judge": "lab/model"
   }
   ```

7. **Ping and price.**
   ```bash
   python3 scripts/openrouter_catalogue.py ping --candidates selection/candidates.json
   python3 scripts/openrouter_catalogue.py estimate --catalogue <snapshot> \
     --requirements selection/requirements.json --candidates selection/candidates.json \
     --judge <slug> --cap 5
   ```
   Move any model that fails its ping to `considered_and_cut` with the error, and replace
   it if the field has got thin. Over budget, drop models from the expensive end. Keep the
   field wide and the outputs per model as they are.

## Report back

A table of candidates (model, lab, cost per output, why), what was cut and why, the judge,
and the estimated total. Stop here: `run-eval` spends money and needs its own go-ahead.
