#!/usr/bin/env python3
"""The closing card of the reel «Aprendiendo neerlandés con Luis Suárez» (v8, the client: no ebook here — «¿quieres
aprender holandés tú también? Aprende con nosotros desde el español»), with the second reel's voice (Yair), ending on
«Síguenos»: an Instagram profile card «Holandés Nawar» whose «Seguir» button is tapped.
v9 (the client: «aprovechar con algún vídeo dentro de la plataforma… el portátil real abriéndose como en el VSL…
comenta OFERTA y te enviamos los detalles de nuestra formación… algún cartel tipo Black Friday, últimas plazas»): the
VSL's MacBook opens onto the course (tools/gen.py), the voice ends on «Comenta OFERTA».
v10 (the client: «no quiero enseñar mi plataforma tipo mira esto, cómpralo… más buscar el dolor… que no suene a
comercial, va para Instagram… comenta QUIERO y te contamos nuestro método… alguna ventaja, desde el español, a tu
ritmo… que la voz acompañe pero no se haga pesada»): Suárez frozen, the viewer's pain, two advantages, «Comenta QUIERO».
v11 (the client: Suárez did understand — the joke is that he takes it all to football; and nothing should leave the
screen): «Suárez lo pilló todo… hasta el doble sentido», the three Dutch words with both meanings, «¿Pillas los chistes en
neerlandés, o sonríes por compromiso?», the two advantages and «Comenta QUIERO», all building up and staying.
v12 (the client: like the ebook closing — all on one screen, almost at once, or people leave; no computer): the
indigo screen of the second reel with a phone showing the Instagram DM «QUIERO» → the reply, and «Comenta QUIERO».
v13 (the client: not the typing; the method guide «Método THUIS» as a mockup — three sheets, one straight and two
turned to the sides, so you see you get something real — and a «Black Friday, últimas plazas» tab).
  python3 tools/outro.py voz      the voice-over (ElevenLabs, voice VOICE) → .raw/outro/voz.mp3 + outro.json (word times)
  python3 tools/outro.py audio    the voice-over, a soft music bed and soft effects, mixed → assets/audio/outro.wav
The music bed («musica v1») and the effects come from ../reel-suarez-habla/.raw/outro and ../vsl-formacion-nawar
(tools/fetch_assets.sh copies them to .raw/outro).
The ElevenLabs key goes as a network secret (api.elevenlabs.io, header xi-api-key) or in ELEVENLABS_API_KEY.
"""
import base64, json, os, subprocess, sys, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, ".raw", "outro")
TEXT = ("Recibe el PDF de nuestro método y comienza a hablar neerlandés ya. Este Black Friday quedan las últimas plazas: "
        "comenta QUIERO y te lo enviamos por mensaje.")   # (v14: «el PDF», as on screen)
VOICE = "LP0ZBLgGaLqbDU1l9PDX"         # «Yair - Narration Spanish» (v7; v6 used «Nawar Def»)
MODEL = "eleven_v4"                    # (v7.2; eleven_multilingual_v2 before: it sounded flat)
SETTINGS = {"stability": 0.5, "similarity_boost": 0.8}
TEMPO = 1.1                            # (v10) the take played a touch quicker (pitch kept): light, never heavy


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
    out = [w for w in out if not (w["text"].startswith("[") and w["text"].endswith("]"))]     # the audio tags are not said
    return [{"text": w["text"], "t": round(w["t"], 3), "end": round(w["end"], 3)} for w in out]


def voz(take=None):
    """a new take (or, with a saved take's .mp3 + .json alignment, that one) → .raw/outro/voz.mp3 + outro.json."""
    os.makedirs(RAW, exist_ok=True)
    if take:
        import shutil
        shutil.copyfile(take + ".mp3", os.path.join(RAW, "voz.mp3")); al = json.load(open(take + ".json"))
    else:
        j = api(f"/text-to-speech/{VOICE}/with-timestamps?output_format=mp3_44100_192",
                {"text": TEXT, "model_id": MODEL, "voice_settings": SETTINGS})
        open(os.path.join(RAW, "voz.mp3"), "wb").write(base64.b64decode(j["audio_base64"]))
        al = j.get("alignment") or j["normalized_alignment"]
    ws = words_of(al)
    json.dump({"text": TEXT, "voice": VOICE, "model": MODEL, "settings": SETTINGS, "words": ws},
              open(os.path.join(ROOT, "outro.json"), "w"), ensure_ascii=False, indent=1)
    print(f"voz.mp3: {len(ws)} words, {ws[0]['t']:.2f}–{ws[-1]['end']:.2f} s")


VO_AT = 0.40                           # outro s: the voice-over starts (the ground is in at 0.25)
TAIL = 1.30                            # the end card holds this long after the last word
END = None                             # the outro's length: set from outro.json below (last word + TAIL)
VO_LUFS, BED_LUFS = -15.0, -35.0       # the voice a touch under the interview (−14.5), the bed 20 LU under the voice
BED_FROM = 0.023 + 8 * 4 * 60 / 107.7  # «musica v1» (the BF ad's track): from bar 8, where its light groove comes in
BED_AT, BED_IN, BED_OUT = 0.25, 0.6, 1.2
EQ = "highpass=f=110,lowshelf=f=150:g=-6,lowshelf=f=250:g=-6,equalizer=f=2500:t=q:w=0.9:g=-3"   # (as in the BF ad: room for the voice)
SR = 48000
LEAD = {"ping": 0.28}                  # ping.mp3 opens with 0.3 s of near-silence: trimmed, so it sounds with the pill
SFX = {"whoosh": ("whoosh.mp3", -9), "pop": ("pop.mp3", -19), "click": ("click.mp3", -14), "ping": ("ping.mp3", -15)}


def words():
    """the voice-over's words in outro time (s)."""
    vo = json.load(open(os.path.join(ROOT, "outro.json")))
    return [{"text": w["text"], "t": round(w["t"] / TEMPO + VO_AT, 3), "end": round(w["end"] / TEMPO + VO_AT, 3)} for w in vo["words"]]


if os.path.exists(os.path.join(ROOT, "outro.json")):
    END = round(words()[-1]["end"] + TAIL, 2)


def cues():
    """every timed moment of the outro (s), from the voice-over: the picture (tools/gen.py) and the sound effects
    (audio()) read the same ones."""
    ws = words()
    def at(text, k=0, end=False):
        hits = [w for w in ws if w["text"].strip(".,¡!¿?\"«»").lower() == text.lower()]
        return hits[k]["end" if end else "t"]
    c = dict(GROUND=0.0, TAB=0.20, L1=0.28, L2=0.38, PAGES=0.30, FAN=0.55, BAND=0.46, CTA=0.70,
             BF=at("black") - 0.08, QUIERO=at("quiero") - 0.04, SHINE=END - 1.2)
    return {k: round(v, 3) for k, v in c.items()}


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
    comp = f"atempo={TEMPO},acompressor=threshold=-20dB:ratio=2.5:attack=5:release=90:makeup=2"
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
    c = cues()                                                      # soft effects, under the voice: the whoosh on the cut
    for name, at in (("whoosh", 0.0), ("pop", c["FAN"] + 0.1), ("pop", c["BF"] + 0.05), ("click", c["QUIERO"] + 0.05)):
        f, db = SFX[name]                                           # the price seal landing, the tap on «Publicar», the
        fx = load(os.path.join(RAW, f)) * 10 ** (db / 20)           # message sent
        fx = fx[int(LEAD.get(name, 0) * SR):]                       # (its silence before the sound trimmed)
        a = int(round(at * SR)); m = min(len(fx), n - a); mix[a:a + m] += fx[:m]
    sf.write(tmp, mix, SR)
    peak = np.abs(mix).max()
    os.makedirs(os.path.join(ROOT, "assets", "audio"), exist_ok=True)
    out = os.path.join(ROOT, "assets", "audio", "outro.wav"); sf.write(out, mix, SR, subtype="PCM_24")
    print(f"outro.wav: {END} s, voice {VO_LUFS} LUFS from {VO_AT} s, bed {BED_LUFS} LUFS, peak {20 * np.log10(peak):.1f} dBFS")


if __name__ == "__main__":
    {"voz": lambda: voz(sys.argv[2] if len(sys.argv) > 2 else None), "audio": audio}[sys.argv[1]]()
