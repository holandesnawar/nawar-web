#!/usr/bin/env python3
"""Voz automática para reels de vocabulario «¿Sabes decir ESTO en neerlandés?».

El reel es una cuadrícula de dibujos con su palabra en una etiqueta; las etiquetas se iluminan una a una. Este script:
  1. detect  — encuentra las etiquetas, lee su texto (OCR, tesseract nld) y mide en qué fotograma se ilumina cada una.
  2. tts     — dos generaciones con ElevenLabs: la frase en español («¿Sabes decir esto?», cámbiala con --frase) y todas las
               palabras en neerlandés en una sola llamada (/with-timestamps); cada palabra se recorta con los tiempos
               de sus letras, así suenan con la misma voz y entonación.
  3. mix     — coloca cada palabra cuando se ilumina su etiqueta (la frase, al principio, y la primera palabra justo
               después), baja un poco la música original mientras habla la voz, deja la voz a −16 LUFS y exporta el
               vídeo (la imagen no se toca).

  python3 reel_voz.py all  REEL.mp4 --work trabajo/ --out REEL-voz.mp4
  python3 reel_voz.py detect REEL.mp4 --work trabajo/        # solo detectar (revisa trabajo/deteccion.jpg y palabras.txt)
  python3 reel_voz.py voices                                 # lista las voces de tu cuenta de ElevenLabs

La clave se lee de la variable de entorno ELEVENLABS_API_KEY (nunca se escribe en ningún fichero); también vale un secreto de
red que añada la cabecera xi-api-key en las peticiones a api.elevenlabs.io.
Si el OCR lee mal alguna palabra, corrige trabajo/palabras.txt (una por línea, en el orden en que se iluminan) y vuelve
a lanzar `tts` y `mix`: el fichero manda sobre el OCR. Si la voz pronuncia mal una palabra, escribe después de una barra
cómo debe sonar: «het wc-papier | het weesee-papier» (la etiqueta sigue siendo la misma, solo cambia lo que se lee).
Necesita: ffmpeg, python3 con numpy, opencv-python y pytesseract, y tesseract con el idioma nld.
"""
import argparse, base64, json, os, re, subprocess, sys, urllib.request, urllib.error

import numpy as np

API = "https://api.elevenlabs.io/v1"
FPS_SCAN = 30
DEFAULT_PHRASE = "¿Sabes decir esto?"


# ---------------------------------------------------------------- video helpers
def probe(video):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height,r_frame_rate",
                          "-show_entries", "format=duration", "-of", "json", video], capture_output=True, text=True, check=True).stdout
    j = json.loads(out); s = j["streams"][0]; n, d = s["r_frame_rate"].split("/")
    return int(s["width"]), int(s["height"]), float(n) / float(d), float(j["format"]["duration"])


def frames(video, fps=None, scale=None):
    """yields (time, BGR frame) one at a time (never the whole video in memory)."""
    W, H, vfps, _ = probe(video)
    vf = []
    if fps: vf.append(f"fps={fps}")
    if scale: vf.append(f"scale={scale[0]}:{scale[1]}"); W, H = scale
    cmd = ["ffmpeg", "-v", "error", "-i", video] + (["-vf", ",".join(vf)] if vf else []) + ["-f", "rawvideo", "-pix_fmt", "bgr24", "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    step = 1.0 / (fps or vfps); i = 0; size = W * H * 3
    while True:
        buf = p.stdout.read(size)
        if len(buf) < size: break
        yield i * step, np.frombuffer(buf, np.uint8).reshape(H, W, 3)
        i += 1
    p.wait()


# ---------------------------------------------------------------- 1. detect
def find_labels(video):
    """label boxes: pixels that are saturated orange in at least half of the frames (each label is orange most of the time)."""
    import cv2
    acc, n = None, 0
    for _, f in frames(video, fps=1):
        h, s, v = cv2.split(cv2.cvtColor(f, cv2.COLOR_BGR2HSV))
        m = (h >= 5) & (h <= 22) & (s > 150) & (v > 180)
        acc = m.astype(np.uint16) if acc is None else acc + m; n += 1
    mask = (acc >= n * 0.5).astype(np.uint8) * 255
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((3, 7), np.uint8))
    k, _, st, _ = cv2.connectedComponentsWithStats(mask)
    boxes = [tuple(int(v) for v in st[i][:4]) for i in range(1, k) if st[i][2] > 80 and 30 < st[i][3] < 90 and st[i][4] > 2000]
    return sorted(boxes, key=lambda b: (round(b[1] / 60), b[0]))


def detect(video, work):
    import cv2, pytesseract
    os.makedirs(work, exist_ok=True)
    boxes = find_labels(video)
    if not boxes:
        sys.exit("no he encontrado etiquetas naranjas en el vídeo")
    # every frame: mean colour inside each label (a few px in from the edge)
    _, _, _, dur = probe(video)
    cols, times, refs = [], [], {}                      # refs: two frames (start, middle) to read the labels from
    for t, f in frames(video, fps=FPS_SCAN):
        cols.append([f[y + 8:y + h - 8, x + 8:x + w - 8].reshape(-1, 3).mean(0) for (x, y, w, h) in boxes]); times.append(t)
        if not refs or (len(refs) == 1 and t >= dur / 2): refs[len(times) - 1] = f.copy()
    C = np.array(cols)                                   # frames × labels × BGR
    base = np.median(C, axis=0)                          # the label's usual colour (orange)
    dist = np.linalg.norm(C - base[None], axis=2)        # how far each label is from its usual colour
    changed = dist > 60
    valid = changed.sum(axis=1) <= 3                     # frames where the whole grid changes (end card) don't count
    lit = changed & valid[:, None]
    items = []
    for k, b in enumerate(boxes):
        on = np.where(lit[:, k])[0]
        runs = np.split(on, np.where(np.diff(on) > 1)[0] + 1) if len(on) else []
        runs = [r for r in runs if len(r) >= 5]
        if not runs:
            continue
        r = runs[0]
        items.append({"box": b, "start": round(times[r[0]], 3), "end": round(times[r[-1]] + 1 / FPS_SCAN, 3)})
    # OCR each label on a frame where it is not lit, four ways (binarised / grey, line / word mode); the most common
    # reading wins, and on a tie the one with accents (small dots like the ö of föhn are the first thing to get lost)
    for it in items:
        k = boxes.index(it["box"]); x, y, w, h = it["box"]
        ref = next((f for i, f in refs.items() if not lit[i, k]), next(iter(refs.values())))
        g = cv2.cvtColor(cv2.resize(ref[y:y + h, x:x + w], None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC), cv2.COLOR_BGR2GRAY)
        _, bw = cv2.threshold(g, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        if bw.mean() < 127: bw = 255 - bw                # tesseract wants dark text on white
        gi = g if g.mean() > 127 else 255 - g
        reads = [re.sub(r"^\W+|\W+$", "", re.sub(r"\s+", " ", pytesseract.image_to_string(im, lang="nld", config=f"--psm {psm}")))
                 for im in (bw, gi) for psm in (7, 8)]          # stray marks at the edges (‘ | .) are not part of the word
        reads = [r for r in reads if r]
        it["ocr"] = max(reads, key=lambda r: (reads.count(r), any(ord(ch) > 127 for ch in r))) if reads else "?"
    items.sort(key=lambda it: it["start"])
    json.dump({"video": os.path.abspath(video), "items": items}, open(os.path.join(work, "deteccion.json"), "w"), ensure_ascii=False, indent=1)
    words_txt = os.path.join(work, "palabras.txt")
    if not os.path.exists(words_txt):
        open(words_txt, "w").write("\n".join(it["ocr"] for it in items) + "\n")
    # contact image: every label numbered in speaking order, with its time
    vis = next(iter(refs.values())).copy()
    for i, it in enumerate(items):
        x, y, w, h = it["box"]
        cv2.rectangle(vis, (x, y), (x + w, y + h), (0, 255, 0), 3)
        cv2.putText(vis, f"{i + 1} {it['start']:.1f}s", (x, y - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    cv2.imwrite(os.path.join(work, "deteccion.jpg"), cv2.resize(vis, (vis.shape[1] // 2, vis.shape[0] // 2)))
    print(f"{len(items)} etiquetas (orden en que se iluminan):")
    for i, it in enumerate(items):
        print(f"  {i + 1:2d}. {it['start']:6.2f}–{it['end']:6.2f}s  {it['ocr']}")
    return items


# ---------------------------------------------------------------- 2. tts (ElevenLabs)
def api(path, body=None, method=None):
    # the key comes from ELEVENLABS_API_KEY; without it the request goes out bare, for environments whose proxy adds
    # the key itself (a network secret for api.elevenlabs.io)
    key = os.environ.get("ELEVENLABS_API_KEY")
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    if key: headers["xi-api-key"] = key
    req = urllib.request.Request(API + path, data=json.dumps(body).encode() if body is not None else None,
                                 method=method or ("POST" if body is not None else "GET"), headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        if e.code == 401:
            sys.exit("ElevenLabs no acepta la petición (401): falta la clave o no es válida. Ponla en la variable de entorno "
                     "ELEVENLABS_API_KEY (o como secreto de red para api.elevenlabs.io).")
        sys.exit(f"ElevenLabs {e.code}: {e.read().decode(errors='replace')[:400]}")
    except urllib.error.URLError as e:
        sys.exit(f"no puedo conectar con api.elevenlabs.io ({e.reason}): ¿está permitido ese dominio en la red?")


def voice_id(name_or_id):
    voices = api("/voices")["voices"]
    for v in voices:
        if name_or_id in (v["voice_id"], v["name"]) or v["name"].lower().startswith(name_or_id.lower()):
            return v["voice_id"], v["name"]
    sys.exit(f"no encuentro la voz «{name_or_id}» en tu cuenta (mira `reel_voz.py voices`)")


def tts(text, voice, model, work, name, language=None):
    body = {"text": text, "model_id": model, "voice_settings": {"stability": 0.55, "similarity_boost": 0.8, "style": 0.0}}
    if language:
        body["language_code"] = language
    j = api(f"/text-to-speech/{voice}/with-timestamps?output_format=mp3_44100_128", body)
    mp3 = os.path.join(work, f"{name}.mp3"); open(mp3, "wb").write(base64.b64decode(j["audio_base64"]))
    al = j.get("alignment") or j.get("normalized_alignment")
    json.dump({"text": text, "alignment": al}, open(os.path.join(work, f"{name}.json"), "w"), ensure_ascii=False, indent=1)
    return mp3, al


def generate(work, voice_es, voice_nl, model, phrase):
    items = json.load(open(os.path.join(work, "deteccion.json")))["items"]
    lines = [w.strip() for w in open(os.path.join(work, "palabras.txt")).read().splitlines() if w.strip()]
    words = [(l.split("|")[1] if "|" in l else l).strip() for l in lines]   # what the voice reads
    if len(words) != len(items):
        sys.exit(f"palabras.txt tiene {len(words)} palabras y hay {len(items)} etiquetas")
    ves, nes = voice_id(voice_es); vnl, nnl = voice_id(voice_nl)
    print(f"voz ES: {nes} · voz NL: {nnl} · modelo {model}")
    # generation 1: the Spanish question
    tts(phrase, ves, model, work, "frase_es", language="es" if "v2_5" in model or "flash" in model else None)
    # generation 2: every Dutch word in one go, each as its own short sentence, so they share voice and intonation
    text = "\n\n".join(w[0].upper() + w[1:] + "." for w in words)
    _, al = tts(text, vnl, model, work, "palabras_nl", language="nl" if "v2_5" in model or "flash" in model else None)
    chars, st, en = al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]
    joined = "".join(chars)
    cuts, pos = [], 0
    for w in words:
        target = w[0].upper() + w[1:]
        i = joined.find(target, pos)
        if i < 0:
            sys.exit(f"no encuentro «{w}» en la alineación de ElevenLabs")
        j = i + len(target) - 1; pos = j + 1
        cuts.append({"word": lines[len(cuts)].split("|")[0].strip(), "said": w, "start": round(st[i], 3), "end": round(en[j], 3)})
    json.dump(cuts, open(os.path.join(work, "cortes_nl.json"), "w"), ensure_ascii=False, indent=1)
    print("generadas: frase en español + %d palabras en neerlandés" % len(cuts))


# ---------------------------------------------------------------- 3. mix
def load_audio(path, sr=48000):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "2", "-ar", str(sr), "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()


def lufs_of(x, sr=48000):
    p = subprocess.run(["ffmpeg", "-nostats", "-f", "f32le", "-ar", str(sr), "-ac", "2", "-i", "-", "-af", "ebur128", "-f", "null", "-"],
                       input=x.astype(np.float32).tobytes(), capture_output=True)
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", p.stderr.decode())[-1])


def mix(video, work, out, lead=0.1, gap=0.2, duck_db=-3.0, voice_lufs=-16.0, phrase_at=0.15):
    sr = 48000
    items = json.load(open(os.path.join(work, "deteccion.json")))["items"]
    cuts = json.load(open(os.path.join(work, "cortes_nl.json")))
    music = load_audio(video)
    nl = load_audio(os.path.join(work, "palabras_nl.mp3")); es = load_audio(os.path.join(work, "frase_es.mp3"))
    voice = np.zeros_like(music)
    def put(clip, t):
        a = int(round(t * sr)); b = min(len(voice), a + len(clip)); voice[a:b] += clip[:b - a]; return a, b
    def trim(x):                                          # drop leading/trailing silence of a clip
        e = np.abs(x).max(1); on = np.where(e > 10 ** (-45 / 20))[0]
        return x[max(0, on[0] - int(0.01 * sr)):on[-1] + int(0.06 * sr)] if len(on) else x
    es = trim(es)
    spans = [put(es, phrase_at)]
    t_free = phrase_at + len(es) / sr + gap              # the first word waits for the question to finish
    plan = []
    for it, c in zip(items, cuts):
        a = int(max(0, (c["start"] - 0.03)) * sr); b = int((c["end"] + 0.10) * sr)
        clip = nl[a:b].copy(); f = int(0.008 * sr)
        clip[:f] *= np.linspace(0, 1, f)[:, None]; clip[-f * 3:] *= np.linspace(1, 0, f * 3)[:, None]
        t = max(it["start"] + lead, t_free)
        spans.append(put(clip, t)); t_free = t + len(clip) / sr + 0.05
        plan.append((c["word"], it["start"], round(t, 3)))
    # loudness: the voice to voice_lufs; the original track ducked under it with short ramps
    g = 10 ** ((voice_lufs - lufs_of(voice)) / 20); voice *= g
    env = np.ones(len(music), np.float32); r = int(0.2 * sr); d = 10 ** (duck_db / 20)
    for a, b in spans:
        env[max(0, a - r):b + r] = np.minimum(env[max(0, a - r):b + r], d)
    env = np.convolve(env, np.ones(r) / r, mode="same").astype(np.float32)
    mixd = music * env[:, None] + voice
    wav = os.path.join(work, "mezcla.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(sr), "-ac", "2", "-i", "-", "-af", "alimiter=limit=0.89:level=false", wav],
                   input=mixd.astype(np.float32).tobytes(), check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", video, "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-movflags", "+faststart", "-shortest", out], check=True)
    print(f"vídeo con voz → {out}")
    for w, s, t in plan:
        print(f"  {s:6.2f}s etiqueta · {t:6.2f}s voz  {w}")


# ---------------------------------------------------------------- cli
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("detect", "tts", "mix", "all"):
        p = sub.add_parser(name)
        if name in ("detect", "mix", "all"): p.add_argument("video")
        p.add_argument("--work", default="trabajo")
        if name in ("tts", "all"):
            p.add_argument("--voz-es", default=os.environ.get("ELEVENLABS_VOICE_ES", "Sarah"))
            p.add_argument("--voz-nl", default=os.environ.get("ELEVENLABS_VOICE_NL", "Sarah"))
            p.add_argument("--modelo", default="eleven_multilingual_v2")
            p.add_argument("--frase", default=DEFAULT_PHRASE)
        if name in ("mix", "all"):
            p.add_argument("--out", required=True)
            p.add_argument("--duck", type=float, default=-3.0, help="dB que baja la música original mientras suena la voz")
    sub.add_parser("voices")
    a = ap.parse_args()
    if a.cmd == "voices":
        for v in api("/voices")["voices"]:
            lab = v.get("labels") or {}
            print(f"  {v['name']:<28} {v['voice_id']}  {lab.get('accent', '')} {lab.get('language', '')} {lab.get('gender', '')}")
        return
    if a.cmd in ("detect", "all"): detect(a.video, a.work)
    if a.cmd in ("tts", "all"): generate(a.work, a.voz_es, a.voz_nl, a.modelo, a.frase)
    if a.cmd in ("mix", "all"): mix(a.video, a.work, a.out, duck_db=a.duck)


if __name__ == "__main__":
    main()
