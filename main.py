#!/usr/bin/env python3
"""The World in One Day — Thursday 19 November 2026.

A single editorial poster that sums up the day's six biggest stories,
drawn pixel by pixel on a private raster canvas and encoded as a PNG.
Standard library only, so it runs anywhere Python 3 does:

    python3 main.py            # writes entry.png next to this file

The picture is fully deterministic: same code, same bytes, every run.
"""

import os
import struct
import zlib

W, H = 1024, 1024

# ---------------------------------------------------------------- canvas

class Canvas:
    """A tiny RGB raster surface with just enough drawing primitives."""

    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.px = bytearray(bg) * (w * h)

    def set(self, x, y, rgb):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i:i + 3] = bytes(rgb)

    def rect(self, x, y, w, h, rgb):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.set(xx, yy, rgb)

    def frame(self, x, y, w, h, rgb, t=3):
        self.rect(x, y, w, t, rgb)
        self.rect(x, y + h - t, w, t, rgb)
        self.rect(x, y, t, h, rgb)
        self.rect(x + w - t, y, t, h, rgb)

    def disc(self, cx, cy, r, rgb):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                if (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r:
                    self.set(xx, yy, rgb)

    def ring(self, cx, cy, r, rgb, t=3):
        for yy in range(cy - r - t, cy + r + t + 1):
            for xx in range(cx - r - t, cx + r + t + 1):
                d2 = (xx - cx) ** 2 + (yy - cy) ** 2
                if (r - t) ** 2 <= d2 <= (r + t) ** 2:
                    self.set(xx, yy, rgb)

    def line(self, x0, y0, x1, y1, rgb, t=2):
        steps = max(abs(x1 - x0), abs(y1 - y0), 1)
        for i in range(steps + 1):
            x = x0 + (x1 - x0) * i // steps
            y = y0 + (y1 - y0) * i // steps
            for dy in range(t):
                for dx in range(t):
                    self.set(x + dx, y + dy, rgb)

    def save_png(self, path):
        def chunk(tag, data):
            body = tag + data
            return (struct.pack(">I", len(data)) + body
                    + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF))
        raw = bytearray()
        stride = self.w * 3
        for y in range(self.h):
            raw.append(0)
            raw += self.px[y * stride:(y + 1) * stride]
        png = (b"\x89PNG\r\n\x1a\n"
               + chunk(b"IHDR", struct.pack(">IIBBBBB", self.w, self.h, 8, 2, 0, 0, 0))
               + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
               + chunk(b"IEND", b""))
        with open(path, "wb") as fh:
            fh.write(png)

# ------------------------------------------------------------------ font
# Compact 5x7 bitmap font, rows top to bottom, 'X' = ink.

FONT = {
    "A": [".XXX.", "X...X", "X...X", "XXXXX", "X...X", "X...X", "X...X"],
    "B": ["XXXX.", "X...X", "X...X", "XXXX.", "X...X", "X...X", "XXXX."],
    "C": [".XXXX", "X....", "X....", "X....", "X....", "X....", ".XXXX"],
    "D": ["XXXX.", "X...X", "X...X", "X...X", "X...X", "X...X", "XXXX."],
    "E": ["XXXXX", "X....", "X....", "XXXX.", "X....", "X....", "XXXXX"],
    "F": ["XXXXX", "X....", "X....", "XXXX.", "X....", "X....", "X...."],
    "G": [".XXXX", "X....", "X....", "X..XX", "X...X", "X...X", ".XXX."],
    "H": ["X...X", "X...X", "X...X", "XXXXX", "X...X", "X...X", "X...X"],
    "I": [".XXX.", "..X..", "..X..", "..X..", "..X..", "..X..", ".XXX."],
    "J": ["..XXX", "....X", "....X", "....X", "....X", "X...X", ".XXX."],
    "K": ["X...X", "X..X.", "X.X..", "XX...", "X.X..", "X..X.", "X...X"],
    "L": ["X....", "X....", "X....", "X....", "X....", "X....", "XXXXX"],
    "M": ["X...X", "XX.XX", "X.X.X", "X.X.X", "X...X", "X...X", "X...X"],
    "N": ["X...X", "XX..X", "X.X.X", "X..XX", "X...X", "X...X", "X...X"],
    "O": [".XXX.", "X...X", "X...X", "X...X", "X...X", "X...X", ".XXX."],
    "P": ["XXXX.", "X...X", "X...X", "XXXX.", "X....", "X....", "X...."],
    "Q": [".XXX.", "X...X", "X...X", "X...X", "X.X.X", "X..X.", ".XX.X"],
    "R": ["XXXX.", "X...X", "X...X", "XXXX.", "X.X..", "X..X.", "X...X"],
    "S": [".XXXX", "X....", "X....", ".XXX.", "....X", "....X", "XXXX."],
    "T": ["XXXXX", "..X..", "..X..", "..X..", "..X..", "..X..", "..X.."],
    "U": ["X...X", "X...X", "X...X", "X...X", "X...X", "X...X", ".XXX."],
    "V": ["X...X", "X...X", "X...X", "X...X", "X...X", ".X.X.", "..X.."],
    "W": ["X...X", "X...X", "X...X", "X.X.X", "X.X.X", "XX.XX", "X...X"],
    "X": ["X...X", ".X.X.", "..X..", "..X..", "..X..", ".X.X.", "X...X"],
    "Y": ["X...X", "X...X", ".X.X.", "..X..", "..X..", "..X..", "..X.."],
    "Z": ["XXXXX", "....X", "...X.", "..X..", ".X...", "X....", "XXXXX"],
    "0": [".XXX.", "X...X", "X..XX", "X.X.X", "XX..X", "X...X", ".XXX."],
    "1": ["..X..", ".XX..", "..X..", "..X..", "..X..", "..X..", ".XXX."],
    "2": [".XXX.", "X...X", "....X", "..XX.", ".X...", "X....", "XXXXX"],
    "3": ["XXXX.", "....X", "....X", ".XXX.", "....X", "....X", "XXXX."],
    "4": ["...X.", "..XX.", ".X.X.", "X..X.", "XXXXX", "...X.", "...X."],
    "5": ["XXXXX", "X....", "XXXX.", "....X", "....X", "X...X", ".XXX."],
    "6": [".XXX.", "X....", "X....", "XXXX.", "X...X", "X...X", ".XXX."],
    "7": ["XXXXX", "....X", "...X.", "..X..", ".X...", ".X...", ".X..."],
    "8": [".XXX.", "X...X", "X...X", ".XXX.", "X...X", "X...X", ".XXX."],
    "9": [".XXX.", "X...X", "X...X", ".XXXX", "....X", "....X", ".XXX."],
    " ": [".....", ".....", ".....", ".....", ".....", ".....", "....."],
    ".": [".....", ".....", ".....", ".....", ".....", ".XX..", ".XX.."],
    ",": [".....", ".....", ".....", ".....", ".XX..", ".XX..", ".X..."],
    "-": [".....", ".....", ".....", "XXXXX", ".....", ".....", "....."],
    ":": [".....", ".XX..", ".XX..", ".....", ".XX..", ".XX..", "....."],
    "/": ["....X", "....X", "...X.", "..X..", ".X...", "X....", "X...."],
    "'": ["..X..", "..X..", ".X...", ".....", ".....", ".....", "....."],
    "!": ["..X..", "..X..", "..X..", "..X..", "..X..", ".....", "..X.."],
    "+": [".....", "..X..", "..X..", "XXXXX", "..X..", "..X..", "....."],
    "$": ["..X..", ".XXXX", "X.X.X", ".XXX.", "..X.X", "XXXX.", "..X.."],
}

def text(cv, x, y, s, rgb, scale=2, spacing=1):
    """Draw string s at (x, y); returns the x just past the text."""
    cx = x
    for ch in s.upper():
        glyph = FONT.get(ch, FONT[" "])
        for gy, row in enumerate(glyph):
            for gx, cell in enumerate(row):
                if cell == "X":
                    cv.rect(cx + gx * scale, y + gy * scale, scale, scale, rgb)
        cx += (5 + spacing) * scale
    return cx

def text_w(s, scale=2, spacing=1):
    return len(s) * (5 + spacing) * scale

def centered(cv, y, s, rgb, scale=2):
    text(cv, (W - text_w(s, scale)) // 2, y, s, rgb, scale)

# --------------------------------------------------------------- palette

INK = (16, 20, 34)        # page background, deep ink blue
PANEL = (26, 33, 52)      # panel fill
PAPER = (238, 234, 222)   # headline paper white
MUTE = (148, 160, 184)    # secondary text
GOLD = (232, 184, 75)     # masthead accent
RED = (214, 69, 65)
BLUE = (84, 138, 214)
TEAL = (64, 178, 168)
GREEN = (110, 190, 110)
PINK = (232, 120, 170)
SKY = (120, 180, 235)

# ----------------------------------------------------------------- icons
# Each painter draws inside a 120x84 box whose top-left corner is (x, y).

def icon_summit(cv, x, y):
    """Three leader circles overlapping over a summit table."""
    cv.disc(x + 38, y + 34, 17, RED)
    cv.disc(x + 82, y + 34, 17, BLUE)
    cv.disc(x + 60, y + 52, 17, GOLD)
    cv.rect(x + 14, y + 74, 92, 4, MUTE)

def icon_capitol(cv, x, y):
    """Capitol dome on a columned base."""
    cv.rect(x + 52, y + 8, 16, 8, PAPER)
    for dx in range(-24, 25, 4):
        cv.set(x + 60 + dx, y + 22, PAPER)
    cv.rect(x + 34, y + 24, 52, 5, PAPER)
    cv.rect(x + 40, y + 29, 40, 6, PAPER)
    for i in range(5):
        cv.rect(x + 26 + i * 18, y + 40, 6, 30, PAPER)
    cv.rect(x + 18, y + 72, 84, 5, PAPER)

def icon_chart(cv, x, y):
    """Rising market chart with an arrow head."""
    cv.line(x + 8, y + 76, x + 8, y + 8, MUTE, 2)
    cv.line(x + 8, y + 76, x + 112, y + 76, MUTE, 2)
    pts = [(14, 66), (38, 54), (56, 60), (78, 34), (104, 18)]
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        cv.line(x + ax, y + ay, x + bx, y + by, GREEN, 3)
    cv.line(x + 104, y + 18, x + 92, y + 20, GREEN, 3)
    cv.line(x + 104, y + 18, x + 102, y + 30, GREEN, 3)
    cv.disc(x + 104, y + 18, 4, GREEN)

def icon_europe(cv, x, y):
    """Ring of stars over a two-tone flag band."""
    import math
    for i in range(12):
        a = 2 * math.pi * i / 12
        sx = int(x + 60 + 30 * math.cos(a))
        sy = int(y + 30 + 22 * math.sin(a))
        cv.disc(sx, sy, 3, GOLD)
    cv.rect(x + 22, y + 60, 76, 9, BLUE)
    cv.rect(x + 22, y + 69, 76, 9, GOLD)

def icon_voyager(cv, x, y):
    """Probe with a big dish and a dashed 24h signal path to Earth."""
    cv.disc(x + 34, y + 40, 13, PAPER)
    cv.ring(x + 34, y + 40, 15, MUTE, 2)
    cv.rect(x + 46, y + 38, 26, 4, PAPER)
    cv.disc(x + 78, y + 40, 6, GOLD)
    cv.line(x + 78, y + 40, x + 78, y + 12, MUTE, 2)
    cv.line(x + 78, y + 40, x + 96, y + 62, MUTE, 2)
    for i in range(5):
        cv.disc(x + 92 + i * 5, y + 66 - i * 3, 2, SKY)
    cv.disc(x + 112, y + 52, 5, SKY)

def icon_vice_city(cv, x, y):
    """Palm tree against a neon sun and skyline."""
    cv.disc(x + 84, y + 30, 16, PINK)
    for bx, bh in [(10, 26), (26, 38), (94, 30), (106, 20)]:
        cv.rect(x + bx, y + 78 - bh, 12, bh, (44, 54, 84))
    cv.line(x + 44, y + 78, x + 48, y + 34, TEAL, 3)
    for dx, dy in [(-16, -8), (-8, -13), (4, -14), (14, -9), (18, 0)]:
        cv.line(x + 48, y + 34, x + 48 + dx, y + 34 + dy, TEAL, 3)
    cv.rect(x + 6, y + 78, 108, 3, TEAL)

# ---------------------------------------------------------------- panels

PANELS = [
    ("SHENZHEN", RED, icon_summit,
     "THREE AT ONE TABLE",
     ["XI HOSTS TRUMP AND PUTIN IN A",
      "FIRST-EVER TRILATERAL, APEC",
      "SIDELINES: NUKES, AI, TRADE."]),
    ("WASHINGTON", BLUE, icon_capitol,
     "JEFFRIES GETS THE NOD",
     ["HOUSE DEMOCRATS NOMINATE HIM",
      "251-11. ON TRACK TO BE THE",
      "FIRST BLACK SPEAKER."]),
    ("NASDAQ", GREEN, icon_chart,
     "ANTHROPIC RINGS THE BELL",
     ["AI GIANT DEBUTS AT $83 A SHARE",
      "AS ANT, VALUED NEAR $1.5",
      "TRILLION ON DAY ONE."]),
    ("BRUSSELS", GOLD, icon_europe,
     "45 BILLION FOR UKRAINE",
     ["EU LOAN PROPOSED, REPAID ONLY",
      "AFTER RUSSIA PAYS WAR",
      "REPARATIONS."]),
    ("DEEP SPACE", SKY, icon_voyager,
     "ONE LIGHT-DAY OUT",
     ["VOYAGER 1, 16 BILLION MILES",
      "AWAY: ITS SIGNALS NOW NEED",
      "A FULL 24 HOURS TO REACH US."]),
    ("VICE CITY", PINK, icon_vice_city,
     "GTA VI IS FINALLY OUT",
     ["MIDNIGHT LAUNCH WORLDWIDE,",
      "THE FIRST NEW GTA IN 13",
      "YEARS. QUEUES SINCE DAWN."]),
]

def draw_panel(cv, px, py, pw, ph, kicker, accent, painter, headline, facts):
    cv.rect(px, py, pw, ph, PANEL)
    cv.frame(px, py, pw, ph, accent, 3)
    cv.rect(px, py, pw, 6, accent)
    text(cv, px + 18, py + 16, kicker, accent, scale=2)
    painter(cv, px + pw - 140, py + 40)
    text(cv, px + 18, py + 128, headline, PAPER, scale=2)
    for i, line in enumerate(facts):
        text(cv, px + 18, py + 162 + i * 24, line, MUTE, scale=2)

def build():
    cv = Canvas(W, H, INK)
    # masthead
    cv.rect(0, 0, W, 118, (10, 13, 24))
    cv.rect(0, 118, W, 4, GOLD)
    centered(cv, 22, "THE WORLD IN ONE DAY", GOLD, scale=5)
    centered(cv, 76, "THURSDAY 19 NOVEMBER 2026 - SIX STORIES, ONE PAGE", MUTE, scale=2)
    # panel grid: 2 columns x 3 rows
    mx, my, gap = 28, 146, 20
    pw = (W - 2 * mx - gap) // 2
    ph = (H - my - 26 - 2 * gap) // 3
    for i, (kicker, accent, painter, headline, facts) in enumerate(PANELS):
        col, row = i % 2, i // 2
        draw_panel(cv, mx + col * (pw + gap), my + row * (ph + gap),
                   pw, ph, kicker, accent, painter, headline, facts)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    cv.save_png(out)
    print("wrote", out)

if __name__ == "__main__":
    build()
