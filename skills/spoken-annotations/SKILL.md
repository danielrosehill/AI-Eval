---
name: spoken-annotations
description: Annotate model outputs by voice instead of by hand - define the annotation structure, record spoken feedback per item in the browser, transcribe it, and have a model apply it to the structure (keeping the verbatim transcript and the recording as evidence). Fastest for audio judgements - TTS and voice clones, EQ or mix choices, noise removal - and any eval where clicking through a form is the slow part. Use when the user says "I'll just say it", "record my feedback", "voice annotations", "dictate the annotations", "annotation is too fiddly", or sets up human review of audio outputs.
---

# Spoken annotations

Daniel, 2026-11-18: annotation gets fiddly by hand, and nothing good existed for doing it by voice. The pattern has four
steps:

1. **Define the structure first.** Write down what an annotation consists of: the verdict, the reason categories,
   attributes (gender, ...), and the word- or span-level tag types with their fields. This is the same taxonomy a form
   would use (`screen-then-rank`, step 2). The model can only apply what the structure names, so write it before
   recording.
2. **Record per item.** Each output gets a voice note, recorded in the browser next to the player. The note is stored
   with the item it was about: the system and item for a screen note, or the item and both sides for a pairwise note.
   It uploads at once and needs no other click. The annotator speaks to the structure: "fail, wrong emphasis on the
   third word, it said sef-ER, should be SE-fer, female voice".
3. **Transcribe and apply.** Send the audio, together with the item's context (the text, any reference such as IPA and
   syllables, the allowed categories), to an audio-capable model. Ask in one call for a **verbatim transcript** plus the
   structured annotation as JSON. The context lets the model resolve "the third word" or "the ch sound" to concrete
   fields.
4. **Write with provenance.** Each derived annotation carries `source: "voice:<note id>"`. The transcript, the model and
   its output are kept beside the note. Annotations made by hand win: never overwrite a verdict saved by hand after the
   note was recorded, and log the conflict instead. Start with a dry run that prints each reading, then apply.

The recordings and transcripts are evidence. Publish them with the annotations when the eval is public, which is
Daniel's default for his own evaluations.

## Reference implementation

`danielrosehill/TTS-Pronunciation-Annotation-Starter` (2026-11-18):

- **Recording:** the 🎙 Voice note button, key R, in both passes.
- **Server:** `POST /api/voice/<eval_id>` stores `annotations/<eval_id>/voice/<id>.webm` plus a `voice.jsonl` line.
- **Apply:** `tools/apply_voice_notes.py --config config.json [--verbose] [--apply]`. It converts each note to 16 kHz
  MP3 and sends it to OpenRouter (`google/gemini-3.5-flash`, `input_audio`, temperature 0, JSON). It appends a
  `processed` line (transcript, structured output, usage) and screen rows with `source: "voice:<id>"`.
- **Checked:** a synthetic spoken note came back exactly right: verdict, reason, word position, syllable heard vs
  correct, and gender. It cost under US$0.01 per note.

For another kind of audio judgement, reuse the starter's server route and apply tool, and change the prompt's schema:

- **EQ, mixes, noise removal:** verdict, preferred variant, artefacts heard (hiss, pumping, muffled, sibilance) with
  their timestamps.
- **Voice clones:** likeness, accent drift, artefacts.

## Traps

- **The app keeps a cached copy of the annotation file.** Re-pull it from the dataset before every write, or the app's
  next save will overwrite the rows the apply step wrote.
- **Short or empty recordings:** drop notes under about half a second in the client.
- **Format:** browsers record WebM/Opus or MP4. Convert to MP3 or WAV before sending, as model audio inputs accept
  those reliably.
- **Ambiguity:** let the model return `null` for anything not said ("only record what the annotator said or clearly
  implied"), and report a `confidence` per note.
