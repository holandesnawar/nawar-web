#!/usr/bin/env python3
"""Voz automática para reels de vocabulario «¿Sabes decir ESTO en neerlandés?».

El reel es una cuadrícula de dibujos con su palabra en una etiqueta; las etiquetas se iluminan una a una. Este script:
  1. detect  — encuentra las etiquetas, lee su texto (OCR, tesseract nld) y mide en qué fotograma se ilumina cada una.
  2. tts     — dos generaciones con ElevenLabs: la frase en español («¿Sabes decir esto?», cámbiala con --frase) y todas las
               palabras en neerlandés en una sola llamada (/with-timestamps); cada palabra se recorta con los tiempos
               de sus letras, así suenan con la misma voz y entonación.
  3. mix     — coloca cada palabra cuando se ilumina su etiqueta (la frase, al principio, y la primera palabra justo
               después), deja la música original de fondo a un nivel fijo (los picos en −19 dB como mucho: si viene
               más alta, baja; si ya está más baja, no se toca), la voz a −11 LUFS y un 10 % más lenta (sin cambiar el
               tono), y exporta el vídeo (la imagen no se toca).

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


def tts(text, voice, model, work, name, language=None, speed=1.0):
    body = {"text": text, "model_id": model,
            "voice_settings": {"stability": 0.55, "similarity_boost": 0.8, "style": 0.0, "speed": speed}}
    if language:
        body["language_code"] = language
    j = api(f"/text-to-speech/{voice}/with-timestamps?output_format=mp3_44100_128", body)
    mp3 = os.path.join(work, f"{name}.mp3"); open(mp3, "wb").write(base64.b64decode(j["audio_base64"]))
    al = j.get("alignment") or j.get("normalized_alignment")
    json.dump({"text": text, "alignment": al}, open(os.path.join(work, f"{name}.json"), "w"), ensure_ascii=False, indent=1)
    return mp3, al


def sentence(w):
    return w[0].upper() + w[1:]


def word_times(al, words):
    """(start, end) of each word in an ElevenLabs alignment, in order."""
    chars, st, en = al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]
    joined, out, pos = "".join(chars), [], 0
    for w in words:
        i = joined.find(sentence(w), pos)
        if i < 0:
            sys.exit(f"no encuentro «{w}» en la alineación de ElevenLabs")
        j = i + len(sentence(w)) - 1; pos = j + 1
        out.append((round(st[i], 3), round(en[j], 3)))
    return out


def generate(work, voice_es, voice_nl, model, phrase, speed=1.0, only=None):
    """only: 1-based numbers of the words to generate again (the others and the phrase stay as they are)."""
    items = json.load(open(os.path.join(work, "deteccion.json")))["items"]
    lines = [w.strip() for w in open(os.path.join(work, "palabras.txt")).read().splitlines() if w.strip()]
    words = [(l.split("|")[1] if "|" in l else l).strip() for l in lines]   # what the voice reads
    labels = [l.split("|")[0].strip() for l in lines]
    if len(words) != len(items):
        sys.exit(f"palabras.txt tiene {len(words)} palabras y hay {len(items)} etiquetas")
    ves, nes = voice_id(voice_es); vnl, nnl = voice_id(voice_nl)
    lang = lambda code: code if "v2_5" in model or "flash" in model else None
    print(f"voz ES: {nes} · voz NL: {nnl} · modelo {model} · velocidad {speed}")
    if only:
        # just these words, in a call of their own (same voice and settings, same one-sentence-per-word text); the cut
        # list points them at the new file, so every other word keeps the take that was already approved
        cuts = json.load(open(os.path.join(work, "cortes_nl.json")))
        ks = sorted({int(n) - 1 for n in only})
        if not ks or ks[0] < 0 or ks[-1] >= len(words):
            sys.exit(f"--solo: números de 1 a {len(words)}")
        n = 1
        while os.path.exists(os.path.join(work, f"palabras_nl_fix{n}.mp3")): n += 1
        name = f"palabras_nl_fix{n}"
        _, al = tts("\n\n".join(sentence(words[k]) + "." for k in ks), vnl, model, work, name, language=lang("nl"), speed=speed)
        for k, (a, b) in zip(ks, word_times(al, [words[k] for k in ks])):
            cuts[k] = {"word": labels[k], "said": words[k], "src": name + ".mp3", "start": a, "end": b}
        json.dump(cuts, open(os.path.join(work, "cortes_nl.json"), "w"), ensure_ascii=False, indent=1)
        print(f"generadas de nuevo: {', '.join(labels[k] for k in ks)} → {name}.mp3")
        return
    # generation 1: the Spanish question
    tts(phrase, ves, model, work, "frase_es", language=lang("es"), speed=speed)
    # generation 2: every Dutch word in one go, each as its own short sentence, so they share voice and intonation
    _, al = tts("\n\n".join(sentence(w) + "." for w in words), vnl, model, work, "palabras_nl", language=lang("nl"), speed=speed)
    cuts = [{"word": labels[k], "said": words[k], "src": "palabras_nl.mp3", "start": a, "end": b}
            for k, (a, b) in enumerate(word_times(al, words))]
    json.dump(cuts, open(os.path.join(work, "cortes_nl.json"), "w"), ensure_ascii=False, indent=1)
    print("generadas: frase en español + %d palabras en neerlandés" % len(cuts))


# ---------------------------------------------------------------- 3. mix
def load_audio(path, sr=48000):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "2", "-ar", str(sr), "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()


def ffilter(x, af, sr=48000, same_length=True):
    """runs a stereo float buffer through an ffmpeg audio filter chain."""
    raw = subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(sr), "-ac", "2", "-i", "-", "-af", af, "-f", "f32le", "-"],
                         input=x.astype(np.float32).tobytes(), capture_output=True, check=True).stdout
    y = np.frombuffer(raw, np.float32).reshape(-1, 2)
    if not same_length:
        return y.copy()
    return np.concatenate([y, np.zeros((max(0, len(x) - len(y)), 2), np.float32)])[:len(x)].copy()


def lufs_of(x, sr=48000):
    p = subprocess.run(["ffmpeg", "-nostats", "-f", "f32le", "-ar", str(sr), "-ac", "2", "-i", "-", "-af", "ebur128", "-f", "null", "-"],
                       input=x.astype(np.float32).tobytes(), capture_output=True)
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", p.stderr.decode())[-1])


def mix(video, work, out, lead=0.1, gap=0.2, music_db=-19.0, duck_db=0.0, voice_lufs=-11.0, tempo=0.9, phrase_at=0.15):
    sr = 48000
    items = json.load(open(os.path.join(work, "deteccion.json")))["items"]
    cuts = json.load(open(os.path.join(work, "cortes_nl.json")))
    has_music = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=index", "-of", "csv=p=0", video],
                               capture_output=True, text=True).stdout.strip()
    music = load_audio(video) if has_music else np.zeros((int(round(probe(video)[3] * sr)), 2), np.float32)
    es = load_audio(os.path.join(work, "frase_es.mp3"))
    srcs = {}
    for c in cuts:
        c.setdefault("src", "palabras_nl.mp3")
        if c["src"] not in srcs: srcs[c["src"]] = load_audio(os.path.join(work, c["src"]))
    voice = np.zeros_like(music)
    def put(clip, t):
        a = int(round(t * sr)); b = min(len(voice), a + len(clip)); voice[a:b] += clip[:b - a]; return a, b
    def trim(x):                                          # drop leading/trailing silence of a clip
        e = np.abs(x).max(1); on = np.where(e > 10 ** (-45 / 20))[0]
        return x[max(0, on[0] - int(0.01 * sr)):on[-1] + int(0.06 * sr)] if len(on) else x
    def slow(x):                                          # tempo < 1: same voice and pitch, a little slower (Rubber Band)
        return ffilter(x, f"rubberband=tempo={tempo}:pitchq=quality", same_length=False) if tempo != 1 else x
    es = slow(trim(es))
    spans = [put(es, phrase_at)]
    t_free = phrase_at + len(es) / sr + gap              # the first word waits for the question to finish
    plan = []
    def edges(src, c):
        # ElevenLabs' letter times can be ~0.1 s off (the voicing before a «d» starts earlier than its «d»), so the cut
        # starts 0.03 s before the first letter and then keeps going back while there is still sound (above the word's
        # loudest 5 ms − 40 dB), and the same after the last letter (from +0.10 s); never into the neighbouring words
        x = srcs[src]; h = int(0.005 * sr)
        rms = lambda i: float(np.sqrt((x[max(0, i):max(0, i) + h] ** 2).mean() + 1e-12))
        s0, e0 = int(c["start"] * sr), int(c["end"] * sr)
        thr = max(rms(i) for i in range(s0, max(s0 + h, e0), h)) * 10 ** (-40 / 20)
        same = sorted((d for d in cuts if d["src"] == src), key=lambda d: d["start"]); k = same.index(c)
        lo = int((same[k - 1]["end"] + 0.12) * sr) if k else 0
        hi = int((same[k + 1]["start"] - 0.10) * sr) if k + 1 < len(same) else len(x)
        a = max(lo, int((c["start"] - 0.03) * sr)); b = min(hi, int((c["end"] + 0.10) * sr))
        while a - h >= lo and rms(a - h) > thr: a -= h
        while b + h <= hi and rms(b) > thr: b += h
        return a, b
    for it, c in zip(items, cuts):
        a, b = edges(c["src"], c)
        clip = slow(srcs[c["src"]][a:b].copy()); f = int(0.008 * sr)
        clip[:f] *= np.linspace(0, 1, f)[:, None]; clip[-f * 3:] *= np.linspace(1, 0, f * 3)[:, None]
        # the first letter lands lead + 0.03 s after the label lights (whatever extra sound the cut kept before it)
        t = max(it["start"] + lead + 0.03 - (c["start"] - a / sr) / tempo, t_free)
        spans.append(put(clip, t)); t_free = t + len(clip) / sr + 0.05
        plan.append((c["word"], it["start"], round(t, 3)))
    # loudness: the voice to voice_lufs, after a gentle compressor (from −16 LUFS: −18 dB threshold, 3:1) that evens out
    # the plosives so a loud voice doesn't lean on the limiter; the original track at one fixed background level with its
    # peaks at music_db at most (a track that is already quieter is left as it is, never raised); optionally ducked
    voice *= 10 ** ((-16.0 - lufs_of(voice)) / 20)
    voice = ffilter(voice, "highpass=f=80,acompressor=threshold=0.125:ratio=3:attack=3:release=100:knee=4:makeup=1")
    voice *= 10 ** ((voice_lufs - lufs_of(voice)) / 20)
    peak = float(np.abs(music).max())
    if peak > 10 ** (music_db / 20):
        music *= 10 ** (music_db / 20) / peak
        print(f"música: picos de {20 * np.log10(peak):.1f} a {music_db:.1f} dB ({music_db - 20 * np.log10(peak):+.1f} dB), nivel fijo")
    elif peak > 0:
        print(f"música: picos en {20 * np.log10(peak):.1f} dB, ya por debajo de {music_db:.1f} dB, se deja igual")
    if duck_db:
        env = np.ones(len(music), np.float32); r = int(0.2 * sr); d = 10 ** (-abs(duck_db) / 20)
        for a, b in spans:
            env[max(0, a - r):b + r] = np.minimum(env[max(0, a - r):b + r], d)
        env = np.convolve(np.pad(env, (r // 2, r - r // 2 - 1), mode="edge"), np.ones(r) / r, mode="valid").astype(np.float32)
        music *= env[:, None]
    mixd = music + voice
    over = 20 * np.log10(max(float(np.abs(mixd).max()), 1e-9) / 0.75)
    print(f"voz a {voice_lufs:.1f} LUFS · el limitador recorta {max(0.0, over):.1f} dB en los picos más altos")
    wav = os.path.join(work, os.path.splitext(os.path.basename(out))[0] + ".mezcla.wav")   # one mix per video
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(sr), "-ac", "2", "-i", "-", "-af", "alimiter=limit=0.75:level=false:latency=1", wav],
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
            if name == "tts":
                p.add_argument("--solo", help="genera de nuevo solo estas palabras (números separados por comas, p. ej. 11,17)")
            p.add_argument("--velocidad", type=float, default=1.0, help="velocidad de ElevenLabs, de 0.7 a 1.2 (por defecto 1.0; para ir más lento usa --tempo en mix, que es más fiable)")
        if name in ("mix", "all"):
            p.add_argument("--out", required=True)
            p.add_argument("--musica", type=float, default=-19.0, help="dB máximos de los picos de la música original (por defecto −19, de fondo; nunca la sube)")
            p.add_argument("--voz", type=float, default=-11.0, help="volumen de la voz en LUFS (por defecto −11)")
            p.add_argument("--tempo", type=float, default=0.9, help="velocidad de la voz al mezclar, sin cambiar el tono (por defecto 0.9, un 10%% más lenta; 1 = como sale de ElevenLabs)")
            p.add_argument("--duck", type=float, default=0.0, help="dB que baja además la música mientras suena la voz (por defecto 0, no baja; p. ej. 3)")
    sub.add_parser("voices")
    a = ap.parse_args()
    if a.cmd == "voices":
        for v in api("/voices")["voices"]:
            lab = v.get("labels") or {}
            print(f"  {v['name']:<28} {v['voice_id']}  {lab.get('accent', '')} {lab.get('language', '')} {lab.get('gender', '')}")
        return
    if a.cmd in ("detect", "all"): detect(a.video, a.work)
    if a.cmd in ("tts", "all"):
        generate(a.work, a.voz_es, a.voz_nl, a.modelo, a.frase, speed=a.velocidad,
                 only=[n for n in (getattr(a, "solo", None) or "").split(",") if n.strip()])
    if a.cmd in ("mix", "all"): mix(a.video, a.work, a.out, music_db=a.musica, duck_db=a.duck, voice_lufs=a.voz, tempo=a.tempo)


if __name__ == "__main__":
    main()
