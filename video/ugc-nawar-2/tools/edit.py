#!/usr/bin/env python3
"""Edit decision list → edit.json (UGC #2, «Si tienes un ordenador…»).

Two takes of the same script: take 1 = UGC.POV1, facing camera (with two hook takes and a laptop), take 2 =
UGC.POV2, side angle (interview look, starts at «En cuatro semanas…»). Take 1 is clean end to end, so it carries
the ad; take 2 comes in for the two lines where it is the better read and the camera change helps the story:
«El principal error es pensar que necesitas años o saber inglés primero» (the myth, told to the side) and «En
Nawar practicas desde el primer día…» (with «desde el primer día», which take 1 doesn't say). The first hook take
is used (the second one stops for three seconds in the middle). Every cut sits in a quiet point checked on the
energy envelope (tools/align/…; RMS < −40 dB), all at RATE (pitch preserved). The long pause before «¿Estás listo…?»
is removed at the cut back from the last insert, where the jump is hidden.

Word times: Whisper word timestamps of each take (tools/align/whisper_<take>.json), shifted by WHISPER_BIAS (its
onsets land ~0.15 s late on these takes, checked against the energy envelope at every cut).
"""
import json, os, unicodedata, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RATE = 1.06
WHISPER_BIAS = -0.15
# (take, source in, source out) — hand-checked quiet points
SEGMENTS = [
    ("1", 0.55, 5.80),     # hook: «Si tienes un ordenador y ganas de aprender neerlandés, ya tienes todo lo que necesitas para empezar.»
    ("1", 15.30, 28.05),   # «En cuatro semanas…» + «Vivimos en un país… abrir puertas.»
    ("2", 16.92, 21.43),   # side: «El principal error es pensar que necesitas años o saber inglés primero»
    ("1", 32.58, 37.90),   # «La realidad es que… más rápido de lo que crees.»
    ("2", 29.85, 36.45),   # side: «En Nawar practicas desde el primer día… nada de teoría que luego no usas.»
    ("1", 43.92, 66.40),   # «Aprendes con lecciones grabadas…» → «…como requisito el neerlandés.»
    ("1", 66.98, 74.03),   # «¿Estás listo para comenzar? … te atenderá.» (pause before it removed)
]
FACE = {"1": (540, 720), "2": (480, 540)}   # face centre per take (zoom origin)
SPEECH_END = 73.92     # «…atenderá» ends here in take 1; the take ends on her smile at 74.03
TAIL = 1.4             # hold on her last frame under the «haz clic» button
LEAD = 0.06            # an insert cuts in this long before its first word (source seconds)
# (insert id, ground, first words, first words of what comes after)
INSERTS = [
    ("ins-01", "blue",  "ya puedes presentarte", "vivimos en un"),
    ("ins-02", "paper", "el ingles te saca", "el principal error"),
    ("ins-03", "blue",  "cuando te lo explican", "en nawar practicas"),
    ("ins-04", "blue",  "con situaciones que", "aprendes con lecciones"),
    ("ins-05", "blue",  "por un equipo", "para estudiar cuando"),
    ("ins-06", "blue",  "ejercicios pensados", "y cada semana"),
    ("ins-07", "blue",  "clase en directo", "ademas mientras las"),
    ("ins-08", "paper", "nueve de cada", "estas listo para"),
]
OUTRO = "haz clic en"  # the «haz clic» button pops under her face from here to the end (she stays on screen)

FIX = {"nerlandés,": "neerlandés,", "nerlandés": "neerlandés", "elnerlandés": "el neerlandés", "nirlandés.": "neerlandés.",
       "our": "Nawar", "NowHard": "Nawar", "colecciones": "con lecciones", "teoria": "teoría", "10": "diez", "9": "nueve",
       "ofertes": "ofertas", "nerlandes": "neerlandés"}


def norm(t):
    t = unicodedata.normalize("NFD", t.lower()); t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9 ]", "", t)


def words_of(take):
    """Whisper words of a take as [{text, punct, start}], misheard words fixed, glued words split."""
    out = []
    for a, b, t in json.load(open(os.path.join(ROOT, "tools", "align", f"whisper_{take}.json"))):
        t = t.strip(); m = re.match(r"^([¿¡]?)(.*?)([.,:;?!]*)$", t); pre, core, punct = m.group(1), m.group(2), m.group(3)
        fixed = FIX.get(core + punct, FIX.get(core, core)).rstrip(".,")
        parts = fixed.split(" ")
        for k, p in enumerate(parts):
            out.append({"text": (pre if k == 0 else "") + p, "punct": punct if k == len(parts) - 1 else "",
                        "start": round(a + WHISPER_BIAS + k * 0.12, 3)})
    return out


def main():
    AL = {t: words_of(t) for t in {sg[0] for sg in SEGMENTS}}
    shots, words, t = [], [], 0.0
    for k, (tk, a, b) in enumerate(SEGMENTS):
        W = AL[tk]; dur = round((b - a) / RATE, 3)
        shots.append({"n": k + 1, "take": tk, "start": round(t, 3), "duration": dur, "media_start": a, "media_end": b,
                      "face": FACE[tk]})
        inside = [i for i, w in enumerate(W) if a - 0.12 <= w["start"] < b - 0.06]
        for i in inside:
            w = W[i]; nxt = W[i + 1]["start"] if i + 1 < len(W) else b
            end = min(nxt, b, SPEECH_END if k == len(SEGMENTS) - 1 else b)
            words.append({"shot": k + 1, "text": w["text"], "punct": w["punct"],
                          "t": round(t + max(0.0, w["start"] - a) / RATE, 3), "end": round(t + (end - a) / RATE, 3)})
        t = round(t + dur, 3)
    clip_end = t; total = round(clip_end + TAIL, 3)
    last = shots[-1]; speech_end = round(last["start"] + (SPEECH_END - last["media_start"]) / RATE, 3)
    lead = LEAD / RATE
    def find_t(phrase, after=0.0):
        toks = phrase.split(); n = [norm(w["text"]) for w in words]
        for i in range(len(n) - len(toks) + 1):
            if words[i]["t"] >= after and n[i:i + len(toks)] == toks:
                return words[i]["t"]
        raise SystemExit(f"not found: {phrase}")
    inserts = []
    for iid, ground, p0, p1 in INSERTS:
        a0 = find_t(p0); start = round(a0 - lead, 3)
        end = round(find_t(p1, a0) - lead, 3) if p1 else total
        # an insert never outlives the shot boundary right after it: cut back on the boundary when they are close
        nxt = [s["start"] for s in shots if start < s["start"] <= end + 0.25]
        if nxt and abs(nxt[0] - end) <= 0.25:
            end = nxt[0]
        inserts.append({"id": iid, "ground": ground, "start": start, "duration": round(end - start, 3)})
    girl, g = [], 0.0
    for ins in inserts:
        if ins["start"] > g + 1e-3:
            girl.append({"start": round(g, 3), "end": ins["start"]})
        g = round(ins["start"] + ins["duration"], 3)
    girl.append({"start": g, "end": total})
    outro = round(find_t(OUTRO) - lead, 3)
    json.dump({"rate": RATE, "clip_end": clip_end, "total": total, "speech_end": speech_end, "outro": outro,
               "hold": {"start": clip_end, "duration": TAIL}, "shots": shots, "inserts": inserts, "girl": girl, "words": words},
              open(os.path.join(ROOT, "edit.json"), "w"), ensure_ascii=False, indent=1)
    for sh in shots:
        print(f"  shot {sh['n']} take {sh['take']}  {sh['start']:6.2f}–{sh['start'] + sh['duration']:6.2f}  (source {sh['media_start']}–{sh['media_end']})")
    for gg in girl:
        print(f"  girl   {gg['start']:6.2f}–{gg['end']:6.2f}  " + " ".join(w["text"] for w in words if gg["start"] <= w["t"] < gg["end"]))
    for ins in inserts:
        a0, b0 = ins["start"], ins["start"] + ins["duration"]
        print(f"  {ins['id']} {a0:6.2f}–{b0:6.2f} ({ins['duration']:.2f}s, {ins['ground']})  " +
              " ".join(f"{w['text']}@{w['t'] - a0:.2f}" for w in words if a0 <= w["t"] < b0))
    print("outro from", outro, "· clip end", clip_end, "· total", total, "· speech end", speech_end)


if __name__ == "__main__":
    main()
