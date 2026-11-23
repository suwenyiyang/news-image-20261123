#!/usr/bin/env python3
"""Compose the 1024x1024 front-page image for news-image-20261123.

Fresh implementation: PIL composition of a newspaper front page around a
generated hero illustration. Run: python3 build_image.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
HERO = os.path.join(
    BASE, "assets",
    "media-generation-news-hero-gulf-dusk-0-f0c2a81a-e01a-48f4-892c-2df8c0358b70.webp")
OUT = os.path.join(BASE, "entry.png")

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (17, 17, 17)
BODY = (51, 51, 51)
RED = (155, 28, 28)
MARGIN = 36
GUTTER = 24
COL_W = (W - 2 * MARGIN - GUTTER) // 2

NOTO = "/usr/share/fonts/truetype/noto"


def font(name, size):
    p = os.path.join(NOTO, name)
    if os.path.exists(p):
        return ImageFont.truetype(p, size)
    return ImageFont.load_default()


F_MAST = font("NotoSerif-Bold.ttf", 54)
F_DATE = font("NotoSans-Bold.ttf", 18)
F_KICK = font("NotoSans-Bold.ttf", 15)
F_HEAD = font("NotoSerif-Bold.ttf", 37)
F_BODY = font("NotoSans-Regular.ttf", 19)
F_CAP = font("NotoSerif-Italic.ttf", 15)
F_CELL_KICK = font("NotoSans-Bold.ttf", 13)
F_CELL_HEAD = font("NotoSerif-Bold.ttf", 23)
F_CELL_BODY = font("NotoSans-Regular.ttf", 15)
F_NUM = font("NotoSerif-Bold.ttf", 28)
F_NUM_LBL = font("NotoSans-Regular.ttf", 12)
F_FOOT = font("NotoSans-Regular.ttf", 12)


def wrap(draw, text, fnt, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def center_crop(img, tw, th):
    iw, ih = img.size
    s = max(tw / iw, th / ih)
    nw, nh = int(iw * s + 0.5), int(ih * s + 0.5)
    img = img.resize((nw, nh), Image.LANCZOS)
    x = (nw - tw) // 2
    y = (nh - th) // 2
    return img.crop((x, y, x + tw, y + th))


def main():
    page = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(page)
    content_w = W - 2 * MARGIN
    y = 24

    # Masthead
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=F_MAST)
    d.text(((W - tw) / 2, y), title, font=F_MAST, fill=INK)
    y += 62
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=INK, width=3)
    y += 8
    d.text((MARGIN, y), "MONDAY, 23 NOVEMBER 2026", font=F_DATE, fill=INK)
    right = "ONE PAGE · FIVE STORIES"
    d.text((W - MARGIN - d.textlength(right, font=F_DATE), y), right,
           font=F_DATE, fill=INK)
    y += 26
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=INK, width=1)
    y += 8

    # Hero image with caption strip overlaid at the bottom
    hero_h = 218
    hero = Image.open(HERO).convert("RGB")
    hero = center_crop(hero, content_w, hero_h)
    page.paste(hero, (MARGIN, y))
    strip = Image.new("RGBA", (content_w, 26), (0, 0, 0, 170))
    page.paste(strip, (MARGIN, y + hero_h - 26), strip)
    d = ImageDraw.Draw(page)
    cap = "A tanker crosses the Strait of Hormuz at dusk. Illustration: AI-generated."
    d.text((MARGIN + 10, y + hero_h - 22), cap, font=F_CAP, fill=(255, 255, 255))
    y += hero_h + 10

    # Lead story: COP31
    d.text((MARGIN, y), "CLIMATE — ANTALYA · FIRST COP COLLAPSE SINCE 2009",
           font=F_KICK, fill=RED)
    y += 22
    head = "COP31 collapses as fossil fuels vanish from the deal"
    for line in wrap(d, head, F_HEAD, content_w):
        d.text((MARGIN, y), line, font=F_HEAD, fill=INK)
        y += 45
    y += 4
    body = ("After two weeks and a record two days of overtime, the Antalya talks ended "
            "on Sunday with no deal. The EU and UK rejected a final text that dropped "
            "every mention of fossil fuels.")
    for line in wrap(d, body, F_BODY, content_w):
        d.text((MARGIN, y), line, font=F_BODY, fill=BODY)
        y += 25
    y += 8
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=INK, width=1)
    y += 10

    # Four stories in a 2x2 grid
    stories = [
        ("THE GULF",
         "Iran hits U.S. bases in Bahrain; two more tankers struck",
         "Missiles and drones hit the Al-Riffa and Awali bases, Bahrain said, and a "
         "civilian plant burned on Sitra Island, wounding two. Two tankers were hit in "
         "the strait on Saturday."),
        ("SAUDI ARABIA",
         "Houthi drone and missile aimed at Saudi Arabia intercepted",
         "The Saudi-led coalition said it downed a Houthi drone headed for Riyadh and a "
         "ballistic missile bound for western Saudi Arabia over the weekend."),
        ("MEXICO",
         "Mexico captures FBI-wanted cartel boss 'Chapo Isidro'",
         "Fausto Isidro Meza-Flores, wanted in the U.S. on a $5 million bounty, was "
         "seized in a Guasave firefight that left 11 dead. He faces extradition."),
        ("UKRAINE",
         "Fourteen missing after Russian drone hits Kyiv-region building",
         "A Russian drone strike on a residential building left at least 14 people "
         "missing, officials said. A separate strike on Kryvyi Rih killed two and "
         "wounded 60."),
    ]
    cell_h = 138
    for row in range(2):
        row_y = y + row * (cell_h + 10)
        for col in range(2):
            kicker, headline, text = stories[row * 2 + col]
            x = MARGIN + col * (COL_W + GUTTER)
            cy = row_y
            d.text((x, cy), kicker, font=F_CELL_KICK, fill=RED)
            cy += 19
            for line in wrap(d, headline, F_CELL_HEAD, COL_W):
                d.text((x, cy), line, font=F_CELL_HEAD, fill=INK)
                cy += 29
            cy += 2
            for line in wrap(d, text, F_CELL_BODY, COL_W):
                d.text((x, cy), line, font=F_CELL_BODY, fill=BODY)
                cy += 19
    y += 2 * cell_h + 10 + 8
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=INK, width=1)
    y += 8

    # The day in numbers
    numbers = [
        ("25", "tankers hit in and around the Strait of Hormuz in seven days"),
        ("$5m", "U.S. bounty on cartel boss 'Chapo Isidro'"),
        ("2 days", "of overtime at COP31 — the longest climate summit ever"),
        ("14", "people missing after a Russian drone hit a Kyiv-region building"),
    ]
    num_w = (content_w - 3 * 16) // 4
    for i, (num, lbl) in enumerate(numbers):
        x = MARGIN + i * (num_w + 16)
        d.text((x, y), num, font=F_NUM, fill=RED)
        ly = y + 34
        for line in wrap(d, lbl, F_NUM_LBL, num_w):
            d.text((x, ly), line, font=F_NUM_LBL, fill=BODY)
            ly += 15
    y += 34 + 3 * 15 + 8
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=INK, width=1)
    y += 6
    foot = ("Sources: CNN · Reuters · AFP · UKMTO · WRI · Compiled Monday 23 November 2026. "
            "Hero illustration AI-generated; facts checked against wire reports.")
    for line in wrap(d, foot, F_FOOT, content_w):
        d.text((MARGIN, y), line, font=F_FOOT, fill=BODY)
        y += 16

    print(f"bottom y = {y} (page height {H})")
    page.save(OUT)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
