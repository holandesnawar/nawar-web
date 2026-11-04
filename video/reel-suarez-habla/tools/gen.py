#!/usr/bin/env python3
"""The reel «Suárez habla neerlandés» (9:16, 25 fps), the second Luis Suárez reel, in two versions to choose from:
- con tarjeta (the default): a big frosted white card at the top for the whole reel, «Aprendiendo neerlandés · con Luis
  Suárez» with a round Dutch flag (it is also the cover);
- --sin-tarjeta: no card, only the subtitles.
Both: the interview full frame on his face (assets/video/habla-916.mp4, tools/frame.py), and the subtitles at the bottom:
the Dutch phrase big, in capitals, one size for all, white with the word being said in yellow, and the Spanish under it,
in a grey pill, all centred under his face (the picture is pushed in so his mouth sits above them: tools/frame.py).
  python3 tools/gen.py [--sin-tarjeta]      → index.html
"""
import html, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
YEL = "#FFE11B"
SUB_BOTTOM = 1500                      # the subtitle block stands on this line (frame px): above Instagram's caption band
NL_W, NL_CX = 744, 540                 # centred, and left of its button rail (x > 912 from y ≈ 814)
NL_SIZE = 62                           # one size, two lines at most («|» in tools/subs.py breaks them)
ES_SIZE = 38
CARD_TOP = 214                         # (con tarjeta) the title card, under Instagram's header, over his hair: his eyes
                                       # stay below y ≈ 720
MIN_ON = 0.6                           # a phrase on screen for less than this opens a little early (after the last word
                                       # before it); one that stays long enough after its word (up to 0.7 s) does not
BRIDGE = 0.25                          # a gap shorter than this between two phrases is closed (no one-frame blink)

FLAG = ('<svg viewBox="0 0 48 48" aria-hidden="true"><defs><clipPath id="{id}"><circle cx="24" cy="24" r="24"/></clipPath></defs>'
        '<g clip-path="url(#{id})"><rect width="48" height="16" fill="#AE1C28"/><rect y="16" width="48" height="16" fill="#FFFFFF"/>'
        '<rect y="32" width="48" height="16" fill="#21468B"/></g><circle cx="24" cy="24" r="23" fill="none" stroke="rgba(0,0,0,0.22)" stroke-width="2"/></svg>')

LABEL_CSS = """
      /* the title card: frosted white, like iOS */
      .glass {{ background: rgba(255,255,255,0.80); -webkit-backdrop-filter: blur(28px) saturate(180%); backdrop-filter: blur(28px) saturate(180%);
        box-shadow: 0 1px 0 rgba(255,255,255,0.9) inset, 0 18px 50px rgba(0,0,0,0.22), 0 2px 8px rgba(0,0,0,0.10); color: #1D1D1F;
        font-family: "Inter", sans-serif; }}
      .row {{ position: absolute; left: 0; width: 1080px; display: flex; justify-content: center; }}
      /* the title card, big, at the top for the whole reel */
      #card {{ display: flex; flex-direction: column;
        align-items: center; gap: 2px; padding: 20px 60px 26px; border-radius: 50px; white-space: nowrap; }}
      #card .kick {{ display: flex; align-items: center; gap: 16px; font-weight: 700; font-size: 50px; letter-spacing: -0.015em;
        color: #1D0084; line-height: 1.1; }}
      #card .kick svg {{ width: 54px; height: 54px; display: block; }}
      #card .big {{ font-weight: 700; font-size: 96px; letter-spacing: -0.03em; line-height: 1.02; }}
""".replace("{{", "{").replace("}}", "}")


def main():
    meta = json.load(open(os.path.join(ROOT, "assets", "video", "habla-916.json")))
    D = meta["duration"]
    subs = json.load(open(os.path.join(ROOT, "subs.json")))["phrases"]
    body, js = [], []
    cuts = [s["reel"] for s in meta["segments"][1:]]          # the hard cuts between the moments: no phrase crosses one
    ons = []
    for k, p in enumerate(subs):
        words = p["words"]
        on = max(0.0, words[0]["t"] - 0.05)
        nxt = subs[k + 1]["words"][0]["t"] - 0.05 if k + 1 < len(subs) else D
        if min(nxt, words[-1]["end"] + 0.7) - on < MIN_ON and k:
            on = max(subs[k - 1]["words"][-1]["end"] + 0.03, min(on, words[-1]["end"] - MIN_ON))
        on = max([on] + [c for c in cuts if c <= words[0]["t"]])
        ons.append(on)
    for k, p in enumerate(subs):
        words = p["words"]
        on = ons[k]
        off = min(ons[k + 1], words[-1]["end"] + 0.7) if k + 1 < len(subs) else D
        if k + 1 < len(subs) and ons[k + 1] - off < BRIDGE:
            off = ons[k + 1]
        off = min([off] + [c for c in cuts if c > on])
        spans = " ".join(('<span class="br"></span> ' if i in p.get("breaks", []) else "") +
                         f'<span id="w{k}-{i}" class="w">{html.escape(w["text"])}</span>' for i, w in enumerate(words))
        body.append(f'      <div id="p{k}" class="ph"><div class="nl">{spans}</div>'
                    f'<div class="es"><span>{html.escape(p["es"]).replace("|", "<br>")}</span></div></div>')
        js.append(f'      tl.set("#p{k}", {{ opacity: 1 }}, {on:.3f});')
        js.append(f'      tl.fromTo("#p{k} .nl", {{ scale: 0.86 }}, {{ scale: 1, duration: 0.16, ease: "back.out(1.6)", immediateRender: false }}, {on:.3f});')
        js.append(f'      tl.set("#p{k}", {{ opacity: 0 }}, {off:.3f});')
        for i, w in enumerate(words):
            t1 = words[i + 1]["t"] - 0.03 if i + 1 < len(words) else off
            js.append(f'      tl.set("#w{k}-{i}", {{ color: "{YEL}" }}, {max(on, w["t"] - 0.03):.3f});')
            if i + 1 < len(words):
                js.append(f'      tl.set("#w{k}-{i}", {{ color: "#FFFFFF" }}, {t1:.3f});')
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
      /* a soft shade at the bottom, under the subtitles */
      #shade-bot {{ top: 1180px; height: 740px; background: linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(0,0,0,0.26) 45%, rgba(0,0,0,0.34) 100%); }}
{LABEL_CSS}
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
    <div id="root" data-composition-id="main" data-width="1080" data-height="1920" data-duration="{D}" data-fps="25">
      <video id="v" class="clip" src="assets/video/habla-916.mp4" data-start="0" data-duration="{D}" data-track-index="0" playsinline data-has-audio="true"></video>
      <div id="shade-bot" class="shade"></div>
{{CARD}}{chr(10).join(body)}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
    card = "--sin-tarjeta" not in sys.argv[1:]
    open(os.path.join(ROOT, "index.html"), "w").write(page.replace("{CARD}", (
        f'      <div class="row" style="top: {CARD_TOP}px"><div id="card" class="glass"><div class="kick">{FLAG.format(id="fc")}'
        '<span>Aprendiendo neerlandés</span></div><div class="big">con Luis Suárez</div></div></div>\n') if card else ""))
    print(f"index.html: {D}s, {len(subs)} subtitle phrases" + (", the title card at the top" if card else ", subtitles only"))


if __name__ == "__main__":
    main()
