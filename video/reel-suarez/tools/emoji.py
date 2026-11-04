#!/usr/bin/env python3
"""The two emoji of the title (📚 and 🇳🇱) drawn from Noto Color Emoji to PNG (assets/img/emoji-*.png), so the render
does not depend on a system emoji font.  python3 tools/emoji.py"""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
f = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf", 109)
for name, ch in (("book", "📚"), ("nl", "🇳🇱")):
    im = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((8, 8), ch, font=f, embedded_color=True)
    im.crop(im.getbbox()).save(os.path.join(ROOT, "assets", "img", f"emoji-{name}.png"))
