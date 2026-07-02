#!/usr/bin/env python3
"""Generate /article/does-<x>-cause-acne.html informational pages."""
import os, html, datetime
os.makedirs("article", exist_ok=True)
VER = '29b2213b058b3dbbe63b2ad069034fd4e718ab8b42f4f8d54431f17296323eb9'
AN = 'dTgyD+bV2xvop4os/0GghQ'
PUBLISHED = "2026-06-18"
from content_date import CONTENT_UPDATED, CONTENT_UPDATED_HUMAN
MODIFIED = CONTENT_UPDATED
MOD_HUMAN = CONTENT_UPDATED_HUMAN

# slug, subject, question, verdict_label, paragraphs[], what_to_do[]
ARTICLES = [
 ("does-creatine-cause-acne","creatine","Does creatine cause acne?","Probably not directly",
  ["Creatine is one of the most studied supplements in sport, and there is <strong>no solid evidence that it directly causes acne</strong>. The theory people worry about is that creatine may slightly raise DHT (a potent androgen) — one small study in rugby players found a rise — and androgens can drive oil production and breakouts. But that single finding hasn't been clearly replicated, and most users never notice a skin change.",
   "Where creatine does get blamed unfairly is the company it keeps: heavy training, sweaty skin left unwashed, and whey protein taken alongside it. Those factors are far more likely culprits than the creatine molecule itself."],
  ["Shower and cleanse soon after training, before sweat dries on the skin.",
   "If you also use whey protein, trial cutting it for 4–6 weeks to see if your skin changes.",
   "Keep the rest of your routine non-comedogenic — paste your products into our <a href=\"/comedogenic-ingredient-checker.html\">checker</a>."]),

 ("does-dairy-cause-acne","dairy","Does dairy cause acne?","Possibly — especially skim milk",
  ["Of all the diet–acne links, dairy has the most evidence behind it. Several large observational studies have found an association between milk intake — <strong>particularly skim milk</strong> — and acne. The leading explanation is that milk contains hormones and raises IGF-1, a growth factor that increases oil production and skin-cell turnover.",
   "The link is a statistical association, not proof that dairy causes acne in everyone, and whole milk shows a weaker signal than skim. Plenty of people drink milk with clear skin — but if you break out and consume a lot of dairy, it's a reasonable thing to test."],
  ["Try a 4–6 week reduction in milk (especially skim) and track your skin.",
   "Watch whey and milk-protein supplements too, not just drinking milk.",
   "Reintroduce slowly to see whether your skin reacts."]),

 ("does-whey-protein-cause-acne","whey protein","Does whey protein cause acne?","Possibly",
  ["Whey protein is a common breakout trigger reported by gym-goers, and there is some support for it. Whey strongly raises IGF-1 and insulin, both of which can increase sebum and contribute to acne. Several case reports describe acne improving after stopping whey.",
   "The evidence is limited and individual — many people use whey with no skin issues. If you started breaking out after adding whey, it's one of the easier things to test by elimination."],
  ["Pause whey for 4–6 weeks and watch your skin.",
   "Consider a plant-based protein as a swap during the test.",
   "Keep training hygiene tight: cleanse after workouts."]),

 ("does-sugar-cause-acne","sugar","Does sugar cause acne?","Likely a contributing factor",
  ["This one has reasonable science behind it. Diets high in <strong>high-glycemic</strong> foods — sugar, white bread, sugary drinks — spike blood sugar and insulin, which raises IGF-1 and androgen activity and can worsen acne. Randomised studies of low-glycemic diets have shown improvements in acne.",
   "Sugar isn't the sole cause of acne, and a single dessert won't break you out. But a consistently high-sugar, high-glycemic diet is a plausible aggravator worth addressing alongside your skincare."],
  ["Shift toward lower-glycemic foods (whole grains, protein, vegetables).",
   "Cut back on sugary drinks first — they're the biggest, easiest win.",
   "Give dietary changes 8–12 weeks; skin is slow to respond."]),

 ("does-chocolate-cause-acne","chocolate","Does chocolate cause acne?","Weak and mixed evidence",
  ["The classic 'chocolate causes acne' claim is mostly <strong>not well supported</strong>. A few small studies have suggested that high-cacao dark chocolate might worsen acne in some prone individuals, but the results are mixed and the studies are small.",
   "With milk chocolate, the sugar and dairy are more likely to matter than the cocoa itself — which loops back to the better-evidenced sugar and dairy links. So chocolate's reputation may largely be guilt by association."],
  ["If you suspect chocolate, note whether it's the dairy/sugar version.",
   "Test by reducing it for a few weeks and tracking breakouts.",
   "Focus diet efforts on overall sugar and dairy, which have stronger evidence."]),

 ("does-stress-cause-acne","stress","Does stress cause acne?","Yes — a real aggravator",
  ["Stress doesn't create acne from nothing, but it clearly <strong>worsens</strong> it. Stress raises cortisol and other hormones that increase inflammation and oil production, and studies in students show acne flaring during high-stress exam periods. Stress also makes people pick at their skin and neglect their routine.",
   "So while stress isn't the root cause, managing it is a legitimate part of getting acne under control."],
  ["Build in stress-reduction you'll actually keep up (sleep, exercise, downtime).",
   "Don't abandon your routine when busy — that's when flares happen.",
   "Avoid picking; it turns a flare into scarring."]),

 ("does-sweat-cause-acne","sweat","Does sweat cause acne?","Indirectly, if it's left on the skin",
  ["Sweat itself doesn't cause acne, but <strong>trapped sweat</strong> can. When sweat mixes with oil, bacteria and friction from tight clothing, hats or helmets and is left to sit, it can clog follicles and trigger breakouts (sometimes called 'acne mechanica'). This is why back, chest and forehead breakouts are common in athletes.",
   "The fix isn't to sweat less — it's to not let it linger."],
  ["Cleanse skin (or at least rinse) soon after sweating.",
   "Wear breathable fabrics; wash gym clothes, hats and pillowcases often.",
   "Use a non-comedogenic body wash or salicylic-acid wash for body acne."]),

 ("does-coffee-cause-acne","coffee","Does coffee cause acne?","Probably not directly",
  ["There's <strong>no good evidence that coffee directly causes acne</strong>. Caffeine can raise cortisol, especially in large amounts or with poor sleep, which could theoretically aggravate skin — but this is speculative. More often, the milk and sugar people add to coffee are the relevant variables, both of which have better-established links to acne.",
   "Black coffee in normal amounts is very unlikely to be your acne trigger."],
  ["If you suspect coffee, look at what you add to it first.",
   "Keep caffeine moderate if it's harming your sleep — poor sleep affects skin.",
   "Stay hydrated through the day."]),

 ("does-biotin-cause-acne","biotin","Does biotin cause acne?","Possibly at high supplement doses",
  ["Biotin (vitamin B7) is widely taken for hair and nails, and <strong>high-dose biotin supplements are anecdotally linked to breakouts</strong>. The proposed mechanism is that large amounts of biotin may compete with pantothenic acid (B5) for absorption, and B5 is involved in skin health. The evidence is limited and mostly anecdotal.",
   "Biotin from food is not a concern; this is about mega-dose supplements (often 5,000–10,000 mcg)."],
  ["If you started a biotin supplement and then broke out, trial stopping it.",
   "You rarely need high-dose biotin unless a doctor advised it.",
   "Reassess all new supplements when troubleshooting acne."]),

 ("does-nicotine-cause-acne","nicotine and vaping","Does nicotine or vaping cause acne?","Unclear — possible",
  ["The evidence here is <strong>limited and mixed</strong>. Smoking has been linked in some studies to a specific type of acne (and clearly to skin ageing), while other studies find no link with inflammatory acne. Nicotine constricts blood vessels and affects healing, which could plausibly affect skin. Vaping is too new for solid acne data.",
   "What's clearer is that nicotine harms skin healing and ageing overall, so it's worth avoiding for skin reasons beyond acne."],
  ["If you vape or smoke, treat quitting as a skin-health win regardless of acne.",
   "Keep the rest of your routine non-comedogenic while you assess.",
   "See a dermatologist if breakouts are severe or scarring."]),

 ("does-masturbation-cause-acne","masturbation","Does masturbation cause acne?","No — this is a myth",
  ["This is a persistent myth with <strong>no scientific basis</strong>. Masturbation and sex do not cause acne. The idea comes from old beliefs linking sexual activity to hormone surges, but there's no evidence that normal sexual activity changes the androgen levels that drive acne in any meaningful way.",
   "Acne is driven by genetics, hormones (like normal puberty), oil, clogged pores and bacteria — not by masturbation."],
  ["Ignore this myth and focus on proven factors: routine, hormones, diet.",
   "If acne is bothering you, a consistent non-comedogenic routine matters far more.",
   "See a dermatologist for persistent or severe acne."]),

 ("does-milk-cause-acne","milk","Does milk cause acne?","Possibly — skim milk has the strongest link",
  ["Milk shows up repeatedly in acne research. Observational studies link higher milk intake — <strong>especially skim milk</strong> — with more acne, likely because milk raises IGF-1 and carries hormones that increase oil production. Skim milk shows a stronger association than whole milk, possibly due to processing and added proteins.",
   "It's an association, not a guarantee, and many people drink milk with clear skin. But if you're prone to acne and drink a lot of milk, it's a sensible thing to test."],
  ["Trial reducing milk (especially skim) for 4–6 weeks.",
   "Check whey and milk-protein supplements too.",
   "Reintroduce gradually and watch your skin."]),
]

# Per-article depth: extra "what the research says" paragraphs, a bottom line,
# and real, checkable sources. Evidence strength is described honestly.
EXTRA = {
 "does-creatine-cause-acne": {
   "how": ["The one study people cite is a 2009 trial in college rugby players (van der Merwe et al.) that found creatine loading raised DHT — an androgen — by around 50%. Higher androgens <em>can</em> increase sebum, which is why the concern exists. But that study measured hormones, not acne, and the DHT finding has not been clearly replicated. No trial has shown creatine causing breakouts.",
     "It is also worth separating the supplement from the lifestyle. People who load creatine are usually training hard, sweating into unwashed skin, and often stacking whey protein — all of which have clearer links to breakouts than creatine itself."],
   "bottom": "There is no direct evidence that creatine causes acne. If your skin changed after starting it, look first at training hygiene and any whey protein you take alongside it.",
   "sources": [("van der Merwe J, et al. Three weeks of creatine monohydrate supplementation affects dihydrotestosterone to testosterone ratio. Clin J Sport Med. 2009.", "")] },
 "does-dairy-cause-acne": {
   "how": ["The strongest data come from large observational studies. Adebamowo et al. (Harvard, 2005–2008) found teenagers who drank more milk — especially skim — reported more acne, and a 2018 meta-analysis in <em>Nutrients</em> (Juhl et al., ~78,000 people) confirmed a dose-related association across milk, low-fat and skim milk.",
     "Mechanistically, milk raises IGF-1 and insulin and carries bioactive hormones, all of which can push up sebum production and the skin-cell turnover that blocks pores. Why skim shows a stronger signal than whole milk is still debated — added whey proteins and processing are the leading suspects."],
   "bottom": "Dairy — skim milk in particular — has the most consistent evidence of any dietary acne trigger. It's an association, not a guarantee, but a 4–6 week reduction is a reasonable, low-risk experiment if you're breaking out.",
   "sources": [("Adebamowo CA, et al. Milk consumption and acne in adolescent girls. Dermatol Online J. 2006.", ""),
     ("Juhl CR, et al. Dairy intake and acne vulgaris: a meta-analysis of 78,529 subjects. Nutrients. 2018.", "")] },
 "does-whey-protein-cause-acne": {
   "how": ["The case for whey is built on case series rather than large trials. Several reports (e.g. Simonart, <em>Dermatology</em> 2012; Pontes et al. 2013) describe acne appearing after starting whey and improving after stopping it, often in young male gym-goers.",
     "The proposed mechanism is the same as milk's: whey strongly raises insulin and IGF-1, which increase sebum and follicular activity. Because the evidence is largely anecdotal, the cleanest test is elimination — stop for a few weeks and watch."],
   "bottom": "Whey is a plausible trigger for some people, especially if breakouts started after you added it. The evidence is limited, so test it by elimination rather than assuming.",
   "sources": [("Simonart T. Acne and whey protein supplementation among bodybuilders. Dermatology. 2012.", ""),
     ("Pontes T de C, et al. Incidence of acne vulgaris in young adults using protein-calorie supplements. An Bras Dermatol. 2013.", "")] },
 "does-sugar-cause-acne": {
   "how": ["This is one of the better-evidenced diet links. Randomised controlled trials of low-glycemic-load diets — notably Smith et al. (<em>Am J Clin Nutr</em>, 2007) — have shown measurable improvements in acne compared with high-glycemic diets.",
     "High-glycemic foods spike blood glucose and insulin, which raises IGF-1 and androgen activity and drives sebum. It's the overall glycemic load of the diet that matters, not a single sugary treat."],
   "bottom": "A consistently high-sugar, high-glycemic diet is a credible aggravator of acne, backed by randomised trials. Cutting sugary drinks first is the biggest, easiest win.",
   "sources": [("Smith RN, et al. A low-glycemic-load diet improves symptoms in acne vulgaris patients: a randomized controlled trial. Am J Clin Nutr. 2007.", "")] },
 "does-chocolate-cause-acne": {
   "how": ["Controlled studies are small and mixed. A 2016 trial (Vongraviopap &amp; Asawanonda) found high-dose dark chocolate worsened acne in prone men, while older work found little effect — and the studies are too small to settle it.",
     "With milk chocolate, the sugar and dairy are the more likely culprits, both of which have stronger evidence than cocoa itself. So chocolate's reputation is partly guilt by association."],
   "bottom": "The pure-chocolate link is weak and unsettled. If you suspect it, look at whether it's the sugar and dairy version, and focus diet efforts there.",
   "sources": [("Vongraviopap S, Asawanonda P. Dark chocolate exacerbates acne. Int J Dermatol. 2016.", "")] },
 "does-stress-cause-acne": {
   "how": ["Stress doesn't start acne, but studies show it worsens it. Chiu et al. (<em>Arch Dermatol</em>, 2003) tracked students and found acne severity rose during high-stress exam periods.",
     "Stress raises cortisol and inflammatory signalling, which can increase oil production, and it changes behaviour — more skin-picking, worse sleep and a neglected routine all feed flares."],
   "bottom": "Stress is a genuine aggravator, not a root cause. Managing it — and not abandoning your routine when busy — is a legitimate part of getting acne under control.",
   "sources": [("Chiu A, et al. The response of skin disease to stress: changes in acne vulgaris during examinations. Arch Dermatol. 2003.", "")] },
 "does-sweat-cause-acne": {
   "how": ["The relevant concept is 'acne mechanica', first described by Mills and Kligman in 1975: heat, occlusion, pressure and friction (from helmets, straps, tight synthetic clothing) combined with trapped sweat can provoke breakouts on the back, chest and forehead.",
     "Sweat itself is mostly water and salt — the problem is leaving it to sit and mix with oil and friction, not sweating in the first place."],
   "bottom": "Sweat only contributes when it's trapped against the skin. The fix isn't to sweat less — it's to rinse or cleanse soon after, and reduce friction and occlusion.",
   "sources": [("Mills OH, Kligman A. Acne mechanica. Arch Dermatol. 1975.", "")] },
 "does-coffee-cause-acne": {
   "how": ["There are no studies showing coffee causes acne. The theoretical worry is that caffeine can nudge cortisol up, especially with poor sleep, which could in principle aggravate skin — but this is speculative, not demonstrated.",
     "In practice the milk and sugar people add to coffee are the variables with real evidence behind them, not the coffee itself."],
   "bottom": "Black coffee in normal amounts is very unlikely to be your acne trigger. If you suspect your coffee, look at what you add to it first.",
   "sources": [] },
 "does-biotin-cause-acne": {
   "how": ["There are no clinical trials linking biotin to acne; the connection is anecdotal. The commonly repeated mechanism — that high-dose biotin competes with vitamin B5 (pantothenic acid) for absorption — is a hypothesis, not an established finding.",
     "What's clearer is that you rarely need mega-dose biotin (5,000–10,000 mcg) unless a doctor advised it, and biotin from food is not a concern."],
   "bottom": "The biotin–acne link is anecdotal and tied to high-dose supplements. If you started one and then broke out, trialling stopping it is harmless and worth doing.",
   "sources": [] },
 "does-nicotine-cause-acne": {
   "how": ["Evidence is mixed. Some studies (e.g. Schäfer et al., 2001) report an association between smoking and a non-inflammatory comedonal acne, while others find no link with typical inflammatory acne. Nicotine constricts blood vessels and impairs healing, which could plausibly affect skin.",
     "Vaping is too new to have solid acne data either way."],
   "bottom": "The acne evidence is unclear, but nicotine clearly harms skin healing and ageing — reason enough to quit for skin's sake, regardless of acne.",
   "sources": [("Schäfer T, et al. Epidemiology of acne in the general population: smoking. Br J Dermatol. 2001.", "")] },
 "does-masturbation-cause-acne": {
   "how": ["This myth has no scientific basis. There is no evidence that masturbation or sex changes the androgen levels that drive acne in any meaningful or lasting way.",
     "Acne is driven by genetics, normal hormonal changes (such as puberty), excess oil, clogged pores and bacteria — none of which are affected by masturbation."],
   "bottom": "Masturbation does not cause acne. Ignore the myth and focus on the factors that actually matter: a consistent routine, hormones and diet.",
   "sources": [] },
 "does-milk-cause-acne": {
   "how": ["Milk is the most-studied dietary link. Observational studies (Adebamowo et al.) and a 2018 meta-analysis (Juhl et al., ~78,000 people) repeatedly associate higher milk intake — especially skim — with more acne.",
     "Milk raises IGF-1 and carries hormones that increase sebum; skim shows a stronger association than whole milk, likely due to processing and added proteins."],
   "bottom": "Milk — skim in particular — has the strongest evidence of any single food. It's an association, not a certainty, so test a 4–6 week reduction if you're prone to breakouts.",
   "sources": [("Adebamowo CA, et al. Milk consumption and acne in teenagers. Dermatol Online J. 2006.", ""),
     ("Juhl CR, et al. Dairy intake and acne vulgaris: a meta-analysis. Nutrients. 2018.", "")] },
}

TPL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{q} The Evidence | AcneSafeCheck</title>
<meta name="description" content="{q} {verdict}. We look at what the research actually says about {subj} and acne, and what to do about it.">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#e0654f">
<meta name="ahrefs-site-verification" content="{ver}">
<script src="https://analytics.ahrefs.com/analytics.js" data-key="{an}" async></script>
<link rel="canonical" href="https://acnesafecheck.com/article/{slug}.html">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta property="og:title" content="{q}">
<meta property="og:description" content="{verdict}. What the evidence says about {subj} and acne.">
<meta property="og:type" content="article">
<meta property="og:url" content="https://acnesafecheck.com/article/{slug}.html">
<meta property="og:image" content="https://acnesafecheck.com/og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://acnesafecheck.com/og.png">
<link rel="stylesheet" href="/styles.css">
<script type="application/ld+json">
{{"@context":"https://schema.org","@graph":[
{{"@type":"Article","@id":"https://acnesafecheck.com/article/{slug}.html#article","headline":"{q}","description":"{verdict}. What the evidence says about {subj} and acne.","url":"https://acnesafecheck.com/article/{slug}.html","datePublished":"{pub}","dateModified":"{mod}","inLanguage":"en","author":{{"@type":"Person","@id":"https://acnesafecheck.com/#mitchell","name":"Mitchell Zandwijken","url":"https://acnesafecheck.com/about.html"}},"publisher":{{"@type":"Organization","@id":"https://acnesafecheck.com/#org","name":"AcneSafeCheck","logo":{{"@type":"ImageObject","url":"https://acnesafecheck.com/icon-512.png"}}}},"image":{{"@type":"ImageObject","url":"https://acnesafecheck.com/og.png","width":1200,"height":630}},"mainEntityOfPage":{{"@type":"WebPage","@id":"https://acnesafecheck.com/article/{slug}.html"}}}},
{{"@type":"FAQPage","@id":"https://acnesafecheck.com/article/{slug}.html#faq","mainEntity":[{{"@type":"Question","name":"{q}","acceptedAnswer":{{"@type":"Answer","text":"{verdict}. {answer_plain}"}}}}]}},
{{"@type":"BreadcrumbList","itemListElement":[
{{"@type":"ListItem","position":1,"name":"Home","item":"https://acnesafecheck.com/"}},
{{"@type":"ListItem","position":2,"name":"Does X cause acne?","item":"https://acnesafecheck.com/acne-causes.html"}},
{{"@type":"ListItem","position":3,"name":"{q}","item":"https://acnesafecheck.com/article/{slug}.html"}}]}}]}}
</script>
</head>
<body>
<header><div class="wrap bar">
  <a class="logo" href="/"><span class="dot"></span> AcneSafeCheck</a>
  <nav>
    <a href="/comedogenic-ingredient-checker.html">Comedogenic checker</a>
    <a href="/fungal-acne-safe-checker.html">Fungal acne</a>
    <a href="/comedogenic-ingredients-list.html">Ingredient list</a>
    <a href="/about.html">About</a>
  </nav>
</div></header>

<main class="wrap">
  <section class="hero">
    <h1>{q}</h1>
    <p><strong>Short answer: {verdict}.</strong></p>
  </section>
  <section class="prose">
    {paras}
    <h2>What the research says</h2>
    {how}
    <h2>What you can do</h2>
    <ul>{todo}</ul>
    <h2>Bottom line</h2>
    <p>{bottom}</p>
    <h2>Vet your skincare too</h2>
    <p>Diet is only one piece. Many breakouts are driven by what you put <em>on</em> your skin. Paste your products into our <a href="/comedogenic-ingredient-checker.html">comedogenic ingredient checker</a> to rule out pore-clogging ingredients, and check for <a href="/fungal-acne-safe-checker.html">fungal-acne triggers</a> if your bumps are small and itchy.</p>
    {sources}
    <p class="muted" style="font-size:13px">By <a href="/about.html">Mitchell Zandwijken</a> · Last updated {mod_human}. See our <a href="/about.html">sources &amp; methodology</a>.</p>
  </section>
  <div class="disclaimer"><strong>Note:</strong> This is general educational information, not medical advice, and the diet–acne research is still evolving. For persistent or severe acne, see a dermatologist.</div>
</main>

<footer><div class="wrap">
  AcneSafeCheck · <a href="/comedogenic-ingredient-checker.html">Comedogenic checker</a> · <a href="/comedogenic-ingredients-list.html">Ingredient database</a> · <a href="/about.html">About</a><br>
  Informational only, not medical advice.
</div></footer>
</body>
</html>
"""

import re
def strip_tags(s): return re.sub('<[^>]+>','',s)

def clean_answer(text, limit=320):
    """Sentence-bounded summary for FAQ schema — never cuts off mid-word."""
    t = strip_tags(text).replace('"', "'").strip()
    if len(t) <= limit:
        return t
    cut = t[:limit]
    end = max(cut.rfind('. '), cut.rfind('! '), cut.rfind('? '))
    return (cut[:end+1] if end > 60 else cut[:cut.rfind(' ')]).strip()

for slug, subj, q, verdict, paras, todo in ARTICLES:
    ex = EXTRA.get(slug, {})
    paras_html = ''.join(f'<p>{p}</p>' for p in paras)
    how_html = ''.join(f'<p>{p}</p>' for p in ex.get("how", []))
    todo_html = ''.join(f'<li>{t}</li>' for t in todo)
    bottom = ex.get("bottom", "")
    src = ex.get("sources", [])
    if src:
        items = ''.join(f'<li>{html.escape(strip_tags(t))}</li>' for t, _ in src)
        sources_html = ('<h2>Sources &amp; further reading</h2><ul style="font-size:14px">'
                        + items
                        + '<li><a href="https://www.aad.org/public/diseases/acne" rel="nofollow" target="_blank">American Academy of Dermatology — acne resources</a></li></ul>')
    else:
        sources_html = ('<h2>Sources &amp; further reading</h2><ul style="font-size:14px">'
                        '<li>No controlled studies establish this link; the evidence is anecdotal or theoretical and is described as such above.</li>'
                        '<li><a href="https://www.aad.org/public/diseases/acne" rel="nofollow" target="_blank">American Academy of Dermatology — acne resources</a></li></ul>')
    answer_plain = clean_answer(' '.join(strip_tags(p) for p in paras))
    page = TPL.format(slug=slug, subj=subj, q=q, verdict=verdict,
                      paras=paras_html, how=how_html, todo=todo_html,
                      bottom=html.escape(bottom), sources=sources_html,
                      answer_plain=answer_plain, pub=PUBLISHED, mod=MODIFIED,
                      mod_human=MOD_HUMAN, ver=VER, an=AN)
    open(f"article/{slug}.html","w",encoding="utf-8").write(page)

# Hub page linking all articles
cards = ''.join(
    f'<a class="tile" href="/article/{slug}.html"><b>{html.escape(q)}</b><span>{html.escape(verdict)}</span></a>'
    for slug, subj, q, verdict, paras, todo in ARTICLES)

hub_items = ','.join(
    '{"@type":"ListItem","position":%d,"name":"%s","url":"https://acnesafecheck.com/article/%s.html"}'
    % (i + 1, q.replace('"', "'"), slug)
    for i, (slug, subj, q, verdict, paras, todo) in enumerate(ARTICLES))
HUB_SCHEMA = (
 '<script type="application/ld+json">\n'
 '{"@context":"https://schema.org","@graph":['
 '{"@type":"CollectionPage","@id":"https://acnesafecheck.com/acne-causes.html#page",'
 '"name":"Does X Cause Acne? Myths & Causes, Evidence-Based",'
 '"description":"Evidence-based answers to the most-searched acne questions: does dairy, sugar, creatine, whey, stress, chocolate or coffee cause acne?",'
 '"url":"https://acnesafecheck.com/acne-causes.html","inLanguage":"en",'
 '"isPartOf":{"@id":"https://acnesafecheck.com/#site"},'
 '"publisher":{"@type":"Organization","@id":"https://acnesafecheck.com/#org","name":"AcneSafeCheck"}},'
 '{"@type":"ItemList","name":"Acne causes — article index","itemListElement":[' + hub_items + ']},'
 '{"@type":"BreadcrumbList","itemListElement":['
 '{"@type":"ListItem","position":1,"name":"Home","item":"https://acnesafecheck.com/"},'
 '{"@type":"ListItem","position":2,"name":"Does X cause acne?","item":"https://acnesafecheck.com/acne-causes.html"}]}'
 ']}\n</script>')
HUB = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Does X Cause Acne? Myths &amp; Causes, Evidence-Based | AcneSafeCheck</title>
<meta name="description" content="Evidence-based answers to the most-searched acne questions: does dairy, sugar, creatine, whey, stress, chocolate or coffee cause acne? What the research really says.">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#e0654f">
<meta name="ahrefs-site-verification" content="{VER}">
<script src="https://analytics.ahrefs.com/analytics.js" data-key="{AN}" async></script>
<link rel="canonical" href="https://acnesafecheck.com/acne-causes.html">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta property="og:title" content="Does X Cause Acne? Myths &amp; Causes">
<meta property="og:description" content="Evidence-based answers to the most-searched acne questions.">
<meta property="og:type" content="website">
<meta property="og:url" content="https://acnesafecheck.com/acne-causes.html">
<meta property="og:image" content="https://acnesafecheck.com/og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://acnesafecheck.com/og.png">
<link rel="stylesheet" href="/styles.css">
{HUB_SCHEMA}
</head>
<body>
<header><div class="wrap bar">
  <a class="logo" href="/"><span class="dot"></span> AcneSafeCheck</a>
  <nav>
    <a href="/comedogenic-ingredient-checker.html">Comedogenic checker</a>
    <a href="/fungal-acne-safe-checker.html">Fungal acne</a>
    <a href="/comedogenic-ingredients-list.html">Ingredient list</a>
    <a href="/about.html">About</a>
  </nav>
</div></header>
<main class="wrap">
  <section class="hero">
    <h1>Does X cause acne? Myths &amp; causes</h1>
    <p>Evidence-based answers to the questions people search most about acne and lifestyle — what the research actually shows, and what to do.</p>
  </section>
  <div class="cards">{cards}</div>
  <div class="disclaimer" style="margin-top:24px"><strong>Note:</strong> General educational information, not medical advice. For persistent or severe acne, see a dermatologist.</div>
</main>
<footer><div class="wrap">
  AcneSafeCheck · <a href="/comedogenic-ingredient-checker.html">Comedogenic checker</a> · <a href="/about.html">About</a><br>
  Informational only, not medical advice.
</div></footer>
</body>
</html>
"""
open("acne-causes.html","w",encoding="utf-8").write(HUB)
print("Generated", len(ARTICLES), "articles + hub")
