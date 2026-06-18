#!/usr/bin/env python3
"""Composite localized iPad screenshots into the website's existing device frame."""

from pathlib import Path
import argparse

from PIL import Image, ImageDraw


SCREEN_BOX = (56, 56, 1295, 1708)
SCREEN_RADIUS = 38
LOCALES = ("fr", "de", "es", "ja")
APPEARANCES = ("dark", "light")


def frame_screenshot(source: Path, template: Path, output: Path) -> None:
    frame = Image.open(template).convert("RGBA")
    screenshot = Image.open(source).convert("RGB")
    width = SCREEN_BOX[2] - SCREEN_BOX[0]
    height = SCREEN_BOX[3] - SCREEN_BOX[1]
    screenshot = screenshot.resize((width, height), Image.Resampling.LANCZOS)

    mask = Image.new("L", (width, height), 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        (0, 0, width - 1, height - 1), radius=SCREEN_RADIUS, fill=255
    )
    frame.paste(screenshot, SCREEN_BOX[:2], mask)
    output.parent.mkdir(parents=True, exist_ok=True)
    frame.save(output, optimize=True)
    frame.save(output.with_suffix(".webp"), "WEBP", quality=92, method=6)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    args = parser.parse_args()
    repo = args.repo.resolve()

    for locale in LOCALES:
        for appearance in APPEARANCES:
            source = repo / "source-assets" / "ipad" / locale / f"ipad-collections-{appearance}.png"
            template = repo / "public" / "images" / f"ipad-{appearance}.png"
            output = repo / "public" / "images" / "ipad" / locale / f"ipad-collections-{appearance}.png"
            frame_screenshot(source, template, output)
            print(output.relative_to(repo))


if __name__ == "__main__":
    main()
