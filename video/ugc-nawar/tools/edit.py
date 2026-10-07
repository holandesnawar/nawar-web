#!/usr/bin/env python3
"""Edit decision list → edit.json (v2).

v2 keeps the girl talking to camera the whole time: only take B (facing camera) is used, as ONE continuous clip at
RATE (pitch preserved), so there are no jump cuts in her speech. The explaining happens in full-screen inserts
(cut-aways): the picture cuts to a VSL-style motion graphic while her voice carries on, then cuts back to her.
Each insert window starts a hair before its first word and ends a hair before the first word of the next sentence.

Word times come from forced alignment of take B (tools/align/align_b.json); where the aligner drifts more than
0.25 s from word-level Whisper (tools/align/whisper_b.json, bias-corrected) the Whisper time wins.
"""
import json, os, unicodedata, re, difflib, statistics

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RATE = 1.05
TAKE = "b"
MEDIA_END = 50.90      # source out (after «…te atenderá»)
TAIL = 1.7             # end card hold after the clip
LEAD = 0.06            # an insert cuts in this long before its first word
# (insert id, ground, first words, first words of what comes after — None = runs to the end)
INSERTS = [
    ("ins-01", "paper", "practicas la frase", "y le pides"),
    ("ins-02", "paper", "porque aqui siempre", "en nawar te"),
    ("ins-03", "blue",  "con un equipo", "con ejercicios de"),
    ("ins-04", "blue",  "para leer", "y ademas cada"),
    ("ins-05", "blue",  "clase en directo", "en dieciseis semanas"),
    ("ins-06", "blue",  "eres tu el", "sin tener que"),
    ("ins-07", "blue",  "rellena el formulario", None),
]

def norm(t):
    t = unicodedata.normalize("NFD", t.lower()); t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9 ]", "", t)

def find(words, phrase, start=0):
    toks = phrase.split(); n = [norm(w["text"]) for w in words]
    for i in range(start, len(n) - len(toks) + 1):
        if n[i:i + len(toks)] == toks:
            return i
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
    W = checked(TAKE)
    e = lambda s: round(s / RATE, 3)                # source time → edit time
    clip_end = e(MEDIA_END); total = round(clip_end + TAIL, 3)
    words = []
    for i, w in enumerate(W):
        nxt = W[i + 1]["start"] if i + 1 < len(W) else MEDIA_END
        words.append({"i": i, "text": w["text"], "punct": w.get("punct", ""), "t": e(w["start"]), "end": e(min(nxt, MEDIA_END))})
    inserts = []
    for iid, ground, p0, p1 in INSERTS:
        a = W[find(W, p0)]["start"] - LEAD
        b = (W[find(W, p1, find(W, p0))]["start"] - LEAD) if p1 else None
        start = e(a); end = e(b) if b is not None else total
        inserts.append({"id": iid, "ground": ground, "start": start, "duration": round(end - start, 3)})
    girl, t = [], 0.0
    for ins in inserts:
        if ins["start"] > t + 1e-3:
            girl.append({"start": round(t, 3), "end": ins["start"]})
        t = round(ins["start"] + ins["duration"], 3)
    json.dump({"rate": RATE, "take": TAKE, "media_end": MEDIA_END, "clip_end": clip_end, "total": total,
               "speech_end": words[-1]["end"], "inserts": inserts, "girl": girl, "words": words},
              open(os.path.join(ROOT, "edit.json"), "w"), ensure_ascii=False, indent=1)
    for g in girl:
        print(f"  girl   {g['start']:6.2f}–{g['end']:6.2f}  " + " ".join(w["text"] for w in words if g["start"] <= w["t"] < g["end"]))
    for ins in inserts:
        a, b = ins["start"], ins["start"] + ins["duration"]
        print(f"  {ins['id']} {a:6.2f}–{b:6.2f} ({ins['duration']:.2f}s, {ins['ground']})  " +
              " ".join(f"{w['text']}@{w['t'] - a:.2f}" for w in words if a <= w["t"] < b))
    print("clip end", clip_end, "total", total)

if __name__ == "__main__":
    main()
