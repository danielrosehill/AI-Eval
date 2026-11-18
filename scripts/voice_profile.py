#!/usr/bin/env python3
"""Objective voice profile for TTS runs: speaking rate and an acoustic profile, with no listener judgement.
Helps people pick a voice by type (calm audiobook narrator vs bright, quick podcast host) next to the listening results.
Method from the Hebrew TTS bake-off (2026-11-18): https://github.com/danielrosehill/Hebrew-TTS-Bakeoff-1126

Layout read:
  <runs>/<run>/<item>.wav       one clip per item (any format ffmpeg reads; .wav, .mp3, .flac, .ogg are globbed)
  <runs>/<run>/meta.json        optional; "voice_gender": "male" | "female" sets the pitch range and label group
  <texts>                       JSONL with {"id": "<item>", "text": "<what the clip should say>"}

Per run, pooled over its clips:
  wpm               source words / seconds of speech x 60 (leading and trailing silence trimmed, internal pauses kept)
  wpm_by_clip
  f0_median_hz, f0_p10_hz, f0_p90_hz, f0_range_st (p90/p10 in semitones), f0_sd_st (spread around the median, semitones)
  centroid_hz       spectral centre of gravity of the 500-8000 Hz band (16 kHz resample): brightness
  hnr_db            harmonics-to-noise ratio: high = clean, low = breathy or rough
  labels            register (absolute per gender: male <110/<140 Hz, female <185/<225 Hz -> low/mid/high);
                    intonation, brightness, clarity as thirds among runs of the same gender (relative to this field);
                    pace vs the median wpm (slow < -10%, fast > +10%)
  flags             wpm below 0.65x or above 1.4x the median: almost always skipped, repeated or truncated text
Pitch is tracked in 60-250 Hz (male), 100-450 Hz (female), 60-400 Hz (unknown) to avoid octave errors.

Audio is decoded through ffmpeg, never Praat's own reader: streamed WAVs with a 0xFFFFFFFF data size (seen from Fish
Audio's API) make Praat allocate ~16 GB. Cost: about a second and ~200 MB per clip; hundreds of clips are fine locally,
thousands belong on a cloud worker (references/compute.md).

    uv run --with praat-parselmouth --with numpy python3 scripts/voice_profile.py --runs results --texts items.jsonl \
        --out voice_profiles.json [--gender run-a=male --gender run-b=female]
"""
import argparse, json, math, re, statistics, subprocess
from pathlib import Path

import numpy as np
import parselmouth

SR = 24000
PITCH_RANGE = {"male": (60, 250), "female": (100, 450)}
EXTS = (".wav", ".mp3", ".flac", ".ogg", ".m4a")


def words(text):
    return len([w for w in re.split(r"\s+", text) if re.search(r"\w", w)])


def decode(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).astype(np.float64)


def speech_seconds(x):
    """Duration minus leading and trailing silence: 20 ms frames below (peak - 35 dB, at least -60 dBFS)."""
    n = SR // 50
    frames = x[: len(x) // n * n].reshape(-1, n)
    if not len(frames):
        return len(x) / SR
    db = 20 * np.log10(np.sqrt((frames ** 2).mean(axis=1)) + 1e-12)
    voiced = np.where(db > max(db.max() - 35, -60))[0]
    return max(0.1, (voiced[-1] - voiced[0] + 1) * n / SR) if len(voiced) else len(x) / SR


def acoustics(x, gender):
    snd = parselmouth.Sound(x, sampling_frequency=SR)
    lo, hi = PITCH_RANGE.get(gender, (60, 400))
    f0 = snd.to_pitch_ac(time_step=0.01, pitch_floor=lo, pitch_ceiling=hi).selected_array["frequency"]
    band = parselmouth.praat.call(snd.resample(16000), "Filter (pass Hann band)", 500, 8000, 100)
    h = snd.to_harmonicity_cc(time_step=0.01, minimum_pitch=lo).values[0]
    h = h[h > -100]
    return f0[f0 > 0], band.to_spectrum().get_center_of_gravity(power=2.0), float(np.median(h)) if len(h) else None


def profile(folder, texts, gender):
    f0s, cents, hnrs, w_tot, s_tot, by_clip = [], [], [], 0, 0.0, {}
    for clip in sorted(p for p in folder.iterdir() if p.suffix.lower() in EXTS and p.stem in texts):
        x = decode(clip)
        f0, c, h = acoustics(x, gender)
        sp, n = speech_seconds(x), words(texts[clip.stem])
        f0s.append(f0); cents.append(c)
        if h is not None:
            hnrs.append(h)
        w_tot += n; s_tot += sp; by_clip[clip.stem] = round(60 * n / sp, 1)
    if not by_clip:
        return None
    p = {"wpm": round(60 * w_tot / s_tot, 1), "wpm_by_clip": by_clip, "voice_gender": gender, "flags": []}
    f0 = np.concatenate(f0s)
    if len(f0):
        med, p10, p90 = (float(np.percentile(f0, q)) for q in (50, 10, 90))
        p.update(f0_median_hz=round(med, 1), f0_p10_hz=round(p10, 1), f0_p90_hz=round(p90, 1),
                 f0_range_st=round(12 * math.log2(p90 / p10), 1), f0_sd_st=round(float(np.std(12 * np.log2(f0 / med))), 2))
    p["centroid_hz"] = round(statistics.mean(cents))
    p["hnr_db"] = round(statistics.mean(hnrs), 1) if hnrs else None
    return p


def label(out):
    med_wpm = statistics.median(p["wpm"] for p in out.values())
    for p in out.values():
        p["labels"] = {}
        g, f = p["voice_gender"], p.get("f0_median_hz")
        if f and g in ("male", "female"):
            lo, hi = (110, 140) if g == "male" else (185, 225)
            p["labels"]["register"] = "low" if f < lo else "high" if f >= hi else "mid"
    for key, (name, a_, b_, c_) in {"f0_sd_st": ("intonation", "flatter", "moderate", "livelier"),
                                    "centroid_hz": ("brightness", "darker", "neutral", "brighter"),
                                    "hnr_db": ("clarity", "breathier", "moderate", "cleaner")}.items():
        for g in {p["voice_gender"] for p in out.values()}:
            vs = sorted(p[key] for p in out.values() if p["voice_gender"] == g and p.get(key) is not None)
            if len(vs) < 3:
                continue
            lo, hi = vs[len(vs) // 3], vs[2 * len(vs) // 3]
            for p in out.values():
                if p["voice_gender"] == g and p.get(key) is not None:
                    p["labels"][name] = a_ if p[key] < lo else c_ if p[key] >= hi else b_
    for p in out.values():
        r = p["wpm"] / med_wpm - 1
        p["labels"]["pace"] = "slow" if r < -0.1 else "fast" if r > 0.1 else "average"
        p["pace_vs_median"] = round(r, 2)
        if not 0.65 <= p["wpm"] / med_wpm <= 1.4:
            p["flags"].append("pace far outside the other voices: check for skipped, repeated or truncated text")
        if not p["flags"]:
            del p["flags"]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--runs", required=True, type=Path)
    ap.add_argument("--texts", required=True, type=Path)
    ap.add_argument("--out", default="voice_profiles.json", type=Path)
    ap.add_argument("--gender", action="append", default=[], help="run=male|female (overrides meta.json)")
    a = ap.parse_args()
    texts = {r["id"]: r["text"] for r in map(json.loads, a.texts.read_text().splitlines()) if r.get("text")}
    given = dict(g.split("=", 1) for g in a.gender)
    out = {}
    for folder in sorted(d for d in a.runs.iterdir() if d.is_dir()):
        meta = json.loads((folder / "meta.json").read_text()) if (folder / "meta.json").exists() else {}
        p = profile(folder, texts, given.get(folder.name) or meta.get("voice_gender"))
        if p:
            out[folder.name] = p
    if not out:
        raise SystemExit("no clips matched: expected <runs>/<run>/<item id>.wav with ids from --texts")
    label(out)
    a.out.write_text(json.dumps(out, ensure_ascii=False, indent=1))
    for run, p in out.items():
        print(f"{run:36} {p['wpm']:6.1f} wpm  f0 {p.get('f0_median_hz', 0):6.1f} Hz  {' / '.join(p['labels'].values())}"
              + ("  ⚠" if p.get("flags") else ""))


if __name__ == "__main__":
    main()
