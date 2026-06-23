#!/usr/bin/env python3
"""Scan all .html files and emit sitemap.xml with priorities + lastmod."""
import os, glob, datetime

BASE = "https://acnesafecheck.com"

def lastmod_for(path):
    """Real per-file modified date (YYYY-MM-DD) from the filesystem."""
    return datetime.date.fromtimestamp(os.path.getmtime(path)).isoformat()

urls = []
for path in glob.glob("*.html") + glob.glob("ingredient/*.html") + glob.glob("non-comedogenic/*.html") + glob.glob("article/*.html"):
    rel = path
    loc = f"{BASE}/{rel}" if "/" in rel else f"{BASE}/{rel}"
    mod = lastmod_for(path)
    # homepage handled separately
    if rel == "index.html":
        loc = f"{BASE}/"
        pri = "1.0"
    elif rel in ("comedogenic-ingredient-checker.html","pore-clogging-ingredient-checker.html"):
        pri = "0.9"
    elif rel in ("comedogenic-ingredients-list.html","comedogenic.html"):
        pri = "0.8"
    elif rel.startswith("ingredient/"):
        pri = "0.6"
    elif rel.startswith("non-comedogenic/"):
        pri = "0.7"
    elif rel.startswith("article/"):
        pri = "0.6"
    else:
        pri = "0.5"
    urls.append((loc, pri, mod))

urls.sort(key=lambda x: (-float(x[1]), x[0]))
out = ['<?xml version="1.0" encoding="UTF-8"?>',
       '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for loc, pri, mod in urls:
    out.append(f'  <url><loc>{loc}</loc><lastmod>{mod}</lastmod><priority>{pri}</priority></url>')
out.append('</urlset>')
open("sitemap.xml", "w", encoding="utf-8").write("\n".join(out) + "\n")
print("Sitemap:", len(urls), "URLs")
