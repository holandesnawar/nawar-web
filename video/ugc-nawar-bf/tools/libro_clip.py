#!/usr/bin/env python3
"""The ebook for ins-04, cut to her words, from the client's «Animación Libro Interactivo» (4 s: the cover of «Holandés
sin miedo» opens, the pages turn — Klanken (Sonidos), De familie, De nummers, Hebben en zijn — and it closes).

assets/video/libro-ins04.mp4 (1280×720, silent) runs from the start of ins-04 to «gramática»:
  · the cover, still, while she says «este libro: 70 páginas en español, para…» (a CSS push moves it),
  · on «imprimir» the book opens (source 0.30–1.05 s, real speed),
  · then the pages riffle (source 1.05–3.10 s, sped up) and land on «De nummers | Hebben en zijn» as she says «gramática».
Two stills follow in ins-04 (assets/img/libro-nummers.png = that last spread, for «gramática» and «ejercicios»;
assets/img/libro-klanken.png = «Cómo usar este libro | Klanken (Sonidos)», for «cómo pronunciar los sonidos»).
The sped-up part keeps its own frames (no interpolation needed).
"""
import json, os, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, ".raw", "libro.mp4")
COVER, OPEN0, OPEN1, END, KLANKEN = 0.15, 0.30, 1.05, 3.10, 1.00   # source seconds


def main():
    ed = json.load(open(os.path.join(ROOT, "edit.json")))
    ins = next(i for i in ed["inserts"] if i["id"] == "ins-04")
    W = [w for w in ed["words"] if ins["start"] <= w["t"] < ins["start"] + ins["duration"]]
    t = lambda word: next(w["t"] for w in W if w["text"].lower().strip("¿¡") == word) - ins["start"]
    hold = round(t("imprimir") - 0.05, 3)                      # cover until «imprimir»
    open_d = OPEN1 - OPEN0                                     # the book opens at real speed
    riffle = round(t("gramática") + 0.05 - hold - open_d, 3)  # the pages, landing on «gramática»
    sp = (END - OPEN1) / riffle
    out = os.path.join(ROOT, "assets", "video", "libro-ins04.mp4")
    n = int(round(hold * 30)); f = lambda sec: int(round(sec * 30))
    fc = (f"[0:v]split=3[s0][s1][s2];"
          f"[s0]trim=start_frame={f(COVER)}:end_frame={f(COVER) + 1},loop=loop={n - 1}:size=1:start=0,setpts=N/30/TB[a];"
          f"[s1]trim=start_frame={f(OPEN0)}:end_frame={f(OPEN1)},setpts=N/30/TB[b];"
          f"[s2]trim=start_frame={f(OPEN1)}:end_frame={f(END)},setpts=(PTS-STARTPTS)/{sp:.4f},fps=30,setpts=N/30/TB[c];"
          f"[a][b][c]concat=n=3:v=1:a=0,format=yuv420p[v]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", SRC, "-filter_complex", fc, "-map", "[v]", "-an", "-c:v", "libx264",
                    "-preset", "slow", "-crf", "16", "-g", "15", "-movflags", "+faststart", out], check=True)
    for name, at in (("libro-nummers", END), ("libro-klanken", KLANKEN)):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{at}", "-i", SRC, "-frames:v", "1",
                        os.path.join(ROOT, "assets", "img", f"{name}.png")], check=True)
    print(f"libro-ins04.mp4: cover {hold}s · opens {open_d:.2f}s · pages {riffle}s (×{sp:.2f}) = {hold + open_d + riffle:.2f}s")


if __name__ == "__main__":
    main()
