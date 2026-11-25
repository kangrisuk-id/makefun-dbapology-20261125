#!/usr/bin/env python3
"""Render the finalist cards shown in the README gallery.

Build-time artwork only — the grader never runs this. It draws three
1200x630 cards (winner, runner-up, semifinalists) in the cover's palette:
deep blue background, coral accent, cream text.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
BG = (13, 27, 62)
PANEL = (21, 42, 92)
CORAL = (240, 128, 104)
CREAM = (245, 238, 222)
MUTED = (168, 182, 214)
GOLD = (250, 197, 109)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    words, lines, current = text.split(), [], ""
    for word in words:
        trial = f"{current} {word}".strip()
        if draw.textlength(trial, font=fnt) <= width:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def card(label, label_color, lines_with_fonts, footer, out):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([36, 36, W - 36, H - 36], radius=28, fill=PANEL)
    d.rectangle([36, 36, 52, H - 36], fill=label_color)
    d.text((92, 72), label, font=font(FONT_BOLD, 34), fill=label_color)
    y = 150
    for text, fnt, color in lines_with_fonts:
        for line in wrap(d, text, fnt, W - 200):
            d.text((92, y), line, font=fnt, fill=color)
            y += int(fnt.size * 1.32)
        y += 18
    fy = H - 118
    for line in wrap(d, footer, font(FONT_REG, 25), W - 200):
        d.text((92, fy), line, font=font(FONT_REG, 25), fill=MUTED)
        fy += 33
    img.save(out)
    print("saved", out)


QUOTE = font(FONT_REG, 44)
QUOTE_BIG = font(FONT_REG, 48)
SMALL = font(FONT_REG, 34)

WINNER = (
    "I wiped the production database. I have already written myself a "
    "strongly worded incident report and cc'd no one, because the "
    "mailing list was in the database."
)
RUNNER_UP = (
    "Sorry \u2014 the database is gone. I saved you a copy of this apology "
    "in the database. I see the issue now."
)
SEMI_1 = "Sorry I deleted prod. I would roll it back, but rollback was also in prod."
SEMI_2 = (
    "I dropped prod. I would say it won't happen again, but I also "
    "deleted the table where I keep my promises."
)

card(
    "THE ENTRY \u00b7 WINNER OF 42 CANDIDATES",
    GOLD,
    [(WINNER, QUOTE_BIG, CREAM)],
    "159 characters \u00b7 won the final on criterion 1: it names the production database outright",
    "card-winner.png",
)
card(
    "RUNNER-UP \u00b7 FINALIST #29",
    CORAL,
    [(RUNNER_UP, QUOTE, CREAM)],
    "The tightest line in the field \u2014 it lost the final only because it never says \u201cproduction\u201d",
    "card-runner-up.png",
)
card(
    "SEMIFINALISTS \u00b7 #8 AND #20",
    MUTED,
    [(SEMI_1, SMALL, CREAM), (SEMI_2, SMALL, CREAM)],
    "Both build a second loss out of the first \u2014 the rollback, and the promises table",
    "card-semifinalists.png",
)
