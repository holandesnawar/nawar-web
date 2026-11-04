#!/usr/bin/env python3
"""The subtitles: what is said, in short phrases (Dutch as said, Spanish under it), timed word by word from ElevenLabs
Scribe's transcript of the ad (.raw/scribe.json, word timestamps). The Dutch text is checked by ear against the client's
transcript (.raw/suarez.txt) and two Scribe passes; Suárez's own broken Dutch is kept as he says it («Suárez nooit zitten
op de bank»). The Spanish keeps the ad's puns: «fluiten» = to whistle → «pitar» (the referees whistle at him),
«bank» = sofa / the substitutes' bench → «banco / banquillo», «kaartje» = business card → «tarjeta» (yellow and red ones).
«antifluitregeling» is written closed, as Dutch spelling wants (and «antipitidos» as the RAE does).
  python3 tools/subs.py      → subs.json (reel times: source time − T0)
"""
import difflib, json, os, re, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T0 = 135 / 25            # the reel starts at source frame 135 (Suárez walking in, after the ad's brand intro)
END = 40.08              # …and ends before the brand voice-over («Alleen bij …», 40.20)

# (who, Dutch, Spanish): m = the shop assistant, s = Suárez
PHRASES = [      # v3 (after QA): whole clauses where a half would flash by, no article cut from its noun; «we» as said;
                 # every phrase fits two lines at the one subtitle size
    ("m", "Ah, een sportman", "Ah, un deportista"),
    ("m", "van Ajax.", "del Ajax."),
    ("m", "Ja, beroemde club.", "Sí, un club famoso."),
    ("m", "Cruijff, Keizer, Abe Lenstra.", "Cruijff, Keizer, Abe Lenstra."),
    ("m", "Wat kan ik voor u oplossen?", "¿En qué le puedo ayudar?"),
    ("s", "Ja, ik hoorde iets over", "Sí, oí algo sobre"),
    ("s", "één antifluitregeling.", "un control antipitidos."),
    ("m", "Ah, u bedoelt ons hoortoestel", "Ah, se refiere a nuestro audífono"),
    ("m", "met geavanceerde antifluitregeling.", "con control antipitidos avanzado."),
    ("m", "Voorkomt dat u", "Evita que oiga"),
    ("m", "irritante fluittonen hoort.", "pitidos molestos."),
    ("s", "Ja, heel irritant.", "Sí, muy molesto."),
    ("s", "Zij fluiten", "Ellos pitan"),
    ("s", "veel te vaak tegen mij.", "demasiadas veces en mi contra."),
    ("m", "Oh, maar dan is dit model niks voor u.", "Oh, entonces este modelo no es para usted."),
    ("m", "Gaan we naar ons oordopjesgamma.", "Vamos a nuestra gama de tapones para los oídos."),
    ("m", "Neemt u maar even op de bank plaats.", "Siéntese un momento en el banco."),
    ("s", "Hè?", "¿Eh?"),
    ("s", "Suárez nooit zitten op de bank.", "Suárez nunca se sienta en el banquillo."),
    ("m", "Nou, veel succes ermee.", "Pues nada, mucha suerte con ellos."),
    ("m", "En mocht u nog een fluitje horen,", "Y si vuelve a oír un pitido,"),
    ("m", "gewoon even langskomen, hè?", "pásese por aquí, ¿eh?"),
    ("m", "Kaartje?", "¿Una tarjeta?"),
    ("s", "Nee, nee, ik heb kaartjes genoeg.", "No, no, ya tengo tarjetas de sobra."),
]


# (phrase, word) → (start, end) in source seconds: «hè?» after «langskomen» (37.68–37.82 by its waveform; not in Scribe)
OVERRIDE = {(21, 3): (37.68, 37.84)}


def norm(w):
    w = unicodedata.normalize("NFD", w.lower())
    return re.sub(r"[^a-z0-9]", "", "".join(c for c in w if unicodedata.category(c) != "Mn"))


def main():
    sc = [w for w in json.load(open(os.path.join(ROOT, ".raw", "scribe.json")))["words"]
          if w.get("type") == "word" and T0 - 0.2 <= w["start"] < END]
    A = [(p, w) for p, (_, nl, _) in enumerate(PHRASES) for w in nl.split()]
    a, b = [norm(w) for _, w in A], [norm(w["text"]) for w in sc]
    times = [None] * len(A)
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1):
                times[i1 + k] = (sc[j1 + k]["start"], sc[j1 + k]["end"])
        elif tag == "replace":                                   # same span, other spelling: share its time out
            s0, s1 = sc[j1]["start"], sc[j2 - 1]["end"]
            n = i2 - i1
            for k in range(n):
                times[i1 + k] = (s0 + (s1 - s0) * k / n, s0 + (s1 - s0) * (k + 1) / n)
    for k in range(len(times)):                                  # a word Scribe did not hear: between its neighbours
        if times[k] is None:
            prev = next((times[j][1] for j in range(k - 1, -1, -1) if times[j]), T0)
            nxt = next((times[j][0] for j in range(k + 1, len(times)) if times[j]), prev + 0.3)
            times[k] = (prev, max(prev + 0.08, min(nxt, prev + 0.3)))
    for (p, w), (t0, t1) in OVERRIDE.items():                    # times set by ear where Scribe heard nothing
        k = [i for i, (pp, _) in enumerate(A) if pp == p][w]
        times[k] = (t0, t1)
        if k > 0 and times[k - 1][1] > t0:
            times[k - 1] = (times[k - 1][0], t0)
    out = []
    for p, (who, nl, es) in enumerate(PHRASES):
        ws = [(w, times[k]) for k, (pp, w) in enumerate(A) if pp == p]
        out.append({"who": who, "es": es, "words": [{"text": w, "t": round(t[0] - T0, 3), "end": round(t[1] - T0, 3)} for w, t in ws]})
    unheard = [A[k][1] for k in range(len(A)) if not any(abs(times[k][0] - w["start"]) < 1e-6 for w in sc)]
    json.dump({"t0": T0, "end": END, "phrases": out}, open(os.path.join(ROOT, "subs.json"), "w"), ensure_ascii=False, indent=1)
    print(f"subs.json: {len(out)} phrases, {len(A)} words; respelled/unheard (timed from neighbours): {unheard}")


if __name__ == "__main__":
    main()
