#!/usr/bin/env python3
"""Render the news-image-20261120 round-2 entry: a broadsheet front page,
'THE WORLD TODAY', summing up Friday 20 November 2026. Round 2 leads with the
first-ever Trump-Xi-Putin summit in Shenzhen (verified live: Reuters/WSJ/NY
Post, 19-20 Nov 2026), with the ICJ Myanmar genocide ruling as second story
and Houthi missile strike on Riyadh, plus a day-in-brief strip. Drawn fresh
with PIL. Output: entry.png (1024x1024)."""
from PIL import Image, ImageDraw, ImageFont
import math
import os

W, H = 1024, 1024
PAPER = (247, 242, 229)
INK = (18, 18, 18)
RED = (163, 22, 33)
GREY = (96, 92, 82)
NAVY = (27, 42, 74)
NAVY2 = (36, 56, 96)
WOOD = (138, 90, 43)
WOOD_L = (172, 118, 58)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading, center=None):
    for ln in lines:
        xx = (center - draw.textlength(ln, font=fnt)) / 2 if center else x
        draw.text((xx, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def star(draw, cx, cy, r_out, r_in, fill, rot=-90):
    pts = []
    for i in range(10):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + i * 36)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=fill)


def flag_us(draw, x, y, w, h):
    stripe = h / 13.0
    for i in range(13):
        c = (178, 34, 52) if i % 2 == 0 else (255, 255, 255)
        draw.rectangle([x, y + i * stripe, x + w, y + (i + 1) * stripe], fill=c)
    cw, ch = w * 0.4, stripe * 7
    draw.rectangle([x, y, x + cw, y + ch], fill=(60, 59, 110))
    for r in range(4):
        for c in range(5):
            sx = x + 6 + c * (cw - 10) / 4
            sy = y + 5 + r * (ch - 9) / 3
            draw.ellipse([sx - 1.6, sy - 1.6, sx + 1.6, sy + 1.6], fill=(255, 255, 255))
    draw.rectangle([x, y, x + w, y + h], outline=(0, 0, 0), width=1)


def flag_cn(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    star(draw, x + w * 0.20, y + h * 0.28, h * 0.20, h * 0.08, (255, 222, 0))
    for sx, sy in [(0.42, 0.14), (0.50, 0.26), (0.50, 0.44), (0.42, 0.56)]:
        star(draw, x + w * sx, y + h * sy, h * 0.08, h * 0.032, (255, 222, 0))
    draw.rectangle([x, y, x + w, y + h], outline=(0, 0, 0), width=1)


def flag_ru(draw, x, y, w, h):
    for i, c in enumerate([(255, 255, 255), (0, 57, 166), (213, 0, 50)]):
        draw.rectangle([x, y + i * h / 3, x + w, y + (i + 1) * h / 3], fill=c)
    draw.rectangle([x, y, x + w, y + h], outline=(0, 0, 0), width=1)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---- outer borders ----
d.rectangle([12, 12, W - 13, H - 13], outline=INK, width=3)
d.rectangle([20, 20, W - 21, H - 21], outline=INK, width=1)

MX = 38
CW = W - 2 * MX

# ---- black masthead band (reverse) ----
d.rectangle([24, 24, W - 25, 112], fill=INK)
f = font(SERIF_B, 58)
t = "THE WORLD TODAY"
d.text(((W - d.textlength(t, font=f)) / 2, 38), t, font=f, fill=(250, 246, 236))

# ---- dateline ----
y = 124
f = font(SANS_B, 22)
t = "FRIDAY, 20 NOVEMBER 2026"
d.text(((W - d.textlength(t, font=f)) / 2, y), t, font=f, fill=INK)
y = 152
f = font(SANS, 14)
t = "SHENZHEN  •  THE HAGUE  •  RIYADH  •  ANTALYA"
d.text(((W - d.textlength(t, font=f)) / 2, y), t, font=f, fill=GREY)

# ---- lead art panel: THE TABLE OF THREE ----
PX0, PY0, PX1, PY1 = MX, 176, W - MX, 404
d.rectangle([PX0, PY0, PX1, PY1], fill=NAVY)
d.rectangle([PX0, PY0, PX1, PY1], outline=INK, width=2)
# three flags hanging above the table
FW, FH = 132, 78
flag_us(d, 150, 190, FW, FH)
flag_cn(d, 446, 190, FW, FH)
flag_ru(d, 742, 190, FW, FH)
for cx in (150 + FW / 2, 446 + FW / 2, 742 + FW / 2):
    d.line([(cx, 176), (cx, 190)], fill=(200, 200, 200), width=3)
# three chairs, drawn before the table so the table overlaps them
for cx in (215, 512, 809):
    d.rounded_rectangle([cx - 34, 272, cx + 34, 336], radius=8, fill=(20, 30, 55),
                        outline=(120, 140, 190), width=2)
# round table
d.ellipse([512 - 265, 296, 512 + 265, 368], fill=WOOD)
d.ellipse([512 - 265, 296, 512 + 265, 352], fill=WOOD_L)
d.ellipse([512 - 265, 296, 512 + 265, 352], outline=(90, 55, 20), width=2)
# caption inside panel
f = font(SANS_B, 15)
t = "THE TABLE OF THREE — THE FIRST MEETING OF THE LEADERS OF THE U.S., CHINA AND RUSSIA"
d.text(((W - d.textlength(t, font=f)) / 2, 380), t, font=f, fill=(220, 226, 240))

# ---- lead headline ----
y = 410
f = font(SANS_B, 20)
t = "FIRST-EVER THREE-WAY SUMMIT"
d.text(((W - d.textlength(t, font=f)) / 2, y), t, font=f, fill=RED)
y = 436
f = font(SERIF_B, 47)
for ln in ("TRUMP, XI AND PUTIN", "MEET IN SHENZHEN"):
    d.text(((W - d.textlength(ln, font=f)) / 2, y), ln, font=f, fill=INK)
    y += 56
y = 556
f = font(SANS, 19)
lines = wrap(d, "Leaders sign a four-point \u201cpeace declaration\u201d — nuclear war "
                "\u201cmust never be fought\u201d — but no word on Ukraine or Iran.",
             f, CW - 40)
draw_lines(d, lines, 0, y, f, INK, 25, center=W)

# ---- rule ----
d.line([(MX, 622), (W - MX, 622)], fill=INK, width=2)

# ---- two columns ----
COLW = (CW - 28) // 2
y0 = 640
# left: ICJ
x = MX
f = font(SANS_B, 15)
d.text((x, y0), "THE HAGUE", font=f, fill=RED)
y = y0 + 24
f = font(SERIF_B, 27)
lines = wrap(d, "WORLD COURT: MYANMAR COMMITTED GENOCIDE", f, COLW)
y = draw_lines(d, lines, x, y, f, INK, 33)
y += 6
f = font(SANS, 17)
lines = wrap(d, "First state ever found guilty of genocide, 9–6. Court orders "
                "reparations and safe return of the Rohingya.", f, COLW)
draw_lines(d, lines, x, y, f, INK, 22)
# right: Riyadh
x = MX + COLW + 28
f = font(SANS_B, 15)
d.text((x, y0), "RIYADH", font=f, fill=RED)
y = y0 + 24
f = font(SERIF_B, 27)
lines = wrap(d, "HOUTHI MISSILE HITS RIYADH TOWER", f, COLW)
y = draw_lines(d, lines, x, y, f, INK, 33)
y += 6
f = font(SANS, 17)
lines = wrap(d, "Saudi wealth-fund tower damaged in financial-district strike; "
                "Riyadh intercepts more missiles and drones.", f, COLW)
draw_lines(d, lines, x, y, f, INK, 22)
# vertical divider
d.line([(512, 640), (512, 786)], fill=GREY, width=1)

# ---- rule ----
d.line([(MX, 806), (W - MX, 806)], fill=INK, width=2)

# ---- THE DAY IN BRIEF strip ----
y = 822
f = font(SANS_B, 18)
d.text((MX, y), "THE DAY IN BRIEF", font=f, fill=INK)
d.line([(MX + 190, y + 10), (W - MX, y + 10)], fill=RED, width=3)
brief = [
    ("MARKETS", "Nikkei −4.8% as AI sell-off deepens; S&P falls for a fifth day"),
    ("CLIMATE", "COP31 draft drops call to phase out fossil fuels"),
    ("GAZA", "Israeli troops cross Yellow Line in central Gaza"),
    ("AFRICA", "Kenya discharges its last Ebola patient"),
]
BW = (CW - 3 * 18) // 4
y = 856
for i, (kick, head) in enumerate(brief):
    x = MX + i * (BW + 18)
    f = font(SANS_B, 13)
    d.text((x, y), kick, font=f, fill=RED)
    f = font(SANS_B, 16)
    lines = wrap(d, head, f, BW)
    draw_lines(d, lines, x, y + 20, f, INK, 20)

# ---- footer ALSO line ----
y = 952
f = font(SANS, 14)
lines = wrap(d, "ALSO: Iran war enters ninth month as Hormuz tanker attacks rise  •  "
                "Russia strikes Kyiv overnight  •  Anthropic debuts on Nasdaq",
             f, CW)
draw_lines(d, lines, 0, y, f, GREY, 18, center=W)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
img.save(out, "PNG")
print("wrote", out, os.path.getsize(out), "bytes")
