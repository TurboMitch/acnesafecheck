#!/usr/bin/env python3
"""Generate /vs/<a>-vs-<b>.html comparison pages for commonly-compared ingredients,
plus a /vs/index.html hub. Query-shaped content ("X vs Y for acne") for search and
LLM answers. Pairs are validated against db.json — unknown names fail the build.
Run after gen_db.py."""
import html, json, os
from content_date import CONTENT_UPDATED, CONTENT_UPDATED_HUMAN

DB = json.load(open("db.json", encoding="utf-8"))
by_name = {e["n"]: e for e in DB}
VER = '29b2213b058b3dbbe63b2ad069034fd4e718ab8b42f4f8d54431f17296323eb9'
AN = 'dTgyD+bV2xvop4os/0GghQ'
BASE = "https://acnesafecheck.com"
PUBLISHED = CONTENT_UPDATED

# Commonly-compared pairs (both names must exist in db.json).
PAIRS = [
    ("Coconut Oil", "Jojoba Oil"),
    ("Shea Butter", "Cocoa Butter"),
    ("Squalane", "Jojoba Oil"),
    ("Argan Oil", "Rosehip Oil"),
    ("Coconut Oil", "Olive Oil"),
    ("Sunflower Oil", "Safflower Oil"),
    ("Hemp Seed Oil", "Argan Oil"),
    ("Grapeseed Oil", "Jojoba Oil"),
    ("Mineral Oil", "Petrolatum"),
    ("Cetyl Alcohol", "Cetearyl Alcohol"),
    ("Dimethicone", "Cyclopentasiloxane"),
    ("Glycerin", "Hyaluronic Acid"),
    ("Niacinamide", "Salicylic Acid"),
    ("Beeswax", "Candelilla Wax"),
    ("Lanolin", "Petrolatum"),
    ("Tea Tree Oil", "Salicylic Acid"),
    ("Zinc Oxide", "Titanium Dioxide"),
    ("Sweet Almond Oil", "Jojoba Oil"),
    ("Avocado Oil", "Olive Oil"),
    ("Castor Oil", "Coconut Oil"),
]

for a, b in PAIRS:
    for n in (a, b):
        if n not in by_name:
            raise SystemExit(f"FATAL: '{n}' not in db.json — fix PAIRS in gen_vs.py")

os.makedirs("vs", exist_ok=True)
def esc(s): return html.escape(str(s), quote=True)
def jp(s): return json.dumps(str(s))[1:-1].replace("</", "<\\/")

def pill(r):
    if r >= 3: return f'<span class="pill bad">Clogging risk · {r}/5</span>'
    if r >= 1: return f'<span class="pill low">Low risk · {r}/5</span>'
    return '<span class="pill safe">Acne safe · 0/5</span>'

def rating_phrase(r):
    if r >= 4: return "a high pore-clogging risk"
    if r == 3: return "a moderate pore-clogging risk"
    if r == 2: return "a mild, low pore-clogging risk"
    if r == 1: return "a very low pore-clogging risk"
    return "non-comedogenic (acne safe)"

def verdict(ea, eb):
    """One-paragraph verdict comparing two entries for acne-prone skin."""
    a, b = ea["n"], eb["n"]
    ra, rb = ea["r"], eb["r"]
    faa, fab = bool(ea.get("fa")), bool(eb.get("fa"))
    if ra == rb:
        base = (f"{a} and {b} score the same on the comedogenic scale ({ra}/5), so for "
                f"pore-clogging alone there is no clear winner.")
        if faa != fab:
            safer = b if faa else a
            other = a if faa else b
            base += (f" The tiebreaker is fungal acne: {other} can feed Malassezia while "
                     f"{safer} is not a common trigger, so {safer} is the safer default if "
                     f"you're prone to fungal breakouts.")
        else:
            base += " Pick on texture, price and how your own skin responds — and patch test."
        return base
    lo, hi = (ea, eb) if ra < rb else (eb, ea)
    s = (f"{lo['n']} is the safer choice for acne-prone skin: it rates {lo['r']}/5 "
         f"({rating_phrase(lo['r'])}) versus {hi['r']}/5 for {hi['n']} "
         f"({rating_phrase(hi['r'])}).")
    if bool(lo.get("fa")):
        s += (f" One caveat: {lo['n']} can still feed Malassezia, so it isn't the best pick "
              f"if fungal acne is your problem.")
    elif bool(hi.get("fa")):
        s += f" {hi['n']} is also a common fungal-acne (Malassezia) trigger — another reason to avoid it."
    return s

def winner_name(ea, eb):
    if ea["r"] < eb["r"]: return ea["n"]
    if eb["r"] < ea["r"]: return eb["n"]
    faa, fab = bool(ea.get("fa")), bool(eb.get("fa"))
    if faa != fab: return eb["n"] if faa else ea["n"]
    return None  # true tie

def fa_cell(e): return "Yes — can feed Malassezia" if e.get("fa") else "No"

def row(label, va, vb):
    return f"<tr><td><strong>{label}</strong></td><td>{va}</td><td>{vb}</td></tr>"

TPL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{a} vs {b} for Acne: Which Clogs Pores? | AcneSafeCheck</title>
<meta name="description" content="{a} ({ra}/5) vs {b} ({rb}/5) on the comedogenic scale — which is safer for acne-prone skin, plus fungal-acne status and acne-safe alternatives.">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#e0654f">
<meta name="ahrefs-site-verification" content="{ver}">
<script src="https://analytics.ahrefs.com/analytics.js" data-key="{an}" async></script>
<link rel="canonical" href="{base}/vs/{slug}.html">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta property="og:title" content="{a} vs {b} for Acne: Which Clogs Pores?">
<meta property="og:description" content="{a} rates {ra}/5, {b} rates {rb}/5 on the comedogenicity scale. See which is safer for acne-prone skin.">
<meta property="og:type" content="article">
<meta property="og:url" content="{base}/vs/{slug}.html">
<meta property="og:image" content="{base}/og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{base}/og.png">
<link rel="stylesheet" href="/styles.css">
<script type="application/ld+json">
{jsonld}
</script>
</head>
<body>
<header><div class="wrap bar">
  <a class="logo" href="/"><span class="dot"></span> AcneSafeCheck</a>
  <nav>
    <a href="/comedogenic-ingredient-checker.html">Comedogenic checker</a>
    <a href="/comedogenic-ingredients-list.html">Ingredient list</a>
    <a href="/vs/index.html">Comparisons</a>
    <a href="/about.html">About</a>
  </nav>
</div></header>

<main class="wrap">
  <p class="muted" style="font-size:13px;margin:14px 0 0"><a href="/vs/index.html">Comparisons</a> › {a} vs {b}</p>
  <section class="hero" style="padding-top:18px">
    <h1>{a} vs {b}: which is better for acne-prone skin?</h1>
    <p><strong>Quick answer:</strong> {quick}</p>
  </section>

  <section class="card">
    <h2 style="margin-top:0">Side by side</h2>
    <table style="width:100%;border-collapse:collapse;font-size:15px">
      <thead><tr><td></td><td><strong><a href="/ingredient/{sa}.html">{a}</a></strong></td><td><strong><a href="/ingredient/{sb}.html">{b}</a></strong></td></tr></thead>
      <tbody>
      {rows}
      </tbody>
    </table>
    <p class="muted" style="font-size:13px;margin:10px 0 0">Scale: 0 = non-comedogenic (won't clog pores) … 5 = very likely to clog pores.</p>
  </section>

  <section class="prose">
    <h2>The verdict</h2>
    <p>{verdict}</p>
    <h2>{a}: {ra}/5</h2>
    <p>{para_a} Full breakdown: <a href="/ingredient/{sa}.html">is {a} comedogenic?</a></p>
    <h2>{b}: {rb}/5</h2>
    <p>{para_b} Full breakdown: <a href="/ingredient/{sb}.html">is {b} comedogenic?</a></p>
    <h2>Checking a real product?</h2>
    <p>Single-ingredient ratings are guidance, not a lab test of a finished formula — concentration and the rest of the ingredient list matter (Draelos &amp; DiNardo, 2006). Paste the full list into the <a href="/comedogenic-ingredient-checker.html">comedogenic ingredient checker</a> to screen everything at once, or the <a href="/fungal-acne-safe-checker.html">fungal-acne checker</a> if Malassezia is your problem.</p>
    <p class="muted" style="font-size:13px">By <a href="/about.html">Mitchell Zandwijken</a> · Rated against published comedogenicity references (Fulton 1984; Draelos &amp; DiNardo 2006) · Last updated {mod_human}.</p>
  </section>

  <div class="disclaimer"><strong>Note:</strong> Informational only, not medical advice. Real-world effects depend on concentration, the full formula and your individual skin.</div>
</main>

<footer><div class="wrap">
  AcneSafeCheck · <a href="/vs/index.html">All comparisons</a> · <a href="/comedogenic-ingredients-list.html">Ingredient database</a> · <a href="/comedogenic-ingredient-checker.html">Comedogenic checker</a> · <a href="/about.html">About</a><br>
  Informational only, not medical advice.
</div></footer>
</body>
</html>
"""

def para(e):
    r = e["r"]
    s = f"{e['n']} rates {r}/5 — {rating_phrase(r)}."
    if r >= 3:
        s += " If you break out easily, avoid it in leave-on products, especially when it appears near the top of the ingredient list."
    elif r >= 1:
        s += " Most skin tolerates it well; very reactive skin may want to patch test."
    else:
        s += " It is not known to clog pores and is generally a safe choice for acne-prone skin."
    s += (" It can also feed Malassezia, so people with fungal acne usually avoid it."
          if e.get("fa") else " It is not a common fungal-acne (Malassezia) trigger.")
    return s

made = []
for a, b in PAIRS:
    ea, eb = by_name[a], by_name[b]
    slug = f"{ea['s']}-vs-{eb['s']}"
    url = f"{BASE}/vs/{slug}.html"
    win = winner_name(ea, eb)
    v = verdict(ea, eb)
    if win:
        quick = (f"{win} is the safer pick for acne-prone skin. {a} rates {ea['r']}/5 and "
                 f"{b} rates {eb['r']}/5 on the comedogenic scale.")
    else:
        quick = (f"It's a tie on comedogenicity — both rate {ea['r']}/5. "
                 f"Choose on texture and how your skin responds.")
    rows = "\n      ".join([
        row("Comedogenic rating", pill(ea["r"]), pill(eb["r"])),
        row("Category", esc(ea["c"]), esc(eb["c"])),
        row("Pore-clogging (≥3)", "Yes" if ea["r"] >= 3 else "No", "Yes" if eb["r"] >= 3 else "No"),
        row("Fungal-acne trigger", fa_cell(ea), fa_cell(eb)),
    ])
    faq = [
        {"@type": "Question", "name": f"Which is better for acne-prone skin: {a} or {b}?",
         "acceptedAnswer": {"@type": "Answer", "text": v}},
        {"@type": "Question", "name": f"Is {a} comedogenic?",
         "acceptedAnswer": {"@type": "Answer",
                            "text": f"{a} has a comedogenicity rating of {ea['r']} out of 5 — {rating_phrase(ea['r'])}."}},
        {"@type": "Question", "name": f"Is {b} comedogenic?",
         "acceptedAnswer": {"@type": "Answer",
                            "text": f"{b} has a comedogenicity rating of {eb['r']} out of 5 — {rating_phrase(eb['r'])}."}},
    ]
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "@id": url + "#article",
         "headline": f"{a} vs {b} for Acne: Which Clogs Pores?",
         "description": f"{a} ({ea['r']}/5) vs {b} ({eb['r']}/5) on the comedogenic scale.",
         "url": url, "datePublished": PUBLISHED, "dateModified": CONTENT_UPDATED, "inLanguage": "en",
         "author": {"@type": "Person", "@id": f"{BASE}/#mitchell", "name": "Mitchell Zandwijken",
                    "url": f"{BASE}/about.html"},
         "publisher": {"@type": "Organization", "@id": f"{BASE}/#org", "name": "AcneSafeCheck",
                       "logo": {"@type": "ImageObject", "url": f"{BASE}/icon-512.png"}},
         "image": {"@type": "ImageObject", "url": f"{BASE}/og.png", "width": 1200, "height": 630},
         "mainEntityOfPage": {"@type": "WebPage", "@id": url},
         "about": [{"@type": "Thing", "name": a}, {"@type": "Thing", "name": b}]},
        {"@type": "FAQPage", "@id": url + "#faq", "mainEntity": faq},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE}/"},
            {"@type": "ListItem", "position": 2, "name": "Comparisons", "item": f"{BASE}/vs/index.html"},
            {"@type": "ListItem", "position": 3, "name": f"{a} vs {b}", "item": url}]},
    ]}
    page = TPL.format(a=esc(a), b=esc(b), ra=ea["r"], rb=eb["r"], sa=ea["s"], sb=eb["s"],
                      slug=slug, base=BASE, quick=esc(quick), verdict=esc(v),
                      para_a=esc(para(ea)), para_b=esc(para(eb)), rows=rows,
                      jsonld=json.dumps(ld, ensure_ascii=False),
                      mod_human=CONTENT_UPDATED_HUMAN, ver=VER, an=AN)
    open(f"vs/{slug}.html", "w", encoding="utf-8").write(page)
    made.append((a, b, slug, win, ea["r"], eb["r"]))

# ---- hub page ----
items = "\n".join(
    f'    <a class="tile" href="/vs/{slug}.html"><b>{esc(a)} vs {esc(b)}</b>'
    f'<span>{esc(a)} {ra}/5 · {esc(b)} {rb}/5 — {"winner: " + esc(win) if win else "tie"}</span></a>'
    for a, b, slug, win, ra, rb in made)
hub_ld = {"@context": "https://schema.org", "@graph": [
    {"@type": "CollectionPage", "@id": f"{BASE}/vs/index.html#page",
     "name": "Ingredient comparisons for acne-prone skin",
     "description": "Side-by-side comedogenicity comparisons of commonly confused skincare ingredients.",
     "url": f"{BASE}/vs/index.html", "inLanguage": "en",
     "isPartOf": {"@id": f"{BASE}/#site"},
     "publisher": {"@type": "Organization", "@id": f"{BASE}/#org", "name": "AcneSafeCheck"}},
    {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE}/"},
        {"@type": "ListItem", "position": 2, "name": "Comparisons", "item": f"{BASE}/vs/index.html"}]}]}
hub = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Ingredient Comparisons for Acne-Prone Skin — X vs Y, Which Clogs Pores? | AcneSafeCheck</title>
<meta name="description" content="Side-by-side comedogenicity comparisons of commonly confused skincare ingredients: coconut oil vs jojoba, shea vs cocoa butter, squalane vs jojoba and more.">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#e0654f">
<meta name="ahrefs-site-verification" content="{VER}">
<script src="https://analytics.ahrefs.com/analytics.js" data-key="{AN}" async></script>
<link rel="canonical" href="{BASE}/vs/index.html">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta property="og:title" content="Ingredient Comparisons for Acne-Prone Skin">
<meta property="og:description" content="X vs Y: which clogs pores? Side-by-side comedogenicity comparisons.">
<meta property="og:type" content="website">
<meta property="og:url" content="{BASE}/vs/index.html">
<meta property="og:image" content="{BASE}/og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{BASE}/og.png">
<link rel="stylesheet" href="/styles.css">
<script type="application/ld+json">
{json.dumps(hub_ld, ensure_ascii=False)}
</script>
</head>
<body>
<header><div class="wrap bar">
  <a class="logo" href="/"><span class="dot"></span> AcneSafeCheck</a>
  <nav>
    <a href="/comedogenic-ingredient-checker.html">Comedogenic checker</a>
    <a href="/comedogenic-ingredients-list.html">Ingredient list</a>
    <a href="/ingredients.html">All ingredients</a>
    <a href="/about.html">About</a>
  </nav>
</div></header>

<main class="wrap">
  <section class="hero">
    <h1>Ingredient comparisons</h1>
    <p>Side-by-side comedogenicity match-ups of ingredients people often choose between. Each comparison shows the 0–5 rating, fungal-acne status and a clear verdict for acne-prone skin.</p>
  </section>

  <div class="tiles">
{items}
  </div>

  <section class="prose">
    <p>Don't see your pair? Look both ingredients up in the <a href="/ingredients.html">A–Z index</a>, or paste a full product into the <a href="/comedogenic-ingredient-checker.html">comedogenic checker</a>.</p>
  </section>

  <div class="disclaimer"><strong>Note:</strong> Informational only, not medical advice.</div>
</main>

<footer><div class="wrap">
  AcneSafeCheck · <a href="/comedogenic-ingredients-list.html">Ingredient database</a> · <a href="/comedogenic-ingredient-checker.html">Comedogenic checker</a> · <a href="/about.html">About</a><br>
  Informational only, not medical advice.
</div></footer>
</body>
</html>
"""
open("vs/index.html", "w", encoding="utf-8").write(hub)
print(f"Generated {len(made)} vs pages + hub")
