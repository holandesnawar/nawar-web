#!/usr/bin/env python3
"""index.html: the reel «Aprendiendo neerlandés con Luis Suárez» (9:16, 25 fps), v7 — in the design of the second reel's
final version (../reel-suarez-habla, v7.6):
- the ad full frame (assets/video/suarez-916.mp4, tools/frame.py);
- the hook for the first seconds, in the client's design: «Aprendiendo / neerlandés con / Luis Suárez» in Inter
  ExtraBold, white with a thick round black outline, the 📚 and 🇳🇱 icons (tools/img) on either side of the middle line.
  It sits over the chest (the faces are at the top in the first shots: Suárez's, then the assistant's down to y ≈ 890);
- the subtitles at the bottom: the Dutch phrase big, in capitals, white with the word being said in yellow, the Spanish
  under it in a grey pill (raised onto the nose in Suárez's extreme close-ups, so his lips stay in sight);
- the closing ad of the second reel (its compositions/outro.html, voice, book and sound, copied from ../reel-suarez-habla:
  «Habla neerlandés sin miedo, como Luis Suárez… Comenta OFERTA»), over the ad's last 0.3 s.
  python3 tools/gen.py
"""
import html, json, os, re, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HABLA = os.path.join(ROOT, "..", "reel-suarez-habla")
YEL = "#FFE11B"
SUB_BOTTOM = 1500                 # the subtitle block stands on this line (frame px), as in the second reel
NL_W, NL_CX = 744, 540
NL_SIZE, ES_SIZE = 62, 38
HOOK_TOP, HOOK_SIZE, HOOK_LH = 920, 77, 1.06   # over the chest, under the assistant's lips (y ≈ 890), clear of the subtitles
HOOK_OUTLINE = 6
HOOK_OUT = 3.30                   # on screen from the first frame (the cover), it leaves here
HOOK = ["Aprendiendo", "neerlandés con", "Luis Suárez"]
ICONS = {"books": 108, "nl": 88}
ICON_DY = {"books": 22, "nl": 9}
ICON_GAP = 18
OUT_LEAD = 0.30                   # the closing ad comes in over the ad's last 0.3 s
UP = [(7.96, 9.60), (16.64, 20.52), (26.04, 27.80)]       # Suárez's extreme close-ups: the subtitles sit higher, on his
UP_DY = -440                      # nose (block bottom ≈ 1060), so his lips stay in sight; the bottom shade is off there
MIN_ON = 0.6                      # a one-word phrase opens a little early (after the last word before it) to be read
ON_AT = {11: 16.64, 18: 26.04,    # these open on the cut into Suárez's close-up (the phrase before closes there: no
         22: 32.40, 23: 33.00}    # block over his lips for a frame, no jump mid-shot); «Kaartje?» on the cut to the card
OFF_AT = {18: 27.80}              # …and this one closes on the cut out of it (the dip to black)


def outline_shadow(r, color="#000"):
    """a round outline of r px around the text: the glyph shifted to every direction on two rings (text-shadow)."""
    import math
    out = []
    for rr, n in ((r, 32), (r * 0.55, 16)):
        for k in range(n):
            a = 2 * math.pi * k / n
            out.append(f"{rr * math.cos(a):.2f}px {rr * math.sin(a):.2f}px 0 {color}")
    return ", ".join(out)


def segments(on, off):
    """the y offset of a phrase over its time on screen: UP_DY inside Suárez's close-ups. It changes only on a cut, and never for a bit shorter than 0.4 s (that bit takes its neighbour's place)."""
    base = 0
    cuts = sorted({c for ab in UP for c in ab if on < c < off})
    edges = [on] + cuts + [off]
    segs = [[edges[i], edges[i + 1], UP_DY if any(a <= (edges[i] + edges[i + 1]) / 2 < b for a, b in UP) else base]
            for i in range(len(edges) - 1)]
    while len(segs) > 1:
        i = min(range(len(segs)), key=lambda j: segs[j][1] - segs[j][0])
        if segs[i][1] - segs[i][0] >= 0.4:
            break
        j = i - 1 if i == len(segs) - 1 or (i > 0 and segs[i - 1][1] - segs[i - 1][0] >= segs[i + 1][1] - segs[i + 1][0]) else i + 1
        a, b = sorted((i, j))
        keep = segs[j][2]
        segs[a:b + 1] = [[segs[a][0], segs[b][1], keep]]
    return segs


def main():
    meta = json.load(open(os.path.join(ROOT, "assets", "video", "suarez-916.json")))
    D = meta["duration"]
    # the closing ad: built in the second reel (its tools/gen.py and tools/outro.py), copied as it is
    shutil.copyfile(os.path.join(HABLA, "compositions", "outro.html"), os.path.join(ROOT, "compositions", "outro.html"))
    for f in ("audio/outro.wav", "video/libro.webm", "video/libro.json"):
        os.makedirs(os.path.dirname(os.path.join(ROOT, "assets", f)), exist_ok=True)
        shutil.copyfile(os.path.join(HABLA, "assets", f), os.path.join(ROOT, "assets", f))
    os.makedirs(os.path.join(ROOT, "assets", "img"), exist_ok=True)
    for k in ICONS:
        shutil.copyfile(os.path.join(ROOT, "tools", "img", f"emoji-{k}.png"), os.path.join(ROOT, "assets", "img", f"emoji-{k}.png"))
    OEND = float(re.search(r'data-composition-id="outro"[^>]*data-duration="([\d.]+)"', open(os.path.join(ROOT, "compositions", "outro.html")).read()).group(1))
    OUT0 = round(D - OUT_LEAD, 3)
    TOTAL = round(OUT0 + OEND, 3)
    subs = json.load(open(os.path.join(ROOT, "subs.json")))["phrases"]
    body, js = [], []
    ons = []
    for k, p in enumerate(subs):
        words = p["words"]
        on = max(0.0, words[0]["t"] - 0.05)
        if words[-1]["end"] - on < MIN_ON and k:                   # short: open early, after the phrase before it is said
            on = max(subs[k - 1]["words"][-1]["end"] + 0.03, min(on, words[-1]["end"] - MIN_ON))
        ons.append(ON_AT.get(k, on))
    for k, p in enumerate(subs):
        words = p["words"]
        on = ons[k]
        off = OFF_AT.get(k, min(ons[k + 1], words[-1]["end"] + 0.7) if k + 1 < len(subs) else D)
        spans = " ".join(('<span class="br"></span> ' if i in p.get("breaks", []) else "") +
                         f'<span id="w{k}-{i}" class="w">{html.escape(w["text"])}</span>' for i, w in enumerate(words))
        body.append(f'      <div id="p{k}" class="ph"><div class="nl">{spans}</div>'
                    f'<div class="es"><span>{html.escape(p["es"]).replace("|", "<br>")}</span></div></div>')
        for a, b, dy in segments(on, off):
            js.append(f'      tl.set("#p{k}", {{ y: {dy} }}, {a:.3f});')
        js.append(f'      tl.set("#p{k}", {{ opacity: 1 }}, {on:.3f});')
        js.append(f'      tl.fromTo("#p{k} .nl", {{ scale: 0.86 }}, {{ scale: 1, duration: 0.16, ease: "back.out(1.6)", immediateRender: false }}, {on:.3f});')
        js.append(f'      tl.set("#p{k}", {{ opacity: 0 }}, {off:.3f});')
        for i, w in enumerate(words):
            t1 = words[i + 1]["t"] - 0.03 if i + 1 < len(words) else off
            js.append(f'      tl.set("#w{k}-{i}", {{ color: "{YEL}" }}, {max(on, w["t"] - 0.03):.3f});')
            if i + 1 < len(words):
                js.append(f'      tl.set("#w{k}-{i}", {{ color: "#FFFFFF" }}, {t1:.3f});')
    fonts = "\n".join([f'      @font-face {{ font-family: "{f}"; font-weight: {w}; src: url("assets/fonts/{f.lower()}-latin-{w}-normal.woff2") format("woff2"); }}'
                       for f, w in (("Poppins", 700), ("Poppins", 900), ("Inter", 600), ("Inter", 700))] +
                      ['      @font-face { font-family: "InterV"; font-weight: 100 900; src: url("assets/fonts/inter-var-latin.woff2") format("woff2"); }'])
    icons = {k: f'<img class="em em-{k}" src="assets/img/emoji-{k}.png" alt="">' for k in ICONS}
    hook = (f'<div class="hl"><span>{html.escape(HOOK[0])}</span></div>'
            f'<div class="hl"><span class="mid">{icons["books"]}{html.escape(HOOK[1])}{icons["nl"]}</span></div>'
            f'<div class="hl"><span>{html.escape(HOOK[2])}</span></div>')
    shade = "\n".join(f'      tl.set("#shade-bot", {{ opacity: 0 }}, {a:.2f});\n      tl.set("#shade-bot", {{ opacity: 1 }}, {b:.2f});' for a, b in UP)
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
      /* a soft shade at the bottom, under the subtitles */
      #shade-bot {{ top: 1180px; height: 740px; background: linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(0,0,0,0.26) 45%, rgba(0,0,0,0.34) 100%); }}
      /* the hook: the client's design — Inter ExtraBold, white, a thick round black outline, the icons on the middle line */
      #hook {{ position: absolute; left: 0; top: {HOOK_TOP}px; width: 1080px; text-align: center; color: #FFFFFF;
        font-family: "InterV", sans-serif; font-weight: 800; font-size: {HOOK_SIZE}px; line-height: {HOOK_LH}; letter-spacing: -0.012em;
        text-shadow: {outline_shadow(HOOK_OUTLINE)}; transform-origin: 50% 40%; }}
      #hook .hl {{ white-space: nowrap; }}
      #hook .mid {{ position: relative; display: inline-block; }}
      #hook .em {{ position: absolute; top: 50%; display: block; }}
      #hook .em-books {{ height: {ICONS["books"]}px; top: calc(50% + {ICON_DY["books"]}px); right: calc(100% + {ICON_GAP + HOOK_OUTLINE}px); transform: translateY(-50%); }}
      #hook .em-nl {{ height: {ICONS["nl"]}px; top: calc(50% + {ICON_DY["nl"]}px); left: calc(100% + {ICON_GAP + HOOK_OUTLINE}px); transform: translateY(-50%); }}
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
      <video id="v" class="clip" src="assets/video/suarez-916.mp4" data-start="0" data-duration="{D}" data-track-index="0" playsinline data-has-audio="true"></video>
      <div id="shade-bot" class="shade"></div>
      <div id="hook">{hook}</div>
{chr(10).join(body)}
      <div id="outro" data-composition-id="outro" data-composition-src="compositions/outro.html" data-start="{OUT0}" data-duration="{OEND}" data-track-index="2" data-width="1080" data-height="1920"></div>
      <audio id="a-outro" src="assets/audio/outro.wav" data-start="{OUT0}" data-duration="{OEND}" data-track-index="3"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      // the hook: on screen from the first frame (it is the cover), it leaves at {HOOK_OUT} s
      tl.to("#hook", {{ opacity: 0, scale: 0.96, duration: 0.30, ease: "power2.in" }}, {HOOK_OUT});
      // the bottom shade is off in Suárez's extreme close-ups (it would darken his lips)
{shade}
{chr(10).join(js)}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
    open(os.path.join(ROOT, "index.html"), "w").write(page)
    print(f"index.html: {TOTAL}s (the ad {D}s, the closing ad from {OUT0}s), {len(subs)} subtitle phrases")


if __name__ == "__main__":
    main()
