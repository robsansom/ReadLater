"""Shared image processing helpers for the website build scripts."""

from __future__ import annotations

import numpy as np
from PIL import Image, ImageDraw


_CANVAS_THRESHOLD = 16
"""Per-channel tolerance for identifying the Figma-export canvas via flood-fill."""


def _canvas_mask_from_corners(
    rgb: Image.Image,
    threshold: int,
    matte: tuple[int, int, int] | None = None,
) -> np.ndarray:
    """Return a boolean mask of pixels reachable from any corner via flood-fill.

    Dark mockups export on a pure-black canvas; light mockups may export on
    pure white (#FFFFFF). We flood from each corner using the colour that
    matches that corner so only the surrounding canvas is captured, never
    the device itself.
    """

    width, height = rgb.size
    working = rgb.copy()
    sentinel = (255, 0, 255)
    is_light_matte = matte is not None and sum(matte) > 400

    for corner in (
        (0, 0),
        (width - 1, 0),
        (0, height - 1),
        (width - 1, height - 1),
    ):
        cr, cg, cb = working.getpixel(corner)
        if cr <= threshold and cg <= threshold and cb <= threshold:
            ImageDraw.floodfill(working, corner, sentinel, thresh=threshold)
        elif is_light_matte and cr >= 240 and cg >= 240 and cb >= 240:
            ImageDraw.floodfill(working, corner, sentinel, thresh=threshold)

    arr = np.array(working)
    return (
        (arr[:, :, 0] == 255)
        & (arr[:, :, 1] == 0)
        & (arr[:, :, 2] == 255)
    )


def composite_device_on_matte(
    source: Image.Image,
    matte: tuple[int, int, int],
    *,
    fringe_blend: bool = False,
    fringe_radius: int = 6,
    fringe_luminance: int = 50,
) -> Image.Image:
    """Replace the Figma black canvas with a solid page-background colour.

    Device mockups are theme-locked — dark shots only appear on the dark
    page, light shots only on the light page. Making the surrounding canvas
    transparent (the old approach) creates a hard binary alpha silhouette;
    browsers then stair-step the edge and any dark anti-aliasing pixels from
    the Figma export read as a jagged dark fringe on the light surface.

    Instead we emit a plain RGB image: canvas pixels become the page matte,
    device pixels stay untouched. On light mockups we optionally blend the
    thin ring of near-black AA pixels adjacent to the canvas toward the matte
    so the outer bezel doesn't carry black-matte halos.
    """

    rgb = source.convert("RGB")
    canvas = _canvas_mask_from_corners(rgb, _CANVAS_THRESHOLD, matte=matte)
    arr = np.array(rgb, dtype=np.float32)
    matte_arr = np.array(matte, dtype=np.float32)

    arr[canvas] = matte_arr

    if fringe_blend:
        luminance = arr.max(axis=2)
        edge_zone = _dilate_mask(canvas, fringe_radius) & ~canvas
        fringe = edge_zone & (luminance < fringe_luminance)
        weight = np.clip(luminance / float(fringe_luminance), 0.0, 1.0)
        for channel in range(3):
            ch = arr[:, :, channel]
            ch[fringe] = (
                ch[fringe] * weight[fringe] + matte_arr[channel] * (1.0 - weight[fringe])
            )
            arr[:, :, channel] = ch

    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB")


def _dilate_mask(mask: np.ndarray, radius: int) -> np.ndarray:
    """Cheap square dilation — good enough for a few pixels of edge band."""

    out = mask.copy()
    height, width = mask.shape
    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            if dy == 0 and dx == 0:
                continue
            y0 = max(0, dy)
            y1 = min(height, height + dy)
            x0 = max(0, dx)
            x1 = min(width, width + dx)
            sy0 = max(0, -dy)
            sy1 = sy0 + (y1 - y0)
            sx0 = max(0, -dx)
            sx1 = sx0 + (x1 - x0)
            out[y0:y1, x0:x1] |= mask[sy0:sy1, sx0:sx1]
    return out


def knock_out_canvas_black(
    source: Image.Image, threshold: int = _CANVAS_THRESHOLD
) -> Image.Image:
    """Make the Figma export's black canvas transparent.

    Used for icons and glow assets that must composite on both page surfaces.
    Device mockups should use `composite_device_on_matte` instead.
    """

    img = source.convert("RGBA")
    canvas = _canvas_mask_from_corners(img.convert("RGB"), threshold)
    arr = np.array(img)
    arr[canvas, 3] = 0
    return Image.fromarray(arr, "RGBA")
