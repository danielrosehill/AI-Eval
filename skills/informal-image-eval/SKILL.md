---
name: informal-image-eval
description: Informal micro-round of an image-generation eval on fal - refresh the list of current fal image models and prices, pick 3-5 cost-effective candidates, run one or two text-to-image prompts with two tries each (about 20 images, well under $1), and put the images in the eval's annotation Space for human grading. Use when the user says "informal image eval", "try a few image models", "test the newer image models", "draw up a model list", "a couple of generations on a few models", or for the periodic Tech-Graphics-Benchmark round. Not a full sweep; never all prompts x all models.
---

# Informal image eval

A quick look every few months at whether newer, cheaper image models now do the
job, not a scored benchmark. **Small by design:** 3–5 models × 1–2 prompts × 2 tries,
text-to-image unless the user asks for image-to-image. Roughly 20 images. The user
grades them by hand; there is no LLM judge.

Rejected on 2026-10-28: a 15-model panel × every prompt × 2 tries (168 images,
~$6.40). The user's words: "far too much... a couple of tries on a few different models,
save those so I can do annotations, that can be it". Don't scale a round up unasked.

**Reference implementation:** `danielrosehill/Tech-Graphics-Benchmark`: `scripts/fal_catalogue.py`,
`scripts/run_t2i.py`, `configs/<run_id>.json`, `panels/<YYYY-MM>.json`, and the
annotation Space in `space/`. For another eval, copy the two scripts and keep the run layout.

## 1. Refresh the model list (only when the longlist is stale)

If the newest `panels/*.json` is more than a couple of months old, or the user asks
"what's out there now":

```bash
uv run python scripts/fal_catalogue.py   # -> catalogue/fal-YYYY-MM-DD.jsonl
```

That's the fal Platform API: `GET https://api.fal.ai/v1/models?category=text-to-image`
(paged), then `GET /v1/models/pricing?endpoint_id=...`. Pricing returns 429 quickly;
the script backs off. Diff the snapshot against the previous one for new endpoints.

Prices: `unit` is `images`, `megapixels` (a 1024×768 image ≈ 0.79 MP) or a
**placeholder** (`unit_price` 1 with `units`/`credits`) for token-billed models: GPT
Image, Nano Banana Lite, MAI, Nano Banana 2.1. Read those off the model page,
`https://fal.ai/models/<endpoint_id>` (search the HTML for `pricingInfoOverride`).
Some API prices are also wrong in the other direction: Ideogram V4.5 shows 0.001
units but costs $0.008–0.22 per image by quality.

Write the longlist to `panels/<YYYY-MM>.json`: label, t2i and edit endpoints, USD per
1K image, and **where the price came from**. Target band: about $0.05 per image or
less (the user's "good and cheap enough to use repeatedly" point), plus the incumbent
above the band as the reference. Prefer models tagged `typography`, recent releases,
and one or two open-weights ones.

## 2. Pick the round

- **Models:** 3–5 from the longlist, spread across price tiers. Always include the
  current incumbent so there's a bar to beat.
- **Prompts:** 1–2, the core ones unless the user names others.
- **Tries:** 2 per model per prompt.
- **Inputs per model:** fetch the schema from
  `https://fal.ai/api/openapi/queue/openapi.json?endpoint_id=<id>`. Turn off
  `enable_prompt_expansion` wherever it exists, or the model rewrites the exact
  strings being tested. Use one aspect ratio for all models (`image_size:
  landscape_4_3`, or `aspect_ratio: "4:3"` for Nano Banana). Use the cheap quality tier the
  user would actually run (`quality: low` or `medium`), not max.

Write `configs/<run_id>.json` (`run_id` = `YYYY-MM-DD-informal`) with a `budget_usd`.
The spending limit is $5 per task; a round should come in under $1.

## 3. Run

```bash
uv run python scripts/run_t2i.py configs/<run_id>.json --dry-run
uv run python scripts/run_t2i.py configs/<run_id>.json
```

The harness is resumable, writes opaque shuffled `gen_id`s (keeping the Space blind),
and estimates spend from the config's prices, since fal responses carry no cost. Then check
the output directly: `file runs/<run_id>/images/*` shows real PNGs, and Read one image
to see that it rendered. Don't grade them; that's the user's job.

## 4. Save for annotation

```bash
hf upload <owner>/<Eval>-Runs runs/<run_id> <run_id> --repo-type dataset --exclude spend.json
```

Verify with `HfApi().list_repo_files` (the CLI can report "0 uploaded" on a successful
commit), then `HfApi().restart_space("<owner>/<Eval>-Annotate")` so the Space
picks the run up. Then call the Space's show handler with `gradio_client` and check that it returns an
image path. Gradio won't serve the HF hub cache without `allowed_paths` (see `deploy-arena`). Images stay out of git (`runs/*/images/` in `.gitignore`); the
manifest and config are committed.

## 5. Record and reply

Add a row to the README's Results table: run, models, prompts, image count, cost,
"awaiting annotation". Commit and push. Reply in a few lines: models, image count,
cost, the Space link. Once the annotations are in, a follow-up turns them into the
Results row and, if the index stage changed, calls `register-eval`.
