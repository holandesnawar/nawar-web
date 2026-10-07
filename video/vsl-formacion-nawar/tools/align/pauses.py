"""Pause structure + prosody metrics for each voice take."""
import sys, json
import numpy as np, librosa

def analyze(path):
    y, sr = librosa.load(path, sr=22000, mono=True)
    hop = 220  # 10 ms
    rms = librosa.feature.rms(y=y, frame_length=882, hop_length=hop)[0]
    db = librosa.amplitude_to_db(rms, ref=np.max)
    voiced = db > -40
    # pauses: runs of unvoiced >= 0.18 s
    pauses, start = [], None
    for i, v in enumerate(voiced):
        if not v and start is None:
            start = i
        if v and start is not None:
            if (i - start) * 0.01 >= 0.18:
                pauses.append((round(start * 0.01, 2), round(i * 0.01, 2)))
            start = None
    first = np.argmax(voiced) * 0.01
    last = (len(voiced) - np.argmax(voiced[::-1])) * 0.01
    f0, vflag, _ = librosa.pyin(y, fmin=70, fmax=400, sr=sr, hop_length=512)
    f0v = f0[~np.isnan(f0)]
    semis = 12 * np.log2(f0v / np.median(f0v))
    peak = float(np.max(np.abs(y)))
    clip = int(np.sum(np.abs(y) > 0.99))
    return {
        "file": path, "dur": round(len(y) / sr, 2), "speech_start": round(first, 2), "speech_end": round(last, 2),
        "n_pauses": len(pauses), "pause_total": round(sum(b - a for a, b in pauses), 2),
        "long_pauses": [p for p in pauses if p[1] - p[0] > 0.6],
        "f0_median": round(float(np.median(f0v)), 1), "pitch_range_semitones_p5_p95": round(float(np.percentile(semis, 95) - np.percentile(semis, 5)), 2),
        "pitch_std_semitones": round(float(np.std(semis)), 2), "peak": round(peak, 3), "clipped_samples": clip,
        "pauses": pauses,
    }

if __name__ == "__main__":
    out = [analyze(p) for p in sys.argv[1:]]
    for o in out:
        print(json.dumps({k: v for k, v in o.items() if k != "pauses"}, ensure_ascii=False))
    json.dump(out, open("pauses.json", "w"), indent=1)
