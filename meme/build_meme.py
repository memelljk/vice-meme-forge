#!/usr/bin/env python3
"""Build the vice-meme-forge GTA 6 meme with PIL only.

Scene: the make.fun ghost finally reaches Leonida. A sunset boulevard,
a neon billboard for make.fun worked into the skyline, and the ghost
itself riding a magenta convertible, sunglasses on, coin in hand.

Deterministic: every coordinate and colour below is a fixed constant,
so two runs produce byte-identical meme.png files.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
SIZE = 1200
HORIZON = 790

FONT_PATH = HERE / "Anton-Regular.ttf"
GHOST_PATH = HERE / "ghost.png"
OUT_PATH = HERE / "meme.png"

TOP_CAPTION = "13 YEARS. 2 DELAYS. 47 FAKE SICK DAYS."
BOTTOM_CAPTION = "LAUNCH WEEK IN LEONIDA: WORTH EVERY ONE"

GHOST_HEIGHT = 500


def font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_PATH), size)


def lerp(a: int, b: int, t: float) -> int:
    return round(a + (b - a) * t)


def sky_gradient(img: Image.Image) -> None:
    """Vertical gradient: deep purple -> magenta -> hot orange."""
    stops = [
        (0.00, (34, 8, 66)),
        (0.45, (122, 22, 110)),
        (0.72, (214, 44, 116)),
        (1.00, (255, 138, 54)),
    ]
    px = img.load()
    for y in range(HORIZON):
        t = y / max(1, HORIZON - 1)
        for i in range(len(stops) - 1):
            t0, c0 = stops[i]
            t1, c1 = stops[i + 1]
            if t0 <= t <= t1:
                f = (t - t0) / (t1 - t0)
                colour = tuple(lerp(c0[k], c1[k], f) for k in range(3))
                break
        for x in range(SIZE):
            px[x, y] = colour


def draw_sun(draw: ImageDraw.ImageDraw) -> None:
    cx, cy, r = 880, 600, 155
    # Soft halo rings, widest and faintest first.
    for extra, colour in ((46, (255, 120, 90)), (26, (255, 158, 92))):
        draw.ellipse([cx - r - extra, cy - r - extra, cx + r + extra, cy + r + extra],
                     fill=colour)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 205, 110))
    # Retro cut lines across the lower sun.
    for i, dy in enumerate((58, 88, 116)):
        draw.rectangle([cx - r, cy + dy, cx + r, cy + dy + 7 + i * 3],
                       fill=(238, 84, 110))


CLOUDS = [
    (120, 150, 300, 44),
    (700, 110, 260, 38),
    (980, 210, 240, 36),
    (420, 90, 200, 30),
]


def draw_clouds(base: Image.Image) -> None:
    layer = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for x, y, w, h in CLOUDS:
        d.ellipse([x, y, x + w, y + h], fill=(30, 6, 52, 110))
        d.ellipse([x + w * 0.25, y - h * 0.45, x + w * 0.75, y + h * 0.4],
                  fill=(30, 6, 52, 110))
    base.alpha_composite(layer.filter(ImageFilter.GaussianBlur(6)))


def draw_billboard(draw: ImageDraw.ImageDraw) -> None:
    # Pole first, then the board, planted on the left skyline.
    draw.rectangle([238, 470, 262, HORIZON], fill=(24, 10, 40))
    draw.rectangle([70, 300, 450, 478], fill=(16, 10, 44))
    draw.rectangle([70, 300, 450, 478], outline=(255, 45, 160), width=7)
    draw.rectangle([84, 314, 436, 464], outline=(40, 220, 255), width=3)
    title = font(76)
    draw.text((260, 356), "make.fun", font=title, anchor="mm",
              fill=(255, 255, 255))
    sub = font(27)
    draw.text((260, 424), "agents earn real money here", font=sub, anchor="mm",
              fill=(255, 205, 90))


def draw_palm(draw: ImageDraw.ImageDraw, base_x: int, top_y: int,
              lean: int, scale: float) -> None:
    colour = (18, 6, 34)
    base_y = HORIZON + 26
    top_x = base_x + lean
    # Trunk: a tapering stack of short segments along a gentle curve.
    steps = 14
    for i in range(steps):
        t0 = i / steps
        t1 = (i + 1) / steps
        x0 = base_x + (top_x - base_x) * t0
        x1 = base_x + (top_x - base_x) * t1
        y0 = base_y - (base_y - top_y) * t0
        y1 = base_y - (base_y - top_y) * t1
        w = (13 - 7 * t0) * scale
        draw.line([x0, y0, x1, y1], fill=colour, width=max(2, round(w)))
    # Fronds: arcs fanning out of the crown.
    crown = (top_x, top_y)
    for dx, dy, bend in ((-120, -34, 46), (-78, -62, 30), (-30, -78, 12),
                         (34, -76, -14), (84, -58, -30), (124, -28, -48)):
        ex = crown[0] + dx * scale
        ey = crown[1] + dy * scale + abs(dx) * 0.22 * scale
        mx = crown[0] + dx * 0.5 * scale
        my = crown[1] + (dy - bend) * scale
        draw.arc([min(crown[0], ex, mx) - 4, min(crown[1], ey, my) - 4,
                  max(crown[0], ex, mx) + 4, max(crown[1], ey, my) + 60 * scale],
                 start=180, end=360, fill=colour, width=max(3, round(9 * scale)))


def draw_boulevard(draw: ImageDraw.ImageDraw) -> None:
    # Asphalt below the horizon, a neon kerb line and centre dashes.
    draw.rectangle([0, HORIZON, SIZE, SIZE], fill=(26, 14, 42))
    draw.rectangle([0, HORIZON, SIZE, HORIZON + 10], fill=(255, 45, 160))
    draw.rectangle([0, HORIZON + 16, SIZE, HORIZON + 20], fill=(40, 220, 255))
    for x in range(30, SIZE, 150):
        draw.rectangle([x, 1006, x + 74, 1020], fill=(255, 205, 90))


def draw_car(draw: ImageDraw.ImageDraw) -> None:
    body = (232, 32, 128)
    dark = (90, 8, 58)
    # Main body: a low, long convertible silhouette.
    draw.rounded_rectangle([170, 928, 900, 1046], radius=52, fill=body)
    draw.polygon([(900, 972), (1010, 1004), (1000, 1046), (900, 1046)], fill=body)
    # Cabin opening the ghost rises out of.
    draw.rounded_rectangle([330, 900, 760, 968], radius=30, fill=dark)
    # Windshield slant at the front (right side).
    draw.polygon([(760, 906), (852, 952), (760, 962)], fill=(150, 230, 255))
    # Side trim + door line.
    draw.line([190, 1000, 980, 1000], fill=(255, 150, 205), width=6)
    draw.arc([420, 940, 560, 1050], start=300, end=120, fill=dark, width=5)
    # Headlight glow and tail light.
    draw.ellipse([972, 990, 1006, 1016], fill=(255, 236, 160))
    draw.rectangle([178, 998, 198, 1022], fill=(255, 60, 60))
    # Wheels.
    for cx in (268, 838):
        draw.ellipse([cx - 56, 986, cx + 56, 1098], fill=(10, 8, 16))
        draw.ellipse([cx - 26, 1016, cx + 26, 1068], fill=(196, 200, 214))
        draw.ellipse([cx - 8, 1034, cx + 8, 1050], fill=(70, 72, 84))


def draw_sunglasses(img: Image.Image) -> None:
    """Black Vice City shades across the ghost's eyes, placed from the
    ghost's own alpha bounding box so they land on its face."""
    ghost = Image.open(GHOST_PATH).convert("RGBA")
    bbox = ghost.getbbox()
    gx, gy, gw, gh = GHOST_BOX
    # Scale the mark's own bbox into where it sits on the canvas.
    sx = gw / ghost.width
    sy = gh / ghost.height
    bx0 = gx + bbox[0] * sx
    bx1 = gx + bbox[2] * sx
    by0 = gy + bbox[1] * sy
    bw = bx1 - bx0
    eye_y = by0 + 0.335 * (bbox[3] - bbox[1]) * sy
    bar_h = 0.115 * (bbox[3] - bbox[1]) * sy
    layer = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    # The mark's alpha bbox is the whole magenta disc; the ghost's head
    # occupies only its middle band, so the bar spans that band, not
    # the full disc width.
    x0, x1 = bx0 + 0.235 * bw, bx1 - 0.235 * bw
    bar_w = x1 - x0
    d.rounded_rectangle([x0, eye_y, x1, eye_y + bar_h], radius=bar_h * 0.45,
                        fill=(8, 8, 12, 255))
    # Two lens shines.
    for lx in (x0 + 0.12 * bar_w, x0 + 0.56 * bar_w):
        d.line([lx, eye_y + bar_h * 0.62, lx + 0.16 * bar_w, eye_y + bar_h * 0.30],
               fill=(140, 200, 235, 220), width=max(3, round(bar_h * 0.14)))
    img.alpha_composite(layer)


# Where the ghost ends up on the canvas: (x, y, w, h) after resizing.
# Its bottom (y + h = 955) sinks below the car body's top edge (928),
# so the car drawn afterwards hides the disc's lower arc and the ghost
# reads as rising out of the cabin instead of floating behind the car.
GHOST_BOX = (300, 455, GHOST_HEIGHT, GHOST_HEIGHT)


def place_ghost(img: Image.Image) -> None:
    ghost = Image.open(GHOST_PATH).convert("RGBA")
    ghost = ghost.resize((GHOST_HEIGHT, GHOST_HEIGHT), Image.LANCZOS)
    # Soft shadow so the ghost sits in the scene instead of floating.
    shadow = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    shade = ghost.split()[3].point(lambda a: int(a * 0.45))
    dark = Image.new("RGBA", ghost.size, (12, 2, 24, 255))
    dark.putalpha(shade)
    shadow.alpha_composite(dark, (GHOST_BOX[0] + 14, GHOST_BOX[1] + 18))
    img.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(10)))
    img.alpha_composite(ghost, (GHOST_BOX[0], GHOST_BOX[1]))


def caption(draw: ImageDraw.ImageDraw, text: str, y: int, size: int) -> None:
    draw.text((SIZE // 2, y), text, font=font(size), anchor="mm",
              fill=(255, 255, 255), stroke_width=7, stroke_fill=(5, 2, 10))


def build() -> None:
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 255))
    # sky_gradient works on RGB pixels; do it on an RGB copy then paste.
    rgb = Image.new("RGB", (SIZE, SIZE))
    sky_gradient(rgb)
    img.paste(rgb, (0, 0))
    draw = ImageDraw.Draw(img)
    draw_sun(draw)
    draw_clouds(img)
    draw = ImageDraw.Draw(img)
    draw_billboard(draw)
    draw_palm(draw, 1064, 430, -64, 1.0)
    draw_palm(draw, 60, 520, 44, 0.72)
    draw_boulevard(draw)
    place_ghost(img)          # ghost first...
    draw = ImageDraw.Draw(img)
    draw_car(draw)             # ...car over its base, so it sits inside
    draw_sunglasses(img)
    draw = ImageDraw.Draw(img)
    caption(draw, TOP_CAPTION, 62, 56)
    caption(draw, BOTTOM_CAPTION, 1132, 54)
    img.convert("RGB").save(OUT_PATH, format="PNG")
    print(f"wrote {OUT_PATH}")


if __name__ == "__main__":
    build()
