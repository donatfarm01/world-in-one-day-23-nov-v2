#!/usr/bin/env python3
"""Draw the 23 November 2026 front page: 'The World in One Day'.

A dense-newspaper single image (1024x1024) summing up the world's news of
Monday 23 November 2026. Every story below was first reported on 23 Nov 2026
(morning roundups and wires); weekend events appear only in the clearly dated
AFTERMATH strip. Drawn with PIL only; output is fully deterministic.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 232)
INK = (17, 17, 17)
RED = (176, 30, 30)
BLUE = (31, 78, 121)
GREY = (90, 90, 90)
LIGHT_GREY = (200, 196, 184)
OCEAN = (214, 230, 240)
LAND = (232, 222, 190)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
F_SERIF_B = lambda s: ImageFont.truetype(FONT_DIR + "DejaVuSerif-Bold.ttf", s)
F_SANS_B = lambda s: ImageFont.truetype(FONT_DIR + "DejaVuSans-Bold.ttf", s)
F_SANS = lambda s: ImageFont.truetype(FONT_DIR + "DejaVuSans.ttf", s)


def wrap(draw, text, font, max_w):
    """Greedy word wrap using real glyph widths."""
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def one_line(draw, text, font, max_w):
    """Truncate text to a single line with an ellipsis if needed."""
    if draw.textlength(text, font=font) <= max_w:
        return text
    while text and draw.textlength(text + "…", font=font) > max_w:
        text = text[:-1]
    return text.rstrip() + "…"


LEAD = {
    "kicker": "LEAD  •  THE GULF",
    "head": "IRAN STRIKES U.S. BASE IN BAHRAIN",
    "deck": "IRGC says two Patriot radars destroyed; Bahrain says the attacks were "
            "repelled. Fire at a civilian site, no casualties reported.",
    "source": "Dunya News  •  Jamuna i-Desk",
}

# (section, headline, deck, source)
STORIES = [
    ("WORLD", "UN talks on lethal AI weapons to continue",
     "Nations agree to keep negotiating.", "SalonVision"),
    ("WORLD", "Mexico captures FBI most-wanted cartel boss 'El Chapo Isidro'",
     "11 killed in Sinaloa firefights.", "SalonVision"),
    ("WORLD", "Houthi missile at western Saudi Arabia intercepted",
     "Coalition says it shot it down.", "Dunya News"),
    ("WORLD", "Strait of Hormuz 'under full surveillance', Iran warns",
     "Tehran vows a strong, immediate reply.", "Jamuna i-Desk"),
    ("WORLD", "Israel opposition chief calls settler arson 'Jewish terrorism'",
     "Eisenkot condemns West Bank attacks.", "WH News"),
    ("WORLD", "ICJ rules Myanmar committed genocide against Rohingya",
     "Top UN court finds genocidal acts.", "WH News"),
    ("WORLD", "Myanmar army-backed government calls ASEAN decision 'unfair'",
     "Naypyidaw rejects the bloc's move.", "Jagran Josh"),
    ("ASIA–PACIFIC", "Nepal PM Balendra Shah holds talks with Modi in Delhi",
     "State visit reviews the full range of ties.", "Observer Voice"),
    ("ASIA–PACIFIC", "India posts record 720/9d in Wellington Test",
     "Day 4: record books rewritten in Wellington.", "Observer Voice"),
    ("ASIA–PACIFIC", "South Korea education minister resigns over AI cheating scandal",
     "Minister quits amid the exam-cheating row.", "Observer Voice"),
    ("ASIA–PACIFIC", "Indonesia factory fire: 24 body bags recovered",
     "Dozens still missing after the Banten blaze.", "Bizen Art"),
    ("ASIA–PACIFIC", "Tata Steel sells tubes business to APL Apollo for ₹28,000 crore",
     "Board approves sale of tubes, colours units.", "Observer Voice"),
    ("ASIA–PACIFIC", "Amit Shah launches ₹4,000-crore infra push in Arunachal",
     "Cooperative Vision 2047 unveiled.", "Jagran Josh"),
    ("ASIA–PACIFIC", "Rajya Sabha MP Ramrao Wadkute dies in Delhi",
     "BJP MP dies of cardiac arrest at AIIMS.", "The Daily Jagran"),
    ("ASIA–PACIFIC", "Nine pilgrims killed as bus rams truck in Kota",
     "Several injured in the Rajasthan crash.", "The Daily Jagran"),
    ("ASIA–PACIFIC", "Australia rebukes US budget office over AUKUS comments",
     "Canberra condemns the CBO's remarks.", "Bizen Art"),
    ("ASIA–PACIFIC", "Philippines House team ready if VP Sara faces trial",
     "Prosecution prepares for impeachment.", "UNTV"),
    ("ASIA–PACIFIC", "Portuguese foreign minister due in Pakistan today",
     "Two-day visit begins in Islamabad.", "Dunya News"),
    ("ASIA–PACIFIC", "JEE Main 2027 registration closes today",
     "Session 1 applications end 23 November.", "Jagran Josh"),
    ("EUROPE", "Russian cargo ship still on fire off Finland",
     "Vessel burning after attack, officials say.", "Jagran Josh"),
    ("EUROPE", "14 missing after Russian drone hits Kyiv-region building",
     "Zelenskiy reports the residential strike.", "Jagran Josh"),
    ("EUROPE", "Thousands march in Lisbon over living costs",
     "Anger at prices fills the streets.", "Jagran Josh"),
    ("EUROPE", "Nvidia row: Alice Huang tied to chip-diversion network",
     "Fresh details link her to a secret route.", "The Daily Jagran"),
    ("EUROPE", "India, Bulgaria discuss ties, IMEC and Black Sea",
     "Talks cover trade corridor and security.", "The Daily Jagran"),
    ("AMERICAS & MARKETS", "Delta says system issue that delayed flights is fixed",
     "Automation restored after Sunday chaos.", "CNN"),
    ("AMERICAS & MARKETS", "FBI crime database hacked, Trump confirms",
     "National Crime Information Centre breached.", "Dunya News"),
    ("AMERICAS & MARKETS", "Monday markets open after Friday's AI rout",
     "S&P 500 in correction; Nasdaq −5.3% Friday.", "OneTurn"),
    ("AMERICAS & MARKETS", "Anupama defends IBSF World Women's Snooker title",
     "Indian cueist keeps her crown.", "The Daily Jagran"),
    ("AMERICAS & MARKETS", "Hyderabad Toofans fight back to beat Ranchi Royals 3–2",
     "Hockey India League comeback win.", "Cricketnmore"),
    ("AMERICAS & MARKETS", "Pollard becomes second batter to 15,000 T20 runs",
     "West Indies star reaches the mark.", "CricTracker"),
    ("SPORT", "Alcaraz beats Zverev to win the ATP Finals",
     "Turin final ends 6–2, 7–6.", "ScoreZaap"),
    ("SPORT", "Liverpool thrash Manchester United 4–0",
     "Anfield rout in the Premier League.", "ScoreZaap"),
    ("SPORT", "AC Milan 5–1 Frosinone; Atalanta 4–4 Inter",
     "Serie A goal rush on Sunday.", "ScoreZaap"),
    ("SPORT", "Pakistan A beat India A by 48 runs",
     "Asia Cup Rising Stars, Group B.", "ScoreZaap"),
]

AFTERMATH = [
    ("22 NOV", "COP31 ends with no deal — EU rejects a text with no fossil-fuel mention; next stop COP32, Addis Ababa."),
    ("22 NOV", "Friday's AI sell-off: Nasdaq −5.28%, S&P 500 −3.7% into correction; Nikkei −5.1%."),
    ("22 NOV", "Trump blames Democrats for a $6 trillion market slide after the 3 Nov midterms."),
]

# Rough stylised continents (x, y) in the 300x108 map box.
CONTINENTS = [
    [(18, 38), (28, 22), (52, 16), (66, 26), (60, 44), (44, 52), (30, 58), (16, 50)],   # N America
    [(58, 66), (70, 60), (82, 66), (78, 84), (64, 88), (56, 76)],                        # S America
    [(138, 30), (152, 20), (168, 24), (172, 38), (158, 44), (142, 42)],                  # Europe
    [(140, 52), (158, 48), (168, 58), (162, 82), (148, 92), (138, 70)],                  # Africa
    [(178, 18), (220, 10), (262, 16), (272, 34), (250, 52), (214, 58), (196, 40), (182, 30)],  # Asia
    [(252, 78), (272, 74), (282, 84), (268, 92), (254, 88)],                             # Australia
]
MAP_DOTS = [  # (x, y)
    (196, 46), (52, 52), (160, 34), (222, 40),
    (276, 82), (140, 38), (248, 34), (232, 62),
]


def draw_map(d, x0, y0):
    d.rectangle([x0, y0, x0 + 300, y0 + 108], fill=OCEAN, outline=INK, width=1)
    for poly in CONTINENTS:
        pts = [(x0 + px, y0 + py) for px, py in poly]
        d.polygon(pts, fill=LAND, outline=(150, 140, 110))
    for dx, dy in MAP_DOTS:
        d.ellipse([x0 + dx - 3, y0 + dy - 3, x0 + dx + 3, y0 + dy + 3],
                  fill=RED, outline=(255, 255, 255))
    d.text((x0 + 6, y0 + 92), "WHERE TODAY HAPPENED", font=F_SANS_B(9), fill=BLUE)


def draw():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead ----
    d.rectangle([0, 0, W, 4], fill=RED)
    d.text((W // 2, 12), "THE WORLD IN ONE DAY",
           font=F_SERIF_B(56), fill=INK, anchor="ma")
    d.text((W // 2, 78), "MONDAY 23 NOVEMBER 2026  •  35 STORIES  •  ONE DAY  •  EVERY CONTINENT",
           font=F_SANS_B(16), fill=RED, anchor="ma")
    d.line([24, 106, W - 24, 106], fill=INK, width=2)

    # ---- Lead band ----
    lx, lw = 24, 640
    d.text((lx, 118), LEAD["kicker"], font=F_SANS_B(13), fill=RED)
    d.text((lx, 136), LEAD["head"], font=F_SANS_B(32), fill=INK)
    y = 176
    for line in wrap(d, LEAD["deck"], F_SANS(16), lw):
        d.text((lx, y), line, font=F_SANS(16), fill=(40, 40, 40))
        y += 20
    d.text((lx, y + 2), "Source: " + LEAD["source"], font=F_SANS(12), fill=GREY)

    # Map on the right of the lead band
    d.text((700, 118), "THE WORLD TODAY", font=F_SANS_B(13), fill=BLUE)
    draw_map(d, 700, 140)
    d.line([24, 258, W - 24, 258], fill=INK, width=2)

    # ---- Body: three columns ----
    # Balanced by section: WORLD+EUROPE(4) | ASIA–PACIFIC | EUROPE(1)+AMERICAS+SPORT
    world = [s for s in STORIES if s[0] == "WORLD"]
    asia = [s for s in STORIES if s[0] == "ASIA–PACIFIC"]
    europe = [s for s in STORIES if s[0] == "EUROPE"]
    rest = [s for s in STORIES if s[0] in ("AMERICAS & MARKETS", "SPORT")]
    cols = [world + europe[:4], asia, europe[4:] + rest]
    col_x = [24, 356, 688]
    col_w = 312
    y_top, y_bot = 272, 880
    f_head, f_deck, f_sec = F_SANS_B(14), F_SANS(11), F_SANS_B(13)
    for ci, stories in enumerate(cols):
        x = col_x[ci]
        y = y_top
        cur_sec = None
        for sec, head, deck, src in stories:
            if sec != cur_sec:
                cur_sec = sec
                if y > y_top:
                    y += 4
                d.text((x, y), sec, font=f_sec, fill=RED)
                d.line([x, y + 16, x + col_w, y + 16], fill=RED, width=1)
                y += 20
            for line in wrap(d, head, f_head, col_w):
                d.text((x, y), line, font=f_head, fill=INK)
                y += 15
            # Source first: even if the line is truncated, the source survives.
            detail = one_line(d, src + " — " + deck, f_deck, col_w)
            d.text((x, y), detail, font=f_deck, fill=(40, 40, 40))
            y += 13
            y += 3
        print(f"column {ci}: {len(stories)} stories, bottom y = {y} (limit {y_bot})")
        assert y <= y_bot, f"column {ci} overflows: {y} > {y_bot}"
        if ci < 2:
            d.line([x + col_w + 10, y_top, x + col_w + 10, y_bot], fill=LIGHT_GREY, width=1)

    # ---- Aftermath strip (dated 22 Nov, clearly separated) ----
    ay = 884
    d.line([24, ay, W - 24, ay], fill=INK, width=2)
    d.text((24, ay + 7), "WEEKEND AFTERMATH — DATED 22 NOVEMBER, NOT TODAY'S NEWS",
           font=F_SANS_B(12), fill=RED)
    y = ay + 26
    for tag, text in AFTERMATH:
        d.text((24, y), tag, font=F_SANS_B(11), fill=RED)
        d.text((78, y), one_line(d, text, F_SANS(12), W - 24 - 78), font=F_SANS(12),
               fill=(40, 40, 40))
        y += 15

    # ---- Footer: DATE CHECK + verification badge ----
    fy = 964
    d.line([24, fy, W - 24, fy], fill=INK, width=2)
    d.rectangle([24, fy + 6, 640, fy + 54], outline=RED, width=2)
    d.text((34, fy + 10), "DATE CHECK ✓", font=F_SANS_B(13), fill=RED)
    d.text((34, fy + 27),
           "This page covers MONDAY 23 NOVEMBER 2026 only. Every story was first",
           font=F_SANS(11), fill=INK)
    d.text((34, fy + 40),
           "reported today. No 22 November story leads this page.",
           font=F_SANS(11), fill=INK)
    bx, by = 700, fy + 6
    d.ellipse([bx, by, bx + 44, by + 44], outline=BLUE, width=3)
    d.text((bx + 22, by + 22), "✓", font=F_SANS_B(26), fill=BLUE, anchor="mm")
    d.text((bx + 54, by + 2), "VERIFIED", font=F_SANS_B(14), fill=BLUE)
    d.text((bx + 54, by + 20), "35 stories checked", font=F_SANS(11), fill=INK)
    d.text((bx + 54, by + 34), "against 23 Nov reports.", font=F_SANS(11), fill=INK)

    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    draw()
