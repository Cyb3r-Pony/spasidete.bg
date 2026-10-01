#!/usr/bin/env python3
"""Генерира вариантите на снимките: -xs (480), -sm (половината), -md (960)
и WebP за всеки размер. Пуска се само когато се добавят нови снимки.

Generates the photo variants: -xs (480), -sm (half width), -md (960) plus a
WebP for every size. Run it only when new photos are added.

    python3 tools/make-images.py
"""
import os
import glob
from PIL import Image

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PHOTOS = os.path.join(HERE, "assets", "img", "photos")

JPEG_Q = 82
WEBP_Q = 78


def variants(w):
    """Ширините, които си заслужават за оригинал с ширина w."""
    out = [("-xs", 480)]
    half = max(640, w // 2)
    if half < w:
        out.append(("-sm", half))
    # Среден вариант за снимките, които се показват към 900-960 CSS px.
    # A mid-size variant for photos displayed at around 900-960 CSS px.
    if w >= 1200 and abs(960 - half) > 80:
        out.append(("-md", 960))
    return sorted(out, key=lambda x: x[1])


def main():
    originals = [f for f in sorted(glob.glob(os.path.join(PHOTOS, "*.jpg")))
                 if not os.path.basename(f).rsplit(".", 1)[0].endswith(("-xs", "-sm", "-md"))]
    made = 0
    for path in originals:
        base = os.path.basename(path)[:-4]
        im = Image.open(path)
        im = im.convert("RGB")
        w, h = im.size

        # Оригиналът също получава WebP / the original gets a WebP too.
        full_webp = os.path.join(PHOTOS, base + ".webp")
        if not os.path.exists(full_webp):
            im.save(full_webp, "WEBP", quality=WEBP_Q, method=6)
            made += 1

        for sfx, tw in variants(w):
            if tw >= w:
                continue
            th = round(h * tw / w)
            small = im.resize((tw, th), Image.LANCZOS)
            for ext, kw in (("jpg", dict(format="JPEG", quality=JPEG_Q, optimize=True, progressive=True)),
                            ("webp", dict(format="WEBP", quality=WEBP_Q, method=6))):
                out = os.path.join(PHOTOS, "%s%s.%s" % (base, sfx, ext))
                if not os.path.exists(out):
                    small.save(out, **kw)
                    made += 1
                    print("  ->", os.path.basename(out), "%dx%d" % (tw, th))
    print("%d file(s) written." % made)


if __name__ == "__main__":
    main()
