---
name: setup-annotation-space
description: Set up a private Hugging Face Space for grading an eval's outputs by hand - blind to the model, with a rubric from the eval, saving to a private dataset and flowing back into the report. Works for text, image and audio. Use when the user says "set up an annotation space", "I want to grade these myself", "annotate the outputs", "put these in a space". For blind A/B use deploy-arena; for preference data to train on use setup-human-feedback-space.
---

# Set up an annotation Space

The eval-specific layer on top of a general annotation Space: what gets shown, what stays
hidden, and how the grades return to the eval.

**To build the Space,** use `data-annotation:hf-annotation-space` if it's available. Its
invariants, templates and traps apply in full. If it isn't, follow the invariants below and start
from `space/` in `danielrosehill/Tech-Graphics-Benchmark` for images. Read the overlay first
(`../../references/overlay.md`).

## Steps

1. **Requires a run** with outputs. Grading is rarely worth a Space for fewer than about 20: reading
   them in a document is quicker.

2. **Blind the outputs.**
   ```bash
   python3 scripts/blind_items.py rate --responses runs/<run_id>/responses.jsonl \
     --out runs/<run_id>/items.jsonl --key runs/<run_id>/key.json
   ```
   **`key.json` stays local.** It never goes in the Space or the dataset. The grader shouldn't
   learn the model until grading is done. Cost and output size may be shown if value for
   money is part of the question.

3. **Design the form from the eval,** not from a generic scale. Take the criteria from the
   ranked soft requirements in `requirements.json` or from the rubric, one control for each.
   Keep it short, because people grade badly on long forms. Add:
   - hard-failure tags drawn from the objective's failure wording,
   - an optional free-text note,
   - an optional process note, for a criterion the form lacks or something that couldn't be graded.

4. **Create the private artifacts.** Run `create` before any upload, as uploading to a missing id
   creates it public.
   ```bash
   hf repos create <owner>/<Name>-Eval-Ratings --repo-type dataset --private --exist-ok
   hf repos create <owner>/<Name>-Eval-Annotate --repo-type space --space-sdk gradio --private --exist-ok
   ```

5. **Build, test locally, deploy, verify.** Invariants:
   - Space and dataset private, with sign-in through `hf_oauth: true`, so the Space holds no token.
   - One file per decision (`reviews/<id>.json`), so reviewers never collide and re-grading overwrites.
   - Saving is queued and committed in the background. An HF commit takes about 30 seconds and the
     form mustn't wait for it.
   - Keyboard shortcuts, a skip that writes nothing, and a Browse tab.
   - Files fetched with `snapshot_download` need `demo.launch(allowed_paths=[HF_HUB_CACHE])`, or
     every image and audio item errors. Verify that a handler really returns a file.
   - Images: show JPEG previews, because multi-MB PNGs make grading crawl.

6. **Bring the grades back.** Pull the reviews to JSONL, then:
   ```bash
   python3 scripts/blind_items.py unblind --reviews reviews.jsonl \
     --key runs/<run_id>/key.json --out runs/<run_id>/ratings.jsonl
   ```
   Add per-model results to the report, keeping human grades apart from any LLM judge. Where
   both exist, list the disagreements, as they're the most informative rows.

7. **Document** the Space, dataset and pull step in the eval's README.

## Don't

- Don't commit `key.json`, or show model names on the form.
- Don't click the Hugging Face sign-in during verification. That's an OAuth grant, so it's the
  user's click. Their first saved grade is what proves sign-in works; say so until it arrives.
