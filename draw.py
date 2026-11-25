#!/usr/bin/env python3
"""Draw the 25 November 2026 world-news broadsheet (1024x1024).

A single dense front page: masthead, one hero story with a drawn
illustration, three secondary leads, then forty more stories grouped
into six sections across three columns. Every headline and body line
was verified against multiple news sources the same day.
"""

import random
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 231)
INK = (20, 20, 20)
MUTED = (74, 74, 74)
RED = (163, 18, 27)
NAVY = (18, 38, 63)
STEEL = (58, 92, 140)
HAIR = (196, 188, 172)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    """Load a DejaVu font, falling back to the sans face."""
    try:
        return ImageFont.truetype(FONT_DIR + name, size)
    except OSError:
        return ImageFont.truetype(FONT_DIR + "DejaVuSans.ttf", size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
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


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


# ---------------------------------------------------------------- data

HERO = {
    "kicker": "SPACE  •  FIRST FOREIGN ASTRONAUT",
    "headline": "SHENZHOU-24 DOCKS WITH FIRST FOREIGN ASTRONAUT",
    "body": ("Pakistan's Muhammad Zeeshan Ali, 40, becomes the first "
             "Pakistani in orbit and the first foreigner aboard China's "
             "Tiangong station. The Long March-2F lifted off at 08:18 "
             "Beijing time; docking followed about three and a half "
             "hours later."),
    "caption": "Shenzhou-24 docks with Tiangong — first foreign astronaut aboard.",
}

SECONDARY = [
    {
        "kicker": "WAR  •  STRAIT OF HORMUZ",
        "headline": "TWO TANKERS ABLAZE IN STRAIT OF HORMUZ",
        "body": ("Iran's IRGC says two tankers struck mines and exploded; "
                 "Houthis hit the Ras Tanura refinery."),
    },
    {
        "kicker": "MARKETS",
        "headline": "DOW TOPS 50,000 AS ASIAN MARKETS TUMBLE",
        "body": ("Dow closes above 50,000 for the first time; KOSPI plunges "
                 "6.16% and the Nikkei falls 2.78%."),
    },
    {
        "kicker": "TECH  •  LAW",
        "headline": "HUAWEI GUILTY OF STEALING TRADE SECRETS",
        "body": ("A Brooklyn jury convicts the Chinese tech giant on 10 of "
                 "12 counts, including bank fraud."),
    },
]

# Bodies are kept to one line at 11px in a 312px column (<= ~50 chars).
SECTIONS = [
    ("CONFLICT & MIDDLE EAST", [
        ("HOUTHI DRONE HITS RIYADH TOWER",
         "11 hurt in a strike on the financial district."),
        ("SAUDI COALITION HITS HODEIDAH PORT",
         "Strikes on the port and targets in Saada and Amran."),
        ("SAUDI DEFENCES DOWN FOUR DRONES",
         "Interceptions over Ras Tanura; no injuries reported."),
        ("HOUTHIS ADVANCE ON ADEN",
         "Residents prepare to flee as fighters close in."),
        ("ISRAEL KILLS HAMAS COLONEL IN GAZA",
         "Mohammad Abuelouf, his wife and two children killed."),
        ("ISRAELI STRIKE KILLS FAMILY OF FOUR",
         "Airstrike on al-Shati home kills four of a family."),
        ("GAZA STORM THREATENS 1.76M IN TENTS",
         "Storm could endanger 1.76m displaced Palestinians."),
        ("EISENKOT CLINCHES COALITION DEAL",
         "Ex-military chief's party agrees its first pact."),
        ("US WARNS CITIZENS TO LEAVE IRAN",
         "Alert follows attacks in Bahrain and Kuwait."),
    ]),
    ("RUSSIA-UKRAINE", [
        ("OVERNIGHT STRIKES KILL THREE",
         "3 dead, 15 hurt in attacks on Kyiv and Kharkiv."),
        ("UKRAINE DRONES HIT REFINERIES",
         "Syzran and Kuibyshev hit; 145 drones downed."),
        ("490,334 RUSSIAN SOLDIERS DEAD",
         "Leaked Russian data analysed by the BBC."),
        ("MERZ VOWS TO SHOW RUSSIA ITS LIMITS",
         "Merz defends a sharp rise in defence spending."),
        ("UK WARNS OF RUSSIAN SABOTAGE",
         "Defence Ministry and MI5 warn firms backing Ukraine."),
        ("POLAND SEEKS PERMANENT US BASE",
         "Push follows two Russian airspace incursions."),
    ]),
    ("ASIA & PACIFIC", [
        ("MINERS TRAPPED IN JAVA GOLD MINE",
         "26 to 29 unaccounted for, 100 metres deep."),
        ("BANGLADESH RAISES GARMENT PAY 36%",
         "Minimum wage up to 17,000 takas after protests."),
        ("NORTH KOREA EXPELS SWISS DIPLOMAT",
         "Swiss office ordered shut within 48 hours."),
        ("CHINA PROBES SHANGHAI PARTY CHIEF",
         "Chen Jining probed; fourth since 2025."),
        ("SOLOMONS SIGN AUSTRALIA TREATY",
         "Pact bars a foreign military base on the islands."),
        ("AUSTRALIA'S BIG-TECH CRACKDOWN LAW",
         "Firms face fines of up to 5% of global revenue."),
        ("INDIA APPROVES NEW SILCHAR AIRPORT",
         "Greenfield airport at a cost of 2,014 crore rupees."),
        ("6.0 QUAKE HITS SOUTH PACIFIC",
         "Magnitude 6.0 at 10 km depth; 5.9 near Balleny."),
    ]),
    ("MARKETS & BUSINESS", [
        ("DELL POSTS RECORD QUARTER",
         "Revenue $54.9bn, up 103%; AI servers $22bn, up 291%."),
        ("TRUMP PROPOSES 25% TARIFFS",
         "Duties on 14 partners; China faces 20% rate."),
        ("NASDAQ FALLS 1.5%",
         "S&P 500 down 0.5%, its eighth loss in nine days."),
        ("SAMSUNG AND SK HYNIX PLUNGE",
         "Samsung -9.9%, SK Hynix -11.1%, SoftBank -14.8%."),
        ("UKRAINE NEEDS 115BN EUROS FOR 2027",
         "Kyiv seeks funds; 90bn euros secured from the EU."),
        ("UKRAINE-HUNGARY ENERGY DEAL",
         "Kyiv and Budapest agree to deepen energy cooperation."),
    ]),
    ("SCIENCE & TECH", [
        ("POPE WARNS ON COP31 FAILURE",
         "Leo XIV: extreme climate events more frequent."),
        ("US STROKE CASES TO DOUBLE BY 2050",
         "20m Americans by 2050; costs near $423bn a year."),
        ("GUKESH HOLDS SINDAROV",
         "World chess: a gritty draw under time pressure."),
        ("SENEGAL WIN BACK AFRICA CUP",
         "Court ruling returns the title after a chaotic final."),
        ("TRUMP TO MEET EL-SAYED ON HEALTH",
         "President to discuss universal healthcare."),
    ]),
    ("WORLD & CLIMATE", [
        ("LANDMINES KILL NEARLY 7,000 IN 2025",
         "Highest toll in five years from war remnants."),
        ("SUDAN DRONE STRIKES KILL 19",
         "RSF strikes kill 19 civilians, wound 20."),
        ("COLOMBIA FREES ALL HOSTAGES",
         "Forces storm a supermarket; one captor killed."),
        ("SIX DEAD IN CESSNA CRASH",
         "Crash off Mississippi; two boys aged 8 and 10 dead."),
        ("CANADA REJECTS PENTAGON CRITICISM",
         "Defence minister pushes back on US criticism."),
        ("LIBYA OFFICERS DIE OF DRONE WOUNDS",
         "Two officers die after a sea-drone attack."),
    ]),
]


# ---------------------------------------------------------------- drawing

def draw_hero_art(draw, x0, y0, x1, y1):
    """A small night-sky panel: stars, a ringed planet, a rocket."""
    draw.rectangle([x0, y0, x1, y1], fill=NAVY)
    rng = random.Random(20261125)
    for _ in range(70):
        sx = rng.uniform(x0 + 6, x1 - 6)
        sy = rng.uniform(y0 + 6, y1 - 6)
        r = rng.choice([1, 1, 1, 2])
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(235, 238, 245))
    # ringed planet, upper right
    cx, cy, pr = x1 - 78, y0 + 58, 32
    draw.ellipse([cx - pr, cy - pr, cx + pr, cy + pr], fill=(214, 164, 92))
    draw.ellipse([cx - pr, cy - pr, cx + pr, cy + pr], outline=(150, 105, 55), width=2)
    for k in range(-2, 3):
        draw.arc([cx - pr - 22, cy - 13 + k * 3, cx + pr + 22, cy + 13 + k * 3],
                 start=195, end=345, fill=(232, 222, 190), width=2)
    # space station: hub + solar wings
    hx, hy = x0 + 52, y0 + 112
    draw.rectangle([hx - 26, hy - 8, hx + 26, hy + 8], fill=(210, 214, 220))
    draw.rectangle([hx - 26, hy - 3, hx + 26, hy + 3], fill=(150, 158, 170))
    for sx in (hx - 96, hx + 44):
        draw.rectangle([sx, hy - 12, sx + 52, hy + 12], fill=STEEL)
        draw.line([sx, hy, sx + 52, hy], fill=(210, 222, 240), width=1)
        for gx in (13, 26, 39):
            draw.line([sx + gx, hy - 12, sx + gx, hy + 12],
                      fill=(210, 222, 240), width=1)
    # rocket climbing, lower left
    rx, ry = x0 + 118, y1 - 56
    draw.polygon([(rx, ry - 52), (rx + 13, ry - 26), (rx + 13, ry + 6),
                  (rx, ry + 14), (rx - 13, ry + 6), (rx - 13, ry - 26)],
                 fill=(240, 240, 238))
    draw.polygon([(rx, ry - 52), (rx + 13, ry - 26), (rx - 13, ry - 26)],
                 fill=RED)
    draw.polygon([(rx - 13, ry - 2), (rx - 26, ry + 16), (rx - 13, ry + 8)],
                 fill=RED)
    draw.polygon([(rx + 13, ry - 2), (rx + 26, ry + 16), (rx + 13, ry + 8)],
                 fill=RED)
    draw.polygon([(rx - 7, ry + 14), (rx + 7, ry + 14), (rx, ry + 40)],
                 fill=(242, 140, 40))
    draw.polygon([(rx - 4, ry + 14), (rx + 4, ry + 14), (rx, ry + 30)],
                 fill=(250, 210, 90))
    for i in range(3):
        yy = ry + 46 + i * 9
        draw.line([rx - 34 + i * 8, yy, rx + 34 - i * 8, yy],
                  fill=(240, 240, 238), width=2)


def draw_masthead(draw):
    title = "THE WORLD IN ONE PAGE"
    tf = SERIF_B(52)
    tw = draw.textlength(title, font=tf)
    draw.text(((W - tw) / 2, 16), title, font=tf, fill=INK)
    draw.line([28, 82, W - 28, 82], fill=INK, width=2)
    left = "WEDNESDAY, 25 NOVEMBER 2026"
    right = "44 STORIES  •  FROM AROUND THE WORLD"
    lf = SANS_B(17)
    draw.text((28, 96), left, font=lf, fill=INK)
    rw = draw.textlength(right, font=lf)
    draw.text((W - 28 - rw, 96), right, font=lf, fill=INK)
    draw.line([28, 130, W - 28, 130], fill=RED, width=4)


def draw_hero(draw):
    x0, y0 = 28, 148
    text_w = 596
    art_x0, art_y0 = 648, 148
    art_x1, art_y1 = 996, 350
    kf = SANS_B(15)
    draw.text((x0, y0), HERO["kicker"], font=kf, fill=RED)
    hf = SERIF_B(34)
    y = draw_lines(draw, wrap(draw, HERO["headline"], hf, text_w),
                   x0, y0 + 26, hf, INK, 42)
    bf = SANS(17)
    y = draw_lines(draw, wrap(draw, HERO["body"], bf, text_w),
                   x0, y + 8, bf, INK, 21)
    draw_hero_art(draw, art_x0, art_y0, art_x1, art_y1)
    cf = SERIF(13)
    cw = draw.textlength(HERO["caption"], font=cf)
    draw.text((art_x1 - cw, art_y1 + 6), HERO["caption"], font=cf, fill=MUTED)
    draw.line([28, 372, W - 28, 372], fill=INK, width=2)
    return 380


def draw_secondary(draw, y0):
    cols = 3
    margin, gutter = 28, 16
    cw = (W - 2 * margin - (cols - 1) * gutter) // cols
    kf, hf, bf = SANS_B(12), SANS_B(19), SANS(13)
    for i, story in enumerate(SECONDARY):
        x = margin + i * (cw + gutter)
        draw.line([x, y0, x + cw, y0], fill=RED, width=3)
        y = y0 + 8
        y = draw_lines(draw, [story["kicker"]], x, y, kf, RED, 15)
        y = draw_lines(draw, wrap(draw, story["headline"], hf, cw),
                       x, y + 2, hf, INK, 23)
        draw_lines(draw, wrap(draw, story["body"], bf, cw),
                   x, y + 2, bf, MUTED, 17)
    draw.line([28, 500, W - 28, 500], fill=INK, width=2)
    return 508


def draw_sections(draw, y0, y1):
    """Flow section blocks continuously across three columns."""
    margin, gutter = 28, 16
    cols = 3
    cw = (W - 2 * margin - (cols - 1) * gutter) // cols
    head_f, body_f, sec_f = SANS_B(12), SANS(11), SANS_B(13)
    col_x = [margin + i * (cw + gutter) for i in range(cols)]
    col = 0
    y = y0
    for title, items in SECTIONS:
        if y + 22 + 30 > y1 and col < cols - 1:
            col += 1
            y = y0
        draw.rectangle([col_x[col], y, col_x[col] + cw, y + 19], fill=NAVY)
        draw.text((col_x[col] + 6, y + 2), title, font=sec_f, fill=(255, 255, 255))
        y += 22
        for headline, body in items:
            h_lines = wrap(draw, headline, head_f, cw)
            b_lines = wrap(draw, body, body_f, cw)
            need = len(h_lines) * 14 + len(b_lines) * 13 + 3
            if y + need > y1:
                if col >= cols - 1:
                    return
                col += 1
                y = y0
                draw.rectangle([col_x[col], y, col_x[col] + cw, y + 19], fill=NAVY)
                draw.text((col_x[col] + 6, y + 2), title + " (cont.)",
                          font=sec_f, fill=(255, 255, 255))
                y += 22
            y = draw_lines(draw, h_lines, col_x[col], y, head_f, INK, 14)
            y = draw_lines(draw, b_lines, col_x[col], y, body_f, MUTED, 13)
            draw.line([col_x[col], y + 2, col_x[col] + cw, y + 2], fill=HAIR, width=1)
            y += 3


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw.rectangle([4, 4, W - 5, H - 5], outline=INK, width=2)
    draw_masthead(draw)
    y = draw_hero(draw)
    y = draw_secondary(draw, y)
    draw_sections(draw, y, 988)
    foot = ("Compiled from Reuters, AP, BBC, CNA, Dawn and other wires  •  "
            "Wednesday 25 November 2026")
    ff = SANS(12)
    fw = draw.textlength(foot, font=ff)
    draw.text(((W - fw) / 2, 994), foot, font=ff, fill=MUTED)
    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
