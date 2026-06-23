#!/usr/bin/env python3
"""Generate /non-comedogenic/<slug>.html affiliate roundup pages."""
import os, html, json, datetime
from urllib.parse import quote_plus

os.makedirs("non-comedogenic", exist_ok=True)
VER = '29b2213b058b3dbbe63b2ad069034fd4e718ab8b42f4f8d54431f17296323eb9'
AN = 'dTgyD+bV2xvop4os/0GghQ'
PUBLISHED = "2026-06-18"
MODIFIED = datetime.date.today().isoformat()
MOD_HUMAN = datetime.date.today().strftime("%B %Y")
AMZ_TAG = "acnesafecheck-20"   # TODO: replace with the real Amazon Associates tag once approved

def amz(q):
    return f"https://www.amazon.com/s?k={quote_plus(q)}&tag={AMZ_TAG}"

# Each: slug, type label, H1, vol-intent intro, secondary terms, avoid list, lookfor list, picks[(name, blurb, query)]
PAGES = [
 ("non-comedogenic-moisturizer","moisturizer","Best Non-Comedogenic Moisturizers for Acne-Prone Skin",
  "A good non-comedogenic moisturizer hydrates without clogging pores. We focus on lightweight, fragrance-free formulas built around acne-safe humectants and ceramides — and avoid the heavy oils and esters that trigger breakouts.",
  ["non comedogenic face moisturizer","best non comedogenic moisturizer"],
  ["Isopropyl Myristate","Coconut Oil","Cocoa Butter","Algae Extract"],
  ["Hyaluronic Acid","Glycerin","Niacinamide","Squalane","Dimethicone"],
  [("CeraVe Moisturizing Lotion","Fragrance-free, with ceramides + hyaluronic acid; lightweight and widely recommended for acne-prone skin.","CeraVe daily moisturizing lotion"),
   ("La Roche-Posay Toleriane Double Repair","Ceramide + niacinamide formula, fragrance-free, oil-free finish.","La Roche-Posay Toleriane Double Repair moisturizer"),
   ("Neutrogena Hydro Boost Gel-Cream","Hyaluronic-acid gel, oil-free, very light layer of hydration.","Neutrogena Hydro Boost gel cream fragrance free"),
   ("Vanicream Daily Facial Moisturizer","Free of fragrance, dyes and common irritants; squalane + hyaluronic acid.","Vanicream daily facial moisturizer"),
   ("The Ordinary Natural Moisturizing Factors + HA","Budget pick built on glycerin and amino acids; no fragrance.","The Ordinary natural moisturizing factors HA")]),

 ("non-comedogenic-sunscreen","sunscreen","Best Non-Comedogenic Sunscreens That Won't Clog Pores",
  "Sunscreen is non-negotiable for acne-prone skin, but many formulas break people out. We look for lightweight, oil-free filters and avoid the heavy esters that clog pores.",
  ["best non comedogenic sunscreen","oil free sunscreen for acne"],
  ["Octyl Palmitate","Isopropyl Myristate","Coconut Oil"],
  ["Zinc Oxide","Titanium Dioxide","Niacinamide"],
  [("EltaMD UV Clear SPF 46","Zinc-oxide + niacinamide, oil-free, fragrance-free; a dermatologist favourite for acne-prone skin.","EltaMD UV Clear SPF 46"),
   ("La Roche-Posay Anthelios Clear Skin SPF 60","Mattifying, oil-free formula aimed at oily/acne-prone skin.","La Roche-Posay Anthelios Clear Skin SPF 60"),
   ("Neutrogena Clear Face SPF 50","Oil-free and light, designed not to cause breakouts.","Neutrogena Clear Face sunscreen SPF 50"),
   ("Biore UV Aqua Rich SPF 50+","Very lightweight Japanese gel sunscreen popular for oily skin.","Biore UV Aqua Rich Watery Essence SPF50"),
   ("Black Girl Sunscreen SPF 30","No white cast and lightweight; a popular pick for medium-to-deep skin tones.","Black Girl Sunscreen SPF 30")]),

 ("non-comedogenic-cleanser","cleanser","Best Non-Comedogenic Cleansers &amp; Face Washes for Acne",
  "A non-comedogenic cleanser removes oil and makeup without leaving pore-clogging residue. We prefer gentle gel and foaming face washes that don't strip the skin.",
  ["non comedogenic face wash","gentle cleanser for acne"],
  ["Sodium Lauryl Sulfate","Isopropyl Myristate"],
  ["Glycerin","Niacinamide","Salicylic Acid"],
  [("CeraVe Foaming Facial Cleanser","Gel-to-foam, fragrance-free, with niacinamide and ceramides; great for oily/acne-prone skin.","CeraVe foaming facial cleanser"),
   ("La Roche-Posay Toleriane Purifying Cleanser","Gentle gel cleanser, fragrance-free, suitable for sensitive acne-prone skin.","La Roche-Posay Toleriane purifying foaming cleanser"),
   ("Vanicream Gentle Facial Cleanser","No fragrance, dyes or sulfates; very low irritation.","Vanicream gentle facial cleanser"),
   ("CeraVe SA Smoothing Cleanser","Contains salicylic acid for clogged pores and texture.","CeraVe SA smoothing cleanser salicylic acid"),
   ("Cetaphil Gentle Skin Cleanser","Classic low-irritation cleanser for sensitive skin.","Cetaphil gentle skin cleanser")]),

 ("non-comedogenic-foundation","foundation","Best Non-Comedogenic Foundations for Acne-Prone Skin",
  "Foundation is a common hidden cause of breakouts because of heavy pigments and esters. We look for oil-free, non-comedogenic formulas that wear well on acne-prone skin.",
  ["oil free foundation for acne","foundation that won't clog pores"],
  ["Isopropyl Myristate","Myristyl Myristate","Octyl Palmitate"],
  ["Dimethicone","Silica","Niacinamide"],
  [("Clinique Acne Solutions Liquid Makeup","Built for acne-prone skin with salicylic acid; oil-free.","Clinique Acne Solutions liquid makeup"),
   ("Estée Lauder Double Wear","Long-wear, oil-free; popular with oily/acne-prone skin (patch test).","Estee Lauder Double Wear foundation"),
   ("bareMinerals Original Loose Powder","Mineral makeup, minimal ingredients, no added fragrance.","bareMinerals Original loose powder foundation"),
   ("Neutrogena SkinClearing Foundation","Contains salicylic acid; oil-free, aimed at breakout-prone skin.","Neutrogena SkinClearing liquid makeup"),
   ("La Roche-Posay Toleriane Teint","Dermatologist line, fragrance-free options for sensitive skin.","La Roche-Posay Toleriane Teint foundation")]),

 ("non-comedogenic-concealer","concealer","Best Non-Comedogenic Concealers That Won't Cause Breakouts",
  "Concealer sits on the exact spots you're trying to clear, so a non-comedogenic, oil-free formula matters even more than with foundation.",
  ["oil free concealer for acne","concealer for acne prone skin"],
  ["Isopropyl Myristate","Octyl Palmitate"],
  ["Dimethicone","Salicylic Acid","Niacinamide"],
  [("Clinique Acne Solutions Concealer","Targeted at blemishes with salicylic acid.","Clinique Acne Solutions concealer"),
   ("Tarte Shape Tape (matte)","High-coverage; choose the matte/oil-free version and patch test.","Tarte Shape Tape concealer matte"),
   ("NYX Can't Stop Won't Stop Concealer","Affordable, long-wear, oil-free.","NYX Cant Stop Wont Stop concealer"),
   ("La Roche-Posay Toleriane Concealer","Fragrance-free, sensitive-skin friendly.","La Roche-Posay Toleriane concealer"),
   ("Dermablend Cover Care Concealer","Full coverage, fragrance-free, dermatologist-developed.","Dermablend Cover Care concealer")]),

 ("non-comedogenic-primer","primer","Best Non-Comedogenic Primers for Acne-Prone Skin",
  "A non-comedogenic primer smooths skin and helps makeup last without clogging pores. Silicone-based mattifying primers usually suit oily, acne-prone skin best.",
  ["oil free primer","mattifying primer for acne"],
  ["Isopropyl Myristate"],
  ["Dimethicone","Silica","Niacinamide"],
  [("The Ordinary High-Adherence Silicone Primer","Lightweight silicone base, no fragrance, very affordable.","The Ordinary high adherence silicone primer"),
   ("e.l.f. Power Grip Primer","Gripping gel primer, fragrance-free, budget pick.","elf Power Grip primer"),
   ("Smashbox Photo Finish Pore Minimizing","Silicone primer that blurs pores; check for sensitivities.","Smashbox Photo Finish pore minimizing primer"),
   ("Paula's Choice Pore-Reducing Primer","Mattifying, fragrance-free, from a non-comedogenic-focused brand.","Paulas Choice pore reducing primer"),
   ("NYX Pore Filler Primer","Affordable pore-blurring primer.","NYX pore filler primer")]),

 ("non-comedogenic-oils","oils","Non-Comedogenic Oils: Which Face Oils Are Safe for Acne?",
  "Not all face oils clog pores. Some sit low on the comedogenic scale and can suit acne-prone skin. Here are the safest oils and the ones to avoid.",
  ["best oils for acne prone skin","face oil for acne"],
  ["Coconut Oil","Wheat Germ Oil","Flaxseed Oil","Cocoa Butter"],
  ["Hemp Seed Oil","Argan Oil","Squalane","Rosehip Oil","Sunflower Oil"],
  [("The Ordinary 100% Plant-Derived Squalane","Squalane (rating 1) — lightweight, one of the most acne-safe oils.","The Ordinary squalane oil"),
   ("Nutiva Organic Hemp Seed Oil","Hemp seed oil (rating 0) — high in linoleic acid, very acne-safe.","organic hemp seed oil cold pressed"),
   ("Kosas Argan Oil / pure argan oil","Argan oil (rating 0) — nourishing and non-comedogenic.","100% pure argan oil"),
   ("The Ordinary 100% Organic Cold-Pressed Rose Hip Seed Oil","Rosehip oil (rating 1) — good for scarring and tone.","The Ordinary rosehip seed oil"),
   ("Pai Sunflower & Sea Buckthorn / sunflower oil","Sunflower oil (rating 0) — light and high in linoleic acid.","cold pressed sunflower seed oil skincare")]),

 ("non-comedogenic-hair-products","hair products","Non-Comedogenic Hair Products to Stop Hairline &amp; Back Acne",
  "Hair products are a common cause of forehead, hairline and back breakouts (often fungal too). Non-comedogenic, sulfate-light shampoos and conditioners help.",
  ["non comedogenic shampoo","hair products for acne"],
  ["Coconut Oil","Isopropyl Myristate","Lauric Acid"],
  ["Glycerin","Niacinamide","Salicylic Acid"],
  [("Vanicream Free & Clear Shampoo","Free of fragrance, sulfates and common pore-cloggers.","Vanicream Free and Clear shampoo"),
   ("Neutrogena T/Sal Shampoo","Salicylic-acid shampoo helpful for scalp build-up.","Neutrogena T Sal shampoo salicylic acid"),
   ("Nizoral Anti-Dandruff Shampoo","Ketoconazole — useful when fungal acne is involved.","Nizoral anti dandruff shampoo ketoconazole"),
   ("Free & Clear Conditioner","Low-irritant conditioner that rinses clean.","Free and Clear conditioner"),
   ("The Inkey List Salicylic Acid Scalp Treatment","Targets scalp build-up that can clog the hairline.","The Inkey List salicylic acid scalp treatment")]),
]

def pill_safe(): return '<span class="pill safe">Acne safe</span>'
def pill_bad(): return '<span class="pill bad">Avoid</span>'

def slug_for_ing(n):
    import re
    return re.sub(r'[^a-z0-9]+','-',n.lower()).strip('-')

NEWSLETTER = """
  <section class="card" style="background:#fff7f4;border-color:#f3d8cf">
    <h2 style="margin-top:0">Get the acne-safe product cheat sheet</h2>
    <p class="muted">Join the free newsletter for vetted non-comedogenic picks and new ingredient guides. No spam.</p>
    <form class="row" onsubmit="return acsSubscribe(event)">
      <input class="search" style="flex:1;min-width:220px" type="email" name="email" placeholder="you@email.com" required>
      <button class="btn-primary" type="submit">Subscribe</button>
    </form>
    <p id="acsMsg" class="muted" style="font-size:13px;margin:8px 0 0"></p>
  </section>
  <script>
  function acsSubscribe(e){e.preventDefault();var f=e.target,email=f.email.value,m=document.getElementById('acsMsg');m.textContent="Subscribing…";
    fetch("/api/subscribe",{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email:email,list:'newsletter'})})
      .then(r=>r.json()).then(d=>{
        if(d.ok){m.textContent="You're in — thanks for subscribing!";f.reset();}
        else if(d.configured===false){m.textContent="Thanks! You'll be added as soon as the newsletter goes live.";f.reset();}
        else{m.textContent="Hmm, that didn't work — please try again.";}})
      .catch(()=>{m.textContent="Something went wrong, please try again.";});
    return false;}
  </script>
"""

TPL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{h1_plain} | AcneSafeCheck</title>
<meta name="description" content="{desc}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#e0654f">
<meta name="ahrefs-site-verification" content="{ver}">
<script src="https://analytics.ahrefs.com/analytics.js" data-key="{an}" async></script>
<link rel="canonical" href="https://acnesafecheck.com/non-comedogenic/{slug}.html">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta property="og:title" content="{h1_plain}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="article">
<meta property="og:url" content="https://acnesafecheck.com/non-comedogenic/{slug}.html">
<meta property="og:image" content="https://acnesafecheck.com/og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://acnesafecheck.com/og.png">
<link rel="stylesheet" href="/styles.css">
{jsonld}
</head>
<body>
<header><div class="wrap bar">
  <a class="logo" href="/"><span class="dot"></span> AcneSafeCheck</a>
  <nav>
    <a href="/comedogenic-ingredient-checker.html">Comedogenic checker</a>
    <a href="/pore-clogging-ingredient-checker.html">Pore-clogging</a>
    <a href="/comedogenic-ingredients-list.html">Ingredient list</a>
    <a href="/about.html">About</a>
  </nav>
</div></header>

<main class="wrap">
  <section class="hero">
    <h1>{h1}</h1>
    <p>{intro}</p>
  </section>

  <div class="disclaimer" style="margin-top:0"><strong>How we choose:</strong> picks are screened against our comedogenic database for pore-clogging ingredients. Some links are affiliate links — if you buy through them we may earn a small commission at no extra cost to you. Always check the current ingredient list, since formulas change. Informational only, not medical advice.</div>

  <section class="prose">
    <h2>What to look for</h2>
    <p>Acne-safe {type} formulas tend to be built around low-comedogenic ingredients such as {lookfor}. Use our <a href="/comedogenic-ingredient-checker.html">comedogenic ingredient checker</a> to paste any product's list and confirm before you buy.</p>
    <h2>Ingredients to avoid</h2>
    <p>Be cautious with higher-rated pore-cloggers like {avoid}. One of these near the top of the ingredient list is a red flag for breakout-prone skin.</p>
  </section>

  <h2>Top non-comedogenic {type} picks</h2>
  {picks}

  {newsletter}

  <section class="prose">
    <h2>FAQ</h2>
    <h3>Does "non-comedogenic" actually mean anything?</h3>
    <p>It usually means rated 0 on the comedogenic scale, but it isn't a regulated term — a product can be labelled non-comedogenic and still contain a pore-clogger. That's why we check the real ingredient list. Learn more on <a href="/comedogenic.html">what comedogenic means</a>.</p>
    <h3>How do I check a product myself?</h3>
    <p>Paste the ingredient list into our <a href="/comedogenic-ingredient-checker.html">checker</a> — it flags every pore-clogging ingredient and ranks it 0–5.</p>
  </section>
</main>

<footer><div class="wrap">
  AcneSafeCheck · <a href="/comedogenic-ingredients-list.html">Ingredient database</a> · <a href="/comedogenic-ingredient-checker.html">Comedogenic checker</a> · <a href="/about.html">About</a><br>
  Affiliate links help keep AcneSafeCheck free. Informational only, not medical advice.
</div></footer>
</body>
</html>
"""

def esc(s): return html.escape(s, quote=True)

def build_jsonld(slug, typ, h1_plain, intro, picks):
    url = f"https://acnesafecheck.com/non-comedogenic/{slug}.html"
    graph = [
        {"@type": "Article", "@id": url + "#article",
         "headline": h1_plain,
         "description": html.unescape(intro)[:200],
         "url": url, "datePublished": PUBLISHED, "dateModified": MODIFIED,
         "inLanguage": "en",
         "author": {"@type": "Person", "@id": "https://acnesafecheck.com/#mitchell",
                     "name": "Mitchell Zandwijken", "url": "https://acnesafecheck.com/about.html"},
         "publisher": {"@type": "Organization", "@id": "https://acnesafecheck.com/#org",
                       "name": "AcneSafeCheck",
                       "logo": {"@type": "ImageObject", "url": "https://acnesafecheck.com/icon-512.png"}},
         "image": {"@type": "ImageObject", "url": "https://acnesafecheck.com/og.png", "width": 1200, "height": 630},
         "mainEntityOfPage": {"@type": "WebPage", "@id": url}},
        {"@type": "ItemList", "@id": url + "#picks",
         "name": f"Top non-comedogenic {typ} picks",
         "itemListElement": [
             {"@type": "ListItem", "position": i + 1, "name": name, "url": amz(query)}
             for i, (name, blurb, query) in enumerate(picks)]},
        {"@type": "FAQPage", "@id": url + "#faq", "mainEntity": [
            {"@type": "Question", "name": "Does \"non-comedogenic\" actually mean anything?",
             "acceptedAnswer": {"@type": "Answer", "text": "It usually means rated 0 on the comedogenic scale, but it isn't a regulated term — a product can be labelled non-comedogenic and still contain a pore-clogger. That's why we check the real ingredient list."}},
            {"@type": "Question", "name": f"How do I check a {typ} for pore-clogging ingredients?",
             "acceptedAnswer": {"@type": "Answer", "text": "Paste the ingredient list into the AcneSafeCheck comedogenic ingredient checker at https://acnesafecheck.com/comedogenic-ingredient-checker.html — it flags every pore-clogging ingredient and ranks it 0–5 on the comedogenicity scale."}}]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://acnesafecheck.com/"},
            {"@type": "ListItem", "position": 2, "name": typ.capitalize(), "item": url}]},
    ]
    return ('<script type="application/ld+json">\n'
            + json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)
            + '\n</script>')

for slug, typ, h1, intro, secondary, avoid, lookfor, picks in PAGES:
    lookfor_links = ', '.join(f'<a href="/ingredient/{slug_for_ing(x)}.html">{esc(x)}</a>' for x in lookfor)
    avoid_links = ', '.join(f'<a href="/ingredient/{slug_for_ing(x)}.html">{esc(x)}</a>' for x in avoid)
    cards = []
    for name, blurb, query in picks:
        cards.append(
            f'<div class="flag"><div><div class="name">{esc(name)}</div>'
            f'<div class="why">{esc(blurb)}</div>'
            f'<a href="{amz(query)}" rel="nofollow sponsored" target="_blank" style="font-size:13px;font-weight:700">Check price on Amazon →</a></div>'
            f'{pill_safe()}</div>')
    picks_html = '<section class="card">' + ''.join(cards) + '</section>'
    h1_plain = html.unescape(h1).replace('&amp;','&')
    jsonld = build_jsonld(slug, typ, h1_plain, intro, picks)
    page = TPL.format(
        h1=h1, h1_plain=esc(h1_plain), slug=slug, type=typ, type_cap=typ.capitalize(),
        intro=esc(intro), desc=esc(html.unescape(intro)[:155]),
        lookfor=lookfor_links, avoid=avoid_links, picks=picks_html,
        jsonld=jsonld, newsletter=NEWSLETTER, ver=VER, an=AN)
    open(f"non-comedogenic/{slug}.html","w",encoding="utf-8").write(page)
print("Generated", len(PAGES), "roundup pages")
