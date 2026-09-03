#!/usr/bin/env python3
"""LEMONICA — Hollywood district deck (3 slides) from CoStar data."""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
import copy

INK = RGBColor(0x14, 0x14, 0x0B)
INK2 = RGBColor(0x1E, 0x1E, 0x12)
CREAM = RGBColor(0xF5, 0xF0, 0xE2)
WHITE = RGBColor(0xFF, 0xFD, 0xF6)
LEMON = RGBColor(0xE3, 0xB6, 0x2C)
LEMON_SOFT = RGBColor(0xEC, 0xC5, 0x58)
MUTED = RGBColor(0x9B, 0x97, 0x86)
GREY = RGBColor(0x6F, 0x6C, 0x5E)

SERIF = "Georgia"
SANS = "Arial"

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]


def slide():
    s = prs.slides.add_slide(BLANK)
    bg = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid(); bg.fill.fore_color.rgb = INK
    bg.line.fill.background()
    bg.shadow.inherit = False
    return s


def tx(s, x, y, w, h, runs, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, line_spacing=1.0):
    """runs: list of paragraphs; each paragraph = list of (text, size, color, bold, italic, font)"""
    box = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for i, para in enumerate(runs):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = line_spacing
        for (text, size, color, bold, italic, font) in para:
            r = p.add_run()
            r.text = text
            r.font.size = Pt(size)
            r.font.color.rgb = color
            r.font.bold = bold
            r.font.italic = italic
            r.font.name = font
    return box


def footer(s, page):
    tx(s, 0.6, 7.02, 10.5, 0.35, [[
        ("Источник: CoStar Group, Multi-Family Market Report (Fort Lauderdale, Q3 2026), демография по радиусу 1801–1848 N Young Cir, отчёт от 02.09.2026 · PDF: PDF090226_CoStar_YoungCircle.pdf",
         9, MUTED, False, False, SANS)]])
    tx(s, 12.35, 7.02, 0.5, 0.35, [[(str(page), 10, MUTED, True, False, SANS)]], align=PP_ALIGN.RIGHT)


def header(s, kicker, title_runs, sub=None):
    tx(s, 0.6, 0.42, 8.0, 0.3, [[(kicker, 12, LEMON_SOFT, True, False, SANS)]])
    tx(s, 0.6, 0.78, 12.1, 1.5, [title_runs], line_spacing=1.02)
    if sub:
        tx(s, 0.6, 2.05, 12.1, 0.5, [[(sub, 14, MUTED, False, False, SANS)]])


def stat_card(s, x, y, w, h, big, label, sub=None, accent=LEMON):
    card = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    card.adjustments[0] = 0.07
    card.fill.solid(); card.fill.fore_color.rgb = INK2
    card.line.color.rgb = RGBColor(0x3A, 0x3A, 0x22); card.line.width = Pt(1)
    card.shadow.inherit = False
    pad = 0.28
    paras = [[(big, 30, accent, True, False, SERIF)],
             [(label, 12.5, WHITE, True, False, SANS)]]
    if sub:
        paras.append([(sub, 10.5, MUTED, False, False, SANS)])
    tx(s, x + pad, y + pad - 0.04, w - 2 * pad, h - 2 * pad, paras, line_spacing=1.05)


# ============ SLIDE 1 — население ============
s = slide()
header(s, "ГОЛЛИВУД · ФЛОРИДА · 01",
       [("Район растёт: ", 40, WHITE, True, False, SERIF), ("+", 40, LEMON, True, False, SERIF),
        ("7–9% населения", 40, LEMON, True, False, SERIF), (" к 2030 году", 40, WHITE, True, False, SERIF)],
       "Население в радиусе ресторана (CoStar, прогноз 2025 → 2030)")

# chart area
cx, cy, cw, ch = 0.9, 2.85, 7.6, 3.6
groups = [("2 мили", 94132, 100899, "+7,2%"),
          ("5 миль", 382933, 416086, "+8,7%"),
          ("10 миль", 1207030, 1297766, "+7,5%")]
vmax = 1300000.0
band_w = cw / 3
for i, (label, v25, v30, growth) in enumerate(groups):
    gx = cx + i * band_w
    bw = 0.62
    h25 = (v25 / vmax) * (ch - 0.75)
    h30 = (v30 / vmax) * (ch - 0.75)
    b25 = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(gx + 0.55), Inches(cy + ch - 0.75 - h25), Inches(bw), Inches(h25))
    b25.fill.solid(); b25.fill.fore_color.rgb = RGBColor(0x4A, 0x4A, 0x30); b25.line.fill.background(); b25.shadow.inherit = False
    b30 = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(gx + 1.25), Inches(cy + ch - 0.75 - h30), Inches(bw), Inches(h30))
    b30.fill.solid(); b30.fill.fore_color.rgb = LEMON; b30.line.fill.background(); b30.shadow.inherit = False
    def fmt(v):
        return f"{v/1e6:.2f} млн" if v >= 1e6 else f"{v/1e3:.0f} тыс."
    tx(s, gx + 0.35, cy + ch - 0.75 - h25 - 0.34, 1.1, 0.3, [[(fmt(v25), 10.5, MUTED, False, False, SANS)]], align=PP_ALIGN.CENTER)
    tx(s, gx + 1.05, cy + ch - 0.75 - h30 - 0.34, 1.1, 0.3, [[(fmt(v30), 10.5, LEMON_SOFT, True, False, SANS)]], align=PP_ALIGN.CENTER)
    tx(s, gx + 0.25, cy + ch - 0.42, band_w - 0.5, 0.3, [[(label, 13, WHITE, True, False, SANS)]], align=PP_ALIGN.CENTER)
    tx(s, gx + 0.25, cy + ch + 0.02, band_w - 0.5, 0.3, [[(growth, 13, LEMON, True, False, SERIF)]], align=PP_ALIGN.CENTER)
# legend
tx(s, cx + 0.35, cy - 0.28, 3.5, 0.3, [[("■ ", 11, RGBColor(0x4A,0x4A,0x30), False, False, SANS), ("2025    ", 11, MUTED, False, False, SANS),
                                      ("■ ", 11, LEMON, False, False, SANS), ("2030 (прогноз)", 11, MUTED, False, False, SANS)]])

# right column callouts
stat_card(s, 9.05, 2.75, 3.7, 1.55, "1,30 млн", "жителей в радиусе 10 миль — 2030", "сегодня 1,21 млн")
stat_card(s, 9.05, 4.45, 3.7, 1.55, "+33 000", "новых соседей ресторана за 5 лет", "только в радиусе 2 миль")
footer(s, 1)

# ============ SLIDE 2 — люди и доходы ============
s = slide()
header(s, "ГОЛЛИВУД · ФЛОРИДА · 02",
       [("Кто живет рядом: ", 40, WHITE, True, False, SERIF), ("средний класс с доходом", 40, LEMON, True, False, SERIF)],
       "Доходы, возраст и жильё вокруг Young Circle (CoStar, 2025)")

stat_card(s, 0.7, 2.8, 3.9, 1.9, "$60 099", "медианный доход домохозяйства", "радиус 2 мили от ресторана")
stat_card(s, 4.75, 2.8, 3.9, 1.9, "$67 691", "медианный доход домохозяйства", "радиус 5 миль")
stat_card(s, 8.8, 2.8, 3.9, 1.9, "$71 363", "медианный доход домохозяйства", "радиус 10 миль")

stat_card(s, 0.7, 4.9, 3.9, 1.75, "42 253 → 45 179", "домохозяйств в 2 милях", "+6,9% к 2030 году")
stat_card(s, 4.75, 4.9, 3.9, 1.75, "$443 846", "медианная стоимость жилья", "владельцы домов — аудитория ресторана")
stat_card(s, 8.8, 4.9, 3.9, 1.75, "44 года", "средний возраст жителей", "стабильная взрослая клиентская база")
footer(s, 2)

# ============ SLIDE 3 — стройка и спрос ============
s = slide()
header(s, "ГОЛЛИВУД · ФЛОРИДА · 03",
       [("Город застраивается — ", 40, WHITE, True, False, SERIF), ("спрос опережает предложение", 40, LEMON, True, False, SERIF)],
       "Субмаркет Hollywood / Dania Beach и рынок Fort Lauderdale (CoStar, Q3 2026)")

stat_card(s, 0.7, 2.8, 3.9, 1.9, "868", "квартир построено за 12 месяцев", "в субмаркете Hollywood / Dania Beach")
stat_card(s, 4.75, 2.8, 3.9, 1.9, "624", "квартир строится прямо сейчас", "+2,9% к жилому фонду района")
stat_card(s, 8.8, 2.8, 3.9, 1.9, "+1,1%", "рост аренды за год", "2-й результат из 9 субмаркетов")

stat_card(s, 0.7, 4.9, 3.9, 1.75, "$2 160", "средняя ставка аренды", "в субмаркете Hollywood / Dania Beach")
stat_card(s, 4.75, 4.9, 3.9, 1.75, "6 345", "квартир строится в рынке Ft. Lauderdale", "инвестиции $1,5 млрд за год")
stat_card(s, 8.8, 4.9, 3.9, 1.75, "311", "квартир — новый дом у Young Circle", "комплекс Radius, 1801–1848 N Young Cir")
footer(s, 3)

OUT = "/Users/denysharbuzov/Documents/Limonika_Sale_Landing_2026-09-02/presentation/Hollywood_District_CoStar_3slides.pptx"
import os
os.makedirs(os.path.dirname(OUT), exist_ok=True)
prs.save(OUT)
print("saved", OUT)
