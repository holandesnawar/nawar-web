#!/usr/bin/env python3
"""The reel «Suárez habla neerlandés» (9:16, 25 fps), the second Luis Suárez reel:
- the interview full frame on his face (assets/video/habla-916.mp4, tools/frame.py: pushed in so his mouth sits above
  the subtitles);
- the hook, for the first seconds, at the top over his hair, in Instagram's own text look (white, bold, a soft shadow,
  with emoji): «Hablando neerlandés / 📚 sin miedo como 🇳🇱 / Luis Suárez»;
- the subtitles at the bottom: the Dutch phrase big, in capitals, one size for all, white with the word being said in
  yellow, and the Spanish under it, in a grey pill, all centred under his face;
- the closing ad (compositions/outro.html, from tools/outro.py's voice-over, book and sound): on Nawar blue, «Habla
  neerlandés sin miedo», the ebook «Holandés sin miedo» opening and turning its pages, «Black Friday · 1 €» and the call
  to action, a comment field typing «OFERTA».
  python3 tools/gen.py      → index.html, compositions/outro.html
"""
import html, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import outro as O  # noqa: E402

YEL = "#FFE11B"
SUB_BOTTOM = 1500                      # the subtitle block stands on this line (frame px): above Instagram's caption band
NL_W, NL_CX = 744, 540                 # centred, and left of its button rail (x > 912 from y ≈ 814)
NL_SIZE = 62                           # one size, two lines at most («|» in tools/subs.py breaks them)
ES_SIZE = 38
MIN_ON = 0.6                           # a phrase on screen for less than this opens a little early (after the last word
                                       # before it); one that stays long enough after its word (up to 0.7 s) does not
BRIDGE = 0.25                          # a gap shorter than this between two phrases is closed (no one-frame blink)
HOOK_TOP, HOOK_SIZE = 204, 70          # the hook: under Instagram's header, over his hair (his brows stay below y ≈ 500)
HOOK_OUT = 3.30                        # …and it leaves here (it is the cover too: on screen from the first frame)
HOOK = ["Hablando neerlandés", "{books} sin miedo como {nl}", "Luis Suárez"]
EMOJI = {"books": "\U0001F4DA", "nl": "\U0001F1F3\U0001F1F1"}     # 📚 🇳🇱, as pictures from Noto Color Emoji (assets/img)
EMOJI_FONT = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"
OUT_LEAD = 0.30                        # the closing ad's blue comes in over the interview's last 0.3 s


def outro_html(words):
    """compositions/outro.html: the closing ad, O.END s long; `words`: the voice-over's words (outro s)."""
    lib = json.load(open(os.path.join(ROOT, "assets", "video", "libro.json")))
    def at(text, k=0):
        hits = [w for w in words if w["text"].strip(".,").lower() == text.lower()]
        return hits[k]["t"]
    def end(text, k=0):
        hits = [w for w in words if w["text"].strip(".,").lower() == text.lower()]
        return hits[k]["end"]
    BW, BH = lib["width"], lib["height"]
    BOOK_TOP = 572
    c = dict(BL=540 - BW // 2, BT=BOOK_TOP, BW=BW, BH=BH, BS=lib["start"], BD=round(lib["end"] - lib["start"], 3), D=O.END,
             GROW0=round(lib["start"] + 0.6, 3), GROW=round(lib["play"] - lib["start"] - 0.6, 3))
    t = dict(L1=at("habla") - 0.05, L2=at("sin") - 0.06, PRICE=at("black") - 0.08, EURO=at("euro") - 0.04, DATE=end("euro") + 0.05,
             CTA=at("comenta") - 0.06, TYPE0=at("oferta") - 0.02, TYPE1=end("oferta") - 0.10, SEND=end("oferta") + 0.05,
             CAP=at("y") - 0.04, PULSE=O.END - 1.0)
    css = """
    #o-root { position: absolute; inset: 0; overflow: hidden; font-family: "Poppins", sans-serif; }
    .o-full { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; overflow: hidden; }
    .o-blue { background: radial-gradient(circle at 50% 36%, #025dc7 0%, #120081 72%); }
    .o-dots { position: absolute; left: -30px; top: -30px; width: 1140px; height: 1980px;
      background-image: radial-gradient(circle, rgba(255,255,255,0.07) 1.7px, transparent 1.9px); background-size: 30px 30px; }
    .o-amb { position: absolute; left: 40px; top: 380px; width: 1000px; height: 980px; border-radius: 50%;
      background: radial-gradient(ellipse at 50% 50%, rgba(77,163,255,0.22) 0%, rgba(77,163,255,0.07) 45%, rgba(77,163,255,0) 70%); }
    .o-vig { position: absolute; inset: 0; background: radial-gradient(ellipse 85% 70% at 50% 40%, rgba(4,0,40,0) 55%, rgba(4,0,40,0.40) 100%); }
    .o-row { position: absolute; left: 0; width: 1080px; display: flex; justify-content: center; align-items: center; }
    #o-l1 { top: 222px; font-weight: 800; font-size: 86px; line-height: 1.04; letter-spacing: -0.03em; color: #FFFFFF; white-space: nowrap; }
    #o-l2 { top: 322px; }
    .o-chip { display: inline-block; padding: 2px 26px 10px; border-radius: 22px; background: #FFFFFF; color: #1D0084;
      font-weight: 800; font-size: 86px; line-height: 1.04; letter-spacing: -0.03em; white-space: nowrap; }
    #o-book { position: absolute; left: «BL»px; top: «BT»px; width: «BW»px; height: «BH»px; }
    #o-book video { position: absolute; left: 0; top: 0; width: «BW»px; height: «BH»px; display: block; }
    #o-price { top: 446px; }
    .o-ypill { display: flex; align-items: center; gap: 18px; height: 80px; padding: 0 36px; border-radius: 999px; background: #FFD60A;
      color: #08070F; white-space: nowrap; font-weight: 800; font-size: 40px; line-height: 1; letter-spacing: -0.005em; }
    .o-ypill i { display: block; width: 10px; height: 10px; border-radius: 50%; background: #08070F; }
    #o-eur { display: inline-block; font-weight: 800; transform-origin: 50% 55%; }
    #o-date { top: 534px; font-family: "Inter", sans-serif; font-weight: 600; font-size: 29px; line-height: 1; color: rgba(255,255,255,0.88);
      letter-spacing: 0.005em; }
    #o-cta { top: 1290px; }
    .o-field { display: flex; align-items: center; gap: 18px; width: 720px; height: 92px; padding: 0 22px 0 26px; border-radius: 999px;
      background: #FFFFFF; white-space: nowrap; }
    .o-field .o-ic { display: block; width: 46px; height: 46px; flex: 0 0 46px; }
    .o-field .o-lab { font-family: "Inter", sans-serif; font-weight: 600; font-size: 34px; color: #5A6480; line-height: 1; }
    #o-typed { font-weight: 800; font-size: 40px; color: #1D0084; line-height: 1; letter-spacing: 0.01em; }
    #o-caret { display: block; width: 4px; height: 44px; border-radius: 2px; background: #0b6df0; margin-left: -12px; }
    .o-field .o-fill { flex: 1 1 auto; }
    #o-send { display: block; width: 58px; height: 58px; flex: 0 0 58px; transform-origin: 50% 50%; }
    #o-cap { top: 1404px; font-family: "Inter", sans-serif; font-weight: 600; font-size: 33px; line-height: 1; color: #FFFFFF; }
"""
    bubble = ('<svg class="o-ic" viewBox="0 0 48 48"><path d="M24 7 C13.5 7 6 13.9 6 22.3 c0 4.5 2.2 8.6 5.8 11.4 L10 41 l8.3 -4.2 '
              'c1.8 0.5 3.7 0.8 5.7 0.8 c10.5 0 18 -6.9 18 -15.3 S34.5 7 24 7 z" fill="none" stroke="#1D0084" stroke-width="4" stroke-linejoin="round"/></svg>')
    send = ('<svg id="o-send" viewBox="0 0 58 58"><circle cx="29" cy="29" r="29" fill="#0b6df0"/>'
            '<path d="M17 28.5 L41 18 L33.5 41 L28.6 31.2 Z" fill="#FFFFFF" stroke="#FFFFFF" stroke-width="2.4" stroke-linejoin="round"/>'
            '<path d="M28.6 31.2 L41 18" stroke="#0b6df0" stroke-width="2.4" stroke-linecap="round"/></svg>')
    body = f"""
    <div id="o-ground" class="o-full o-blue"><div class="o-dots"></div><div class="o-amb"></div><div class="o-vig"></div></div>
    <div id="o-book"><video id="o-v" class="clip" src="assets/video/libro.webm" muted playsinline data-start="«BS»" data-duration="«BD»" data-track-index="1"></video></div>
    <div id="o-l1" class="o-row">Habla neerlandés</div>
    <div id="o-l2" class="o-row"><span class="o-chip">sin miedo</span></div>
    <div id="o-price" class="o-row"><div class="o-ypill"><span>Black Friday</span><i></i><span>por solo <span id="o-eur">1&nbsp;€</span></span></div></div>
    <div id="o-date" class="o-row">hasta el 30 de noviembre</div>
    <div id="o-cta" class="o-row"><div class="o-field">{bubble}<span class="o-lab">Comenta</span><span id="o-typed"></span><span id="o-caret"></span><span class="o-fill"></span>{send}</div></div>
    <div id="o-cap" class="o-row">y te enviamos los detalles</div>
"""
    js = """
      tl.fromTo("#o-ground", { opacity: 0 }, { opacity: 1, duration: 0.30, ease: "power2.out" }, 0);
      tl.fromTo("#o-book", { opacity: 0, y: 40, scale: 0.93 }, { opacity: 1, y: 0, scale: 0.97, duration: 0.6, ease: "power3.out" }, «BS»);
      // (closed, it is not still: it grows slowly to its size, reached just as it opens)
      tl.to("#o-book", { scale: 1, duration: «GROW», ease: "sine.inOut" }, «GROW0»);
      tl.fromTo("#o-l1", { opacity: 0, y: 26 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, «L1»);
      tl.fromTo("#o-l2 .o-chip", { opacity: 0, scale: 0.88 }, { opacity: 1, scale: 1, duration: 0.42, ease: "back.out(1.5)" }, «L2»);
      tl.fromTo("#o-price", { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.40, ease: "power3.out" }, «PRICE»);
      tl.fromTo("#o-eur", { scale: 1 }, { scale: 1.16, duration: 0.16, ease: "power2.out", yoyo: true, repeat: 1 }, «EURO»);
      tl.fromTo("#o-date", { opacity: 0, y: 10 }, { opacity: 1, y: 0, duration: 0.35, ease: "power2.out" }, «DATE»);
      tl.fromTo("#o-cta", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, «CTA»);
      tl.fromTo("#o-cap", { opacity: 0, y: 10 }, { opacity: 1, y: 0, duration: 0.35, ease: "power2.out" }, «CAP»);
      tl.fromTo("#o-send", { scale: 1 }, { scale: 1.18, duration: 0.14, ease: "power2.out", yoyo: true, repeat: 1 }, «SEND»);
      tl.fromTo("#o-cta .o-field", { scale: 1 }, { scale: 1.04, duration: 0.22, ease: "sine.inOut", yoyo: true, repeat: 1 }, «PULSE»);
      (() => {                                               // «OFERTA» typed letter by letter (one state per letter: seek-safe)
        const el = document.getElementById("o-typed"), full = "OFERTA", typ = { n: 0 };
        el.textContent = "";
        tl.fromTo(typ, { n: 0 }, { n: full.length, duration: «TYPEDUR», ease: "none", immediateRender: false,
          onUpdate: () => { el.textContent = full.slice(0, Math.round(typ.n)); } }, «TYPE0»);
      })();
"""
    blink, k = [], t["CTA"]                                  # the caret blinks while waiting, steady while typing, then goes
    on = True
    while k < t["TYPE0"]:
        blink.append(f'      tl.set("#o-caret", {{ opacity: {1 if on else 0} }}, {k:.3f});'); k += 0.25; on = not on
    blink.append(f'      tl.set("#o-caret", {{ opacity: 1 }}, {t["TYPE0"]:.3f});')
    blink.append(f'      tl.set("#o-caret", {{ opacity: 0 }}, {t["SEND"]:.3f});')
    vals = {**c, **{k: round(v, 3) for k, v in t.items()}, "TYPEDUR": round(t["TYPE1"] - t["TYPE0"], 3)}
    def sub(s):
        for k, v in vals.items():
            s = s.replace(f"«{k}»", str(v))
        return s
    fonts = "\n".join(f'    @font-face {{ font-family: "{f}"; font-weight: {w}; src: url("assets/fonts/{f.lower()}-latin-{w}-normal.woff2") format("woff2"); }}'
                      for f, w in (("Poppins", 700), ("Poppins", 800), ("Poppins", 900), ("Inter", 600), ("Inter", 700)))
    page = f"""<template>
  <script src="assets/vendor/gsap.min.js"></script>
  <style>
{fonts}
{sub(css)}
  </style>
  <div id="o-root" data-composition-id="outro" data-width="1080" data-height="1920" data-duration="{O.END}">
{sub(body)}
  </div>
  <script>
    (function () {{
      const tl = gsap.timeline({{ paused: true }});
{sub(js)}
{chr(10).join(blink)}
      window.__timelines["outro"] = tl;
    }})();
  </script>
</template>
"""
    os.makedirs(os.path.join(ROOT, "compositions"), exist_ok=True)
    open(os.path.join(ROOT, "compositions", "outro.html"), "w").write(page)
    return t


def emoji():
    """the hook's emoji as PNGs (Noto Color Emoji's own bitmaps, 109 px), so the render needs no emoji font."""
    from PIL import Image, ImageDraw, ImageFont
    f = None
    for name, ch in EMOJI.items():
        path = os.path.join(ROOT, "assets", "img", f"emoji-{name}.png")
        if os.path.exists(path):
            continue
        f = f or ImageFont.truetype(EMOJI_FONT, 109)
        im = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((10, 10), ch, font=f, embedded_color=True)
        os.makedirs(os.path.dirname(path), exist_ok=True); im.crop(im.getbbox()).save(path)


def main():
    emoji()
    meta = json.load(open(os.path.join(ROOT, "assets", "video", "habla-916.json")))
    D = meta["duration"]
    OUT0 = round(D - OUT_LEAD, 3)
    TOTAL = round(OUT0 + O.END, 3)
    subs = json.load(open(os.path.join(ROOT, "subs.json")))["phrases"]
    vo = json.load(open(os.path.join(ROOT, "outro.json")))
    words = [{"text": w["text"], "t": round(w["t"] + O.VO_AT, 3), "end": round(w["end"] + O.VO_AT, 3)} for w in vo["words"]]
    cues = outro_html(words)
    body, js = [], []
    cuts = [s["reel"] for s in meta["segments"][1:]]          # the hard cuts between the moments: no phrase crosses one
    ons = []
    for k, p in enumerate(subs):
        words_k = p["words"]
        on = max(0.0, words_k[0]["t"] - 0.05)
        nxt = subs[k + 1]["words"][0]["t"] - 0.05 if k + 1 < len(subs) else D
        if min(nxt, words_k[-1]["end"] + 0.7) - on < MIN_ON and k:
            on = max(subs[k - 1]["words"][-1]["end"] + 0.03, min(on, words_k[-1]["end"] - MIN_ON))
        on = max([on] + [c for c in cuts if c <= words_k[0]["t"]])
        ons.append(on)
    for k, p in enumerate(subs):
        words_k = p["words"]
        on = ons[k]
        off = min(ons[k + 1], words_k[-1]["end"] + 0.7) if k + 1 < len(subs) else D
        if k + 1 < len(subs) and ons[k + 1] - off < BRIDGE:
            off = ons[k + 1]
        off = min([off] + [c for c in cuts if c > on])
        spans = " ".join(('<span class="br"></span> ' if i in p.get("breaks", []) else "") +
                         f'<span id="w{k}-{i}" class="w">{html.escape(w["text"])}</span>' for i, w in enumerate(words_k))
        body.append(f'      <div id="p{k}" class="ph"><div class="nl">{spans}</div>'
                    f'<div class="es"><span>{html.escape(p["es"]).replace("|", "<br>")}</span></div></div>')
        js.append(f'      tl.set("#p{k}", {{ opacity: 1 }}, {on:.3f});')
        js.append(f'      tl.fromTo("#p{k} .nl", {{ scale: 0.86 }}, {{ scale: 1, duration: 0.16, ease: "back.out(1.6)", immediateRender: false }}, {on:.3f});')
        js.append(f'      tl.set("#p{k}", {{ opacity: 0 }}, {off:.3f});')
        for i, w in enumerate(words_k):
            t1 = words_k[i + 1]["t"] - 0.03 if i + 1 < len(words_k) else off
            js.append(f'      tl.set("#w{k}-{i}", {{ color: "{YEL}" }}, {max(on, w["t"] - 0.03):.3f});')
            if i + 1 < len(words_k):
                js.append(f'      tl.set("#w{k}-{i}", {{ color: "#FFFFFF" }}, {t1:.3f});')
    fonts = "\n".join(f'      @font-face {{ font-family: "{f}"; font-weight: {w}; src: url("assets/fonts/{f.lower()}-latin-{w}-normal.woff2") format("woff2"); }}'
                      for f, w in (("Poppins", 700), ("Poppins", 900), ("Inter", 600), ("Inter", 700)))
    hook = "".join(f'<div class="hl">' + html.escape(l).format(**{k: f'<img class="em em-{k}" src="assets/img/emoji-{k}.png" alt="">' for k in EMOJI})
                   + '</div>' for l in HOOK)
    page = f"""<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
{fonts}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #000; }}
      #root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #000; }}
      #v {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }}
      .shade {{ position: absolute; left: 0; width: 1080px; pointer-events: none; }}
      /* soft shades: at the bottom under the subtitles; at the top under the hook (it goes with it) */
      #shade-bot {{ top: 1180px; height: 740px; background: linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(0,0,0,0.26) 45%, rgba(0,0,0,0.34) 100%); }}
      #shade-top {{ top: 0; height: 560px; background: linear-gradient(180deg, rgba(0,0,0,0.30) 0%, rgba(0,0,0,0.16) 55%, rgba(0,0,0,0) 100%); }}
      /* the hook: Instagram's own text look (bold sans, white, a soft shadow, colour emoji) */
      #hook {{ position: absolute; left: 0; top: {HOOK_TOP}px; width: 1080px; text-align: center; color: #FFFFFF;
        font-family: "Inter", sans-serif; font-weight: 700; font-size: {HOOK_SIZE}px; line-height: 1.12;
        letter-spacing: -0.012em; text-shadow: 0 2px 3px rgba(0,0,0,0.45), 0 4px 22px rgba(0,0,0,0.35); }}
      #hook .em {{ display: inline-block; vertical-align: -0.14em; filter: drop-shadow(0 2px 3px rgba(0,0,0,0.35)); }}
      #hook .em-books {{ height: 1.0em; }}
      #hook .em-nl {{ height: 0.80em; vertical-align: -0.06em; }}
      .ph {{ position: absolute; left: {NL_CX - 505}px; bottom: {1920 - SUB_BOTTOM}px; width: 1010px; display: flex; flex-direction: column;
        align-items: center; gap: 6px; opacity: 0; }}
      .nl {{ width: {NL_W}px; font-size: {NL_SIZE}px; display: flex; flex-wrap: wrap; justify-content: center; column-gap: 0.26em; row-gap: 0;
        font-family: "Poppins", sans-serif; font-weight: 900; line-height: 1.02; text-transform: uppercase; letter-spacing: -0.01em;
        color: #FFFFFF; -webkit-text-stroke: 10px #000; paint-order: stroke fill; text-shadow: 0 6px 16px rgba(0,0,0,0.5);
        transform-origin: 50% 60%; }}
      .w {{ display: inline-block; color: #FFFFFF; }}
      .br {{ flex-basis: 100%; height: 0; }}
      .es span {{ display: inline-block; max-width: {NL_W}px; padding: 8px 24px 10px; border-radius: 18px; text-align: center;
        background: rgba(78,78,84,0.78); color: #FFFFFF; font-family: "Poppins", sans-serif; font-weight: 700; font-size: {ES_SIZE}px;
        line-height: 1.2; letter-spacing: -0.005em; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-width="1080" data-height="1920" data-duration="{TOTAL}" data-fps="25">
      <video id="v" class="clip" src="assets/video/habla-916.mp4" data-start="0" data-duration="{D}" data-track-index="0" playsinline data-has-audio="true"></video>
      <div id="shade-bot" class="shade"></div>
      <div id="shade-top" class="shade"></div>
      <div id="hook">{hook}</div>
{chr(10).join(body)}
      <div id="outro" data-composition-id="outro" data-composition-src="compositions/outro.html" data-start="{OUT0}" data-duration="{O.END}" data-track-index="2" data-width="1080" data-height="1920"></div>
      <audio id="a-outro" src="assets/audio/outro.wav" data-start="{OUT0}" data-duration="{O.END}" data-track-index="3"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      // the hook: on screen from the first frame (it is the cover), it leaves at {HOOK_OUT} s with its shade
      tl.to(["#hook", "#shade-top"], {{ opacity: 0, y: -10, duration: 0.35, ease: "power2.in" }}, {HOOK_OUT});
{chr(10).join(js)}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
    open(os.path.join(ROOT, "index.html"), "w").write(page)
    print(f"index.html: {TOTAL}s (the interview {D}s, the closing ad from {OUT0}s), {len(subs)} subtitle phrases; outro cues "
          + ", ".join(f"{k} {v:.2f}" for k, v in cues.items()))


if __name__ == "__main__":
    main()
