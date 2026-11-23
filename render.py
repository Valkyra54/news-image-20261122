#!/usr/bin/env python3
"""Build-time renderer for news-image-20261122 v2 (THE SUNDAY GAZETTE).

Written from the RESEARCH.md + REFRESH-RESULT.md spec. stdlib + Pillow only
at BUILD time; the shipped main.py is stdlib-only and only copies entry.png.
Layout (1024x1024): masthead / 3 lead banners / 12 tiles / markets strip /
"WHERE IT HAPPENED" world-map band (12 pins) / ALSO 2-col list / sources footer.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024

# ---- palette ----
INK = (18, 24, 33)
PAPER = (250, 247, 240)
NAVY = (13, 27, 46)
NAVY2 = (24, 48, 78)
GOLD = (198, 154, 52)
RED = (178, 34, 34)
DARKRED = (139, 22, 22)
TEAL = (14, 96, 98)
GREEN = (27, 120, 62)
ORANGE = (214, 96, 20)
GREY = (90, 96, 104)
LINE = (200, 192, 178)
SEA = (178, 214, 228)
LAND = (226, 214, 178)
LAND2 = (206, 196, 158)

def fb(size):
    return ImageFont.truetype(os.path.join(FONTS, "DejaVuSans-Bold.ttf"), size)

def fr(size):
    return ImageFont.truetype(os.path.join(FONTS, "DejaVuSans.ttf"), size)

def serifb(size):
    return ImageFont.truetype(os.path.join(FONTS, "DejaVuSerif-Bold.ttf"), size)

def wrap(draw, text, font, maxw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def text(draw, xy, s, font, fill, anchor="la"):
    draw.text(xy, s, font=font, fill=fill, anchor=anchor)

def chip(draw, x, y, s, font, bg, fg=(255, 255, 255)):
    w = int(draw.textlength(s, font=font)) + 14
    h = font.size + 8
    draw.rounded_rectangle([x, y, x + w, y + h], radius=4, fill=bg)
    draw.text((x + w / 2, y + h / 2), s, font=font, fill=fg, anchor="mm")
    return w, h

def rrect(draw, box, fill=None, outline=None, width=1, radius=6):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)

# ---- simplified continent polygons (lon, lat) ----
CONTINENTS = [
    # North America
    [(-168, 66), (-150, 70), (-135, 69), (-125, 71), (-112, 68), (-96, 69), (-86, 66),
     (-81, 69), (-76, 62), (-65, 60), (-56, 52), (-60, 47), (-65, 44), (-70, 42),
     (-74, 39), (-76, 35), (-80, 32), (-81, 26), (-84, 30), (-89, 29), (-91, 19),
     (-94, 17), (-97, 16), (-102, 18), (-105, 20), (-110, 23), (-114, 28), (-117, 33),
     (-122, 37), (-124, 42), (-124, 48), (-130, 54), (-135, 58), (-145, 60), (-155, 58),
     (-162, 58), (-166, 60), (-168, 66)],
    # Greenland
    [(-58, 64), (-52, 60), (-44, 60), (-40, 64), (-32, 68), (-22, 70), (-20, 74),
     (-25, 76), (-32, 78), (-45, 80), (-55, 76), (-58, 72), (-60, 68)],
    # South America
    [(-80, 9), (-77, 7), (-77, 4), (-80, -3), (-81, -6), (-77, -12), (-72, -18),
     (-70, -23), (-70, -30), (-72, -37), (-73, -44), (-70, -52), (-66, -55),
     (-65, -47), (-62, -41), (-58, -38), (-52, -33), (-48, -28), (-41, -23),
     (-39, -17), (-35, -9), (-35, -6), (-40, -3), (-44, -2), (-50, 0), (-52, 4),
     (-57, 6), (-62, 9), (-68, 11), (-72, 12), (-76, 10), (-79, 9)],
    # Africa
    [(-6, 35), (0, 36), (10, 37), (11, 34), (20, 32), (30, 31), (32, 31), (35, 28),
     (34, 27), (37, 24), (38, 22), (40, 18), (43, 12), (48, 11), (51, 10), (47, 5),
     (44, 0), (41, -4), (40, -10), (38, -15), (36, -18), (33, -25), (31, -29),
     (28, -33), (25, -34), (20, -35), (18, -32), (17, -29), (14, -22), (12, -18),
     (12, -10), (9, -1), (9, 4), (4, 6), (-8, 5), (-13, 8), (-15, 11), (-17, 15),
     (-17, 21), (-16, 25), (-13, 28), (-10, 31), (-6, 35)],
    # Eurasia
    [(-10, 36), (-9, 38), (-9, 43), (-2, 44), (-2, 48), (-4, 50), (-1, 51), (2, 51),
     (4, 53), (7, 54), (8, 57), (10, 59), (6, 58), (5, 60), (6, 62), (10, 64),
     (13, 66), (18, 69), (21, 70), (25, 71), (30, 70), (35, 68), (40, 67), (45, 68),
     (50, 69), (55, 69), (60, 69), (65, 70), (70, 72), (75, 72), (80, 73), (85, 74),
     (90, 75), (95, 76), (100, 77), (105, 77), (110, 74), (115, 73), (120, 73),
     (125, 72), (130, 72), (135, 71), (140, 72), (145, 72), (150, 70), (155, 69),
     (160, 69), (165, 66), (170, 66), (178, 65), (173, 64), (170, 60), (165, 60),
     (162, 56), (158, 52), (156, 51), (150, 59), (145, 59), (142, 55), (141, 50),
     (140, 45), (137, 43), (135, 43), (132, 43), (130, 42), (127, 40), (125, 39),
     (122, 38), (120, 35), (120, 32), (118, 28), (115, 23), (112, 22), (110, 20),
     (109, 18), (108, 12), (105, 9), (103, 8), (100, 7), (98, 9), (97, 10),
     (95, 16), (93, 17), (92, 21), (89, 22), (88, 22), (86, 20), (83, 18), (80, 15),
     (80, 13), (77, 8), (76, 10), (75, 12), (74, 15), (72, 20), (70, 22), (68, 23),
     (66, 25), (62, 25), (58, 25), (56, 26), (52, 26), (50, 29), (48, 30), (46, 30),
     (44, 29), (42, 29), (39, 30), (36, 36), (34, 36), (30, 36), (27, 37), (26, 38),
     (23, 36), (22, 37), (19, 40), (16, 38), (15, 40), (13, 42), (12, 44), (10, 44),
     (8, 44), (6, 43), (3, 43), (1, 41), (0, 39), (-1, 37), (-3, 36), (-6, 36), (-9, 37)],
    # UK
    [(-5, 50), (-4, 50), (-3, 53), (-5, 54), (-5, 56), (-4, 58), (-3, 58), (-2, 57),
     (-1, 57), (0, 55), (0, 53), (1, 51), (-1, 51), (-3, 50)],
    # Japan
    [(130, 31), (131, 31), (132, 33), (134, 34), (135, 34), (137, 35), (138, 35),
     (139, 36), (140, 36), (141, 39), (141, 41), (142, 42), (143, 42), (144, 43),
     (145, 44), (143, 44), (142, 42), (141, 40), (140, 39), (139, 37), (138, 36),
     (136, 35), (134, 34), (132, 33), (131, 32)],
    # SE Asia islands (Indonesia / Borneo / New Guinea)
    [(95, 5), (98, 3), (100, 0), (102, -2), (104, -3), (106, -6), (108, -7), (110, -7),
     (112, -7), (114, -8), (116, -9), (118, -9), (120, -10), (119, -9), (122, -9),
     (124, -10), (126, -9), (128, -8), (130, -5), (132, -4), (131, -2), (134, -2),
     (136, -2), (138, -3), (140, -5), (141, -8), (140, -8), (138, -8), (136, -7),
     (134, -4), (132, -3), (130, -1), (129, 0), (127, 1), (125, 2), (123, 1),
     (121, 0), (119, 0), (117, 1), (115, 1), (113, 1), (111, 1), (109, 0),
     (107, 0), (105, 1), (103, 2), (101, 3), (99, 4), (97, 5)],
    # Australia
    [(114, -22), (114, -28), (114, -31), (115, -34), (118, -35), (120, -34), (124, -33),
     (129, -32), (132, -32), (135, -35), (137, -35), (140, -38), (142, -39), (145, -38),
     (147, -39), (150, -37), (152, -35), (153, -32), (153, -28), (152, -25), (150, -23),
     (148, -20), (146, -19), (144, -15), (142, -11), (142, -14), (140, -17), (137, -12),
     (136, -12), (135, -15), (133, -12), (131, -12), (130, -13), (128, -14), (126, -14),
     (124, -15), (122, -17), (120, -20), (117, -20), (115, -21)],
    # Madagascar
    [(44, -16), (47, -15), (50, -16), (50, -19), (48, -22), (47, -25), (45, -25),
     (44, -22), (43, -20), (44, -18)],
    # New Zealand
    [(167, -45), (168, -44), (170, -43), (172, -42), (174, -41), (175, -39), (177, -38),
     (178, -38), (177, -39), (176, -40), (175, -41), (173, -42), (172, -43), (170, -44),
     (168, -46), (167, -46)],
]

# ---- content ----
LEADS = [
    dict(kicker="LEAD 1  •  CLIMATE  •  ANTALYA", color=DARKRED,
         headline="COP31 COLLAPSES — NO DEAL ON CLIMATE",
         sub="EU and island nations reject text with no fossil-fuel mention; longest talks ever.",
         chip="NO DEAL", chipbg=DARKRED, src="REUTERS • AP", art="cop"),
    dict(kicker="LEAD 2  •  WAR  •  THE GULF", color=TEAL,
         headline="THE GULF IGNITES — BAHRAIN, HORMUZ, RIYADH",
         sub="Bahrain hit, 2 hurt; 2 tankers struck; Riyadh drone down.",
         chip="ESCALATION", chipbg=ORANGE, src="REUTERS • AP • CNA", art="gulf"),
    dict(kicker="LEAD 3  •  MARKETS  •  GLOBAL", color=GREEN,
         headline="BITCOIN BACK ABOVE $60,000",
         sub="Saturday low $55,130 — a two-year low — then the bounce.",
         chip="$60,784", chipbg=GREEN, src="FINNHUB • COINSTATS", art="btc"),
]

# (headline, sub, place, source, icon, accent)
TILES = [
    ("FACTORY FIRE: 3 DEAD, 39 MISSING", "Search goes on after the blaze",
     "CIKANDE, INDONESIA", "REUTERS", "fire", DARKRED),
    ("VERSTAPPEN WINS LAS VEGAS GP", "Norris 2nd, Piastri 3rd — 35 lead changes",
     "LAS VEGAS", "F1", "car", NAVY2),
    ("PRINCESS OF WALES SPEAKS ON CANCER", "In a new BBC documentary",
     "UNITED KINGDOM", "BBC", "crown", (122, 74, 130)),
    ("TEEN GAMER HELPS FBI RESCUE MISSING GIRL", "Met her in an online game",
     "UNITED STATES", "BBC", "game", TEAL),
    ("US DENIES IRAN'S F-16 CLAIM", "No jet damaged over the Gulf",
     "THE GULF", "CNA", "jet", (90, 90, 96)),
    ("ENGLAND'S RECORD WIN OVER ALL BLACKS", "Nations Championship",
     "ENGLAND", "BBC", "rugby", (30, 60, 40)),
    ("FRANCE INTO FINAL VS SPRINGBOKS", "Nations Championship decider",
     "FRANCE", "BBC", "rugby", (30, 60, 130)),
    ("WASHINGTON HAIR SELLS FOR $4,000", "Auction curiosity",
     "UNITED STATES", "BBC", "gavel", (120, 90, 40)),
    ("SPITTING IMAGE CREATOR PETER FLUCK DIES, 85", "Satire pioneer",
     "UNITED KINGDOM", "BBC", "mask", (100, 60, 110)),
    ("MAN CHARGED AFTER BRADFORD COUNCILLOR STABBED", "Attempted murder charge",
     "BRADFORD", "BBC", "scales", (60, 70, 90)),
    ("IRAQ POWER PLANT FIRE: 4 DEAD, 35 HURT", "Hartha, near Basra",
     "IRAQ", "REUTERS", "plant", DARKRED),
    ("TOXIC ALCOHOL: 18 DEAD, 228 IN HOSPITAL", "Suspected methanol poisoning",
     "MANIPUR, INDIA", "REUTERS", "bottle", DARKRED),
]

MARKET_STRIP = ("MARKETS — FRI 20 NOV CLOSE:  S&P 500 −3.70%   •   NASDAQ −5.28%   •   "
                "DOW −1.93%   •   ANT $88.91   •   BRENT $92.57      |      BTC SUN 22 NOV $60,784")

ALSO_A = [
    "BepiColombo enters Mercury orbit — ESA/JAXA",
    "'El Chapo Isidro' captured in Sinaloa — $5m bounty",
    "FBI probes NCIC database hack",
    "Russian ship Sparta II hit by drones, Finland blames Ukraine",
    "Zelensky: Crimea bridge strike 'fair response'",
    "Cricket: India 720/9, record vs NZ",
    "Huawei jury STILL OUT",
    "Nigeria boat capsizes: ≥24 dead",
    "Peru quake M6.7: 1 dead, 16 hurt",
    "UN 'killer robots' talks deferred to 2028",
    "Lisbon marches over cost of living",
    "Virginia measles death — first since 1978",
]
ALSO_B = [
    "Mamdani: Rikers Island to close by 2032",
    "Denmark accuses Russia over rapper murder plot",
    "Miliband: EU deal not tied to tuition fees",
    "Roundup $7.25bn settlement approved",
    "SoftBank eyed ~$1tn SK Hynix buyout, then dropped it",
    "F1 to use full-time stewards from 2027",
    "Australia edge Wales in rugby",
    "Ireland beat South Africa 20–17; Springboks still in final",
    "Trafalgar Square Christmas tree felled in Norway",
    "'I only sold five copies of GTA 6,' says shopkeeper",
    "Europe ready to negotiate with Russia on Ukraine",
    "St. Johns River breaks 73-year flood record",
]

# (n, lon, lat, label) — pin 4 (Mercury) drawn as a star outside the map
PINS = [
    (1, 30.7, 36.9, "ANTALYA"), (2, 50.6, 26.2, "BAHRAIN"), (3, 46.7, 24.7, "RIYADH"),
    (5, -115.1, 36.2, "LAS VEGAS"), (6, 174.8, -41.3, "WELLINGTON"),
    (7, 106.3, -6.2, "CIKANDE"), (8, -108.5, 25.6, "GUASAVE"),
    (9, 26.5, 60.2, "FINLAND"), (10, 30.5, 50.5, "KYIV"),
    (11, -76.0, -11.2, "JUNIN"), (12, 6.3, 4.8, "BAYELSA"),
]

FOOTER = ("SOURCES:  BBC  •  Reuters  •  Channel News Asia  •  Bloomberg  •  MKT News  •  AP  •  CNN  •  "
          "Finnhub  •  INDECI  •  ESA/JAXA  •  UKMTO  •  NEMA")


# ---- small pictograms for the tile icon panels ----
def icon(draw, kind, box, fg):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    if kind == "fire":
        draw.polygon([(cx, cy - 26), (cx + 16, cy - 2), (cx + 9, cy + 4), (cx + 18, cy + 16),
                      (cx + 6, cy + 22), (cx - 4, cy + 26), (cx - 16, cy + 18), (cx - 18, cy + 2),
                      (cx - 8, cy - 8)], fill=fg)
        draw.ellipse([cx - 6, cy + 6, cx + 6, cy + 20], fill=(255, 200, 60))
    elif kind == "car":
        draw.rounded_rectangle([cx - 24, cy - 6, cx + 24, cy + 8], radius=5, fill=fg)
        draw.polygon([(cx - 12, cy - 6), (cx - 6, cy - 16), (cx + 10, cy - 16), (cx + 16, cy - 6)], fill=fg)
        draw.ellipse([cx - 18, cy + 6, cx - 6, cy + 18], fill=INK)
        draw.ellipse([cx + 6, cy + 6, cx + 18, cy + 18], fill=INK)
        for i in range(4):
            draw.rectangle([cx - 26 + i * 6, cy - 26, cx - 21 + i * 6, cy - 21],
                           fill=(255, 255, 255) if i % 2 == 0 else INK)
    elif kind == "crown":
        draw.polygon([(cx - 22, cy + 14), (cx - 22, cy - 8), (cx - 10, cy + 2), (cx, cy - 16),
                      (cx + 10, cy + 2), (cx + 22, cy - 8), (cx + 22, cy + 14)], fill=fg)
        draw.rectangle([cx - 22, cy + 16, cx + 22, cy + 21], fill=fg)
    elif kind == "game":
        draw.rounded_rectangle([cx - 24, cy - 12, cx + 24, cy + 14], radius=10, fill=fg)
        draw.ellipse([cx - 16, cy - 2, cx - 8, cy + 6], fill=INK)
        draw.ellipse([cx + 10, cy - 4, cx + 18, cy + 4], fill=INK)
        draw.line([cx + 12, cy + 8, cx + 16, cy + 8], fill=INK, width=2)
    elif kind == "jet":
        draw.polygon([(cx - 26, cy + 4), (cx + 8, cy - 8), (cx + 26, cy - 12), (cx + 14, cy + 2),
                      (cx + 26, cy + 12), (cx + 4, cy + 8), (cx - 20, cy + 10)], fill=fg)
    elif kind == "rugby":
        draw.ellipse([cx - 24, cy - 12, cx + 24, cy + 12], fill=fg)
        draw.line([cx - 8, cy - 10, cx - 8, cy + 10], fill=INK, width=2)
        draw.line([cx + 8, cy - 10, cx + 8, cy + 10], fill=INK, width=2)
    elif kind == "gavel":
        draw.rectangle([cx - 20, cy - 14, cx + 20, cy - 4], fill=fg)
        draw.rectangle([cx - 2, cy - 4, cx + 2, cy + 16], fill=fg)
        draw.rectangle([cx - 12, cy + 16, cx + 12, cy + 21], fill=fg)
    elif kind == "mask":
        draw.ellipse([cx - 20, cy - 16, cx + 20, cy + 18], fill=fg)
        draw.ellipse([cx - 12, cy - 4, cx - 4, cy + 2], fill=INK)
        draw.ellipse([cx + 4, cy - 4, cx + 12, cy + 2], fill=INK)
        draw.arc([cx - 10, cy + 2, cx + 10, cy + 14], 0, 180, fill=INK, width=2)
    elif kind == "scales":
        draw.line([cx, cy - 20, cx, cy + 18], fill=fg, width=3)
        draw.line([cx - 18, cy - 16, cx + 18, cy - 16], fill=fg, width=3)
        draw.polygon([(cx - 22, cy - 16), (cx - 14, cy - 16), (cx - 18, cy - 2)], outline=fg, width=2)
        draw.polygon([(cx + 14, cy - 16), (cx + 22, cy - 16), (cx + 18, cy - 2)], outline=fg, width=2)
    elif kind == "plant":
        draw.polygon([(cx - 20, cy - 18), (cx - 12, cy - 18), (cx - 8, cy + 20), (cx - 24, cy + 20)], fill=fg)
        draw.polygon([(cx + 4, cy - 18), (cx + 12, cy - 18), (cx + 16, cy + 20), (cx + 0, cy + 20)], fill=fg)
        draw.line([cx - 26, cy + 4, cx + 26, cy + 4], fill=fg, width=3)
    elif kind == "bottle":
        draw.rounded_rectangle([cx - 12, cy - 20, cx + 12, cy + 20], radius=6, fill=fg)
        draw.rectangle([cx - 5, cy - 28, cx + 5, cy - 18], fill=fg)
        draw.rectangle([cx - 10, cy - 2, cx + 10, cy + 4], fill=INK)
        draw.text((cx, cy + 12), "!", font=fb(16), fill=INK, anchor="mm")

# ---- lead illustrations ----
def art_cop(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(28, 44, 68))
    # big screen
    draw.rectangle([x0 + 30, y0 + 12, x1 - 30, y0 + 62], fill=(240, 238, 228))
    draw.text(((x0 + x1) / 2, y0 + 26), "DRAFT TEXT", font=fb(15), fill=DARKRED, anchor="mm")
    draw.text(((x0 + x1) / 2, y0 + 47), "NO FOSSIL FUELS MENTIONED", font=fb(12), fill=INK, anchor="mm")
    # rows of desks + delegates
    for r in range(3):
        yy = y0 + 74 + r * 16
        draw.rectangle([x0 + 22, yy, x1 - 22, yy + 9], fill=(120, 96, 60))
        for c in range(9):
            cx = x0 + 34 + c * 30
            draw.ellipse([cx - 5, yy - 7, cx + 5, yy + 2], fill=(210, 190, 150))
    # podium
    draw.rectangle([x0 + 130, y1 - 22, x0 + 190, y1 - 4], fill=(198, 154, 52))

def art_gulf(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(16, 52, 66))
    # sea horizon
    draw.rectangle([x0, y0 + 66, x1, y1], fill=(24, 78, 92))
    # tanker silhouette
    draw.rectangle([x0 + 150, y0 + 74, x0 + 300, y0 + 96], fill=(20, 20, 24))
    draw.rectangle([x0 + 158, y0 + 58, x0 + 196, y0 + 74], fill=(20, 20, 24))
    draw.rectangle([x0 + 210, y0 + 62, x0 + 232, y0 + 74], fill=(214, 96, 20))
    draw.rectangle([x0 + 240, y0 + 62, x0 + 262, y0 + 74], fill=(214, 96, 20))
    # flames over Bahrain (left)
    for fx, fy, s in [(52, 52, 1.0), (76, 58, 0.75), (34, 62, 0.6)]:
        draw.polygon([(x0 + fx, y0 + fy - 26 * s), (x0 + fx + 12 * s, y0 + fy - 2 * s),
                      (x0 + fx + 6 * s, y0 + fy + 8 * s), (x0 + fx - 8 * s, y0 + fy + 8 * s),
                      (x0 + fx - 12 * s, y0 + fy - 4 * s)], fill=(255, 140, 20))
    # missile arcs over Riyadh (right) — kept inside the art box
    draw.arc([x0 + 255, y0 + 16, x0 + 315, y0 + 70], 200, 340, fill=(255, 220, 90), width=3)
    draw.arc([x0 + 264, y0 + 24, x0 + 308, y0 + 66], 200, 340, fill=(255, 220, 90), width=2)
    draw.ellipse([x0 + 296, y0 + 22, x0 + 304, y0 + 30], fill=(255, 220, 90))
    # smoke
    for sx in (44, 60, 76):
        draw.ellipse([x0 + sx, y0 + 14, x0 + sx + 16, y0 + 26], fill=(150, 150, 150))

def art_btc(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(255, 255, 255))
    for gy in range(4):
        yy = y0 + 14 + gy * 26
        draw.line([x0 + 10, yy, x1 - 10, yy], fill=(228, 228, 228), width=1)
    pts = [(x0 + 14, y0 + 30), (x0 + 70, y0 + 44), (x0 + 126, y0 + 38), (x0 + 176, y0 + 62),
           (x0 + 216, y0 + 96), (x0 + 256, y0 + 78), (x0 + 296, y0 + 46), (x0 + 316, y0 + 30)]
    draw.line(pts, fill=GREEN, width=4, joint="curve")
    draw.ellipse([pts[4][0] - 5, pts[4][1] - 5, pts[4][0] + 5, pts[4][1] + 5], fill=RED)
    draw.text((pts[4][0] + 4, pts[4][1] + 12), "SAT LOW $55,130", font=fb(10), fill=RED)
    draw.ellipse([pts[-1][0] - 5, pts[-1][1] - 5, pts[-1][0] + 5, pts[-1][1] + 5], fill=GREEN)
    draw.text((x0 + 12, y0 + 10), "$60,784", font=fb(20), fill=GREEN)

ART = {"cop": art_cop, "gulf": art_gulf, "btc": art_btc}

# ---- build ----
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    d.rectangle([0, 0, W, 88], fill=NAVY)
    d.text((W / 2, 12), "THE SUNDAY GAZETTE", font=serifb(46), fill=(255, 255, 255), anchor="ma")
    d.line([60, 66, W - 60, 66], fill=GOLD, width=2)
    d.text((W / 2, 72), "SUNDAY 22 NOVEMBER 2026    •    40 STORIES    •    5 CONTINENTS",
           font=fb(13), fill=GOLD, anchor="ma")

    # leads
    lx = [12, 350, 688]
    lw = 324
    ly, lh = 96, 224
    for i, lead in enumerate(LEADS):
        x = lx[i]
        rrect(d, [x, ly, x + lw, ly + lh], fill=(255, 255, 255), outline=LINE, width=1)
        ART[lead["art"]](d, (x + 1, ly + 1, x + lw - 1, ly + 112))
        chip(d, x + lw - 108, ly + 8, lead["chip"], fb(12), lead["chipbg"])
        d.text((x + 10, ly + 120), lead["kicker"], font=fb(10), fill=lead["color"])
        hl = wrap(d, lead["headline"], fb(20), lw - 20)
        yy = ly + 136
        for ln in hl[:2]:
            d.text((x + 10, yy), ln, font=fb(20), fill=INK)
            yy += 23
        sub = wrap(d, lead["sub"], fr(12), lw - 20)
        for ln in sub[:2]:
            d.text((x + 10, yy), ln, font=fr(12), fill=(60, 60, 60))
            yy += 15
        d.text((x + 10, ly + lh - 16), lead["src"], font=fb(9), fill=GREY)

    # tiles 4x3
    tx0, ty0 = 12, 328
    tw, th, gap = 244, 100, 8
    for idx, (head, sub, place, src, ic, accent) in enumerate(TILES):
        r, c = divmod(idx, 4)
        x = tx0 + c * (tw + gap)
        y = ty0 + r * (th + 6)
        rrect(d, [x, y, x + tw, y + th], fill=(255, 255, 255), outline=LINE, width=1)
        d.rectangle([x + 1, y + 1, x + 62, y + th - 1], fill=accent)
        icon(d, ic, (x + 6, y + 22, x + 56, y + 78), (255, 255, 255))
        d.text((x + 68, y + 6), place, font=fb(8), fill=accent)
        d.text((x + tw - 6, y + 6), src, font=fb(8), fill=GREY, anchor="ra")
        hl = wrap(d, head, fb(13), tw - 76)
        yy = y + 18
        for ln in hl[:3]:
            d.text((x + 68, yy), ln, font=fb(13), fill=INK)
            yy += 15
        sl = wrap(d, sub, fr(10), tw - 76)
        yy = y + th - 32
        for ln in sl[:2]:
            d.text((x + 68, yy), ln, font=fr(10), fill=(70, 70, 70))
            yy += 11

    # markets strip
    d.rectangle([12, 646, W - 12, 674], fill=NAVY)
    d.text((W / 2, 652), MARKET_STRIP, font=fb(11), fill=(255, 255, 255), anchor="ma")

    # map band
    my0, my1 = 682, 838
    d.text((12, my0), "WHERE IT HAPPENED — 12 PLACES, 5 CONTINENTS",
           font=fb(13), fill=INK)
    d.text((W - 12, my0), "EUROPE 3  •  ASIA 3  •  N. AMERICA 2  •  S. AMERICA 1  •  AFRICA 1  •  OCEANIA 1  •  SPACE 1",
           font=fr(10), fill=GREY, anchor="ra")
    mx0, mx1, mtop, mbot = 12, W - 12, my0 + 20, my1
    d.rectangle([mx0, mtop, mx1, mbot], fill=SEA, outline=LINE)
    lat_top, lat_bot = 84.0, -58.0
    def proj(lon, lat):
        px = mx0 + (lon + 180.0) / 360.0 * (mx1 - mx0)
        py = mtop + (lat_top - lat) / (lat_top - lat_bot) * (mbot - mtop)
        return px, py
    for poly in CONTINENTS:
        d.polygon([proj(lon, lat) for lon, lat in poly], fill=LAND, outline=(170, 158, 120))
    # graticule
    for lon in range(-150, 181, 30):
        px = mx0 + (lon + 180.0) / 360.0 * (mx1 - mx0)
        d.line([px, mtop, px, mbot], fill=(200, 226, 236), width=1)
    # pins (nudge 1/2/3 and 9/10 apart with leader lines — they cluster in Europe/ME)
    nudge = {1: (-8, 8), 2: (-5, -10), 3: (5, 10), 9: (-10, -6), 10: (11, -7)}
    for n, lon, lat, label in PINS:
        px, py = proj(lon, lat)
        dx, dy = nudge.get(n, (0, 0))
        qx, qy = px + dx, py + dy
        if (dx, dy) != (0, 0):
            d.line([px, py, qx, qy], fill=RED, width=1)
        d.ellipse([qx - 8, qy - 8, qx + 8, qy + 8], fill=RED, outline=(255, 255, 255), width=2)
        d.text((qx, qy), str(n), font=fb(10), fill=(255, 255, 255), anchor="mm")
    # Mercury star pin (pin 4) — outside the map, top right
    sx, sy = mx1 - 108, mtop + 16
    star = [(sx, sy - 11), (sx + 3, sy - 3), (sx + 11, sy - 3), (sx + 5, sy + 2),
            (sx + 8, sy + 10), (sx, sy + 5), (sx - 8, sy + 10), (sx - 5, sy + 2),
            (sx - 11, sy - 3), (sx - 3, sy - 3)]
    d.polygon(star, fill=GOLD, outline=(255, 255, 255))
    d.text((sx + 16, sy), "4 MERCURY", font=fb(10), fill=INK, anchor="lm")
    d.text((mx0 + 4, mbot - 14), "1 ANTALYA  2 BAHRAIN  3 RIYADH  5 LAS VEGAS  6 WELLINGTON  7 CIKANDE  8 GUASAVE  "
           "9 FINLAND  10 KYIV  11 JUNIN  12 BAYELSA", font=fr(9), fill=(40, 60, 70))

    # ALSO list
    ay = 846
    d.text((12, ay), "ALSO TODAY", font=fb(13), fill=INK)
    d.line([12, ay + 18, W - 12, ay + 18], fill=LINE, width=1)
    f_also = fr(11)
    for i, item in enumerate(ALSO_A):
        d.text((16, ay + 22 + i * 10), "•  " + item, font=f_also, fill=INK)
    for i, item in enumerate(ALSO_B):
        d.text((520, ay + 22 + i * 10), "•  " + item, font=f_also, fill=INK)

    # footer
    d.line([12, 988, W - 12, 988], fill=LINE, width=1)
    d.text((W / 2, 994), FOOTER, font=fr(10), fill=GREY, anchor="ma")
    d.text((W / 2, 1008), "THE SUNDAY GAZETTE  •  All stories first reported Sunday 22 November 2026 unless noted  •  v2 — Monday refresh",
           font=fr(9), fill=GREY, anchor="ma")

    img.save(OUT, optimize=True)
    print("saved", OUT, img.size, os.path.getsize(OUT), "bytes")

if __name__ == "__main__":
    build()
