#!/usr/bin/env python3
"""Generate downloads/acne-safe-cheat-sheet.pdf — the newsletter lead-magnet —
straight from db.json so it can never contradict the site.
Requires: pip install reportlab. Run after gen_db.py."""
import json
from content_date import CONTENT_UPDATED_HUMAN
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, PageBreak)

DB = json.load(open("db.json", encoding="utf-8"))
BRAND = colors.HexColor("#e0654f")
INK = colors.HexColor("#241f1c")
MUTED = colors.HexColor("#6f655e")
CREAM = colors.HexColor("#fbf7f4")
GREEN = colors.HexColor("#1faa59")

styles = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=styles["Title"], textColor=INK, fontSize=22, leading=26, spaceAfter=4)
H2 = ParagraphStyle("H2", parent=styles["Heading2"], textColor=BRAND, fontSize=14, leading=18, spaceBefore=14, spaceAfter=4)
BODY = ParagraphStyle("BODY", parent=styles["Normal"], textColor=INK, fontSize=9.5, leading=13)
SMALL = ParagraphStyle("SMALL", parent=styles["Normal"], textColor=MUTED, fontSize=8, leading=11)

def table(rows, col_widths, header=True):
    t = Table(rows, colWidths=col_widths, repeatRows=1 if header else 0)
    style = [
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("TEXTCOLOR", (0, 0), (-1, -1), INK),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, CREAM]),
        ("LINEBELOW", (0, 0), (-1, 0), 0.75, BRAND),
    ]
    if header:
        style += [("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                  ("TEXTCOLOR", (0, 0), (-1, 0), BRAND)]
    t.setStyle(TableStyle(style))
    return t

worst = sorted([e for e in DB if e["r"] >= 4], key=lambda e: (-e["r"], e["n"]))
moderate = sorted([e for e in DB if e["r"] == 3], key=lambda e: e["n"])
fa_safe_low = sorted([e for e in DB if e["r"] <= 1 and not e.get("fa")], key=lambda e: (e["r"], e["n"]))

# Safe swaps: for the biggest offender categories, list the lowest-rated same-category options.
SWAP_CATS = ["Oil", "Butter", "Ester", "Emulsifier", "Humectant", "Silicone"]
def safest(cat, n=4):
    pool = sorted([e for e in DB if e["c"] == cat and e["r"] <= 1],
                  key=lambda e: (e["r"], 0 if not e.get("fa") else 1, e["n"]))
    return pool[:n]

story = []
story.append(Paragraph("The Acne-Safe Cheat Sheet", H1))
story.append(Paragraph(
    f"Every rating in this sheet comes from the AcneSafeCheck database of {len(DB)} ingredients, "
    "compiled from published comedogenicity references (Fulton et al. 1984; Draelos &amp; DiNardo 2006; AAD). "
    "Scale: 0 = non-comedogenic (acne safe) … 5 = highly pore-clogging. 'FA' marks common "
    f"fungal-acne (Malassezia) triggers. Version: {CONTENT_UPDATED_HUMAN}.", SMALL))
story.append(Spacer(1, 6))

story.append(Paragraph("1. Red flags — avoid in leave-on products (rated 4–5)", H2))
rows = [["Ingredient", "Rating", "Category", "FA"]]
for e in worst:
    rows.append([e["n"], f"{e['r']}/5", e["c"], "yes" if e.get("fa") else ""])
story.append(table(rows, [72*mm, 16*mm, 40*mm, 12*mm]))
story.append(Spacer(1, 4))
story.append(Paragraph("Higher on the ingredient list = higher concentration = bigger risk.", SMALL))

story.append(PageBreak())
story.append(Paragraph("2. Watch-list — moderate risk (rated 3)", H2))
rows = [["Ingredient", "Category", "FA"]]
for e in moderate:
    rows.append([e["n"], e["c"], "yes" if e.get("fa") else ""])
story.append(table(rows, [80*mm, 45*mm, 15*mm]))

story.append(PageBreak())
story.append(Paragraph("3. Safe swaps by category (rated 0–1)", H2))
for cat in SWAP_CATS:
    picks = safest(cat)
    if not picks:
        continue
    line = " · ".join(f"{e['n']} ({e['r']}/5{', FA' if e.get('fa') else ''})" for e in picks)
    story.append(Paragraph(f"<b>{cat}:</b> {line}", BODY))
    story.append(Spacer(1, 3))
story.append(Spacer(1, 6))

story.append(Paragraph("4. Fungal acne? Start with these (rated 0–1, no Malassezia triggers)", H2))
names = ", ".join(e["n"] for e in fa_safe_low[:40])
story.append(Paragraph(names + ".", BODY))
story.append(Spacer(1, 6))

story.append(Paragraph("5. How to read any label in 30 seconds", H2))
for tip in [
    "1. Scan the first 5–7 ingredients — that's where the concentration is.",
    "2. Match them against section 1. One red flag near the top is usually enough to skip the product.",
    "3. \"Non-comedogenic\" on the front label is unregulated — always check the actual INCI list.",
    "4. A single ingredient's score isn't a verdict on a finished formula — treat it as a risk signal and patch test new products (Draelos & DiNardo, 2006).",
    "5. Small, itchy, uniform bumps? Run the fungal-acne check, not just the comedogenic one.",
]:
    story.append(Paragraph(tip, BODY))
    story.append(Spacer(1, 2))
story.append(Spacer(1, 10))
story.append(Paragraph(
    'Check any product in seconds: <b>acnesafecheck.com</b> — paste the list or scan a photo. '
    'Full database, comparisons and API: acnesafecheck.com/data.html. '
    'Informational only, not medical advice. © AcneSafeCheck, CC BY 4.0 with attribution.', SMALL))

import os
os.makedirs("downloads", exist_ok=True)
doc = SimpleDocTemplate("downloads/acne-safe-cheat-sheet.pdf", pagesize=A4,
                        leftMargin=18*mm, rightMargin=18*mm, topMargin=16*mm, bottomMargin=16*mm,
                        title="The Acne-Safe Cheat Sheet — AcneSafeCheck",
                        author="AcneSafeCheck (acnesafecheck.com)")
doc.build(story)
print(f"Cheat sheet: downloads/acne-safe-cheat-sheet.pdf ({len(worst)} red flags, {len(moderate)} watch-list)")
