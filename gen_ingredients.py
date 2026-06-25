#!/usr/bin/env python3
"""Generate /ingredient/<slug>.html for every ingredient in db.json."""
import json, os, html, datetime

DB = json.load(open("db.json", encoding="utf-8"))
os.makedirs("ingredient", exist_ok=True)

VER = '29b2213b058b3dbbe63b2ad069034fd4e718ab8b42f4f8d54431f17296323eb9'
ANALYTICS = 'dTgyD+bV2xvop4os/0GghQ'
PUBLISHED = "2026-06-18"
MODIFIED = datetime.date.today().isoformat()
SAFE_FALLBACK = ["Squalane","Glycerin","Niacinamide","Hyaluronic Acid","Hemp Seed Oil"]
by_name = {e["n"]: e for e in DB}
# category -> low-risk members
cat_safe = {}
for e in DB:
    if e["r"] <= 1:
        cat_safe.setdefault(e["c"], []).append(e)

def verdict(r):
    if r >= 4: return "high pore-clogging risk"
    if r == 3: return "moderate pore-clogging risk"
    if r == 2: return "a mild, low pore-clogging risk"
    if r == 1: return "a very low pore-clogging risk"
    return "non-comedogenic (acne safe)"

def risk_long(name, r):
    if r >= 4:
        return (f"{name} sits high on the comedogenic scale. For acne-prone or breakout-prone skin it is one of the "
                f"ingredients most likely to block pores and contribute to blackheads, whiteheads and pimples, "
                f"especially when it appears near the top of an ingredient list (higher concentration).")
    if r == 3:
        return (f"{name} has a moderate chance of clogging pores. Plenty of people tolerate it, but if you break out "
                f"easily it is worth watching — particularly if it is one of the first few ingredients listed.")
    if r == 2:
        return (f"{name} carries only a mild pore-clogging risk. It is fine for most skin types; very reactive or "
                f"acne-prone skin may still want to patch test a new product that contains it.")
    if r == 1:
        return f"{name} has a very low likelihood of clogging pores and is generally considered safe for acne-prone skin."
    return f"{name} is considered non-comedogenic — it is not known to clog pores and is generally a safe choice for acne-prone skin."

def pill(r):
    if r >= 3: return f'<span class="pill bad">Clogging risk · {r}/5</span>'
    if r >= 1: return f'<span class="pill low">Low risk · {r}/5</span>'
    return '<span class="pill safe">Acne safe · 0/5</span>'

def cat_blurb(c):
    return {
        "Oil":"a plant or carrier oil used to moisturise and condition skin",
        "Butter":"a rich, occlusive butter used to soften and moisturise",
        "Ester":"an emollient ester that gives products a smooth, silky feel",
        "Fatty acid":"a fatty acid used as an emollient or thickener",
        "Fatty alcohol":"a fatty alcohol used to soften skin and thicken formulas",
        "Emulsifier":"an emulsifier that keeps oil and water mixed in a formula",
        "Surfactant":"a cleansing/foaming agent",
        "Marine":"a marine-derived (algae/seaweed) extract",
        "Thickener":"a thickener that controls a product's texture",
        "Wax":"a wax used to give structure to balms and sticks",
        "Occlusive":"an occlusive that forms a barrier to lock in moisture",
        "Colorant":"a cosmetic colorant/dye",
        "Sunscreen":"a UV filter used in sunscreens",
        "Silicone":"a silicone that gives a smooth, blurring finish",
        "Humectant":"a humectant that draws water into the skin",
        "Soothing":"a soothing, skin-calming ingredient",
        "Active":"an active ingredient with a targeted skincare benefit",
        "Essential oil":"an aromatic essential oil",
        "Fragrance":"a fragrance ingredient",
        "Botanical extract":"a botanical (plant) extract",
        "Functional":"a functional ingredient (e.g. preservative, pH adjuster, texture)",
        "Clay":"a clay used to absorb oil and purify",
        "Mineral":"a mineral ingredient",
        "Solvent":"a solvent/base","Misc":"a cosmetic ingredient",
    }.get(c, "a cosmetic ingredient")

def found_in(c):
    """Honest, category-level note on where an ingredient typically shows up."""
    return {
        "Oil":"facial oils, cleansing oils, balms, lip products and richer moisturisers",
        "Butter":"body butters, lip balms, rich creams and bar cleansers",
        "Ester":"foundations, primers, sunscreens, lotions and anything with a light, silky slip",
        "Fatty acid":"creams, cleansers and emulsions, where it works as an emollient or thickener",
        "Fatty alcohol":"creams, conditioners and lotions, where it softens skin and thickens the formula",
        "Emulsifier":"creams, lotions and any product that blends oil and water",
        "Surfactant":"cleansers, face washes and shampoos",
        "Marine":"hydrating serums, masks and 'marine' or 'algae' branded products",
        "Thickener":"gels, serums, masks and lotions, where it controls texture",
        "Wax":"balms, sticks, mascaras and solid formats",
        "Occlusive":"barrier balms, ointments and heavy night creams",
        "Colorant":"makeup, tinted products and coloured cosmetics",
        "Sunscreen":"sunscreens and SPF moisturisers and makeup",
        "Silicone":"primers, foundations, serums and 'smoothing' or 'blurring' products",
        "Humectant":"serums, essences, toners and lightweight moisturisers",
        "Soothing":"calming serums, masks and products for sensitive skin",
        "Active":"treatment serums and targeted skincare",
        "Essential oil":"natural and 'aromatherapy' branded products and fragranced skincare",
        "Fragrance":"scented skincare, makeup and bath products",
        "Botanical extract":"'natural' and plant-based serums, creams, toners and masks",
        "Functional":"almost any formula, as a preservative, pH adjuster or texture agent",
        "Clay":"masks, cleansers and oil-absorbing treatments",
        "Mineral":"makeup, sunscreens and powders",
        "Solvent":"toners, essences and water- or alcohol-based products",
        "Misc":"a range of cosmetic formulas",
    }.get(c, "a range of skincare and makeup products")

def alternatives(e):
    """Lower-risk, same-category options. The window rotates per-ingredient so
    different pages in a large category surface different (not identical) picks."""
    pool = sorted([x for x in cat_safe.get(e["c"], []) if x["n"] != e["n"]],
                  key=lambda x: (x["r"], x["n"]))
    if len(pool) > 5:
        # deterministic rotation seeded by slug, so each page differs but is stable
        seed = sum(ord(ch) for ch in e["s"])
        start = seed % len(pool)
        pool = [pool[(start + i) % len(pool)] for i in range(5)]
    else:
        pool = pool[:5]
    if len(pool) < 3:
        extra = [by_name[n] for n in SAFE_FALLBACK if n in by_name and n != e["n"] and by_name[n] not in pool]
        pool = (pool + extra)[:5]
    return pool

def scale_svg(r):
    """Inline SVG 0–5 comedogenicity scale with the current rating marked.
    Lightweight, themed, and gives AI/image processing a visual data point."""
    colors = ["#1faa59","#7bbf4e","#e0a020","#e08020","#e0654f","#d9402a"]
    cells = []
    for i in range(6):
        fill = colors[i] if i == r else "#eee"
        txt = "#fff" if i == r else "#999"
        weight = "700" if i == r else "400"
        cells.append(
            f'<rect x="{i*46+1}" y="1" width="44" height="30" rx="5" fill="{fill}"/>'
            f'<text x="{i*46+23}" y="21" text-anchor="middle" font-family="Arial,sans-serif" '
            f'font-size="14" font-weight="{weight}" fill="{txt}">{i}</text>')
    return (f'<svg viewBox="0 0 277 32" role="img" aria-label="Comedogenicity rating {r} out of 5" '
            f'style="max-width:280px;width:100%;height:auto;margin:6px 0 2px">{"".join(cells)}</svg>')

TPL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Is {name_h} Comedogenic? Pore-Clogging Rating {r}/5 | AcneSafeCheck</title>
<meta name="description" content="{name_h} has a comedogenicity rating of {r}/5 — {verdict}. See whether {name_h} clogs pores, what it is, and acne-safe alternatives.">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#e0654f">
<meta name="ahrefs-site-verification" content="{ver}">
<script src="https://analytics.ahrefs.com/analytics.js" data-key="{an}" async></script>
<link rel="canonical" href="https://acnesafecheck.com/ingredient/{slug}.html">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta property="og:title" content="Is {name_h} Comedogenic? Rating {r}/5">
<meta property="og:description" content="{name_h}: comedogenicity {r}/5 — {verdict}. Find acne-safe alternatives.">
<meta property="og:type" content="article">
<meta property="og:url" content="https://acnesafecheck.com/ingredient/{slug}.html">
<meta property="og:image" content="https://acnesafecheck.com/og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://acnesafecheck.com/og.png">
<link rel="stylesheet" href="/styles.css">
<script type="application/ld+json">
{{"@context":"https://schema.org","@graph":[
{{"@type":"Article","@id":"https://acnesafecheck.com/ingredient/{slug}.html#article","headline":"Is {name_j} Comedogenic? Pore-Clogging Rating {r}/5","description":"{name_j} has a comedogenicity rating of {r}/5 — {verdict}.","url":"https://acnesafecheck.com/ingredient/{slug}.html","datePublished":"{pub}","dateModified":"{mod}","inLanguage":"en","author":{{"@type":"Person","@id":"https://acnesafecheck.com/#mitchell","name":"Mitchell Zandwijken","url":"https://acnesafecheck.com/about.html"}},"publisher":{{"@type":"Organization","@id":"https://acnesafecheck.com/#org","name":"AcneSafeCheck","logo":{{"@type":"ImageObject","url":"https://acnesafecheck.com/icon-512.png"}}}},"image":{{"@type":"ImageObject","url":"https://acnesafecheck.com/og.png","width":1200,"height":630}},"mainEntityOfPage":{{"@type":"WebPage","@id":"https://acnesafecheck.com/ingredient/{slug}.html"}},"about":{{"@type":"Thing","name":"{name_j}"{also}}},"additionalProperty":{{"@type":"PropertyValue","name":"Comedogenicity rating","value":"{r}","minValue":"0","maxValue":"5","description":"0 = non-comedogenic (won't clog pores), 5 = highly pore-clogging"}},"citation":[{{"@type":"CreativeWork","name":"Comedogenicity of current therapeutic products, cosmetics, and ingredients in the rabbit ear (Fulton JE Jr, Pay SR, Fulton JE III, 1984)","url":"https://pubmed.ncbi.nlm.nih.gov/6229554/"}},{{"@type":"CreativeWork","name":"A re-evaluation of the comedogenicity concept (Draelos ZD, DiNardo JC, 2006)","url":"https://pubmed.ncbi.nlm.nih.gov/16488305/"}}]}},
{{"@type":"FAQPage","@id":"https://acnesafecheck.com/ingredient/{slug}.html#faq","mainEntity":[
{{"@type":"Question","name":"Is {name_j} comedogenic?","acceptedAnswer":{{"@type":"Answer","text":"{name_j} has a comedogenicity rating of {r} out of 5, which is {verdict}. {answer_j}"}}}},
{{"@type":"Question","name":"Does {name_j} clog pores?","acceptedAnswer":{{"@type":"Answer","text":"{clog_j}"}}}},
{{"@type":"Question","name":"Is {name_j} safe for fungal acne (Malassezia)?","acceptedAnswer":{{"@type":"Answer","text":"{fa_j}"}}}}]}},
{{"@type":"BreadcrumbList","itemListElement":[
{{"@type":"ListItem","position":1,"name":"Home","item":"https://acnesafecheck.com/"}},
{{"@type":"ListItem","position":2,"name":"Ingredient list","item":"https://acnesafecheck.com/comedogenic-ingredients-list.html"}},
{{"@type":"ListItem","position":3,"name":"{name_j}","item":"https://acnesafecheck.com/ingredient/{slug}.html"}}]}}]}}
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
  <p class="muted" style="font-size:13px;margin:14px 0 0"><a href="/comedogenic-ingredients-list.html">Ingredient list</a> › {name_h}</p>
  <section class="hero" style="padding-top:18px">
    <h1>Is {name_h} comedogenic?</h1>
    <p><strong>Quick answer:</strong> {name_h} has a comedogenicity rating of <strong>{r}/5</strong> — {verdict}. {fa_short}</p>
  </section>

  <section class="card">
    <div class="score {cls}">
      <div class="big">{r}<span style="font-size:18px">/5</span></div>
      <div><div class="lbl"><strong>{verdict_cap}</strong></div>
      <div class="muted" style="font-size:13px">Comedogenicity scale: 0 = won't clog pores, 5 = very likely to clog pores.</div></div>
    </div>
    {scale}
    <p>{risk_long}</p>
    <p style="margin-top:14px"><a class="btn-primary" style="display:inline-block;text-decoration:none" href="/comedogenic-ingredient-checker.html">Check a full ingredient list →</a></p>
  </section>

  <section class="prose">
    <h2>What is {name_h}?</h2>
    <p>{name_h} is {catblurb}.{alias_sentence} You'll most often see it in {found_in}.</p>
    <p><strong>Fungal-acne (Malassezia) safe?</strong> {fa_text} <a href="/fungal-acne-safe-checker.html">Check a whole product for fungal-acne triggers →</a></p>
    <h2>Does {name_h} clog pores?</h2>
    <p>{clog_para} Remember that where an ingredient sits in the list matters: {name_h} near the top means a higher concentration and more impact than the same ingredient near the end.</p>
    <h2>{alt_heading}</h2>
    <p>{alt_intro}</p>
    {alt_list}
    <h2>How we rate comedogenicity — and its limits</h2>
    <p>The 0–5 comedogenicity scale comes from dermatology research that measured how much individual ingredients clogged pores, originally using the rabbit-ear assay (Fulton et al., 1984). A rating reflects an ingredient's <em>potential</em> to clog pores at high concentration — not a guarantee that any finished product will break you out.</p>
    <p>That distinction matters. A later review (Draelos &amp; DiNardo, 2006) found that a single ingredient's comedogenic score does not reliably predict how a complete formula behaves on real skin: concentration, the rest of the formula, and your own skin all change the result. So read {name_h}'s {r}/5 as a risk signal — most useful when the ingredient sits near the top of the list — rather than a verdict on one specific product.</p>
    <p>AcneSafeCheck compiles published comedogenicity ratings and dermatology references into one searchable database. It is educational, not a lab test of your specific product, and not medical advice.</p>
    <h2>References</h2>
    <ol class="refs" style="font-size:14px;line-height:1.65;padding-left:20px">
      <li>Fulton JE Jr, Pay SR, Fulton JE III. Comedogenicity of current therapeutic products, cosmetics, and ingredients in the rabbit ear. <em>J Am Acad Dermatol.</em> 1984;10(1):96–105. <a href="https://pubmed.ncbi.nlm.nih.gov/6229554/" rel="nofollow noopener" target="_blank">PubMed</a></li>
      <li>Draelos ZD, DiNardo JC. A re-evaluation of the comedogenicity concept. <em>J Am Acad Dermatol.</em> 2006;54(3):507–512. <a href="https://pubmed.ncbi.nlm.nih.gov/16488305/" rel="nofollow noopener" target="_blank">PubMed</a></li>
      <li>American Academy of Dermatology. Acne: causes, treatment and skin-care guidance. <a href="https://www.aad.org/public/diseases/acne" rel="nofollow noopener" target="_blank">aad.org</a></li>
    </ol>
    <p class="muted" style="font-size:13px">By <a href="/about.html">Mitchell Zandwijken</a> · Rated against the published comedogenicity references above · Last updated {mod_human}.</p>
  </section>

  <div class="disclaimer"><strong>Note:</strong> Informational only, not medical advice. Real-world effects depend on concentration, the full formula and your individual skin.</div>
</main>

<footer><div class="wrap">
  AcneSafeCheck · <a href="/comedogenic-ingredients-list.html">Ingredient database</a> · <a href="/ingredients.html">All ingredients</a> · <a href="/comedogenic-ingredient-checker.html">Comedogenic checker</a> · <a href="/about.html">About</a><br>
  Informational only, not medical advice.
</div></footer>
</body>
</html>
"""

def esc(s): return html.escape(s, quote=True)
def jp(s): return s.replace('"', "'")  # JSON-safe (used inside double-quoted JSON strings)

def clog_sentence(name, r):
    if r >= 4: return f"Yes — {name} is one of the higher pore-clogging ingredients (rated {r}/5) and is best avoided in leave-on products if you are acne-prone."
    if r == 3: return f"It can — {name} carries a moderate pore-clogging risk (rated {r}/5), so watch it if you break out easily, especially when it is high on the ingredient list."
    if r == 2: return f"Rarely — {name} has only a mild pore-clogging risk (rated {r}/5) and suits most skin types, though very acne-prone skin may want to patch test."
    if r == 1: return f"Unlikely — {name} has a very low pore-clogging risk (rated {r}/5) and is generally fine for acne-prone skin."
    return f"No — {name} is non-comedogenic (rated 0/5) and is not known to clog pores."

count = 0
for e in DB:
    name = e["n"]; r = e["r"]; slug = e["s"]
    cls = "bad" if r >= 3 else ("warn" if r >= 1 else "ok")
    alts = alternatives(e)
    if r >= 2 and alts:
        alt_heading = f"Acne-safe alternatives to {esc(name)}"
        alt_intro = f"If {esc(name)} breaks you out, these lower-rated {e['c'].lower()} options are far less likely to clog pores:"
    else:
        alt_heading = "Similar acne-safe ingredients"
        alt_intro = f"{esc(name)} is already a low-risk choice. Other acne-safe options you may see alongside it include:"
    if alts:
        alt_list = '<ul>' + ''.join(
            f'<li><a href="/ingredient/{a["s"]}.html">{esc(a["n"])}</a> — {pill(a["r"])}</li>' for a in alts) + '</ul>'
    else:
        alt_list = ''

    # De-tautologised aliases: only mention alternate names that genuinely differ
    real_aliases = [a for a in e["a"] if a.strip().lower() != name.strip().lower()]
    if real_aliases:
        alias_sentence = " On an ingredient label it may also appear as " + ", ".join(esc(a) for a in real_aliases[:6]) + "."
        also_json = ',"alternateName":[' + ",".join('"' + jp(a) + '"' for a in real_aliases[:6]) + ']'
    else:
        alias_sentence = ""
        also_json = ""

    fa = bool(e.get("fa"))
    fa_text = ("No — this is a common Malassezia (fungal acne) trigger, so avoid it if you have fungal acne."
               if fa else "Yes — it is not on common Malassezia (fungal acne) trigger lists.")
    fa_short = ("It is also a common fungal-acne (Malassezia) trigger." if fa
                else "It is not a common fungal-acne trigger.")
    fa_answer = ("No — " + name + " appears on common Malassezia (fungal acne) trigger lists, so people with fungal acne usually avoid it."
                 if fa else "Yes — " + name + " is not on common Malassezia (fungal acne) trigger lists and is generally considered fungal-acne safe.")

    clog_para = clog_sentence(name, r)

    page = TPL.format(
        name_h=esc(name), name_j=jp(name), slug=slug, r=r,
        verdict=verdict(r), verdict_cap=verdict(r).capitalize(),
        risk_long=esc(risk_long(name, r)), answer_j=jp(risk_long(name, r)),
        clog_para=esc(clog_para), clog_j=jp(clog_para),
        catblurb=cat_blurb(e["c"]), found_in=found_in(e["c"]),
        alias_sentence=alias_sentence, also=also_json, cls=cls,
        scale=scale_svg(r),
        alt_heading=alt_heading, alt_intro=alt_intro, alt_list=alt_list,
        fa_text=fa_text, fa_short=fa_short, fa_j=jp(fa_answer),
        pub=PUBLISHED, mod=MODIFIED, mod_human=datetime.date.today().strftime("%B %Y"),
        ver=VER, an=ANALYTICS)
    open(f"ingredient/{slug}.html", "w", encoding="utf-8").write(page)
    count += 1
print("Generated", count, "ingredient pages")
