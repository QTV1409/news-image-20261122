#!/usr/bin/env python3
"""Draw the front page for Sunday 22 November 2026 and save it as PNG.

A newspaper front page, "THE WORLD IN ONE PAGE": one lead story, six
grid stories and a briefs strip, all drawn with Pillow from the news brief
for 22 November 2026. Running this file writes entry.png (1024x1024).
Deterministic: two runs write byte-identical files.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
SIZE = 1024
MARGIN = 36
PAPER = (248, 244, 232)
INK = (20, 20, 20)
BODY_INK = (52, 52, 52)
RED = (168, 35, 26)
RULE = (20, 20, 20)
LIGHT_RULE = (150, 145, 130)
FLAME = (224, 110, 30)
FLAME_DEEP = (190, 60, 20)
NIGHT = (38, 48, 74)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Split text into lines that fit width, keeping words whole."""
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        if not words:
            lines.append("")
            continue
        line = words[0]
        for word in words[1:]:
            trial = line + " " + word
            if draw.textlength(trial, font=fnt) <= width:
                line = trial
            else:
                lines.append(line)
                line = word
        lines.append(line)
    return lines


def text_block(draw, x, y, lines, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, y, x1, width=2, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def draw_flame_band(draw, x, y, w, h):
    """Night skyline with flames: the burning industrial site in Bahrain."""
    draw.rectangle([x, y, x + w, y + h], fill=NIGHT)
    # Stars.
    for sx, sy in [(30, 12), (90, 26), (160, 8), (250, 20), (330, 10),
                   (420, 24), (520, 12), (620, 22), (720, 9), (820, 20),
                   (890, 12), (120, 34), (470, 36), (680, 34)]:
        draw.ellipse([x + sx - 2, y + sy - 2, x + sx + 2, y + sy + 2],
                     fill=(240, 235, 210))
    # Low factory blocks.
    blocks = [(0, 44, 120, 26), (130, 52, 90, 18), (235, 40, 150, 30),
              (400, 50, 110, 20), (525, 42, 130, 28), (670, 54, 90, 16),
              (775, 44, 120, 26)]
    for bx, by, bw, bh in blocks:
        draw.rectangle([x + bx, y + h - bh, x + bx + bw, y + h],
                       fill=(16, 18, 30))
    # Chimneys with smoke dots.
    for cx in (150, 430, 700):
        draw.rectangle([x + cx, y + h - 44, x + cx + 12, y + h], fill=(16, 18, 30))
        for i, r in enumerate((4, 5, 6)):
            cy = y + h - 52 - i * 8
            draw.ellipse([x + cx - r + 6, cy - r,
                          x + cx + r + 6, cy + r],
                         fill=(120, 120, 125))
    # Flames rising from the middle block.
    for fx, fh, fw in [(270, 52, 26), (310, 68, 34), (355, 46, 22),
                       (585, 60, 30), (625, 44, 20)]:
        base = y + h - 26
        draw.polygon([(x + fx, base),
                      (x + fx + fw // 2, base - fh),
                      (x + fx + fw, base)],
                     fill=FLAME_DEEP)
        draw.polygon([(x + fx + 4, base),
                      (x + fx + fw // 2, base - fh + 16),
                      (x + fx + fw - 4, base)],
                     fill=FLAME)
    # Moon.
    draw.ellipse([x + w - 70, y + 8, x + w - 30, y + 48], fill=(238, 232, 205))


def main():
    img = Image.new("RGB", (SIZE, SIZE), PAPER)
    d = ImageDraw.Draw(img)
    right = SIZE - MARGIN
    width = right - MARGIN

    # ---- Masthead ----
    title_font = font(SERIF, 56)
    title = "THE WORLD IN ONE PAGE"
    tw = d.textlength(title, font=title_font)
    d.text(((SIZE - tw) / 2, 22), title, font=title_font, fill=INK)
    rule(d, MARGIN, 94, right, 4)
    rule(d, MARGIN, 100, right, 1)
    date_font = font(SANS_BOLD, 21)
    date = "SUNDAY, 22 NOVEMBER 2026"
    dw = d.textlength(date, font=date_font)
    d.text(((SIZE - dw) / 2, 110), date, font=date_font, fill=INK)
    tag_font = font(SANS, 14)
    tag = "THE DAY'S WORLD NEWS  ·  IN ONE IMAGE"
    tgw = d.textlength(tag, font=tag_font)
    d.text(((SIZE - tgw) / 2, 138), tag, font=tag_font, fill=BODY_INK)
    rule(d, MARGIN, 160, right, 2)

    # ---- Lead story ----
    y = 176
    kick_font = font(SANS_BOLD, 16)
    d.text((MARGIN, y), "THE GULF  ·  MISSILES OVER BAHRAIN", font=kick_font, fill=RED)
    y += 24
    head_font = font(SERIF, 62)
    head = "IRAN STRIKES BAHRAIN"
    hw = d.textlength(head, font=head_font)
    d.text(((SIZE - hw) / 2, y), head, font=head_font, fill=INK)
    y += 72
    body_font = font(SANS, 19)
    lead_body = (
        "Iran's Revolutionary Guards fired missiles and drones at US positions "
        "at the al-Riffa and Awali bases. Bahrain said the attack hit a civilian "
        "industrial site, starting a fire with no injuries, and its air "
        "defences intercepted further attacks."
    )
    lines = wrap(d, lead_body, body_font, width)
    y = text_block(d, MARGIN, y, lines, body_font, BODY_INK, 24)
    y += 6
    draw_flame_band(d, MARGIN, y, width, 64)
    y += 64 + 12
    rule(d, MARGIN, y, right, 2)
    y += 12

    # ---- Grid: six stories, two columns x three rows ----
    stories = [
        ("ANTALYA  ·  CLIMATE",
         "COP31 IN DOUBLE OVERTIME",
         "The UN climate summit stalls as the new draft drops the words "
         "\u201cfossil fuels\u201d; ministers demand the phase-out wording back."),
        ("SINALOA  ·  MEXICO",
         "CARTEL BOSS CAPTURED",
         "Mexican forces seize Fausto Isidro Meza Flores, known as "
         "\u201cEl Chapo Isidro\u201d; 11 are killed in the violence that follows."),
        ("SHENZHEN  ·  SUMMIT",
         "TRUMP, XI AND PUTIN MEET",
         "The three leaders hold a trilateral meeting and agree to begin "
         "talks on reducing nuclear risk."),
        ("NEW YORK  ·  MARKETS",
         "AI SELL-OFF HITS STOCKS",
         "The S&P 500 falls 3.7% and Japan's Nikkei 5.1% as investors dump "
         "AI and chip shares; US stocks enter correction."),
        ("BALTIC SEA  ·  WAR AT SEA",
         "RUSSIAN SHIP ABLAZE",
         "A cargo ship burns in the Gulf of Finland after a drone strike; "
         "Ukraine hits a Russian ship as a missile kills two in Kryvyi Rih."),
        ("WASHINGTON  ·  CYBER",
         "FBI DATABASE HACKED",
         "Trump confirms a breach of the FBI's National Crime Information "
         "Centre, the system holding fingerprints and wanted-person records."),
    ]
    col_w = (width - 28) // 2
    row_h = 136
    grid_top = y
    for i, (kicker, headline, body) in enumerate(stories):
        col = i % 2
        row = i // 2
        x = MARGIN + col * (col_w + 28)
        cy = grid_top + row * row_h
        d.text((x, cy), kicker, font=kick_font, fill=RED)
        h_font = font(SERIF, 21)
        h_lines = wrap(d, headline, h_font, col_w)
        hy = text_block(d, x, cy + 24, h_lines[:2], h_font, INK, 26)
        b_font = font(SANS, 15)
        b_lines = wrap(d, body, b_font, col_w)
        text_block(d, x, hy + 2, b_lines[:3], b_font, BODY_INK, 19)
        if col == 0:
            d.line([(x + col_w + 14, cy), (x + col_w + 14, cy + row_h - 18)],
                   fill=LIGHT_RULE, width=1)
        if row < 2:
            rule(d, x, cy + row_h - 6, x + col_w, 1, LIGHT_RULE)
    y = grid_top + 3 * row_h + 4
    rule(d, MARGIN, y, right, 2)
    y += 12

    # ---- Briefs ----
    d.text((MARGIN, y), "IN BRIEF", font=kick_font, fill=RED)
    y += 24
    brief_font = font(SANS, 15)
    briefs = [
        "EU and Indonesia sign a trade deal after ten years of talks.",
        "Denmark expels a Russian attach\u00e9 over an alleged plot.",
        "Thousands march in Lisbon over living costs; protests in France.",
        "Boat capsizes in Nigeria, 24 dead; Jakarta factory fire, 36 missing.",
        "Israeli strike hits a Gaza aid vehicle; three killed.",
    ]
    for item in briefs:
        d.text((MARGIN + 14, y), "\u2022", font=brief_font, fill=RED)
        lines = wrap(d, item, brief_font, width - 14)
        y = text_block(d, MARGIN + 32, y, lines, brief_font, BODY_INK, 19)
        y += 1
    y += 4
    rule(d, MARGIN, y, right, 1, LIGHT_RULE)
    y += 8

    # ---- Footer: sources ----
    foot_font = font(SANS, 12)
    foot = ("Sources: OneTurn  ·  Dunya News  ·  Dawn  ·  The Economic Times  ·  "
            "China Daily Asia  —  first reported 22 November 2026")
    fw = d.textlength(foot, font=foot_font)
    d.text(((SIZE - fw) / 2, y), foot, font=foot_font, fill=BODY_INK)

    out = HERE / "entry.png"
    img.save(out, format="PNG", optimize=True)
    raw = out.read_bytes()
    print(f"wrote {out} ({len(raw)} bytes)")


if __name__ == "__main__":
    main()
