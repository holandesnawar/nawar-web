#!/usr/bin/env python3
"""Assemble a frame from its source (placeholders /*MAC_CSS*/ and <!--CHROME-->), write atomically."""
import os, sys
W = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.join(W, "..", "videos", "nawar-vsl")
fid, pfx = sys.argv[1], sys.argv[2]
src = open(os.path.join(W, f"{fid}.src.html")).read()
mac = open(os.path.join(W, "mac_css.txt")).read().replace("fXX-", pfx + "-")
chrome = open(os.path.join(W, "chrome.txt")).read().replace("fXX-", pfx + "-").strip()
out = src.replace("/*MAC_CSS*/", mac.strip()).replace("<!--CHROME-->", chrome)
assert out.lstrip().startswith("<template") and out.rstrip().endswith("</template>")
dst = os.path.join(PROJ, "compositions", "frames", f"{fid}.html")
tmp = dst + ".tmp"
open(tmp, "w").write(out)
os.replace(tmp, dst)
print("wrote", dst, len(out.splitlines()), "lines")
