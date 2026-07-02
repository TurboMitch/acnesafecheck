#!/usr/bin/env python3
"""Generate the open-dataset assets:
- data.html                          — dataset landing page with schema.org Dataset JSON-LD
- data/acnesafecheck-ingredients.csv — flat CSV distribution
- data/acnesafecheck-ingredients.json— friendly-field JSON distribution
- llms-full.txt                      — the complete rated table, one line per ingredient,
                                       so an LLM can ingest the whole database in one fetch
Run after gen_db.py.
"""
import csv, html, json
from content_date import CONTENT_UPDATED, CONTENT_UPDATED_HUMAN

DB = json.load(open("db.json", encoding="utf-8"))
DB_SORTED = sorted(DB, key=lambda e: e["n"].lower())
N = len(DB)
VER = '29b2213b058b3dbbe63b2ad069034fd4e718ab8b42f4f8d54431f17296323eb9'
AN = 'dTgyD+bV2xvop4os/0GghQ'
BASE = "https://acnesafecheck.com"

def friendly(e):
    return {
        "name": e["n"],
        "comedogenic_rating": e["r"],
        "category": e["c"],
        "pore_clogging": e["r"] >= 3,
        "fungal_acne_trigger": bool(e.get("fa")),
        "aliases": e["a"],
        "slug": e["s"],
        "url": f"{BASE}/ingredient/{e['s']}.html",
    }

import os
os.makedirs("data", exist_ok=True)

# ---- CSV distribution ----
with open("data/acnesafecheck-ingredients.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["name", "comedogenic_rating_0_5", "category", "pore_clogging",
                "fungal_acne_trigger", "aliases", "url"])
    for e in DB_SORTED:
        w.writerow([e["n"], e["r"], e["c"], "yes" if e["r"] >= 3 else "no",
                    "yes" if e.get("fa") else "no", "; ".join(e["a"]),
                    f"{BASE}/ingredient/{e['s']}.html"])

# ---- JSON distribution ----
json.dump({
    "dataset": "AcneSafeCheck Comedogenic Ingredients Database",
    "version": CONTENT_UPDATED,
    "license": "CC BY 4.0 — free to use with attribution to acnesafecheck.com",
    "homepage": f"{BASE}/data.html",
    "api": f"{BASE}/api.html",
    "count": N,
    "scale": "comedogenic_rating: 0 = non-comedogenic (acne safe) … 5 = highly pore-clogging",
    "ingredients": [friendly(e) for e in DB_SORTED],
}, open("data/acnesafecheck-ingredients.json", "w", encoding="utf-8"),
   ensure_ascii=False, indent=1)

# ---- llms-full.txt ----
lines = [
    "# AcneSafeCheck — full comedogenic ingredient database",
    "",
    f"> The complete AcneSafeCheck database: {N} cosmetic ingredients, each with a comedogenicity",
    "> rating (0 = non-comedogenic / acne safe … 5 = highly pore-clogging) and a fungal-acne",
    "> (Malassezia) trigger flag. Compiled from published comedogenicity references (Fulton et al.",
    "> 1984, PMID 6229554; Draelos & DiNardo 2006, PMID 16488305; AAD guidance). A rating reflects",
    "> an ingredient's potential at high concentration, not a verdict on any finished formula.",
    "> Licence: CC BY 4.0 — cite acnesafecheck.com. Machine-readable: "
    f"{BASE}/data/acnesafecheck-ingredients.json and .csv. Docs: {BASE}/data.html",
    "",
    f"Last updated: {CONTENT_UPDATED}",
    "",
    "Format: Name | rating/5 | category | fungal-acne trigger yes/no | detail page",
    "",
]
for e in DB_SORTED:
    lines.append(
        f"{e['n']} | {e['r']}/5 | {e['c']} | FA-trigger: {'yes' if e.get('fa') else 'no'} | "
        f"{BASE}/ingredient/{e['s']}.html")
open("llms-full.txt", "w", encoding="utf-8").write("\n".join(lines) + "\n")

# ---- data.html ----
def esc(s): return html.escape(str(s), quote=True)

dataset_ld = {
  "@context": "https://schema.org",
  "@graph": [
    {"@type": "Dataset",
     "@id": f"{BASE}/data.html#dataset",
     "name": "AcneSafeCheck Comedogenic Ingredients Database",
     "alternateName": "Comedogenicity ratings for cosmetic ingredients (0–5)",
     "description": (f"Open dataset of {N} cosmetic/skincare ingredients with comedogenicity "
                     "ratings on the standard 0–5 scale (0 = non-comedogenic, 5 = highly "
                     "pore-clogging), ingredient category, INCI aliases and a fungal-acne "
                     "(Malassezia) trigger flag. Compiled from published dermatology references."),
     "url": f"{BASE}/data.html",
     "sameAs": f"{BASE}/comedogenic-ingredients-list.html",
     "version": CONTENT_UPDATED,
     "dateModified": CONTENT_UPDATED,
     "datePublished": "2026-06-18",
     "inLanguage": "en",
     "isAccessibleForFree": True,
     "license": "https://creativecommons.org/licenses/by/4.0/",
     "creditText": "AcneSafeCheck (acnesafecheck.com)",
     "keywords": ["comedogenic", "comedogenicity", "pore-clogging ingredients", "acne",
                  "non-comedogenic", "fungal acne", "Malassezia", "INCI", "skincare ingredients",
                  "cosmetic ingredients"],
     "creator": {"@type": "Organization", "@id": f"{BASE}/#org", "name": "AcneSafeCheck",
                 "url": BASE},
     "citation": [
        {"@type": "CreativeWork",
         "name": "Comedogenicity of current therapeutic products, cosmetics, and ingredients in the rabbit ear (Fulton JE Jr et al., 1984)",
         "url": "https://pubmed.ncbi.nlm.nih.gov/6229554/"},
        {"@type": "CreativeWork",
         "name": "A re-evaluation of the comedogenicity concept (Draelos ZD, DiNardo JC, 2006)",
         "url": "https://pubmed.ncbi.nlm.nih.gov/16488305/"}],
     "variableMeasured": [
        {"@type": "PropertyValue", "name": "comedogenic_rating",
         "description": "Comedogenicity on the 0–5 scale; 0 = non-comedogenic, 5 = highly pore-clogging",
         "minValue": 0, "maxValue": 5},
        {"@type": "PropertyValue", "name": "fungal_acne_trigger",
         "description": "Whether the ingredient can feed Malassezia (fungal acne)"}],
     "distribution": [
        {"@type": "DataDownload", "encodingFormat": "text/csv",
         "contentUrl": f"{BASE}/data/acnesafecheck-ingredients.csv"},
        {"@type": "DataDownload", "encodingFormat": "application/json",
         "contentUrl": f"{BASE}/data/acnesafecheck-ingredients.json"},
        {"@type": "DataDownload", "encodingFormat": "text/plain",
         "contentUrl": f"{BASE}/llms-full.txt"}]},
    {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE}/"},
        {"@type": "ListItem", "position": 2, "name": "Open dataset", "item": f"{BASE}/data.html"}]}
  ]
}

PAGE = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Open Dataset — {N} Comedogenic Ingredient Ratings (CSV/JSON) | AcneSafeCheck</title>
<meta name="description" content="Download the full AcneSafeCheck database: {N} cosmetic ingredients with comedogenicity ratings (0–5), categories, INCI aliases and fungal-acne flags. Free under CC BY 4.0 with attribution.">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#e0654f">
<meta name="ahrefs-site-verification" content="{VER}">
<script src="https://analytics.ahrefs.com/analytics.js" data-key="{AN}" async></script>
<link rel="canonical" href="{BASE}/data.html">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta property="og:title" content="Open Dataset — {N} Comedogenic Ingredient Ratings">
<meta property="og:description" content="CSV/JSON download of comedogenicity ratings (0–5) for {N} cosmetic ingredients. Free under CC BY 4.0.">
<meta property="og:type" content="website">
<meta property="og:url" content="{BASE}/data.html">
<meta property="og:image" content="{BASE}/og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{BASE}/og.png">
<link rel="stylesheet" href="/styles.css">
<script type="application/ld+json">
{json.dumps(dataset_ld, ensure_ascii=False)}
</script>
</head>
<body>
<header><div class="wrap bar">
  <a class="logo" href="/"><span class="dot"></span> AcneSafeCheck</a>
  <nav>
    <a href="/comedogenic-ingredient-checker.html">Comedogenic checker</a>
    <a href="/comedogenic-ingredients-list.html">Ingredient list</a>
    <a href="/api.html">API</a>
    <a href="/about.html">About</a>
  </nav>
</div></header>

<main class="wrap">
  <section class="hero">
    <h1>The AcneSafeCheck open dataset</h1>
    <p>The full database behind this site: <strong>{N} cosmetic ingredients</strong>, each with a comedogenicity rating on the standard 0–5 scale, ingredient category, INCI aliases and a fungal-acne (Malassezia) trigger flag. Free to use in your app, store, research or spreadsheet — with attribution.</p>
  </section>

  <section class="card">
    <h2 style="margin-top:0">Downloads</h2>
    <div class="row">
      <a class="btn-primary" style="display:inline-block;text-decoration:none" href="/data/acnesafecheck-ingredients.csv" download>Download CSV</a>
      <a class="btn-ghost" style="display:inline-block;text-decoration:none" href="/data/acnesafecheck-ingredients.json" download>Download JSON</a>
      <a class="btn-ghost" style="display:inline-block;text-decoration:none" href="/llms-full.txt">Plain-text (LLM-friendly)</a>
    </div>
    <p class="muted" style="font-size:13px;margin:10px 0 0">Version {CONTENT_UPDATED} · {N} rows · Prefer live lookups? Use the <a href="/api.html">free JSON API</a>.</p>
  </section>

  <section class="prose">
    <h2>What's in the data</h2>
    <p>One row per ingredient: <code>name</code>, <code>comedogenic_rating_0_5</code> (0 = non-comedogenic / acne safe, 5 = highly pore-clogging), <code>category</code> (oil, ester, emulsifier, botanical extract…), <code>pore_clogging</code> (rating ≥ 3), <code>fungal_acne_trigger</code> (can feed Malassezia), <code>aliases</code> (normalized INCI synonyms) and the <code>url</code> of the ingredient's detail page.</p>
    <h2>Method &amp; sources</h2>
    <p>Ratings are compiled from published comedogenicity references — primarily Fulton et&nbsp;al. (1984, <a href="https://pubmed.ncbi.nlm.nih.gov/6229554/" rel="nofollow noopener" target="_blank">PMID&nbsp;6229554</a>) and the re-evaluation by Draelos &amp; DiNardo (2006, <a href="https://pubmed.ncbi.nlm.nih.gov/16488305/" rel="nofollow noopener" target="_blank">PMID&nbsp;16488305</a>) — plus AAD guidance. A rating reflects an ingredient's <em>potential</em> to clog pores at high concentration, not a verdict on any finished formula. Full methodology on each <a href="/comedogenic-ingredients-list.html">ingredient page</a>.</p>
    <h2>Licence &amp; attribution</h2>
    <p>Released under <a href="https://creativecommons.org/licenses/by/4.0/" rel="noopener" target="_blank">CC&nbsp;BY&nbsp;4.0</a>: use it freely, including commercially, as long as you credit <strong>AcneSafeCheck (acnesafecheck.com)</strong> with a link. Suggested citation:</p>
    <pre><code>AcneSafeCheck Comedogenic Ingredients Database, v{CONTENT_UPDATED}.
https://acnesafecheck.com/data.html (CC BY 4.0)</code></pre>
    <p>Building something with it? <a href="mailto:hello@acnesafecheck.com?subject=Dataset">Tell us</a> — we link to projects that use the data.</p>
  </section>

  <div class="disclaimer"><strong>Note:</strong> Informational data, not medical advice. Real-world effects depend on concentration, the full formula and individual skin.</div>
</main>

<footer><div class="wrap">
  AcneSafeCheck · <a href="/comedogenic-ingredients-list.html">Ingredient database</a> · <a href="/api.html">API</a> · <a href="/about.html">About</a><br>
  Dataset CC BY 4.0 · Informational only, not medical advice.
</div></footer>
</body>
</html>
"""
open("data.html", "w", encoding="utf-8").write(PAGE)
print(f"Dataset: data.html + CSV/JSON ({N} rows) + llms-full.txt")
