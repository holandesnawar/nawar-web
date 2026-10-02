"""Frame timing plan derived from the word-aligned voiceover (v2).

Master timeline: the voiceover file starts at VO_OFFSET. Each frame starts LEAD seconds before its
first spoken word (inside the preceding pause), so the cut lands just ahead of the voice — except the
cuts the soundtrack dictates (audio_v2.json): the music STOP (20-pausa), the DROP (21-portatil) and the
re-drop on the call to action (38-cta). The end card runs to the end of the soundtrack.
Writes timing.json with per-frame windows and frame-relative word cues.
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEAD = 0.12

# (frame_id, first words of the frame)
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
    ("13-tres-fases", "Son tres fases"),
    ("14-supervivencia", "Presentarte"),
    ("15-vocabulario", "Luego vocabulario"),
    ("16-estructura", "Y después estructura"),
    ("17-traducir", "Todo para que"),
    ("18-sonidos", "Y desde el primer"),
    ("19-delatan", "Son los que"),
    ("20-pausa", "Vale"),
    ("21-portatil", "Dieciséis semanas"),
    ("22-modulos", "Diez módulos"),
    ("23-camino", "Cada módulo se"),
    ("24-videos", "Aprendes con vídeos"),
    ("25-practica", "Lectura escritura"),
    ("26-flashcards", "Además tienes"),
    ("27-consultas", "Te atascas"),
    ("28-directo", "Y cada semana"),
    ("29-mismo-profe", "La cara que"),
    ("30-sin-tests", "Y una cosa más"),
    ("31-suerte", "Estamos cansados"),
    ("32-practicas", "En Nawar escribes"),
    ("33-de-verdad", "No puedes jugar"),
    ("34-al-terminar", "Al terminar"),
    ("35-sin-ingles", "Y cuando el otro"),
    ("36-promesa", "No prometemos"),
    ("37-ahora", "El algún día"),
    ("38-cta", "Completa tu matrícula"),
    ("39-end-card", "Formación Nawar"),
]

def find(words, phrase, start_at):
    toks = phrase.split()
    norm = lambda s: s.lower().strip(",.¿?¡!…:")
    for i in range(start_at, len(words) - len(toks) + 1):
        if all(norm(words[i + k]["text"]) == norm(toks[k]) for k in range(len(toks))):
            return i
    raise SystemExit(f"phrase not found: {phrase}")

def main():
    plan = json.load(open(os.path.join(ROOT, "audio_v2.json")))
    VO_OFFSET = plan["vo_offset"]
    FORCED = {"20-pausa": plan["stop"], "21-portatil": plan["drop"], "38-cta": plan["redrop"]}
    words = json.load(open(os.path.join(ROOT, "transcript.json")))
    starts, idx = [], 0
    for fid, phrase in FRAMES:
        i = find(words, phrase, idx)
        starts.append(i)
        idx = i + 1
    frames = []
    for n, (fid, _) in enumerate(FRAMES):
        w0 = starts[n]
        w1 = starts[n + 1] if n + 1 < len(FRAMES) else len(words)
        t0 = 0.0 if n == 0 else FORCED.get(fid, round(words[w0]["start"] + VO_OFFSET - LEAD, 3))
        frames.append({"id": fid, "start": round(t0, 3), "w0": w0, "w1": w1})
    for n, f in enumerate(frames):
        f["end"] = frames[n + 1]["start"] if n + 1 < len(frames) else plan["total"]
        f["words"] = [
            {"text": w["text"] + (w["punct"] if w["punct"] in [",", ".", "?", "!", "…", ":", ";"] else ""),
             "t": round(w["start"] + VO_OFFSET - f["start"], 3),
             "end": round(w["end"] + VO_OFFSET - f["start"], 3)}
            for w in words[f["w0"]:f["w1"]]
        ]
        f["duration"] = round(f["end"] - f["start"], 3)
        f.pop("w0", None); f.pop("w1", None)
    total = frames[-1]["end"]
    music = {k: plan[k] for k in ("stop", "drop", "redrop", "final_hit", "breakdown", "riser")}
    json.dump({"vo_offset": VO_OFFSET, "total": total, "music": music, "frames": frames},
              open(os.path.join(ROOT, "timing.json"), "w"), ensure_ascii=False, indent=1)
    for f in frames:
        line = " ".join(w["text"] for w in f["words"])
        print(f'{f["id"]:<18} {f["start"]:7.2f}-{f["end"]:7.2f} ({f["duration"]:5.2f}s)  {line[:95]}')
    print("TOTAL", total, "music", music)

if __name__ == "__main__":
    main()
