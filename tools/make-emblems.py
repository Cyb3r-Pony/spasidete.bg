#!/usr/bin/env python3
"""Прави малките варианти на емблемите (192 px широчина) — те се показват
най-много на 58 CSS px, така че оригиналът от 341 px е излишен товар на
всяка страница. Запазва прозрачността.

Builds the small emblem variants (192 px wide). The emblems are displayed at
58 CSS px at most, so the 341 px original is dead weight on every page.
Transparency is preserved.

    python3 tools/make-emblems.py
"""
import os
from PIL import Image

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(HERE, "assets", "img")

TARGET_W = 192
WEBP_Q = 82
NAMES = ("cybercrime-gdbop", "gdbop-mvr")


def main():
    for name in NAMES:
        src = os.path.join(IMG, name + ".png")
        im = Image.open(src).convert("RGBA")
        w, h = im.size
        th = round(h * TARGET_W / w)
        small = im.resize((TARGET_W, th), Image.LANCZOS)

        small.save(os.path.join(IMG, name + "-sm.webp"), "WEBP",
                   quality=WEBP_Q, method=6)
        # PNG резервният вариант се свежда до палитра, за да не натежи.
        # The PNG fallback is palette-reduced so it does not outweigh the original.
        small.convert("RGBA").quantize(colors=128, method=Image.FASTOCTREE).save(
            os.path.join(IMG, name + "-sm.png"), "PNG", optimize=True)

        for ext in ("webp", "png"):
            p = os.path.join(IMG, "%s-sm.%s" % (name, ext))
            print("  -> %s  %dx%d  %d KB" % (os.path.basename(p), TARGET_W, th,
                                             os.path.getsize(p) // 1024))


if __name__ == "__main__":
    main()
