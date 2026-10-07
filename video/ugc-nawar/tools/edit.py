#!/usr/bin/env python3
"""Edit decision list → edit.json (shots on the timeline + every word at its edit time).

Two separate takes of the same script: A = side angle (interview look), B = facing camera. The edit alternates
them sentence by sentence (B carries the hook and the CTA), each cut sitting in the quietest point between two
words (checked against the energy envelope), and plays everything at RATE (pitch preserved) for a tighter pace.
Word times come from forced alignment of each take (tools/align/align_<take>.json); where the aligner drifts more
than 0.25 s from word-level Whisper (tools/align/whisper_<take>.json, bias-corrected) the Whisper time wins.
"""
import json, os, unicodedata, re, difflib, statistics

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RATE = 1.05
TAIL = 1.1            # hold after the last word (the CTA end card)
# (take, source in, source out, first words, last words) — in/out are the hand-checked quiet points
EDL = [
    ("b", 0.00, 4.05, "si vives en", "escucha esto"),
    ("b", 4.05, 8.80, "seguro que te", "te bloqueas"),
    ("a", 5.30, 10.40, "y le pides", "sin pensarlo"),
    ("b", 13.10, 17.72, "eso no se", "cambia al ingles"),
    ("a", 15.07, 20.14, "en nawar te", "tu idioma"),
    ("b", 22.66, 25.58, "cuentas con lecciones", "tu puedas"),
    ("a", 23.40, 28.95, "con ejercicios de", "simple test"),
    ("b", 31.09, 37.90, "y ademas cada", "la pronunciacion"),
    ("a", 35.68, 42.24, "en dieciseis semanas", "a nadie"),
    ("b", 43.30, 50.90, "estas listo para", "te atendera"),
]

def norm(t):
    t = unicodedata.normalize("NFD", t.lower()); t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9 ]", "", t)

def find(words, phrase, start=0, last=False):
    toks = phrase.split(); n = [norm(w["text"]) for w in words]
    for i in range(start, len(n) - len(toks) + 1):
        if n[i:i + len(toks)] == toks:
            return i + len(toks) - 1 if last else i
    raise SystemExit(f"not found: {phrase}")

def checked(take):
    W = json.load(open(os.path.join(ROOT, "tools", "align", f"align_{take}.json")))["words"]
    H = json.load(open(os.path.join(ROOT, "tools", "align", f"whisper_{take}.json")))
    sm = difflib.SequenceMatcher(a=[norm(w["text"]).replace(" ", "") for w in W], b=[norm(h[2]).replace(" ", "") for h in H], autojunk=False)
    pairs = [(m.a + k, m.b + k) for m in sm.get_matching_blocks() for k in range(m.size)]
    bias = statistics.median(W[i]["start"] - H[j][0] for i, j in pairs)
    fixed = 0
    for i, j in pairs:
        wt = H[j][0] + bias
        if abs(W[i]["start"] - wt) > 0.25:
            W[i] = dict(W[i], start=round(wt, 3)); fixed += 1
    for k in range(1, len(W)):                      # keep the order monotonic
        if W[k]["start"] <= W[k - 1]["start"]:
            W[k] = dict(W[k], start=round(W[k - 1]["start"] + 0.04, 3))
    print(f"take {take}: {fixed} word(s) moved to Whisper timing (bias {bias:+.3f})")
    return W

def main():
    AL = {t: checked(t) for t in "ab"}
    shots, words, t = [], [], 0.0
    for k, (take, a, b, p0, p1) in enumerate(EDL):
        W = AL[take]; i0 = find(W, p0); i1 = find(W, p1, i0, last=True)
        dur = round((b - a) / RATE, 3)
        shots.append({"n": k + 1, "take": take, "start": round(t, 3), "duration": dur, "media_start": a, "media_end": b})
        for i in range(i0, i1 + 1):
            w = W[i]; nxt = W[i + 1]["start"] if i < i1 else b
            words.append({"shot": k + 1, "text": w["text"], "punct": w.get("punct", ""),
                          "t": round(t + (w["start"] - a) / RATE, 3), "end": round(t + (min(nxt, b) - a) / RATE, 3)})
        t += dur
    total = round(t + TAIL, 3)
    json.dump({"rate": RATE, "total": total, "speech_end": round(t, 3), "shots": shots, "words": words},
              open(os.path.join(ROOT, "edit.json"), "w"), ensure_ascii=False, indent=1)
    for s in shots:
        ws = [w for w in words if w["shot"] == s["n"]]
        print(f"shot {s['n']:2d} {s['take']} {s['start']:6.2f}–{s['start'] + s['duration']:6.2f}  " +
              " ".join(f"{w['text']}@{w['t']:.2f}" for w in ws))
    print("total", total)

if __name__ == "__main__":
    main()
