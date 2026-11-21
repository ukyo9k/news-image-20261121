"""Draw the 21 November 2026 world-news poster (1024x1024 PNG).

Run locally with Pillow installed:  python3 draw_poster.py
Writes entry.png next to this script. All artwork is drawn from scratch
with PIL primitives; no external images are used.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = "entry.png"

PAPER = (248, 244, 232)
INK = (17, 24, 39)
NAVY = (24, 48, 84)
NAVY_DARK = (16, 32, 58)
RED = (185, 28, 28)
RED_LIGHT = (220, 38, 38)
GOLD = (201, 162, 39)
WHITE = (255, 255, 255)
CARD = (255, 255, 255)
GREY = (75, 85, 99)
TEAL = (13, 148, 136)
BLUE = (37, 99, 235)
GREEN = (22, 163, 74)
AMBER = (217, 119, 6)
PURPLE = (124, 58, 237)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


F_MAST = font("DejaVuSans-Bold.ttf", 66)
F_DATE = font("DejaVuSans-Bold.ttf", 30)
F_KICK = font("DejaVuSans-Bold.ttf", 20)
F_LEAD = font("DejaVuSans-Bold.ttf", 46)
F_LEAD_SUB = font("DejaVuSans.ttf", 25)
F_TILE_H = font("DejaVuSans-Bold.ttf", 24)
F_TILE_B = font("DejaVuSans.ttf", 19)
F_FOOT = font("DejaVuSans.ttf", 17)
F_TAG = font("DejaVuSans-Bold.ttf", 16)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_text_block(draw, x, y, lines, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def starburst(draw, cx, cy, r1, r2, n=12, fill=RED_LIGHT):
    import math

    pts = []
    for i in range(n * 2):
        r = r1 if i % 2 == 0 else r2
        a = math.pi * i / n
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=fill)


def icon_chart(draw, x, y, s, color=RED):
    # falling market line with arrowhead
    pts = [(x, y + s * 0.15), (x + s * 0.3, y + s * 0.35),
           (x + s * 0.55, y + s * 0.3), (x + s * 0.8, y + s * 0.75)]
    draw.line(pts, fill=color, width=max(4, s // 10), joint="curve")
    draw.polygon([(x + s * 0.8, y + s * 0.75), (x + s * 0.62, y + s * 0.72),
                  (x + s * 0.8, y + s * 0.55)], fill=color)
    draw.line([(x, y + s), (x + s, y + s)], fill=INK, width=3)


def icon_circles(draw, x, y, s, c1=BLUE, c2=RED):
    draw.ellipse([x, y, x + s * 0.6, y + s * 0.6], outline=c1, width=5)
    draw.ellipse([x + s * 0.4, y + s * 0.25, x + s, y + s * 0.85],
                 outline=c2, width=5)


def icon_gavel(draw, x, y, s, color=AMBER):
    draw.rectangle([x, y + s * 0.2, x + s * 0.55, y + s * 0.45], fill=color)
    draw.line([(x + s * 0.5, y + s * 0.3), (x + s * 0.95, y + s * 0.75)],
              fill=color, width=max(4, s // 9))
    draw.line([(x, y + s * 0.85), (x + s * 0.6, y + s * 0.85)],
              fill=INK, width=4)


def icon_pill(draw, x, y, s, c1=TEAL, c2=WHITE):
    draw.rounded_rectangle([x, y + s * 0.25, x + s, y + s * 0.75],
                           radius=s * 0.25, fill=c1)
    draw.rounded_rectangle([x + s * 0.5, y + s * 0.25, x + s, y + s * 0.75],
                           radius=s * 0.25, fill=c2, outline=c1, width=3)
    draw.line([(x + s * 0.5, y + s * 0.25), (x + s * 0.5, y + s * 0.75)],
              fill=c1, width=3)


def icon_globe(draw, x, y, s, color=GREEN):
    draw.ellipse([x, y, x + s, y + s], outline=color, width=5)
    draw.ellipse([x + s * 0.25, y, x + s * 0.75, y + s], outline=color, width=3)
    draw.line([(x, y + s * 0.5), (x + s, y + s * 0.5)], fill=color, width=3)
    draw.arc([x, y + s * 0.15, x + s, y + s * 0.85], 200, 340, fill=color, width=3)


def icon_cloud(draw, x, y, s, color=BLUE):
    draw.ellipse([x, y + s * 0.25, x + s * 0.55, y + s * 0.65], fill=color)
    draw.ellipse([x + s * 0.3, y, x + s * 0.85, y + s * 0.55], fill=color)
    draw.ellipse([x + s * 0.55, y + s * 0.3, x + s, y + s * 0.65], fill=color)
    draw.rectangle([x, y + s * 0.5, x + s, y + s * 0.65], fill=color)
    for dx in (0.15, 0.45, 0.75):
        draw.line([(x + s * dx, y + s * 0.78), (x + s * dx, y + s * 0.95)],
                  fill=color, width=4)


def draw_lead_graphic(draw, x0, y0, gw, gh):
    """Stylised night scene: three bridges over a river, explosion, missile arc."""
    draw.rectangle([x0, y0, x0 + gw, y0 + gh], fill=NAVY_DARK)
    # stars
    for sx, sy in [(0.12, 0.15), (0.3, 0.08), (0.55, 0.18), (0.78, 0.1),
                   (0.9, 0.22), (0.42, 0.28), (0.66, 0.3)]:
        draw.ellipse([x0 + gw * sx - 2, y0 + gh * sy - 2,
                      x0 + gw * sx + 2, y0 + gh * sy + 2], fill=GOLD)
    # missile arc (dashed trail + missile)
    import math

    trail = []
    for t in range(0, 21):
        f = t / 20.0
        trail.append((x0 + gw * (0.08 + 0.62 * f),
                      y0 + gh * (0.62 - 0.45 * math.sin(f * math.pi * 0.9))))
    for i in range(0, len(trail) - 1, 2):
        draw.line([trail[i], trail[i + 1]], fill=(255, 200, 100), width=3)
    mx, my = trail[-1]
    draw.polygon([(mx, my - 8), (mx + 26, my), (mx, my + 8)], fill=(255, 200, 100))
    # explosion over middle bridge
    starburst(draw, x0 + gw * 0.5, y0 + gh * 0.42, 46, 20, fill=RED_LIGHT)
    starburst(draw, x0 + gw * 0.5, y0 + gh * 0.42, 24, 10, fill=(255, 200, 60))
    # river
    draw.rectangle([x0, y0 + gh * 0.78, x0 + gw, y0 + gh], fill=(30, 90, 160))
    draw.line([(x0, y0 + gh * 0.78), (x0 + gw, y0 + gh * 0.78)],
              fill=(120, 180, 230), width=3)
    # three bridge arches
    for bx in (0.12, 0.42, 0.72):
        draw.arc([x0 + gw * bx, y0 + gh * 0.52, x0 + gw * (bx + 0.16),
                  y0 + gh * 0.86], 180, 360, fill=WHITE, width=6)
        draw.line([(x0 + gw * bx, y0 + gh * 0.68),
                   (x0 + gw * (bx + 0.16), y0 + gh * 0.68)], fill=WHITE, width=5)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 148], fill=NAVY)
    d.rectangle([0, 148, W, 154], fill=GOLD)
    title = "THE WORLD TODAY"
    tw = d.textlength(title, font=F_MAST)
    d.text(((W - tw) / 2, 18), title, font=F_MAST, fill=WHITE)
    date = "SATURDAY  21  NOVEMBER  2026"
    dw = d.textlength(date, font=F_DATE)
    d.text(((W - dw) / 2, 100), date, font=F_DATE, fill=GOLD)

    # ---- lead story ----
    lx, ly, lw, lh = 24, 172, 976, 318
    d.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=10,
                        fill=CARD, outline=(200, 190, 165), width=2)
    d.rectangle([lx, ly + 8, lx + 10, ly + lh - 8], fill=RED)
    gx = lx + 600
    draw_lead_graphic(d, gx, ly + 14, lw - 624, lh - 28)
    tx = lx + 30
    d.text((tx, ly + 18), "LEAD  ·  EUROPE  ·  WAR IN UKRAINE",
           font=F_KICK, fill=RED)
    head = wrap(d, "RUSSIAN MISSILES LAND IN POLAND", F_LEAD, 540)
    y = draw_text_block(d, tx, ly + 52, head, F_LEAD, INK, 52)
    sub = wrap(d, "NATO calls it a grave violation as the same "
                  "barrage hits three bridges in Kyiv — at least "
                  "nine killed.", F_LEAD_SUB, 545)
    draw_text_block(d, tx, y + 8, sub, F_LEAD_SUB, GREY, 32)

    # ---- six tiles ----
    tiles = [
        ("MARKETS", "Wall Street slides into correction",
         "S&P 500 and Dow fall as AI shares plunge.",
         RED, icon_chart),
        ("EUROPE", "UK and EU seal reset deals",
         "Food, carbon and youth deals agreed in Brussels.",
         BLUE, icon_circles),
        ("JUSTICE", "Guilty: Palisades Fire arsonist",
         "LA jury convicts Jonathan Rinderknecht of arson.",
         AMBER, icon_gavel),
        ("HEALTH", "Cancer pill shrinks tumours",
         "Tumours shrank in 6 in 10 patients in early data.",
         TEAL, icon_pill),
        ("CLIMATE", "COP31 enters final stage",
         "Fossil fuels and finance unresolved in Turkey.",
         GREEN, icon_globe),
        ("WEATHER", "Cyclone Akvan weakens over India",
         "370,000 evacuated in Odisha; rain lingers.",
         PURPLE, icon_cloud),
    ]
    gx0, gy0, gap = 24, 508, 14
    tw_, th_ = 318, 214
    for i, (tag, head, body, color, icon) in enumerate(tiles):
        col, row = i % 3, i // 3
        x = gx0 + col * (tw_ + gap)
        y = gy0 + row * (th_ + gap)
        d.rounded_rectangle([x, y, x + tw_, y + th_], radius=10,
                            fill=CARD, outline=(200, 190, 165), width=2)
        d.rectangle([x, y, x + tw_, y + 6], fill=color)
        icon(d, x + 16, y + 18, 44)
        d.text((x + 72, y + 24), tag, font=F_TAG, fill=color)
        hlines = wrap(d, head, F_TILE_H, tw_ - 32)
        yy = draw_text_block(d, x + 16, y + 74, hlines[:3], F_TILE_H, INK, 28)
        blines = wrap(d, body, F_TILE_B, tw_ - 32)
        # clamp body lines so text never runs past the tile's bottom edge
        room = (y + th_ - 12) - (yy + 6)
        max_body = max(1, room // 24)
        draw_text_block(d, x + 16, yy + 6, blines[:max_body], F_TILE_B, GREY, 24)

    # ---- footer ----
    foot = ("Reported Saturday 21 November 2026  ·  Sources: Reuters · AP · BBC · "
            "IMD · US Dept. of Justice")
    fw = d.textlength(foot, font=F_FOOT)
    d.text(((W - fw) / 2, 972), foot, font=F_FOOT, fill=GREY)

    img.save(OUT, "PNG", optimize=True)


if __name__ == "__main__":
    main()
