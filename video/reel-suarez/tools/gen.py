#!/usr/bin/env python3
"""index.html: the reel «Aprendiendo neerlandés con Luis Suárez» (9:16, 25 fps) in the look of the Mario Casas reel
(Drive: «Estrategia de contenido para reels»): the ad full frame (assets/video/suarez-916.mp4, tools/frame.py), the
title as a frosted white card over the chest for the first 3 s (the hook and the cover: «APRENDIENDO NEERLANDÉS · con
Luis Suárez», a round Dutch flag), then a small frosted pill at the top that steps out of the close-ups (v4: the
labels of the second reel, ../reel-suarez-habla), and under the faces the subtitles: the
Dutch phrase big, in capitals, one size for all, white with the word being said in yellow, and the Spanish under it,
in a grey pill (a little higher in Suárez's close-ups, so his lips show).
  python3 tools/gen.py
"""
import html, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
YEL = "#FFE11B"
NL_TOP, NL_W, NL_CX = 1110, 830, 490   # the Dutch block (frame px): clear of Instagram's button rail (x > 930, with a
NL_SIZE = 76                      # margin for the pop-in) and of its caption band at the bottom; one size for every
                                  # phrase, which wraps onto two lines at most (tools/subs.py keeps them that short)
TITLE_TOP = 918                   # the title card over the chest for the first seconds, under the assistant's mouth (his
TITLE_DY = 50                     # lips reach y ≈ 890): the cover stays clear; the subtitles that open under it sit 50 px lower
TAG_AT = 3.0                      # the big title (the hook and the cover) lifts away here…
TAG_IN = 5.10                     # …and the small pill settles at the top once the assistant's head is down (5.04)
TAG_OFF = [(7.96, 10.52), (14.40, 30.28)]  # the close-ups (Suárez's, and the assistant's: he leans in up to 10.52 and is
                                  # close from the cut at 14.40) and Suárez's wide tilt-up (to 30.28): eyes at the top
UP = [(7.96, 9.60), (16.64, 20.52), (26.04, 27.80)]       # Suárez's extreme close-ups: the subtitles sit higher, on his
UP_DY = -300                      # nose, so his lips stay in sight (eyes ≤ 620, lips ≥ 1000; the block moves on the cuts only,
                                  # and the bottom shade is off there: it would darken his lips)
MIN_ON = 0.6                      # a one-word phrase opens a little early (after the last word before it) to be read
ON_AT = {11: 16.64, 18: 26.04,    # these open on the cut into Suárez's close-up (the phrase before closes there: no
         22: 32.40, 23: 33.00}    # block over his lips for a frame, no jump mid-shot); «Kaartje?» on the cut to the card
OFF_AT = {18: 27.80}              # …and this one closes on the cut out of it (the dip to black)

FLAG = ('<svg viewBox="0 0 48 48" aria-hidden="true"><defs><clipPath id="{id}"><circle cx="24" cy="24" r="24"/></clipPath></defs>'
        '<g clip-path="url(#{id})"><rect width="48" height="16" fill="#AE1C28"/><rect y="16" width="48" height="16" fill="#FFFFFF"/>'
        '<rect y="32" width="48" height="16" fill="#21468B"/></g><circle cx="24" cy="24" r="23" fill="none" stroke="rgba(0,0,0,0.22)" stroke-width="2"/></svg>')
# the labels (v4): frosted white, like iOS — the same as the second reel (../reel-suarez-habla)
LABEL_CSS = """
      .glass { background: rgba(255,255,255,0.80); -webkit-backdrop-filter: blur(28px) saturate(180%); backdrop-filter: blur(28px) saturate(180%);
        box-shadow: 0 1px 0 rgba(255,255,255,0.9) inset, 0 18px 50px rgba(0,0,0,0.22), 0 2px 8px rgba(0,0,0,0.10); color: #1D1D1F;
        font-family: "Inter", sans-serif; }
      .row { position: absolute; left: 0; width: 1080px; display: flex; justify-content: center; }
      #card { display: flex; flex-direction: column; align-items: center; gap: 2px; padding: 22px 48px 26px; border-radius: 44px; white-space: nowrap; }
      #card .kick { display: flex; align-items: center; gap: 14px; font-weight: 700; font-size: 44px; letter-spacing: -0.015em;
        color: #1D0084; line-height: 1.1; }
      #card .kick svg { width: 46px; height: 46px; display: block; }
      #card .big { font-weight: 700; font-size: 80px; letter-spacing: -0.03em; line-height: 1.02; }
      #tag { display: flex; align-items: center; gap: 12px; padding: 10px 28px 10px 12px; border-radius: 999px; white-space: nowrap; opacity: 0;
        font-weight: 600; font-size: 32px; letter-spacing: -0.01em; line-height: 1; }
      #tag svg { width: 40px; height: 40px; display: block; }
"""


def segments(on, off):
    """the y offset of a phrase over its time on screen: UP_DY inside Suárez's close-ups, TITLE_DY if it opens under the
    title card. It changes only on a cut, and never for a bit shorter than 0.4 s (that bit takes its neighbour's place)."""
    base = TITLE_DY if on < TAG_AT else 0
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
    # a phrase still under the card's offset when the card lifts away glides up with it (no jump later, mid-shot)
    glide = "\n".join(f'      tl.to("#p{k}", {{ y: 0, duration: 0.32, ease: "power2.inOut" }}, {TAG_AT});'
                      for k in range(len(subs)) if ons[k] < TAG_AT < (min(ons[k + 1], subs[k]["words"][-1]["end"] + 0.7) if k + 1 < len(subs) else D))
    fonts = "\n".join(f'      @font-face {{ font-family: "{f}"; font-weight: {w}; src: url("assets/fonts/{f.lower()}-latin-{w}-normal.woff2") format("woff2"); }}'
                      for f, w in (("Poppins", 700), ("Poppins", 900), ("Inter", 600), ("Inter", 700)))
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
      #shade-top {{ top: 0; height: 700px; opacity: 0.55; background: linear-gradient(180deg, rgba(0,0,0,0.42) 0%, rgba(0,0,0,0.18) 55%, rgba(0,0,0,0) 100%); }}
      #shade-bot {{ top: 1020px; height: 560px; background: linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(0,0,0,0.30) 45%, rgba(0,0,0,0.30) 75%, rgba(0,0,0,0) 100%); }}
{LABEL_CSS}
      .ph {{ position: absolute; left: {NL_CX - 505}px; top: {NL_TOP}px; width: 1010px; display: flex; flex-direction: column; align-items: center;
        gap: 12px; opacity: 0; }}
      .nl {{ width: {NL_W}px; font-size: {NL_SIZE}px; display: flex; flex-wrap: wrap; justify-content: center; column-gap: 0.26em; row-gap: 0;
        font-family: "Poppins", sans-serif; font-weight: 900; line-height: 1.02; text-transform: uppercase; letter-spacing: -0.01em;
        color: #FFFFFF; -webkit-text-stroke: 10px #000; paint-order: stroke fill; text-shadow: 0 6px 16px rgba(0,0,0,0.5);
        transform-origin: 50% 60%; }}
      .w {{ display: inline-block; color: #FFFFFF; }}
      .br {{ flex-basis: 100%; height: 0; }}
      .es span {{ display: inline-block; max-width: {NL_W}px; padding: 10px 22px 12px; border-radius: 18px; text-align: center;
        background: rgba(78,78,84,0.78); color: #FFFFFF; font-family: "Poppins", sans-serif; font-weight: 700; font-size: 46px;
        line-height: 1.2; letter-spacing: -0.005em; text-wrap: balance; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-width="1080" data-height="1920" data-duration="{D}" data-fps="25">
      <video id="v" class="clip" src="assets/video/suarez-916.mp4" data-start="0" data-duration="{D}" data-track-index="0" playsinline data-has-audio="true"></video>
      <div id="shade-top" class="shade"></div>
      <div id="shade-bot" class="shade"></div>
      <div class="row" style="top: {TITLE_TOP}px; left: {NL_CX - 540}px"><div id="card" class="glass"><div class="kick">{FLAG.format(id="fc")}<span>Aprendiendo neerlandés</span></div><div class="big">con Luis Suárez</div></div></div>
      <div class="row" style="top: 206px"><div id="tag" class="glass">{FLAG.format(id="ft")}<span>Neerlandés con Luis Suárez</span></div></div>
{chr(10).join(body)}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      // the title card from the first frame (the cover); at {TAG_AT} s it lifts away and the small pill settles at the top
      tl.to("#card", {{ y: -20, scale: 0.94, opacity: 0, duration: 0.32, ease: "power2.inOut" }}, {TAG_AT});
      tl.fromTo("#tag", {{ opacity: 0, y: 18, scale: 0.94 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.42, ease: "power3.out", immediateRender: false }}, {TAG_IN});
{chr(10).join(f'      tl.to("#tag", {{ opacity: 0, y: -8, scale: 0.96, duration: 0.2, ease: "power2.in" }}, {a - 0.2:.2f});{chr(10)}      tl.fromTo("#tag", {{ opacity: 0, y: 12, scale: 0.96 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.36, ease: "power3.out", immediateRender: false }}, {b:.2f});' for a, b in TAG_OFF)}
      // the cover is not darkened: the top shade is light and steady, the bottom one comes in with the first subtitle
      tl.set("#shade-bot", {{ opacity: 0 }}, 0);
      tl.set("#shade-bot", {{ opacity: 1 }}, {ons[0]:.3f});
{glide}
{chr(10).join(f'      tl.set("#shade-bot", {{ opacity: 0 }}, {a:.2f});{chr(10)}      tl.set("#shade-bot", {{ opacity: 1 }}, {b:.2f});' for a, b in UP)}
{chr(10).join(js)}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
    open(os.path.join(ROOT, "index.html"), "w").write(page)
    print(f"index.html: {D}s, {len(subs)} subtitle phrases")


if __name__ == "__main__":
    main()
