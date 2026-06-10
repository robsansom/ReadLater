"""Build favicons and web icons for both light and dark master variants.

The user provides two 1024x1024 PNG masters (one dark, one light/default).
This script:
- copies each master to public/images/app-icon{,-light}.png
- writes 32x32 favicon{,-light}.png at /public
- writes 180x180 apple-touch-icon{,-light}.png at /public
- writes 192/256/512 PWA/OG icons at /public/images, with `-light` siblings

The dark variant remains the primary (used as the OS favicon by default
and as the in-page header logo when the page is in its dark state). The
light variant is used when <html> picks up `is-light` so the on-page
logo always reads with enough contrast against the current surface.

PIL with LANCZOS keeps the rounded corners clean on every downscale.
"""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _image_utils import knock_out_canvas_black  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
IMAGES = PUBLIC / "images"

ASSETS = Path(
    "/Users/MummyDaddy/.cursor/projects/Users-MummyDaddy-My-Projects-Code-Projects-Pouch3-Website/assets"
)

# (master path, suffix used on every emitted file). Empty suffix = dark/default.
VARIANTS: tuple[tuple[Path, str], ...] = (
    (
        ASSETS
        / "Read_Later_v4-iOS-Dark-1024x1024_1x-9c2bcb01-9c74-44a5-9737-5bee48580eb1.png",
        "",
    ),
    (
        ASSETS
        / "Read_Later_v4-iOS-Default-1024x1024_1x-ca75c415-f228-4a93-99ab-432004ce3f36.png",
        "-light",
    ),
)


def emit_variant(master: Path, suffix: str) -> None:
    if not master.exists():
        raise SystemExit(f"Master icon not found at {master}")

    IMAGES.mkdir(parents=True, exist_ok=True)

    with Image.open(master) as raw:
        # Knock the pure-black canvas around the rounded icon shape out to
        # alpha so the icon composites cleanly on any header surface. The
        # rounded icon itself is left untouched — the flood stops at the
        # icon's anti-aliased edge.
        master_img = knock_out_canvas_black(raw)

        master_dest = IMAGES / f"app-icon{suffix}.png"
        master_img.save(master_dest, "PNG", optimize=True)
        print(f"{master_dest.name:<26} {master_dest.stat().st_size // 1024} KB (1024)")

        for size, target in (
            (32, PUBLIC / f"favicon{suffix}.png"),
            (180, PUBLIC / f"apple-touch-icon{suffix}.png"),
            (192, IMAGES / f"icon-192{suffix}.png"),
            (256, IMAGES / f"icon-256{suffix}.png"),
            (512, IMAGES / f"icon-512{suffix}.png"),
        ):
            resized = master_img.resize((size, size), Image.LANCZOS)
            resized.save(target, "PNG", optimize=True)
            print(f"{target.name:<26} {target.stat().st_size // 1024} KB ({size})")


def main() -> None:
    for master, suffix in VARIANTS:
        emit_variant(master, suffix)


if __name__ == "__main__":
    main()
