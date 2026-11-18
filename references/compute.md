# Where eval work runs

Evals mix light work (API calls, scoring, small scripts) with heavy work (local models, GPU inference, audio or image
analysis over large sets). Heavy work does not belong on the user's laptop: it competes with everything else they are
doing, and an out-of-memory killer can take it down halfway with no output.

## Rule

| Work | Where |
|---|---|
| API calls, scoring text, small scripts, a pilot on a handful of items | Local |
| Anything that needs a GPU, loads a model, or needs more than ~1-2 GB of RAM | A cloud worker |
| Batch audio or image analysis over hundreds of files or more | A cloud worker, unless a small local probe has shown it stays light |

**Default cloud worker: [Modal](https://modal.com)**, if the user is authenticated there. Check before planning
around it: `modal profile current` (or `modal token info`) succeeds, or `~/.modal.toml` exists. A user may name a
wrapper or workspace in their overlay `conventions.md`; that wins. No Modal access: say so, and offer another hosted
route (a hosted API, a Hugging Face Space or Job, another machine) or ask before running heavy work locally.

## Before running anything locally that could grow

1. **Probe small:** one or two items, and print peak memory (`resource.getrusage(...).ru_maxrss`) and time per item.
2. **Cap it:** run under `ulimit -v <kB>` (e.g. 2-3 GB) so a runaway fails with an error instead of freezing the machine
   or being killed silently.
3. **Scale out, not up:** if items x time or memory is large, move it to Modal (one function per item or per batch,
   `.map()` over the inputs), with the inputs in a Modal Volume or fetched from Hugging Face.

## Seen in real runs

- 2026-11-18, TTS voice profiling (`scripts/voice_profile.py`): a Praat-based pass over ~600 clips was killed twice by
  `earlyoom` at 6.7 GB RSS on a laptop, with no output. Cause: streamed WAVs with a 0xFFFFFFFF data size made Praat
  allocate ~16 GB for one file. Fixed by decoding through ffmpeg; found by step 2 above (a capped scan per file). It
  should have been probed small and capped first, and sent to Modal when it grew.

## Modal sketch

```python
import modal
app = modal.App("eval-batch")
image = modal.Image.debian_slim().apt_install("ffmpeg").pip_install("praat-parselmouth", "numpy")

@app.function(image=image, memory=4096, timeout=600)
def measure(item: dict) -> dict:
    ...  # per-item work; return JSON-able results

@app.local_entrypoint()
def main():
    items = [...]  # small payloads or URLs; large inputs go in a modal.Volume
    results = list(measure.map(items))
```

Run with the user's own way of invoking Modal (overlay `conventions.md`), and state the expected cost first: the spend
rules in `conventions.md` apply to cloud compute as much as to API calls.
