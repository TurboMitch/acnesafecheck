# AcneSafeCheck

Free acne-safe / comedogenic ingredient checker. Static site (HTML + CSS + vanilla JS) with two Vercel serverless functions.

## Pages
- index.html — Acne safe ingredient checker (home)
- comedogenic-ingredient-checker.html / pore-clogging-ingredient-checker.html
- fungal-acne-safe-checker.html, product-checker.html (Open Beauty Facts search)
- comedogenic-ingredients-list.html — searchable 560-ingredient database
- ingredients.html — A–Z index; ingredient/*.html — 560 generated ingredient pages
- non-comedogenic/*.html — product roundups; article/*.html — guides
- api.html — public API docs; premium.html — waitlist

## API (api/)
- api/check.js — GET /api/check?ingredient=… or ?ingredients=… (public, rate/size-capped)
- api/subscribe.js — POST /api/subscribe (Resend audience; needs RESEND_API_KEY + RESEND_AUDIENCE_ID env vars)

## Generators — run in this order
    python3 gen_db.py           # db.json + checker.js + static table in comedogenic-ingredients-list.html
    python3 gen_data.py         # data.html + data/*.csv|json + llms-full.txt (open dataset)
    python3 gen_vs.py           # vs/*.html ingredient comparison pages + hub
    python3 gen_ingredients.py  # ingredient/*.html (from db.json)
    python3 gen_index_page.py   # ingredients.html (from db.json)
    python3 gen_articles.py     # article/*.html
    python3 gen_roundups.py     # non-comedogenic/*.html (validates ingredient links against db.json)
    python3 gen_sitemap.py      # sitemap.xml (lastmod from git history) — run LAST
    python3 gen_img.py          # only when the brand images change (needs Pillow + a TrueType font)

"Last updated" / dateModified dates come from content_date.py (CONTENT_UPDATED). Bump it only
when content meaningfully changes — do not stamp build dates on unchanged pages.

## Deploy
    vercel --prod
    python3 indexnow_submit.py   # after deploy

Domain: acnesafecheck.com
