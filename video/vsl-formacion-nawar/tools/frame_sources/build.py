#!/usr/bin/env python3
"""Expand {{WINCSS}} / {{CHROME}} in a frame template (scratchpad) into compositions/frames/<id>.html."""
import re, sys, os
P = "/tmp/claude-0/-home-user-nawar-web/36d31257-d6ae-5587-b324-a9f00bcc433b/scratchpad"
PROJ = P + "/videos/nawar-vsl"
md = open(PROJ + "/tools/mac_mockup.md").read()
css = re.search(r"```css\n(.*?)```", md, re.S).group(1)
wincss = css[css.index("/* standalone macOS window"):]
wincss = ".fNN-win { --u: calc(var(--sw) / 1120); }\n" + wincss
wincss = wincss.replace("object-position: var(--fx, 50%) 50%", "object-position: var(--fx, 50%) var(--fy, 50%)")
chrome = re.search(r"## Markup — standalone macOS window\n\n```html\n(.*?)```", md, re.S).group(1)
chrome = chrome[chrome.index('  <div class="fNN-chrome">'):chrome.index('  <div class="fNN-content"')]
chrome = chrome.replace(">holandesnawar.com<", ">app.holandesnawar.com<")
for fid in sys.argv[1:]:
    pre = "f" + fid[:2]
    src = open(f"{P}/v3w/{fid}.tpl.html").read()
    w = "\n".join("    " + l for l in wincss.replace("fNN-", pre + "-").rstrip().splitlines())
    c = chrome.replace("fNN-", pre + "-").rstrip("\n")
    out = src.replace("{{WINCSS}}", w.strip()).replace("{{CHROME}}", c.strip())
    if fid == "25-practica":   # 3 windows: favicon as a CSS background (avoids duplicate_media_discovery_risk)
        out = out.replace('<img src="assets/img/logo-nawar.png" alt="" />', '<i class="f25-favlogo"></i>')
    assert "{{" not in out
    open(f"{PROJ}/compositions/frames/{fid}.html", "w").write(out)
    print("wrote", fid, len(out.splitlines()), "lines")
