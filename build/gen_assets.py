"""Regenerates AURA' app icon + NSIS installer artwork.

The mark is the arc reactor from the HUD: armored shield housing, cyan glass,
triangular core. Keep the BMP dimensions exactly as they are — 150x57 and
164x314 are NSIS's fixed slots for the header banner and welcome sidebar.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math, os

HERE = os.path.dirname(os.path.abspath(__file__))

# AURA palette: deep indigo surfaces, violet light
CYAN      = (154, 124, 255)    # accent (violet) — name kept for call-site compatibility
CYAN_LITE = (223, 214, 255)
STEEL     = (122, 126, 200)
STEEL_DK  = (36, 34, 82)
NAVY      = (24, 21, 69)
BG_DARK   = (5, 5, 14)
BG_DARK2  = (20, 26, 68)

FONT_BOLD = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
FONT_SEMI = "/usr/share/fonts/truetype/google-fonts/Poppins-SemiBold.ttf"
if not os.path.exists(FONT_SEMI):
    FONT_SEMI = FONT_BOLD if os.path.exists(FONT_BOLD) else None

# Mobius hologram geometry — same parametric surface as the renderer
import math as _m
BAND, CAM = 0.52, 3.4

def _mobius(u, v):
    h = u / 2.0
    r = 1 + v * BAND * _m.cos(h)
    return (r * _m.cos(u), r * _m.sin(u), v * BAND * _m.sin(h))

def _xf(p, ax, ay):
    x, y, z = p
    x1 =  x * _m.cos(ay) + z * _m.sin(ay)
    z1 = -x * _m.sin(ay) + z * _m.cos(ay)
    y2 =  y * _m.cos(ax) - z1 * _m.sin(ax)
    z2 =  y * _m.sin(ax) + z1 * _m.cos(ax)
    return (x1, y2, z2)

def _proj(p, s, cx, cy):
    k = CAM / (CAM - p[2])
    return (cx + p[0] * s * k, cy + p[1] * s * k)

def _edge(v, s, cx, cy, tilt=0.62, spin=0.85, steps=120):
    return [_proj(_xf(_mobius(i / steps * 2 * _m.pi, v), tilt, spin), s, cx, cy)
            for i in range(steps + 1)]

def radial_bg(size, c1, c2, center=None):
    w, h = size
    img = Image.new("RGB", size, c2)
    if center is None:
        center = (w // 2, int(h * 0.15))
    maxd = math.hypot(max(center[0], w - center[0]), max(center[1], h - center[1]))
    px = img.load()
    for y in range(h):
        for x in range(w):
            d = min(1, math.hypot(x - center[0], y - center[1]) / maxd)
            px[x, y] = tuple(int(c1[i] + (c2[i] - c1[i]) * d) for i in range(3))
    return img

def draw_reactor(img, cx, cy, size):
    """Draws the Mobius hologram. size = radius in px."""
    d = ImageDraw.Draw(img)
    s = size / 1.5
    inner, outer = _edge(-1, s, cx, cy), _edge(1, s, cx, cy)
    # ribbon body: connect the two edges so it reads as a solid band
    if size > 26:
        step = max(1, len(inner) // 40)
        for i in range(0, len(inner) - step, step):
            d.polygon([inner[i], inner[i + step], outer[i + step], outer[i]],
                      fill=(104, 100, 214, 168))
    w = max(1, int(size * 0.055))
    d.line(inner, fill=CYAN_LITE, width=w, joint="curve")
    d.line(outer, fill=CYAN_LITE, width=w, joint="curve")
    if size > 26:
        ring = [_proj(_xf((_m.cos(i / 80 * 2 * _m.pi) * 1.52, _m.sin(i / 80 * 2 * _m.pi) * 1.52, 0), 0.62, 0.3), s, cx, cy)
                for i in range(81)]
        d.line(ring, fill=STEEL, width=max(1, int(size * 0.02)))
    return img


def reactor_composite(size_px, cx, cy, size):
    base = Image.new("RGBA", size_px, (0, 0, 0, 0))
    glow = Image.new("RGBA", size_px, (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    s = size / 1.5
    for v in (-1, 1):
        gd.line(_edge(v, s, cx, cy), fill=CYAN + (190,), width=max(3, int(size * 0.22)), joint="curve")
    glow = glow.filter(ImageFilter.GaussianBlur(max(2, int(size * 0.20))))
    base = Image.alpha_composite(base, glow)
    layer = Image.new("RGBA", size_px, (0, 0, 0, 0))
    draw_reactor(layer, cx, cy, size)
    return Image.alpha_composite(base, layer)


def draw_tracked(draw, xy, text, font, fill, tracking=0, anchor="la"):
    widths = [draw.textlength(ch, font=font) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x, y = xy
    if anchor == "ma":
        x -= total / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=font, fill=fill)
        x += w + tracking

def font(path, sz):
    try:
        return ImageFont.truetype(path, sz)
    except Exception:
        return ImageFont.load_default()

# ---------------- App icon ----------------
S = 256
icon = Image.new("RGBA", (S, S), (0, 0, 0, 0))
bg = Image.new("RGBA", (S, S), (0, 0, 0, 0))
ImageDraw.Draw(bg).ellipse([3, 3, S - 3, S - 3], fill=(8, 8, 22, 255))
icon = Image.alpha_composite(icon, bg)
icon = Image.alpha_composite(icon, reactor_composite((S, S), S // 2, S // 2 + 4, int(S * 0.40)))
ImageDraw.Draw(icon).ellipse([3, 3, S - 3, S - 3], outline=CYAN, width=4)
icon.save(os.path.join(HERE, "icon_256.png"))
icon.save(os.path.join(HERE, "icon.ico"), sizes=[(s, s) for s in (16, 24, 32, 48, 64, 128, 256)])

# ---------------- Installer header (150x57) ----------------
HW, HH = 150, 57
header = radial_bg((HW, HH), BG_DARK2, BG_DARK, center=(30, HH // 2)).convert("RGBA")
header = Image.alpha_composite(header, reactor_composite((HW, HH), 28, HH // 2, 20)).convert("RGB")
draw_tracked(ImageDraw.Draw(header), (56, HH // 2 - 12), "AURA", font(FONT_SEMI, 20), (226, 222, 255), tracking=3)
header.save(os.path.join(HERE, "installerHeader.bmp"), "BMP")

# ---------------- Installer sidebar (164x314) ----------------
SW, SH = 164, 314
sidebar = radial_bg((SW, SH), BG_DARK2, BG_DARK, center=(SW // 2, int(SH * 0.34))).convert("RGBA")
sidebar = Image.alpha_composite(sidebar, reactor_composite((SW, SH), SW // 2, int(SH * 0.34), 56)).convert("RGB")
sd = ImageDraw.Draw(sidebar)
f_big, f_small = font(FONT_SEMI, 22), font(FONT_BOLD, 8)
draw_tracked(sd, (SW // 2, int(SH * 0.34) + 74), "AURA", f_big, (226, 222, 255), tracking=6, anchor="ma")
draw_tracked(sd, (SW // 2, int(SH * 0.34) + 110), "PERSONAL AI ASSISTANT", f_small, (122, 120, 178), tracking=1, anchor="ma")
sd.line([(24, SH - 34), (SW - 24, SH - 34)], fill=(79, 211, 245), width=1)
sd.text((SW // 2, SH - 20), "v1.8.0", font=f_small, fill=(96, 92, 150), anchor="mm")
sidebar.save(os.path.join(HERE, "installerSidebar.bmp"), "BMP")

print("done:", sorted(os.listdir(HERE)))
