#!/usr/bin/env python3
"""Render THE SUNDAY GAZETTE — news-image-20261122 v1 (build-time only; PIL ok here).
main.py (the graded entrypoint) is stdlib-only and just copies entry.png.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BASE = os.path.dirname(os.path.abspath(__file__))
F = os.path.join(BASE, "fonts")
PAPER = (246, 241, 231)
INK = (26, 26, 26)
RED = (163, 30, 30)
BLUE = (31, 68, 110)
TEAL = (24, 90, 86)
GOLD = (176, 124, 30)
PANEL = (255, 253, 246)
GREY = (110, 108, 100)
LIGHT = (232, 226, 212)

def font(name, size):
    return ImageFont.truetype(os.path.join(F, name), size)

SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img, "RGBA")

def wrap(text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if fnt.getlength(t) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def text(x, y, s, fnt, fill=INK, anchor="la"):
    d.text((x, y), s, font=fnt, fill=fill, anchor=anchor)

def para(x, y, s, fnt, width, fill=INK, leading=None, max_lines=None):
    lines = wrap(s, fnt, width)
    if max_lines:
        lines = lines[:max_lines]
    lh = leading or int(fnt.size * 1.22)
    for i, ln in enumerate(lines):
        d.text((x, y + i * lh), ln, font=fnt, fill=fill)
    return y + len(lines) * lh

def chip(x, y, s, fnt, bg=INK, fg=(255, 253, 246), pad=4):
    w = fnt.getlength(s) + pad * 2
    h = fnt.size + pad * 2 - 2
    d.rounded_rectangle([x, y, x + w, y + h], radius=3, fill=bg)
    d.text((x + pad, y + pad - 1), s, font=fnt, fill=fg)
    return w

def sky(x, y, w, h, top, bot):
    for i in range(h):
        t = i / max(1, h - 1)
        c = tuple(int(top[k] + (bot[k] - top[k]) * t) for k in range(3))
        d.line([(x, y + i), (x + w, y + i)], fill=c)

def sun(x, y, r, core=(255, 236, 180), halo=(255, 214, 120)):
    d.ellipse([x - r - 14, y - r - 14, x + r + 14, y + r + 14], fill=halo + (60,))
    d.ellipse([x - r, y - r, x + r, y + r], fill=core)

def flame(x, y, s=1.0):
    # stylised flame: outer orange, inner yellow, core white
    d.polygon([(x, y - 26 * s), (x + 11 * s, y - 4 * s), (x + 7 * s, y + 8 * s),
               (x - 7 * s, y + 8 * s), (x - 11 * s, y - 4 * s)], fill=(230, 110, 30))
    d.polygon([(x, y - 16 * s), (x + 7 * s, y - 1 * s), (x + 4 * s, y + 8 * s),
               (x - 4 * s, y + 8 * s), (x - 7 * s, y - 1 * s)], fill=(245, 190, 60))
    d.ellipse([x - 3.5 * s, y - 2 * s, x + 3.5 * s, y + 8 * s], fill=(255, 240, 180))

def smoke(x, y, s=1.0, col=(90, 88, 84)):
    for dx, dy, r in [(0, 0, 9), (8, -9, 11), (-7, -16, 12), (3, -26, 13), (-4, -36, 12)]:
        d.ellipse([x + dx * s - r * s, y + dy * s - r * s,
                   x + dx * s + r * s, y + dy * s + r * s], fill=col + (150,))

def panel(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=PANEL, outline=INK, width=1)

# ---------------------------------------------------------------- masthead
d.line([(8, 10), (1016, 10)], fill=INK, width=2)
text(512, 16, "THE SUNDAY GAZETTE", SERIF_B(46), anchor="ma")
text(8, 64, "SUNDAY 22 NOVEMBER 2026", SANS_B(13))
text(1016, 64, "40 STORIES  •  5 CONTINENTS", SANS_B(13), anchor="ra")
d.line([(8, 82), (1016, 82)], fill=INK, width=3)
d.line([(8, 86), (1016, 86)], fill=INK, width=1)

# ---------------------------------------------------------------- leads
LX = [8, 344, 680]
LW = 328
LY, LH = 92, 200

def lead_head(x, y, w, kicker, head, sub):
    chip(x, y, kicker, SANS_B(11), bg=RED)
    para(x, y + 24, head, SERIF_B(16), w, leading=19, max_lines=2)
    para(x, y + 64, sub, SANS(10), w, leading=13, max_lines=2)

# --- LEAD 1: COP31 conference hall, dawn light through windows
x, y = LX[0], LY
panel(x, y, LW, LH)
hx, hy, hw, hh = x + 1, y + 1, LW - 2, 112
sky(hx, hy, hw, hh, (58, 74, 96), (214, 176, 120))
# tall windows with warm dawn light
for i, wx in enumerate([14, 62, 110, 158, 206, 254]):
    d.rectangle([hx + wx, hy + 10, hx + wx + 34, hy + 62], fill=(255, 214, 130), outline=(40, 40, 40), width=2)
    d.line([(hx + wx + 17, hy + 10), (hx + wx + 17, hy + 62)], fill=(40, 40, 40), width=1)
# floor + delegate rows (backs of heads, one natural light)
d.rectangle([hx, hy + 62, hx + hw, hy + hh], fill=(74, 66, 58))
for row, ry in enumerate([70, 84, 98]):
    for cx in range(18, hw - 10, 26):
        d.ellipse([hx + cx, hy + ry, hx + cx + 16, hy + ry + 15], fill=(30, 28, 26) if row % 2 else (52, 48, 44))
        d.rectangle([hx + cx - 2, hy + ry + 14, hx + cx + 18, hy + ry + 20], fill=(30, 28, 26) if row % 2 else (52, 48, 44))
# screen: draft with fossil fuels crossed out
d.rectangle([hx + 96, hy + 66, hx + 232, hy + 112], fill=(250, 248, 240), outline=INK, width=2)
text(hx + 164, hy + 70, "DRAFT TEXT", SANS_B(9), anchor="ma")
text(hx + 164, hy + 82, "NO MENTION OF", SANS_B(10), anchor="ma")
text(hx + 164, hy + 94, "FOSSIL FUELS", SANS_B(11), fill=RED, anchor="ma")
# countdown clock chip
chip(hx + 8, hy + 8, "VOTE 06:00 GMT TODAY", SANS_B(10), bg=RED)
lead_head(x, y + 110, LW - 4, "LEAD 1  •  CLIMATE  •  ANTALYA",
          "COP31: DEAL ON THE TABLE — VOTE DUE TODAY",
          "Africa rejects funding; still no fossil-fuel mention.")

# --- LEAD 2: the Gulf at night — Bahrain flame, tankers, missile arcs
x, y = LX[1], LY
panel(x, y, LW, LH)
hx, hy, hw, hh = x + 1, y + 1, LW - 2, 112
sky(hx, hy, hw, hh, (16, 22, 38), (52, 62, 84))
# stars
for sx, sy in [(20, 12), (60, 22), (120, 8), (180, 18), (240, 10), (300, 24), (90, 30), (270, 34)]:
    d.ellipse([hx + sx, hy + sy, hx + sx + 2, hy + sy + 2], fill=(255, 255, 255))
# sea
d.rectangle([hx, hy + 62, hx + hw, hy + hh], fill=(24, 44, 66))
for wx in range(0, hw, 34):
    d.line([(hx + wx, hy + 96), (hx + wx + 18, hy + 96)], fill=(90, 130, 160), width=2)
# Bahrain flame (left)
d.rectangle([hx + 18, hy + 46, hx + 52, hy + 62], fill=(60, 58, 52))
flame(hx + 35, hy + 44, 0.9)
text(hx + 35, hy + 100, "BAHRAIN", SANS_B(9), fill=(255, 220, 160), anchor="ma")
# tanker 1 (centre, bow hit, smoke)
d.rectangle([hx + 120, hy + 66, hx + 210, hy + 82], fill=(120, 40, 30), outline=INK, width=1)
d.rectangle([hx + 196, hy + 54, hx + 206, hy + 66], fill=(90, 88, 84))
smoke(hx + 130, hy + 60, 0.7)
flame(hx + 128, hy + 64, 0.6)
text(hx + 165, hy + 100, "HORMUZ: 2 TANKERS HIT", SANS_B(9), fill=(255, 220, 160), anchor="ma")
# missile arcs over Riyadh (right)
for k, (ax, ay) in enumerate([(252, 30), (268, 22), (284, 28)]):
    d.line([(hx + ax - 18, hy + ay + 12), (hx + ax + 2, hy + ay - 2)], fill=(255, 190, 90), width=2)
    d.ellipse([hx + ax - 2, hy + ay - 5, hx + ax + 4, hy + ay + 1], fill=(255, 220, 140))
text(hx + 268, hy + 100, "RIYADH", SANS_B(9), fill=(255, 220, 160), anchor="ma")
lead_head(x, y + 110, LW - 4, "LEAD 2  •  WAR  •  THE GULF",
          "THE GULF IGNITES — BAHRAIN, HORMUZ, RIYADH",
          "Iran hits Bahrain; 2 tankers struck; 3 missiles down.")

# --- LEAD 3: Bitcoin chart — fall to $55,130, bounce through $60,000
x, y = LX[2], LY
panel(x, y, LW, LH)
hx, hy, hw, hh = x + 1, y + 1, LW - 2, 112
d.rectangle([hx, hy, hx + hw, hy + hh], fill=(18, 26, 34))
# grid
for gy in range(hy + 16, hy + hh, 22):
    d.line([(hx + 8, gy), (hx + hw - 8, gy)], fill=(60, 72, 84), width=1)
# dashed $60,000 threshold
for gx in range(hx + 10, hx + hw - 10, 12):
    d.line([(gx, hy + 34), (gx + 7, hy + 34)], fill=(255, 200, 90), width=2)
text(hx + 12, hy + 20, "$60,000", SANS_B(10), fill=(255, 200, 90))
# chart line: 59k -> 55,130 low -> 60,207
pts = [(14, 52), (60, 58), (100, 72), (140, 96), (180, 104), (220, 88), (260, 56), (300, 34)]
pts = [(hx + px, hy + py) for px, py in pts]
d.line(pts, fill=(90, 220, 160), width=3, joint="curve")
d.ellipse([pts[4][0] - 4, pts[4][1] - 4, pts[4][0] + 4, pts[4][1] + 4], fill=(255, 90, 70), outline=(255, 255, 255), width=1)
_lx = hx + 12
text(_lx, hy + 100, "SAT LOW $55,130", SANS_B(9), fill=(255, 140, 120))
text(_lx + SANS_B(9).getlength("SAT LOW $55,130"), hy + 100, "  \u2022  SUN 22 NOV  \u2022  FEAR & GREED 11", SANS_B(9), fill=(200, 210, 220))
d.ellipse([pts[-1][0] - 4, pts[-1][1] - 4, pts[-1][0] + 4, pts[-1][1] + 4], fill=(90, 220, 160), outline=(255, 255, 255), width=1)
text(pts[-1][0] - 66, pts[-1][1] - 16, "$60,207", SANS_B(10), fill=(90, 220, 160))
lead_head(x, y + 110, LW - 4, "LEAD 3  •  MARKETS  •  CRYPTO",
          "BITCOIN BACK ABOVE $60,000",
          "After Saturday's two-year low, the bounce.")

# ---------------------------------------------------------------- tiles
TX = [8, 262, 516, 770]
TW = 246
TY = [300, 454, 608]
TH = 144

def tile(x, y, w, place, head, sub, src):
    panel(x, y, w, TH)
    ix, iy, iw, ih = x + 1, y + 1, w - 2, 88
    return ix, iy, iw, ih

def tile_text(x, y, w, head, sub, src):
    para(x + 6, y + 94, head, SANS_B(12), w - 12, leading=14, max_lines=2)
    para(x + 6, y + 122, sub, SANS(10), w - 60, leading=12, max_lines=1)
    text(x + w - 6, y + 124, src, SANS_B(8), fill=GREY, anchor="ra")

def place_tag(ix, iy, s):
    chip(ix + 5, iy + 5, s, SANS_B(9), bg=INK)

def person(ix, iy, px, py, s=1.0, skin=(214, 164, 120), shirt=(60, 90, 140)):
    d.ellipse([ix + px - 7 * s, iy + py - 8 * s, ix + px + 7 * s, iy + py + 8 * s], fill=skin)
    d.polygon([(ix + px - 11 * s, iy + py + 22 * s), (ix + px - 8 * s, iy + py + 7 * s),
               (ix + px + 8 * s, iy + py + 7 * s), (ix + px + 11 * s, iy + py + 22 * s)], fill=shirt)

# ---- ROW A
# T4 Indonesia factory fire
x, y = TX[0], TY[0]
ix, iy, iw, ih = tile(x, y, TW, None, None, None, None)
sky(ix, iy, iw, ih, (44, 40, 44), (150, 90, 60))
smoke(ix + 120, iy + 44, 0.8)
d.rectangle([ix, iy + 58, ix + iw, iy + ih], fill=(58, 50, 46))
d.rectangle([ix + 20, iy + 34, ix + 130, iy + 66], fill=(96, 84, 70), outline=INK, width=2)
d.rectangle([ix + 34, iy + 44, ix + 52, iy + 66], fill=(255, 170, 60))
d.rectangle([ix + 66, iy + 44, ix + 84, iy + 66], fill=(255, 170, 60))
d.rectangle([ix + 98, iy + 44, ix + 116, iy + 66], fill=(255, 170, 60))
flame(ix + 43, iy + 42, 0.8); flame(ix + 75, iy + 42, 0.8); flame(ix + 107, iy + 42, 0.8)
d.rectangle([ix + 150, iy + 52, ix + 226, iy + 66], fill=(150, 40, 30))
text(ix + 188, iy + 68, "RESCUE ONGOING", SANS_B(9), fill=(255, 220, 160), anchor="ma")
place_tag(ix, iy, "CIKANDE, INDONESIA")
tile_text(x, y, TW, "FACTORY FIRE: 3 DEAD, 36 MISSING",
          "Search goes on after the blaze", "REUTERS")

# T5 F1 Las Vegas
x, y = TX[1], TY[0]
ix, iy, iw, ih = tile(x, y, TW, None, None, None, None)
sky(ix, iy, iw, ih, (20, 16, 44), (90, 40, 110))
sun(ix + 205, iy + 22, 12, core=(255, 200, 120))
d.rectangle([ix, iy + 58, ix + iw, iy + ih], fill=(40, 38, 44))
for bx in range(0, iw, 24):
    d.line([(ix + bx, iy + 58), (ix + bx, iy + 88)], fill=(255, 210, 90), width=1)
# three race cars with light trails
for cx, cy, col in [(40, 66, (220, 30, 30)), (110, 74, (40, 120, 220)), (180, 70, (240, 240, 240))]:
    d.line([(ix + cx - 34, iy + cy + 4), (ix + cx, iy + cy + 4)], fill=(255, 220, 120), width=2)
    d.polygon([(ix + cx - 16, iy + cy), (ix + cx + 14, iy + cy), (ix + cx + 18, iy + cy + 8),
               (ix + cx - 18, iy + cy + 8)], fill=col, outline=INK, width=1)
    d.ellipse([ix + cx - 10, iy + cy + 8, ix + cx - 4, iy + cy + 14], fill=INK)
    d.ellipse([ix + cx + 6, iy + cy + 8, ix + cx + 12, iy + cy + 14], fill=INK)
chip(ix + iw - 108, iy + 6, "RACE UNDERWAY", SANS_B(10), bg=RED)
place_tag(ix, iy, "LAS VEGAS")
tile_text(x, y, TW, "F1: VERSTAPPEN LEADS, LAP 22/50",
          "No winner yet — race still running", "SPORTS")

# T6 Catherine, Princess of Wales
x, y = TX[2], TY[0]
ix, iy, iw, ih = tile(x, y, TW, None, None, None, None)
sky(ix, iy, iw, ih, (120, 140, 160), (220, 205, 185))
sun(ix + 200, iy + 20, 14)
d.rectangle([ix, iy + 60, ix + iw, iy + ih], fill=(110, 96, 80))
# documentary camera on tripod
d.rectangle([ix + 24, iy + 30, ix + 66, iy + 52], fill=(40, 40, 44), outline=INK, width=1)
d.ellipse([ix + 62, iy + 34, ix + 74, iy + 48], fill=(150, 190, 220), outline=INK, width=1)
d.line([(ix + 45, iy + 52), (ix + 34, iy + 86)], fill=INK, width=3)
d.line([(ix + 45, iy + 52), (ix + 56, iy + 86)], fill=INK, width=3)
d.line([(ix + 45, iy + 52), (ix + 45, iy + 86)], fill=INK, width=3)
# seated figure, warm side light
person(ix, iy, 150, 42, 1.6, skin=(216, 170, 128), shirt=(96, 60, 90))
d.ellipse([ix + 128, iy + 28, ix + 172, iy + 56], fill=(70, 50, 40))
d.ellipse([ix + 134, iy + 32, ix + 166, iy + 54], fill=(216, 170, 128))
place_tag(ix, iy, "LONDON")
tile_text(x, y, TW, "CATHERINE SPEAKS OPENLY ON CANCER",
          "In a new BBC documentary", "BBC")

# T7 teen gamer helps FBI
x, y = TX[3], TY[0]
ix, iy, iw, ih = tile(x, y, TW, None, None, None, None)
sky(ix, iy, iw, ih, (30, 44, 70), (90, 110, 150))
# game screen glow
d.rectangle([ix + 130, iy + 12, ix + 228, iy + 62], fill=(16, 22, 34), outline=(120, 180, 255), width=2)
d.rectangle([ix + 138, iy + 20, ix + 178, iy + 54], fill=(40, 90, 160))
d.polygon([(ix + 150, iy + 26), (ix + 166, iy + 54), (ix + 150, iy + 54)], fill=(255, 220, 120))
d.polygon([(ix + 196, iy + 26), (ix + 210, iy + 40), (ix + 196, iy + 54)], fill=(120, 220, 120))
text(ix + 179, iy + 64, "ONLINE GAME", SANS_B(8), fill=(180, 210, 240), anchor="ma")
# teen with headset
person(ix, iy, 66, 40, 1.5, skin=(214, 164, 120), shirt=(40, 120, 90))
d.arc([ix + 52, iy + 28, ix + 80, iy + 50], 180, 360, fill=INK, width=3)
d.rectangle([ix + 50, iy + 38, ix + 56, iy + 48], fill=INK)
d.rectangle([ix + 76, iy + 38, ix + 82, iy + 48], fill=INK)
# FBI badge chip
chip(ix + 96, iy + 70, "FBI", SANS_B(11), bg=(31, 68, 110))
place_tag(ix, iy, "USA")
tile_text(x, y, TW, "TEEN GAMER, 16, HELPS FBI SAVE MISSING GIRL",
          "They met in an online game", "BBC")

# ---- ROW B
# T8 US denies F-16 claim
x, y = TX[0], TY[1]
ix, iy, iw, ih = tile(x, y, TW, None, None, None, None)
sky(ix, iy, iw, ih, (24, 34, 56), (120, 130, 150))
sun(ix + 30, iy + 20, 12)
# jet silhouette
d.polygon([(ix + 90, iy + 44), (ix + 170, iy + 44), (ix + 190, iy + 50), (ix + 170, iy + 56),
           (ix + 90, iy + 56), (ix + 100, iy + 50)], fill=(60, 64, 70))
d.polygon([(ix + 120, iy + 44), (ix + 132, iy + 30), (ix + 140, iy + 44)], fill=(60, 64, 70))
d.polygon([(ix + 120, iy + 56), (ix + 132, iy + 70), (ix + 140, iy + 56)], fill=(60, 64, 70))
d.line([(ix + 60, iy + 50), (ix + 90, iy + 50)], fill=(200, 210, 220), width=2)
# duelling claim labels
chip(ix + 12, iy + 66, "IRAN: JET HIT", SANS_B(9), bg=RED)
chip(ix + 128, iy + 66, "US: NOT HIT", SANS_B(9), bg=BLUE)
place_tag(ix, iy, "THE GULF")
tile_text(x, y, TW, "US DENIES IRAN CLAIM OF F-16 HIT",
          "Tehran said a missile hit the jet", "CNA")

# T9 England rugby record win
x, y = TX[1], TY[1]
ix, iy, iw, ih = tile(x, y, TW, None, None, None, None)
sky(ix, iy, iw, ih, (90, 130, 90), (190, 215, 170))
d.rectangle([ix, iy + 58, ix + iw, iy + ih], fill=(52, 110, 62))
for gy in range(iy + 62, iy + ih, 10):
    d.line([(ix, gy), (ix + iw, gy)], fill=(70, 130, 78), width=1)
d.line([(ix + 120, iy + 58), (ix + 120, iy + 88)], fill=(255, 255, 255), width=2)
# rugby ball mid-flight + posts
d.ellipse([ix + 88, iy + 26, ix + 148, iy + 52], fill=(200, 170, 110), outline=INK, width=2)
d.line([(ix + 118, iy + 26), (ix + 118, iy + 52)], fill=INK, width=2)
d.line([(ix + 196, iy + 18), (ix + 196, iy + 58)], fill=(255, 255, 255), width=3)
d.line([(ix + 226, iy + 18), (ix + 226, iy + 58)], fill=(255, 255, 255), width=3)
d.line([(ix + 196, iy + 40), (ix + 226, iy + 40)], fill=(255, 255, 255), width=3)
person(ix, iy, 60, 52, 1.4, skin=(200, 150, 110), shirt=(255, 255, 255))
place_tag(ix, iy, "LONDON")
tile_text(x, y, TW, "ENGLAND'S RECORD WIN OVER NEW ZEALAND",
          "Nations Championship", "BBC")

# T10 France into final
x, y = TX[2], TY[1]
ix, iy, iw, ih = tile(x, y, TW, None, None, None, None)
sky(ix, iy, iw, ih, (70, 90, 150), (200, 205, 220))
d.rectangle([ix, iy + 58, ix + iw, iy + ih], fill=(52, 110, 62))
# two flags facing off
d.rectangle([ix + 24, iy + 18, ix + 92, iy + 54], fill=(255, 255, 255), outline=INK, width=1)
d.rectangle([ix + 24, iy + 18, ix + 47, iy + 54], fill=(0, 60, 160))
d.rectangle([ix + 70, iy + 18, ix + 92, iy + 54], fill=(220, 40, 40))
d.rectangle([ix + 154, iy + 18, ix + 222, iy + 54], fill=(0, 110, 60), outline=INK, width=1)
text(ix + 188, iy + 26, "SA", SANS_B(16), fill=(255, 220, 60), anchor="ma")
text(ix + 123, iy + 24, "VS", SERIF_B(18), anchor="ma")
d.ellipse([ix + 88, iy + 60, ix + 148, iy + 86], fill=(200, 170, 110), outline=INK, width=2)
place_tag(ix, iy, "PARIS")
tile_text(x, y, TW, "FRANCE INTO FINAL VS SPRINGBOKS",
          "Nations final next weekend", "BBC")

# T11 Washington hair $4,000
x, y = TX[3], TY[1]
ix, iy, iw, ih = tile(x, y, TW, None, None, None, None)
sky(ix, iy, iw, ih, (120, 100, 80), (215, 195, 160))
sun(ix + 210, iy + 20, 12)
d.rectangle([ix, iy + 60, ix + iw, iy + ih], fill=(120, 88, 60))
# auction podium + gavel
d.rectangle([ix + 30, iy + 44, ix + 130, iy + 66], fill=(90, 66, 44), outline=INK, width=1)
d.rectangle([ix + 44, iy + 66, ix + 116, iy + 74], fill=(70, 50, 34))
d.polygon([(ix + 150, iy + 40), (ix + 190, iy + 28), (ix + 196, iy + 36), (ix + 156, iy + 48)], fill=(60, 44, 30))
d.line([(ix + 178, iy + 42), (ix + 196, iy + 62)], fill=(60, 44, 30), width=4)
# framed hair lock + price tag
d.rectangle([ix + 160, iy + 52, ix + 220, iy + 84], fill=(250, 248, 240), outline=(176, 124, 30), width=2)
d.arc([ix + 176, iy + 56, ix + 204, iy + 80], 0, 360, fill=(120, 100, 70), width=2)
text(ix + 190, iy + 58, "$4,000", SANS_B(11), fill=RED, anchor="ma")
place_tag(ix, iy, "USA")
tile_text(x, y, TW, "A LOCK OF WASHINGTON'S HAIR: $4,000",
          "Sold at auction", "BBC")

# ---- ROW C
# T12 Peter Fluck obituary
x, y = TX[0], TY[2]
ix, iy, iw, ih = tile(x, y, TW, None, None, None, None)
sky(ix, iy, iw, ih, (60, 60, 80), (180, 170, 160))
d.rectangle([ix, iy + 56, ix + iw, iy + ih], fill=(70, 60, 58))
# puppet theatre stage
d.rectangle([ix + 60, iy + 14, ix + 186, iy + 66], fill=(140, 30, 30), outline=INK, width=2)
d.rectangle([ix + 66, iy + 20, ix + 180, iy + 60], fill=(30, 28, 34))
d.ellipse([ix + 104, iy + 28, ix + 142, iy + 58], fill=(216, 170, 128))
d.ellipse([ix + 112, iy + 38, ix + 120, iy + 44], fill=INK)
d.ellipse([ix + 126, iy + 38, ix + 134, iy + 44], fill=INK)
d.arc([ix + 112, iy + 44, ix + 134, iy + 56], 0, 180, fill=INK, width=2)
d.rectangle([ix + 60, iy + 62, ix + 186, iy + 70], fill=(176, 124, 30))
place_tag(ix, iy, "LONDON")
tile_text(x, y, TW, "SPITTING IMAGE CO-CREATOR DIES AT 85",
          "Peter Fluck, satirist", "BBC")

# T13 Bradford councillor stabbed
x, y = TX[1], TY[2]
ix, iy, iw, ih = tile(x, y, TW, None, None, None, None)
sky(ix, iy, iw, ih, (100, 110, 130), (200, 200, 195))
d.rectangle([ix, iy + 56, ix + iw, iy + ih], fill=(90, 88, 84))
# courthouse columns
for cx in [30, 80, 130, 180]:
    d.rectangle([ix + cx, iy + 18, ix + cx + 18, iy + 62], fill=(220, 214, 198), outline=INK, width=1)
d.rectangle([ix + 18, iy + 10, ix + 212, iy + 20], fill=(200, 192, 172), outline=INK, width=1)
d.rectangle([ix + 18, iy + 62, ix + 212, iy + 70], fill=(200, 192, 172), outline=INK, width=1)
chip(ix + 66, iy + 76, "CHARGED", SANS_B(10), bg=RED)
place_tag(ix, iy, "BRADFORD")
tile_text(x, y, TW, "MAN CHARGED AFTER COUNCILLOR STABBED",
          "Attempted murder charge", "BBC")

# T14 Iraq Hartha power plant fire
x, y = TX[2], TY[2]
ix, iy, iw, ih = tile(x, y, TW, None, None, None, None)
sky(ix, iy, iw, ih, (50, 44, 44), (160, 100, 60))
smoke(ix + 150, iy + 44, 0.8)
d.rectangle([ix, iy + 58, ix + iw, iy + ih], fill=(62, 54, 48))
# cooling towers + plant
d.polygon([(ix + 30, iy + 30), (ix + 44, iy + 30), (ix + 48, iy + 62), (ix + 26, iy + 62)], fill=(180, 172, 158), outline=INK, width=1)
d.polygon([(ix + 80, iy + 30), (ix + 94, iy + 30), (ix + 98, iy + 62), (ix + 76, iy + 62)], fill=(180, 172, 158), outline=INK, width=1)
d.rectangle([ix + 130, iy + 40, ix + 210, iy + 62], fill=(96, 84, 70), outline=INK, width=1)
flame(ix + 150, iy + 38, 0.9); flame(ix + 190, iy + 38, 0.7)
place_tag(ix, iy, "BASRA, IRAQ")
tile_text(x, y, TW, "POWER PLANT FIRE: 4 DEAD, 35 HURT",
          "Gas pipeline involved", "REUTERS")

# T15 Manipur toxic alcohol
x, y = TX[3], TY[2]
ix, iy, iw, ih = tile(x, y, TW, None, None, None, None)
sky(ix, iy, iw, ih, (70, 80, 90), (190, 185, 175))
d.rectangle([ix, iy + 56, ix + iw, iy + ih], fill=(110, 100, 88))
# bottles + hospital cross
for bx, bh in [(40, 34), (70, 44), (100, 30)]:
    d.rectangle([ix + bx, iy + 62 - bh, ix + bx + 16, iy + 62], fill=(40, 90, 50), outline=INK, width=1)
    d.rectangle([ix + bx + 5, iy + 54 - bh, ix + bx + 11, iy + 62 - bh], fill=(40, 90, 50))
d.rectangle([ix + 150, iy + 14, ix + 222, iy + 62], fill=(250, 250, 248), outline=INK, width=1)
d.rectangle([ix + 180, iy + 22, ix + 192, iy + 54], fill=RED)
d.rectangle([ix + 168, iy + 34, ix + 204, iy + 46], fill=RED)
place_tag(ix, iy, "MANIPUR, INDIA")
tile_text(x, y, TW, "TOXIC ALCOHOL: 11 DEAD, 180+ IN HOSPITAL",
          "Suspected methanol poisoning", "REUTERS")

# ---------------------------------------------------------------- market strip
MX, MY, MW, MH = 8, 760, 1008, 36
d.rectangle([MX, MY, MX + MW, MY + MH], fill=(24, 30, 38), outline=INK, width=1)
text(MX + 10, MY + 11, "MARKETS", SANS_B(13), fill=(255, 220, 140))
# mini falling sparkline for stocks
sx0, sy0 = MX + 108, MY + 8
d.line([(sx0, sy0 + 4), (sx0 + 18, sy0 + 8), (sx0 + 36, sy0 + 16), (sx0 + 54, sy0 + 22)],
       fill=(255, 120, 100), width=2)
text(MX + 178, MY + 11, "FRI 20 NOV CLOSE:  S&P 500 -3.70%  •  NASDAQ -5.28%  •  DOW -1.93%  •  ANT $88.91  •  BRENT $92.57",
     SANS_B(11), fill=(235, 235, 230))
text(MX + MW - 10, MY + 11, "BTC SUN 22 NOV $60,207", SANS_B(11), fill=(90, 220, 160), anchor="ra")

# ---------------------------------------------------------------- bottom band: map + ALSO
BY = 804
# ---- map panel
d.rectangle([8, BY, 560, 996], fill=PANEL, outline=INK, width=1)
text(16, BY + 6, "WHERE IT HAPPENED", SANS_B(13))
text(552, BY + 6, "12 PINS", SANS_B(11), fill=GREY, anchor="ra")
d.line([(16, BY + 24), (552, BY + 24)], fill=INK, width=1)

MAP_X, MAP_Y, MAP_W, MAP_H = 16, 834, 536, 128
LAT_TOP, LAT_BOT = 84.0, -58.0

def ll(lon, lat):
    px = MAP_X + (lon + 180.0) / 360.0 * MAP_W
    py = MAP_Y + (LAT_TOP - lat) / (LAT_TOP - LAT_BOT) * MAP_H
    return px, py

d.rectangle([MAP_X, MAP_Y, MAP_X + MAP_W, MAP_Y + MAP_H], fill=(222, 232, 235), outline=GREY, width=1)
# graticule
for lon in range(-150, 181, 30):
    x0, _ = ll(lon, 0)
    d.line([(x0, MAP_Y), (x0, MAP_Y + MAP_H)], fill=(200, 212, 216), width=1)
for lat in range(-30, 61, 30):
    _, y0 = ll(0, lat)
    d.line([(MAP_X, y0), (MAP_X + MAP_W, y0)], fill=(200, 212, 216), width=1)

NA = [(-168,66),(-162,60),(-158,58),(-152,60),(-145,60),(-140,60),(-135,58),(-130,54),(-126,49),(-124,40),(-120,34),(-114,29),(-110,24),(-105,20),(-100,17),(-95,16),(-92,15),(-88,13),(-85,11),(-82,9),(-80,8),(-79,9),(-83,9),(-87,13),(-90,14),(-91,18),(-90,21),(-87,21),(-84,24),(-82,28),(-81,31),(-80,32),(-76,35),(-75,39),(-73,41),(-70,42),(-68,44),(-65,44),(-60,46),(-55,47),(-60,50),(-65,50),(-65,55),(-60,55),(-55,52),(-60,49),(-64,58),(-68,58),(-72,62),(-78,62),(-85,66),(-90,68),(-95,69),(-110,68),(-125,70),(-140,70),(-155,71),(-165,68)]
SA = [(-79,9),(-77,4),(-80,-3),(-81,-6),(-78,-10),(-75,-15),(-72,-18),(-70,-24),(-70,-30),(-72,-37),(-73,-44),(-74,-50),(-70,-54),(-66,-55),(-68,-50),(-66,-45),(-62,-40),(-58,-34),(-52,-32),(-48,-28),(-41,-23),(-39,-17),(-35,-8),(-35,-5),(-38,-3),(-42,-2),(-48,0),(-52,4),(-55,6),(-59,8),(-62,10),(-66,11),(-71,12),(-75,10),(-77,7)]
AF = [(-6,35),(-10,31),(-15,27),(-17,21),(-17,15),(-16,12),(-13,8),(-8,5),(-4,5),(0,6),(4,6),(7,4),(9,4),(9,-1),(12,-5),(13,-10),(12,-15),(13,-19),(15,-23),(17,-28),(19,-33),(25,-34),(30,-31),(33,-26),(36,-21),(39,-16),(40,-11),(41,-5),(42,0),(46,4),(51,11),(48,11),(44,12),(42,12),(40,15),(38,18),(37,21),(35,24),(34,27),(33,30),(31,32),(28,32),(24,32),(20,32),(16,32),(12,33),(10,37),(6,37),(2,36),(-2,35)]
EU = [(-10,36),(-9,38),(-9,43),(-3,44),(-1,46),(-4,48),(-2,49),(0,51),(2,53),(5,53),(8,55),(8,57),(10,58),(6,58),(5,60),(6,62),(10,64),(12,66),(16,68),(20,70),(25,71),(29,71),(31,70),(30,68),(33,67),(36,66),(40,65),(43,63),(44,60),(44,57),(42,55),(39,53),(37,50),(35,47),(33,45),(30,46),(28,44),(26,43),(23,40),(22,38),(23,36),(26,36),(28,37),(30,36),(33,36),(36,36),(35,34),(33,31),(30,31),(30,36),(28,36),(26,38),(24,39),(22,40),(21,42),(19,43),(16,44),(13,45),(10,44),(8,43),(5,42),(3,42),(0,40),(-2,37),(-5,36),(-8,36)]
UK = [(-5,50),(-3,53),(-5,56),(-3,58),(-1,57),(0,53),(1,51),(-2,51)]
IE = [(-10,52),(-8,55),(-6,55),(-6,52),(-8,51)]
AS = [(29,41),(35,42),(40,44),(45,46),(50,48),(55,50),(60,52),(65,54),(70,57),(75,62),(80,66),(85,70),(90,72),(95,74),(100,75),(105,76),(110,75),(115,73),(120,72),(125,71),(130,71),(135,71),(140,72),(145,71),(150,70),(155,69),(160,67),(165,65),(170,66),(170,62),(165,60),(162,58),(160,55),(158,52),(156,50),(152,48),(148,45),(144,44),(142,41),(140,38),(138,35),(136,33),(134,31),(132,30),(130,28),(128,25),(126,23),(124,21),(122,19),(120,17),(118,15),(116,12),(114,10),(112,8),(110,5),(108,3),(106,1),(104,1),(102,3),(100,6),(99,9),(100,12),(102,14),(104,15),(106,17),(108,19),(106,21),(104,23),(102,24),(100,22),(98,20),(96,18),(94,17),(92,21),(90,22),(88,21),(86,20),(84,18),(82,16),(80,13),(79,9),(77,8),(76,10),(75,13),(74,17),(73,20),(71,21),(69,22),(67,24),(65,25),(62,25),(60,25),(58,26),(57,27),(56,27),(54,26),(52,25),(51,28),(50,29),(49,30),(48,29),(48,27),(50,26),(52,25),(54,24),(56,24),(58,23),(59,22),(58,20),(56,18),(54,17),(52,15),(50,14),(48,13),(45,12),(43,12),(42,15),(41,18),(40,20),(39,21),(38,24),(37,27),(36,29),(35,29),(34,28),(35,31),(36,36),(33,36),(30,36)]
AU = [(113,-22),(114,-30),(115,-33),(118,-35),(124,-33),(129,-32),(132,-32),(135,-35),(138,-35),(140,-38),(145,-38),(147,-39),(150,-37),(153,-32),(153,-27),(150,-22),(146,-19),(142,-15),(142,-11),(137,-12),(135,-15),(132,-12),(130,-13),(126,-14),(122,-17),(118,-20)]
LAND = (216, 203, 176)
for poly in (NA, SA, AF, EU, UK, IE, AS, AU):
    d.polygon([ll(lo, la) for lo, la in poly], fill=LAND, outline=(90, 80, 60), width=1)
# islands: Indonesia, Japan, Philippines, Madagascar, NZ
for lo, la, r in [(100,-2,4),(105,-6,4),(110,-7,4),(115,-8,4),(120,-9,3),(125,-8,3),(130,-3,3),(135,-4,3),(140,-5,3),
                  (130,31,3),(133,34,3),(136,36,3),(139,38,3),(141,41,3),(141,44,3),
                  (120,14,3),(122,16,3),(124,11,3),(47,-16,3),(48,-20,3),
                  (167,-45,3),(170,-42,3),(174,-39,3),(176,-38,3)]:
    cx, cy = ll(lo, la)
    d.ellipse([cx - r, cy - r * 0.6, cx + r, cy + r * 0.6], fill=LAND, outline=(90, 80, 60), width=1)

PINS = [(1, 30.7, 36.9, "ANTALYA"), (2, 50.6, 26.2, "BAHRAIN"), (3, 46.7, 24.7, "RIYADH"),
        (5, -115.14, 36.17, "LAS VEGAS"), (6, 174.78, -41.29, "WELLINGTON"),
        (7, 106.3, -6.2, "CIKANDE"), (8, -108.5, 25.6, "GUASAVE"),
        (9, 26.5, 60.2, "FINLAND"), (10, 30.52, 50.45, "KYIV"),
        (11, -76.0, -11.2, "JUNIN"), (12, 6.3, 4.8, "BAYELSA")]
OFF = {1: (-52, 8), 2: (8, -16), 3: (8, 8), 5: (-52, -14), 6: (-62, -4), 7: (6, 8),
       8: (-58, 8), 9: (-48, -12), 10: (10, -4), 11: (-46, 8), 12: (8, 6)}
for n, lon, lat, name in PINS:
    px, py = ll(lon, lat)
    px = min(max(px, MAP_X + 9), MAP_X + MAP_W - 10)
    py = min(max(py, MAP_Y + 9), MAP_Y + MAP_H - 9)
    d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=(255, 255, 255), width=1)
    text(px, py - 6, str(n), SANS_B(10), fill=(255, 255, 255), anchor="ma")
    dx, dy = OFF[n]
    text(px + dx, py + dy, name, SANS_B(8), fill=INK)
# Mercury pin 4 — space, top-right corner
mx0, my0 = MAP_X + MAP_W - 112, MAP_Y + 8
d.ellipse([mx0, my0, mx0 + 22, my0 + 22], fill=(200, 120, 60), outline=INK, width=1)
d.ellipse([mx0 + 5, my0 + 6, mx0 + 11, my0 + 11], fill=(150, 80, 40))
d.ellipse([mx0 + 13, my0 + 13, mx0 + 17, my0 + 16], fill=(150, 80, 40))
d.ellipse([mx0 + 6, my0 + 6, mx0 + 24, my0 + 24], outline=(90, 80, 60), width=1)
text(mx0 + 30, my0 + 2, "4 MERCURY", SANS_B(9), fill=INK)
text(mx0 + 30, my0 + 14, "BepiColombo", SANS(8), fill=GREY)
# legend
text(16, MAP_Y + MAP_H + 8, "EUROPE 3  •  ASIA 3  •  N. AMERICA 2  •  S. AMERICA 1  •  AFRICA 1  •  OCEANIA 1  •  SPACE 1",
     SANS_B(10), fill=GREY)
text(16, MAP_Y + MAP_H + 24, "Pins match the numbered stories on this page.",
     SANS(9), fill=GREY)

# ---- ALSO panel
d.rectangle([568, BY, 1016, 996], fill=PANEL, outline=INK, width=1)
text(578, BY + 6, "ALSO", SANS_B(13))
d.line([(578, BY + 24), (1006, BY + 24)], fill=INK, width=1)
ALSO_L = [
    ("16", "BepiColombo in Mercury orbit"),
    ("17", "\u201cEl Chapo Isidro\u201d caught \u2014 $5m"),
    ("18", "FBI probes NCIC database hack"),
    ("19", "Sparta II hit by drones, Finland"),
    ("20", "Zelensky: Crimea strike \u201cfair\u201d"),
    ("21", "Cricket: India 720/9, record vs NZ"),
    ("22", "Huawei jury STILL OUT"),
    ("23", "Nigeria boat: \u226524 dead"),
    ("24", "Peru quake: 1 dead, 16 injured"),
    ("25", "UN \u201ckiller robot\u201d talks: no rules"),
    ("26", "Lisbon march over living costs"),
    ("27", "Virginia measles death since 1978"),
]
ALSO_R = [
    ("28", "Mamdani: Rikers to close by 2032"),
    ("29", "Denmark: Russia plot to kill rapper"),
    ("30", "Miliband: EU deal, not tuition fees"),
    ("31", "Roundup $7.25bn settlement OK'd"),
    ("32", "SoftBank eyed $1tn SK Hynix deal"),
    ("33", "F1: full-time stewards from 2027"),
    ("34", "Australia edge Wales in rugby"),
    ("35", "Ireland beat S. Africa 20\u201317"),
    ("36", "Trafalgar tree felled in Norway"),
    ("37", "\u201cI only sold five copies of GTA 6\u201d"),
    ("38", "Europe ready to talk to Russia"),
    ("39", "Florida river: 73-year flood record"),
]
def also_col(x, items):
    yy = BY + 30
    for num, s in items:
        text(x, yy, num, SANS_B(10), fill=RED)
        text(x + 20, yy, s, SANS(10))
        yy += 13
also_col(578, ALSO_L)
also_col(800, ALSO_R)

# ---------------------------------------------------------------- footer
text(512, 1004, "SOURCES: BBC  •  REUTERS  •  CHANNEL NEWS ASIA  •  BLOOMBERG  •  MKT NEWS  •  AP  •  CNN  •  FINNHUB  •  INDECI  •  ESA/JAXA",
     SANS(11), anchor="ma")

img.save(os.path.join(BASE, "entry.png"), optimize=True)
print("saved entry.png", os.path.getsize(os.path.join(BASE, "entry.png")), "bytes")
