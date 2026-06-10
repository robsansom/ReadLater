"""Stage device mockups for the website.

Inputs are pre-framed PNGs with the device chrome and halftone background
pattern baked in. Figma exports on a solid canvas — black for dark mockups,
white for light ones. The matte step replaces only the outer canvas (via
corner flood-fill) with the page background colour so the dot pattern and
device pixels stay untouched.

Figma @3x exports target 3072×2718. The site renders them at the 1x
layout size (1024×906 logical px) via CSS — asset pixels ÷ 3 = display size.

For each device shot we emit a PNG + WebP into /public/images.
"""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _image_utils import composite_device_on_matte  # noqa: E402

ASSETS = Path(
    "/Users/MummyDaddy/.cursor/projects/Users-MummyDaddy-My-Projects-Code-Projects-Pouch3-Website/assets"
)
DEST = Path(__file__).resolve().parent.parent / "public" / "images"

PAGE_DARK = (0, 0, 0)
PAGE_LIGHT = (243, 242, 247)

# 1x layout size — must match HTML width/height on showcase <img> tags.
DISPLAY_WIDTH = 1024
DISPLAY_HEIGHT = 906

# @3x output (1024 × 3); site CSS displays at 1x layout size.
OUTPUT_MAX_WIDTH = DISPLAY_WIDTH * 3

# Device mockups: (source, output stem, page matte, fringe_blend).
DEVICE_PICKS: tuple[tuple[str, str, tuple[int, int, int], bool], ...] = (
    ("1a.png", "device-bookmarks-dark", PAGE_DARK, False),
    ("2.png", "device-collection-light", PAGE_LIGHT, True),
    ("3.png", "device-detail-dark", PAGE_DARK, False),
    ("4.png", "screen-bookmarks-ipad", PAGE_DARK, False),
    ("5.png", "screen-collection-ipad", PAGE_LIGHT, True),
)


def emit_device(
    source_name: str,
    dest_stem: str,
    matte: tuple[int, int, int],
    fringe_blend: bool,
) -> None:
    source = ASSETS / source_name
    if not source.exists():
        raise SystemExit(f"Missing source asset: {source}")

    with Image.open(source) as raw:
        img = composite_device_on_matte(raw, matte, fringe_blend=fringe_blend)

        original_size = (img.width, img.height)
        if img.width > OUTPUT_MAX_WIDTH:
            scale = OUTPUT_MAX_WIDTH / img.width
            new_size = (OUTPUT_MAX_WIDTH, int(img.height * scale))
            output = img.resize(new_size, Image.LANCZOS)
        else:
            output = img.copy()
            new_size = (img.width, img.height)

        png_target = DEST / f"{dest_stem}.png"
        webp_target = DEST / f"{dest_stem}.webp"
        output.save(png_target, "PNG", optimize=True)
        output.save(webp_target, "WEBP", quality=92, method=6)

        scale_note = ""
        if new_size[0] > DISPLAY_WIDTH:
            scale_note = f" | display @ {DISPLAY_WIDTH}×{DISPLAY_HEIGHT} (÷{new_size[0] // DISPLAY_WIDTH})"

        print(
            f"{dest_stem:<26} {original_size[0]}x{original_size[1]} -> "
            f"{new_size[0]}x{new_size[1]}{scale_note} | "
            f"png {png_target.stat().st_size // 1024} KB, "
            f"webp {webp_target.stat().st_size // 1024} KB"
        )


def main() -> None:
    DEST.mkdir(parents=True, exist_ok=True)
    for source, stem, matte, fringe_blend in DEVICE_PICKS:
        emit_device(source, stem, matte, fringe_blend)


if __name__ == "__main__":
    main()
