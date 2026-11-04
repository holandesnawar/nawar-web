#!/usr/bin/env python3
"""index.html: the reel «Suárez habla neerlandés» (9:16, 25 fps), the second Luis Suárez reel, in the look of the first
(../reel-suarez) with the new, Apple-like labels:
- the interview full frame on his face (assets/video/habla-916.mp4, tools/frame.py);
- for the first 3 s (the hook and the cover) a frosted white card, «APRENDIENDO NEERLANDÉS · con Luis Suárez» with a
  round Dutch flag, which then becomes a small frosted pill at the top («Neerlandés con Luis Suárez»);
- the subtitles: the Dutch phrase big, in capitals, one size for all, white with the word being said in yellow, and the
  Spanish under it, in a grey pill; the reporter (off screen) has a small «Periodista» pill over his lines.
  python3 tools/gen.py
"""
import html, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
YEL = "#FFE11B"
NL_TOP, NL_W, NL_CX = 372, 940, 540    # the Dutch block (frame px), high: his face fills the frame, so the subtitles sit
NL_SIZE = 76                           # on his hair and his eyes and mouth stay in sight; under Instagram's header and
                                       # above its button rail (x > 912 from y ≈ 814), so the block can be wider than in
                                       # the first reel; one size, two lines at most («|» in tools/subs.py breaks them)
TAG_AT = 3.0                           # the title card (the hook and the cover) becomes the small pill at the top here
MIN_ON = 0.6                           # a phrase on screen for less than this opens a little early (after the last word
                                       # before it); one that stays long enough after its word (up to 0.7 s) does not
S_LIFT = 36                            # Suárez's lines (no «Periodista» pill over them) sit this much higher: clear of his brows

FLAG = ('<svg viewBox="0 0 48 48" aria-hidden="true"><defs><clipPath id="{id}"><circle cx="24" cy="24" r="24"/></clipPath></defs>'
        '<g clip-path="url(#{id})"><rect width="48" height="16" fill="#AE1C28"/><rect y="16" width="48" height="16" fill="#FFFFFF"/>'
        '<rect y="32" width="48" height="16" fill="#21468B"/></g><circle cx="24" cy="24" r="23" fill="none" stroke="rgba(0,0,0,0.22)" stroke-width="2"/></svg>')
MIC = ('<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="8.5" y="2.5" width="7" height="12" rx="3.5" fill="currentColor"/>'
       '<path d="M5.5 11.5a6.5 6.5 0 0 0 13 0M12 18v3.5M8.5 21.5h7" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>')

LABEL_CSS = """
      /* the labels: frosted white, like iOS (title card, top pill, «Periodista») */
      .glass {{ background: rgba(255,255,255,0.80); -webkit-backdrop-filter: blur(28px) saturate(180%); backdrop-filter: blur(28px) saturate(180%);
        box-shadow: 0 1px 0 rgba(255,255,255,0.9) inset, 0 18px 50px rgba(0,0,0,0.22), 0 2px 8px rgba(0,0,0,0.10); color: #1D1D1F;
        font-family: "Inter", sans-serif; }}
      .row {{ position: absolute; left: 0; width: 1080px; display: flex; justify-content: center; }}
      #card {{ display: flex; flex-direction: column;
        align-items: center; gap: 2px; padding: 22px 48px 26px; border-radius: 44px; white-space: nowrap; }}
      #card .kick {{ display: flex; align-items: center; gap: 14px; font-weight: 700; font-size: 44px; letter-spacing: -0.015em;
        color: #1D0084; line-height: 1.1; }}
      #card .kick svg {{ width: 46px; height: 46px; display: block; }}
      #card .big {{ font-weight: 700; font-size: 80px; letter-spacing: -0.03em; line-height: 1.02; }}
      #tag {{ display: flex; align-items: center; gap: 12px;
        padding: 10px 28px 10px 12px; border-radius: 999px; white-space: nowrap; opacity: 0; font-weight: 600; font-size: 32px;
        letter-spacing: -0.01em; line-height: 1; }}
      #tag svg {{ width: 40px; height: 40px; display: block; }}
      .who {{ position: absolute; left: 50%; top: -54px; transform: translateX(-50%); display: flex; align-items: center; gap: 8px;
        padding: 8px 18px 8px 12px; border-radius: 999px; font-weight: 700; font-size: 24px; letter-spacing: 0.12em; text-transform: uppercase;
        line-height: 1; white-space: nowrap; color: #1D0084; }}
      .who svg {{ width: 26px; height: 26px; display: block; }}
""".replace("{{", "{").replace("}}", "}")


def main():
    meta = json.load(open(os.path.join(ROOT, "assets", "video", "habla-916.json")))
    D = meta["duration"]
    subs = json.load(open(os.path.join(ROOT, "subs.json")))["phrases"]
    body, js = [], []
    ons = []
    for k, p in enumerate(subs):
        words = p["words"]
        on = max(0.0, words[0]["t"] - 0.05)
        nxt = subs[k + 1]["words"][0]["t"] - 0.05 if k + 1 < len(subs) else D
        if min(nxt, words[-1]["end"] + 0.7) - on < MIN_ON and k:
            on = max(subs[k - 1]["words"][-1]["end"] + 0.03, min(on, words[-1]["end"] - MIN_ON))
        ons.append(on)
    for k, p in enumerate(subs):
        words = p["words"]
        on = ons[k]
        off = min(ons[k + 1], words[-1]["end"] + 0.7) if k + 1 < len(subs) else D
        spans = " ".join(('<span class="br"></span> ' if i in p.get("breaks", []) else "") +
                         f'<span id="w{k}-{i}" class="w">{html.escape(w["text"])}</span>' for i, w in enumerate(words))
        who = f'<div class="who glass">{MIC}<span>Periodista</span></div>' if p["who"] == "r" else ""
        top = NL_TOP - (S_LIFT if p["who"] == "s" else 0)
        body.append(f'      <div id="p{k}" class="ph" style="top: {top}px">{who}<div class="nl">{spans}</div>'
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
      /* a soft shade at the top only, under the subtitles (no text lower down: his mouth keeps its own light) */
      #shade-top {{ top: 0; height: 760px; background: linear-gradient(180deg, rgba(0,0,0,0.30) 0%, rgba(0,0,0,0.10) 55%, rgba(0,0,0,0) 100%); }}
{LABEL_CSS}
      .ph {{ position: absolute; left: {NL_CX - 505}px; top: {NL_TOP}px; width: 1010px; display: flex; flex-direction: column; align-items: center;
        gap: 12px; opacity: 0; }}
      .nl {{ width: {NL_W}px; font-size: {NL_SIZE}px; display: flex; flex-wrap: wrap; justify-content: center; column-gap: 0.26em; row-gap: 0;
        font-family: "Poppins", sans-serif; font-weight: 900; line-height: 1.02; text-transform: uppercase; letter-spacing: -0.01em;
        color: #FFFFFF; -webkit-text-stroke: 10px #000; paint-order: stroke fill; text-shadow: 0 6px 16px rgba(0,0,0,0.5);
        transform-origin: 50% 60%; }}
      .w {{ display: inline-block; color: #FFFFFF; }}
      .br {{ flex-basis: 100%; height: 0; }}
      .es span {{ display: inline-block; white-space: nowrap; padding: 8px 24px 10px; border-radius: 18px; text-align: center;
        background: rgba(78,78,84,0.78); color: #FFFFFF; font-family: "Poppins", sans-serif; font-weight: 700; font-size: 44px;
        line-height: 1.2; letter-spacing: -0.005em; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-width="1080" data-height="1920" data-duration="{D}" data-fps="25">
      <video id="v" class="clip" src="assets/video/habla-916.mp4" data-start="0" data-duration="{D}" data-track-index="0" playsinline data-has-audio="true"></video>
      <div id="shade-top" class="shade"></div>
      <div class="row" style="top: {CARD_TOP}px"><div id="card" class="glass"><div class="kick">{FLAG.format(id="fc")}<span>Aprendiendo neerlandés</span></div><div class="big">con Luis Suárez</div></div></div>
      <div class="row" style="top: 206px"><div id="tag" class="glass">{FLAG.format(id="ft")}<span>Neerlandés con Luis Suárez</span></div></div>
{chr(10).join(body)}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      // the title card from the first frame (the cover); at {TAG_AT} s it lifts away and the small pill settles at the top
      tl.to("#card", {{ y: -20, scale: 0.94, opacity: 0, duration: 0.32, ease: "power2.inOut" }}, {TAG_AT});
      tl.fromTo("#tag", {{ opacity: 0, y: 18, scale: 0.94 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.42, ease: "power3.out", immediateRender: false }}, {TAG_AT + 0.24});
{chr(10).join(js)}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
    open(os.path.join(ROOT, "index.html"), "w").write(page)
    print(f"index.html: {D}s, {len(subs)} subtitle phrases")


CARD_TOP = 1310                        # the title card under his mouth, over his chin and collar (above the caption band)


if __name__ == "__main__":
    main()
