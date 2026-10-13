#!/usr/bin/env python3
"""Edit decision list → edit.json (UGC #2, «Si tienes un ordenador…»).

Two takes of the same script: take 1 = UGC.POV1, facing camera (with two hook takes and a laptop), take 2 =
UGC.POV2, side angle (interview look: she talks to someone off camera — until the call to action, where she turns
to that camera, points and talks into it). The client wants her looking into the lens in every shot, so:
- the ad is cut from take 1, with a recomposed close-up of it as a second camera (camera B, tools/cam_b.py →
  take-1-b.mp4, same frames and sound) for «El principal error es pensar que necesitas» and «En Nawar practicas…»;
  the cut B → A on «…años o saber inglés primero» (in her pause, before a glance off to the side);
- the real change of angle is the CTA: take 1 up to «haz clic en el botón de aquí abajo,», then take 2, the side
  camera she now looks into, for «rellena el formulario» and (jump cut over her pause) «y una persona de nuestro
  equipo te atenderá», ending on her smile.
The first hook take is used (the second one stops for three seconds in the middle). Every cut sits in a quiet point
checked on the energy envelope (RMS < −40 dB), all at RATE (pitch preserved). The long pause before «¿Estás
listo…?» is removed at the cut back from the last insert, where the jump is hidden.

Word times: Whisper word timestamps of each take (tools/align/whisper_<take>.json), shifted by WHISPER_BIAS (its
onsets land ~0.15 s late on these takes, checked against the energy envelope at every cut).
"""
import json, os, unicodedata, re
from cam_b import face_on_screen

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RATE = 1.06
WHISPER_BIAS = -0.15
# (take, source in, source out, camera A|B) — hand-checked quiet points
SEGMENTS = [
    ("1", 0.55, 5.80, "A"),     # hook: «Si tienes un ordenador y ganas de aprender neerlandés, ya tienes todo lo que necesitas para empezar.»
    ("1", 15.30, 28.08, "A"),   # «En cuatro semanas…» + «Vivimos en un país… abrir puertas.»
    ("1", 28.08, 30.78, "B"),   # close-up: «El principal error es pensar que necesitas»
    ("1", 30.78, 37.90, "A"),   # «años o saber inglés primero. La realidad es que… más rápido de lo que crees.»
    ("1", 37.90, 43.92, "B"),   # close-up: «En Nawar practicas con situaciones… nada de la teoría que luego no usas.»
    ("1", 43.92, 66.56, "A"),   # «Aprendes con lecciones grabadas…» → «…como requisito el neerlandés.»
    ("1", 66.94, 70.56, "A"),   # «¿Estás listo para comenzar? Si es así, haz clic en el botón de aquí abajo,» (most of the pause before it removed;
                                #  no silence before «rellena» in this take: cut in the dip, a longer fade in gen.py)
    ("2", 70.84, 72.25, "A"),   # side camera, looking into it: «rellena el formulario»
    ("2", 74.50, 76.74, "A"),   # «y una persona de nuestro equipo te atenderá» + her smile (her 2 s pause cut)
]
FACE = {"1": (540, 720), "2": (510, 545)}   # face centre in each take (zoom origin); camera B: face_on_screen(FACE["1"])
SPEECH_END = 76.50     # «…atenderá» ends here in take 2; the shot runs on to her smile (76.74)
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
    for k, (tk, a, b, cam) in enumerate(SEGMENTS):
        W = AL[tk]; dur = round((b - a) / RATE, 3)
        shots.append({"n": k + 1, "take": tk, "cam": cam, "start": round(t, 3), "duration": dur, "media_start": a, "media_end": b,
                      "face": FACE[tk] if cam == "A" else face_on_screen(FACE[tk])})
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
        print(f"  shot {sh['n']} take {sh['take']} cam {sh['cam']}  {sh['start']:6.2f}–{sh['start'] + sh['duration']:6.2f}  (source {sh['media_start']}–{sh['media_end']})")
    for gg in girl:
        print(f"  girl   {gg['start']:6.2f}–{gg['end']:6.2f}  " + " ".join(w["text"] for w in words if gg["start"] <= w["t"] < gg["end"]))
    for ins in inserts:
        a0, b0 = ins["start"], ins["start"] + ins["duration"]
        print(f"  {ins['id']} {a0:6.2f}–{b0:6.2f} ({ins['duration']:.2f}s, {ins['ground']})  " +
              " ".join(f"{w['text']}@{w['t'] - a0:.2f}" for w in words if a0 <= w["t"] < b0))
    print("outro from", outro, "· clip end", clip_end, "· total", total, "· speech end", speech_end)


if __name__ == "__main__":
    main()
