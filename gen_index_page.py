#!/usr/bin/env python3
"""Generate /ingredients.html — a crawlable A–Z index of every ingredient.
Distributes internal link equity from the homepage/nav to all 560 pages."""
import json, html, datetime

DB = json.load(open("db.json", encoding="utf-8"))
VER = '29b2213b058b3dbbe63b2ad069034fd4e718ab8b42f4f8d54431f17296323eb9'
AN = 'dTgyD+bV2xvop4os/0GghQ'
MOD_HUMAN = datetime.date.today().strftime("%B %Y")

def esc(s): return html.escape(s, quote=True)
def pill(r):
    if r >= 3: return f'<span class="pill bad">{r}/5</span>'
    if r >= 1: return f'<span class="pill low">{r}/5</span>'
    return '<span class="pill safe">0/5</span>'

# Group A–Z (non-alpha first chars go under '#')
groups = {}
for e in sorted(DB, key=lambda x: x["n"].lower()):
    first = e["n"][0].upper()
    key = first if first.isalpha() else "#"
    groups.setdefault(key, []).append(e)

letters = sorted(groups.keys())
nav = ' '.join(f'<a href="#{l}">{l}</a>' for l in letters)

sections = []
for l in letters:
    items = ''.join(
        f'<li><a href="/ingredient/{e["s"]}.html">{esc(e["n"])}</a> {pill(e["r"])}</li>'
        for e in groups[l])
    sections.append(
        f'<section id="{l}" class="prose"><h2>{l}</h2>'
        f'<ul class="ingindex">{items}</ul></section>')

links_total = len(DB)
sections_html = ''.join(sections)
PAGE = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>All Comedogenic Ingredients (A–Z Index of {links_total}) | AcneSafeCheck</title>
<meta name="description" content="Browse every ingredient in the AcneSafeCheck database — {links_total} skincare and makeup ingredients with their comedogenic (pore-clogging) rating from 0 to 5, indexed A to Z.">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#e0654f">
<meta name="ahrefs-site-verification" content="{VER}">
<script src="https://analytics.ahrefs.com/analytics.js" data-key="{AN}" async></script>
<link rel="canonical" href="https://acnesafecheck.com/ingredients.html">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta property="og:title" content="All Comedogenic Ingredients (A–Z Index)">
<meta property="og:description" content="Every ingredient in the database with its 0–5 comedogenic rating, indexed A–Z.">
<meta property="og:type" content="website">
<meta property="og:url" content="https://acnesafecheck.com/ingredients.html">
<meta property="og:image" content="https://acnesafecheck.com/og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://acnesafecheck.com/og.png">
<link rel="stylesheet" href="/styles.css">
<style>.ingindex{{list-style:none;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:4px 18px}}.ingindex li{{display:flex;justify-content:space-between;align-items:center;gap:8px;padding:3px 0;border-bottom:1px solid #f1e9e5}}.azbar{{position:sticky;top:0;background:#fff;padding:8px 0;font-weight:700;letter-spacing:1px}}.azbar a{{display:inline-block;padding:2px 6px}}</style>
<script type="application/ld+json">
{{"@context":"https://schema.org","@graph":[
{{"@type":"CollectionPage","@id":"https://acnesafecheck.com/ingredients.html#page","name":"All comedogenic ingredients (A–Z)","description":"Index of {links_total} skincare and makeup ingredients with their 0–5 comedogenic rating.","url":"https://acnesafecheck.com/ingredients.html","inLanguage":"en","isPartOf":{{"@id":"https://acnesafecheck.com/#site"}},"publisher":{{"@type":"Organization","@id":"https://acnesafecheck.com/#org","name":"AcneSafeCheck"}}}},
{{"@type":"BreadcrumbList","itemListElement":[
{{"@type":"ListItem","position":1,"name":"Home","item":"https://acnesafecheck.com/"}},
{{"@type":"ListItem","position":2,"name":"All ingredients","item":"https://acnesafecheck.com/ingredients.html"}}]}}]}}
</script>
</head>
<body>
<header><div class="wrap bar">
  <a class="logo" href="/"><span class="dot"></span> AcneSafeCheck</a>
  <nav>
    <a href="/comedogenic-ingredient-checker.html">Comedogenic checker</a>
    <a href="/pore-clogging-ingredient-checker.html">Pore-clogging</a>
    <a href="/ingredients.html">All ingredients</a>
    <a href="/about.html">About</a>
  </nav>
</div></header>

<main class="wrap">
  <section class="hero">
    <h1>All comedogenic ingredients (A–Z)</h1>
    <p>Every one of the <strong>{links_total} ingredients</strong> in our database, with its comedogenicity rating from 0 (acne safe) to 5 (high pore-clogging risk). Looking for one product? Use the <a href="/comedogenic-ingredient-checker.html">ingredient checker</a> or the <a href="/comedogenic-ingredients-list.html">searchable list</a>.</p>
  </section>
  <div class="azbar wrap" style="padding-left:0">{nav}</div>
  {sections_html}
  <div class="disclaimer"><strong>Note:</strong> Ratings are general guidance, not medical advice. Real-world effects depend on concentration, the full formula and your individual skin. Last updated {MOD_HUMAN}.</div>
</main>

<footer><div class="wrap">
  AcneSafeCheck · <a href="/comedogenic-ingredients-list.html">Searchable database</a> · <a href="/comedogenic-ingredient-checker.html">Comedogenic checker</a> · <a href="/about.html">About</a><br>
  Informational only, not medical advice.
</div></footer>
</body>
</html>
"""
open("ingredients.html", "w", encoding="utf-8").write(PAGE)
print(f"Generated ingredients.html with {links_total} links across {len(letters)} letter groups")
