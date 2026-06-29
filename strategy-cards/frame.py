#!/usr/bin/env python3
"""
Wrap a tall card into a feed-friendly canvas with a BLURRED side-fill
(no cropping — full card stays visible, blurred enlargement fills the gaps).

Usage:
  python frame.py output/034-tsmom-hybrid.png output/034-tsmom-45.png 1080x1350
  python frame.py <in> <out> [WxH]   # default 1080x1350 (Instagram 4:5)
"""
import sys, pathlib
from PIL import Image, ImageFilter, ImageEnhance

def frame(src, dst, cw, ch):
    card = Image.open(src).convert("RGB")
    iw, ih = card.size

    # --- background: scale card to COVER the canvas, blur + darken ---
    cover = max(cw / iw, ch / ih)
    bg = card.resize((int(iw * cover) + 2, int(ih * cover) + 2), Image.LANCZOS)
    bx = (bg.width - cw) // 2
    by = (bg.height - ch) // 2
    bg = bg.crop((bx, by, bx + cw, by + ch))
    bg = bg.filter(ImageFilter.GaussianBlur(45))
    bg = ImageEnhance.Brightness(bg).enhance(0.55)

    # --- foreground: scale card to FIT inside the canvas, centered ---
    fit = min(cw / iw, ch / ih)
    fw, fh = int(iw * fit), int(ih * fit)
    fg = card.resize((fw, fh), Image.LANCZOS)
    fx, fy = (cw - fw) // 2, (ch - fh) // 2

    canvas = bg.copy()
    # soft shadow behind the card for separation from the blur
    shadow = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    from PIL import ImageDraw
    ImageDraw.Draw(shadow).rectangle([fx - 6, fy - 6, fx + fw + 6, fy + fh + 6], fill=(0, 0, 0, 150))
    shadow = shadow.filter(ImageFilter.GaussianBlur(14))
    canvas = canvas.convert("RGBA")
    canvas.alpha_composite(shadow)
    canvas.paste(fg, (fx, fy))
    canvas.convert("RGB").save(dst, quality=95)
    print(f"saved -> {dst}  ({cw}x{ch}, card {fw}x{fh} centered, {fx}px side-fill)")

if __name__ == "__main__":
    src, dst = sys.argv[1], sys.argv[2]
    size = sys.argv[3] if len(sys.argv) > 3 else "1080x1350"
    cw, ch = (int(x) for x in size.lower().split("x"))
    frame(src, dst, cw, ch)
