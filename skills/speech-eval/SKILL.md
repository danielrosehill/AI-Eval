---
name: speech-eval
description: Evaluate speech models - speech-to-text with word error rate on the user's real audio, and text-to-speech with blind human listening. Use when the user says "evaluate ASR", "which transcription model", "WER", "test speech recognition", "compare TTS voices", or "which text-to-speech is best".
---

# Evaluate speech models

Speech differs from text in two ways. The test set has to be real audio, and OpenRouter's
catalogue is only a partial source, so check each provider's own model list as well.

## Speech to text

1. **Use the user's real audio:** their voice, microphone, room, accent and vocabulary. A public
   benchmark's score says little about a user's own recordings. 10–20 clips covering the hard
   conditions are enough to start.

2. **Write reference transcripts by hand,** or correct a machine draft closely. Errors in the
   reference count against every model.

3. **Normalise before scoring,** and record how: case, punctuation, numbers, and fillers. Without
   this, WER mostly measures formatting. Use the same normaliser for every model.

4. **Go wide:** many models, each clip once. ASR output varies little between runs, so
   repeats buy almost nothing. Run many clips instead.

5. **Score.** WER and CER with `jiwer`. CER suits languages without clear word boundaries or with
   rich morphology. WER treats every word alike, so also check the words that matter for the
   job, such as names and domain terms, and report those separately.

6. **Record** speed, price per audio hour, language, and whether it gives timestamps and
   speaker labels. **Read the worst clips.** Models can hallucinate fluent text over silence or
   noise, which a total score hides.

## Text to speech

No metric captures whether a voice is pleasant to hear, so listening decides.

1. **Use real scripts:** the same 2–3 passages per model, including the hard parts (names,
   numbers, abbreviations, other languages, long sentences).
2. **Go wide on models and voices,** two takes each. Takes vary in TTS, so the second take matters.
3. **Listen blind.** `deploy-arena` for A/B, or `setup-annotation-space` for rating on naturalness,
   pronunciation and pacing. Match loudness first, as louder clips tend to win.
4. **Script the objective checks:** transcribe the audio with an ASR model and compare it with
   the script. This catches dropped or invented words, and pronunciation failures.
5. **Record** cost per hour of audio, latency, and voice licensing, especially for voice clones.

## Storage

Audio stays out of git (`runs/*/audio/`). Publishing recordings of real voices needs the
speaker's consent, so keep those datasets private unless the user says otherwise.
