"""Build the Open Graph / social preview card.

The card uses the same Google Sans Flex family as the website and the
site's existing exported app icon, so brand-name changes do not need a
manual raster edit.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
DEST = ROOT / "public" / "images" / "social-card.png"
ICON = ROOT / "public" / "images" / "app-icon.png"

FONT_CANDIDATES = (
    Path("/Users/MummyDaddy/Library/Fonts/GoogleSansFlex-VariableFont_GRAD,ROND,opsz,slnt,wdth,wght.ttf"),
    Path("/Library/Fonts/SF-Pro-Display-Bold.otf"),
)

WIDTH = 1200
HEIGHT = 630
SCALE = 3

BLACK = (0, 0, 0, 255)
WHITE = (248, 247, 250, 255)
MUTED = (139, 136, 144, 255)
ACCENT = (250, 52, 84, 255)


def font_path() -> Path:
    for candidate in FONT_CANDIDATES:
        if candidate.exists():
            return candidate
    raise SystemExit("No suitable brand font found.")


def load_font(size: int, variation: str) -> ImageFont.FreeTypeFont:
    font = ImageFont.truetype(str(font_path()), size * SCALE)
    if hasattr(font, "set_variation_by_name"):
        try:
            font.set_variation_by_name(variation)
        except OSError:
            pass
    return font


def point(value: int) -> int:
    return value * SCALE


def main() -> None:
    canvas = Image.new("RGBA", (point(WIDTH), point(HEIGHT)), BLACK)
    draw = ImageDraw.Draw(canvas)

    with Image.open(ICON) as raw_icon:
        icon = raw_icon.convert("RGBA").resize((point(92), point(92)), Image.LANCZOS)
    canvas.alpha_composite(icon, (point(72), point(65)))

    wordmark = load_font(40, "SemiBold")
    headline = load_font(100, "Bold")
    small = load_font(30, "Regular")

    draw.text((point(186), point(96)), "Find Later", font=wordmark, fill=WHITE)
    draw.text((point(70), point(252)), "Save anything.", font=headline, fill=WHITE)
    draw.text((point(72), point(382)), "Find everything.", font=headline, fill=ACCENT)
    draw.text((point(72), point(528)), "For iPhone & iPad", font=small, fill=MUTED)

    output = canvas.resize((WIDTH, HEIGHT), Image.LANCZOS).convert("RGB")
    output.save(DEST, "PNG", optimize=True)
    print(f"Wrote {DEST}")


if __name__ == "__main__":
    main()
