#!/usr/bin/env python3
"""The closing ad of the reel «Suárez habla neerlandés» (after the interview): the ebook «Holandés sin miedo» for Black
Friday at 1 €, with a voice-over, ending on «Comenta OFERTA».
  python3 tools/outro.py voz      the voice-over (ElevenLabs, voice VOICE) → .raw/outro/voz.mp3 + outro.json (word times)
  python3 tools/outro.py libro    the ebook animation (the client's «Animación libro interactivo.html», .raw/outro/libro.html)
                                  rendered frame by frame on a transparent ground → assets/video/libro.webm (VP9 + alpha)
  python3 tools/outro.py audio    the voice-over, a soft music bed and a whoosh, mixed → assets/audio/outro.wav
The ElevenLabs key goes as a network secret (api.elevenlabs.io, header xi-api-key) or in ELEVENLABS_API_KEY.
"""
import base64, json, os, subprocess, sys, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, ".raw", "outro")
TEXT = ("Habla neerlandés sin miedo, como Luis Suárez. Nuestro ebook, Holandés sin miedo, este Black Friday por solo un "
        "euro. Comenta OFERTA y te enviamos los detalles.")
VOICE = "6mAi1CJ7479mdT2HGuMI"         # «Nawar Def» (the account's Spanish voice, peninsular)
MODEL = "eleven_multilingual_v2"
SETTINGS = {"stability": 0.5, "similarity_boost": 0.8, "style": 0.0, "speed": 1.0}


def api(path, body):
    h = {"Content-Type": "application/json", "Accept": "application/json"}
    if os.environ.get("ELEVENLABS_API_KEY"):
        h["xi-api-key"] = os.environ["ELEVENLABS_API_KEY"]
    req = urllib.request.Request("https://api.elevenlabs.io/v1" + path, data=json.dumps(body).encode(), headers=h, method="POST")
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.loads(r.read())


def words_of(al):
    """the alignment's characters grouped into words: [{text, t, end}] (seconds)."""
    out, cur = [], None
    for c, s, e in zip(al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]):
        if c.isspace():
            if cur: out.append(cur); cur = None
            continue
        if cur is None:
            cur = {"text": c, "t": s, "end": e}
        else:
            cur["text"] += c; cur["end"] = e
    if cur: out.append(cur)
    return [{"text": w["text"], "t": round(w["t"], 3), "end": round(w["end"], 3)} for w in out]


def voz():
    os.makedirs(RAW, exist_ok=True)
    j = api(f"/text-to-speech/{VOICE}/with-timestamps?output_format=mp3_44100_192",
            {"text": TEXT, "model_id": MODEL, "voice_settings": SETTINGS})
    open(os.path.join(RAW, "voz.mp3"), "wb").write(base64.b64decode(j["audio_base64"]))
    al = j.get("alignment") or j["normalized_alignment"]
    ws = words_of(al)
    json.dump({"text": TEXT, "voice": VOICE, "model": MODEL, "settings": SETTINGS, "words": ws},
              open(os.path.join(ROOT, "outro.json"), "w"), ensure_ascii=False, indent=1)
    print(f"voz.mp3: {len(ws)} words, {ws[0]['t']:.2f}–{ws[-1]['end']:.2f} s")


BOOK_START, BOOK_PLAY, BOOK_END = 0.30, 4.10, 12.30   # outro s: the closed book shows; it opens (on «ebook»); last frame
FPS = 25
CLOCK = "const tick = (now) => { setT(((now - t0) / 1000) % TOTAL); raf = requestAnimationFrame(tick); };"
SEEK = "const tick = () => { setT(window.__T || 0); raf = requestAnimationFrame(tick); };"
SHADOW = "boxShadow: '0 50px 80px -24px rgba(15,25,70,.45), 0 16px 30px -10px rgba(15,25,70,.3)'"   # the book's drop shadow:
                                                                                                   # off (flat, as in the BF ad)
DISPLAY_W = 846                        # the book's box in the reel (px wide)
SHOT_JS = r"""
const { chromium } = require('playwright');
(async () => {
  const [page, out, n, fps] = process.argv.slice(2);
  const b = await chromium.launch();
  const pg = await b.newPage({ viewport: { width: 1300, height: 1100 }, deviceScaleFactor: 1.5 });
  await pg.route('**/*', r => /^(file|data|blob):/.test(r.request().url()) ? r.continue() : r.abort());   // offline
  await pg.goto('file://' + page);
  await pg.waitForFunction(() => window.LibroEmbed && document.querySelectorAll('img').length > 10, null, { timeout: 60000 });
  await pg.addStyleTag({ content: 'html, body { padding: 100px 30px 0 30px !important; }' });   // room around the 1240×900 view: nothing is cut
  await pg.evaluate(() => Promise.all([...document.images].map(i => i.decode().catch(() => 0))));
  for (let k = 0; k < +n; k++) {
    await pg.evaluate(t => { window.__T = t; return new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r))); }, k / +fps);
    await pg.screenshot({ path: `${out}/f${String(k).padStart(4, '0')}.png`, omitBackground: true });
  }
  await b.close();
})();
"""


def libro():
    """the book, rendered at its own clock (T = 0…7 s: it opens, three pages turn, it closes) with T set frame by frame
    (window.__T instead of the page's real-time clock), on a transparent ground, then held closed before (from
    BOOK_START) and after (to BOOK_END) → assets/video/libro.webm, DISPLAY_W wide (+ libro.json)."""
    import gzip, re, shutil
    src = open(os.path.join(RAW, "libro.html"), encoding="utf-8").read()
    m = re.search(r'(<script type="__bundler/manifest">)(.*?)(</script>)', src, re.S)
    man = json.loads(m.group(2))
    key = next(k for k, v in man.items() if b"LibroEmbed" in gzip.decompress(base64.b64decode(v["data"])))
    jsx = gzip.decompress(base64.b64decode(man[key]["data"])).decode("utf-8")
    assert jsx.count(CLOCK) == 1 and jsx.count(SHADOW) == 1, "the animation's code is not as expected"
    jsx = jsx.replace(CLOCK, SEEK).replace(SHADOW, "boxShadow: 'none'")
    man[key]["data"] = base64.b64encode(gzip.compress(jsx.encode("utf-8"))).decode()
    page = os.path.join(RAW, "libro-seek.html")
    open(page, "w", encoding="utf-8").write(src[:m.start(2)] + json.dumps(man) + src[m.end(2):])
    frames = os.path.join(RAW, "libro-frames"); shutil.rmtree(frames, ignore_errors=True); os.makedirs(frames)
    js = os.path.join(RAW, "shot.cjs"); open(js, "w").write(SHOT_JS)
    n = int(round(7.0 * FPS)) + 1                                  # T = 0 … 7.0 (closed again)
    subprocess.run(["node", js, page, frames, str(n), str(FPS)], check=True)
    from PIL import Image
    import numpy as np
    box = None                                                     # the union of the book's extent over every frame
    for k in range(n):
        a = np.asarray(Image.open(os.path.join(frames, f"f{k:04d}.png")))[..., 3]
        ys, xs = np.nonzero(a > 4)
        b = [xs.min(), ys.min(), xs.max() + 1, ys.max() + 1]
        box = b if box is None else [min(box[0], b[0]), min(box[1], b[1]), max(box[2], b[2]), max(box[3], b[3])]
    H0 = a.shape[0]; W0 = a.shape[1]
    box = [max(0, box[0] - 12), max(0, box[1] - 12), min(W0, box[2] + 12), min(H0, box[3] + 12)]
    assert box[1] > 0 and box[3] < H0 and box[0] > 0 and box[2] < W0, f"the book touches the capture's edge: {box}"
    cw, ch = box[2] - box[0], box[3] - box[1]
    dw = DISPLAY_W; dh = int(round(ch * dw / cw / 2)) * 2
    pre = int(round((BOOK_PLAY - BOOK_START) * FPS)); post = int(round((BOOK_END - BOOK_START) * FPS)) - pre - n
    seq = [0] * pre + list(range(n)) + [n - 1] * post
    lst = os.path.join(RAW, "libro-seq.txt")
    open(lst, "w").write("".join(f"file 'libro-frames/f{k:04d}.png'\nduration {1 / FPS:.4f}\n" for k in seq) +
                         f"file 'libro-frames/f{seq[-1]:04d}.png'\n")
    out = os.path.join(ROOT, "assets", "video", "libro.webm")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-vf",
                    f"crop={cw}:{ch}:{box[0]}:{box[1]},scale={dw}:{dh}:flags=lanczos,format=yuva420p", "-r", str(FPS), "-frames:v", str(len(seq)), "-c:v", "libvpx-vp9",
                    "-pix_fmt", "yuva420p", "-b:v", "0", "-crf", "18", "-row-mt", "1", "-auto-alt-ref", "0", out], check=True)
    # where the closed book sits in the clip (for the layout): its box in the first frame, in clip px
    a = np.asarray(Image.open(os.path.join(frames, "f0000.png")))[..., 3]; ys, xs = np.nonzero(a > 4); sc = dw / cw
    closed = [round((xs.min() - box[0]) * sc), round((ys.min() - box[1]) * sc), round((xs.max() - box[0]) * sc), round((ys.max() - box[1]) * sc)]
    json.dump({"width": dw, "height": dh, "fps": FPS, "start": BOOK_START, "play": BOOK_PLAY, "end": BOOK_END, "closed": closed},
              open(os.path.join(ROOT, "assets", "video", "libro.json"), "w"))
    print(f"libro.webm: {dw}×{dh}, {len(seq)} frames ({len(seq) / FPS:.2f} s): closed {pre}, animation {n}, closed {post}; "
          f"capture box {box}, the closed book at {closed}")


VO_AT = 0.60                           # outro s: the voice-over starts (the blue is fully in at 0.30)
END = 12.30                            # the outro's length (the cover and the call to action hold after the last word)
VO_LUFS, BED_LUFS = -15.0, -35.0       # the voice a touch under the interview (−14.5), the bed 20 LU under the voice
BED_FROM = 0.023 + 8 * 4 * 60 / 107.7  # «musica v1» (the BF ad's track): from bar 8, where its light groove comes in
BED_AT, BED_IN, BED_OUT = 0.25, 0.6, 1.2
EQ = "highpass=f=110,lowshelf=f=150:g=-6,lowshelf=f=250:g=-6,equalizer=f=2500:t=q:w=0.9:g=-3"   # (as in the BF ad: room for the voice)
SR = 48000


def lufs(path):
    import re
    out = subprocess.run(["ffmpeg", "-nostats", "-i", path, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", out)[-1])


def load(path, extra=""):
    import numpy as np
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-af", f"aresample={SR}{',' + extra if extra else ''}", "-ac", "2",
                          "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()


def audio():
    """the outro's sound: a soft whoosh on the cut to blue, the bed fading in under it, the voice-over from VO_AT →
    assets/audio/outro.wav (END s, 48 kHz)."""
    import numpy as np, soundfile as sf
    n = int(round(END * SR)); mix = np.zeros((n, 2), np.float32)
    tmp = os.path.join(RAW, "vo.wav")
    # the voice to VO_LUFS with its true peak under −2.5 dBTP (as the interview): a gentle compressor, then loudnorm in
    # two passes (measured, then applied)
    comp = "acompressor=threshold=-20dB:ratio=2.5:attack=5:release=90:makeup=2"
    out = subprocess.run(["ffmpeg", "-nostats", "-i", os.path.join(RAW, "voz.mp3"), "-af",
                          f"{comp},loudnorm=I={VO_LUFS}:TP=-2.5:LRA=7:print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
    ms = json.loads(out[out.rindex("{"):out.rindex("}") + 1])
    ln = (f"loudnorm=I={VO_LUFS}:TP=-2.5:LRA=7:measured_I={ms['input_i']}:measured_TP={ms['input_tp']}:measured_LRA={ms['input_lra']}"
          f":measured_thresh={ms['input_thresh']}:offset={ms['target_offset']}:linear=true")
    vo = load(os.path.join(RAW, "voz.mp3"), f"{comp},{ln},aresample={SR}")
    a = int(VO_AT * SR); mix[a:a + len(vo)] += vo[:n - a]
    bed = load(os.path.join(RAW, "music.mp3"), f"atrim=start={BED_FROM:.3f}:duration={END - BED_AT + 1:.3f},asetpts=N/SR/TB,{EQ}")
    sf.write(tmp, bed, SR); bed *= 10 ** ((BED_LUFS - lufs(tmp)) / 20)
    m = int((END - BED_AT) * SR); bed = bed[:m]
    t = np.arange(len(bed)) / SR
    bed *= np.clip(t / BED_IN, 0, 1)[:, None] * np.clip((END - BED_AT - t) / BED_OUT, 0, 1)[:, None]
    a = int(BED_AT * SR); mix[a:a + len(bed)] += bed
    wh = load(os.path.join(RAW, "whoosh.mp3")) * 10 ** (-9 / 20)    # soft: under the bed's first bar
    mix[:len(wh)] += wh[:n]
    sf.write(tmp, mix, SR)
    peak = np.abs(mix).max()
    os.makedirs(os.path.join(ROOT, "assets", "audio"), exist_ok=True)
    out = os.path.join(ROOT, "assets", "audio", "outro.wav"); sf.write(out, mix, SR, subtype="PCM_24")
    print(f"outro.wav: {END} s, voice {VO_LUFS} LUFS from {VO_AT} s, bed {BED_LUFS} LUFS, peak {20 * np.log10(peak):.1f} dBFS")


if __name__ == "__main__":
    {"voz": voz, "libro": libro, "audio": audio}[sys.argv[1]]()
