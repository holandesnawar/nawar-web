#!/usr/bin/env python3
"""index.html: the reel «Aprendiendo neerlandés con Luis Suárez» (9:16, 25 fps) in the look of the Mario Casas reel
(Drive: «Estrategia de contenido para reels»): the ad full frame (assets/video/suarez-916.mp4, tools/frame.py), the
title at the top from the first frame, then a one-line tag (📚 … 🇳🇱 — Noto Color Emoji, drawn to PNG by tools/emoji.py —, white with a black outline), and under the faces the subtitles: the
Dutch phrase big, in capitals, white with the word being said in yellow, and the Spanish under it, in a grey pill.
  python3 tools/gen.py
"""
import html, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
YEL = "#FFE11B"
NL_TOP, NL_W = 1150, 940          # the Dutch line's box (frame px) — above Instagram's caption/username band (≥ 1480)
TITLE_TOP = 236
TAG_AT = 3.0                      # the big title (the hook and the cover) becomes a one-line tag at the top here


def em_width(s):
    """rough width of an upper-case Poppins Black string, in em."""
    w = 0.0
    for ch in s.upper():
        w += 0.98 if ch in "MW" else 0.36 if ch in "I" else 0.27 if ch == " " else 0.3 if ch in ".,?!'-" else 0.74
    return w


def main():
    meta = json.load(open(os.path.join(ROOT, "assets", "video", "suarez-916.json")))
    D = meta["duration"]
    subs = json.load(open(os.path.join(ROOT, "subs.json")))["phrases"]
    body, js = [], []
    for k, p in enumerate(subs):
        words = p["words"]
        on = max(0.0, words[0]["t"] - 0.05)
        nxt = subs[k + 1]["words"][0]["t"] - 0.05 if k + 1 < len(subs) else D
        off = min(nxt, words[-1]["end"] + 0.7) if k + 1 < len(subs) else D
        text = " ".join(w["text"] for w in words)
        size = min(86, int(NL_W / em_width(text)))
        lines = 1
        if size < 64:
            size, lines = 72, 2
        spans = " ".join(f'<span id="w{k}-{i}" class="w">{html.escape(w["text"])}</span>' for i, w in enumerate(words))
        body.append(f'      <div id="p{k}" class="ph"><div class="nl" style="font-size: {size}px">{spans}</div>'
                    f'<div class="es"><span>{html.escape(p["es"])}</span></div></div>')
        js.append(f'      tl.set("#p{k}", {{ opacity: 1 }}, {on:.3f});')
        js.append(f'      tl.fromTo("#p{k} .nl", {{ scale: 0.86 }}, {{ scale: 1, duration: 0.16, ease: "back.out(2.2)", immediateRender: false }}, {on:.3f});')
        js.append(f'      tl.set("#p{k}", {{ opacity: 0 }}, {off:.3f});')
        for i, w in enumerate(words):
            t1 = words[i + 1]["t"] - 0.03 if i + 1 < len(words) else off
            js.append(f'      tl.set("#w{k}-{i}", {{ color: "{YEL}" }}, {max(on, w["t"] - 0.03):.3f});')
            if i + 1 < len(words):
                js.append(f'      tl.set("#w{k}-{i}", {{ color: "#FFFFFF" }}, {t1:.3f});')
    fonts = "\n".join(f'      @font-face {{ font-family: "{f}"; font-weight: {w}; src: url("assets/fonts/{f.lower()}-latin-{w}-normal.woff2") format("woff2"); }}'
                      for f, w in (("Poppins", 700), ("Poppins", 800), ("Poppins", 900), ("Inter", 700)))
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
      #shade-top {{ top: 0; height: 700px; background: linear-gradient(180deg, rgba(0,0,0,0.42) 0%, rgba(0,0,0,0.18) 55%, rgba(0,0,0,0) 100%); }}
      #shade-bot {{ top: 1020px; height: 560px; background: linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(0,0,0,0.30) 45%, rgba(0,0,0,0.30) 75%, rgba(0,0,0,0) 100%); }}
      #title {{ position: absolute; left: 0; top: {TITLE_TOP}px; width: 1080px; text-align: center; color: #FFFFFF; transform-origin: 50% 0%;
        font-family: "Poppins", sans-serif; font-weight: 800; font-size: 76px; line-height: 1.08; letter-spacing: -0.01em;
        -webkit-text-stroke: 9px #000; paint-order: stroke fill; text-shadow: 0 6px 18px rgba(0,0,0,0.45); }}
      #title .emo {{ position: absolute; width: 112px; height: auto; filter: drop-shadow(0 6px 12px rgba(0,0,0,0.35)); }}
      #emo-book {{ left: 52px; top: 22px; }}
      #emo-flag {{ right: 52px; top: 90px; }}
      #tag {{ position: absolute; left: 0; top: 214px; width: 1080px; display: flex; justify-content: center; opacity: 0; }}
      #tag div {{ display: flex; align-items: center; gap: 16px; padding: 10px 26px 12px; border-radius: 999px;
        background: rgba(0,0,0,0.42); color: #FFFFFF; font-family: "Poppins", sans-serif; font-weight: 800; font-size: 42px;
        line-height: 1; letter-spacing: -0.005em; white-space: nowrap; }}
      #tag i {{ display: block; height: 46px; background-size: contain; background-repeat: no-repeat; background-position: center; }}
      #tag-book {{ width: 47px; background-image: url("assets/img/emoji-book.png"); }}
      #tag-nl {{ width: 62px; background-image: url("assets/img/emoji-nl.png"); }}
      .ph {{ position: absolute; left: 0; top: {NL_TOP}px; width: 1080px; display: flex; flex-direction: column; align-items: center;
        gap: 20px; opacity: 0; }}
      .nl {{ width: {NL_W}px; display: flex; flex-wrap: wrap; justify-content: center; column-gap: 0.26em; row-gap: 0;
        font-family: "Poppins", sans-serif; font-weight: 900; line-height: 1.02; text-transform: uppercase; letter-spacing: -0.01em;
        color: #FFFFFF; -webkit-text-stroke: 10px #000; paint-order: stroke fill; text-shadow: 0 6px 16px rgba(0,0,0,0.5);
        transform-origin: 50% 60%; }}
      .w {{ display: inline-block; color: #FFFFFF; }}
      .es span {{ display: inline-block; max-width: 900px; padding: 10px 26px 12px; border-radius: 18px; text-align: center;
        background: rgba(78,78,84,0.78); color: #FFFFFF; font-family: "Poppins", sans-serif; font-weight: 700; font-size: 46px;
        line-height: 1.2; letter-spacing: -0.005em; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-width="1080" data-height="1920" data-duration="{D}" data-fps="25">
      <video id="v" class="clip" src="assets/video/suarez-916.mp4" data-start="0" data-duration="{D}" data-track-index="0" playsinline data-has-audio="true"></video>
      <div id="shade-top" class="shade"></div>
      <div id="shade-bot" class="shade"></div>
      <div id="title"><img id="emo-book" class="emo" src="assets/img/emoji-book.png" alt="" />Aprendiendo<br/>neerlandés<br/>con Luis Suárez<img id="emo-flag" class="emo" src="assets/img/emoji-nl.png" alt="" /></div>
      <div id="tag"><div><i id="tag-book"></i><span>Neerlandés con Luis Suárez</span><i id="tag-nl"></i></div></div>
{chr(10).join(body)}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      // the big title from the first frame (the cover), then a one-line tag that keeps clear of the faces
      tl.to("#title", {{ opacity: 0, y: -40, scale: 0.86, duration: 0.3, ease: "power2.in" }}, {TAG_AT});
      tl.fromTo("#tag", {{ opacity: 0, y: 24 }}, {{ opacity: 1, y: 0, duration: 0.32, ease: "power3.out", immediateRender: false }}, {TAG_AT + 0.18});
      tl.to("#shade-top", {{ opacity: 0.55, duration: 0.4, ease: "none" }}, {TAG_AT});
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
