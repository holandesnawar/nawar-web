"""Frame timing plan derived from the word-aligned voiceover.

Master timeline: the voiceover starts at VO_OFFSET. Each frame starts LEAD
seconds before its first spoken word (inside the preceding pause), so the cut
lands just ahead of the voice. Writes timing.json with per-frame windows and
frame-relative word cues, which the packet builder and assembler consume.
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VO_OFFSET = 0.40
LEAD = 0.12
END_CARD = 6.2

# (frame_id, first word index of the frame) — word ids from transcript.json
FRAMES = [
    ("01-hook", "Si"),
    ("02-no-valgas", "Y no, no es que"),
    ("03-tres-minutos", "Te lo explico"),
    ("04-llevas-anos", "Llevas años aquí"),
    ("05-situaciones", "Pero llegas"),
    ("06-atascado", "y el neerlandés se"),
    ("07-intentos", "Y no será"),
    ("08-app-silencio", "Una app"),
    ("09-preguntas", "Ahora dime"),
    ("10-escuelas", "Casi ninguna"),
    ("11-nawar-nace", "Nawar nace"),
    ("12-metodo", "Un método"),
    ("13-tres-fases", "Tres fases"),
    ("14-supervivencia", "Presentarte"),
    ("15-vocabulario", "Vocabulario real"),
    ("16-estructura", "Estructura y soltura"),
    ("17-traducir", "Todo con un"),
    ("18-sonidos", "Y desde el primer"),
    ("19-delatan", "Son los que"),
    ("20-por-dentro", "Cómo es por"),
    ("21-tu-ritmo", "Tú marcas"),
    ("22-clase-directo", "Cada semana"),
    ("23-comunidad", "Y tienes una"),
    ("24-acompanado", "Avanzas a tu"),
    ("25-end-card", None),
]

def find(words, phrase, start_at):
    toks = phrase.split()
    norm = lambda s: s.lower().strip(",.¿?¡!…:")
    for i in range(start_at, len(words) - len(toks) + 1):
        if all(norm(words[i + k]["text"]) == norm(toks[k]) for k in range(len(toks))):
            return i
    raise SystemExit(f"phrase not found: {phrase}")

def main():
    words = json.load(open(os.path.join(ROOT, "transcript.json")))
    starts, idx = [], 0
    for fid, phrase in FRAMES:
        if phrase is None:
            starts.append(None)
            continue
        i = find(words, phrase, idx)
        starts.append(i)
        idx = i + 1
    spoken = [(k, fid) for k, (fid, phrase) in enumerate(FRAMES) if phrase is not None]
    frames = []
    for n, (k, fid) in enumerate(spoken):
        w0 = starts[k]
        w1 = starts[spoken[n + 1][0]] if n + 1 < len(spoken) else len(words)
        t0 = 0.0 if n == 0 else round(words[w0]["start"] + VO_OFFSET - LEAD, 3)
        frames.append({"id": fid, "start": t0, "w0": w0, "w1": w1})
    for n, f in enumerate(frames):
        f["end"] = frames[n + 1]["start"] if n + 1 < len(frames) else round(words[f["w1"] - 1]["end"] + VO_OFFSET + 0.45, 3)
        f["words"] = [
            {"text": w["text"] + (w["punct"] if w["punct"] in [",", ".", "?", "!", "…", ":", ";"] else ""),
             "t": round(w["start"] + VO_OFFSET - f["start"], 3),
             "end": round(w["end"] + VO_OFFSET - f["start"], 3)}
            for w in words[f["w0"]:f["w1"]]
        ]
    end_id = [fid for fid, phrase in FRAMES if phrase is None][0]
    t0 = frames[-1]["end"]
    frames.append({"id": end_id, "start": t0, "end": round(t0 + END_CARD, 3), "words": []})
    for f in frames:
        f["duration"] = round(f["end"] - f["start"], 3)
        f.pop("w0", None); f.pop("w1", None)
    total = frames[-1]["end"]
    json.dump({"vo_offset": VO_OFFSET, "total": total, "frames": frames}, open(os.path.join(ROOT, "timing.json"), "w"), ensure_ascii=False, indent=1)
    for f in frames:
        line = " ".join(w["text"] for w in f["words"])
        print(f'{f["id"]:<18} {f["start"]:7.2f}-{f["end"]:7.2f} ({f["duration"]:5.2f}s)  {line[:90]}')
    print("TOTAL", total)

if __name__ == "__main__":
    main()
