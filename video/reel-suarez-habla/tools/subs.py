#!/usr/bin/env python3
"""The subtitles: what is said, phrase by phrase (Dutch as said, Spanish under it), timed word by word from ElevenLabs
Scribe's transcript of the interview (.raw/scribe.json; checked against a second pass, .raw/scribe_v1.json). Suárez's
broken Dutch is kept as he says it («Wij echt blij», «Voor mij maakt niet uit», «Trainer weet»); only the «uh»s and
the stutters («Ik-ik», «is-is», «in, in vier», «op, op tien», «Ben je, ben je») are left out. «r» is the reporter (off screen: a small label says so).
  python3 tools/subs.py      → subs.json (reel times)
"""
import difflib, json, os, re, sys, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from frame import SEGMENTS, FPS  # noqa: E402

# (who, Dutch, Spanish): r = the reporter, s = Suárez
PHRASES = [
    ("r", "Het was spannend.", "Fue emocionante."),
    ("s", "Wie?", "¿Quién?"),
    ("r", "De wedstrijd was|spannend, denk ik.", "El partido fue emocionante, creo."),
    ("s", "Ja, klein beetje.", "Sí, un poquito."),
    ("r", "Feestje gevierd?", "¿Hubo fiestecita?"),
    ("s", "Sorry?", "¿Perdón?"),
    ("r", "Feest.|Feestje gevierd?", "Fiesta. ¿Hubo fiestecita?"),
    ("s", "Ah, nee, nee,|nee, nee.", "Ah, no, no, no, no."),
    ("s", "Wij echt blij.|Echt tevreden.", "Muy contentos. Muy satisfechos."),
    ("s", "Maar nu is klaar", "Pero ya se acabó"),
    ("s", "omdat wij hebben|volgende wedstrijd", "porque tenemos el próximo partido"),
    ("s", "in vier… in|achtenveertig uur.", "en cuatro…|en cuarenta y ocho horas."),
    ("r", "Ben je blij dat je|in de spits staat?", "¿Contento de jugar de delantero?"),
    ("s", "Ja, voor mij|maakt niet uit.", "Sí, a mí me da igual."),
    ("s", "Ik wil spelen|links, rechts,", "Quiero jugar por la izquierda,|por la derecha,"),
    ("s", "in de spits,|op tien ook.", "de delantero, de diez también."),
    ("s", "Voor mij|maakt niet uit.", "A mí me da igual."),
    ("s", "Ik wil spelen.|Trainer weet.", "Quiero jugar. El entrenador sabrá."),
    ("r", "Je hebt geen|liefste positie?", "¿No tienes una posición favorita?"),
    ("r", "De positie waar je…", "La posición en la que…"),
    ("r", "…het graagst|op speelt.", "…más te gusta jugar."),
    ("s", "Nee, nee, nee, nee.", "No, no, no, no."),
    ("s", "Voor mij|geen probleem.", "Por mí, no hay problema."),
    ("s", "Geen probleem.", "Ningún problema."),
    ("s", "Ik wil alleen|maar spelen.", "Yo solo quiero jugar."),
]
SKIP = {"uh"}
# times set by ear and by the waveform where Scribe is off (reel seconds): (phrase, word, the word, start, end)
FIX = [(5, 0, "Sorry?", 7.48, 8.02),                                       # (the drawn-out «Sss…» is heard from 7.48)
       (7, 1, "nee,", 10.56, 10.86), (7, 2, "nee,", 11.20, 11.66), (7, 3, "nee,", 11.72, 11.90), (7, 4, "nee.", 11.96, 12.22),
       (11, 2, "in", 19.57, 19.70), (11, 3, "achtenveertig", 19.72, 20.58),   # Scribe: «negen en veertig»; he says
                                                                           # «in achtenveertig» (48: [a], [x], 2 syllables)
       (15, 3, "op", 28.21, 28.46),                                         # «op, op tien»: the first «op» counts
       (17, 0, "Ik", 30.58, 30.84),                                         # «Ik, ik wil spelen» (Scribe: «Ik-ik» at 30.94)
       (19, 2, "waar", 35.46, 35.56), (19, 3, "je…", 35.58, 35.86)]       # «waar je het, waar je het graagst»


def norm(w):
    w = unicodedata.normalize("NFD", w.lower())
    return re.sub(r"[^a-z0-9]", "", "".join(c for c in w if unicodedata.category(c) != "Mn"))


def reel_time(t):
    """source time → reel time (None outside the moments used)."""
    r0 = 0.0
    for a, b in SEGMENTS:
        if a / FPS - 0.05 <= t <= (b + 1) / FPS + 0.05:
            return r0 + t - a / FPS
        r0 += (b - a + 1) / FPS
    return None


def main():
    sc = []
    for w in json.load(open(os.path.join(ROOT, ".raw", "scribe.json")))["words"]:
        if w.get("type") != "word" or norm(w["text"]) in SKIP:
            continue
        t0, t1 = reel_time(w["start"]), reel_time(w["end"])
        if t0 is None or t1 is None:
            continue
        for part in re.split(r"(?<=\w)-(?=\w)", w["text"]):          # «Ik-ik» → «Ik» «ik» (stutters)
            sc.append({"text": part, "start": t0, "end": t1})
    A = [(p, w) for p, (_, nl, _) in enumerate(PHRASES) for w in nl.replace("|", " ").split()]
    a, b = [norm(w) for _, w in A], [norm(w["text"]) for w in sc]
    times = [None] * len(A)
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1):
                times[i1 + k] = (sc[j1 + k]["start"], sc[j1 + k]["end"])
        elif tag == "replace" and i2 - i1 == j2 - j1:
            for k in range(i2 - i1):
                times[i1 + k] = (sc[j1 + k]["start"], sc[j1 + k]["end"])
    matched = {}                                                   # a phrase said with a stutter («Ben je, ben je…»)
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():   # starts on the
        if tag == "equal":                                         # first try: its subtitle comes in with the voice
            for k in range(i2 - i1):
                matched[i1 + k] = j1 + k
    for k, (p, w) in enumerate(A):
        if k in matched and (k == 0 or A[k - 1][0] != p):
            j = matched[k]
            heads = {norm(x) for _, x in [q for q in A if q[0] == p][:2]}
            while j > 0 and (j - 1) not in matched.values() and norm(sc[j - 1]["text"]) in heads and sc[j]["start"] - sc[j - 1]["start"] < 0.6:
                j -= 1
            times[k] = (sc[j]["start"], times[k][1])
    missing = [A[k][1] for k in range(len(A)) if times[k] is None]
    for k in range(len(times)):                                    # a word not matched: between its neighbours
        if times[k] is None:
            prev = next((times[j][1] for j in range(k - 1, -1, -1) if times[j]), 0.0)
            nxt = next((times[j][0] for j in range(k + 1, len(times)) if times[j]), prev + 0.3)
            times[k] = (prev, max(prev + 0.08, min(nxt, prev + 0.3)))
    for p, i, text, t0, t1 in FIX:
        k = [j for j, (pp, _) in enumerate(A) if pp == p][i]
        assert A[k][1] == text, (p, i, A[k][1], text)
        times[k] = (t0, t1)
    out = []
    for p, (who, nl, es) in enumerate(PHRASES):
        ws = [(w, times[k]) for k, (pp, w) in enumerate(A) if pp == p]
        brk = [len(part.split()) for part in nl.split("|")[:-1]]          # «|»: the Dutch line breaks before word i
        brk = [sum(brk[:i + 1]) for i in range(len(brk))]
        out.append({"who": who, "es": es, "breaks": brk, "words": [{"text": w, "t": round(t[0], 3), "end": round(t[1], 3)} for w, t in ws]})
    json.dump({"phrases": out}, open(os.path.join(ROOT, "subs.json"), "w"), ensure_ascii=False, indent=1)
    print(f"subs.json: {len(out)} phrases, {len(A)} words; timed from neighbours: {missing}")


if __name__ == "__main__":
    main()
