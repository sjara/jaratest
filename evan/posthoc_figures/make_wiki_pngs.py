#!/usr/bin/env python3
"""Make wiki-ready PNG copies of post-hoc figures: opaque RGB, optimized, < --max-mb.

Size limits: at most --max-width px wide and/or at most --max-megapixels in total (either can be
omitted). Images already within the limits are never upscaled or resampled. With --include-tif,
.tif/.tiff files are converted to PNG too. Copies go to <out_dir>/<same subfolder>/<stem><suffix>.png.
If a file would still exceed --max-mb, it is shrunk further in 10% steps.

Examples:
    # 1600 px wide copies (wiki_png/, *_wiki.png)
    python make_wiki_pngs.py /path/to/posthoc_figures best_frequency_stacks bf_example_cells FOV_WF_bv_maps
    # largest size under 12.5 MP, PNGs and TIFFs
    python make_wiki_pngs.py /path/to/posthoc_figures best_frequency_stacks bf_example_cells FOV_WF_bv_maps \
        --max-width 0 --max-megapixels 12.5 --include-tif --out-dir /path/to/posthoc_figures/wiki_png_12p5MP \
        --suffix _wiki12p5MP
"""
import argparse
import math
from pathlib import Path

from PIL import Image


def to_wiki(src, dst, max_width, max_pixels, max_bytes):
    im = Image.open(src)
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        bg = Image.new("RGB", im.size, "white")
        bg.paste(im, mask=im.getchannel("A"))
        im = bg
    else:
        im = im.convert("RGB")
    scale = 1.0
    if max_width:
        scale = min(scale, max_width / im.width)
    if max_pixels:
        scale = min(scale, math.sqrt(max_pixels / (im.width * im.height)))
    width = min(im.width, math.floor(im.width * scale))
    if max_pixels:  # rounding of the height must not push the area over the limit
        while width * round(im.height * width / im.width) >= max_pixels:
            width -= 1
    while True:
        out = im if width == im.width else im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
        out.save(dst, optimize=True)
        if dst.stat().st_size < max_bytes or width < 400:
            return out.size, dst.stat().st_size
        width = int(width * 0.9)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("root", type=Path, help="posthoc_figures folder")
    ap.add_argument("subfolders", nargs="+", help="subfolders of root whose PNGs to convert")
    ap.add_argument("--out-dir", type=Path, default=None, help="default: <root>/wiki_png")
    ap.add_argument("--max-width", type=int, default=1600, help="0 = no width limit")
    ap.add_argument("--max-megapixels", type=float, default=None)
    ap.add_argument("--include-tif", action="store_true")
    ap.add_argument("--suffix", default="_wiki")
    ap.add_argument("--max-mb", type=float, default=2.0)
    args = ap.parse_args()
    out_root = args.out_dir or args.root / "wiki_png"
    for sub in args.subfolders:
        patterns = ["*.png"] + (["*.tif", "*.tiff"] if args.include_tif else [])
        for src in sorted(p for pat in patterns for p in (args.root / sub).glob(pat)):
            dst_dir = out_root / sub
            dst_dir.mkdir(parents=True, exist_ok=True)
            dst = dst_dir / f"{src.stem}{args.suffix}.png"
            max_px = int(args.max_megapixels * 1e6) if args.max_megapixels else None
            size, nbytes = to_wiki(src, dst, args.max_width, max_px, int(args.max_mb * 1e6))
            print(f"{nbytes / 1e6:5.2f} MB  {size[0]}x{size[1]} = {size[0] * size[1] / 1e6:5.2f} MP  "
                  f"{dst.relative_to(out_root)}")


if __name__ == "__main__":
    main()
