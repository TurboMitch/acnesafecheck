#!/usr/bin/env python3
"""Scan all .html files and emit sitemap.xml with priorities + lastmod.

lastmod comes from each file's last git commit date, so a fresh clone or CI
rebuild doesn't reset every date (file mtime did). Files with uncommitted
changes — i.e. genuinely just modified — fall back to CONTENT_UPDATED.
"""
import glob, subprocess
from content_date import CONTENT_UPDATED

BASE = "https://acnesafecheck.com"

def _git_dates():
    """One `git log` pass -> {path: last-commit-date}; empty dict if git unavailable."""
    try:
        out = subprocess.run(
            ["git", "log", "--format=%cs", "--name-only"],
            capture_output=True, text=True, check=True).stdout
    except Exception:
        return {}
    dates, cur = {}, None
    for line in out.splitlines():
        if not line.strip():
            continue
        if len(line) == 10 and line[4] == "-" and line[7] == "-":
            cur = line
        elif cur and line not in dates:
            dates[line] = cur
    return dates

def _dirty_files():
    try:
        out = subprocess.run(["git", "status", "--porcelain"],
                             capture_output=True, text=True, check=True).stdout
        return {l[3:].strip() for l in out.splitlines() if l.strip()}
    except Exception:
        return set()

GIT_DATES = _git_dates()
DIRTY = _dirty_files()

def lastmod_for(path):
    if path in DIRTY or path not in GIT_DATES:
        return CONTENT_UPDATED
    return GIT_DATES[path]

urls = []
for path in glob.glob("*.html") + glob.glob("ingredient/*.html") + glob.glob("non-comedogenic/*.html") + glob.glob("article/*.html"):
    rel = path
    loc = f"{BASE}/{rel}"
    mod = lastmod_for(path)
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
