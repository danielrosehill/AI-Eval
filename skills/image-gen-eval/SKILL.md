---
name: image-gen-eval
description: Evaluate generative image models for a real job - model sourcing, per-image pricing, prompt set design, blind human grading, and where automated checks help or mislead. Use when the user says "evaluate image models", "which image model should I use", "compare image generators", "image eval", or "text-to-image benchmark". For a quick look at what's new, use informal-image-eval.
---

# Evaluate generative image models

Image evals differ from text in almost every step: pricing, storage, judging and comparison
are all handled differently, so `run-eval` doesn't apply directly. The objective and workload
steps do. Run `define-objective` and `define-workload-requirements` first.

## What's different

| | Text | Image |
|---|---|---|
| Price | Per token, returned as `usage.cost` | Per image or megapixel, varying by size and quality; often not returned at all |
| Hidden behaviour | Reasoning tokens | **Prompt expansion:** the model rewrites the prompt before drawing |
| Storage | JSONL | Binary files, kept out of git |
| Judging | LLM judge is usable | Humans first. A vision-model judge misses what matters most |
| Output count | Two per model is cheap | Every image has to be looked at, so the total is the real limit |

## Workload requirements to pin down

Text in the image (exact strings, language, script); style or photorealism; aspect ratio and
resolution; image-to-image or editing; brand or character consistency across images; volume and
target cost per image; licence for commercial use; the provider's content rules.

## Steps

1. **Find models.** Use two sources and compare:
   - **fal:** `GET https://api.fal.ai/v1/models?category=text-to-image`, with prices from
     `/v1/models/pricing`. See `informal-image-eval` step 1 for placeholder prices.
   - **OpenRouter:** `probe-openrouter`, then `filter` with `"output_modalities": ["image"]`.
     Prices there are per token, so cost per image has to be measured with one test call.

2. **Keep it wide, but count images.** The budget is **attention**, not only money. Default to
   about **20–40 images in total**, spending them on models: for example, 10–15 models × 1 prompt ×
   2 tries beats 4 models × 5 prompts × 2 tries. Add a prompt only if it tests a different
   requirement. Always include the incumbent.

3. **Write prompts that discriminate.** Use real briefs, each aimed at a requirement. Exact text
   strings, counted objects, and spatial relations ("the red cube left of the blue sphere") find
   differences where "a beautiful landscape" finds none.

4. **Equalise the settings.** Turn off prompt expansion wherever it exists (fetch each model's
   input schema), and use one aspect ratio and the quality tier production would use. Record
   any setting a model can't match.

5. **Get a yes on the estimate.** Show models, image count and cost, with where each price
   came from. Hard cap as in `run-eval`. Where responses carry no cost, meter from the listed
   prices and say that's an estimate.

6. **Run** with opaque shuffled ids, so grading can be blind. Save to `runs/<run_id>/images/`,
   ignored by git, with a `manifest.jsonl` of id, model, prompt, seed, cost and size. Reference
   implementation: `scripts/` in `danielrosehill/Tech-Graphics-Benchmark`. Check the
   files are real images (`file runs/<run_id>/images/*`) and open one.

7. **Grade by hand.** `setup-annotation-space`, with criteria from the requirements. Typical
   ones: prompt adherence, text accuracy, artefacts, usability as is.

8. **Use automated checks only where they're reliable.**
   - **Text rendering:** OCR against the expected string is objective, and worth doing.
   - **Hard failures:** blank images, refusals, wrong dimensions can all be scripted.
   - **Vision-model judge:** fine for pre-sorting a large set. Don't trust it on small text,
     hands or counting, and don't use it as the final grade.
   - **FID, CLIP score:** these measure distributions and caption similarity, not whether an image
     will do the job. Skip them unless the user is doing research.

9. **Report** tiers as in `run-eval`, with measured cost per usable image, meaning cost divided
   by the share of images that were usable. A cheap model needing four tries isn't cheap.

## Storage

Publish images to a `-Runs` dataset, not git. Check licence terms before making images public.
