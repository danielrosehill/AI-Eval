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
6. **Measure what doesn't need ears:** an objective voice profile per voice, to help people pick by type next to the
   listening results. `scripts/voice_profile.py` (`--runs <dir>/<run>/<item>.wav --texts items.jsonl`) gives:
   - **Words per minute,** pooled: total source words / total seconds of speech (edge silence trimmed, pauses kept).
     Pool over passages, not single sentences: a six-word sentence reads at ~250 WPM with no pauses, a paragraph at
     ~130. A WPM far from the rest (<0.65x or >1.4x the median) is a flag for skipped, repeated or truncated text,
     not a pace.
   - **Pitch** (median F0 and register for the voice's gender), **intonation** (F0 spread in semitones),
     **brightness** (spectral centre of gravity, 500-8000 Hz) and **clarity** (harmonics-to-noise ratio).
     Track pitch in a per-gender range (male 60-250 Hz, female 100-450 Hz) to avoid octave errors. Label
     intonation, brightness and clarity relative to voices of the same gender: absolute cut-offs call most male
     voices "breathy" and most TTS "lively".
   - Decode audio with ffmpeg, not the analysis library's own reader: streamed WAV headers can claim billions of
     samples.
   It is CPU work, about a second per clip: fine locally for hundreds of clips after a capped probe; thousands go to a
   cloud worker (`../../references/compute.md`).
7. **Keep the listener's view of each voice apart from the measurements:** what it suits (audiobooks, podcasts,
   narration, learner reference, IVR...), what it doesn't, and a few descriptors in their words, one row per voice
   (`run, uses[], avoid[], character[], note`). Present both side by side; never infer a use the listener didn't state.

## Compute

Local ASR or TTS models, GPU inference and large batch analysis do not run on the user's laptop: see
`../../references/compute.md` (Modal by default when the user is authenticated there).

## Storage

Audio stays out of git (`runs/*/audio/`). Publishing recordings of real voices needs the
speaker's consent, so keep those datasets private unless the user says otherwise.
