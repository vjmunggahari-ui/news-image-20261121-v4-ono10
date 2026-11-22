#!/usr/bin/env python3
"""Render the Saturday 21 November 2026 front page (1024x1024 PNG).

Reads stories.json next to this file and draws a broadsheet front page:
masthead, UTC timeline, six big numbers, a 9-region bar, three hero
panels with original drawn scenes, 13 numbered mid stories with
mini-drawings, a dotted world map with numbered pins, the 33-story
also-list, a date-check box and a watch-on-Sunday strip.

Every story carries a HALF-LIFE tag (FLASH / DEVELOPING / STRUCTURAL):
how long the story will matter, not how sure we are of it.

Deterministic: fixed fonts, fixed geometry, no timestamps, no random
input. Run twice and the bytes are identical.
"""
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

W = H = 1024
M = 28  # outer margin
CW = W - 2 * M  # content width

PAPER = (248, 243, 230)
INK = (26, 26, 26)
RED = (179, 32, 44)
NAVY = (31, 58, 95)
MUTED = (107, 98, 87)
FAINT = (200, 190, 170)
SEA = (178, 205, 222)
LAND = (233, 216, 180)
WHITE = (255, 255, 255)
CREAM = (238, 231, 214)

HALF = {
    "FLASH": (180, 83, 9),
    "DEVELOPING": (15, 118, 110),
    "STRUCTURAL": (109, 40, 217),
}

FONTS = {
    "serif_b": "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
    "serif": "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
    "serif_i": "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf",
    "sans": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "sans_b": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
}
_cache = {}


def F(name, size):
    key = (name, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(FONTS[name], size)
    return _cache[key]


def width(text, font):
    return font.getlength(text)


def wrap(text, font, max_w):
    """Greedy word wrap; returns a list of lines."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if width(trial, font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text(d, xy, s, font, fill=INK):
    d.text(xy, s, font=font, fill=fill)


def centered(d, cx, y, s, font, fill=INK):
    d.text((cx - width(s, font) / 2, y), s, font=font, fill=fill)


def chip(d, x, y, label, bg, fg=WHITE, size=8):
    """Small rounded tag; returns its right edge."""
    f = F("sans_b", size)
    w = int(width(label, f)) + 10
    h = size + 7
    d.rounded_rectangle([x, y, x + w, y + h], radius=3, fill=bg)
    d.text((x + 5, y + 3), label, font=f, fill=fg)
    return x + w


# ---------------------------------------------------------------- world map
# Continents as lon/lat boxes; rasterised into a dotted map.
LAND_BOXES = [
    (-168, -95, 60, 72), (-165, -55, 45, 60), (-125, -66, 25, 45),
    (-105, -86, 14, 25), (-95, -80, 7, 14), (-58, -20, 60, 83),
    (-80, -35, -5, 12), (-75, -40, -25, -5), (-70, -55, -55, -25),
    (-10, 30, 36, 58), (-5, 25, 58, 70), (-22, -14, 63, 66),
    (-5, 2, 50, 58),
    (-17, 32, 15, 32), (-10, 42, -5, 15), (12, 35, -35, -5),
    (35, 180, 50, 75), (30, 130, 30, 50), (60, 140, 20, 30),
    (95, 110, 5, 25), (75, 90, 8, 35), (100, 120, 20, 40),
    (125, 145, 30, 45), (95, 105, 0, 20), (115, 130, -10, 5),
    (130, 150, -5, 0), (113, 154, -40, -10), (166, 178, -47, -34),
]


def is_land(lon, lat):
    return any(a <= lon <= b and c <= lat <= dd
               for a, b, c, dd in LAND_BOXES)


def lonlat_to_map(lon, lat, x0, y0, mw, mh):
    x = x0 + (lon + 180.0) / 360.0 * mw
    y = y0 + (75.0 - lat) / 130.0 * mh
    return x, y


def draw_map(d, x0, y0, mw, mh, stories, region_colors):
    d.rectangle([x0, y0, x0 + mw, y0 + mh], fill=(223, 232, 236),
                outline=FAINT)
    cols, rows = 72, 36
    for r in range(rows):
        lat = 75.0 - (r + 0.5) * (130.0 / rows)
        for c in range(cols):
            lon = -180.0 + (c + 0.5) * (360.0 / cols)
            if is_land(lon, lat):
                cx = x0 + (c + 0.5) * (mw / cols)
                cy = y0 + (r + 0.5) * (mh / rows)
                d.ellipse([cx - 1.6, cy - 1.6, cx + 1.6, cy + 1.6],
                          fill=(150, 140, 110))
    offsets = {9: (0, -10), 12: (13, -8), 13: (9, 10), 16: (-11, 8)}
    for s in stories:
        if s.get("tier") not in ("hero", "mid"):
            continue
        if s.get("lat") is None:
            continue
        px, py = lonlat_to_map(s["lon"], s["lat"], x0, y0, mw, mh)
        dx, dy = offsets.get(s["n"], (0, 0))
        px, py = px + dx, py + dy
        col = region_colors[s["region"]]
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=col,
                  outline=WHITE, width=1)
        num = str(s["n"])
        f = F("sans_b", 8)
        d.text((px - width(num, f) / 2, py - 5.5), num, font=f, fill=WHITE)


# ---------------------------------------------------------------- mini scenes
def mini_scene(d, x, y, w, h, key):
    d.rectangle([x, y, x + w, y + h], fill=CREAM, outline=FAINT)
    cx, cy = x + w / 2, y + h / 2
    if key == "gulf":
        d.polygon([(x + 6, y + h - 6), (x + w - 6, y + 8), (x + w - 6, y + h - 6)],
                  fill=SEA)
        d.polygon([(x + 6, y + 6), (x + w - 14, y + 6), (x + 6, y + h - 10)],
                  fill=LAND)
        d.ellipse([x + w - 22, y + 10, x + w - 10, y + 22], fill=RED)
        d.text((x + 6, y + 4), "BAHRAIN", font=F("sans_b", 7), fill=INK)
        d.text((x + w - 26, y + h - 12), "HORMUZ", font=F("sans_b", 6),
               fill=NAVY)
    elif key == "quake":
        for i, r in enumerate((6, 12, 18)):
            d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=RED,
                      width=1 if i else 2)
        d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=RED)
        d.line([x + 4, y + h - 8, x + w - 4, y + h - 8], fill=INK, width=2)
        d.text((x + 4, y + 2), "M 6.7", font=F("sans_b", 8), fill=RED)
    elif key == "cop31":
        for i in range(7):
            bx = x + 4 + i * 7
            d.rectangle([bx, y + 16, bx + 6, y + 30],
                        fill=RED if i == 6 else NAVY)
        d.text((x + 4, y + 2), "NOV 9-21", font=F("sans_b", 7), fill=INK)
        d.text((x + 4, y + 32), "+1 DAY", font=F("sans_b", 8), fill=RED)
    elif key == "wanted":
        d.rectangle([x + 14, y + 6, x + w - 14, y + h - 6], outline=INK)
        d.ellipse([cx - 8, y + 10, cx + 8, y + 26], outline=INK, width=2)
        d.line([x + 18, y + 32, x + w - 18, y + 32], fill=INK)
        d.line([x + 20, y + 36, x + w - 20, y + 36], fill=INK)
        d.text((cx - 4, y + h - 12), "$5m", font=F("sans_b", 7), fill=RED)
    elif key == "waves":
        for i in range(3):
            yy = y + 12 + i * 9
            d.arc([x + 6, yy - 6, x + w - 6, yy + 10], 200, 340, fill=NAVY,
                  width=2)
        d.text((x + 4, y + 2), "M 6.8", font=F("sans_b", 8), fill=NAVY)
    elif key == "flags":
        d.rectangle([x + 5, y + 10, x + 24, y + 30], fill=NAVY)
        for k in range(6):
            import math
            a = math.pi * k / 3
            d.ellipse([cx - 14 + 6 * math.cos(a) - 1, y + 20 + 6 * math.sin(a) - 1,
                       cx - 14 + 6 * math.cos(a) + 1, y + 20 + 6 * math.sin(a) + 1],
                      fill=(255, 215, 0))
        d.rectangle([x + w - 24, y + 10, x + w - 5, y + 20], fill=RED)
        d.rectangle([x + w - 24, y + 20, x + w - 5, y + 30], fill=WHITE)
    elif key == "bitcoin":
        d.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=(247, 147, 26))
        d.text((cx - 5, cy - 8), "B", font=F("sans_b", 14), fill=WHITE)
        d.line([x + 4, y + h - 6, x + w - 4, y + 8], fill=RED, width=2)
    elif key == "mercury":
        d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=(120, 113, 108))
        d.ellipse([x + 4, y + 6, x + w - 4, y + h - 6], outline=NAVY)
        d.ellipse([x + w - 10, y + 8, x + w - 6, y + 12], fill=RED)
    elif key == "ship":
        d.polygon([(x + 6, y + 26), (x + w - 6, y + 26), (x + w - 12, y + 34),
                   (x + 12, y + 34)], fill=NAVY)
        d.rectangle([x + 18, y + 16, x + 24, y + 26], fill=NAVY)
        d.polygon([(cx - 4, y + 6), (cx + 4, y + 6), (cx, y + 14)], fill=RED)
        d.text((x + 4, y + 2), "16 SAFE", font=F("sans_b", 7), fill=INK)
    elif key == "fire":
        d.polygon([(cx - 8, y + 30), (cx, y + 12), (cx + 8, y + 30)],
                  fill=(247, 147, 26))
        d.polygon([(cx - 4, y + 30), (cx, y + 20), (cx + 4, y + 30)],
                  fill=RED)
        d.text((x + 4, y + 2), "4 DEAD", font=F("sans_b", 7), fill=RED)
    elif key == "jets":
        for i, yy in enumerate((y + 14, y + 26)):
            d.polygon([(x + 8 + i * 10, yy), (x + 22 + i * 10, yy + 4),
                       (x + 8 + i * 10, yy + 8)], fill=NAVY)
        d.text((x + 4, y + 32), "21 JETS", font=F("sans_b", 7), fill=INK)
    elif key == "port":
        d.line([x + 10, y + 8, x + 10, y + 34], fill=INK, width=2)
        d.line([x + 10, y + 8, x + w - 10, y + 14], fill=INK, width=2)
        d.rectangle([x + w - 18, y + 26, x + w - 8, y + 34], fill=NAVY)
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=RED)
    elif key == "rugby":
        d.ellipse([x + 8, y + 14, x + w - 8, y + 30], fill=(120, 70, 20))
        d.line([cx, y + 14, cx, y + 30], fill=WHITE)
        d.text((x + 4, y + 2), "37-12", font=F("sans_b", 9), fill=INK)
    elif key == "cricket":
        d.line([x + 12, y + 10, x + 30, y + 32], fill=(150, 110, 60), width=4)
        d.ellipse([x + w - 16, y + 8, x + w - 8, y + 16], fill=RED)
        d.text((x + 4, y + 32), "486-4", font=F("sans_b", 9), fill=INK)
    elif key == "hospital":
        d.rectangle([x + 8, y + 16, x + w - 8, y + 34], outline=INK)
        d.line([x + 8, y + 24, x + w - 8, y + 24], fill=INK)
        d.text((cx - 4, y + 4), "+", font=F("sans_b", 12), fill=RED)
    elif key == "robot":
        d.rectangle([cx - 10, y + 10, cx + 10, y + 28], outline=INK, width=2)
        d.line([cx, y + 4, cx, y + 10], fill=INK, width=2)
        d.ellipse([cx - 5, y + 16, cx - 1, y + 20], fill=INK)
        d.ellipse([cx + 1, y + 16, cx + 5, y + 20], fill=INK)
        d.text((x + 4, y + 32), "128", font=F("sans_b", 9), fill=INK)


def hero_scene(d, x, y, w, h, key):
    if key == "gulf":
        d.rectangle([x, y, x + w, y + h], fill=LAND)
        # the Gulf as a diagonal sea band
        d.polygon([(x + 60, y), (x + 190, y), (x + w, y + h),
                   (x + 150, y + h)], fill=SEA)
        d.polygon([(x + 60, y), (x + 190, y), (x + 210, y + 26),
                   (x + 80, y + 26)], fill=(214, 196, 158))
        # missile tracks from Iran (top-left) to Bahrain
        for dx in (0, 26):
            d.line([x + 92 + dx, y + 6, x + 138 + dx, y + 40], fill=INK,
                   width=2)
            d.polygon([(x + 138 + dx, y + 40), (x + 130 + dx, y + 36),
                       (x + 134 + dx, y + 48)], fill=INK)
        bx, by = x + 152, y + 48
        d.ellipse([bx - 8, by - 8, bx + 8, by + 8], fill=RED)
        d.ellipse([bx - 3, by - 3, bx + 3, by + 3], fill=WHITE)
        kx, ky = x + 256, y + 42
        d.ellipse([kx - 7, ky - 7, kx + 7, ky + 7], fill=RED)
        d.text((x + 8, y + 6), "IRAN", font=F("sans_b", 10), fill=INK)
        d.text((bx - 24, by + 10), "BAHRAIN", font=F("sans_b", 9), fill=INK)
        d.text((x + 8, y + h - 16), "2 AIR BASES HIT", font=F("sans_b", 8),
               fill=RED)
        d.text((x + w - 92, y + h - 16), "2 TANKERS HIT", font=F("sans_b", 8),
               fill=RED)
    elif key == "quake":
        d.rectangle([x, y, x + w, y + h], fill=(233, 216, 180))
        d.rectangle([x, y + 26, x + w, y + h], fill=(198, 164, 120))
        d.rectangle([x, y + 52, x + w, y + h], fill=(160, 120, 80))
        d.line([x, y + 26, x + w, y + 26], fill=INK, width=2)
        d.text((x + 10, y + 6), "LIMA", font=F("sans_b", 9), fill=INK)
        d.text((x + w - 70, y + 6), "JUNIN", font=F("sans_b", 9), fill=INK)
        ex, ey = x + w - 130, y + 60
        for yy in range(y + 26, ey, 8):
            d.line([ex, yy, ex, yy + 4], fill=RED, width=2)
        for r in (9, 18, 27):
            d.ellipse([ex - r, ey - r, ex + r, ey + r], outline=RED, width=2)
        d.ellipse([ex - 4, ey - 4, ex + 4, ey + 4], fill=RED)
        d.text((x + 10, y + h - 18), "108 km DEEP  ·  00:09 UTC",
               font=F("sans_b", 9), fill=WHITE)
    elif key == "cop31":
        d.rectangle([x, y, x + w, y + h], fill=(224, 238, 228))
        d.text((x + 10, y + 6), "NOV 9 - 20 SCHEDULED", font=F("sans_b", 9),
               fill=INK)
        for i in range(13):
            bx = x + 8 + i * 21
            col = RED if i == 12 else NAVY
            d.rectangle([bx, y + 26, bx + 18, y + 48], fill=col)
            d.text((bx + 4, y + 30), str(9 + i), font=F("sans_b", 9),
                   fill=WHITE)
        bx = x + 8 + 13 * 21
        d.rectangle([bx, y + 26, bx + 18, y + 48], outline=RED, width=2)
        d.text((bx + 4, y + 30), "21", font=F("sans_b", 9), fill=RED)
        d.text((x + 10, y + 56), "DAY 13 OF A 12-DAY SUMMIT", font=F("sans_b", 10),
               fill=RED)
        d.text((x + w - 70, y + 56), "1.5 C", font=F("serif_b", 14), fill=RED)


# ---------------------------------------------------------------- page
def main():
    with open(os.path.join(ROOT, "stories.json")) as fh:
        data = json.load(fh)
    stories = data["stories"]
    featured = [s for s in stories if s["tier"] in ("hero", "mid")]
    listed = [s for s in stories if s["tier"] == "list"]
    region_colors = {r["name"]: tuple(int(r["color"][i:i + 2], 16)
                                       for i in (1, 3, 5))
                     for r in data["regions"]}

    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([14, 14, W - 14, H - 14], outline=INK, width=2)
    d.rectangle([20, 20, W - 20, H - 20], outline=FAINT, width=1)

    # kicker
    text(d, (M, 26), "THE WORLD IN ONE DAY", F("sans_b", 13), RED)
    right = "49 STORIES  ·  9 REGIONS  ·  EVERY ONE DATED SATURDAY 21 NOVEMBER 2026"
    f = F("sans_b", 11)
    d.text((W - M - width(right, f), 27), right, font=f, fill=INK)

    # masthead
    size = 58
    while size > 30:
        f = F("serif_b", size)
        if width(data["masthead"], f) <= CW:
            break
        size -= 2
    centered(d, W / 2, 46, data["masthead"], f)
    centered(d, W / 2, 108, data["deck"], F("serif_i", 16), MUTED)
    d.line([M, 132, W - M, 132], fill=INK, width=2)
    d.line([M, 136, W - M, 136], fill=INK, width=1)

    # UTC timeline
    y = 144
    chip(d, M, y, "THE DAY IN UTC", RED, size=9)
    tx = M + 118
    d.line([tx, y + 8, W - M, y + 8], fill=FAINT, width=2)
    n = len(data["timeline"])
    step = (W - M - tx) / n
    for i, t in enumerate(data["timeline"]):
        cx = tx + step * i + step / 2
        d.ellipse([cx - 3, y + 5, cx + 3, y + 11], fill=RED)
        tf = F("sans_b", 10)
        centered(d, cx, y - 1, t["time"], tf, RED)
        ef = F("sans", 8)
        centered(d, cx, y + 14, t["event"], ef, MUTED)

    # stat boxes
    y = 172
    bw = (CW - 5 * 6) / 6
    for i, s in enumerate(data["stats"]):
        x = M + i * (bw + 6)
        d.rectangle([x, y, x + bw, y + 50], outline=FAINT, width=1)
        d.line([x, y, x + bw, y], fill=RED, width=3)
        bf = F("serif_b", 24)
        centered(d, x + bw / 2, y + 5, s["big"], bf)
        for j, line in enumerate(wrap(s["label"], F("sans", 8.5), bw - 8)):
            centered(d, x + bw / 2, y + 32 + j * 10, line, F("sans", 8.5),
                     MUTED)

    # region bar
    y = 230
    short = {"Middle East": "Mid East", "Europe": "Europe", "Asia": "Asia",
             "Africa": "Africa", "N. America": "N. Amer.",
             "S. America": "S. Amer.", "Oceania": "Oceania",
             "Global": "", "Space": ""}
    total = sum(r["count"] for r in data["regions"])
    x = M
    for r in data["regions"]:
        wseg = CW * r["count"] / total
        col = region_colors[r["name"]]
        d.rectangle([x, y, x + wseg - 1, y + 18], fill=col)
        label = f"{short[r['name']]} {r['count']}" if short[r["name"]] else ""
        lf = F("sans_b", 8)
        if label and width(label, lf) <= wseg - 6:
            d.text((x + 4, y + 4), label, font=lf, fill=WHITE)
        x += wseg

    # heroes
    y = 256
    hh = 206
    hw = (CW - 2 * 12) / 3
    for i, s in enumerate(featured[:3]):
        x = M + i * (hw + 12)
        hero_scene(d, x, y, hw, 72, s["scene"])
        d.rectangle([x, y + 74, x + hw, y + 90], fill=RED)
        d.text((x + 6, y + 78), s["kicker"], font=F("sans_b", 11),
               fill=WHITE)
        chip(d, x + hw - 92, y + 94, s["half_life"], HALF[s["half_life"]],
             size=8)
        pf = F("sans_b", 9)
        d.text((x, y + 95), f"{s['n']}  {s['place']}", font=pf, fill=INK)
        hy = y + 110
        for line in wrap(s["headline"], F("serif_b", 18), hw)[:2]:
            d.text((x, hy), line, font=F("serif_b", 18), fill=INK)
            hy += 20
        dy = hy + 2
        for line in wrap(s["deck"], F("sans", 9.5), hw)[:3]:
            d.text((x, dy), line, font=F("sans", 9.5), fill=INK)
            dy += 11.5
        d.text((x, y + hh - 22), s["source"], font=F("sans", 8), fill=MUTED)
        nxt = f"NEXT: {s['next']}"
        nf = F("serif_i", 9.5)
        while width(nxt, nf) > hw and len(nxt) > 20:
            nxt = nxt[:-4] + "\u2026"
        d.text((x, y + hh - 11), nxt, font=nf, fill=NAVY)

    # mid stories: rows of 5, 4, 4
    y = 468
    row_h = 74
    mids = featured[3:]
    row_defs = [(5, 0), (4, 5), (4, 9)]
    for ri, (count, start) in enumerate(row_defs):
        ry = y + ri * row_h
        cw = (CW - (count - 1) * 8) / count
        for j in range(count):
            s = mids[start + j]
            x = M + j * (cw + 8)
            mini_scene(d, x, ry + 2, 46, 38, s["scene"])
            tx = x + 52
            tw = cw - 52
            chip(d, x + cw - 78, ry, s["half_life"], HALF[s["half_life"]],
                 size=7)
            hf = F("sans_b", 8)
            d.text((tx, ry), f"{s['n']}  {s['place']}", font=hf, fill=INK)
            hy = ry + 12
            for line in wrap(s["headline"], F("serif_b", 11.5), tw)[:2]:
                d.text((tx, hy), line, font=F("serif_b", 11.5), fill=INK)
                hy += 13.5
            dy = hy + 1
            for line in wrap(s["deck"], F("sans", 8.5), tw)[:2]:
                d.text((tx, dy), line, font=F("sans", 8.5), fill=INK)
                dy += 10.5
            d.text((tx, ry + row_h - 10), s["source"], font=F("sans", 7.5),
                   fill=MUTED)

    # half-life legend
    ly = 694
    centered(d, W / 2, ly, data["half_life_legend"], F("sans", 9), MUTED)

    # section header
    y = 710
    d.line([M, y, W - M, y], fill=INK, width=2)
    text(d, (M, y + 6), "WHERE IT HAPPENED", F("sans_b", 11), RED)
    text(d, (M, y + 20), "Pins carry each story's number; colour = region.",
         F("sans", 8.5), MUTED)
    right_h = "ALSO ON SATURDAY 21 NOVEMBER  —  33 MORE STORIES"
    rf = F("sans_b", 11)
    d.text((W - M - width(right_h, rf), y + 6), right_h, font=rf, fill=RED)

    # bottom band: map + also list
    by = 742
    bh = 200
    map_w = 300
    draw_map(d, M, by, map_w, 140, stories, region_colors)
    my = by + 146
    text(d, (M, my), "7 and 8 are placeless: money and orbit.",
         F("serif_i", 9), MUTED)
    # region legend, three columns
    ly2 = my + 15
    for i, r in enumerate(data["regions"]):
        lx = M + (i % 3) * 102
        lyy = ly2 + (i // 3) * 12
        col = region_colors[r["name"]]
        d.rectangle([lx, lyy, lx + 8, lyy + 8], fill=col)
        d.text((lx + 12, lyy - 1), f"{r['name']} {r['count']}",
               font=F("sans", 8), fill=INK)

    lx = M + map_w + 14
    lw = W - M - lx
    col_w = (lw - 12) / 2
    half = 17
    for ci, chunk in enumerate((listed[:half], listed[half:])):
        cx = lx + ci * (col_w + 12)
        iy = by
        for s in chunk:
            col = region_colors[s["region"]]
            d.ellipse([cx, iy, cx + 11, iy + 11], fill=col)
            num = str(s["n"])
            nf = F("sans_b", 7)
            d.text((cx + 5.5 - width(num, nf) / 2, iy + 1.5), num, font=nf,
                   fill=WHITE)
            lines = wrap(s["text"], F("sans", 9), col_w - 16)
            ty = iy - 1
            for line in lines[:2]:
                d.text((cx + 15, ty), line, font=F("sans", 9), fill=INK)
                ty += 11
            iy += 12 * max(1, len(lines[:2]))
            if iy > by + bh - 4:
                break

    # date check
    y = 948
    d.rectangle([M, y, W - M, y + 28], outline=RED, width=1)
    chip(d, M + 4, y + 6, "DATE CHECK", RED, size=9)
    dx = M + 92
    for j, line in enumerate(wrap(data["date_check"], F("sans", 9),
                                  W - M - dx - 6)):
        d.text((dx, y + 4 + j * 11), line, font=F("sans", 9), fill=INK)

    # watch strip + footer
    y = 982
    text(d, (M, y), "WATCH ON SUNDAY:", F("sans_b", 9), RED)
    wf = F("sans", 9)
    d.text((M + 108, y), data["watch_sunday"], font=wf, fill=INK)
    centered(d, W / 2, 995, data["footer"], F("sans", 7.5), MUTED)

    out = os.path.join(ROOT, "entry.png")
    img.save(out, format="PNG")
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
