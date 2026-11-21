"""Forced alignment of a known script to a voice take, aeneas-style.

1. Synthesize the script with espeak-ng (Spanish) and record word events
   (text offset + audio position) from the synth callback.
2. MFCC both signals and DTW-align them.
3. Map each espeak word start/end through the DTW path into the real audio,
   then snap word starts to nearby energy onsets.

Usage: python3 align.py narration.txt voice.mp3 out.json [--rate 175]
"""
import ctypes, json, re, sys, os, unicodedata
import numpy as np, librosa
import espeakng_loader

SR = 22000  # hop 220 == exactly 10 ms

class EspeakEvent(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_int),
        ("unique_identifier", ctypes.c_uint),
        ("text_position", ctypes.c_int),
        ("length", ctypes.c_int),
        ("audio_position", ctypes.c_int),
        ("sample", ctypes.c_int),
        ("user_data", ctypes.c_void_p),
        ("id", ctypes.c_char * 8),
    ]

def synth(text, rate):
    lib = ctypes.CDLL(espeakng_loader.get_library_path())
    data = espeakng_loader.get_data_path()
    lib.espeak_Initialize.restype = ctypes.c_int
    sr = lib.espeak_Initialize(2, 0, os.path.dirname(data).encode(), 0)  # AUDIO_OUTPUT_SYNCHRONOUS
    if sr <= 0:
        raise SystemExit("espeak init failed")
    lib.espeak_SetVoiceByName(b"es")
    lib.espeak_SetParameter(1, rate, 0)  # espeakRATE
    chunks, events = [], []
    CB = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.POINTER(ctypes.c_short), ctypes.c_int, ctypes.POINTER(EspeakEvent))

    def cb(wav, n, ev):
        if n > 0:
            chunks.append(np.ctypeslib.as_array(wav, shape=(n,)).copy())
        i = 0
        while ev[i].type != 0:
            e = ev[i]
            if e.type == 1:  # WORD
                events.append((e.text_position, e.length, e.audio_position / 1000.0))
            i += 1
        return 0

    cbf = CB(cb)
    lib.espeak_SetSynthCallback(cbf)
    b = text.encode("utf-8")
    lib.espeak_Synth(ctypes.c_char_p(b), len(b) + 1, 0, 1, 0, 1, None, None)  # POS_CHARACTER, espeakCHARS_UTF8
    lib.espeak_Synchronize()
    audio = np.concatenate(chunks).astype(np.float32) / 32768.0
    return audio, sr, events

def words_with_offsets(text):
    # character offsets (1-based, in characters not bytes) of each word token
    out = []
    for m in re.finditer(r"[\wÀ-ÿ'’]+", text):
        out.append({"text": m.group(0), "char": m.start() + 1})
    return out

def feats(y, sr, hop_s):
    hop = int(sr * hop_s)
    m = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=14, n_fft=1024, hop_length=hop)[1:]
    m = (m - m.mean(axis=1, keepdims=True)) / (m.std(axis=1, keepdims=True) + 1e-6)
    return m

def main():
    txt_path, wav_path, out_path = sys.argv[1:4]
    rate = int(sys.argv[sys.argv.index("--rate") + 1]) if "--rate" in sys.argv else 175
    text = open(txt_path, encoding="utf-8").read().strip().replace("\n", " ")
    syn, ssr, ev = synth(text, rate)
    syn = librosa.resample(syn, orig_sr=ssr, target_sr=SR)
    real, _ = librosa.load(wav_path, sr=SR, mono=True)
    hop_s = 0.02
    A, B = feats(syn, SR, hop_s), feats(real, SR, hop_s)
    D, wp = librosa.sequence.dtw(X=A, Y=B, metric="euclidean", backtrack=True)
    wp = wp[::-1]
    cost = D[-1, -1] / len(wp)
    # map synthetic time -> real time (take median real index per synthetic index)
    syn_to_real = {}
    for i, j in wp:
        syn_to_real.setdefault(i, []).append(j)
    nA = A.shape[1]
    mapping = np.array([np.median(syn_to_real.get(i, [np.nan])) for i in range(nA)])
    idx = np.arange(nA)
    ok = ~np.isnan(mapping)
    mapping = np.interp(idx, idx[ok], mapping[ok])
    def s2r(t):
        k = min(int(round(t / hop_s)), nA - 1)
        return float(mapping[k] * hop_s)

    words = words_with_offsets(text)
    # match espeak word events to tokens by char offset (espeak positions are 1-based char offsets)
    ev_sorted = sorted(ev, key=lambda e: e[0])
    starts_syn = []
    for w in words:
        cand = [e for e in ev_sorted if e[0] <= w["char"] + 1]
        starts_syn.append(cand[-1][2] if cand else 0.0)
    # local DTW path quality per word (cost along path segment)
    path_cost = np.array([np.linalg.norm(A[:, i] - B[:, j]) for i, j in wp])
    syn_dur = len(syn) / SR
    res = []
    for k, w in enumerate(words):
        s_syn = starts_syn[k]
        e_syn = starts_syn[k + 1] if k + 1 < len(words) else syn_dur
        s = s2r(s_syn)
        e = s2r(max(e_syn - 0.03, s_syn + 0.05))
        i0, i1 = int(s_syn / hop_s), int(e_syn / hop_s)
        sel = (wp[:, 0] >= i0) & (wp[:, 0] <= i1)
        lc = float(path_cost[sel].mean()) if sel.any() else None
        res.append({"text": w["text"], "start": round(s, 3), "end": round(max(e, s + 0.05), 3), "local_cost": round(lc, 3) if lc else None})
    # snap starts to energy onsets within +-80ms
    rms = librosa.feature.rms(y=real, frame_length=882, hop_length=220)[0]
    db = librosa.amplitude_to_db(rms, ref=np.max)
    for r in res:
        k0 = int(r["start"] / 0.01)
        lo, hi = max(k0 - 8, 1), min(k0 + 8, len(db) - 1)
        seg = db[lo:hi]
        if len(seg) > 2 and seg.min() < -35:  # starts after a silence: snap to rise
            rise = [k for k in range(lo, hi) if db[k - 1] < -35 <= db[k]]
            if rise:
                r["start"] = round(min(rise, key=lambda k: abs(k - k0)) * 0.01, 3)
    json.dump({"voice": wav_path, "dtw_cost": round(float(cost), 4), "duration": round(len(real) / SR, 3), "words": res}, open(out_path, "w"), ensure_ascii=False, indent=1)
    lc = np.array([r["local_cost"] or 0 for r in res])
    worst = sorted(range(len(res)), key=lambda k: -lc[k])[:8]
    print(f"{wav_path}: dtw_cost={cost:.4f} words={len(res)} syn_dur={syn_dur:.1f}s real={len(real)/SR:.1f}s")
    print("  highest local cost:", [(res[k]['text'], res[k]['start'], res[k]['local_cost']) for k in sorted(worst)])

if __name__ == "__main__":
    main()
