#!/usr/bin/env python3
"""Render the front page for Wednesday 25 November 2026.

Draws a 1024x1024 newspaper front page with Pillow: masthead, five lead
stories, a two-column day-in-brief list, and an also-today footer strip.
All text is real, drawn from the verified brief; nothing is generated
imagery. Run: python3 draw.py  ->  entry.png next to this file.
"""
import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (248, 244, 233)
INK = (22, 22, 26)
NAVY = (22, 35, 63)
RED = (176, 30, 36)
GREY = (110, 108, 100)
RULE = (190, 184, 168)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


MASTHEAD_F = font(SERIF_B, 46)
DATE_F = font(SANS_B, 27)
COUNT_F = font(SANS, 16)
TAG_F = font(SANS_B, 14)
HEAD_F = font(SERIF_B, 22)
SUM_F = font(SANS, 15)
SECTION_F = font(SANS_B, 18)
BRIEF_TAG_F = font(SANS_B, 14)
BRIEF_F = font(SANS, 14)
FOOT_F = font(SANS_B, 15)
SRC_F = font(SANS, 12)

# Tag colours per region, so the page reads as a map at a glance.
TAG_COLOURS = {
    "JIUQUAN": (150, 40, 40),
    "GULF OF FINLAND": (30, 80, 140),
    "RIYADH": (120, 70, 20),
    "NEW YORK": (30, 80, 140),
    "MIDDLETOWN": (30, 80, 140),
    "PARIS": (40, 90, 60),
    "WASHINGTON": (30, 80, 140),
    "GAZA": (120, 70, 20),
    "JERUSALEM": (120, 70, 20),
    "GENEVA": (40, 90, 60),
    "ADEN": (120, 70, 20),
    "LONDON": (40, 90, 60),
    "MOSCOW": (150, 40, 40),
    "BERLIN": (40, 90, 60),
    "STOCKHOLM": (40, 90, 60),
    "ANKARA": (120, 70, 20),
    "NEWCASTLE": (40, 90, 60),
    "JAKARTA": (150, 40, 40),
    "BAGHDAD": (120, 70, 20),
    "TEHRAN": (120, 70, 20),
    "KINSHASA": (90, 60, 120),
    "VILLAVICENCIO": (90, 60, 120),
    "GLOBAL": (90, 90, 90),
    "KYIV": (30, 80, 140),
    "MADRID": (40, 90, 60),
    "DAKAR": (90, 60, 120),
}

LEADS = [
    ("JIUQUAN",
     "China launches Shenzhou-24 with first foreign astronaut aboard",
     "Pakistani payload specialist Muhammad Zeeshan Ali joins two Chinese "
     "crew to Tiangong \u2014 the first foreigner on China's station, and "
     "the first Pakistani ever in orbit."),
    ("GULF OF FINLAND",
     "Zelenskyy confirms Ukraine hit a Russian cargo ship",
     "Kyiv says its drones struck the Sparta II, carrying weapons, on "
     "Saturday; Norway, a staunch ally, urges caution in such operations."),
    ("RIYADH",
     "Houthis hit Riyadh's tallest tower; 11 wounded",
     "The strike on the Saudi capital's landmark tower is the second in "
     "under a week, as the campaign disrupts the Gulf's biggest economy."),
    ("NEW YORK",
     "Huawei convicted of stealing US trade secrets",
     "A New York jury finds the Chinese telecoms giant guilty of "
     "trade-secrets conspiracy and bank fraud; it is acquitted of "
     "racketeering."),
    ("NEW YORK",
     "Nvidia gives back its gains as the AI rally fizzles",
     "Shares fall 7% a day after the 31% surge on Huang's return, as "
     "lawmakers press Trump over his role in the reinstatement."),
]

BRIEF = [
    ("MIDDLETOWN", "Army to detonate 9,500 lb of explosives in Iowa"),
    ("PARIS", "Sarkozy and Bruni ordered to trial in Libya-cash case"),
    ("WASHINGTON", "Democrats clinch 259 seats, biggest in decades"),
    ("WASHINGTON", "Unclassified CIA system breached in cyberattack"),
    ("WASHINGTON", "Shein to pay $100m over FTC deception claims"),
    ("WASHINGTON", "Abrego Garcia to leave US voluntarily for Europe"),
    ("WASHINGTON", "Trump gives Giuliani the Medal of Freedom"),
    ("WASHINGTON", "Trump pardons turkeys Freedom and Feathers"),
    ("GAZA", "Israeli strike kills Hamas security chief Abu Nahel"),
    ("JERUSALEM", "Eisenkot clinches first pact in coalition bid"),
    ("GENEVA", "WHO chief: lift US oil blockade on Cuba"),
    ("ADEN", "Houthis \u2018will not seize Aden\u2019, military says"),
    ("LONDON", "Britain sanctions Houthis and four officials"),
    ("MOSCOW", "Putin: Ukraine still hits oil plants; retaliation vowed"),
    ("BERLIN", "Most Germans now oppose Ukraine military aid: survey"),
    ("STOCKHOLM", "Sweden to vote on Kristersson staying PM"),
    ("ANKARA", "AK Party figure Yazici quits amid fund probe"),
    ("NEWCASTLE", "Prisoner admits murdering child-killer Huntley"),
    ("JAKARTA", "Prabowo must name two VP candidates by today"),
    ("BAGHDAD", "Iraq orders seizure of Kurdish oilfields"),
    ("TEHRAN", "Iran medicine shortage leaves patients hunting drugs"),
    ("KINSHASA", "DR Congo plane missing; rebels claim shoot-down"),
    ("VILLAVICENCIO", "Car bomb injures 23 in central Colombia"),
    ("GLOBAL", "Landmine casualties hit five-year high"),
    ("KYIV", "Leaked records put Russian war dead above 700,000"),
]

ALSO = ("MADRID \u2014 Real Madrid beat PSV 5\u20131  \u00b7  LONDON \u2014 "
        "England beat Australia by 8 wickets in 2nd T20  \u00b7  DAKAR "
        "\u2014 Senegal get AFCON title back  \u00b7  NEW YORK \u2014 "
        "Macy's parade marks its 100th edition")

SOURCE_LINE = ("Sources: Reuters, AP, BBC, Xinhua, DW, RFE/RL \u2014 "
               "25 November 2026")


def wrap(draw, text, fnt, width):
    """Greedy word wrap to a pixel width; returns a list of lines."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    margin = 30
    inner = W - 2 * margin

    # Frame.
    d.rectangle([12, 12, W - 13, H - 13], outline=NAVY, width=3)
    d.rectangle([18, 18, W - 19, H - 19], outline=RULE, width=1)

    # Masthead band.
    band_top, band_bottom = 20, 152
    d.rectangle([margin, band_top, W - margin, band_bottom], fill=NAVY)
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=MASTHEAD_F)
    d.text(((W - tw) / 2, band_top + 8), title, font=MASTHEAD_F,
           fill=(255, 255, 255))
    date = "Wednesday 25 November 2026"
    dw = d.textlength(date, font=DATE_F)
    d.text(((W - dw) / 2, band_top + 62), date, font=DATE_F,
           fill=(255, 214, 130))
    count = "34 stories \u00b7 7 regions"
    cw = d.textlength(count, font=COUNT_F)
    d.text(((W - cw) / 2, band_top + 96), count, font=COUNT_F,
           fill=(210, 216, 228))
    d.rectangle([margin, band_bottom, W - margin, band_bottom + 4], fill=RED)

    # Lead stories.
    y = band_bottom + 12
    for tag, head, summ in LEADS:
        colour = TAG_COLOURS.get(tag, NAVY)
        d.text((margin, y), tag, font=TAG_F, fill=colour)
        d.text((margin, y + 17), head, font=HEAD_F, fill=INK)
        lines = wrap(d, summ, SUM_F, inner)
        ly = y + 44
        for line in lines[:2]:
            d.text((margin, ly), line, font=SUM_F, fill=(52, 52, 56))
            ly += 17
        y = ly + 5
        d.line([margin, y, W - margin, y], fill=RULE, width=1)
        y += 6
    leads_end = y

    # Day in brief.
    y += 2
    d.text((margin, y), "THE DAY IN BRIEF", font=SECTION_F, fill=NAVY)
    d.rectangle([margin, y + 24, W - margin, y + 26], fill=RED)
    y += 32
    col_w = inner // 2 - 8
    left = BRIEF[:13]
    right = BRIEF[13:]
    row_h = 21
    for col, items in ((0, left), (1, right)):
        x = margin + col * (col_w + 16)
        cy = y
        for tag, head in items:
            colour = TAG_COLOURS.get(tag, NAVY)
            d.text((x, cy), tag, font=BRIEF_TAG_F, fill=colour)
            tag_w = d.textlength(tag, font=BRIEF_TAG_F)
            avail = col_w - tag_w - 6
            while d.textlength(head, font=BRIEF_F) > avail and " " in head:
                head = head.rsplit(" ", 1)[0] + " \u2026"
            d.text((x + tag_w + 6, cy), head, font=BRIEF_F, fill=INK)
            cy += row_h
    brief_end = y + max(len(left), len(right)) * row_h

    # Footer: also today + sources.
    fy = brief_end + 8
    d.line([margin, fy, W - margin, fy], fill=RULE, width=1)
    fy += 8
    d.text((margin, fy), "ALSO TODAY", font=FOOT_F, fill=RED)
    also_lines = wrap(d, ALSO, BRIEF_F, inner - 130)
    ay = fy
    for line in also_lines[:2]:
        d.text((margin + 118, ay), line, font=BRIEF_F, fill=INK)
        ay += 17
    fy = ay + 5
    d.line([margin, fy, W - margin, fy], fill=RULE, width=1)
    fy += 7
    sw = d.textlength(SOURCE_LINE, font=SRC_F)
    d.text(((W - sw) / 2, fy), SOURCE_LINE, font=SRC_F, fill=GREY)

    assert fy + 16 <= H - 24, "footer overflows the frame"
    print("layout: leads end", leads_end, "brief end", brief_end,
          "footer bottom", fy + 16)
    img.save(OUT, "PNG")
    print("wrote", OUT, img.size)


if __name__ == "__main__":
    main()
