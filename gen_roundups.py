#!/usr/bin/env python3
"""Generate /non-comedogenic/<slug>.html product roundup pages.

Each pick carries real editorial detail (texture, who it suits, what to
double-check) plus a deep link into the live product checker so readers can
analyze the CURRENT ingredient list — formulas change, static verdicts rot.
"""
import os, html, json, re
from urllib.parse import quote_plus

os.makedirs("non-comedogenic", exist_ok=True)
VER = '29b2213b058b3dbbe63b2ad069034fd4e718ab8b42f4f8d54431f17296323eb9'
AN = 'dTgyD+bV2xvop4os/0GghQ'
from content_date import CONTENT_UPDATED, CONTENT_UPDATED_HUMAN
PUBLISHED = "2026-06-18"
MODIFIED = CONTENT_UPDATED
MOD_HUMAN = CONTENT_UPDATED_HUMAN
# Amazon Associates tag. Leave EMPTY until the Associates account is approved —
# shipping an unregistered tag mis-attributes and breaches Amazon's Operating Agreement.
AMZ_TAG = ""

def amz(q):
    base = f"https://www.amazon.com/s?k={quote_plus(q)}"
    return f"{base}&tag={AMZ_TAG}" if AMZ_TAG else base

def pc_link(name):
    """Deep link into the live product checker (Open Beauty Facts search)."""
    return f"/product-checker.html?q={quote_plus(name)}"

def anchor(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")

# ---------------------------------------------------------------------------
# PAGES: slug, typ, h1, desc (meta), intro, avoid[], lookfor[], picks[]
# pick = (name, blurb, detail, key_ingredients[], amazon query)
# ---------------------------------------------------------------------------
PAGES = [
 dict(slug="non-comedogenic-moisturizer", typ="moisturizer",
  h1="Best Non-Comedogenic Moisturizers for Acne-Prone Skin",
  desc="Non-comedogenic moisturizers for acne-prone skin: fragrance-free ceramide & hyaluronic-acid picks, each screened against our pore-clogging database.",
  intro="A good non-comedogenic moisturizer hydrates without clogging pores. We focus on lightweight, fragrance-free formulas built around acne-safe humectants and ceramides — and avoid the heavy oils and esters that trigger breakouts.",
  avoid=["Isopropyl Myristate","Coconut Oil","Cocoa Butter","Algae Extract"],
  lookfor=["Hyaluronic Acid","Glycerin","Niacinamide","Squalane","Dimethicone"],
  picks=[
   ("CeraVe Moisturizing Lotion",
    "Fragrance-free, with ceramides + hyaluronic acid; lightweight and widely recommended for acne-prone skin.",
    "A thin, fast-absorbing lotion that layers well under sunscreen or makeup without pilling. Suits normal-to-dry acne-prone skin; if you're very oily, the gel texture of Hydro Boost below may feel nicer. It uses cetearyl alcohol (rated 2) as an emulsifier — fine for most, but very reactive skin should patch test.",
    ["Hyaluronic Acid","Cetearyl Alcohol"], "CeraVe daily moisturizing lotion"),
   ("La Roche-Posay Toleriane Double Repair",
    "Ceramide + niacinamide formula, fragrance-free, oil-free finish.",
    "A slightly richer cream than CeraVe's lotion, aimed at barrier repair — a good pick if acne treatments (retinoids, benzoyl peroxide) have left your skin dry and irritated. The niacinamide adds an anti-inflammatory bonus.",
    ["Niacinamide","Glycerin"], "La Roche-Posay Toleriane Double Repair moisturizer"),
   ("Neutrogena Hydro Boost Gel-Cream",
    "Hyaluronic-acid gel, oil-free, very light layer of hydration.",
    "The lightest texture here — a water-gel that disappears into skin, which makes it the usual pick for oily or combination acne-prone skin. Choose the fragrance-free version; the original contains fragrance, which some acne-prone skin doesn't tolerate.",
    ["Hyaluronic Acid","Dimethicone"], "Neutrogena Hydro Boost gel cream fragrance free"),
   ("Vanicream Daily Facial Moisturizer",
    "Free of fragrance, dyes and common irritants; squalane + hyaluronic acid.",
    "The minimal-ingredient pick: Vanicream formulates specifically for reactive skin, so this is the safest starting point if you suspect an ingredient sensitivity but don't know which one. Light lotion texture, no essential oils, no botanical extracts.",
    ["Squalane","Hyaluronic Acid"], "Vanicream daily facial moisturizer"),
   ("The Ordinary Natural Moisturizing Factors + HA",
    "Budget pick built on glycerin and amino acids; no fragrance.",
    "The cheapest way to get a fragrance-free, low-comedogenic moisturizer. It's a classic cream (not a gel) and can feel slightly tacky for a minute after applying — fine under makeup once absorbed.",
    ["Glycerin","Hyaluronic Acid"], "The Ordinary natural moisturizing factors HA")]),

 dict(slug="non-comedogenic-sunscreen", typ="sunscreen",
  h1="Best Non-Comedogenic Sunscreens That Won't Clog Pores",
  desc="Non-comedogenic sunscreens that won't clog pores: oil-free, zinc-oxide and lightweight gel SPF picks, screened against our pore-clogging database.",
  intro="Sunscreen is non-negotiable for acne-prone skin, but many formulas break people out. We look for lightweight, oil-free filters and avoid the heavy esters that clog pores.",
  avoid=["Octyl Palmitate","Isopropyl Myristate","Coconut Oil"],
  lookfor=["Zinc Oxide","Titanium Dioxide","Niacinamide"],
  picks=[
   ("EltaMD UV Clear SPF 46",
    "Zinc-oxide + niacinamide, oil-free, fragrance-free; a dermatologist favourite for acne-prone skin.",
    "The default dermatologist recommendation for acne-prone and rosacea-prone skin. The niacinamide calms redness, and the texture is a light lotion that doesn't leave a heavy film. Pricier than drugstore picks — that's its main downside.",
    ["Zinc Oxide","Niacinamide"], "EltaMD UV Clear SPF 46"),
   ("La Roche-Posay Anthelios Clear Skin SPF 60",
    "Mattifying, oil-free formula aimed at oily/acne-prone skin.",
    "A dry-touch sunscreen that actively absorbs surface oil — the pick if shine is your main complaint. Because it's mattifying it can feel tight on drier skin; pair it with a light moisturizer underneath.",
    ["Silica"], "La Roche-Posay Anthelios Clear Skin SPF 60"),
   ("Neutrogena Clear Face SPF 50",
    "Oil-free and light, designed not to cause breakouts.",
    "The accessible drugstore option — liquid-lotion texture, broad spectrum, easy to rebuy anywhere. It contains fragrance, so very sensitive skin may prefer EltaMD or a mineral option.",
    [], "Neutrogena Clear Face sunscreen SPF 50"),
   ("Biore UV Aqua Rich SPF 50+",
    "Very lightweight Japanese gel sunscreen popular for oily skin.",
    "The famous watery-gel texture makes this the most comfortable daily sunscreen many acne-prone people have tried — it feels like a serum, not an SPF. Check the current ingredient list when buying, as the formula has been revised several times.",
    ["Glycerin"], "Biore UV Aqua Rich Watery Essence SPF50"),
   ("Black Girl Sunscreen SPF 30",
    "No white cast and lightweight; a popular pick for medium-to-deep skin tones.",
    "Built to leave zero white cast on deeper skin tones. Note: it contains some plant butters and oils, so if you're extremely clog-prone, run the current list through the checker and see how your skin responds — for many it wears well.",
    [], "Black Girl Sunscreen SPF 30")]),

 dict(slug="non-comedogenic-cleanser", typ="cleanser",
  h1="Best Non-Comedogenic Cleansers &amp; Face Washes for Acne",
  desc="Gentle non-comedogenic cleansers for acne-prone skin: fragrance-free gel and foaming face washes screened against our pore-clogging ingredient database.",
  intro="A non-comedogenic cleanser removes oil and makeup without leaving pore-clogging residue. We prefer gentle gel and foaming face washes that don't strip the skin.",
  avoid=["Sodium Lauryl Sulfate","Isopropyl Myristate"],
  lookfor=["Glycerin","Niacinamide","Salicylic Acid"],
  picks=[
   ("CeraVe Foaming Facial Cleanser",
    "Gel-to-foam, fragrance-free, with niacinamide and ceramides; great for oily/acne-prone skin.",
    "The standard first recommendation for oily, acne-prone skin: cleans thoroughly without the squeaky-stripped feeling. If your skin is dry or you're on drying acne treatment, CeraVe's Hydrating (non-foaming) version is gentler.",
    ["Niacinamide","Glycerin"], "CeraVe foaming facial cleanser"),
   ("La Roche-Posay Toleriane Purifying Cleanser",
    "Gentle gel cleanser, fragrance-free, suitable for sensitive acne-prone skin.",
    "Slightly gentler than CeraVe Foaming with a similar gel-foam format. A good switch if foaming cleansers usually leave your skin feeling tight.",
    ["Glycerin","Niacinamide"], "La Roche-Posay Toleriane purifying foaming cleanser"),
   ("Vanicream Gentle Facial Cleanser",
    "No fragrance, dyes or sulfates; very low irritation.",
    "The most stripped-back formula here — the pick when you're eliminating variables to find what's breaking you out, or washing twice daily around harsh actives.",
    ["Glycerin"], "Vanicream gentle facial cleanser"),
   ("CeraVe SA Smoothing Cleanser",
    "Contains salicylic acid for clogged pores and texture.",
    "Adds a low dose of salicylic acid (BHA) to dissolve the oil inside pores — useful for blackheads and rough texture. Don't stack it with a separate BHA treatment unless your skin tolerates both.",
    ["Salicylic Acid"], "CeraVe SA smoothing cleanser salicylic acid"),
   ("Cetaphil Gentle Skin Cleanser",
    "Classic low-irritation cleanser for sensitive skin.",
    "The decades-old dermatology staple. It doesn't foam and won't fully remove heavy makeup, but as a gentle morning cleanse or second cleanse it's hard to irritate anyone with it.",
    ["Glycerin"], "Cetaphil gentle skin cleanser")]),

 dict(slug="non-comedogenic-foundation", typ="foundation",
  h1="Best Non-Comedogenic Foundations for Acne-Prone Skin",
  desc="Non-comedogenic foundations for acne-prone skin: oil-free formulas that wear well without clogging pores, each screened for comedogenic ingredients.",
  intro="Foundation is a common hidden cause of breakouts because of heavy pigments and esters. We look for oil-free, non-comedogenic formulas that wear well on acne-prone skin.",
  avoid=["Isopropyl Myristate","Myristyl Myristate","Octyl Palmitate"],
  lookfor=["Dimethicone","Silica","Niacinamide"],
  picks=[
   ("Clinique Acne Solutions Liquid Makeup",
    "Built for acne-prone skin with salicylic acid; oil-free.",
    "One of the few foundations formulated specifically for breakout-prone skin, with a medium-coverage satin finish. The salicylic acid is a token dose — treat it as makeup that won't make things worse, not as treatment.",
    ["Salicylic Acid","Dimethicone"], "Clinique Acne Solutions liquid makeup"),
   ("Estée Lauder Double Wear",
    "Long-wear, oil-free; popular with oily/acne-prone skin (patch test).",
    "The long-wear benchmark: matte, high coverage, survives a full day on oily skin. High-coverage long-wear formulas are also harder to remove — double cleanse at night, or residue can undo the non-comedogenic benefit.",
    ["Dimethicone"], "Estee Lauder Double Wear foundation"),
   ("bareMinerals Original Loose Powder",
    "Mineral makeup, minimal ingredients, no added fragrance.",
    "A five-ingredient mineral powder — the shortest ingredient list in this roundup and the easiest to vet. Coverage is buildable but lighter than liquids; best for mild-to-moderate coverage needs.",
    ["Zinc Oxide","Titanium Dioxide"], "bareMinerals Original loose powder foundation"),
   ("Neutrogena SkinClearing Foundation",
    "Contains salicylic acid; oil-free, aimed at breakout-prone skin.",
    "The budget acne-focused liquid. Shade range and finish are more limited than the premium picks, but it's a safe drugstore default for breakout-prone skin.",
    ["Salicylic Acid"], "Neutrogena SkinClearing liquid makeup"),
   ("La Roche-Posay Toleriane Teint",
    "Dermatologist line, fragrance-free options for sensitive skin.",
    "The sensitive-skin pick: fragrance-free with a natural (not flat-matte) finish. Good when your skin is both reactive and breakout-prone and most makeup stings.",
    ["Glycerin"], "La Roche-Posay Toleriane Teint foundation")]),

 dict(slug="non-comedogenic-concealer", typ="concealer",
  h1="Best Non-Comedogenic Concealers That Won't Cause Breakouts",
  desc="Non-comedogenic concealers that won't cause breakouts: oil-free, blemish-friendly picks screened against our pore-clogging ingredient database.",
  intro="Concealer sits on the exact spots you're trying to clear, so a non-comedogenic, oil-free formula matters even more than with foundation.",
  avoid=["Isopropyl Myristate","Octyl Palmitate"],
  lookfor=["Dimethicone","Salicylic Acid","Niacinamide"],
  picks=[
   ("Clinique Acne Solutions Concealer",
    "Targeted at blemishes with salicylic acid.",
    "Made for the exact use case: covering an active blemish without feeding it. Coverage is moderate — enough for redness, not for deep discoloration.",
    ["Salicylic Acid"], "Clinique Acne Solutions concealer"),
   ("Tarte Shape Tape (matte)",
    "High-coverage; choose the matte/oil-free version and patch test.",
    "The high-coverage favourite. It's thick, so use a thin layer and remove thoroughly at night — buildup, not the formula itself, is what tends to cause problems.",
    ["Dimethicone"], "Tarte Shape Tape concealer matte"),
   ("NYX Can't Stop Won't Stop Concealer",
    "Affordable, long-wear, oil-free.",
    "Budget long-wear pick with a matte finish and wide shade range. A good first concealer to test whether liquid concealers agree with your skin at all.",
    ["Dimethicone"], "NYX Cant Stop Wont Stop concealer"),
   ("La Roche-Posay Toleriane Concealer",
    "Fragrance-free, sensitive-skin friendly.",
    "The low-irritation option from a dermatology-adjacent line — natural finish, kind to skin that reacts to most makeup.",
    ["Glycerin"], "La Roche-Posay Toleriane concealer"),
   ("Dermablend Cover Care Concealer",
    "Full coverage, fragrance-free, dermatologist-developed.",
    "Built for covering serious discoloration (post-acne marks, scarring) with a fragrance-free formula. Full coverage means thorough removal matters — double cleanse.",
    ["Dimethicone"], "Dermablend Cover Care concealer")]),

 dict(slug="non-comedogenic-primer", typ="primer",
  h1="Best Non-Comedogenic Primers for Acne-Prone Skin",
  desc="Non-comedogenic primers for oily, acne-prone skin: mattifying, fragrance-free picks screened for pore-clogging ingredients.",
  intro="A non-comedogenic primer smooths skin and helps makeup last without clogging pores. Silicone-based mattifying primers usually suit oily, acne-prone skin best.",
  avoid=["Isopropyl Myristate"],
  lookfor=["Dimethicone","Silica","Niacinamide"],
  picks=[
   ("The Ordinary High-Adherence Silicone Primer",
    "Lightweight silicone base, no fragrance, very affordable.",
    "A simple, cheap silicone primer that blurs and grips makeup. Silicones like dimethicone are large molecules that sit on top of skin — despite their reputation, they rate low on the comedogenic scale.",
    ["Dimethicone"], "The Ordinary high adherence silicone primer"),
   ("e.l.f. Power Grip Primer",
    "Gripping gel primer, fragrance-free, budget pick.",
    "A sticky hydrating gel rather than a silicone blur — better if your makeup slides off rather than creases. Water-based and light, popular with acne-prone users.",
    ["Glycerin"], "elf Power Grip primer"),
   ("Smashbox Photo Finish Pore Minimizing",
    "Silicone primer that blurs pores; check for sensitivities.",
    "The classic pore-blurring primer. Run the current formula through the checker — some Photo Finish variants contain botanical extracts that sensitive skin may not love.",
    ["Dimethicone"], "Smashbox Photo Finish pore minimizing primer"),
   ("Paula's Choice Pore-Reducing Primer",
    "Mattifying, fragrance-free, from a non-comedogenic-focused brand.",
    "From a brand that publishes full ingredient rationales for every product — the transparency pick. Mattifying without a heavy silicone feel.",
    ["Niacinamide"], "Paulas Choice pore reducing primer"),
   ("NYX Pore Filler Primer",
    "Affordable pore-blurring primer.",
    "Drugstore blurring primer that performs close to premium versions. Contains dimethicone-family silicones; low clogging risk for most skin.",
    ["Dimethicone"], "NYX pore filler primer")]),

 dict(slug="non-comedogenic-oils", typ="oils",
  h1="Non-Comedogenic Oils: Which Face Oils Are Safe for Acne?",
  desc="Which face oils won't clog pores? Comedogenic ratings for popular face oils, plus the safest non-comedogenic picks for acne-prone skin.",
  intro="Not all face oils clog pores. Some sit low on the comedogenic scale and can suit acne-prone skin. Here are the safest oils and the ones to avoid.",
  avoid=["Coconut Oil","Wheat Germ Oil","Flaxseed Oil","Cocoa Butter"],
  lookfor=["Hemp Seed Oil","Argan Oil","Squalane","Rosehip Oil","Sunflower Oil"],
  picks=[
   ("The Ordinary 100% Plant-Derived Squalane",
    "Squalane (rating 1) — lightweight, one of the most acne-safe oils.",
    "Squalane is a saturated, stable emollient rather than a true plant oil — which is why it's so unlikely to clog pores or oxidize. The closest thing to a universally safe facial oil.",
    ["Squalane"], "The Ordinary squalane oil"),
   ("Nutiva Organic Hemp Seed Oil",
    "Hemp seed oil (rating 0) — high in linoleic acid, very acne-safe.",
    "Acne-prone skin tends to be low in linoleic acid, and hemp seed oil is one of the richest sources — a rare case where an oil may actively help. Buy cold-pressed and refrigerate; it oxidizes faster than most.",
    ["Hemp Seed Oil"], "organic hemp seed oil cold pressed"),
   ("Pure Argan Oil",
    "Argan oil (rating 0) — nourishing and non-comedogenic.",
    "Balanced oleic/linoleic profile and rated 0 — a richer feel than squalane for dry, acne-prone skin. Look for 100% pure, cold-pressed argan with nothing else in the bottle.",
    ["Argan Oil"], "100% pure argan oil"),
   ("The Ordinary 100% Organic Cold-Pressed Rose Hip Seed Oil",
    "Rosehip oil (rating 1) — good for scarring and tone.",
    "High in linoleic acid plus naturally occurring trans-retinoic acid — often chosen for post-acne marks. It's delicate: keep it away from heat and use it up within a few months of opening.",
    ["Rosehip Oil"], "The Ordinary rosehip seed oil"),
   ("Cold-Pressed Sunflower Seed Oil",
    "Sunflower oil (rating 0) — light and high in linoleic acid.",
    "The budget linoleic-acid option and a common base in barrier-repair formulas. Cosmetic-grade, cold-pressed versions are best for skin use.",
    ["Sunflower Oil"], "cold pressed sunflower seed oil skincare")]),

 dict(slug="non-comedogenic-hair-products", typ="hair products",
  h1="Non-Comedogenic Hair Products to Stop Hairline &amp; Back Acne",
  desc="Non-comedogenic hair products to stop hairline, forehead and back acne: sulfate-light, fungal-acne-aware shampoos and conditioners.",
  intro="Hair products are a common cause of forehead, hairline and back breakouts (often fungal too). Non-comedogenic, sulfate-light shampoos and conditioners help.",
  avoid=["Coconut Oil","Isopropyl Myristate","Lauric Acid"],
  lookfor=["Glycerin","Niacinamide","Salicylic Acid"],
  picks=[
   ("Vanicream Free & Clear Shampoo",
    "Free of fragrance, sulfates and common pore-cloggers.",
    "The elimination-diet shampoo: no fragrance, no botanicals, no common cloggers. If hairline or back acne clears after switching, your old shampoo was likely the culprit.",
    ["Glycerin"], "Vanicream Free and Clear shampoo"),
   ("Neutrogena T/Sal Shampoo",
    "Salicylic-acid shampoo helpful for scalp build-up.",
    "3% salicylic acid dissolves scalp build-up that migrates to the hairline. Use 1–2× a week alongside a gentle daily shampoo.",
    ["Salicylic Acid"], "Neutrogena T Sal shampoo salicylic acid"),
   ("Nizoral Anti-Dandruff Shampoo",
    "Ketoconazole — useful when fungal acne is involved.",
    "Ketoconazole 1% is antifungal — if your 'back acne' is actually Malassezia folliculitis (small, itchy, uniform bumps), this used as a short-contact wash is one of the most effective over-the-counter options. See our fungal acne guide.",
    [], "Nizoral anti dandruff shampoo ketoconazole"),
   ("Free & Clear Conditioner",
    "Low-irritant conditioner that rinses clean.",
    "Conditioner is the usual back-acne culprit because it coats skin as it rinses. This one skips the heavy quats, oils and fragrance — and tie your hair up after conditioning.",
    ["Glycerin"], "Free and Clear conditioner"),
   ("The Inkey List Salicylic Acid Scalp Treatment",
    "Targets scalp build-up that can clog the hairline.",
    "A leave-on BHA for the scalp line — helpful if breakouts hug your hairline. Keep it on the scalp side, not the face.",
    ["Salicylic Acid"], "The Inkey List salicylic acid scalp treatment")]),
]

def pill_safe(): return '<span class="pill safe">Screened pick</span>'

# Resolve ingredient display names to REAL db.json slugs (by name, then alias).
_DB = json.load(open("db.json", encoding="utf-8"))
_slug_by_key = {}
for _e in _DB:
    _slug_by_key[_e["n"].lower()] = _e["s"]
    for _a in _e["a"]:
        _slug_by_key.setdefault(_a, _e["s"])

def slug_for_ing(n, fatal=True):
    key = n.lower().strip()
    if key not in _slug_by_key:
        if fatal:
            raise SystemExit(f"FATAL: ingredient '{n}' not found in db.json (name or alias) — fix PAGES.")
        return None
    return _slug_by_key[key]

NEWSLETTER = """
  <section class="card" style="background:#fff7f4;border-color:#f3d8cf">
    <h2 style="margin-top:0">Get the free Acne-Safe Cheat Sheet (PDF)</h2>
    <p class="muted">All red-flag ingredients rated 4–5, safe swaps per category and the fungal-acne quick list — plus occasional new ingredient guides by email. No spam.</p>
    <form class="row" onsubmit="return acsSubscribe(event)">
      <input class="search" style="flex:1;min-width:220px" type="email" name="email" placeholder="you@email.com" required>
      <button class="btn-primary" type="submit">Send me the cheat sheet</button>
    </form>
    <p id="acsMsg" class="muted" style="font-size:13px;margin:8px 0 0"></p>
  </section>
  <script>
  function acsTrack(n){try{if(navigator.sendBeacon)navigator.sendBeacon('/api/event?e='+encodeURIComponent(n));else fetch('/api/event?e='+n,{keepalive:true});}catch(_){}}
  function acsSubscribe(e){e.preventDefault();var f=e.target,email=f.email.value,m=document.getElementById('acsMsg');m.textContent="Subscribing…";acsTrack('subscribe_attempt');
    fetch("/api/subscribe",{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email:email,list:'newsletter'})})
      .then(r=>r.json()).then(d=>{
        if(d.ok){acsTrack('subscribe_ok');f.reset();m.innerHTML="You're in — thanks! Here's your <a href=\\"/downloads/acne-safe-cheat-sheet.pdf\\" onclick=\\"acsTrack('cheatsheet_download')\\"><strong>Acne-Safe Cheat Sheet (PDF)</strong></a>.";}
        else if(d.configured===false){acsTrack('subscribe_fail');m.textContent="Signups aren't live just yet — please check back soon.";}
        else{acsTrack('subscribe_fail');m.textContent="Hmm, that didn't work — please try again.";}})
      .catch(()=>{acsTrack('subscribe_fail');m.textContent="Something went wrong, please try again.";});
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
    <a href="/">Checker</a>
    <a href="/fungal-acne-safe-checker.html">Fungal acne</a>
    <a href="/comedogenic-ingredients-list.html">Ingredient list</a>
    <a href="/about.html">About</a>
  </nav>
</div></header>

<main class="wrap">
  <section class="hero">
    <h1>{h1}</h1>
    <p>{intro}</p>
  </section>

  <div class="disclaimer" style="margin-top:0"><strong>How we choose:</strong> picks are screened against our <a href="/comedogenic-ingredients-list.html">550+ ingredient comedogenic database</a> for pore-clogging ingredients, favouring fragrance-free formulas with published ingredient lists. Formulas change, so every pick links to a live ingredient analysis you can run yourself before buying. Some links are affiliate links — if you buy through them we may earn a small commission at no extra cost to you. Informational only, not medical advice. Last reviewed {mod_human}.</div>

  <section class="prose">
    <h2>What to look for</h2>
    <p>Acne-safe {typ} formulas tend to be built around low-comedogenic ingredients such as {lookfor}. Use our <a href="/">comedogenic ingredient checker</a> to paste any product's list and confirm before you buy.</p>
    <h2>Ingredients to avoid</h2>
    <p>Be cautious with higher-rated pore-cloggers like {avoid}. One of these near the top of the ingredient list is a red flag for breakout-prone skin.</p>
  </section>

  <h2>Top non-comedogenic {typ} picks</h2>
  {picks}

  {newsletter}

  <section class="prose">
    <h2>FAQ</h2>
    <h3>Does "non-comedogenic" actually mean anything?</h3>
    <p>It usually means rated 0 on the comedogenic scale, but it isn't a regulated term — a product can be labelled non-comedogenic and still contain a pore-clogger. That's why we check the real ingredient list. Learn more on <a href="/comedogenic.html">what comedogenic means</a>.</p>
    <h3>How do I check a product myself?</h3>
    <p>Paste the ingredient list into our <a href="/">checker</a> — it flags every pore-clogging ingredient, ranks it 0–5, and marks fungal-acne triggers. Or use the <a href="/product-checker.html">product search</a> to look a product up by name.</p>
    <h3>A pick broke me out — does that mean the list is wrong?</h3>
    <p>Not necessarily. Comedogenic ratings are risk signals, not guarantees: concentration, the full formula and your individual skin all matter, and purging from actives can look like a breakout. Patch test new products on one area for 1–2 weeks before full-face use.</p>
  </section>
</main>

<footer><div class="wrap">
  More guides: <a href="/non-comedogenic/non-comedogenic-moisturizer.html">Moisturizers</a> · <a href="/non-comedogenic/non-comedogenic-sunscreen.html">Sunscreens</a> · <a href="/non-comedogenic/non-comedogenic-cleanser.html">Cleansers</a> · <a href="/non-comedogenic/non-comedogenic-foundation.html">Foundations</a> · <a href="/non-comedogenic/non-comedogenic-concealer.html">Concealers</a> · <a href="/non-comedogenic/non-comedogenic-primer.html">Primers</a> · <a href="/non-comedogenic/non-comedogenic-oils.html">Face oils</a> · <a href="/non-comedogenic/non-comedogenic-hair-products.html">Hair products</a><br>
  AcneSafeCheck · <a href="/comedogenic-ingredients-list.html">Ingredient database</a> · <a href="/">Comedogenic checker</a> · <a href="/about.html">About</a><br>
  Affiliate links help keep AcneSafeCheck free. Informational only, not medical advice.
</div></footer>
</body>
</html>
"""

def esc(s): return html.escape(s, quote=True)

def singular(typ):
    special = {"oils": "a face oil", "hair products": "a hair product"}
    if typ in special: return special[typ]
    return ("an " if typ[0] in "aeiou" else "a ") + typ

def key_links(keys):
    out = []
    for k in keys:
        s = slug_for_ing(k, fatal=False)
        if s: out.append(f'<a href="/ingredient/{s}.html">{esc(k)}</a>')
    return out

def build_jsonld(slug, typ, h1_plain, desc, picks):
    url = f"https://acnesafecheck.com/non-comedogenic/{slug}.html"
    graph = [
        {"@type": "Article", "@id": url + "#article",
         "headline": h1_plain,
         "description": desc,
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
             {"@type": "ListItem", "position": i + 1, "name": p[0], "url": f"{url}#{anchor(p[0])}"}
             for i, p in enumerate(picks)]},
        {"@type": "FAQPage", "@id": url + "#faq", "mainEntity": [
            {"@type": "Question", "name": "Does \"non-comedogenic\" actually mean anything?",
             "acceptedAnswer": {"@type": "Answer", "text": "It usually means rated 0 on the comedogenic scale, but it isn't a regulated term — a product can be labelled non-comedogenic and still contain a pore-clogger. That's why we check the real ingredient list."}},
            {"@type": "Question", "name": f"How do I check {singular(typ)} for pore-clogging ingredients?",
             "acceptedAnswer": {"@type": "Answer", "text": "Paste the ingredient list into the free AcneSafeCheck comedogenic ingredient checker at https://acnesafecheck.com/ — it flags every pore-clogging ingredient, ranks it 0–5 on the comedogenicity scale, and marks fungal-acne triggers."}}]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://acnesafecheck.com/"},
            {"@type": "ListItem", "position": 2, "name": typ.capitalize(), "item": url}]},
    ]
    return ('<script type="application/ld+json">\n'
            + json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)
            + '\n</script>')

for page in PAGES:
    slug, typ, h1, desc, intro = page["slug"], page["typ"], page["h1"], page["desc"], page["intro"]
    lookfor_links = ', '.join(f'<a href="/ingredient/{slug_for_ing(x)}.html">{esc(x)}</a>' for x in page["lookfor"])
    avoid_links = ', '.join(f'<a href="/ingredient/{slug_for_ing(x)}.html">{esc(x)}</a>' for x in page["avoid"])
    cards = []
    for name, blurb, detail, keys, query in page["picks"]:
        kl = key_links(keys)
        key_html = ('<div class="why" style="margin-top:6px"><strong>Key ingredients:</strong> ' + ', '.join(kl) + '</div>') if kl else ''
        cards.append(
            f'<div class="flag" id="{anchor(name)}"><div><div class="name">{esc(name)}</div>'
            f'<div class="why">{esc(blurb)}</div>'
            f'<div class="why" style="margin-top:6px">{esc(detail)}</div>'
            f'{key_html}'
            f'<div style="margin-top:8px;font-size:13px;font-weight:700">'
            f'<a href="{pc_link(name)}">Analyze current ingredients →</a>'
            f' &nbsp;·&nbsp; <a href="{amz(query)}" rel="nofollow sponsored" target="_blank">Find on Amazon →</a>'
            f'</div></div>'
            f'{pill_safe()}</div>')
    picks_html = '<section class="card">' + ''.join(cards) + '</section>'
    h1_plain = html.unescape(h1).replace('&amp;','&')
    if len(desc) > 165:
        raise SystemExit(f"FATAL: meta description for {slug} is {len(desc)} chars — keep under 165.")
    jsonld = build_jsonld(slug, typ, h1_plain, desc, page["picks"])
    out = TPL.format(
        h1=h1, h1_plain=esc(h1_plain), slug=slug, typ=typ,
        intro=esc(intro), desc=esc(desc),
        lookfor=lookfor_links, avoid=avoid_links, picks=picks_html,
        jsonld=jsonld, newsletter=NEWSLETTER, ver=VER, an=AN,
        mod_human=MOD_HUMAN)
    open(f"non-comedogenic/{slug}.html","w",encoding="utf-8").write(out)
print("Generated", len(PAGES), "roundup pages")
