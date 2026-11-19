# Grading an eval's outputs by hand in an annotation Space

The eval-specific layer. The Space itself (invariants, templates, blind grading, traps) is built by
`data-annotation:hf-annotation-space`; read its "Blind grading" section. Voice grading is
`data-annotation:spoken-annotations`. Read the overlay first (`references/overlay.md`).

Two-pass default: when the question is "which outputs are acceptable, and which acceptable one is best", use
`screen-then-rank`. This is one of its passes.

## Steps

1. **Requires a run** with outputs. Grading is rarely worth a Space for fewer than about 20: reading them in a document is quicker.
2. **Blind the outputs.**
   ```bash
   python3 scripts/blind_items.py rate --responses runs/<run_id>/responses.jsonl \
     --out runs/<run_id>/items.jsonl --key runs/<run_id>/key.json
   ```
   `key.json` stays local: never in the Space or the dataset. Cost and output size may be shown if value for money is part of the question.
3. **Design the form from the eval,** not from a generic scale: one control per ranked soft requirement in
   `requirements.json` (or per rubric criterion), kept short. Add hard-failure tags drawn from the objective's failure
   wording, an optional free-text note, and an optional process note.
4. **Build the Space** with `data-annotation:hf-annotation-space` (private Space and dataset, named `<Name>-Eval-Annotate`
   and `<Name>-Eval-Ratings`). For images, `space/` in `danielrosehill/Tech-Graphics-Benchmark` is a worked example.
   If the plugin isn't available, follow the invariants in that skill's documentation.
5. **Bring the grades back** (`data-annotation:pull-annotations`), then un-blind:
   ```bash
   python3 scripts/blind_items.py unblind --reviews reviews.jsonl \
     --key runs/<run_id>/key.json --out runs/<run_id>/ratings.jsonl
   ```
   Add per-model results to the report, keeping human grades apart from any LLM judge. Where both exist, list the disagreements.
6. **Document** the Space, dataset and pull step in the eval's README.

## Don't

- Don't commit `key.json`, or show model names on the form.
- Don't click the Hugging Face sign-in during verification: it's an OAuth grant, so it's the user's click.
